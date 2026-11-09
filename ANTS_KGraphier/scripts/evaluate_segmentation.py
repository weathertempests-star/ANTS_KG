"""Fixed-candidate, fixed-budget comparisons and source event verification."""
import argparse
from pathlib import Path
import torch
from ants_kgraphier.io import jsonl, write_json
from ants_kgraphier.store import connect, event
from ants_kgraphier.segmentation.training import load_dataset, load_model, evaluate


class Nearest(torch.nn.Module):
    def forward(self, x, edges, anchor):
        return -abs(x[:,113])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run',type=Path,required=True)
    p.add_argument('--store',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    report={'scope':'Local weak supervision only; unknown context is unscored, not irrelevant.'}
    for name in ('model-kg-complete','model-no-kg'):
        model,config=load_model(args.run/name)
        data=[d for d in load_dataset(args.run/'graphs.jsonl',args.run/'weak.jsonl',config['use_kg']) if d[0]['split']=='test']
        report[name]=evaluate(model,data,config['budget'],config['threshold'])
    report['nearest-budget32']=evaluate(Nearest(),data,32,0.)
    report['anchor-only']=evaluate(Nearest(),data,32,1.)
    verified=0
    with connect(args.store) as db:
        for g in jsonl(args.run/'selected.jsonl'):
            assert len(g['events'])<=g['selection_config']['budget']
            assert g['anchor_event_id'] in {e['event_id'] for e in g['events']}
            for e in g['events']:
                source=event(db,g['recording_sha256'],e['row'])
                if any(e[k]!=v for k,v in source.items()):
                    raise ValueError('selected event differs from source index')
                verified+=1
    report['verified_selected_events']=verified
    write_json(args.output,report)
    print({k:v['metrics'] for k,v in report.items() if isinstance(v,dict) and 'metrics' in v})
    print('Verified source events:',verified)


if __name__=='__main__':
    main()
