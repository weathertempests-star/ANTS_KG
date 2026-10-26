"""Reproduce node counts from collected path facts, without inventing node semantics."""
import csv
import json
from collections import Counter
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ALIASES = {'HKEY_LOCAL_MACHINE': 'HKLM', 'HKEY_CURRENT_USER': 'HKCU',
           'HKEY_USERS': 'HKU', 'HKEY_CLASSES_ROOT': 'HKCR', 'HKEY_CURRENT_CONFIG': 'HKCC'}


def canonical(path):
    parts = path.rstrip('\\').split('\\')
    parts[0] = ALIASES.get(parts[0].upper(), parts[0].upper())
    if parts[0] not in {'HKLM', 'HKCU', 'HKU', 'HKCR', 'HKCC'} or any(not p for p in parts):
        raise ValueError('invalid registry path: ' + path)
    return tuple(p.casefold() for p in parts)


def summarize(observations):
    keys, rejected = {}, []
    for observation in observations:
        # Several Microsoft ADMX_RemovableStorage rows concatenate a GUID to its
        # parent name. Keep the evidence but do not silently repair or count it.
        if re.search(r'[^\\{]\{[0-9a-fA-F-]{36}\}', observation['path']):
            rejected.append({**observation, 'reason': 'Suspected missing separator before GUID in source; requires independent verification.'})
            continue
        identity = canonical(observation['path'])
        row = keys.setdefault(identity, {'path': observation['path'].rstrip('\\'), 'evidence': []})
        row['evidence'].append(observation)
    nodes = {}
    for components, record in keys.items():
        display = record['path'].split('\\')
        for depth in range(1, len(components) + 1):
            prefix = components[:depth]
            node = nodes.setdefault(prefix, {'path': '\\'.join(display[:depth]), 'depth': depth,
                    'label': display[depth - 1], 'parent_path': '\\'.join(display[:depth-1]) or None,
                    'template_dependent': any(re.fullmatch(r'<[^<>]+>', p) for p in prefix),
                    'is_placeholder': bool(re.fullmatch(r'<[^<>]+>', prefix[-1])), 'sources': set()})
            node['sources'].update(e['source'] for e in record['evidence'])
    for identity, node in nodes.items():
        node['sources'] = sorted(node['sources'])
        node['explicitly_listed'] = identity in keys
        node['semantic_status'] = 'inventory_only_not_yet_explained'
    depth_rows = []
    for depth in sorted({n['depth'] for n in nodes.values()}):
        group = [n for n in nodes.values() if n['depth'] == depth]
        depth_rows.append({'depth': depth, 'fixed_nodes': sum(not n['template_dependent'] for n in group),
                           'template_dependent_nodes': sum(n['template_dependent'] for n in group),
                           'placeholder_nodes': sum(n['is_placeholder'] for n in group), 'total_nodes': len(group)})
    return {'explicit_paths': [keys[k] for k in sorted(keys)], 'nodes': [nodes[k] for k in sorted(nodes)],
            'quarantined': rejected, 'by_depth': depth_rows,
            'summary': {'observations': len(observations), 'accepted_unique_paths': len(keys),
                        'quarantined_observations': len(rejected),
                        'quarantined_unique_paths': len({canonical(r['path']) for r in rejected}),
                        'nodes': len(nodes), 'edges': sum(n['parent_path'] is not None for n in nodes.values()),
                        'roots': len([n for n in nodes.values() if n['depth'] == 1]),
                        'fixed_nodes': sum(not n['template_dependent'] for n in nodes.values()),
                        'template_dependent_nodes': sum(n['template_dependent'] for n in nodes.values()),
                        'placeholder_nodes': sum(n['is_placeholder'] for n in nodes.values()),
                        'by_root': dict(Counter(k[0].upper() for k in nodes))}}


def main():
    observations = []
    for name in ('registry_policy_observations.json', 'registry_core_observations.json'):
        observations.extend(json.loads((ROOT / 'knowledge' / name).read_text())['observations'])
    result = summarize(observations)
    result['retrieved_on'] = '2026-10-16'
    result['scope'] = 'Cross-version documented Windows registry-key inventory; not an exhaustive list, not an installed-machine snapshot.'
    result['counting'] = 'Root is depth 1. Unique full prefixes, case-insensitive. Values excluded. Dynamic slots count once per contextual prefix. HKCR/HKCC remain logical views, not extra physical hives.'
    output = ROOT / 'artifacts/registry-inventory'
    output.mkdir(exist_ok=True)
    (output / 'inventory.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    for filename, rows, fields in (
        ('nodes.csv', result['nodes'], ['depth', 'path', 'parent_path', 'template_dependent', 'is_placeholder', 'explicitly_listed']),
        ('depth-counts.csv', result['by_depth'], list(result['by_depth'][0])),
        ('paths.csv', result['explicit_paths'], ['path'])):
        with (output / filename).open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)
    print(json.dumps({'summary': result['summary'], 'by_depth': result['by_depth']}, indent=2))


if __name__ == '__main__':
    main()
