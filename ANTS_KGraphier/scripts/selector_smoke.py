"""Executable local plumbing check, NOT scientific segmentation evaluation.

Uses explicitly synthetic membership based on operation/actor agreement on real
recorded candidates. Scores measure this rule only; no manual labels invented.
"""
import argparse
from collections import Counter
from pathlib import Path

from ants_kgraphier.io import jsonl, canonical, write_json
from ants_kgraphier.segmentation.annotations import template
from ants_kgraphier.segmentation.training import train, select, load_model, load_dataset, evaluate


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--graphs', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    counts = Counter()
    graph_path, annotation_path = args.output/'graphs.jsonl', args.output/'annotations.jsonl'
    with graph_path.open('x') as gf, annotation_path.open('x') as af:
        for g in jsonl(args.graphs):
            group = g['dependency_group']
            if counts[group] >= 8:
                continue
            counts[group] += 1
            # Leave whole dependency groups intact. Existing pilot tests are
            # already seen; this dataset is never advertised as blind testing.
            if group.startswith('CHT-2b294'):
                g['split'] = 'validation'
            anchor = next(e for e in g['events'] if e['event_id'] == g['anchor_event_id'])
            a = template(g)
            a.update(episode_id=g['id'], provenance='weak_rule', reviewer='smoke-actor-operation-v1', complete=True)
            a['memberships'] = [dict(event_id=e['event_id'], role='core' if e['src']==anchor['src'] and e['op']==anchor['op'] else 'unrelated', confidence=.25) for e in g['events']]
            gf.write(canonical(g)+'\n')
            af.write(canonical(a)+'\n')
    train(graph_path, annotation_path, args.output/'model', epochs=3, budget=16, selection_metric='macro_f1')
    select(graph_path, args.output/'model', args.output/'selected.jsonl')
    model, config = load_model(args.output/'model')
    test = [d for d in load_dataset(graph_path, annotation_path) if d[0]['split']=='test']
    report = evaluate(model, test, config['budget'], config['threshold'])
    report['warning'] = 'Plumbing smoke only: synthetic actor/operation agreement supervision; not human activity boundaries or malicious labels.'
    write_json(args.output/'smoke.json', report)


if __name__ == '__main__':
    main()
