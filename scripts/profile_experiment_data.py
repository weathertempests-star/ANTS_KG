"""Read-only inventory of the eleven supplied recordings; never infer true labels.

CHT arrays are loaded one file at a time; large APT JSONL files are streamed.
Raw targets may combine key and value names. Exact-node matches below are a
lexical audit only, not a validated semantic coverage measure.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from standardizer_pkg.knowledge import split_input


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def profile(path, known):
    is_array = path.parent.name == 'CHT_selected'
    report = dict(path=str(path.relative_to(ROOT)), bytes=path.stat().st_size,
                  sha256=digest(path), format='json_array' if is_array else 'jsonl')
    counts = defaultdict(Counter)
    timestamps, processes, targets, fingerprints = Counter(), defaultdict(set), {}, set()
    content_fingerprints = set()
    total = duplicates = inversions = reg_rows = reg_values = missing_keys = 0
    previous = low = high = None
    with path.open(encoding='utf-8') as stream:
        rows = json.load(stream) if is_array else (json.loads(line) for line in stream if line.strip())
        for row in rows:
            total += 1
            if not isinstance(row, dict):
                raise ValueError('non-object record in ' + str(path))
            counts['top_fields'].update(row.keys())
            label = str(row.get('label', '<missing>'))
            relation = str(row.get('relation', '<missing>'))
            counts['labels'][label] += 1
            counts['relations'][relation] += 1
            counts['label_relation'][label + ' | ' + relation] += 1
            src, dst = row.get('srcNode'), row.get('dstNode')
            counts['source_object_types'][type(src).__name__] += 1
            counts['destination_object_types'][type(dst).__name__] += 1
            src = src if isinstance(src, dict) else {}
            dst = dst if isinstance(dst, dict) else {}
            counts['source_fields'].update(src.keys())
            counts['destination_fields'].update(dst.keys())
            counts['node_type_pairs'][str(src.get('Type')) + ' -> ' + str(dst.get('Type'))] += 1
            proc = src.get('UUID') if src.get('Type') == 'Process' else None
            if proc:
                processes[proc].add(label)
            fingerprint = hashlib.sha256(json.dumps(row, sort_keys=True, separators=(',', ':')).encode()).digest()[:16]
            duplicates += fingerprint in fingerprints
            fingerprints.add(fingerprint)
            content = {k:v for k,v in row.items() if k not in {'label', 'timestamp_raw'}}
            content_fingerprints.add(hashlib.sha256(json.dumps(content, sort_keys=True, separators=(',', ':')).encode()).digest()[:16])
            timestamp = row.get('timestamp')
            counts['timestamp_types'][type(timestamp).__name__] += 1
            if isinstance(timestamp, (int, float)) and not isinstance(timestamp, bool):
                low = timestamp if low is None else min(low, timestamp)
                high = timestamp if high is None else max(high, timestamp)
                inversions += previous is not None and timestamp < previous
                previous = timestamp
                timestamps[timestamp] += 1
            if 'timestamp_raw' in row:
                counts['timestamp_raw_presence']['empty' if row['timestamp_raw'] == '' else 'nonempty'] += 1
                counts['timestamp_raw_labels'][label] += 1
            text = ' '.join(str(src.get(k, '')) for k in ('Name', 'Image', 'Cmdline')).lower()
            for marker in ('maliciousfiles', '\\evil\\', 'caldera', 'sandcat'):
                if marker in text:
                    counts['source_marker_rows'][marker] += 1
                    counts['source_marker_labels'][marker + ' | ' + label] += 1
            if dst.get('Type') == 'Registry':
                reg_rows += 1
                counts['registry_labels'][label] += 1
                counts['registry_relations'][relation] += 1
                counts['registry_label_relation'][label + ' | ' + relation] += 1
                reg_values += 'Value' in dst
                counts['registry_value_presence_by_label'][label + (' | present' if 'Value' in dst else ' | absent')] += 1
                target = dst.get('Key')
                if not isinstance(target, str):
                    missing_keys += 1
                    continue
                if target not in targets:
                    parts, _ = split_input(target, 'registry')
                    components = tuple(parts[-1]['canonical_components']) if parts else ()
                    depth = next((i for i in range(len(components), 0, -1) if components[:i] in known), 0)
                    targets[target] = (components in known, depth)
                exact, depth = targets[target]
                counts['raw_target_exact_match_by_label'][label + (' | exact' if exact else ' | nonexact')] += 1
                counts['raw_target_known_depth'][str(depth)] += 1
    report.update(records=total, exact_duplicate_records=duplicates,
                  registry_records=reg_rows, registry_records_with_Value=reg_values,
                  registry_records_missing_Key=missing_keys, unique_registry_raw_targets=len(targets),
                  unique_registry_raw_targets_exact_nodes=sum(v[0] for v in targets.values()),
                  source_process_uuids=len(processes), source_process_uuids_with_mixed_labels=sum(len(v)>1 for v in processes.values()),
                  timestamp_min=low, timestamp_max=high, timestamp_distinct=len(timestamps),
                  timestamp_adjacent_decreases=inversions,
                  timestamp_records_sharing_time=sum(n for n in timestamps.values() if n > 1))
    report.update({k: dict(sorted(v.items())) for k, v in counts.items()})
    return report, content_fingerprints


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'artifacts/experiment-planning/data_profile.json')
    args = parser.parse_args()
    graph_path = ROOT/'artifacts/knowledge-vault/kg.json'
    graph = json.loads(graph_path.read_text())
    known = {tuple(n['canonical_components']) for n in graph['nodes']}
    paths = sorted((ROOT/'data/CHT_selected').glob('*.json')) + sorted((ROOT/'data/Apt').glob('*/events.json'))
    if len(paths) != 11:
        raise ValueError('expected six CHT files and five APT recordings')
    results, membership, overlap = [], {}, Counter()
    for index, path in enumerate(paths):
        item, signatures = profile(path, known)
        for signature in signatures:
            mask = membership.get(signature, 0)
            for previous in range(index):
                if mask & (1 << previous):
                    overlap[(previous, index)] += 1
            membership[signature] = mask | (1 << index)
        results.append(item)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps({'scan_complete':False,'recordings':results}, indent=2)+'\n')
        print(json.dumps({k:item[k] for k in ('path','records','registry_records','labels','registry_labels')},ensure_ascii=False), flush=True)
    ignored = []
    for p in sorted((ROOT/'data').rglob('*checkpoint*.json')):
        sha = digest(p)
        ignored.append({'path':str(p.relative_to(ROOT)), 'sha256':sha,
                        'identical_to':[r['path'] for r in results if r['sha256']==sha]})
    report = {'schema':'recording-planning-profile-1','graph_sha256':digest(graph_path),
              'input_policy':'Explicit six top-level CHT arrays and five APT */events.json; exclude notebook checkpoints.',
              'label_policy':'User confirms per-event manual annotation. Preserve original labels; binary mapping and annotation-guideline audit remain explicit.',
              'coverage_policy':'Raw-target exact-node matches only; key/value separation and view/template adaptation are not applied.',
              'recordings':results,'excluded_checkpoints':ignored,'scan_complete':True,
              'cross_recording_identical_events':[{'left':results[a]['path'],'right':results[b]['path'],'unique_shared':n} for (a,b),n in sorted(overlap.items())],
              'overlap_policy':'128-bit truncated SHA-256 of full record excluding label and timestamp_raw; unique signatures per recording, retaining timestamp and UUID; no semantic deduplication.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

if __name__ == '__main__':
    main()
