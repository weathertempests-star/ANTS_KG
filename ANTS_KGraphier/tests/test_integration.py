"""End-to-end trained backbone, persisted index and tamper rejection."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from ants_kgraphier.io import canonical, digest, write_json
from ants_kgraphier.knowledge import Knowledge
from ants_kgraphier.retrieval import train, build_index, evaluate
from ants_kgraphier.analyst import functional_query, search, render

ROOT = Path(__file__).resolve().parents[1]


class IntegrationTests(unittest.TestCase):
    def test_trained_search_and_modified_index(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            kg = Knowledge(ROOT.parent / "artifacts/knowledge-vault/kg.json")
            vendor = ROOT / "vendor/ProvG-Searcher"
            graphs = []
            for i in range(8):
                op = "RegSetValue" if i % 2 else "RegQueryValue"
                key = "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Example\\ImagePath"
                rec = "train" if i < 4 else "test"
                event = {"rec": rec, "row": i, "ord": i, "src": "p" + str(i), "dst": "r" + str(i),
                         "src_type": "Process", "dst_type": "Registry", "op": op, "raw_key": key,
                         "raw_sha": "fixture", "event_id": f"{rec}:{i}",
                         "selection": {"reason": "anchor"}, "knowledge": kg.annotate(key, op)}
                graphs.append({"id": str(i), "anchor_row": i, "anchor_event_id": f"{rec}:{i}",
                               "recording_sha256": rec, "kg_sha256": kg.sha256,
                               "split": rec, "dependency_group": rec, "events": [event]})
            path = root / "graphs.jsonl"
            path.write_text("".join(canonical(g) + "\n" for g in graphs))
            model_dir = root / "model"
            result = train(path, kg, vendor, model_dir, epochs=1, pairs=8)
            self.assertEqual(result["training_groups"], ["train"])
            self.assertEqual(result["pairs"], 16)
            build_index(path, model_dir, vendor, root / "index")
            score = evaluate(path, model_dir, root / "index", vendor, root / "eval.json", query_count=2, gallery_size=4)
            self.assertEqual(score["query_count"], 2)
            q = functional_query(kg, "HKLM\\SYSTEM", "RegSetValue")
            found = search(path, model_dir, root / "index", vendor, q, root / "search.json", topk=4, shortlist=8)
            self.assertEqual(len(found["results"]), 4)
            self.assertTrue(all(item["anchor"]["op"] == "RegSetValue" for item in found["results"]))
            render(root / "search.json", root / "search.html")
            self.assertIn("not malicious verdicts", (root / "search.html").read_text())
            (root / "index/ids.json").write_text("[]")
            with self.assertRaises(ValueError):
                search(path, model_dir, root / "index", vendor, q, root / "bad.json", topk=4, shortlist=8)


if __name__ == "__main__":
    unittest.main()
