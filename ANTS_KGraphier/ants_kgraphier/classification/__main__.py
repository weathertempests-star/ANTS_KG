"""python -m ants_kgraphier.classification COMMAND --help"""
import argparse
import json
from pathlib import Path
from types import SimpleNamespace

from ..io import write_json
from .data import prepare, audit_store, load_dataset
from .training import train, predict, evaluate


def compare(args):
    output = Path(args.output)
    output.mkdir(parents=True,exist_ok=False)
    (output/'.building').touch()
    matrix = dict(seeds=args.seeds, epochs=args.epochs, device=args.device, threads=args.threads,
                  data=str(args.data), complete=False)
    write_json(output/'matrix.json',matrix)
    rows = []
    for dataset in sorted(Path(args.data).glob('*/graphs.jsonl')):
        data = load_dataset(dataset.parent)
        encodings = {}
        for mode, kg in [('prior',False),('anchor',True),('counts',False),('pool',True),('rgcn',True),('rgcn',False)]:
            for seed in args.seeds:
                name = f'{dataset.parent.name}-{mode}-kg{int(kg)}-s{seed}'
                run = output/name
                options = SimpleNamespace(data=dataset.parent,output=run,mode=mode,no_kg=not kg,seed=seed,
                                          epochs=args.epochs,batch_size=32,patience=8,device=args.device,
                                          threads=args.threads,resume=None)
                train(options, data=data, encodings=encodings)
                inference = SimpleNamespace(data=dataset.parent,model=run,split='test',output=run/'test.json')
                report = evaluate(inference, data=data)
                inference.output = run/'predictions.jsonl'
                predict(inference, data=data)
                rows.append(dict(dataset=dataset.parent.name,mode=mode,kg=kg,seed=seed,
                                 balanced_accuracy=report['binary']['balanced_accuracy'],
                                 technique_macro_f1=report['technique_oracle']['macro_f1'],
                                 technique_e2e_micro_f1=report['technique_end_to_end']['micro_f1'],
                                 report=str(run/'test.json')))
                write_json(output/'comparison.json',rows)
        del data, encodings
    if not rows:
        raise ValueError('no prepared extractor datasets found')
    header = '| Dataset | Model | KG | Seed | Binary balanced accuracy | Technique macro-F1 |\n|---|---|---|---|---|---|\n'
    (output/'comparison.md').write_text(header + ''.join(
        f"| {r['dataset']} | {r['mode']} | {r['kg']} | {r['seed']} | {r['balanced_accuracy']} | {r['technique_macro_f1']} |\n" for r in rows))
    matrix.update(complete=True, runs=len(rows))
    write_json(output/'matrix.json',matrix)
    (output/'.building').unlink()
    return dict(runs=len(rows),output=str(output))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    for command in ('prepare','audit'):
        p = sub.add_parser(command)
        p.add_argument('--store',required=True,type=Path)
        p.add_argument('--splits',type=Path,default=Path('ANTS_KGraphier/configs/segmentation-splits.json'))
        p.add_argument('--output',required=True,type=Path)
        if command=='prepare':
            p.add_argument('--kg',type=Path,default=Path('artifacts/knowledge-vault/kg.json'))
            p.add_argument('--per-recording',type=int,default=2000)
            p.add_argument('--seed',type=int,default=17)
            p.add_argument('--budgets',type=int,nargs='+',default=[33,128])
    p = sub.add_parser('train')
    p.add_argument('--data',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--mode',choices=['prior','anchor','counts','pool','rgcn'],default='rgcn')
    p.add_argument('--no-kg',action='store_true')
    p.add_argument('--seed',type=int,default=17)
    p.add_argument('--epochs',type=int,default=50)
    p.add_argument('--batch-size',type=int,default=32)
    p.add_argument('--patience',type=int,default=8)
    p.add_argument('--device',default='cpu')
    p.add_argument('--threads',type=int,default=1)
    p.add_argument('--resume',type=Path)
    for command in ('predict','evaluate'):
        p = sub.add_parser(command)
        p.add_argument('--data',type=Path,required=True)
        p.add_argument('--model',type=Path,required=True)
        p.add_argument('--split',choices=['train','validation','test','all'],default='test')
        p.add_argument('--output',type=Path,required=True)
    p = sub.add_parser('compare')
    p.add_argument('--data',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--seeds',type=int,nargs='+',default=[7,17,27])
    p.add_argument('--epochs',type=int,default=50)
    p.add_argument('--device',default='cpu')
    p.add_argument('--threads',type=int,default=1)
    args = parser.parse_args()
    for key in ('epochs','batch_size','patience','threads','per_recording'):
        if hasattr(args,key) and getattr(args,key)<1:
            parser.error(key+' must be positive')
    if hasattr(args,'budgets') and (min(args.budgets)<1 or len(set(args.budgets))!=len(args.budgets)):
        parser.error('budgets must be distinct positive integers')
    if args.command=='audit':
        result = audit_store(args.store,json.loads(args.splits.read_text()))
        write_json(args.output,result)
        print(json.dumps(dict(recordings=len(result['recordings']),unknown_labels=len(result['unknown_labels']),
                              cross_split_duplicates=len(result['cross_split_exact_events']))))
    else:
        result = dict(prepare=prepare,train=train,predict=predict,evaluate=evaluate,compare=compare)[args.command](args)
        print(json.dumps({k:v for k,v in result.items() if k in ('output','runs','graphs','validation_score','validation_usable','binary')},ensure_ascii=False))


if __name__=='__main__':
    main()
