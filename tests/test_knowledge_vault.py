"""Shared-vault consistency and preservation of user-owned notes."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from standardizer_pkg import KnowledgeBase, export_vault, validate_vault
from standardizer_pkg.zettelkasten import note_path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'tests/fixtures/registry_seed_v1.json'
INVENTORY = ROOT / 'artifacts/registry-inventory/inventory.json'


class KnowledgeVaultTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kb = KnowledgeBase.load_catalog(CATALOG, INVENTORY)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.vault = Path(self.temp.name) / 'vault'
        export_vault(self.kb, self.vault)

    def bytes(self):
        return {str(p.relative_to(self.vault)): p.read_bytes() for p in self.vault.rglob('*') if p.is_file()}

    def test_197_notes_190_queue_entries_and_all_generated_links_resolve(self):
        result = validate_vault(self.vault)
        self.assertEqual((result['nodes'], result['edges'], result['managed_files']), (197, 192, 201))
        self.assertEqual(len(list((self.vault / 'notes').iterdir())), 197)
        queue = (self.vault / 'REVIEW_QUEUE.md').read_text()
        pending = {note_path(n['id']) for n in self.kb.to_dict()['nodes'] if n['status'] == 'pending'}
        links = re.findall(r'\]\((notes/[^)]+)\)', queue)
        self.assertEqual(len(links), 190)
        self.assertEqual(set(links), pending)
        for phrase in ('40 pending / 45', '117 pending / 119', '33 pending / 33'):
            self.assertIn(phrase, queue)
        for path in self.vault.rglob('*.md'):
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                if not target.startswith('<https://'):
                    self.assertTrue((path.parent / target).is_file(), (path, target))
        manifest = json.loads((self.vault / 'manifest.json').read_text())
        for name, digest in manifest['files'].items():
            self.assertEqual(hashlib.sha256((self.vault / name).read_bytes()).hexdigest(), digest)
        self.assertEqual(manifest['graph_sha256'], hashlib.sha256((self.vault / 'kg.json').read_bytes()).hexdigest())

    def test_refresh_is_deterministic_and_preserves_personal_notes(self):
        personal = self.vault / 'personal' / 'research.md'
        personal.parent.mkdir()
        personal.write_text('My own unfinished research.\n')
        before = self.bytes()
        export_vault(self.kb, self.vault)
        self.assertEqual(self.bytes(), before)
        smaller = KnowledgeBase.load_catalog(CATALOG)
        export_vault(smaller, self.vault)
        self.assertEqual(len(list((self.vault / 'notes').iterdir())), 7)
        self.assertEqual(personal.read_text(), 'My own unfinished research.\n')
        export_vault(self.kb, self.vault)
        self.assertEqual(self.bytes(), before)

    def test_manual_edit_even_with_updated_manifest_is_rejected_without_writes(self):
        note = next((self.vault / 'notes').iterdir())
        note.write_text(note.read_text() + '\nManual research.\n')
        manifest_path = self.vault / 'manifest.json'
        manifest = json.loads(manifest_path.read_text())
        manifest['files'][str(note.relative_to(self.vault))] = hashlib.sha256(note.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest))
        before = self.bytes()
        with self.assertRaises(ValueError):
            validate_vault(self.vault)
        with self.assertRaises(ValueError):
            export_vault(self.kb, self.vault)
        self.assertEqual(self.bytes(), before)

    def test_missing_stale_and_broken_generated_links_are_detected(self):
        note = next((self.vault / 'notes').iterdir())
        original = note.read_bytes()
        note.unlink()
        with self.assertRaises(ValueError):
            validate_vault(self.vault)
        note.write_bytes(original)
        stale = self.vault / 'notes' / 'stale.md'
        stale.write_text('Old generated note')
        with self.assertRaises(ValueError):
            validate_vault(self.vault)
        with self.assertRaises(ValueError):
            export_vault(self.kb, self.vault)
        stale.unlink()
        index = self.vault / 'INDEX.md'
        index.write_text(index.read_text() + '\n[Broken](notes/missing.md)\n')
        with self.assertRaisesRegex(ValueError, 'broken generated link'):
            validate_vault(self.vault)

    def test_json_markdown_and_manifest_drift_are_all_detected(self):
        for filename in ('kg.json', 'manifest.json', 'INDEX.md', 'REVIEW_QUEUE.md'):
            path = self.vault / filename
            original = path.read_bytes()
            path.write_bytes(original + b'\n')
            with self.subTest(filename=filename), self.assertRaises(ValueError):
                validate_vault(self.vault)
            path.write_bytes(original)
        path = self.vault / 'kg.json'
        data = json.loads(path.read_text())
        node = next(n for n in data['nodes'] if n['status'] == 'documented')
        node['explanation'] = 'A changed authored explanation with stale Markdown.'
        path.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            validate_vault(self.vault)

    def test_symlinks_and_unmanaged_reserved_paths_are_not_overwritten(self):
        elsewhere = Path(self.temp.name) / 'elsewhere.md'
        elsewhere.write_text('Keep this file')
        note = next((self.vault / 'notes').iterdir())
        note.unlink()
        note.symlink_to(elsewhere)
        with self.assertRaises(ValueError):
            export_vault(self.kb, self.vault)
        self.assertEqual(elsewhere.read_text(), 'Keep this file')
        other = Path(self.temp.name) / 'other'
        other.mkdir()
        (other / 'REVIEW_QUEUE.md').write_text('Existing user file')
        with self.assertRaises(ValueError):
            export_vault(self.kb, other)
        self.assertEqual((other / 'REVIEW_QUEUE.md').read_text(), 'Existing user file')

    def test_path_punctuation_cannot_create_generated_links_or_filenames(self):
        definitions = json.loads(CATALOG.read_text())['definitions'][:1]
        definitions.append({**definitions[0], 'path': r'HKLM\A](missing.md)<script>~~~`x`'})
        graph = KnowledgeBase(definitions)
        export_vault(graph, self.vault)
        self.assertEqual(validate_vault(self.vault)['nodes'], 2)
        self.assertEqual({p.name for p in (self.vault / 'notes').iterdir()},
                         {Path(note_path(n['id'])).name for n in graph.to_dict()['nodes']})

    def test_cli_build_export_validate_resolve_and_failure_exit_codes(self):
        def run(*args, code=0):
            result = subprocess.run([sys.executable, '-m', 'standardizer_pkg', *map(str, args)],
                                    text=True, capture_output=True, cwd=ROOT)
            self.assertEqual(result.returncode, code, result.stderr)
            return result
        graph = Path(self.temp.name) / 'build.json'
        run('knowledge-build', CATALOG, '--inventory', INVENTORY, '-o', graph)
        run('knowledge-vault', graph, '-o', self.vault)
        self.assertTrue(json.loads(run('knowledge-validate-vault', self.vault).stdout)['valid'])
        before = self.bytes()
        result = json.loads(run('knowledge-resolve', self.vault / 'kg.json', 'registry',
                                r'HKLM\System\CurrentControlSet\Control\Session Manager').stdout)
        self.assertTrue(result['path_complete'])
        self.assertTrue(result['explanations_complete'])
        self.assertEqual(len(result['steps']), 5)
        self.assertEqual(self.bytes(), before)
        run('knowledge-build', CATALOG, '--inventory', INVENTORY, '-o', INVENTORY, code=2)
        run('knowledge-build', CATALOG, '-o', self.vault / 'kg.json', code=2)
        run('knowledge-build', CATALOG, '-o', graph, '--markdown', self.vault / 'INDEX.md', code=2)
        run('knowledge-resolve', graph, 'registry', 'HKLM', '-o', graph, code=2)
        run('knowledge-resolve', graph, 'registry', 'HKLM', '-o', self.vault / 'REVIEW_QUEUE.md', code=2)
        self.assertEqual(self.bytes(), before)
        for old_action in ('build', 'query', 'serve', 'vault', 'tool-schemas'):
            run(old_action, code=2)
        self.assertIn('knowledge-vault', run('--help').stdout)
        (self.vault / 'INDEX.md').write_text('Changed')
        run('knowledge-validate-vault', self.vault, code=2)
        run('knowledge-vault', graph, '-o', self.vault, code=2)
