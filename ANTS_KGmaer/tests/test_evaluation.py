"""Evaluate imperfect runs: missing rows must never improve the denominator."""

import unittest

from ants_kgmaer.common.files import canonical, jsonl, read_json, write_json
from ants_kgmaer.data.sampling import select_targets
from ants_kgmaer.evaluation.scoring import evaluate_run, sample_weight
from ants_kgmaer.evaluation.comparison import compare_evaluations
from ants_kgmaer.data.store import readonly
from ants_kgmaer.presentation.report import details, render_report
from ants_kgmaer.experiments.runner import execute_run
import test_data_pipeline


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        fixture = test_data_pipeline.DataPipelineTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.root = fixture.root
        self.dataset, _ = fixture.fixture()
        self.selection = self.root / "selection"
        select_targets(self.dataset, self.selection, negatives=1)
        self.config = self.root / "config.json"
        write_json(self.config, {"schema": "ants-run-config-1", "condition": "normalized",
                                 "model": {"backend": "mock"}})
        self.run = self.root / "run"
        execute_run(self.config, self.dataset, self.selection, self.run)

    def score(self):
        output = self.root / "evaluation"
        manifest = evaluate_run(self.dataset, self.selection, self.run, output)
        return manifest, read_json(output / "metrics.json")

    def partial(self, records):
        # Simulate an interrupted export: no completed manifest claims these files.
        (self.run / "manifest.json").unlink()
        (self.run / "predictions.jsonl").write_text("".join(canonical(r) + "\n" for r in records))

    def test_mock_abstentions_and_sampling_weights(self):
        manifest, metrics = self.score()
        self.assertTrue(manifest["complete"])
        self.assertTrue(metrics["engineering_only"])
        self.assertEqual(metrics["weighted"]["raw_events"], 4)
        self.assertEqual(metrics["weighted"]["coverage"], 0)
        self.assertEqual(metrics["weighted"]["BA_all"], 0)
        # One of six source rows has an unknown annotation and is quarantined.
        self.assertEqual(sum(metrics["weighted"]["support"].values()), 5)
        self.assertEqual(sum(metrics["unweighted"]["support"].values()), 4)
        self.assertEqual(metrics["strata"]["technique"]["T1112"]["support"]["malicious"], 2)
        self.assertIsNone(metrics["strata"]["technique"]["T1112"]["BA_all"])

    def test_missing_predictions_remain_in_all_denominators(self):
        records = list(jsonl(self.run / "predictions.jsonl"))
        self.partial(records[:1])
        _, metrics = self.score()
        self.assertFalse(metrics["run_complete"])
        self.assertEqual(metrics["weighted"]["raw_events"], 4)
        self.assertEqual(metrics["weighted"]["status_counts"]["missing_prediction"], 3)
        self.assertEqual(metrics["weighted"]["BA_all"], 0)

    def test_duplicate_and_foreign_prediction_ids_rejected(self):
        records = list(jsonl(self.run / "predictions.jsonl"))
        self.partial([records[0], records[0]])
        with self.assertRaisesRegex(ValueError, "Duplicate prediction"):
            self.score()
        (self.run / "predictions.jsonl").write_text(canonical({"event_id": "foreign"}) + "\n")
        with self.assertRaisesRegex(ValueError, "outside"):
            evaluate_run(self.dataset, self.selection, self.run, self.root / "foreign-score")

    def test_generated_prediction_tampering_is_rejected(self):
        with (self.run / "predictions.jsonl").open("a") as stream:
            stream.write("{}\n")
        with self.assertRaisesRegex(ValueError, "changed artifact"):
            self.score()

    def test_engineering_limit_is_identical_for_runner_and_evaluator(self):
        config = read_json(self.config)
        config["engineering_limit"] = 1
        write_json(self.config, config, replace=True)
        self.run = self.root / "one-event"
        execute_run(self.config, self.dataset, self.selection, self.run)
        _, metrics = self.score()
        self.assertEqual(metrics["weighted"]["raw_events"], 1)
        self.assertIsNone(metrics["weighted"]["BA_all"])
        self.assertEqual(metrics["recording_macro_BA"]["defined_recordings"], 0)

    def test_bad_sampling_probabilities_rejected(self):
        for probability in (0, -1, 1.1, True, float("nan"), float("inf"), None):
            with self.subTest(probability=probability), self.assertRaises(ValueError):
                sample_weight({"inclusion_probability": probability})

    def test_paired_join_and_positive_delta_against_abstention(self):
        self.score()
        answers = readonly(self.dataset / "answers.sqlite")
        try:
            records = [{"event_id": target["event_id"], "status": "valid",
                        "answer": {"prediction": "malicious" if answers.execute(
                            "SELECT label_binary FROM labels WHERE event_id=?", (target["event_id"],)
                        ).fetchone()[0] else "benign"}}
                       for target in jsonl(self.selection / "targets.jsonl")]
        finally:
            answers.close()
        # Artificial perfect predictions test the scorer, never model performance.
        self.partial(records)
        right = self.root / "perfect-evaluation"
        evaluate_run(self.dataset, self.selection, self.run, right)
        comparison = compare_evaluations(self.root / "evaluation", right, self.root / "comparison.json", 20)
        self.assertEqual(comparison["paired_events"], 4)
        self.assertEqual(comparison["bootstrap"]["delta_BA_all_right_minus_left"], 1)
        self.assertEqual(comparison["bootstrap"]["blocks"], 1)
        self.assertTrue(comparison["engineering_only"])

    def test_paired_join_refuses_different_target_sets(self):
        self.score()
        config = read_json(self.config)
        config["engineering_limit"] = 1
        write_json(self.config, config, replace=True)
        run = self.root / "limited-run"
        execute_run(self.config, self.dataset, self.selection, run)
        right = self.root / "limited-evaluation"
        evaluate_run(self.dataset, self.selection, run, right)
        with self.assertRaisesRegex(ValueError, "missing targets"):
            compare_evaluations(self.root / "evaluation", right, self.root / "comparison.json", 20)

    def test_report_has_real_case_counts_and_escapes_untrusted_text(self):
        self.score()
        output = self.root / "report"
        render_report(self.root / "evaluation", self.run, output)
        document = (output / "report.html").read_text()
        self.assertIn("ENGINEERING / MOCK", document)
        self.assertIn("unresolved: 4 events", document)
        self.assertIn("TP: 0 events", document)
        self.assertIn("No observed cases", document)
        self.assertIn("not detection performance", (output / "EXPERIMENT_REPORT.md").read_text())
        self.assertIn('xmlns="http://www.w3.org/2000/svg"', (output / "per_recording_ba.svg").read_text())
        self.assertNotIn("<script>", details("<script>", {"log": "<script>alert(1)</script>"}))
        self.assertIn("&lt;script&gt;", details("test", {"log": "<script>"}))
        with self.assertRaises(FileExistsError):
            render_report(self.root / "evaluation", self.run, output)


if __name__ == "__main__":
    unittest.main()
