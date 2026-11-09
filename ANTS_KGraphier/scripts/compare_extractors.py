"""Paired label-independent extraction diagnostics; not boundary accuracy."""
import argparse
from collections import Counter
from pathlib import Path
import time
from ants_kgraphier.io import jsonl,write_json
from ants_kgraphier.knowledge import Knowledge
from ants_kgraphier.store import connect
from ants_kgraphier.extract import extract,validate_graph


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--store',type=Path,required=True)
    p.add_argument('--anchors',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--kg',type=Path,default=Path('artifacts/knowledge-vault/kg.json'))
    p.add_argument('--per-recording',type=int,default=4)
    args=p.parse_args()
    if args.output.exists(): raise FileExistsError(args.output)
    if args.per_recording < 1: raise ValueError('sample size must be positive')
    counts=Counter(); anchors=[]
    for g in jsonl(args.anchors):
        rec=g['recording_sha256']
        if counts[rec]>=args.per_recording: continue
        counts[rec]+=1; anchors.append((rec,g['anchor_row']))
    kg=Knowledge(args.kg); reports=[]
    with connect(args.store) as db:
        for rec,row in anchors:
            for method in ('temporal','trec'):
                start=time.perf_counter()
                g=extract(db,rec,row,kg,method=method,hops=2,fanout=8,budget=33)
                seconds=time.perf_counter()-start
                validate_graph(g,db,kg)
                reports.append(dict(recording=rec,anchor_row=row,method=method,events=len(g['events']),
                                    clipped=g['budget_truncated'],seconds=seconds,
                                    max_hop=max(e['selection']['hop'] for e in g['events']),
                                    diagnostics=g.get('sampling_diagnostics')))
    summary={}
    for method in ('temporal','trec'):
        rows=[r for r in reports if r['method']==method]
        summary[method]=dict(graphs=len(rows),mean_events=sum(r['events'] for r in rows)/len(rows),
                             clipped=sum(r['clipped'] for r in rows),seconds=sum(r['seconds'] for r in rows),
                             max_hop=max(r['max_hop'] for r in rows))
    result=dict(scope='Same anchors and budget; first N anchors per recording from supplied corpus. No accuracy claim or label use.',
                settings=dict(hops=2,fanout=8,budget=33),timing_limitation='Temporal runs before trec for each anchor; cache/order effects are uncontrolled. Timings are diagnostic, not a speedup estimate.',summary=summary,records=reports)
    write_json(args.output,result)
    print(summary)


if __name__=='__main__': main()
