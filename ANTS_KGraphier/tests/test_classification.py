"""Classification semantics, feature isolation and deterministic training."""
import copy
import json
from pathlib import Path
import tempfile
import sqlite3
from types import SimpleNamespace
import unittest

import torch

from ants_kgraphier.io import canonical
from ants_kgraphier.classification.data import parse_label, supervision, load_dataset, prepare, audit_store
from ants_kgraphier.classification.model import encode, vocabulary, Classifier, targets
from ants_kgraphier.classification.metrics import binary_metrics, evaluate_rows, dependency_bootstrap
from ants_kgraphier.classification.training import train, load_checkpoint, infer


def graph(rec='r', row=0, split='train'):
    events = [dict(row=row+i,event_id=f'{rec}:{row+i}',rec=rec,src='actor',dst='key'+str(i),
                   src_type='Process',dst_type='Registry',op='RegSetValue',ord=i,
                   knowledge=dict(node_ids=['prefix']),raw_key='secret') for i in range(2)]
    return dict(id=f'{rec}-{row}',recording_sha256=rec,dependency_group=rec,split=split,
                events=events,anchor_row=row,anchor_event_id=f'{rec}:{row}',kg_sha256='kg',
                budget_truncated=False,settings=dict(method='temporal',budget=33))


def dataset(path):
    with (path/'graphs.jsonl').open('w') as gf, (path/'labels.jsonl').open('w') as lf:
        for split in ('train','validation','test'):
            for i in range(4):
                g = graph(split,i*2,split)
                labels = {i*2:'T1547.001' if i%2 else 'benign',i*2+1:'benign'}
                gf.write(canonical(g)+'\n')
                lf.write(canonical(supervision(g,labels))+'\n')


