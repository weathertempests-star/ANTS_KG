"""Planning inventory must preserve labels and tolerate missing event endpoints."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import profile_experiment_data as profiler


class RecordingProfileTests(unittest.TestCase):
    def test_jsonl_null_endpoint_duplicates_and_registry_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / 'events.json'
            row = {'srcNode': {'Type':'Process','UUID':'p'},
                   'dstNode': {'Type':'Registry','Key':r'HKLM\SOFTWARE','Value':'1'},
                   'relation':'RegSetValue','label':'T1112_test','timestamp':2}
            rows = [row, row, {'srcNode':None,'dstNode':None,'relation':'Other','label':'benign','timestamp':1}]
            path.write_text('\n'.join(json.dumps(r) for r in rows)+'\n\n')
            with patch.object(profiler, 'ROOT', root):
                result, signatures = profiler.profile(path, {('hkey_local_machine',),('hkey_local_machine','software')})
            self.assertEqual(result['records'], 3)
            self.assertEqual(result['registry_labels'], {'T1112_test':2})
            self.assertEqual(result['registry_records_with_Value'], 2)
            self.assertEqual(result['exact_duplicate_records'], 1)
            self.assertEqual(result['timestamp_adjacent_decreases'], 1)
            self.assertEqual(result['destination_object_types'], {'NoneType':1,'dict':2})
            self.assertEqual(result['unique_registry_raw_targets_exact_nodes'], 1)
            self.assertEqual(len(signatures), 2)

    def test_array_keeps_manual_labels_and_overlap_ignores_label_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / 'CHT_selected'
            folder.mkdir()
            row = {'srcNode':{'Type':'Process','UUID':'p'},'dstNode':{'Type':'Registry','Key':'HKLM'},
                   'relation':'RegQueryKey','timestamp':0,'label':'benign'}
            first, second = folder/'first.json', folder/'second.json'
            first.write_text(json.dumps([row]))
            second.write_text(json.dumps([{**row,'label':'T1112','timestamp_raw':''}]))
            with patch.object(profiler, 'ROOT', root):
                a, sig_a = profiler.profile(first, {('hkey_local_machine',)})
                b, sig_b = profiler.profile(second, {('hkey_local_machine',)})
            self.assertEqual(sig_a, sig_b)
            self.assertNotEqual(a['sha256'], b['sha256'])
            self.assertEqual(a['labels'], {'benign':1})
            self.assertEqual(b['labels'], {'T1112':1})
            self.assertEqual(b['timestamp_raw_labels'], {'T1112':1})
            self.assertEqual(a['format'], 'json_array')

    def test_raw_value_target_is_not_reported_as_exact_key_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            path=root/'events.json'
            row={'srcNode':{},'dstNode':{'Type':'Registry','Key':r'HKLM\SOFTWARE\SomeValue'},
                 'relation':'RegQueryValue','timestamp':0,'label':'benign'}
            path.write_text(json.dumps(row)+'\n')
            with patch.object(profiler,'ROOT',root):
                result,_=profiler.profile(path,{('hkey_local_machine',),('hkey_local_machine','software')})
            self.assertEqual(result['unique_registry_raw_targets_exact_nodes'],0)
            self.assertEqual(result['raw_target_known_depth'],{'2':1})

if __name__ == '__main__':
    unittest.main()
