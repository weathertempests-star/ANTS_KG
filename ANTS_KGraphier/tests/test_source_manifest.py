import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('make_sources',Path(__file__).resolve().parents[1]/'scripts/make_sources.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SourceManifestTests(unittest.TestCase):
    def test_valid_unlabeled_and_invalid_schema(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            event=dict(srcNode=dict(Type='Process',UUID='host:p'),dstNode=dict(Type='Registry',UUID='host:k',Key='HKLM\\SYSTEM'),relation='RegOpenKey',timestamp=0)
            path=root/'events.jsonl'
            path.write_text(json.dumps(event)+'\n')
            source=dict(recordings=[dict(id='fixture',path='events.jsonl',format='jsonl',dependency_group='script1')])
            result=module.make_sources(root,source,root/'sources.json')
            self.assertEqual(result['audit'][0]['unlabeled'],1)
            self.assertEqual(result['recordings'][0]['expected_records'],1)
            event['dstNode'].pop('Key')
            path.write_text(json.dumps(event)+'\n')
            with self.assertRaises(ValueError):
                module.make_sources(root,source,root/'invalid.json')
            self.assertFalse((root/'invalid.json').exists())

    def test_escape_and_duplicates(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                module.make_sources(td,dict(recordings=[dict(id='x',path='../outside')]),Path(td)/'out.json')