class ClassificationTests(unittest.TestCase):
    def test_label_union_unknown_and_unseen(self):
        g=graph()
        a=supervision(g,{0:'T1547.001_instance',1:'T1016'})
        self.assertEqual(a['techniques'],['T1016','T1547'])
        self.assertEqual(parse_label('T1547.001_bogus!')['status'],'unknown')
        a=supervision(g,{0:'T1547.001',1:None})
        self.assertEqual(a['binary'],1)
        y,m=targets(a,['T1547','T1112'])
        self.assertEqual(m.tolist(),[1,1,0])
        report=evaluate_rows([(g,a)],[[.8,.7]],['T1112'],(.5,.5))
        self.assertEqual(report['uncovered_techniques']['T1547']['events'],1)
        a=supervision(g,{0:'benign',1:'malformed'})
        self.assertIsNone(a['binary'])

    def test_features_and_no_edges(self):
        g=graph()
        v=vocabulary([(g,{})])
        original=encode(g,v)
        changed=copy.deepcopy(g)
        changed.update(id='private',recording_sha256='private',sampling='private',label='T1112')
        for e in changed['events']:
            e.update(raw_key='different',raw_sha='different',timestamp_raw=999,label='T1112',name='private')
            e['ord']=e['ord']*100+50
        encoded=encode(changed,v)
        for x,y in zip(original[:3],encoded[:3]):
            self.assertTrue(torch.equal(x,y))
        self.assertEqual(encode(g,v,False)[0].shape,original[0].shape)
        unknown=copy.deepcopy(g)
        unknown['events'][0]['op']='Never seen'
        self.assertEqual(encode(unknown,v)[0][0,len(v['kind'])].item(),1)
        model=Classifier(original[0].shape[1],2).eval()
        no_edge=(original[0],torch.empty(3,0,dtype=torch.long),original[2],original[3])
        self.assertTrue(torch.isfinite(model(no_edge)).all())
        # Disjoint union batching is invariant to other graphs and has no padding.
        self.assertTrue(torch.allclose(model.forward_batch([original,no_edge])[0],model(original), atol=1e-6))
        self.assertTrue(torch.allclose(model.forward_batch([original,no_edge])[1],model(no_edge), atol=1e-6))

    def test_metrics_hand_calculated_and_ties(self):
        m=binary_metrics([1,1,0,0],[.9,.4,.8,.1])
        self.assertEqual(m['balanced_accuracy'],.5)
        self.assertEqual(m['f1'],.5)
        self.assertEqual(m['confusion_matrix'],[[1,1],[1,1]])
        self.assertAlmostEqual(m['pr_auc'],5/6)
        self.assertEqual(binary_metrics([1,0],[.5,.5])['pr_auc'],.5)
        self.assertIsNone(binary_metrics([0,0],[.1,.2])['balanced_accuracy'])

    def test_dependency_bootstrap_resamples_groups(self):
        data, predictions = [], []
        for rid in ('a', 'b'):
            for i in range(2):
                g = graph(rid, i*2, 'test')
                a = supervision(g, {i*2: 'T1112' if i else 'benign', i*2+1: 'benign'})
                data.append((g, a))
                predictions.append([.9 if i else .1, .9 if i else .1])
        report = dependency_bootstrap(data, predictions, ['T1112'], (.5, .5), repeats=30)
        self.assertEqual(report['groups'], 2)
        self.assertEqual(report['intervals']['binary.balanced_accuracy'],
                         dict(low=1., high=1., valid_replicates=30))
        self.assertEqual(report, dependency_bootstrap(data, predictions, ['T1112'], (.5, .5), repeats=30))

    def test_gated_techniques_and_model_controls(self):
        g=graph()
        label=supervision(g,{0:'T1547.001',1:'benign'})
        report=evaluate_rows([(g,label)],[[.1,.9,.2]],['T1547','T1112'],(.5,.5))
        self.assertEqual(report['technique_oracle']['macro_f1'],1)
        self.assertEqual(report['technique_end_to_end']['micro_f1'],0)
        self.assertEqual(report['technique_oracle']['balanced_accuracy_classes'],0)
        vocab=vocabulary([(g,label)])
        encoded=encode(g,vocab)
        for mode in ('anchor','counts','pool','rgcn'):
            for classes in (0,2):
                model=Classifier(encoded[0].shape[1],classes,mode).eval()
                self.assertEqual(tuple(model.forward_batch([encoded,encoded]).shape),(2,classes+1))
        changed=copy.deepcopy(g)
        changed.update(split='test')
        changed['events'][0]['op']='TestOnlyOperation'
        self.assertNotIn('TestOnlyOperation',vocabulary([(g,label),(changed,label)])['operation'])

    def test_leakage_and_all_negative_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            dataset(path)
            rows=[json.loads(x) for x in (path/'graphs.jsonl').read_text().splitlines()]
            rows[-1]['dependency_group']='train'
            (path/'graphs.jsonl').write_text(''.join(canonical(g)+'\n' for g in rows))
            with self.assertRaisesRegex(ValueError,'leakage'):
                load_dataset(path)
            dataset(path)
            labels=[json.loads(x) for x in (path/'labels.jsonl').read_text().splitlines()]
            for a in labels:
                if a['graph_id'].startswith('validation'):
                    a['binary']=0
            (path/'labels.jsonl').write_text(''.join(canonical(a)+'\n' for a in labels))
            with self.assertRaisesRegex(ValueError,'validation'):
                train(self.options(path,path/'model'))

    def test_preparation_shared_anchors_and_duplicate_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            store=path/'events.sqlite'
            with sqlite3.connect(store) as db:
                db.executescript("CREATE TABLE recordings(id TEXT,data TEXT); "
                    "CREATE TABLE events(rec TEXT,row INTEGER,ord REAL,src TEXT,dst TEXT,src_type TEXT,dst_type TEXT,op TEXT,raw_key TEXT,raw_sha TEXT); "
                    "CREATE TABLE labels(rec TEXT,row INTEGER,label TEXT);")
                for split in ('train','validation','test'):
                    db.execute('INSERT INTO recordings VALUES(?,?)',(split,canonical(dict(id=split,store_id=split,dependency_group=split))))
                    for row in range(4):
                        db.execute('INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?,?)',
                            (split,row,row,f'{split}:src:{row}',f'{split}:dst:{row}','Process','Registry','RegSetValue','key',f'{split}:{row}'))
                        db.execute('INSERT INTO labels VALUES(?,?,?)',(split,row,'T1112' if row%2 else 'benign'))
            (path/'kg.json').write_text('{"nodes":[]}')
            splits={s:s for s in ('train','validation','test')}
            (path/'splits.json').write_text(json.dumps(splits))
            prepare(SimpleNamespace(store=store,splits=path/'splits.json',kg=path/'kg.json',
                                    output=path/'prepared',budgets=[33,128],seed=17,per_recording=1))
            identities=[]
            for directory in sorted((path/'prepared').glob('*-*')):
                if not directory.is_dir():
                    continue
                data=load_dataset(directory)
                identities.append([(g['recording_sha256'],g['anchor_row']) for g,a in data])
                self.assertEqual({a['binary'] for g,a in data if g['split']=='validation'},{0,1})
                self.assertEqual(sum(g['split']=='test' for g,a in data),1)
                self.assertEqual(sum(g['split']=='train' for g,a in data),1)
            self.assertEqual(len(identities),6)
            self.assertTrue(all(x==identities[0] for x in identities))
            with sqlite3.connect(store) as db:
                db.execute("UPDATE events SET raw_sha='duplicate' WHERE row=0")
            self.assertEqual(len(audit_store(store,splits)['cross_split_exact_events']),1)

    def test_validation_support_is_split_wide(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            store = path/'events.sqlite'
            splits = {'train': 'train', 'test': 'test', 'val-a': 'validation', 'val-b': 'validation'}
            with sqlite3.connect(store) as db:
                db.executescript("CREATE TABLE recordings(id TEXT,data TEXT); "
                    "CREATE TABLE events(rec TEXT,row INTEGER,ord REAL,src TEXT,dst TEXT,src_type TEXT,dst_type TEXT,op TEXT,raw_key TEXT,raw_sha TEXT); "
                    "CREATE TABLE labels(rec TEXT,row INTEGER,label TEXT);")
                for rid in splits:
                    db.execute('INSERT INTO recordings VALUES(?,?)', (rid, canonical(dict(id=rid,store_id=rid,dependency_group=rid))))
                    for row in range(3):
                        db.execute('INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?,?)',
                                   (rid,row,row,f'{rid}:p:{row}',f'{rid}:r:{row}','Process','Registry','Write','key',f'{rid}:{row}'))
                        db.execute('INSERT INTO labels VALUES(?,?,?)', (rid,row,'T1112' if rid=='val-b' else 'benign'))
            (path/'kg.json').write_text('{"nodes":[]}')
            (path/'splits.json').write_text(json.dumps(splits))
            result = prepare(SimpleNamespace(store=store,splits=path/'splits.json',kg=path/'kg.json',
                                             output=path/'prepared',budgets=[33],seed=17,per_recording=1))
            self.assertTrue(result['validation_usable'])
            anchors = json.loads((path/'prepared'/'anchors.json').read_text())
            self.assertEqual(len(anchors), 4)
            self.assertEqual({a['sampling'] for a in anchors}, {'uniform'})

    def test_compare_command_artifacts(self):
        from ants_kgraphier.classification.__main__ import compare
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            data=path/'data'/'temporal-33'
            data.mkdir(parents=True)
            dataset(data)
            result=compare(SimpleNamespace(data=data.parent,output=path/'runs',seeds=[7],epochs=1,
                                           device='cpu',threads=1))
            self.assertEqual(result['runs'],6)
            self.assertFalse((path/'runs'/'.building').exists())
            self.assertTrue(json.loads((path/'runs'/'matrix.json').read_text())['complete'])
            rows=json.loads((path/'runs'/'comparison.json').read_text())
            self.assertEqual({r['mode'] for r in rows},{'prior','anchor','counts','pool','rgcn'})
            self.assertEqual(len(list((path/'runs').glob('*/predictions.jsonl'))),6)

    def options(self,data,output,epochs=2,resume=None):
        return SimpleNamespace(data=data,output=output,epochs=epochs,resume=resume,mode='rgcn',
                               seed=7,no_kg=False,device='cpu',threads=1,batch_size=2,patience=8)

    def test_resume_and_inference(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            dataset(path)
            train(self.options(path,path/'full'))
            train(self.options(path,path/'first',epochs=1))
            train(self.options(path,path/'resumed',resume=path/'first'/'last.pt'))
            full=load_checkpoint(path/'full'/'last.pt')
            resumed=load_checkpoint(path/'resumed'/'last.pt')
            self.assertEqual(full['history'],resumed['history'])
            for key in full['state']:
                self.assertTrue(torch.equal(full['state'][key],resumed['state'][key]),key)
            data,p,config,thresholds=infer(path,path/'resumed')
            self.assertEqual(len(p),4)
            self.assertEqual(config['classes'],['T1547'])


if __name__=='__main__':
    unittest.main()
