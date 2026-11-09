import copy
import unittest

import torch

from ants_kgraphier.segmentation.annotations import template, targets, validate_splits
from ants_kgraphier.segmentation.model import encode, Selector, stochastic_mask, bernoulli_kl
from ants_kgraphier.segmentation.decode import decode


def graph():
    events = []
    for i, (src, dst) in enumerate([('a', 'b'), ('b', 'c'), ('c', 'd'), ('x', 'y')]):
        events.append(dict(event_id=f'r:{i}', row=i, ord=i, src=src, dst=dst,
                           src_type='Process', dst_type='Registry', op='RegSetValue', knowledge=None))
    return dict(id='g', recording_sha256='r', anchor_event_id='r:0', anchor_row=0,
                events=events, dependency_group='d', split='train')


class SegmentationTests(unittest.TestCase):
    def test_unknown_not_negative(self):
        g = graph()
        a = template(g)
        self.assertEqual(targets(a, g)[1], [0.] * 4)
        a.update(episode_id='e', reviewer='test', memberships=[{'event_id':'r:0','role':'core'}])
        self.assertEqual(targets(a, g)[1], [1., 0., 0., 0.])

    def test_split_leakage(self):
        with self.assertRaises(ValueError):
            validate_splits([graph(), dict(graph(), split='test')])

    def test_connector_and_budget(self):
        g = graph()
        out = decode(g, [.1, .1, .9, .99], budget=3)
        self.assertEqual([e['row'] for e in out['events']], [0, 1, 2])
        self.assertEqual(out['events'][1]['learned_selection']['role'], 'connector')
        self.assertEqual(len(decode(g, [.1, .1, .9, .99], budget=2)['events']), 1)
        self.assertEqual(len(g['events']), 4)

    def test_labels_and_names_not_features(self):
        g = graph()
        other = copy.deepcopy(g)
        for e in other['events']:
            e.update(label='attack', timestamp_raw='secret', Name='malware.exe')
        self.assertTrue(torch.equal(encode(g)[0], encode(other)[0]))

    def test_gradient_and_deterministic_eval(self):
        torch.manual_seed(7)
        model = Selector(16)
        args = encode(graph())
        logits = model(*args)
        loss = stochastic_mask(logits).sum() + bernoulli_kl(logits)
        loss.backward()
        self.assertTrue(any(p.grad.abs().sum() > 0 for p in model.parameters()))
        self.assertTrue(torch.equal(stochastic_mask(logits, training=False), logits.sigmoid()))

    def test_resume_matches_uninterrupted(self):
        import tempfile
        from pathlib import Path
        from ants_kgraphier.io import canonical
        from ants_kgraphier.segmentation.training import train, load_model
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            graphs, annotations = [], []
            for split in ('train', 'validation', 'test'):
                g = graph()
                g.update(id=split, recording_sha256=split, dependency_group=split, split=split,
                         anchor_event_id=split+':0')
                for e in g['events']:
                    e['event_id'] = split+':'+str(e['row'])
                a = template(g)
                a.update(episode_id=split, reviewer='fixture', complete=True,
                         memberships=[dict(event_id=e['event_id'],role='core' if e['row']==0 else 'context' if e['row']==1 else 'unrelated') for e in g['events']])
                graphs.append(g); annotations.append(a)
            gp, ap = root/'graphs.jsonl', root/'annotations.jsonl'
            gp.write_text(''.join(canonical(g)+'\n' for g in graphs))
            ap.write_text(''.join(canonical(a)+'\n' for a in annotations))
            train(gp,ap,root/'full',epochs=2,hidden=8,pretrain_epochs=1,stochastic=True)
            train(gp,ap,root/'first',epochs=1,hidden=8,pretrain_epochs=1,stochastic=True)
            train(gp,ap,root/'resumed',epochs=2,hidden=8,resume=root/'first/last.pt',pretrain_epochs=1,stochastic=True)
            full,_=load_model(root/'full'); resumed,_=load_model(root/'resumed')
            for key,value in full.state_dict().items():
                self.assertTrue(torch.equal(value,resumed.state_dict()[key]))
            # Compare final optimizer-step model too, not only the best epoch.
            a=torch.load(root/'full/last.pt',weights_only=True)
            b=torch.load(root/'resumed/last.pt',weights_only=True)
            for key,value in a['model'].items():
                self.assertTrue(torch.equal(value,b['model'][key]))

    def test_ties_have_no_precedence(self):
        g = graph()
        for e in g['events']:
            e['ord'] = 1
        self.assertEqual(encode(g)[1].shape, (2, 0))


if __name__ == '__main__':
    unittest.main()
