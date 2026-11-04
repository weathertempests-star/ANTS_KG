import csv
import json
import sqlite3
import unittest

from ants_kgmaer.common.files import jsonl
from ants_kgmaer.evaluation.duplicates import duplicate_sensitivity, equivalence_key, grouped_metrics
from ants_kgmaer.evaluation.review import export_review, import_review
from ants_kgmaer.evaluation.scoring import evaluate_run
from ants_kgmaer.experiments.runner import execute_run
from ants_kgmaer.models.mock import MockAdapter
import test_evaluation


class ReviewAndDuplicateTests(unittest.TestCase):
    setUp = test_evaluation.EvaluationTests.setUp

    def test_observed_duplicate_integration(self):
        evaluated = self.root / "evaluated"
        evaluate_run(self.dataset, self.selection, self.run, evaluated)
        result = duplicate_sensitivity(self.dataset, evaluated, self.root / "duplicates.json")
        self.assertTrue(result["engineering_only"])
        for mode in ("exact", "normalized"):
            self.assertEqual(result["results"][mode]["metrics"]["raw_events"], 4)
            self.assertEqual(result["results"][mode]["metrics"]["BA_all"], 0)

    def test_equal_group_mass_and_conflicts_remain_individual(self):
        connection = sqlite3.connect(":memory:")
        self.addCleanup(connection.close)
        connection.execute("CREATE TABLE members(mode,event_id,group_id,truth,prediction,weight,status)")
        rows = [("a", "repeated", 1, 1, 2), ("b", "repeated", 1, 0, 1),
                ("c", "conflict", 0, 0, 5), ("d", "conflict", 1, 1, 1)]
        connection.executemany("INSERT INTO members VALUES('exact',?,?,?,?,?,'valid')", rows)
        result = grouped_metrics(connection, "exact")
        self.assertEqual(result["observed_groups"], 2)
        self.assertEqual(result["conflicting_groups"], 1)
        self.assertEqual(result["conflicting_events_kept_individual"], 2)
        self.assertAlmostEqual(result["metrics"]["support"]["benign"], 1)
        self.assertAlmostEqual(result["metrics"]["support"]["malicious"], 2)
        self.assertAlmostEqual(result["metrics"]["BA_all"], (1 + (1 + 2 / 3) / 2) / 2)

    def test_normalized_groups_do_not_cross_process_recording_order_or_value(self):
        event = {"recording_id": "a", "actor_id": "p", "normalized_signature": "n", "order_ref": 1,
                 "facts": json.dumps({"optional_value_data": "a"})}
        original = equivalence_key(event, "normalized")
        for key, value in (("recording_id", "b"), ("actor_id", "q"), ("order_ref", 2),
                           ("facts", json.dumps({"optional_value_data": "b"}))):
            self.assertNotEqual(original, equivalence_key({**event, key: value}, "normalized"))

    def claim_run(self):
        answer = {"prediction": "benign", "evidence_event_ids": ["event_0"], "knowledge_node_ids": [],
                  "claims": [{"statement": "A Registry operation is observed.", "evidence_ids": ["event_0"]}],
                  "unknowns": [], "score": None}
        run = self.root / "claims"
        execute_run(self.config, self.dataset, self.selection, run, adapter=MockAdapter([answer] * 4))
        return run

    def test_blinded_review_distinguishes_valid_ids_and_human_support(self):
        review = self.root / "review"
        manifest = export_review(self.claim_run(), review, limit=2)
        self.assertEqual(manifest["population_claims"], 4)
        self.assertEqual(manifest["sampled_claims"], 2)
        packets = list(jsonl(review / "blind/packets.jsonl"))
        for packet in packets:
            self.assertEqual(set(packet), {"review_id", "claim", "events", "knowledge"})
        annotations = self.root / "annotations.csv"
        with annotations.open("w", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["review_id", "judgment", "reviewer", "note"])
            for packet, judgment in zip(packets, ("supported", "unsupported")):
                writer.writerow([packet["review_id"], judgment, "fixture-reviewer", "Synthetic judgment for test"])
        result = import_review(review, annotations, self.root / "review-result.json")
        self.assertEqual(result["human_support_rate_reviewed"], 0.5)
        self.assertEqual(result["citation_id_validity_rate_sampled"], 1)
        self.assertEqual(result["completion_rate"], 1)

    def test_empty_and_pending_reviews_never_claim_support(self):
        empty = self.root / "empty-review"
        export_review(self.run, empty)
        result = import_review(empty, empty / "blind/reviews.csv", self.root / "empty-result.json")
        self.assertIsNone(result["human_support_rate_reviewed"])
        self.assertEqual(result["sampled_claims"], 0)
        review = self.root / "pending-review"
        export_review(self.claim_run(), review, limit=2)
        result = import_review(review, review / "blind/reviews.csv", self.root / "pending-result.json")
        self.assertEqual(result["judgments"]["pending"], 2)
        self.assertEqual(result["completion_rate"], 0)
        self.assertIsNone(result["human_support_rate_reviewed"])

    def test_unknown_reviewer_assignment_rejected(self):
        review = self.root / "review"
        export_review(self.run, review)
        annotations = self.root / "wrong.csv"
        annotations.write_text("review_id,judgment,reviewer,note\nforeign,supported,test,note\n")
        with self.assertRaisesRegex(ValueError, "Unknown"):
            import_review(review, annotations, self.root / "invalid.json")


if __name__ == "__main__":
    unittest.main()
