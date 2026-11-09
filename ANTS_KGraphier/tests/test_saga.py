"""SAGA provenance gates and dependency-component splitting."""
import json
from pathlib import Path
import tempfile
import unittest

from ants_kgraphier.saga import dependency_split, inspect_archive, build_sources
from ants_kgraphier.classification.metrics import dependency_bootstrap


class SagaTests(unittest.TestCase):
    def test_mixed_and_shared_background_dependencies(self):
        recordings = [dict(id=x) for x in 'abcdef']
        evidence = {'a': {'mixed': True, 'components': ['b', 'c']},
                    'd': {'backgrounds': ['shared']}, 'e': {'backgrounds': ['shared']}}
        result = dependency_split(recordings, evidence)
        self.assertTrue(result['viable'])
        self.assertEqual(sorted(map(len, result['groups'].values())), [1, 2, 3])
        self.assertEqual(set(result['splits'].values()), {'train', 'validation', 'test'})
        self.assertEqual(result, dependency_split(list(reversed(recordings)), evidence))
        stopped = dependency_split(recordings, evidence, [('a', 'd')])
        self.assertFalse(stopped['viable'])
        with self.assertRaisesRegex(ValueError, 'unresolved'):
            dependency_split(recordings, {'a': {'mixed': True}})

    def test_checksum_mismatch_preserves_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root/'archive.zip'
            archive.write_bytes(b'not official data')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                inspect_archive(archive, root/'audit')
            manifest = json.loads((root/'audit'/'source-manifest.json').read_text())
            self.assertFalse(manifest['checksum_verified'])
            self.assertFalse((root/'audit'/'raw').exists())

    def test_adapter_and_group_bootstrap_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sources = []
            for i in range(3):
                name = f'{i}.jsonl'
                event = dict(srcNode={'Type': 'Process', 'UUID': f'p{i}'},
                             dstNode={'Type': 'Registry', 'UUID': f'r{i}', 'Key': 'HKLM\\X'},
                             timestamp=i, relation='RegSetValue', label='T1547.001')
                (root/name).write_text(json.dumps(event)+'\n')
                sources.append(dict(id=str(i), path=name, format='jsonl'))
            manifest = build_sources(root, {'recordings': sources}, root/'output')
            self.assertEqual(len(manifest['recordings']), 3)
            self.assertIn('feasibility', manifest['dependency_scope'])
        result = dependency_bootstrap([({'dependency_group': 'same'}, {})], [], [], (.5, .5))
        self.assertEqual(result['groups'], 1)
        self.assertIn('unavailable_reason', result)


if __name__ == '__main__':
    unittest.main()
