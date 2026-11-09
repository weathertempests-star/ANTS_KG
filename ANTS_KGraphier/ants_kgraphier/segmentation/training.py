"""Supervised membership training; validation-only checkpoint selection."""
import copy
import json
from pathlib import Path
import random
import time

import torch
from torch.nn import functional as F

from ..io import jsonl, digest, write_json, canonical
from .annotations import targets, validate_splits
from .model import Selector, encode, bernoulli_kl, stochastic_mask
from .decode import decode


def load_dataset(graph_path, annotation_path, use_kg=True):
    from .dataset import Dataset
    return Dataset(graph_path, annotation_path, use_kg)


def membership_loss(logits, y, weights):
    # Balance reviewed classes within each activity. Unknowns contribute nothing.
    pieces = []
    for value in (0, 1):
        w = weights * (y == value)
        if w.sum() > 0:
            pieces.append((F.binary_cross_entropy_with_logits(logits, y, reduction='none') * w).sum() / w.sum())
    if not pieces:
        raise ValueError('no supervision')
    return torch.stack(pieces).mean()


def evaluate(model, data, budget=32, threshold=.5, device='cpu'):
    records = []
    model.eval()
    with torch.no_grad():
        for g, a, (x, edges, anchor), y, w in data:
            scores = model(x.to(device), edges.to(device), anchor).sigmoid().cpu().tolist()
            out = decode(g, scores, budget, threshold)
            selected = {e['event_id'] for e in out['events']}
            positive = {m['event_id'] for m in a['memberships'] if m['role'] in {'core', 'context'}}
            negative = {m['event_id'] for m in a['memberships'] if m['role'] == 'unrelated'}
            tp, fp = len(selected & positive), len(selected & negative)
            outside = len(a['required_outside_candidate'])
            recall = tp / (len(positive) + outside) if len(positive) + outside else None
            precision = tp / (tp + fp) if tp + fp else None
            f1 = 2 * tp / (2 * tp + fp + len(positive) - tp + outside) if positive or fp or outside else None
            context_positive = positive - {g['anchor_event_id']}
            context_tp = len(selected & context_positive)
            context_f1 = 2*context_tp/(len(context_positive)+outside+context_tp+fp) if context_positive or outside else None
            records.append(dict(graph_id=g['id'], episode_id=a['episode_id'], provenance=a['provenance'],
                                selected=len(selected), reviewed_selected=tp+fp,
                                precision=precision, recall=recall, f1=f1, context_f1=context_f1,
                                reviewed_context_positives=len(context_positive),
                                candidate_recall=len(positive)/(len(positive)+outside) if positive or outside else None))
    # Average anchors within an episode before macro averaging episodes.
    episodes = {}
    for row in records:
        episodes.setdefault(row['episode_id'], []).append(row)
    means = {}
    for key in ('precision', 'recall', 'f1', 'candidate_recall', 'selected', 'context_f1'):
        values = []
        for rows in episodes.values():
            valid = [r[key] for r in rows if r[key] is not None]
            if valid:
                values.append(sum(valid)/len(valid))
        means['macro_' + key] = sum(values)/len(values) if values else None
    return dict(metrics=means, episodes=len(episodes), graphs=len(records), records=records,
                context_supported_graphs=sum(r['reviewed_context_positives'] > 0 for r in records),
                scope='Reviewed membership only; unknown events are not negatives; context F1 excludes the mandatory anchor.')


