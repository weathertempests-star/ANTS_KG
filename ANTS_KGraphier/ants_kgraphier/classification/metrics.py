"""Masked metrics with explicit support and undefined balanced accuracy."""
from collections import defaultdict


def binary_metrics(y, scores, threshold=.5):
    pairs = [(int(a), float(b)) for a, b in zip(y, scores) if a is not None]
    tp = sum(a == 1 and b >= threshold for a, b in pairs)
    fp = sum(a == 0 and b >= threshold for a, b in pairs)
    fn = sum(a == 1 and b < threshold for a, b in pairs)
    tn = sum(a == 0 and b < threshold for a, b in pairs)
    positive, negative = tp + fn, tn + fp
    precision, recall = tp / max(1, tp+fp), tp / max(1, positive)
    f1 = 2*tp / max(1, 2*tp+fp+fn)
    # Non-interpolated PR area (average precision), grouped ties.
    bins = defaultdict(list)
    for a, b in pairs:
        bins[b].append(a)
    running_tp = running_n = 0
    ap = 0.
    for score in sorted(bins, reverse=True):
        running_tp += sum(bins[score])
        running_n += len(bins[score])
        ap += sum(bins[score]) / max(1, positive) * running_tp / running_n
    return dict(n=len(pairs), positive=positive, negative=negative,
                prevalence=positive/len(pairs) if pairs else None,
                balanced_accuracy=(recall + tn/negative)/2 if positive and negative else None,
                precision=precision, recall=recall, f1=f1,
                macro_f1=(f1 + 2*tn/max(1, 2*tn+fp+fn))/2 if pairs else None,
                pr_auc=ap if positive else None, pr_auc_definition='average precision; grouped score ties',
                confusion_matrix=[[tn, fp], [fn, tp]])


def technique_metrics(labels, probabilities, classes, threshold, binary_threshold=None):
    per_class = {}
    for i, t in enumerate(classes):
        y, p = [], []
        for a, pred in zip(labels, probabilities):
            if binary_threshold is None and a['binary'] != 1:
                continue
            y.append(int(t in a['techniques']) if a['complete'] or t in a['techniques'] else None)
            p.append(pred[i+1] if binary_threshold is None or pred[0] >= binary_threshold else -1)
        per_class[t] = binary_metrics(y, p, threshold)
    supported = [m for m in per_class.values() if m['positive']]
    valid = [m['balanced_accuracy'] for m in per_class.values() if m['balanced_accuracy'] is not None]
    tp = sum(m['confusion_matrix'][1][1] for m in per_class.values())
    fp = sum(m['confusion_matrix'][0][1] for m in per_class.values())
    fn = sum(m['confusion_matrix'][1][0] for m in per_class.values())
    return dict(per_class=per_class, macro_f1=sum(m['f1'] for m in supported)/len(supported) if supported else None,
                macro_f1_scope='classes with observed positive support', supported_classes=len(supported),
                micro_f1=2*tp/max(1, 2*tp+fp+fn),
                balanced_accuracy=sum(valid)/len(valid) if valid else None, balanced_accuracy_classes=len(valid))


def evaluate_rows(data, probabilities, classes, thresholds):
    labels = [a for _, a in data]
    b, t = thresholds
    result = dict(binary=binary_metrics([a['binary'] for a in labels], [p[0] for p in probabilities], b),
                  technique_oracle=technique_metrics(labels, probabilities, classes, t),
                  technique_end_to_end=technique_metrics(labels, probabilities, classes, t, b))
    unseen = sorted({t for a in labels for t in a['techniques']} - set(classes))
    result['uncovered_techniques'] = {t: dict(graphs=sum(t in a['techniques'] for a in labels),
        events=len({eid for a in labels for eid in a['technique_events'].get(t, [])})) for t in unseen}
    return result


def choose_thresholds(data, probabilities, classes):
    # Independent binary and shared Technique thresholds; deterministic ties
    # prefer proximity to 0.5, then the smaller threshold.
    grid = sorted([i/20 for i in range(1, 20)], key=lambda x: (abs(x-.5), x))
    b = max(grid, key=lambda x: binary_metrics([a['binary'] for _, a in data], [p[0] for p in probabilities], x)['balanced_accuracy'])
    t = max(grid, key=lambda x: technique_metrics([a for _, a in data], probabilities, classes, x)['macro_f1'] or 0)
    report = evaluate_rows(data, probabilities, classes, (b,t))
    binary = report['binary']['balanced_accuracy']
    technique = report['technique_oracle']['macro_f1']
    return (b,t), (binary+technique)/2 if technique is not None else binary, technique is None


