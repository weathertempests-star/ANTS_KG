import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from standardizer_pkg import KnowledgeBase

CATALOG = Path(__file__).resolve().parents[1] / 'tests/fixtures/registry_seed_v1.json'
TARGET = r'HKLM\System\CurrentControlSet\Control\Session Manager'


class SharedKnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.kb = KnowledgeBase.load_catalog(CATALOG)

    def test_requested_path_is_five_shared_nodes(self):
        result = self.kb.resolve(TARGET, 'registry')
        self.assertTrue(result['complete'])
        self.assertEqual([s['raw'] for s in result['steps']], ['HKLM', 'System', 'CurrentControlSet', 'Control', 'Session Manager'])
        self.assertEqual(len(result['edges']), 4)
        for step in result['steps']:
            self.assertGreater(len(step['knowledge']['explanation']), 100)
            start, end = step['source_span']
            self.assertEqual(TARGET[start:end], step['raw'])
        control_set = result['steps'][2]['knowledge']
        for word in ('startup', 'drivers', 'services'):
            self.assertIn(word, control_set['explanation'])

    def test_repeated_inputs_aliases_and_shared_branch_never_add_nodes(self):
        before = self.kb.to_dict()
        a = self.kb.resolve(TARGET, 'registry')
        b = self.kb.resolve(TARGET.replace('HKLM', 'HKEY_LOCAL_MACHINE').upper(), 'registry')
        c = self.kb.resolve(r'HKLM\SYSTEM\CurrentControlSet\Services', 'registry')
        self.assertEqual(a['path_node_ids'], b['path_node_ids'])
        self.assertEqual(a['path_node_ids'][:3], c['path_node_ids'][:3])
        self.assertNotEqual(a['path_node_ids'][3], c['path_node_ids'][3])
        for _ in range(20):
            self.kb.resolve(TARGET, 'registry')
        self.assertEqual(self.kb.to_dict(), before)
        self.assertEqual(len(before['nodes']), 7)
        self.assertNotIn('event_id', json.dumps(before))
        self.assertNotIn('malicious_example', json.dumps(before))
        self.assertNotIn('benign_example', json.dumps(before))

    def test_unknown_suffix_does_not_inherit_ancestor_meaning(self):
        result = self.kb.resolve(TARGET + r'\Unknown\Child', 'registry')
        self.assertFalse(result['complete'])
        self.assertEqual([s['match'] for s in result['steps']], ['known'] * 5 + ['unknown'] * 2)
        self.assertIsNone(result['steps'][-1]['knowledge'])
        unrelated = self.kb.resolve(r'HKLM\Other\CurrentControlSet', 'registry')
        self.assertIsNone(unrelated['steps'][-1]['node_id'])
        self.assertFalse(self.kb.resolve('', 'registry')['complete'])
        slash = self.kb.resolve(r'HKLM\SYSTEM/CurrentControlSet', 'registry')
        self.assertEqual(len(slash['steps']), 2)
        self.assertFalse(slash['complete'])

    def test_retrieval_is_detached(self):
        result = self.kb.resolve(TARGET, 'registry')
        result['steps'][0]['knowledge']['explanation'] = 'changed'
        self.assertNotEqual(self.kb.resolve(TARGET, 'registry')['steps'][0]['knowledge']['explanation'], 'changed')

    def test_authoring_requires_unique_nodes_and_explicit_parents(self):
        definitions = json.loads(CATALOG.read_text())['definitions']
        with self.assertRaises(ValueError):
            KnowledgeBase(definitions[1:])
        with self.assertRaises(ValueError):
            KnowledgeBase(definitions + [copy.deepcopy(definitions[0])])
        with self.assertRaises(ValueError):
            KnowledgeBase([{**definitions[0], 'malicious_example': 'not supported'}])

    def test_roundtrip_and_tampered_edge_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'kg.json'
            self.kb.save(path)
            self.assertEqual(KnowledgeBase.load(path).to_dict(), self.kb.to_dict())
            data = json.loads(path.read_text())
            data['edges'][0]['target'] = 'wrong'
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                KnowledgeBase.load(path)

    def test_other_domains_use_same_prefix_structure_with_explicit_definitions(self):
        def row(domain, path):
            return dict(domain=domain, path=path, role='test_fixture', explanation='Structural test fixture only.',
                        status='structural', sources=['https://example.org/test-fixture'])
        kb = KnowledgeBase([row('file', 'C:'), row('file', r'C:\Windows'),
                            row('command', 'reg'), row('command', 'reg query')])
        self.assertTrue(kb.resolve('c:/WINDOWS', 'file')['complete'])
        self.assertTrue(kb.resolve('reg query', 'command')['complete'])
        self.assertFalse(kb.resolve('reg query HKLM', 'command')['complete'])
        self.assertFalse(kb.resolve('reg add', 'command')['complete'])
        with self.assertRaises(ValueError):
            kb.resolve(r'\\server\share', 'file')

    def test_cli_build_and_read_only_resolve(self):
        with tempfile.TemporaryDirectory() as tmp:
            graph, md = Path(tmp) / 'kg.json', Path(tmp) / 'kg.md'
            def run(*args):
                return subprocess.run([sys.executable, '-m', 'standardizer_pkg', *map(str, args)],
                                      text=True, capture_output=True, check=True)
            run('knowledge-build', CATALOG, '-o', graph, '--markdown', md)
            before = graph.read_bytes()
            result = json.loads(run('knowledge-resolve', graph, 'registry', TARGET).stdout)
            self.assertTrue(result['complete'])
            self.assertEqual(before, graph.read_bytes())
            self.assertEqual(md.read_text(), KnowledgeBase.load(graph).markdown())
