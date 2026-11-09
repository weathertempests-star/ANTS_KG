"""Re-extract a deterministic stratified sample and trace its manual labels."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import random

from ants_kgraphier.classification.data import read_jsonl, supervision
from ants_kgraphier.extract import validate_graph
from ants_kgraphier.io import digest, write_json
from ants_kgraphier.knowledge import Knowledge
from ants_kgraphier.store import connect


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data',type=Path,required=True)
    p.add_argument('--store',type=Path,required=True)
    p.add_argument('--kg',type=Path,default=Path('artifacts/knowledge-vault/kg.json'))
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--per-split',type=int,default=5)
    args=p.parse_args()
    if args.per_split<1:
        p.error('per-split must be positive')
    manifest=json.loads((args.data/'manifest.json').read_text())
    anchor_rows=json.loads((args.data/'anchors.json').read_text())
    expected={(a['recording'],a['row'],a['split']) for a in anchor_rows}
    kg=Knowledge(args.kg)
    reports=[]
    with connect(args.store) as db:
        for path in sorted(args.data.glob('*/graphs.jsonl')):
            labels={a['graph_id']:a for a in read_jsonl(path.parent/'labels.jsonl')}
            rng=random.Random(17)
            chosen=defaultdict(list)
            counts=defaultdict(int)
            anchors=set()
            for g in read_jsonl(path):
                anchors.add((g['recording_sha256'],g['anchor_row'],g['split']))
                split=g['split']
                counts[split]+=1
                if len(chosen[split])<args.per_split:
                    chosen[split].append(g)
                else:
                    i=rng.randrange(counts[split])
                    if i<args.per_split:
                        chosen[split][i]=g
            if anchors!=expected or sum(counts.values())!=len(expected):
                raise ValueError('shared anchor list mismatch: '+str(path))
            for name in ('graphs.jsonl','labels.jsonl'):
                if digest(path.parent/name)!=manifest['files'][path.parent.name+'/'+name]:
                    raise ValueError('artifact hash mismatch')
            checked=[]
            for graphs in chosen.values():
                for g in graphs:
                    validate_graph(g,db,kg)
                    raw_labels={e['row']:db.execute('SELECT label FROM labels WHERE rec=? AND row=?',
                         (g['recording_sha256'],e['row'])).fetchone()[0] for e in g['events']}
                    actual=supervision(g,raw_labels)
                    if any(labels[g['id']][k]!=v for k,v in actual.items()):
                        raise ValueError('manual label mismatch: '+g['id'])
                    checked.append(g['id'])
            reports.append(dict(dataset=path.parent.name,graphs=sum(counts.values()),
                                reextracted=len(checked),checked_graph_ids=checked,shared_anchors=True,
                                manual_labels_match=True,hashes_match=True))
    write_json(args.output,dict(seed=17,per_split=args.per_split,results=reports))
    print(json.dumps(dict(datasets=len(reports),reextracted=sum(r['reextracted'] for r in reports))))


if __name__=='__main__':
    main()
