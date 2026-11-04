import csv
import unittest

from ants_kgmaer.common.files import jsonl, read_json, write_json
from ants_kgmaer.evaluation.scoring import evaluate_run
from ants_kgmaer.experiments.preparation import prepare_inputs
from ants_kgmaer.experiments.population import audit_population
import test_evaluation


class PreparationTests(unittest.TestCase):
    setUp = test_evaluation.EvaluationTests.setUp

    def prepare(self):
        output = self.root / "prepared"
        prepare_inputs(self.config, self.dataset, self.selection, output)
        return output

    def test_unresolved_boundaries_and_label_free_contexts(self):
        prepared = self.prepare()
        records = list(jsonl(prepared / "coverage_events.jsonl"))
        self.assertEqual(len(records), 4)
        ambiguous = [r for r in records if r["match"] == "boundary_unresolved"]
        self.assertEqual(len(ambiguous), 1)
        self.assertFalse(ambiguous[0]["path_complete"])
        self.assertFalse(ambiguous[0]["explanations_complete"])
        self.assertEqual(len(list(jsonl(prepared / "contexts.jsonl"))), 4)
        for name in ("contexts.jsonl", "kg_context_cache.jsonl"):
            text = (prepared / name).read_text()
            for forbidden in ('"label"', '"label_binary"', '"truth"', '"timestamp_raw"'):
                self.assertNotIn(forbidden, text)
        with (prepared / "coverage_report.csv").open() as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(sum(int(row["raw_events"]) for row in rows), 4)
        self.assertEqual(sum(float(row["weighted_events"]) for row in rows), 5)

    def test_evaluation_coverage_strata_preserve_denominators(self):
        prepared = self.prepare()
        output = self.root / "scored"
        evaluate_run(self.dataset, self.selection, self.run, output, prepared)
        metrics = read_json(output / "metrics.json")
        self.assertEqual(sum(v["raw_events"] for v in metrics["strata"]["match"].values()), 4)
        self.assertEqual(metrics["strata"]["match"]["boundary_unresolved"]["raw_events"], 1)
        self.assertIsNotNone(metrics["coverage_preparation_manifest_sha256"])

    def test_changed_coverage_is_rejected(self):
        prepared = self.prepare()
        with (prepared / "coverage_events.jsonl").open("a") as stream:
            stream.write('{}\n')
        with self.assertRaisesRegex(ValueError, "changed artifact"):
            evaluate_run(self.dataset, self.selection, self.run, self.root / "scored", prepared)

    def test_different_template_policy_is_rejected(self):
        config = read_json(self.config)
        config["template_candidates"] = True
        write_json(self.config, config, replace=True)
        prepared = self.prepare()
        with self.assertRaisesRegex(ValueError, "template_candidates"):
            evaluate_run(self.dataset, self.selection, self.run, self.root / "scored", prepared)

    def test_population_counts_every_registry_row_including_quarantine(self):
        output = self.root / "population"
        manifest = audit_population(self.dataset, output)
        summary = read_json(output / "summary.json")
        self.assertEqual(manifest["registry_events"], 6)
        self.assertLess(manifest["unique_queries"], 6)
        self.assertEqual(summary["truth_counts"], {"0": 3, "1": 2, "quarantined": 1})
        self.assertEqual(sum(summary["match_counts"].values()), 6)
        self.assertEqual(summary["match_counts"]["boundary_unresolved"], 1)


if __name__ == "__main__":
    unittest.main()
