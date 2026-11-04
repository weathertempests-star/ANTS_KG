import json
import unittest

from ants_kgmaer.common.files import jsonl, write_json
from ants_kgmaer.data.store import EventStore
from ants_kgmaer.experiments.journal import RunJournal
from ants_kgmaer.experiments.runner import execute_run, prepare_session
from ants_kgmaer.knowledge.repository import KnowledgeRepository
from ants_kgmaer.models.mock import MockAdapter
import test_data_pipeline
from ants_kgmaer.data.sampling import select_targets


class HistoryAdapter(MockAdapter):
    def generate(self, messages, schema, max_tokens):
        if "anyOf" in schema:
            body = json.loads(messages[-1]["content"])
            self.responses.append({"action": "finalize"} if body["tool_observations"] else {
                "action": "retrieve", "calls": [{"tool": "get_prior_context", "arguments": {"k": 16}}]})
        return super().generate(messages, schema, max_tokens)


class DynamicHistoryTests(unittest.TestCase):
    def setUp(self):
        fixture = test_data_pipeline.DataPipelineTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.root = fixture.root
        self.dataset, _ = fixture.fixture()
        self.store = EventStore(self.dataset / "events.sqlite")
        self.repo = KnowledgeRepository()
        self.addCleanup(self.store.close)
        self.addCleanup(self.repo.close)
        self.ids = list(self.store.registry_ids("a"))
        self.config = {"schema": "ants-run-config-1", "condition": "agent", "history_k": 0,
                       "dynamic_history": True, "model": {"backend": "mock"}}

    def session(self, adapter, target=None, trace=None):
        return prepare_session(adapter, self.repo, self.store, target or self.ids[2], self.config, trace)

    def test_context_reveal_cannot_enable_dependent_lookup_in_same_batch(self):
        calls = [{"tool": "get_prior_context", "arguments": {"k": 2}},
                 {"tool": "lookup_registry", "arguments": {"event_ids": ["event_1"]}}]
        adapter = MockAdapter([{"action": "retrieve", "calls": calls},
                               {"action": "retrieve", "calls": [calls[1]]}])
        trace = []
        session = self.session(adapter, trace=lambda k, v: trace.append((k, v)))
        self.assertEqual(session.context["history"], [])
        result = session.execute("agent")
        self.assertEqual(len(result["final_input"]["context"]["history"]), 2)
        self.assertEqual(sum(kind == "tool_error" for kind, _ in trace), 1)
        self.assertEqual(result["tool_requests"], 3)
        first = json.loads(adapter.requests[0][-1]["content"])
        second = json.loads(adapter.requests[1][-1]["content"])
        self.assertEqual(first["events"]["history"], [])
        self.assertEqual(len(second["events"]["history"]), 2)
        self.assertEqual(second["events"]["history"][0]["order_group"], second["events"]["history"][1]["order_group"])

    def test_equal_order_events_are_not_revealed(self):
        session = self.session(HistoryAdapter(), target=self.ids[1])
        result = session.execute("agent")
        self.assertEqual(result["final_input"]["context"]["history"], [])

    def test_history_is_restored_after_interrupted_action(self):
        journal = RunJournal(self.root / "journal.sqlite", "fixture")
        self.addCleanup(journal.close)
        target = self.ids[2]
        journal.begin(target)
        trace = lambda k, v: journal.trace(target, k, v)
        adapter = MockAdapter([{"action": "retrieve", "calls": [{"tool": "get_prior_context", "arguments": {"k": 2}}]},
                               RuntimeError("interrupted")])
        with self.assertRaisesRegex(RuntimeError, "interrupted"):
            self.session(adapter, trace=trace).execute("agent")
        resumed = self.session(MockAdapter(), trace=trace)
        journal.restore(target, resumed)
        self.assertEqual(len(resumed.context["history"]), 2)
        result = resumed.execute("agent")
        self.assertEqual(result["usage"]["calls"], 3)
        self.assertEqual(result["usage"]["unknown_usage_attempts"], 1)
        self.assertEqual(result["retrieval_rounds"], 2)

    def test_dynamic_replay_uses_identical_acquired_history(self):
        selection = self.root / "selection"
        select_targets(self.dataset, selection, negatives=1)
        config = self.root / "agent.json"
        write_json(config, self.config)
        source = self.root / "agent-run"
        execute_run(config, self.dataset, selection, source, adapter=HistoryAdapter())
        replay = self.root / "replay.json"
        write_json(replay, {**self.config, "condition": "replay", "replay_run": str(source)})
        output = self.root / "replayed"
        execute_run(replay, self.dataset, selection, output)
        self.assertEqual(list(jsonl(source / "evidence_packets.jsonl")), list(jsonl(output / "evidence_packets.jsonl")))


if __name__ == "__main__":
    unittest.main()
