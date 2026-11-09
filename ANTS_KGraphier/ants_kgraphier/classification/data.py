"""Auditable manual labels and shared, nested Registry anchor sampling."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import random
import re

from ..extract import extract
from ..io import canonical, digest, fingerprint, write_json
from ..knowledge import Knowledge
from ..store import connect, recordings

LABEL = re.compile(r'^(T\d{4}(?:\.\d{3})?)(?:_[A-Za-z0-9-]+)?$')


def parse_label(raw):
    if raw == 'benign':
        return dict(raw=raw, status='benign', attack_id=None, parent=None)
    match = LABEL.fullmatch(raw) if isinstance(raw, str) else None
    if match:
        full = match[1]
        return dict(raw=raw, status='malicious', attack_id=full, parent=full.split('.')[0])
    return dict(raw=raw, status='unknown', attack_id=None, parent=None)


def supervision(graph, labels):
    parsed = {e['event_id']: parse_label(labels.get(e['row'])) for e in graph['events']}
    malicious = [eid for eid, item in parsed.items() if item['status'] == 'malicious']
    complete = all(item['status'] != 'unknown' for item in parsed.values())
    return dict(graph_id=graph['id'], binary=1 if malicious else (0 if complete else None),
                techniques=sorted({item['parent'] for item in parsed.values() if item['parent']}),
                malicious_event_ids=malicious,
                technique_events={t: [eid for eid, p in parsed.items() if p['parent'] == t]
                                  for t in sorted({p['parent'] for p in parsed.values() if p['parent']})},
                anchor_malicious=parsed[graph['anchor_event_id']]['status'] == 'malicious',
                anchor_status=parsed[graph['anchor_event_id']]['status'], complete=complete,
                unknown_event_ids=[eid for eid, item in parsed.items() if item['status'] == 'unknown'],
                source_sha256=graph['recording_sha256'],
                event_labels_sha256=fingerprint(parsed))


def read_jsonl(path):
    with Path(path).open() as f:
        for line in f:
            yield json.loads(line)


def audit_store(store, splits):
    with connect(store) as db:
        recs = recordings(db)
        for r in recs:
            if splits.get(r['dependency_group']) not in {'train', 'validation', 'test'}:
                raise ValueError('missing/invalid dependency split: ' + r['dependency_group'])
        split_by_rec = {r['store_id']: splits[r['dependency_group']] for r in recs}
        labels = [dict(parse_label(r[0]), count=r[1]) for r in db.execute(
            'SELECT label,count(*) FROM labels GROUP BY label')]
        # SQLite does the large grouping on disk. Exact raw-event hashes include
        # all original fields; collisions here are evidence, not script identity.
        duplicates = []
        for r in db.execute('SELECT raw_sha,group_concat(DISTINCT rec),count(*) FROM events '
                            'GROUP BY raw_sha HAVING count(DISTINCT rec)>1'):
            ids = r[1].split(',')
            if len({split_by_rec[i] for i in ids}) > 1:
                duplicates.append(dict(raw_sha256=r[0], recordings=ids, occurrences=r[2]))
        scopes = sorted({r.get('dependency_scope', 'unconfirmed; recording-level feasibility only') for r in recs})
        return dict(recordings=recs, label_map=labels, cross_split_exact_events=duplicates,
                    unknown_labels=[x for x in labels if x['status'] == 'unknown'],
                    script_reuse='; '.join(scopes),
                    exact_duplicate_policy='block preparation; consolidate confirmed dependency groups and rerun')


def prepare(args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    (output / '.building').touch()
    splits = json.loads(Path(args.splits).read_text())
    audit = audit_store(args.store, splits)
    write_json(output / 'split-audit.json', audit)
    write_json(output / 'label-map.json', audit['label_map'])
    if audit['cross_split_exact_events']:
        raise ValueError('cross-split exact event duplicates; inspect split-audit.json and repair groups')
    kg = Knowledge(args.kg)
    settings = [(m, b) for m in ('trec', 'temporal', 'window') for b in args.budgets]
    handles = {}
    for method, budget in settings:
        d = output / f'{method}-{budget}'
        d.mkdir()
        handles[method, budget] = ((d / 'graphs.jsonl').open('x'), (d / 'labels.jsonl').open('x'))
    reports, anchors = [], []
    coverage = {key: defaultdict(set) for key in settings}
    raw_support = Counter()
    try:
        with connect(args.store) as db:
            states = []
            for rec in recordings(db):
                rid, group = rec['store_id'], rec['dependency_group']
                population = [r[0] for r in db.execute(
                    "SELECT row FROM events WHERE rec=? AND dst_type='Registry' ORDER BY row", (rid,))]
                random.Random(str(args.seed) + rid).shuffle(population)
                for label, count in db.execute('SELECT label,count(*) FROM labels WHERE rec=? GROUP BY label', (rid,)):
                    parent = parse_label(label)['parent']
                    if parent:
                        raw_support[parent] += count
                states.append(dict(rec=rec, split=splits[group], population=population,
                                   done=0, support={key: Counter() for key in settings}))
            # Expansion is decided across the entire validation split, not per recording.
            # Each tier is a prefix of the same label-independent random permutation.
            for tier in dict.fromkeys((args.per_recording, max(args.per_recording, 8000), None)):
                for state in states:
                    if tier != args.per_recording and state['split'] != 'validation':
                        continue
                    rec, split = state['rec'], state['split']
                    rid, group = rec['store_id'], rec['dependency_group']
                    selected = state['population'][:tier]
                    if len(selected) == state['done']:
                        continue
                    labels = {r[0]: r[1] for r in db.execute('SELECT row,label FROM labels WHERE rec=?', (rid,))}
                    for row in selected[state['done']:]:
                        sampling = 'uniform' if state['done'] == 0 else 'validation_expansion'
                        anchors.append(dict(recording=rid, row=row, split=split, sampling=sampling))
                        for method, budget in settings:
                            graph = extract(db, rid, row, kg, method=method, hops=2, fanout=8,
                                            budget=budget, mode='offline')
                            graph.update(split=split, dependency_group=group)
                            label = supervision(graph, labels)
                            label['sampling'] = sampling
                            for technique, ids in label['technique_events'].items():
                                coverage[method, budget][technique].update(ids)
                            gf, lf = handles[method, budget]
                            gf.write(canonical(graph) + '\n')
                            lf.write(canonical(label) + '\n')
                            state['support'][method, budget][str(label['binary'])] += 1
                    state['done'] = len(selected)
                validation_counts = {key: Counter() for key in settings}
                for state in states:
                    if state['split'] == 'validation':
                        for key in settings:
                            validation_counts[key].update(state['support'][key])
                if all(c['0'] and c['1'] for c in validation_counts.values()):
                    break
            for state in states:
                reports.append(dict(recording=state['rec']['id'], split=state['split'],
                                    population=len(state['population']), sampled=state['done'],
                                    support={f'{m}-{b}': dict(c) for (m,b),c in state['support'].items()}))
                print(canonical(reports[-1]), flush=True)
    finally:
        for pair in handles.values():
            for f in pair:
                f.close()
    write_json(output / 'anchors.json', anchors)
    validation_support = {f'{m}-{b}': Counter() for m, b in settings}
    for report in reports:
        if report['split'] == 'validation':
            for key, counts in report['support'].items():
                validation_support[key].update(counts)
    valid = all(c['0'] and c['1'] for c in validation_support.values())
    write_json(output / 'technique-coverage.json', {f'{m}-{b}': {
        t: dict(raw_events=n, extracted_events=len(coverage[m, b][t]),
                coverage=len(coverage[m, b][t])/n) for t, n in raw_support.items()}
        for m, b in settings})
    files = {str(p.relative_to(output)): digest(p) for p in output.glob('*/*.jsonl')}
    write_json(output / 'manifest.json', dict(schema='classification-1', seed=args.seed,
               per_recording=args.per_recording, budgets=args.budgets, splits=splits,
               kg_sha256=kg.sha256, source_manifest_sha256=fingerprint(audit['recordings']),
               anchors_sha256=digest(output/'anchors.json'), files=files, recordings=reports,
               validation_usable=valid, validation_support=validation_support,
               protocol='custom source-group split; SAGA-only when using SAGA store',
               limitation=audit['script_reuse']))
    (output / '.building').unlink()
    return dict(output=str(output), validation_usable=valid)


def load_dataset(directory):
    directory = Path(directory)
    if (directory.parent / '.building').exists():
        raise ValueError('incomplete preparation')
    label_rows = list(read_jsonl(directory / 'labels.jsonl'))
    labels = {a['graph_id']: a for a in label_rows}
    if len(labels) != len(label_rows):
        raise ValueError('duplicate graph labels')
    data = [(g, labels[g['id']]) for g in read_jsonl(directory / 'graphs.jsonl')]
    if len(data) != len(labels) or len({g['id'] for g, _ in data}) != len(data):
        raise ValueError('duplicate or unmatched graph labels')
    assignments = defaultdict(set)
    for g, a in data:
        if a['source_sha256'] != g['recording_sha256']:
            raise ValueError('label provenance mismatch')
        for key in ('recording_sha256', 'dependency_group'):
            assignments[key, g[key]].add(g['split'])
    if any(len(v) > 1 for v in assignments.values()):
        raise ValueError('cross-split recording/dependency leakage')
    manifest_path = directory.parent / 'manifest.json'
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        for name in ('graphs.jsonl', 'labels.jsonl'):
            key = f'{directory.name}/{name}'
            if manifest['files'][key] != digest(directory / name):
                raise ValueError('dataset hash mismatch')
    return data
