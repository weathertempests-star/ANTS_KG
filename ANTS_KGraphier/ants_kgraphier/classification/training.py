"""Reproducible supervised training, frozen validation thresholds and inference."""
import json
from pathlib import Path
import random

import torch
from torch.nn import functional as F

from ..io import canonical, digest, write_json
from .data import load_dataset
from .model import Classifier, encode, positive_weights, targets, vocabulary
from .metrics import choose_thresholds, grouped_report, dependency_bootstrap


def atomic_save(value, path):
    temp = path.with_suffix('.tmp')
    torch.save(value, temp)
    temp.replace(path)
    write_json(path.with_suffix('.sha256.json'), dict(sha256=digest(path)))


def load_checkpoint(path):
    path = Path(path)
    expected = json.loads(path.with_suffix('.sha256.json').read_text())['sha256']
    if digest(path) != expected:
        raise ValueError('checkpoint integrity mismatch')
    return torch.load(path, map_location='cpu', weights_only=False)


def probabilities(model, encoded, device):
    model.eval()
    with torch.no_grad():
        return [row for start in range(0,len(encoded),32)
                for row in model.forward_batch(encoded[start:start+32]).sigmoid().cpu().tolist()]


def train(args, data=None, encodings=None):
    torch.set_num_threads(args.threads)
    torch.manual_seed(args.seed)
    random.seed(args.seed)
    if args.device.startswith('cuda'):
        torch.cuda.manual_seed_all(args.seed)
    torch.use_deterministic_algorithms(True)
    manifest_path = Path(args.data).parent/'manifest.json'
    if manifest_path.exists() and not json.loads(manifest_path.read_text()).get('validation_usable', True):
        raise ValueError('preparation reports insufficient validation classes; model selection stopped')
    if args.mode == 'prior' and args.resume:
        raise ValueError('prior baseline has no optimizer to resume')
    data = load_dataset(args.data) if data is None else data
    train_data = [(g,a) for g,a in data if g['split']=='train']
    validation = [(g,a) for g,a in data if g['split']=='validation']
    if not train_data or {a['binary'] for _,a in validation if a['binary'] is not None} != {0,1}:
        raise ValueError('training data or both validation binary classes missing; model selection stopped')
    classes = sorted({t for _,a in train_data for t in a['techniques']})
    vocab = vocabulary(train_data)
    snapshots = {g['kg_sha256'] for g,_ in data}
    if len(snapshots)!=1:
        raise ValueError('mixed KG snapshots')
    config = dict(schema='classification-model-1', torch_version=str(torch.__version__),
                  code_sha256={name: digest(Path(__file__).parent/name)
                               for name in ('model.py','training.py','metrics.py','data.py')},
                  seed=args.seed, mode=args.mode, use_kg=not args.no_kg,
                  learning_rate=.001, weight_decay=.0001, batch_size=args.batch_size,
                  patience=args.patience, device=args.device, threads=args.threads,
                  classes=classes, vocabulary=vocab, kg_sha256=next(iter(snapshots)),
                  dataset={f: digest(Path(args.data)/f) for f in ('graphs.jsonl','labels.jsonl')})
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    (output/'.building').touch()
    weights = positive_weights(train_data, classes).to(args.device)
    width = sum(map(len, vocab.values()))+1
    model = Classifier(width, len(classes), args.mode).to(args.device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=.001, weight_decay=.0001)
    start, best, stale, history = 0, -1., 0, []
    best_state = None
    thresholds = (.5,.5)
    if args.resume:
        checkpoint = load_checkpoint(args.resume)
        if checkpoint['config'] != config:
            raise ValueError('resume requires identical configuration and data hashes')
        model.load_state_dict(checkpoint['state'])
        optimizer.load_state_dict(checkpoint['optimizer'])
        start, best, stale = checkpoint['epoch'], checkpoint['best'], checkpoint['stale']
        history, thresholds, best_state = checkpoint['history'], checkpoint['thresholds'], checkpoint['best_state']
        random.setstate(checkpoint['python_rng'])
        torch.set_rng_state(checkpoint['torch_rng'])
        if checkpoint['cuda_rng'] is not None:
            torch.cuda.set_rng_state_all(checkpoint['cuda_rng'])
    if args.mode == 'prior':
        pairs = [targets(a,classes) for _,a in train_data]
        y, mask = [torch.stack([p[i] for p in pairs]) for i in range(2)]
        prior = (y*mask).sum(0)/mask.sum(0).clamp_min(1)
        predictions = [prior.tolist() for _ in validation]
        thresholds, best, insufficient = choose_thresholds(validation, predictions, classes)
        atomic_save(dict(config=config, prior=prior.tolist(), thresholds=thresholds), output/'best.pt')
        write_json(output/'model.json', dict(config=config, validation_score=best, technique_validation_insufficient=insufficient))
        (output/'.building').unlink()
        return dict(output=str(output), validation_score=best)
    if encodings is None:
        encodings = {}
    if args.no_kg not in encodings:
        encodings[args.no_kg] = ([encode(g, vocab, not args.no_kg) for g,_ in train_data],
                                  [encode(g, vocab, not args.no_kg) for g,_ in validation])
    encoded_train, encoded_val = encodings[args.no_kg]
    if start >= args.epochs:
        raise ValueError('resume epochs must exceed completed epochs')
    for epoch in range(start, args.epochs):
        if stale >= args.patience:
            break
        model.train()
        order = list(range(len(train_data)))
        random.shuffle(order)
        loss_total = 0.
        for offset in range(0,len(order),args.batch_size):
            indices = order[offset:offset+args.batch_size]
            optimizer.zero_grad()
            logits = model.forward_batch([encoded_train[i] for i in indices])
            pairs = [targets(train_data[i][1],classes) for i in indices]
            y, mask = [torch.stack([p[j] for p in pairs]).to(args.device) for j in range(2)]
            losses = F.binary_cross_entropy_with_logits(logits,y,pos_weight=weights,reduction='none')*mask
            loss = losses[:,0].sum()/mask[:,0].sum().clamp_min(1)
            if classes:
                loss = loss + losses[:,1:].sum()/mask[:,1:].sum().clamp_min(1)
            loss.backward()
            optimizer.step()
            loss_total += loss.item()*len(indices)
        predictions = probabilities(model,encoded_val,args.device)
        candidate_thresholds, score, insufficient = choose_thresholds(validation,predictions,classes)
        history.append(dict(epoch=epoch+1, loss=loss_total/len(train_data), validation_score=score,
                            thresholds=candidate_thresholds, technique_validation_insufficient=insufficient))
        if score > best:
            best, stale, thresholds = score, 0, candidate_thresholds
            best_state = {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
        else:
            stale += 1
        checkpoint = dict(config=config,state=model.state_dict(),optimizer=optimizer.state_dict(),epoch=epoch+1,
                          best=best,stale=stale,history=history,thresholds=thresholds,best_state=best_state,
                          python_rng=random.getstate(),torch_rng=torch.get_rng_state(),
                          cuda_rng=torch.cuda.get_rng_state_all() if args.device.startswith('cuda') else None)
        atomic_save(checkpoint,output/'last.pt')
        print(canonical(history[-1]),flush=True)
    atomic_save(dict(config=config,state=best_state,thresholds=thresholds),output/'best.pt')
    write_json(output/'model.json',dict(config=config,history=history,validation_score=best,
                                      positive_weights=weights.cpu().tolist()))
    (output/'.building').unlink()
    return dict(output=str(output),validation_score=best)


def infer(data_path, model_path, split='test', data=None):
    if (Path(model_path)/'.building').exists():
        raise ValueError('incomplete training run')
    checkpoint = load_checkpoint(Path(model_path)/'best.pt')
    config = checkpoint['config']
    torch.set_num_threads(config['threads'])
    data = [(g,a) for g,a in (load_dataset(data_path) if data is None else data) if split=='all' or g['split']==split]
    if any(g['kg_sha256']!=config['kg_sha256'] for g,_ in data):
        raise ValueError('KG snapshot differs from training')
    if 'prior' in checkpoint:
        predictions = [checkpoint['prior'] for _ in data]
    else:
        model = Classifier(sum(map(len,config['vocabulary'].values()))+1,len(config['classes']),config['mode'])
        model.load_state_dict(checkpoint['state'])
        predictions = probabilities(model,[encode(g,config['vocabulary'],config['use_kg']) for g,_ in data],'cpu')
    return data,predictions,config,checkpoint['thresholds']


def predict(args, data=None):
    data, probabilities_, config, thresholds = infer(args.data,args.model,args.split,data=data)
    with Path(args.output).open('x') as f:
        for (g,a),p in zip(data,probabilities_):
            techniques = [t for t,score in zip(config['classes'],p[1:]) if score>=thresholds[1]]
            f.write(canonical(dict(graph_id=g['id'], malicious_probability=p[0],
                                  technique_probabilities=dict(zip(config['classes'],p[1:])),
                                  malicious=p[0]>=thresholds[0], oracle_techniques=techniques,
                                  techniques=techniques if p[0]>=thresholds[0] else [],
                                  thresholds=thresholds, model_sha256=digest(Path(args.model)/'best.pt'))) + '\n')
    return dict(graphs=len(data),output=str(args.output))


def evaluate(args, data=None):
    data,predictions,config,thresholds = infer(args.data,args.model,args.split,data=data)
    if not data:
        raise ValueError('empty evaluation split')
    report = grouped_report(data,predictions,config['classes'],thresholds)
    report['confidence_intervals'] = dependency_bootstrap(data,predictions,config['classes'],thresholds)
    report.update(split=args.split,thresholds=thresholds,config=config,
                  model_sha256=digest(Path(args.model)/'best.pt'),
                  scope='Custom source-group protocol; consult preparation provenance for dependency coverage. Synthetic SAGA results do not establish real-world performance.')
    write_json(args.output,report)
    return report
