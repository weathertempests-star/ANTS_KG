import unittest
from unittest.mock import patch
from ants_kgraphier.trec import sample


def event(row, op='ReadFile'):
    return dict(row=row,ord=row,src=str(row),dst=str(row+1),op=op)


class TrecTests(unittest.TestCase):
    def run_chain(self, poi=False, budget=20, mode='offline'):
        data=[event(i,'RegSetValue' if poi and i==2 else 'ReadFile') for i in range(7)]
        def neighbors(db, rec, node, order, direction, limit):
            return [e for e in data if node in {e['src'],e['dst']} and
                    (e['ord']<order if direction=='before' else e['ord']>order)][:limit]
        with patch('ants_kgraphier.extract.neighbors',neighbors):
            return sample(None,'r',data[0],2,2,budget,mode)

    def test_stop_and_poi_restart(self):
        selected,_,stats=self.run_chain()
        self.assertEqual(set(selected),{0,1,2})
        self.assertGreater(stats['branch_stops'],0)
        selected,reasons,stats=self.run_chain(poi=True)
        self.assertEqual(set(selected),{0,1,2,3,4})
        self.assertEqual(reasons[2]['gap_since_poi'],0)
        self.assertEqual(stats['poi_hits'],1)

    def test_budget_past_and_unknown_order(self):
        selected,_,stats=self.run_chain(poi=True,budget=2)
        self.assertEqual(len(selected),2)
        self.assertTrue(stats['budget_truncated'])
        self.assertEqual(set(self.run_chain(mode='past')[0]),{0})
        a=event(0); a['ord']=None
        self.assertEqual(set(sample(None,'r',a,2,2,20,'offline')[0]),{0})
