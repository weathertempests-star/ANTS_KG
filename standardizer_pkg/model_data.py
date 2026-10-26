"""Provider-neutral, reproducible learning records from reviewed prefix knowledge.

These exports prepare data; they do not claim that a model was trained or evaluated.
Split families are dataset partitions, not inferred registry functionality tags.
"""
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path

from .knowledge import KnowledgeBase
from .zettelkasten import _atomic_write

FORMAT = 'registry-learning-data-1'
SYSTEM_MESSAGE = (
    'Explain Windows Registry knowledge using the supplied key scope and documented evidence. '
    'Distinguish keys, values, configuration, actual operations and outcomes. '
    'State uncertainty and platform limits. Never infer execution, policy enforcement or intent from a path alone.'
)


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def _jsonl(rows):
    return ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows)


def _sha(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def split_family(node):
    """Conservative cross-hive concept groups; not semantic labels or attack tags."""
    parts = node['canonical_components'][1:]
    if parts and parts[0] == '<userhive>':
        parts = parts[1:]
    components = set(parts)
    # More specific families precede their namespace containers.
    groups = [
        ('internet_zones', {'internet settings', 'zones', 'lockdown_zones'}),
        ('certificates', {'systemcertificates', 'cryptography'}),
        ('com_and_associations', {'classes'}),
        ('event_logging', {'eventlog', 'audit'}),
        ('device_installation', {'deviceinstall', 'driverinstall', 'class', 'deviceclasses', 'codeviceinstallers', 'enum'}),
        ('removable_storage', {'removablestoragedevices'}),
        ('printing', {'printers'}),
        ('remote_desktop', {'terminal services', 'workspaces'}),
        ('time_service', {'w32time'}),
        ('remote_management', {'winrm'}),
        ('name_resolution', {'dnsclient'}),
        ('network_providers', {'networkprovider'}),
        ('network_configuration', {'network connections', 'network', 'tcpip', 'tcpip6'}),
        ('file_sharing', {'lanmanserver', 'lanmanworkstation'}),
        ('authentication', {'kerberos', 'netlogon', 'lsa', 'sam', 'security'}),
        ('code_integrity', {'deviceguard'}),
        ('antimalware_configuration', {'windows defender'}),
        ('application_compatibility', {'appcompat'}),
        ('autorun', {'run', 'runonce'}),
        ('software_installation', {'uninstall'}),
        ('user_interface', {'explorer', 'comdlg32', 'windows nt'}),
        ('environment_and_initialization', {'session manager', 'environment'}),
        ('hardware_configuration', {'hardware', 'hardware profiles'}),
        ('filesystem_configuration', {'filesystem', 'filesystems'}),
        ('service_configuration', {'services'}),
    ]
    for family, tokens in groups:
        if components & tokens:
            return family
    if not parts or parts == ['.default']:
        return 'registry_roots'
    return 'structural_namespaces'


def split_for_family(family):
    # Entire concept families are held out, including both hive scopes and all task variants.
    bucket = int(_sha('registry-learning-split-v1:' + family)[:8], 16) % 10
    return 'test' if bucket == 0 else 'validation' if bucket == 1 else 'train'


def audit_graph(graph):
    data = graph.to_dict()
    problems = []
    if not data['nodes']:
        problems.append('learning data requires at least one researched Registry node')
    summaries = {}
    for node in data['nodes']:
        research = node.get('research', {})
        if node['domain'] != 'registry' or node['status'] == 'pending' or not research:
            problems.append(node['id'] + ': missing researched Registry knowledge')
            continue
        if len(node['explanation'].split()) < 25:
            problems.append(node['id'] + ': explanation too short for a self-contained concept')
        summary = research['summary'].casefold().strip()
        if summary in summaries:
            problems.append(node['id'] + ': duplicate atomic claim with ' + summaries[summary])
        summaries[summary] = node['id']
        if node['status'] == 'documented' and not any(e['support'] == 'direct' for e in research['evidence']):
            problems.append(node['id'] + ': documented status without direct evidence')
        if node['status'] == 'structural' and not any(e['support'] == 'structural_inference' for e in research['evidence']):
            problems.append(node['id'] + ': structural status without explicit inference evidence')
    return {'valid': not problems, 'problems': problems, 'nodes': len(data['nodes']),
            'hierarchy_edges': len(data['edges']), 'semantic_edges': len(data.get('semantic_edges', [])),
            'status_counts': dict(Counter(n['status'] for n in data['nodes'])),
            'note': 'Schema/content checks only; factual correctness requires the separate source and editorial review.'}


def render_model_data(graph):
    audit = audit_graph(graph)
    if not audit['valid']:
        raise ValueError('model export needs complete research: ' + '; '.join(audit['problems']))
    data = graph.to_dict()
    nodes = sorted(data['nodes'], key=lambda n: n['id'])
    positions = {n['id']: i for i, n in enumerate(nodes)}
    records, examples = [], {split: [] for split in ('train', 'validation', 'test')}
    for node in nodes:
        research = node['research']
        family = split_family(node)
        split = split_for_family(family)
        records.append({'schema': FORMAT, 'node_index': positions[node['id']], 'node_id': node['id'],
                        'path': node['path'], 'canonical_components': node['canonical_components'],
                        'depth': node['depth'], 'parent_id': node['parent_id'], 'status': node['status'],
                        'role': node['role'], 'explanation': node['explanation'], 'research': research,
                        'template_dependent': node['template_dependent'], 'is_placeholder': node['is_placeholder'],
                        'path_sources': node['path_sources'], 'explanation_sources': node['explanation_sources'],
                        'split_family': family, 'split': split})
        key = json.dumps(node['path'], ensure_ascii=False)
        meaning = (research['summary'] + '\n\n' + node['explanation'] + '\n\nScope: ' + research['scope'] +
                   '. Evidence status: ' + node['status'] + '.\nApplicability: ' + research['applicability'])
        interpretation = research['log_context'] + '\n\nCannot establish from the path:\n' + '\n'.join('- ' + s for s in research['cannot_infer'])
        if node['template_dependent']:
            meaning += '\nThis is a template-dependent knowledge pattern; no concrete name has been matched.'
        for task, prompt, answer in (
            ('explain_prefix', 'Explain the system role of the Registry key ' + key + ' in its complete prefix context.', meaning),
            ('interpret_path_only', 'A system-level log names the Registry key ' + key + '. No event type, operation, result or value data is supplied. What does this identify, and what remains unknown?', interpretation),
        ):
            examples[split].append({'id': node['id'] + ':' + task, 'node_id': node['id'], 'task': task,
                                    'split_family': family, 'evidence_status': node['status'], 'sources': node['explanation_sources'],
                                    'authorship': 'source-grounded AI-authored knowledge; deterministic prompt/answer projection',
                                    'messages': [{'role': 'system', 'content': SYSTEM_MESSAGE},
                                                 {'role': 'user', 'content': prompt},
                                                 {'role': 'assistant', 'content': answer}]})
    split_by_id = {r['node_id']: r['split'] for r in records}
    edges = [{**e, 'edge_kind': kind} for kind, rows in (('hierarchy', data['edges']), ('semantic', data.get('semantic_edges', []))) for e in rows]
    edge_index = [{'source': positions[e['source']], 'target': positions[e['target']], 'type': e['type'], 'kind': e['edge_kind']} for e in edges]
    files = {'node-records.jsonl': _jsonl(records), 'graph/edge-index.json': _json(edge_index),
             'graph/snapshot.json': _json(data),
             'graph/semantic-edges.jsonl': _jsonl(data.get('semantic_edges', [])),
             'graph/node-index.json': _json([{'index': positions[n['id']], 'node_id': n['id'], 'split': split_by_id[n['id']]} for n in nodes]),
             'graph/train-edge-index.json': _json([row for row, edge in zip(edge_index, edges) if split_by_id[edge['source']] == split_by_id[edge['target']] == 'train']),
             'audit.json': _json(audit)}
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=['source_id', 'target_id', 'relation', 'kind', 'source_split', 'target_split'])
    writer.writeheader()
    for edge in edges:
        writer.writerow({'source_id': edge['source'], 'target_id': edge['target'], 'relation': edge['type'], 'kind': edge['edge_kind'],
                         'source_split': split_by_id[edge['source']], 'target_split': split_by_id[edge['target']]})
    files['graph/edges.csv'] = stream.getvalue()
    for split, rows in examples.items():
        files['sft/' + split + '.jsonl'] = _jsonl(rows)
    families = {r['split_family']: r['split'] for r in records}
    files['splits.json'] = _json({'strategy': 'registry-learning-split-v1', 'families': dict(sorted(families.items())),
                                  'node_counts': dict(Counter(r['split'] for r in records)),
                                  'example_counts': {k: len(v) for k, v in examples.items()},
                                  'limitations': ['Related concepts, ancestor knowledge and documentation may still overlap across families.',
                                                  'Full graph exports are transductive; train-edge-index excludes validation/test endpoints.',
                                                  'This split supports a small pilot, not a claim of independent real-log generalization.']})
    manifest = {'schema': FORMAT, 'graph_sha256': _sha(_json(data)), 'files': {name: _sha(content) for name, content in sorted(files.items())},
                'nodes': len(nodes), 'sft_examples': sum(len(v) for v in examples.values())}
    files['manifest.json'] = _json(manifest)
    return files


