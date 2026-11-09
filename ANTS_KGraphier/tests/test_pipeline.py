import copy
import json
from pathlib import Path
import tempfile
import unittest

from ants_kgraphier.extract import extract, symbolic, validate_graph
from ants_kgraphier.io import digest, write_json
from ants_kgraphier.knowledge import Knowledge
from ants_kgraphier.store import connect, ingest

ROOT = Path(__file__).resolve().parents[1]


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.kg = Knowledge(ROOT.parent / "artifacts/knowledge-vault/kg.json")
        def row(order, actor="p1", target="HKLM\\SYSTEM\\CurrentControlSet\\Services\\Example\\ImagePath", label="benign"):
            return {"srcNode": {"UUID": actor, "Type": "Process", "Name": "MaliciousFiles\\secret.exe"},
                    "dstNode": {"UUID": "shared", "Type": "Registry", "Key": target},
                    "relation": "RegSetValue", "timestamp": order, "label": label}
        self.rows = [row(0), row(1), row(1, "p2"), row(2), row(3, target="HKLM\\SOFTWARE\\different"), row(4)]
        self.rows[1]["timestamp_raw"] = "SECRET_LABEL_ARTIFACT"
        self.path = self.root / "source.json"
        write_json(self.path, self.rows)
        self.rec = digest(self.path)
        self.sources = {"recordings": [{"id": "fixture", "path": "source.json", "format": "json_array",
                                       "sha256": self.rec, "expected_records": len(self.rows), "dependency_group": "g"}]}
        self.store = self.root / "events.sqlite"
        ingest(self.root, self.sources, self.store)
        self.db = connect(self.store)
        self.addCleanup(self.db.close)

    def test_ties_and_temporal_paths(self):
        graph = extract(self.db, self.rec, 1, self.kg, budget=20)
        self.assertNotIn(2, [e["row"] for e in graph["events"]])
        # A tied event can be reached via a later event on an independent
        # backwards traversal only if that traversal is explicitly started;
        # this extractor preserves each anchor-relative direction.
        validate_graph(graph, self.db, self.kg)
        for e in graph["events"]:
            if e["row"] == 1:
                continue
            parent = next(p for p in graph["events"] if p["row"] == e["selection"]["parent_row"])
            if e["selection"]["direction"] == "before":
                self.assertLess(e["ord"], parent["ord"])
            else:
                self.assertGreater(e["ord"], parent["ord"])

    def test_budget_past_and_tamper(self):
        graph = extract(self.db, self.rec, 3, self.kg, mode="past", budget=2)
        self.assertLessEqual(len(graph["events"]), 2)
        self.assertTrue(all(e["ord"] < 2 for e in graph["events"] if e["row"] != 3))
        tampered = copy.deepcopy(graph)
        tampered["events"][0]["op"] = "RegDeleteKey"
        with self.assertRaises(ValueError):
            validate_graph(tampered, self.db, self.kg)

    def test_model_view_excludes_labels_identifiers_and_timestamps(self):
        graph = extract(self.db, self.rec, 3, self.kg)
        for node in symbolic(graph)["nodes"].values():
            self.assertEqual(set(node), {"kind", "operation", "anchor", "knowledge"})
            self.assertNotIn("SECRET", json.dumps(node))
            self.assertNotIn("MaliciousFiles", json.dumps(node))
        # Changing annotation artifacts leaves model graph unchanged.
        edited = copy.deepcopy(graph)
        for e in edited["events"]:
            e["label"] = "T0000"
            e["timestamp_raw"] = "changed"
            e["raw_sha"] = "changed"
        self.assertEqual(symbolic(graph), symbolic(edited))

    def test_raw_trace_and_source_mutation(self):
        from ants_kgraphier.analyst import trace
        result = trace(self.db, self.rec, 1, self.root)
        self.assertEqual(result["raw_event"], self.rows[1])
        self.path.write_text("[]")
        with self.assertRaises(ValueError):
            trace(self.db, self.rec, 1, self.root)

    def test_preserves_registry_identity_and_unknown_boundary(self):
        a = self.db.execute("SELECT dst FROM events WHERE row=0").fetchone()[0]
        b = self.db.execute("SELECT dst FROM events WHERE row=4").fetchone()[0]
        self.assertNotEqual(a, b)
        info = self.kg.annotate("HKLM\\SYSTEM", "RegQueryValue")
        self.assertEqual(info["boundary"], "unresolved")
        self.assertNotEqual(info["match"], "exact_key")
        self.assertLess(len(info["node_ids"]), len(info["lexical_node_ids"]))

    def test_exhaustive_and_query_conditioned_anchors(self):
        from ants_kgraphier.extract import export_candidates, export_query_candidates
        from ants_kgraphier.io import jsonl
        result = export_candidates(self.db, self.kg, self.root / "all", {"g": "test"}, per_recording=0)
        self.assertEqual(result["recordings"][0]["sampled"], 6)
        self.assertTrue(all(g["inclusion_probability"] == 1 for g in jsonl(self.root / "all/graphs.jsonl")))
        result = export_query_candidates(self.db, self.kg, self.root / "query", {"g": "test"},
                                         "HKLM\\SYSTEM", "RegSetValue")
        self.assertEqual(result["recordings"][0]["matched_anchors"], 5)
        self.assertEqual(result["recordings"][0]["operation_population"], 6)
        for graph in jsonl(self.root / "query/graphs.jsonl"):
            validate_graph(graph, self.db, self.kg)


