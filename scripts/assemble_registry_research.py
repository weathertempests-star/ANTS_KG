"""Assemble independently researched batches only after coverage and evidence checks."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from urllib.parse import urldefrag

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from standardizer_pkg import KnowledgeBase
from standardizer_pkg.knowledge import SCHEMA, _components
from standardizer_pkg.model_data import audit_graph

BATCHES = ('core', 'user_zones', 'machine_policy')


def identity(path):
    return tuple(_components(path, 'registry')[-1]['canonical_components'])


def assemble():
    definitions, relations, reviews, inputs = {}, [], {}, {}
    for name in BATCHES:
        path = ROOT / 'knowledge/research/batches' / (name + '.json')
        raw = path.read_bytes()
        data = json.loads(raw)
        assigned = json.loads((ROOT / 'knowledge/research/assignments' / (name + '.json')).read_text())
        expected = {identity(n['path']) for n in assigned['nodes']}
        actual = {identity(n['path']) for n in data['definitions']}
        if actual != expected or len(actual) != len(data['definitions']):
            raise ValueError(name + ': incomplete, extra or duplicate assigned paths')
        unresolved = [issue for issue in data.get('open_issues', []) if not isinstance(issue, dict) or issue.get('blocking', True)]
        if unresolved:
            raise ValueError(name + ': unresolved research issues: ' + str(unresolved))
        sources_read = {urldefrag(r['url'])[0] for r in data['source_reviews'] if r.get('verification') == 'read'}
        for row in data['definitions']:
            key = identity(row['path'])
            if key in definitions:
                raise ValueError('overlapping assignments: ' + row['path'])
            for url in row['sources']:
                if urldefrag(url)[0] not in sources_read:
                    raise ValueError(name + ': explanation source not reviewed: ' + url)
            definitions[key] = row
        for relation in data['relations']:
            if any(urldefrag(url)[0] not in sources_read for url in relation['sources']):
                raise ValueError(name + ': semantic relation source not reviewed')
            relations.append(relation)
        for review in data['source_reviews']:
            reviews.setdefault(urldefrag(review['url'])[0], []).append({'batch': name, **review})
        inputs[name] = hashlib.sha256(raw).hexdigest()
    inventory = ROOT / 'artifacts/registry-inventory/inventory.json'
    hierarchy = json.loads(inventory.read_text())
    if set(definitions) != {identity(n['path']) for n in hierarchy['nodes']}:
        raise ValueError('research coverage does not match the complete inventory')
    # Duplicate peer proposals are equivalent only if their complete content agrees.
    relation_map = {}
    for row in relations:
        key = (identity(row['source_path']), row['relation'], identity(row['target_path']))
        if key in relation_map and relation_map[key] != row:
            raise ValueError('conflicting semantic relation proposals: ' + str(key))
        relation_map[key] = row
    catalog = {'schema': SCHEMA, 'definitions': [definitions[identity(n['path'])] for n in hierarchy['nodes']],
               'relations': [relation_map[k] for k in sorted(relation_map)]}
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'catalog.json'
        path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
        graph = KnowledgeBase.load_catalog(path, inventory)
        audit = audit_graph(graph)
    if not audit['valid']:
        raise ValueError('content gate failed: ' + '; '.join(audit['problems']))
    return catalog, {'schema': 'registry-research-sources-1', 'batch_sha256': inputs,
                     'sources': [{'url': url, 'reviews': reviews[url]} for url in sorted(reviews)],
                     'audit': audit}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'knowledge/windows_registry.json')
    parser.add_argument('--sources-output', type=Path, default=ROOT / 'knowledge/research/source_reviews.json')
    args = parser.parse_args()
    catalog, reviews = assemble()
    if args.output.resolve() == args.sources_output.resolve():
        raise ValueError('catalog and source-review outputs must differ')
    args.output.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    args.sources_output.write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(reviews['audit'], indent=2))


if __name__ == '__main__':
    main()
