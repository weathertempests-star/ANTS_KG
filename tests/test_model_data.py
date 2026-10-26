"""Evidence-aware knowledge, model context, migration and learning-data contracts."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

from standardizer_pkg import KnowledgeBase, export_vault, validate_vault
from standardizer_pkg.knowledge import adapt_registry_path
from standardizer_pkg.model_data import audit_graph, export_model_data, render_model_data, validate_model_data, split_family

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys'


def researched(path, explanation=None):
    return dict(domain='registry', path=path, role='test_namespace',
                explanation=explanation or ('This fixture describes the full prefix ' + path + ' as a configuration namespace. '
                    'Its containing scope and child definitions identify which stored settings are being discussed. '
                    'No operation, configured value, or effective behavior is supplied by this definition.'),
                sources=[SOURCE], status='documented', research={
                    'summary': 'The fixture ' + path + ' identifies its own configuration namespace.',
                    'scope': 'machine' if path.startswith('HKLM') else 'user',
                    'log_context': 'A log targeting ' + path + ' concerns this fixture namespace; inspect the event operation and outcome before describing a change.',
                    'cannot_infer': ['The path does not establish a successful operation.', 'The key name does not reveal stored value data.'],
                    'value_semantics': [{'name': 'Example', 'kind': 'value', 'meaning': 'A test-only named value.', 'source': SOURCE}],
                    'applicability': 'Test fixture only; no Windows compatibility claim.',
                    'evidence': [{'url': SOURCE, 'section': 'Fixture', 'claim': 'Test evidence only.', 'support': 'direct'}]})


def graph():
    return KnowledgeBase([researched('HKLM'), researched(r'HKLM\SOFTWARE'), researched('HKCU'), researched(r'HKCU\Software')],
                         relations=[{'source_path': r'HKLM\SOFTWARE', 'target_path': r'HKCU\Software',
                                     'relation': 'SCOPE_COUNTERPART', 'explanation': 'Distinct fixture scopes, not physical-key equivalence.', 'sources': [SOURCE]}])


class ModelDataTests(unittest.TestCase):
    def test_cli_context_and_model_data_guard_generated_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            snapshot = root / 'source.json'
            graph().save(snapshot)
            dataset = root / 'data'
            def run(*args):
                return subprocess.run([sys.executable, '-m', 'standardizer_pkg', *map(str, args)],
                                      text=True, capture_output=True, cwd=ROOT)
            self.assertEqual(run('knowledge-model-data', snapshot, '-o', dataset).returncode, 0)
            result = run('knowledge-context', snapshot, r'HKLM\SOFTWARE', '--value-name', 'Example')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['value_knowledge'][0]['name'], 'Example')
            output = dataset / 'node-records.jsonl'
            before = output.read_bytes()
            result = run('knowledge-context', snapshot, 'HKLM', '-o', output)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(output.read_bytes(), before)
            self.assertEqual(run('knowledge-validate-model-data', snapshot, dataset).returncode, 0)

    def test_unnamed_value_is_distinct_from_literal_default_name(self):
        row = researched('HKLM')
        row['research']['value_semantics'] = [
            {'name': '', 'kind': 'value', 'meaning': 'Unnamed value.', 'source': SOURCE},
            {'name': '(Default)', 'kind': 'value', 'meaning': 'Literal named value.', 'source': SOURCE},
        ]
        kb = KnowledgeBase([row])
        self.assertEqual(kb.model_context('HKLM')['value_knowledge'], [])
        self.assertEqual(kb.model_context('HKLM', '')['value_knowledge'][0]['meaning'], 'Unnamed value.')
        self.assertEqual(kb.model_context('HKLM', '(Default)')['value_knowledge'][0]['meaning'], 'Literal named value.')
        row['research']['value_semantics'][0]['kind'] = 'subkey'
        with self.assertRaises(ValueError):
            KnowledgeBase([row])

    def test_complete_semantic_evidence_is_exported(self):
        kb = graph()
        files = render_model_data(kb)
        edges = [json.loads(line) for line in files['graph/semantic-edges.jsonl'].splitlines()]
        self.assertEqual(edges, kb.to_dict()['semantic_edges'])
        self.assertEqual(json.loads(files['graph/snapshot.json']), kb.to_dict())

    def test_edited_manifest_cannot_delete_personal_file_or_hide_modified_record(self):
        kb = graph()
        for attack in ('personal', 'record'):
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as tmp:
                export_model_data(kb, tmp)
                root = Path(tmp)
                personal = root / 'personal.txt'
                personal.write_text('Keep this file')
                manifest_path = root / 'manifest.json'
                manifest = json.loads(manifest_path.read_text())
                if attack == 'personal':
                    manifest['files']['personal.txt'] = hashlib.sha256(personal.read_bytes()).hexdigest()
                else:
                    records = root / 'node-records.jsonl'
                    records.write_text(records.read_text().replace('Test fixture only', 'Manual alteration'))
                    manifest['files']['node-records.jsonl'] = hashlib.sha256(records.read_bytes()).hexdigest()
                manifest_path.write_text(json.dumps(manifest))
                before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}
                with self.assertRaises(ValueError):
                    export_model_data(kb, root)
                self.assertEqual(before, {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()})

    def test_context_separates_value_from_key_and_does_not_mutate(self):
        kb = graph()
        before = kb.to_dict()
        context = kb.model_context(r'HKLM\Software', 'example')
        self.assertTrue(context['path_complete'])
        self.assertEqual(len(context['prefix_knowledge']), 2)
        self.assertEqual(context['value_knowledge'][0]['name'], 'Example')
        self.assertEqual(len(context['semantic_edges']), 1)
        context['prefix_knowledge'][0]['research']['summary'] = 'Changed'
        context['value_knowledge'][0]['meaning'] = 'Changed'
        self.assertEqual(kb.to_dict(), before)
        unknown = kb.model_context(r'HKLM\Software\Example')
        self.assertFalse(unknown['path_complete'])
        self.assertEqual(unknown['unknown_components'], ['Example'])
        self.assertEqual(unknown['value_knowledge'], [])
        self.assertEqual(kb.model_context(r'HKLM\Software\Missing', 'Example')['value_knowledge'], [])
        with self.assertRaises(TypeError):
            kb.model_context('HKLM', 42)

    def test_nt_native_adapter_is_explicit_and_keeps_user_sid_scope(self):
        machine = adapt_registry_path(r'\Registry\Machine\SOFTWARE', 'nt_native')
        self.assertEqual(machine['canonical_path'], r'HKLM\SOFTWARE')
        self.assertTrue(machine['adapted'])
        user = adapt_registry_path(r'\REGISTRY\USER\S-1-5-21-1-2-3-1001\Software', 'nt_native')
        self.assertEqual(user['canonical_path'], r'HKU\S-1-5-21-1-2-3-1001\Software')
        self.assertNotIn('HKCU', user['canonical_path'])
        with self.assertRaises(ValueError):
            adapt_registry_path(r'\Device\HarddiskVolume1', 'nt_native')
        with self.assertRaises(ValueError):
            adapt_registry_path(r'\Registry\A\Machine', 'nt_native')

    def test_constrained_template_candidates_do_not_claim_exact_paths(self):
        kb = KnowledgeBase.load(ROOT / 'artifacts/knowledge-vault/kg.json')
        raw = r'HKLM\SYSTEM\CurrentControlSet\Services\ExampleSvc\Parameters'
        exact = kb.resolve(raw, 'registry')
        self.assertFalse(exact['path_complete'])
        self.assertFalse(exact['pattern_complete'])
        candidate = kb.resolve(raw, 'registry', template_candidates=True)
        self.assertFalse(candidate['path_complete'])
        self.assertTrue(candidate['pattern_complete'])
        self.assertTrue(candidate['pattern_explanations_complete'])
        self.assertEqual(candidate['template_bindings'], {'<servicename>': 'ExampleSvc'})
        self.assertEqual([s['match'] for s in candidate['steps']][-2:], ['template_candidate'] * 2)
        self.assertTrue(any('does not assert' in warning for warning in candidate['warnings']))
        context = kb.model_context(raw, 'ImagePath', template_candidates=True)
        self.assertFalse(context['path_complete'])
        self.assertTrue(context['pattern_complete'])
        self.assertEqual(context['prefix_knowledge'][-1]['lookup_match'], 'template_candidate')
        # Typed GUID and SID placeholders reject lookalikes but accept documented shapes.
        good_guid = kb.resolve(r'HKLM\SOFTWARE\Classes\CLSID\{00000000-0000-0000-0000-000000000001}',
                               'registry', template_candidates=True)
        bad_guid = kb.resolve(r'HKLM\SOFTWARE\Classes\CLSID\not-a-guid',
                              'registry', template_candidates=True)
        self.assertTrue(good_guid['pattern_complete'])
        self.assertFalse(bad_guid['pattern_complete'])
        native_user = kb.model_context(
            r'\Registry\User\S-1-5-21-1-2-3-1001\Environment', path_format='nt_native',
            template_candidates=True)
        self.assertTrue(native_user['pattern_complete'])
        self.assertFalse(native_user['path_complete'])
        self.assertEqual(native_user['template_bindings']['<userhive>'], 'S-1-5-21-1-2-3-1001')

    def test_research_requires_explicit_evidence_and_limits(self):
        for edit in (lambda d: d['research'].update(cannot_infer=[]),
                     lambda d: d['research']['evidence'][0].update(url='https://example.org/unlisted'),
                     lambda d: d['research']['evidence'][0].update(support='guess'),
                     lambda d: d['research']['value_semantics'][0].update(kind='key_or_value'),
                     lambda d: d['research'].update(scope='definitely_malicious')):
            row = researched('HKLM')
            edit(row)
            with self.subTest(edit=edit), self.assertRaises(ValueError):
                KnowledgeBase([row])
        row = researched('HKLM')
        row['status'] = 'structural'
        self.assertFalse(audit_graph(KnowledgeBase([row]))['valid'])
        row['research']['evidence'][0]['support'] = 'structural_inference'
        self.assertTrue(audit_graph(KnowledgeBase([row]))['valid'])

    def test_semantic_links_require_valid_endpoints_sources_and_distinctness(self):
        row = {'source_path': 'HKLM', 'target_path': 'HKCU', 'relation': 'DISTINCT_SCOPE', 'explanation': 'Fixture scopes.', 'sources': [SOURCE]}
        for edit in (lambda r: r.update(target_path='HKU'), lambda r: r.update(target_path='HKLM'),
                     lambda r: r.update(sources=[]), lambda r: r.update(relation='vague-link')):
            relation = copy.deepcopy(row)
            edit(relation)
            with self.subTest(edit=edit), self.assertRaises(ValueError):
                KnowledgeBase([researched('HKLM'), researched('HKCU')], relations=[relation])
        with self.assertRaises(ValueError):
            KnowledgeBase([researched('HKLM'), researched('HKCU')], relations=[row, row])

    def test_old_vault_can_refresh_without_losing_personal_notes(self):
        old = KnowledgeBase.load(ROOT / 'tests/fixtures/registry_seed_snapshot_v2.json')
        self.assertEqual(old.to_dict()['schema'], 'prefix-knowledge-2')
        with tempfile.TemporaryDirectory() as tmp:
            export_vault(old, tmp)
            personal = Path(tmp) / 'personal' / 'research.md'
            personal.parent.mkdir()
            personal.write_text('Personal annotation')
            export_vault(graph(), tmp)
            self.assertTrue(validate_vault(tmp)['valid'])
            self.assertEqual(personal.read_text(), 'Personal annotation')
            self.assertTrue((Path(tmp) / 'CONCEPTS.md').is_file())
            self.assertEqual(json.loads((Path(tmp) / 'manifest.json').read_text())['format_version'], 3)
        with tempfile.TemporaryDirectory() as tmp:
            export_vault(old, tmp)
            (Path(tmp) / 'CONCEPTS.md').write_text('User-owned file predating the new format')
            with self.assertRaises(ValueError):
                export_vault(graph(), tmp)
            self.assertEqual((Path(tmp) / 'CONCEPTS.md').read_text(), 'User-owned file predating the new format')

    def test_snapshot_roundtrip_and_semantic_edge_tamper_rejection(self):
        kb = graph()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'kg.json'
            kb.save(path)
            self.assertEqual(KnowledgeBase.load(path).to_dict(), kb.to_dict())
            data = kb.to_dict()
            data['semantic_edges'][0]['target'] = 'unknown'
            path.write_text(json.dumps(data))
            with self.assertRaises((ValueError, KeyError)):
                KnowledgeBase.load(path)

    def test_learning_exports_are_deterministic_grouped_and_guarded(self):
        kb = graph()
        before = kb.to_dict()
        with tempfile.TemporaryDirectory() as tmp:
            export_model_data(kb, tmp)
            self.assertTrue(validate_model_data(kb, tmp)['valid'])
            rows = [json.loads(line) for line in (Path(tmp) / 'node-records.jsonl').read_text().splitlines()]
            same_family = [r for r in rows if r['path'].casefold().endswith('software')]
            self.assertEqual(len({r['split_family'] for r in same_family}), 1)
            self.assertEqual(len({r['split'] for r in same_family}), 1)
            for path in (Path(tmp) / 'sft').iterdir():
                examples = [json.loads(line) for line in path.read_text().splitlines()]
                for example in examples:
                    record = next(r for r in rows if r['node_id'] == example['node_id'])
                    self.assertEqual(path.stem, record['split'])
                    self.assertEqual([m['role'] for m in example['messages']], ['system', 'user', 'assistant'])
            personal = Path(tmp) / 'personal.txt'
            personal.write_text('Keep')
            export_model_data(kb, tmp)
            self.assertEqual(personal.read_text(), 'Keep')
            target = Path(tmp) / 'node-records.jsonl'
            target.write_text(target.read_text() + '\n')
            with self.assertRaises(ValueError):
                validate_model_data(kb, tmp)
            with self.assertRaises(ValueError):
                export_model_data(kb, tmp)
        self.assertEqual(kb.to_dict(), before)

    def test_unresearched_catalog_cannot_be_exported_as_training_data(self):
        kb = KnowledgeBase.load_catalog(ROOT / 'tests/fixtures/registry_seed_v1.json')
        with self.assertRaises(ValueError):
            render_model_data(kb)
        with self.assertRaises(ValueError):
            render_model_data(KnowledgeBase([]))

    def test_zone_and_template_variants_share_family(self):
        kb = KnowledgeBase([researched('HKLM'), researched('HKCU')])
        for hive in ('HKLM', 'HKCU'):
            for zone in ('Zones', 'Lockdown_Zones'):
                n = {'canonical_components': [hive, 'software', 'policies', 'microsoft', 'windows', 'currentversion', 'internet settings', zone.casefold(), '3']}
                self.assertEqual(split_family(n), 'internet_zones')