class BackboneTests(unittest.TestCase):
    def test_real_upstream_order_formula_and_direction(self):
        import torch
        from ants_kgraphier.backbone import make_model
        torch.set_num_threads(1)
        model = make_model(ROOT / "vendor/ProvG-Searcher", 8)
        a = torch.tensor([[2., 3.]])
        b = torch.tensor([[1., 2.]])
        self.assertEqual(model.predict((a, b)).item(), 0)
        self.assertEqual(model.predict((b, a)).item(), 2)
        self.assertEqual(model.criterion((a, b), torch.tensor([1])).item(), 0)
        self.assertEqual(model.criterion((a, b), torch.tensor([0])).item(), 1)

    def test_exact_verifier_rejects_wrong_operation_direction_and_anchor(self):
        from ants_kgraphier.retrieval import contains, nxgraph
        from ants_kgraphier.analyst import functional_query
        kg = Knowledge(ROOT.parent / "artifacts/knowledge-vault/kg.json")
        query = functional_query(kg, "HKLM\\SYSTEM", "RegSetValue")
        self.assertTrue(contains(nxgraph(query), nxgraph(query)))
        bad = copy.deepcopy(query)
        bad["nodes"]["operation"]["operation"] = "RegQueryValue"
        self.assertFalse(contains(nxgraph(bad), nxgraph(query)))
        bad = copy.deepcopy(query)
        bad["edges"][0] = ("operation", "process", 0)
        self.assertFalse(contains(nxgraph(bad), nxgraph(query)))

    def test_encoder_has_gradient_and_permutation_invariance(self):
        import torch
        from torch_geometric.data import Batch
        from ants_kgraphier.backbone import Features, make_model
        from ants_kgraphier.analyst import functional_query
        kg = Knowledge(ROOT.parent / "artifacts/knowledge-vault/kg.json")
        graph = functional_query(kg, "HKLM\\SYSTEM", "RegSetValue")
        f = Features(kg.nodes, ["RegSetValue"])
        model = make_model(ROOT / "vendor/ProvG-Searcher", f.dim)
        model.eval()
        a = model.emb_model(Batch.from_data_list([f.encode(graph)]))
        rename = {k: "renamed" + str(i) for i, k in enumerate(reversed(graph["nodes"]))}
        changed = {"nodes": {rename[k]: v for k, v in graph["nodes"].items()},
                   "edges": [(rename[a], rename[b], t) for a, b, t in graph["edges"]]}
        b = model.emb_model(Batch.from_data_list([f.encode(changed)]))
        self.assertTrue(torch.allclose(a, b, atol=1e-6))
        a.sum().backward()
        self.assertTrue(any(p.grad is not None and p.grad.abs().sum() > 0 for p in model.parameters()))


if __name__ == "__main__":
    unittest.main()