def _check_destination(root, names):
    for name in names:
        path = root / name
        if path.is_absolute() and root not in path.parents:
            raise ValueError('unsafe generated data path')
        if '..' in Path(name).parts or Path(name).is_absolute():
            raise ValueError('unsafe generated data path')
        for part in [path, *path.parents]:
            if part.is_symlink():
                raise ValueError('generated data paths cannot contain symlinks')


def export_model_data(graph, directory):
    files = render_model_data(graph)
    root = Path(directory).absolute()
    old = {}
    manifest_path = root / 'manifest.json'
    _check_destination(root, files)
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        if manifest.get('schema') != FORMAT or not isinstance(manifest.get('files'), dict):
            raise ValueError('destination is not a managed model dataset')
        old = manifest['files']
        if set(old) != set(files) - {'manifest.json'}:
            raise ValueError('model manifest contains missing or unmanaged file paths')
        _check_destination(root, old)
        for name, digest in old.items():
            path = root / name
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise ValueError('model dataset was manually changed or is incomplete: ' + name)
        validate_model_data(KnowledgeBase.load(root / 'graph/snapshot.json'), root)
    for name in set(files) - set(old) - {'manifest.json'}:
        if (root / name).exists():
            raise ValueError('model dataset would overwrite unmanaged file: ' + name)
    root.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        if name != 'manifest.json':
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            _atomic_write(path, content)
    for name in set(old) - set(files):
        (root / name).unlink()
    _atomic_write(manifest_path, files['manifest.json'])
    return validate_model_data(graph, directory)


def validate_model_data(graph, directory):
    root = Path(directory).absolute()
    files = render_model_data(graph)
    _check_destination(root, files)
    for name, expected in files.items():
        path = root / name
        if not path.is_file() or path.read_bytes() != expected.encode('utf-8'):
            raise ValueError('model dataset differs from supplied knowledge graph: ' + name)
    return {'valid': True, 'files': len(files), 'graph_sha256': _sha(_json(graph.to_dict()))}
