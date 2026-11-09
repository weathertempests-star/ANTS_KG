"""Audit explicitly listed normalized recordings and create an ingest manifest.

Never guesses paths, labels, formats, host identities, or dependency groups.
For external logs, normalize first and retain raw-to-normalized provenance.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

from ants_kgraphier.io import rows, digest, write_json


def make_sources(root, spec, output):
    root, output = Path(root).resolve(), Path(output)
    if output.exists():
        raise FileExistsError(output)
    entries, audit, ids, paths, hashes = [], [], set(), set(), set()
    for source in spec['recordings']:
        sid, relative = source['id'], source['path']
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or path in paths or sid in ids:
            raise ValueError('duplicate source or source outside root')
        if not isinstance(source.get('dependency_group'), str) or not source['dependency_group']:
            raise ValueError('explicit dependency group required')
        if source['format'] not in {'jsonl', 'json_array'}:
            raise ValueError('explicit supported format required')
        counts = Counter()
        for item in rows(path, source['format']):
            if not isinstance(item, dict):
                raise ValueError('event must be an object')
            if not isinstance(item.get('relation'), str) or not item['relation']:
                raise ValueError('operation missing')
            for side in ('srcNode', 'dstNode'):
                node = item.get(side)
                if not isinstance(node, dict) or not isinstance(node.get('Type'), str):
                    raise ValueError('normalize endpoint Type before ingest')
                if not node.get('UUID'):
                    raise ValueError('normalize host-scoped stable UUID before ingest')
                if node['Type'] == 'Registry' and not isinstance(node.get('Key'), str):
                    raise ValueError('Registry endpoint requires raw Key')
            if item.get('label') is not None and not isinstance(item['label'], str):
                raise ValueError('label must be text or null')
            order = item.get('timestamp')
            import math
            if isinstance(order, bool) or not isinstance(order, (int,float)) or not math.isfinite(order):
                raise ValueError('normalize finite ordinal timestamp before ingest')
            counts['events'] += 1
            counts['registry'] += item['dstNode']['Type'] == 'Registry'
            counts['unlabeled'] += item.get('label') is None
        if not counts['events']:
            raise ValueError('empty source')
        sha = digest(path)
        if sha in hashes:
            raise ValueError('identical recording content listed twice')
        entries.append(dict(source,sha256=sha,expected_records=counts['events']))
        audit.append(dict(id=sid,**counts))
        ids.add(sid); paths.add(path); hashes.add(sha)
    if not entries:
        raise ValueError('no recordings')
    result = dict(schema='ants-sources-1', recordings=entries, audit=audit,
                  scope='Schema audit only; event labels do not establish activity membership or script independence.')
    write_json(output,result)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--spec',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    result=make_sources(args.root,json.loads(args.spec.read_text()),args.output)
    print(json.dumps(result['audit'],indent=2))


if __name__=='__main__':
    main()
