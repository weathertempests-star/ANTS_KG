import json
import unittest

from ants_kgmaer.agent.budget import Budget
from ants_kgmaer.agent.session import AgentSession
from ants_kgmaer.agent.validation import decision, parse_output
from ants_kgmaer.agent.schemas import DECISION
from ants_kgmaer.evaluation.metrics import Accumulator
from ants_kgmaer.evaluation.paired import paired_bootstrap
from ants_kgmaer.knowledge.repository import KnowledgeRepository
from ants_kgmaer.models.contracts import BudgetExceeded, ModelReply
from ants_kgmaer.models.mock import MockAdapter


def abstain():
    return {"prediction": "insufficient_evidence", "evidence_event_ids": ["event_0"],
            "knowledge_node_ids": [], "claims": [], "unknowns": ["Missing behavioral evidence"], "score": None}


class AgentPolicyTests(unittest.TestCase):
    def session(self, responses=None):
        registry = {"lookup_target": r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager",
                    "key_path": r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager",
                    "value_name": None, "path_format": "canonical", "boundary_status": "key_confirmed"}
        context = {"target": {"id": "event_0", "relation": "RegOpenKey"}, "history": [], "context_limits": []}
        events = {"event_0": {"facts": {"registry": registry}}}
        return AgentSession(MockAdapter(responses), KnowledgeRepository(), context, events, {})

    def test_mock_agent_is_bounded_and_explicitly_synthetic(self):
        result = self.session().execute("agent")
        self.assertTrue(result["synthetic"])
        self.assertEqual(result["status"], "abstained")
        self.assertLessEqual(result["usage"]["calls"], 4)
        self.assertEqual(result["tool_requests"], 1)

    def test_bad_final_output_gets_only_one_repair(self):
        session = self.session(["not JSON", "still not JSON"])
        result = session.execute("normalized")
        self.assertEqual(result["status"], "invalid_output")
        self.assertEqual(result["usage"]["calls"], 2)

    def test_fabricated_reference_is_not_accepted(self):
        response = abstain()
        response["knowledge_node_ids"] = ["invented"]
        with self.assertRaises(ValueError):
            decision(json.dumps(response), {"event_0"}, set())

    def test_duplicate_json_fields_are_rejected(self):
        text = json.dumps(abstain()).replace('"score": null', '"score": null, "score": null')
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            parse_output(text, DECISION)

    def test_budget_reserves_later_calls_and_tracks_unknown_usage(self):
        budget = Budget()
        budget.allow(4096, 2)
        budget.start()
        budget.uncertain()
        self.assertEqual(budget.usage()["unknown_token_upper_bound"], 4608)
        with self.assertRaises(BudgetExceeded):
            budget.allow(4097)
        budget.calls = 3
        with self.assertRaises(BudgetExceeded):
            budget.allow(100, 1)

    def test_weighted_macro_recall_is_not_prevalence_accuracy(self):
        metrics = Accumulator()
        metrics.add(0, 0, 1000)
        metrics.add(1, 0, 1)
        self.assertEqual(metrics.result()["BA_all"], 0.5)

    def test_abstentions_count_as_failure_and_single_class_is_na(self):
        metrics = Accumulator()
        metrics.add(0, 0)
        self.assertIsNone(metrics.result()["BA_all"])
        metrics.add(0, 1)
        metrics.add(0, None, status="invalid_output")
        metrics.add(1, 1)
        metrics.add(1, 0)
        metrics.add(1, None, status="abstained")
        result = metrics.result()
        self.assertAlmostEqual(result["BA_all"], 1 / 3)
        self.assertAlmostEqual(result["macro_F1"], 0.4)
        self.assertAlmostEqual(result["coverage"], 2 / 3)
        self.assertEqual(result["selective_BA"], 0.5)
        self.assertEqual(result["raw_events"], 6)

    def test_paired_bootstrap_is_deterministic_and_handles_single_class_draws(self):
        blocks = {"negative": ([[10, 0, 0], [0, 0, 0]], [[10, 0, 0], [0, 0, 0]]),
                  "positive": ([[0, 0, 0], [2, 0, 0]], [[0, 0, 0], [0, 2, 0]])}
        a = paired_bootstrap(blocks, 100)
        self.assertEqual(a, paired_bootstrap(blocks, 100))
        self.assertEqual(a["delta_BA_all_right_minus_left"], 0.5)
        self.assertLess(a["valid_repetitions"], 100)


if __name__ == "__main__":
    unittest.main()
