"""Acceptance checks for merging path evidence with independently authored knowledge."""
import copy
from collections import Counter
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from standardizer_pkg import KnowledgeBase

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'tests/fixtures/registry_seed_v1.json'
INVENTORY = ROOT / 'artifacts/registry-inventory/inventory.json'
TARGET = r'HKLM\System\CurrentControlSet\Control\Session Manager'
ORIGINAL_IDS = {
    'knowledge:23067446c79f6f808ec9de07', 'knowledge:0c0cbf02701df6d652a5dc75',
    'knowledge:47075c2ddad8552fd6d1728a', 'knowledge:cf70125942441319173f4965',
    'knowledge:7646fcec5941d5a9b6d3ef85', 'knowledge:67ee8ba9716dc0d7a0e5161f',
    'knowledge:1b4dc8589a4514f201b7f19e',
}


class InventoryKnowledgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kb = KnowledgeBase.load_catalog(CATALOG, INVENTORY)
        cls.inventory = json.loads(INVENTORY.read_text())

    def test_exact_counts_and_full_prefix_edges_match_inventory(self):
        graph = self.kb.to_dict()
        nodes = {n['id']: n for n in graph['nodes']}
        self.assertEqual((len(nodes), len(graph['edges'])), (197, 192))
        self.assertEqual(Counter(n['depth'] for n in nodes.values()),
                         {r['depth']: r['total_nodes'] for r in self.inventory['by_depth']})
        self.assertEqual({n['path'] for n in nodes.values()}, {n['path'] for n in self.inventory['nodes']})
        for edge in graph['edges']:
            self.assertEqual(edge['type'], 'HAS_CHILD')
            self.assertEqual(nodes[edge['source']]['canonical_components'], nodes[edge['target']]['canonical_components'][:-1])
        self.assertEqual(graph['provenance']['inventory_sha256'], hashlib.sha256(INVENTORY.read_bytes()).hexdigest())

    def test_original_ids_and_seven_explanations_are_preserved(self):
        old = KnowledgeBase.load_catalog(CATALOG).to_dict()['nodes']
        self.assertEqual({n['id'] for n in old}, ORIGINAL_IDS)
        new = {n['id']: n for n in self.kb.to_dict()['nodes']}
        for node in old:
            for field in ('explanation', 'role', 'status', 'explanation_sources', 'canonical_components'):
                self.assertEqual(node[field], new[node['id']][field])
        self.assertEqual(sum(n['status'] != 'pending' for n in new.values()), 7)

    def test_pending_nodes_keep_evidence_separate_and_tags_empty(self):
        nodes = self.kb.to_dict()['nodes']
        self.assertEqual(sum(n['status'] == 'pending' for n in nodes), 190)
        for n in nodes:
            self.assertTrue(n['path_sources'])
            self.assertEqual(n['candidate_tags'], [])
            if n['status'] == 'pending':
                self.assertEqual(n['explanation'], '')
                self.assertEqual(n['role'], '')
                self.assertEqual(n['explanation_sources'], [])
        forbidden = {'event_id', 'event', 'trace', 'malicious_example', 'benign_example', 'attack_id'}
        self.assertFalse(any(forbidden & set(n) for n in nodes))

    def test_pending_path_is_not_complete_semantic_knowledge(self):
        result = self.kb.resolve(r'HKLM\SOFTWARE', 'registry')
        self.assertTrue(result['path_complete'])
        self.assertFalse(result['explanations_complete'])
        self.assertFalse(result['complete'])
        self.assertEqual(result['steps'][-1]['match'], 'known')
        self.assertEqual(result['steps'][-1]['explanation_status'], 'pending')
        self.assertIsNotNone(result['steps'][-1]['node_id'])

    def test_session_manager_is_five_nodes_and_resolution_never_mutates(self):
        before = self.kb.to_dict()
        for raw in (TARGET, TARGET.upper(), TARGET.replace('HKLM', 'HKEY_LOCAL_MACHINE')) * 5:
            result = self.kb.resolve(raw, 'registry')
            self.assertTrue(result['path_complete'])
            self.assertTrue(result['explanations_complete'])
            self.assertEqual(len(result['path_node_ids']), 5)
            self.assertEqual(len(result['edges']), 4)
            result['steps'][0]['knowledge']['path_sources'].append('changed')
        self.assertEqual(before, self.kb.to_dict())

    def test_templates_remain_structural_and_do_not_match_concrete_names(self):
        nodes = self.kb.to_dict()['nodes']
        self.assertEqual(sum(n['template_dependent'] for n in nodes), 22)
        self.assertEqual(sum(n['is_placeholder'] for n in nodes), 12)
        concrete = self.kb.resolve(r'HKLM\SYSTEM\CurrentControlSet\Services\ExampleService\Parameters', 'registry')
        self.assertEqual([s['match'] for s in concrete['steps']], ['known'] * 4 + ['unknown'] * 2)
        self.assertFalse(concrete['path_complete'])
        literal = self.kb.resolve(r'HKLM\SYSTEM\CurrentControlSet\Services\<ServiceName>\Parameters', 'registry')
        self.assertTrue(literal['path_complete'])
        self.assertFalse(literal['explanations_complete'])
        self.assertEqual([s['match'] for s in literal['steps']][-2:], ['literal_template'] * 2)
        self.assertTrue(literal['warnings'])

    def test_empty_nonstring_unsupported_and_unknown_inputs(self):
        self.assertFalse(self.kb.resolve('', 'registry')['path_complete'])
        for value in (None, 10, []):
            with self.subTest(value=value), self.assertRaises(TypeError):
                self.kb.resolve(value, 'registry')
        with self.assertRaises(ValueError):
            self.kb.resolve('HKLM', 'network')
        self.assertFalse(self.kb.resolve(TARGET + r'\Unknown', 'registry')['path_complete'])
        self.assertFalse(self.kb.resolve('HKLM/SYSTEM', 'registry')['path_complete'])

    def test_inventory_tampering_fails_before_build(self):
        mutations = [
            lambda d: d['nodes'][0].update(depth=2),
            lambda d: d['nodes'][0].update(template_dependent=True),
            lambda d: d['nodes'][0].update(parent_path='HKLM'),
            lambda d: d['nodes'][0].update(sources=['https://example.org/unsupported']),
            lambda d: d['nodes'][0].update(explicitly_listed=False),
            lambda d: d['nodes'].append(copy.deepcopy(d['nodes'][0])),
            lambda d: d['summary'].update(nodes=198),
            lambda d: d['by_depth'][0].update(total_nodes=99),
            lambda d: d['explicit_paths'][0]['evidence'][0].update(path='HKLM'),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'inventory.json'
            for change in mutations:
                data = copy.deepcopy(self.inventory)
                change(data)
                path.write_text(json.dumps(data))
                with self.subTest(change=change), self.assertRaises(ValueError):
                    KnowledgeBase.load_catalog(CATALOG, path)

    def test_catalog_can_explain_a_node_using_inventory_parents(self):
        definition = dict(domain='registry', path=r'HKLM\SOFTWARE', role='test_fixture',
                          explanation='Authored fixture explanation.', sources=['https://example.org/fixture'], status='documented')
        with tempfile.TemporaryDirectory() as tmp:
            catalog = Path(tmp) / 'catalog.json'
            catalog.write_text(json.dumps({'schema': 'prefix-knowledge-1', 'definitions': [definition]}))
            kb = KnowledgeBase.load_catalog(catalog, INVENTORY)
            step = kb.resolve(r'HKLM\SOFTWARE', 'registry')['steps'][-1]
            self.assertEqual(step['knowledge']['explanation_sources'], definition['sources'])
            self.assertNotIn(definition['sources'][0], step['knowledge']['path_sources'])
            for definitions in ([definition, definition], [{**definition, 'path': r'HKLM\Uninventoried'}]):
                catalog.write_text(json.dumps({'schema': 'prefix-knowledge-1', 'definitions': definitions}))
                with self.assertRaises(ValueError):
                    KnowledgeBase.load_catalog(catalog, INVENTORY)

    def test_snapshot_rejects_fabricated_pending_explanation_tags_or_metadata(self):
        original = self.kb.to_dict()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'kg.json'
            self.kb.save(path)
            self.assertEqual(KnowledgeBase.load(path).to_dict(), original)
            for field, value in [('explanation', 'Fabricated'), ('candidate_tags', [{'tag': 'auto'}]),
                                 ('depth', True), ('is_placeholder', True), ('path_sources', 'not a list')]:
                data = copy.deepcopy(original)
                data['nodes'][0][field] = value
                path.write_text(json.dumps(data))
                with self.subTest(field=field), self.assertRaises(ValueError):
                    KnowledgeBase.load(path)
