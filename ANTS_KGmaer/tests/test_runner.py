from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ants_kgmaer.common.files import jsonl, read_json, write_json
from ants_kgmaer.experiments.config import load_config
from ants_kgmaer.experiments.runner import execute_run
from ants_kgmaer.data.sampling import select_targets
from ants_kgmaer.models.mock import MockAdapter
from ants_kgmaer.experiments.journal import RunJournal

import test_data_pipeline


class RunnerTests(unittest.TestCase):
    def setUp(self):
        fixture = test_data_pipeline.DataPipelineTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.root = fixture.root
        self.dataset, _ = fixture.fixture()
        self.selection = self.root / "selection"
        select_targets(self.dataset, self.selection, negatives=1)

    def config(self, condition="normalized"):
        path = self.root / (condition + ".json")
        if not path.exists():
            write_json(path, {"schema": "ants-run-config-1", "condition": condition,
                             "model": {"backend": "mock"}, "history_k": 0})
        return path

    def test_all_connected_conditions_complete_and_resume_without_new_calls(self):
        for condition in ("raw", "normalized", "text", "graph", "flat", "unrelated", "agent", "budget"):
            with self.subTest(condition=condition):
                model = MockAdapter()
                output = self.root / ("run-" + condition)
                result = execute_run(self.config(condition), self.dataset, self.selection, output, adapter=model)
                self.assertTrue(result["complete"])
                self.assertEqual(result["target_count"], 4)
                self.assertTrue(result["engineering_only"])
                count = len(model.requests)
                execute_run(self.config(condition), self.dataset, self.selection, output, adapter=model)
                self.assertEqual(len(model.requests), count)
                self.assertEqual(len(list(jsonl(output / "predictions.jsonl"))), 4)

    def test_interrupted_inference_keeps_unknown_cost_on_resume(self):
        model = MockAdapter([RuntimeError("simulated process interruption")])
        output = self.root / "interrupted"
        with self.assertRaisesRegex(RuntimeError, "interruption"):
            execute_run(self.config(), self.dataset, self.selection, output, adapter=model)
        execute_run(self.config(), self.dataset, self.selection, output, adapter=MockAdapter())
        results = list(jsonl(output / "predictions.jsonl"))
        resumed = [item for item in results if item["usage"]["unknown_usage_attempts"]]
        self.assertEqual(len(resumed), 1)
        self.assertEqual(resumed[0]["usage"]["unknown_token_upper_bound"], 4608)
        self.assertEqual(resumed[0]["usage"]["calls"], 2)

    def test_generated_file_edits_are_not_silently_replaced(self):
        output = self.root / "managed"
        execute_run(self.config(), self.dataset, self.selection, output)
        (output / "predictions.jsonl").write_text("manual edit")
        with self.assertRaisesRegex(ValueError, "artifact changed"):
            execute_run(self.config(), self.dataset, self.selection, output)
        self.assertEqual((output / "predictions.jsonl").read_text(), "manual edit")

    def test_plaintext_credentials_in_config_are_rejected(self):
        path = self.config()
        config = read_json(path)
        config["model"]["api_key"] = "secret"
        write_json(path, config, replace=True)
        with self.assertRaisesRegex(ValueError, "credentials"):
            load_config(path)

    def test_replay_preserves_final_packet_and_accounts_for_acquisition(self):
        source = self.root / "source-agent"
        execute_run(self.config("agent"), self.dataset, self.selection, source)
        replay_config = self.root / "replay-config.json"
        write_json(replay_config, {"schema": "ants-run-config-1", "condition": "replay",
                                  "model": {"backend": "mock"}, "replay_run": str(source)})
        output = self.root / "replayed"
        execute_run(replay_config, self.dataset, self.selection, output)
        source_packets = {r["event_id"]: r["final_input"] for r in jsonl(source / "evidence_packets.jsonl")}
        replay_packets = {r["event_id"]: r["final_input"] for r in jsonl(output / "evidence_packets.jsonl")}
        self.assertEqual(source_packets, replay_packets)
        for result in jsonl(output / "predictions.jsonl"):
            self.assertEqual(result["usage"]["calls"], 1)
            self.assertGreater(result["replay"]["acquisition_usage"]["calls"], 0)
            self.assertEqual(result["tool_requests"], 0)
        # A resumed replay cannot consume more inference calls.
        model = MockAdapter()
        execute_run(replay_config, self.dataset, self.selection, output, adapter=model)
        self.assertEqual(len(model.requests), 0)

    def test_replay_refuses_different_history(self):
        source = self.root / "source-agent"
        execute_run(self.config("agent"), self.dataset, self.selection, source)
        replay_config = self.root / "replay-config.json"
        write_json(replay_config, {"schema": "ants-run-config-1", "condition": "replay", "history_k": 16,
                                  "model": {"backend": "mock"}, "replay_run": str(source)})
        with self.assertRaisesRegex(ValueError, "history_k"):
            execute_run(replay_config, self.dataset, self.selection, self.root / "replayed")

    def test_received_decision_survives_crash_before_result_commit(self):
        output = self.root / "reply-checkpoint"
        with patch.object(RunJournal, "finish", side_effect=RuntimeError("commit interrupted")):
            with self.assertRaisesRegex(RuntimeError, "commit interrupted"):
                execute_run(self.config(), self.dataset, self.selection, output)
        model = MockAdapter()
        execute_run(self.config(), self.dataset, self.selection, output, adapter=model)
        self.assertEqual(len(model.requests), 3)
        self.assertEqual({row["usage"]["calls"] for row in jsonl(output / "predictions.jsonl")}, {1})

    def test_repair_allowance_does_not_reset_after_interruption(self):
        output = self.root / "repair-checkpoint"
        with patch.object(RunJournal, "finish", side_effect=RuntimeError("commit interrupted")):
            with self.assertRaisesRegex(RuntimeError, "commit interrupted"):
                execute_run(self.config(), self.dataset, self.selection, output, adapter=MockAdapter(["bad", "bad"]))
        model = MockAdapter()
        execute_run(self.config(), self.dataset, self.selection, output, adapter=model)
        self.assertEqual(len(model.requests), 3)
        invalid = [row for row in jsonl(output / "predictions.jsonl") if row["status"] == "invalid_output"]
        self.assertEqual(len(invalid), 1)
        self.assertEqual(invalid[0]["usage"]["calls"], 2)

    def test_config_cannot_increase_protocol_budget(self):
        path = self.config()
        config = read_json(path)
        config["limits"] = {"max_calls": 5}
        write_json(path, config, replace=True)
        with self.assertRaisesRegex(ValueError, "protocol maxima"):
            load_config(path)


if __name__ == "__main__":
    unittest.main()