def train(graph_path, annotation_path, output, epochs=20, seed=7, use_kg=True,
          device='cpu', budget=32, hidden=64, lr=.001, bottleneck=.001,
          selection_metric='macro_context_f1', resume=None, pretrain_epochs=0, stochastic=False):
    if epochs < 1 or budget < 1:
        raise ValueError('epochs and budget must be positive')
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    torch.manual_seed(seed)
    random.seed(seed)
    torch.set_num_threads(1)
    data = load_dataset(graph_path, annotation_path, use_kg)
    train_data = data.view('train')
    validation = data.view('validation')
    if not train_data or not validation:
        raise ValueError('reviewed train and validation examples required')
    if selection_metric not in {'macro_f1', 'macro_context_f1'}:
        raise ValueError('invalid selection metric')
    if selection_metric == 'macro_context_f1' and not any(
        any(m['role'] in {'core','context'} and m['event_id'] != g['anchor_event_id'] for m in a['memberships'])
        or a['required_outside_candidate'] for g,a,*_ in validation):
        data.close()
        raise ValueError('validation has no reviewed positive context; annotate context or explicitly use macro_f1 for a smoke experiment')
    signature = dict(graphs_sha256=digest(graph_path), annotations_sha256=digest(annotation_path),
                     hidden=hidden, use_kg=use_kg, seed=seed, budget=budget, lr=lr,
                     bottleneck=bottleneck, selection_metric=selection_metric, device=str(device),
                     pretrain_epochs=pretrain_epochs, stochastic=stochastic)
    output.mkdir(parents=True)
    model = Selector(hidden).to(device)
    from .pretrain import pretrain
    pretrain_history = pretrain(model, graph_path, pretrain_epochs if resume is None else 0, use_kg, device, lr)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    best, state, history = -1, None, []
    start_epoch = 0
    if resume is not None:
        resume = Path(resume)
        meta = json.loads(resume.with_suffix('.json').read_text())
        if digest(resume) != meta['sha256'] or meta['signature'] != signature:
            raise ValueError('resume hash, inputs, device or configuration changed')
        saved = torch.load(resume, map_location='cpu', weights_only=True)
        model.load_state_dict(saved['model'])
        optimizer.load_state_dict(saved['optimizer'])
        for values in optimizer.state.values():
            for key, value in values.items():
                if isinstance(value, torch.Tensor):
                    values[key] = value.to(device)
        start_epoch, best, state, chosen, history = saved['epoch'], saved['best'], saved['best_state'], saved['chosen'], saved['history']
        pretrain_history = saved['pretrain_history']
        random.setstate(saved['python_rng'])
        torch.set_rng_state(saved['torch_rng'])
        if saved['cuda_rng'] is not None:
            torch.cuda.set_rng_state_all(saved['cuda_rng'])
        if epochs <= start_epoch:
            raise ValueError('epochs must exceed completed checkpoint epochs')
    start = time.perf_counter()
    for epoch in range(start_epoch, epochs):
        model.train()
        train_data.indices.sort()
        random.shuffle(train_data.indices)
        losses = []
        for g, a, (x, edges, anchor), y, w in train_data:
            optimizer.zero_grad()
            logits = model(x.to(device), edges.to(device), anchor)
            supervised_logits = torch.logit(stochastic_mask(logits).clamp(1e-6,1-1e-6)) if stochastic else logits
            loss = membership_loss(supervised_logits, y.to(device), w.to(device)) + bottleneck * bernoulli_kl(logits)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.)
            optimizer.step()
            losses.append(float(loss.detach()))
        candidates = [(threshold, evaluate(model, validation, budget, threshold, device)) for threshold in (.3, .5, .7)]
        threshold, report = max(candidates, key=lambda pair: pair[1]['metrics'][selection_metric] or 0)
        score = report['metrics'][selection_metric] or 0
        history.append(dict(epoch=epoch+1, loss=sum(losses)/len(losses), validation_score=score, selection_metric=selection_metric, threshold=threshold))
        if score > best:
            best = score
            state = {k: v.detach().cpu().clone() for k,v in model.state_dict().items()}
            chosen = dict(epoch=epoch+1, threshold=threshold, validation=report)
        checkpoint = dict(epoch=epoch+1, model=model.state_dict(), optimizer=optimizer.state_dict(),
                          best=best, best_state=state, chosen=chosen, history=history,
                          python_rng=random.getstate(), torch_rng=torch.get_rng_state(),
                          cuda_rng=torch.cuda.get_rng_state_all() if str(device).startswith('cuda') else None,
                          pretrain_history=pretrain_history)
        torch.save(checkpoint, output/'last.pt.tmp')
        (output/'last.pt.tmp').replace(output/'last.pt')
        write_json(output/'last.json', dict(sha256=digest(output/'last.pt'), signature=signature))
        print(canonical(history[-1]), flush=True)
    torch.save(state, output / 'weights.pt')
    config = dict(schema='kgraphier-selector-1', hidden=hidden, use_kg=use_kg, seed=seed,
                  epochs=epochs, budget=budget, lr=lr, bottleneck=bottleneck, selection_metric=selection_metric,
                  pretrain_epochs=pretrain_epochs, stochastic=stochastic, pretrain_history=pretrain_history,
                  kg_hashes=sorted(data.kg_hashes),
                  graphs_sha256=digest(graph_path), annotations_sha256=digest(annotation_path),
                  weights_sha256=digest(output/'weights.pt'), training_graphs=len(train_data),
                  validation_graphs=len(validation), provenance=[r[0] for r in data.db.execute('SELECT DISTINCT provenance FROM examples ORDER BY provenance')],
                  seconds=time.perf_counter()-start, **chosen)
    write_json(output/'model.json', config)
    write_json(output/'history.json', history)
    data.close()
    return config


def load_model(path, device='cpu'):
    path = Path(path)
    if (path/'INVALID_RUN.txt').exists():
        raise ValueError('checkpoint marked invalid')
    config = json.loads((path/'model.json').read_text())
    if digest(path/'weights.pt') != config['weights_sha256']:
        raise ValueError('checkpoint hash mismatch')
    model = Selector(config['hidden']).to(device)
    model.load_state_dict(torch.load(path/'weights.pt', map_location=device, weights_only=True))
    model.eval()
    return model, config


def select(graph_path, model_path, output, device='cpu'):
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    model, config = load_model(model_path, device)
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output.open('x') as f, torch.no_grad():
        for g in jsonl(graph_path):
            if config.get('kg_hashes') and g.get('kg_sha256') not in config['kg_hashes']:
                raise ValueError('selector KG snapshot mismatch')
            x, edges, anchor = encode(g, config['use_kg'])
            scores = model(x.to(device), edges.to(device), anchor).sigmoid().cpu().tolist()
            out = decode(g, scores, config['budget'], config['threshold'])
            out['selector_weights_sha256'] = config['weights_sha256']
            f.write(canonical(out)+'\n')
            count += 1
    return {'graphs': count, 'sha256': digest(output)}
