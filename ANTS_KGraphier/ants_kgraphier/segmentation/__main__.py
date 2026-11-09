import argparse
from pathlib import Path
from ..io import jsonl, write_json, canonical
from .annotations import template
from .training import train, select, load_model, load_dataset, evaluate


def main():
    parser = argparse.ArgumentParser(description='Learned event membership selection')
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('templates', 'train', 'select', 'evaluate'):
        p = sub.add_parser(name)
        p.add_argument('--graphs', type=Path, required=True)
        p.add_argument('--output', type=Path, required=True)
        if name in ('train', 'evaluate'):
            p.add_argument('--annotations', type=Path, required=True)
        if name in ('select', 'evaluate'):
            p.add_argument('--model', type=Path, required=True)
        if name != 'templates':
            p.add_argument('--device', default='cpu')
        if name == 'train':
            p.add_argument('--epochs', type=int, default=20)
            p.add_argument('--seed', type=int, default=7)
            p.add_argument('--budget', type=int, default=32)
            p.add_argument('--no-kg', action='store_true')
            p.add_argument('--selection-metric', choices=['macro_context_f1','macro_f1'], default='macro_context_f1')
            p.add_argument('--resume', type=Path)
            p.add_argument('--pretrain-epochs', type=int, default=0)
            p.add_argument('--stochastic', action='store_true')
        if name == 'evaluate':
            p.add_argument('--split', choices=['validation','test'], default='test')
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    if args.command == 'templates':
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as f:
            for g in jsonl(args.graphs):
                f.write(canonical(template(g))+'\n')
    elif args.command == 'train':
        train(args.graphs, args.annotations, args.output, epochs=args.epochs, seed=args.seed,
              budget=args.budget, use_kg=not args.no_kg, device=args.device, selection_metric=args.selection_metric, resume=args.resume, pretrain_epochs=args.pretrain_epochs, stochastic=args.stochastic)
    elif args.command == 'select':
        print(canonical(select(args.graphs, args.model, args.output, args.device)))
    else:
        model, config = load_model(args.model, args.device)
        dataset = load_dataset(args.graphs, args.annotations, config['use_kg'])
        data = dataset.view(args.split)
        if not data:
            raise ValueError('no reviewed examples in requested split')
        result = evaluate(model, data, config['budget'], config['threshold'], args.device)
        result['split'] = args.split
        result['weights_sha256'] = config['weights_sha256']
        write_json(args.output, result)
        dataset.close()


if __name__ == '__main__':
    main()
