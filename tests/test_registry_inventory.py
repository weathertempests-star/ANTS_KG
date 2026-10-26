import json
from pathlib import Path
import unittest

from scripts.plan_registry_inventory import canonical, summarize

ROOT = Path(__file__).resolve().parents[1]


class RegistryInventoryTests(unittest.TestCase):
    def row(self, path, **extra):
        return {'path': path, 'source': 'https://example.org/documentation', **extra}

    def test_full_prefix_dedup_case_alias_and_trailing_separator(self):
        data = summarize([self.row(r'HKLM\System\Control'),
                          self.row('HKEY_LOCAL_MACHINE\\SYSTEM\\Control\\'),
                          self.row(r'HKLM\Other\Control')])
        self.assertEqual(data['summary']['accepted_unique_paths'], 2)
        self.assertEqual(data['summary']['nodes'], 5)
        self.assertEqual(data['summary']['edges'], 4)
        self.assertEqual(data['by_depth'][2]['total_nodes'], 2)

    def test_values_are_not_path_nodes(self):
        data = summarize([self.row(r'HKLM\SYSTEM', value_name='ValueOne'),
                          self.row(r'HKLM\SYSTEM', value_name='ValueTwo')])
        self.assertEqual(data['summary']['nodes'], 2)
        self.assertEqual(len(data['explicit_paths'][0]['evidence']), 2)

    def test_template_descendants_and_fixed_guid(self):
        data = summarize([self.row(r'HKLM\Services\<ServiceName>\Parameters'),
                          self.row(r'HKLM\Classes\{00000000-0000-0000-0000-000000000000}')])
        self.assertEqual(data['summary']['template_dependent_nodes'], 2)
        self.assertEqual(data['summary']['placeholder_nodes'], 1)
        self.assertEqual(data['summary']['quarantined_observations'], 0)

    def test_malformed_source_is_quarantined_not_repaired(self):
        data = summarize([self.row(r'HKLM\Bad{00000000-0000-0000-0000-000000000000}'), self.row('HKLM')])
        self.assertEqual(data['summary']['nodes'], 1)
        self.assertEqual(data['summary']['quarantined_unique_paths'], 1)

    def test_saved_inventory_reproduces_and_contains_existing_knowledge(self):
        rows = []
        for name in ('registry_core_observations.json', 'registry_policy_observations.json'):
            rows += json.loads((ROOT / 'knowledge' / name).read_text())['observations']
        actual = summarize(rows)
        saved = json.loads((ROOT / 'artifacts/registry-inventory/inventory.json').read_text())
        self.assertEqual(actual['summary'], saved['summary'])
        self.assertEqual(actual['by_depth'], saved['by_depth'])
        nodes = {canonical(n['path']) for n in actual['nodes']}
        definitions = json.loads((ROOT / 'knowledge/windows_registry.json').read_text())['definitions']
        self.assertTrue(all(canonical(d['path']) in nodes for d in definitions))
        self.assertEqual(sum(r['total_nodes'] for r in actual['by_depth']), len(nodes))
        self.assertTrue(all(n['sources'] for n in actual['nodes']))
        self.assertTrue(all(n['depth'] == len(canonical(n['path'])) for n in actual['nodes']))
        self.assertTrue(all(canonical(n['parent_path']) in nodes for n in actual['nodes'] if n['parent_path']))
