"""Preserved research evidence and the committed vault remain reproducible."""
import ast
import hashlib
import json
from pathlib import Path
import unittest

import standardizer_pkg
from standardizer_pkg import KnowledgeBase, validate_vault
from standardizer_pkg.zettelkasten import render_vault
from standardizer_pkg.model_data import audit_graph, validate_model_data
from scripts.assemble_registry_research import assemble
from scripts.audit_registry_research import audit
from scripts.prepare_registry_evaluation import render_evaluation, validate_evaluation

ROOT = Path(__file__).resolve().parents[1]


class ResearchArtifactsTests(unittest.TestCase):
    def test_saved_vault_matches_catalog_and_inventory(self):
        kb = KnowledgeBase.load_catalog(ROOT / 'knowledge/windows_registry.json',
                                        ROOT / 'artifacts/registry-inventory/inventory.json')
        vault = ROOT / 'artifacts/knowledge-vault'
        self.assertTrue(validate_vault(vault)['valid'])
        graph = kb.to_dict()
        self.assertEqual(graph['schema'], 'prefix-knowledge-3')
        self.assertEqual((len(graph['nodes']), len(graph['edges'])), (197, 192))
        self.assertEqual(sum(n['status'] == 'pending' for n in graph['nodes']), 0)
        self.assertEqual(sum(n['status'] == 'documented' for n in graph['nodes']), 145)
        self.assertEqual(sum(n['status'] == 'structural' for n in graph['nodes']), 52)
        self.assertEqual(len(graph['semantic_edges']), 46)
        self.assertTrue(audit_graph(kb)['valid'])
        self.assertTrue(all(n['candidate_tags'] == [] for n in graph['nodes']))
        seed = KnowledgeBase.load_catalog(ROOT / 'tests/fixtures/registry_seed_v1.json')
        explained = {n['id']: n for n in graph['nodes'] if n['status'] != 'pending'}
        self.assertTrue({n['id'] for n in seed.to_dict()['nodes']} <= set(explained))
        for node in seed.to_dict()['nodes']:
            self.assertEqual(explained[node['id']]['explanation'], node['explanation'])
        for name, expected in render_vault(kb).items():
            self.assertEqual((vault / name).read_bytes(), expected.encode('utf-8'), name)

    def test_research_assembly_and_model_artifacts_are_reproducible(self):
        catalog, reviews = assemble()
        self.assertEqual(catalog, json.loads((ROOT / 'knowledge/windows_registry.json').read_text()))
        self.assertEqual(reviews, json.loads((ROOT / 'knowledge/research/source_reviews.json').read_text()))
        kb = KnowledgeBase.load(ROOT / 'artifacts/knowledge-vault/kg.json')
        self.assertTrue(validate_model_data(kb, ROOT / 'artifacts/model-data')['valid'])
        rows = [json.loads(line) for line in (ROOT / 'artifacts/model-data/node-records.jsonl').read_text().splitlines()]
        self.assertEqual(len(rows), 197)
        examples = []
        for path in (ROOT / 'artifacts/model-data/sft').glob('*.jsonl'):
            examples.extend(json.loads(line) for line in path.read_text().splitlines())
        self.assertEqual(len(examples), 394)
        self.assertEqual(len({e['id'] for e in examples}), 394)
        by_id = {r['node_id']: r for r in rows}
        for e in examples:
            self.assertEqual(e['sources'], by_id[e['node_id']]['explanation_sources'])
        splits = {}
        for row in rows:
            splits.setdefault(row['split_family'], set()).add(row['split'])
        self.assertTrue(all(len(s) == 1 for s in splits.values()))
        positions = json.loads((ROOT / 'artifacts/model-data/graph/node-index.json').read_text())
        for edge in json.loads((ROOT / 'artifacts/model-data/graph/train-edge-index.json').read_text()):
            self.assertEqual(positions[edge['source']]['split'], 'train')
            self.assertEqual(positions[edge['target']]['split'], 'train')

    def test_review_coverage_and_evaluation_paths(self):
        kb = KnowledgeBase.load(ROOT / 'artifacts/knowledge-vault/kg.json')
        for batch in ('core', 'user_zones', 'machine_policy'):
            data = json.loads((ROOT / 'knowledge/research/batches' / (batch + '.json')).read_text())
            review = json.loads((ROOT / 'knowledge/research/reviews' / (batch + '_peer.json')).read_text())
            self.assertEqual(set(review['reviewed_paths']), {n['path'] for n in data['definitions']})
        cases = [json.loads(line) for line in (ROOT / 'evaluation/registry_cases.jsonl').read_text().splitlines()]
        self.assertEqual(len({c['id'] for c in cases}), 17)
        for case in cases:
            self.assertTrue(case['expected_propositions'])
            self.assertTrue(case['prohibited_inferences'])
            for path in case['knowledge_paths']:
                self.assertTrue(kb.resolve(path, 'registry')['path_complete'], path)

    def test_evaluation_package_separates_prompts_from_answers(self):
        evaluation = ROOT / 'evaluation'
        rendered = render_evaluation(evaluation / 'registry_cases.jsonl', evaluation / 'rubric.json')
        self.assertEqual(validate_evaluation(evaluation), {'valid': True, 'cases': 17, 'files': 3})
        prompt_rows = [json.loads(line) for line in rendered['prompts.jsonl'].splitlines()]
        answer_rows = [json.loads(line) for line in rendered['answer-key.jsonl'].splitlines()]
        self.assertEqual([row['id'] for row in prompt_rows], [row['id'] for row in answer_rows])
        for row in prompt_rows:
            self.assertFalse({'expected_propositions', 'prohibited_inferences',
                              'knowledge_paths', 'sources'} & set(row))
        for name, content in rendered.items():
            self.assertEqual((evaluation / name).read_text(), content, name)

    def test_research_audit_is_current_and_reproducible(self):
        path = ROOT / 'knowledge/research/research_audit.json'
        saved = json.loads(path.read_text())
        self.assertEqual(saved, audit(saved['as_of']))
        self.assertEqual(saved['result'], 'valid_for_declared_research_scope')

    def test_rule_archive_preserves_source_patterns_order_and_inactive_status(self):
        data = json.loads((ROOT / 'knowledge/registry_rule_reference.json').read_text())
        source = data['original_source_text']
        self.assertEqual(hashlib.sha256(source.encode('utf-8')).hexdigest(), data['origin']['sha256'])
        assignments = {s.targets[0].id: s for s in ast.parse(source).body
                       if isinstance(s, ast.Assign) and isinstance(s.targets[0], ast.Name)}
        self.assertEqual(sum(len(g['rules']) for g in data['groups']), 84)
        for group in data['groups']:
            originals = assignments[group['name']].value.elts
            self.assertEqual(len(originals), len(group['rules']))
            for index, (original, rule) in enumerate(zip(originals, group['rules'])):
                call, label = original.elts
                self.assertEqual(rule['order'], index)
                self.assertEqual(rule['regex'], ast.literal_eval(call.args[0]))
                self.assertEqual(rule['output_label'], ast.literal_eval(label))
                self.assertEqual(rule['flags_expression'], ast.get_source_segment(source, call.args[1]))
                self.assertEqual(rule['source_line'], original.lineno)
                self.assertEqual(rule['source_expression'], ast.get_source_segment(source, original))
                self.assertEqual(rule['executed_by_entry_point'], group['name'] in {'HIVE_RULES', 'CATEGORY_RULES'})
                self.assertFalse(rule['functional_tag_approved'])
                if group['name'] == 'CATEGORY_RULES':
                    self.assertTrue(rule['operation_or_risk_implication'])
        self.assertEqual(len(data['disabled_rules']), 1)
        disabled = data['disabled_rules'][0]
        self.assertFalse(disabled['enabled_in_table'])
        self.assertFalse(disabled['executed_by_entry_point'])
        self.assertTrue(disabled['operation_or_risk_implication'])
        self.assertTrue(source.splitlines()[disabled['source_line'] - 1].lstrip().startswith('#'))
        self.assertEqual(data['fallbacks']['no_category_match'], '<OTHER_ACTION>')

    def test_removed_prototype_files_and_public_interfaces_are_absent(self):
        cleanup = json.loads((ROOT / 'artifacts/prototype-cleanup.json').read_text())
        for row in cleanup['removed_files']:
            self.assertFalse((ROOT / row['path']).exists(), row['path'])
        self.assertEqual(standardizer_pkg.__all__, ['KnowledgeBase', 'export_vault', 'validate_vault'])
        for name in ('standardize', 'KnowledgeGraph', 'build_kg', 'standardize_trace', 'KGTools'):
            self.assertFalse(hasattr(standardizer_pkg, name))
