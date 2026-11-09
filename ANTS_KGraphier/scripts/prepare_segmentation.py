"""Prepare reproducible local candidates, blank review forms, and weak supervision.

Uniform Registry samples are supplemented with labeled anchors for TRAIN ONLY.
Weak labels are hypotheses, never gold activity boundaries. Label metadata is
stored solely in annotations, never in candidate model features.
"""
import argparse
import json
from pathlib import Path
import random

from ants_kgraphier.io import canonical, write_json, digest
from ants_kgraphier.store import connect, recordings
from ants_kgraphier.extract import extract
from ants_kgraphier.knowledge import Knowledge
from ants_kgraphier.segmentation.annotations import template


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--store', type=Path, required=True)
    p.add_argument('--kg', type=Path, default=Path('artifacts/knowledge-vault/kg.json'))
    p.add_argument('--splits', type=Path, default=Path('ANTS_KGraphier/configs/segmentation-splits.json'))
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--per-recording', type=int, default=40)
    p.add_argument('--train-labeled', type=int, default=40)
    p.add_argument('--method',choices=['temporal','trec','window'],default='temporal')
    p.add_argument('--budget', type=int, default=128)
    p.add_argument('--seed', type=int, default=17)
    args = p.parse_args()
    if args.per_recording < 1 or args.train_labeled < 0:
        p.error('invalid sampling sizes')
    splits = json.loads(args.splits.read_text())
    kg = Knowledge(args.kg)
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/'.building').touch()
    reports = []
    with connect(args.store) as db, (args.output/'graphs.jsonl').open('x') as gf, (args.output/'review.jsonl').open('x') as rf, (args.output/'weak.jsonl').open('x') as wf:
        for rec in recordings(db):
            rid = rec['store_id']
            split = splits[rec['dependency_group']]
            count = db.execute("SELECT count(*) FROM events WHERE rec=? AND dst_type='Registry'", (rid,)).fetchone()[0]
            rng = random.Random(str(args.seed)+rid)
            positions = set(rng.sample(range(count), min(count,args.per_recording)))
            chosen = {r[0]:'uniform' for i,r in enumerate(db.execute("SELECT row FROM events WHERE rec=? AND dst_type='Registry' ORDER BY row", (rid,))) if i in positions}
            if split == 'train' and args.train_labeled:
                labeled = [r[0] for r in db.execute("SELECT e.row FROM events e JOIN labels l ON e.rec=l.rec AND e.row=l.row WHERE e.rec=? AND e.dst_type='Registry' AND l.label IS NOT NULL AND lower(l.label)!='benign' ORDER BY e.row", (rid,))]
                for row in rng.sample(labeled, min(len(labeled),args.train_labeled)):
                    chosen.setdefault(row, 'training_label_enrichment')
            reviewed = 0
            for row, sampling in sorted(chosen.items()):
                g = extract(db,rid,row,kg,method=args.method,hops=3,fanout=16,budget=args.budget)
                g.update(split=split,dependency_group=rec['dependency_group'],sampling=sampling)
                gf.write(canonical(g)+'\n')
                a = template(g)
                rf.write(canonical(a)+'\n')
                anchor = next(e for e in g['events'] if e['row']==row)
                labels = {e['row']:db.execute('SELECT label FROM labels WHERE rec=? AND row=?',(rid,e['row'])).fetchone()[0] for e in g['events']}
                label = labels[row]
                a.update(provenance='weak_rule',reviewer='same-annotation-actor-v1',episode_id=g['id'])
                # Same label is only weak evidence, not an invocation ID.
                for e in g['events']:
                    role = 'unknown'
                    if e['row']==row:
                        role = 'core'
                    elif label and label.lower()!='benign' and labels[e['row']]==label and e['src']==anchor['src']:
                        role = 'context'
                    elif e['src']!=anchor['src']:
                        role = 'unrelated'
                    a['memberships'].append(dict(event_id=e['event_id'],role=role,confidence=.25))
                wf.write(canonical(a)+'\n')
                reviewed += 1
            reports.append(dict(recording=rec['id'],split=split,population=count,candidates=reviewed))
    write_json(args.output/'manifest.json',dict(schema='segmentation-preparation-1',recordings=reports,
        seed=args.seed,kg_sha256=kg.sha256,splits=splits,graphs_sha256=digest(args.output/'graphs.jsonl'),
        weak_sha256=digest(args.output/'weak.jsonl'),
        limitation='Weak actor/annotation hypotheses only. Benign does not imply irrelevant. Episode IDs are per-anchor proxies. Script reuse audit remains pending.'))

    (args.output/'.building').unlink()


if __name__=='__main__':
    main()
