import copy
import json
from pathlib import Path
import tempfile
import unittest

from ants_kgmaer.common.files import file_hash, read_json, write_json
from ants_kgmaer.data.context import build_context
from ants_kgmaer.data.contracts import RelationContract
from ants_kgmaer.data.ingest import ingest
from ants_kgmaer.data.sampling import select_targets, validate_splits
from ants_kgmaer.data.sources import stream_array
from ants_kgmaer.data.store import EventStore, readonly
from ants_kgmaer.knowledge.engine import KnowledgeBase

ROOT = Path(__file__).resolve().parents[1]


def event(order, label="benign", relation="RegOpenKey", key=r"HKLM\SOFTWARE\Microsoft"):
    return {"srcNode": {"Type": "Process", "UUID": "process-uuid", "Name": "a.exe",
                        "Image": r"C:\Users\TestU\Evil\MaliciousFiles" + "\\" + "a" * 32 + ".exe", "Cmdline": "a.exe"},
            "dstNode": {"Type": "Registry", "Key": key}, "timestamp": order, "relation": relation,
            "label": label, **({"timestamp_raw": ""} if label != "benign" else {})}


class DataPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.relations = ROOT / "configs/relations.json"

    def fixture(self):
        first = [event(10), event(10), event(11, "T1112"), event(12, "unknown")]
        second = [event(10), event(13, "T1112", "RegQueryValue", r"HKCU\Software\Entry")]
        write_json(self.root / "a.json", first)
        (self.root / "b.json").write_text("\n".join(json.dumps(row) for row in second))
        sources = {"schema": "ants-sources-1", "recordings": [
            {"id": name, "cohort": "CHT" if name == "a" else "APT", "path": name + ".json",
             "format": "json_array" if name == "a" else "jsonl", "sha256": file_hash(self.root / (name + ".json")),
             "expected_records": count, "dependency_group": name} for name, count in [("a", 4), ("b", 2)]]}
        write_json(self.root / "sources.json", sources)
        write_json(self.root / "labels.json", {"schema": "ants-labels-1", "mapping": {"benign": 0, "T1112": 1}})
        ingest(self.root / "sources.json", self.root, self.root / "labels.json", self.relations, self.root / "dataset")
        return self.root / "dataset", sources

    def test_streamed_array_tiny_chunks_and_malformed_tail(self):
        path = self.root / "array.json"
        values = [{"unicode": "註冊表", "escaped": '\\"'}, {"nested": {"a": [1, 2]}}]
        path.write_text(json.dumps(values, ensure_ascii=False))
        self.assertEqual(list(stream_array(path, 1)), values)
        for bad in ('[{"a":1},]', '[{"a":1}', '[] trailing', '[42]'):
            path.write_text(bad)
            with self.assertRaises(ValueError):
                list(stream_array(path, 3))

    def test_separate_labels_strict_history_and_no_prompt_leak(self):
        dataset, _ = self.fixture()
        store = EventStore(dataset / "events.sqlite")
        self.addCleanup(store.close)
        ids = list(store.registry_ids("a"))
        packet, _ = build_context(store, ids[1], 16)
        self.assertEqual(packet["history"], [])
        packet, _ = build_context(store, ids[2], 16)
        self.assertEqual(len(packet["history"]), 2)
        self.assertEqual(packet["history"][0]["order_group"], packet["history"][1]["order_group"])
        text = json.dumps(packet)
        for forbidden in ["timestamp_raw", "T1112", "label", "process-uuid", "TestU", "MaliciousFiles", "a" * 32]:
            self.assertNotIn(forbidden, text)
        self.assertNotIn("labels", {row[0] for row in store.connection.execute("SELECT name FROM sqlite_master")})
        self.assertTrue(read_json(dataset / "source_manifest.json")["complete"])

    def test_sampling_probabilities_quarantine_and_dependency_split(self):
        dataset, sources = self.fixture()
        report = select_targets(dataset, self.root / "selection", negatives=1)
        self.assertEqual(sum(r["selected_positive"] for r in report["recordings"]), 2)
        self.assertEqual(report["recordings"][0]["negative_inclusion_probability"], 0.5)
        overlaps = read_json(self.root / "selection/overlap_audit.json")
        self.assertEqual(overlaps["dependency_groups"], [["a", "b"]])
        with self.assertRaises(ValueError):
            validate_splits(sources["recordings"], overlaps["dependency_groups"], {"a": "test", "b": "development"})

    def test_value_contract_requires_evidence_and_preserves_uncertainty(self):
        contract = RelationContract(self.relations)
        result = contract.adapt("RegQueryValue", {"Key": r"HKCU\Software\Entry"}, "a")
        self.assertIsNone(result["key_path"])
        self.assertIsNone(result["value_name"])
        document = copy.deepcopy(contract.document)
        rule = {"operation": "query_value", "encoding": "separate_field", "value_name_field": "ValueName"}
        document["recording_overrides"] = {"a": {"RegQueryValue": rule}}
        write_json(self.root / "contract.json", document)
        with self.assertRaises(ValueError):
            RelationContract(self.root / "contract.json")
        rule["evidence"] = "Synthetic exporter fixture with independent ValueName field"
        write_json(self.root / "contract.json", document, replace=True)
        result = RelationContract(self.root / "contract.json").adapt(
            "RegQueryValue", {"Key": r"HKCU\Software", "ValueName": r"name\with\slashes"}, "a")
        self.assertEqual(result["value_name"], r"name\with\slashes")

    def test_knowledge_preserves_snapshot_and_five_session_manager_steps(self):
        path = ROOT / "ants_kgmaer/resources/kg.json"
        graph = KnowledgeBase.load(path)
        before = graph.to_dict()
        for _ in range(2):
            result = graph.model_context(r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager")
            self.assertEqual(len(result["prefix_knowledge"]), 5)
        self.assertEqual(graph.to_dict(), before)
        self.assertEqual(len(before["nodes"]), 197)
        self.assertEqual(len(before["edges"]), 192)


if __name__ == "__main__":
    unittest.main()