def grouped_report(data, probabilities, classes, thresholds):
    result = evaluate_rows(data, probabilities, classes, thresholds)
    groups = defaultdict(list)
    unique, seen = [], set()
    for i, (g,a) in enumerate(data):
        groups['recording:' + g['recording_sha256']].append(i)
        group = 'malicious_anchor' if a['anchor_malicious'] else ('benign_anchor_malicious_context' if a['anchor_status']=='benign' and a['binary']==1 else 'all_benign' if a['binary']==0 else 'unknown')
        groups['anchor:' + group].append(i)
        groups['truncated:' + str(g['budget_truncated'])].append(i)
        size = len(g['events'])
        groups['size:' + ('1' if size==1 else '2-8' if size<=8 else '9-33' if size<=33 else '34+')].append(i)
        signature = tuple(sorted(e['event_id'] for e in g['events']))
        if signature not in seen:
            seen.add(signature)
            unique.append(i)
    groups['deduplicated_event_sets'] = unique
    result['groups'] = {key: evaluate_rows([data[i] for i in indices], [probabilities[i] for i in indices], classes, thresholds)
                        for key, indices in groups.items()}
    rec_metrics = [v['binary']['balanced_accuracy'] for k,v in result['groups'].items() if k.startswith('recording:') and v['binary']['balanced_accuracy'] is not None]
    result['recording_macro_balanced_accuracy'] = sum(rec_metrics)/len(rec_metrics) if rec_metrics else None
    result['recording_macro_valid_recordings'] = len(rec_metrics)
    result['event_counts'] = dict(graphs=len(data), total=sum(len(g['events']) for g,_ in data), unique_event_sets=len(unique))
    result['errors'] = [dict(graph_id=g['id'], binary=a['binary'], probability=p[0], techniques=a['techniques'])
                        for (g,a),p in zip(data, probabilities) if a['binary'] is not None and (p[0]>=thresholds[0]) != bool(a['binary'])][:100]
    result['technique_errors'] = [dict(graph_id=g['id'], expected=a['techniques'],
        predicted=[t for t,score in zip(classes,p[1:]) if score>=thresholds[1]],
        complete=a['complete']) for (g,a),p in zip(data,probabilities)
        if a['binary']==1 and (any(t in a['techniques'] and score<thresholds[1] for t,score in zip(classes,p[1:]))
        or (a['complete'] and any(t not in a['techniques'] and score>=thresholds[1] for t,score in zip(classes,p[1:]))))][:100]
    return result


def dependency_bootstrap(data, probabilities, classes, thresholds, repeats=1000, seed=17):
    """Percentile intervals resample whole dependency groups, never subgraphs."""
    import random
    groups = defaultdict(list)
    for i, (graph, _) in enumerate(data):
        groups[graph['dependency_group']].append(i)
    keys = sorted(groups)
    result = dict(unit='source dependency group', groups=len(keys), seed=seed,
                  repeats=repeats, confidence=.95, intervals={})
    if len(keys) < 2:
        result['unavailable_reason'] = 'fewer than two independent evaluation groups'
        return result
    rng = random.Random(seed)
    samples = defaultdict(list)
    for _ in range(repeats):
        indices = [i for key in rng.choices(keys, k=len(keys)) for i in groups[key]]
        report = evaluate_rows([data[i] for i in indices], [probabilities[i] for i in indices], classes, thresholds)
        for section, metric in [('binary', 'balanced_accuracy'), ('binary', 'f1'),
                                ('technique_oracle', 'macro_f1'), ('technique_end_to_end', 'micro_f1')]:
            value = report[section][metric]
            if value is not None:
                samples[section+'.'+metric].append(value)
    for key, values in samples.items():
        values.sort()
        result['intervals'][key] = dict(low=values[int(.025*(len(values)-1))],
                                        high=values[int(.975*(len(values)-1))], valid_replicates=len(values))
    return result
