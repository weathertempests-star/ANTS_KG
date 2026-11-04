import copy
import tempfile
import unittest
from pathlib import Path

from ants_kgmaer.agent.evidence import Evidence, prune_one
from ants_kgmaer.agent.tools import ToolBox
from ants_kgmaer.knowledge.repository import KnowledgeRepository
from ants_kgmaer.models.http import check_origin
from ants_kgmaer.models.vllm import VllmAdapter


def registry(boundary="key_confirmed"):
    return {"lookup_target": r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager",
            "key_path": r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager",
            "value_name": None, "path_format": "canonical", "boundary_status": boundary,
            "view": "not_recorded"}


class KnowledgeToolsTests(unittest.TestCase):
    def test_uncertain_boundary_cannot_be_reported_as_complete(self):
        repository = KnowledgeRepository()
        result = repository.lookup(registry("unresolved"))
        self.assertEqual(result["match"], "boundary_unresolved")
        self.assertFalse(result["path_complete"])
        self.assertFalse(result["explanations_complete"])
        self.assertEqual(len(result["nodes"]), 5)

    def test_cache_does_not_mutate_graph_and_preserves_cannot_infer(self):
        with tempfile.TemporaryDirectory() as temp:
            repository = KnowledgeRepository(cache_path=Path(temp) / "cache.sqlite")
            self.addCleanup(repository.close)
            before = repository.engine.to_dict()
            result = repository.lookup(registry())
            self.assertEqual(repository.lookup(registry()), result)
            self.assertEqual(before, repository.engine.to_dict())
            for node in result["nodes"]:
                self.assertTrue(node["research"]["cannot_infer"])
                self.assertIn("path_sources", node)

    def test_tool_scope_and_rejected_requests_consume_budget(self):
        repository, evidence = KnowledgeRepository(), Evidence()
        toolbox = ToolBox(repository, {"event_0": {"facts": {"registry": registry()}}}, evidence)
        call = {"tool": "lookup_registry", "arguments": {"event_ids": ["future_event"]}}
        for _ in range(4):
            with self.assertRaises(ValueError):
                toolbox.call(call, set(), {"event_0"})
        self.assertEqual(toolbox.requests, 4)
        with self.assertRaisesRegex(ValueError, "budget"):
            toolbox.call({"tool": "lookup_registry", "arguments": {"event_ids": ["event_0"]}}, set(), {"event_0"})
        self.assertEqual(evidence.nodes, {})

    def test_node_expansion_requires_delivered_seed(self):
        repository, evidence = KnowledgeRepository(), Evidence()
        toolbox = ToolBox(repository, {"event_0": {"facts": {"registry": registry()}}}, evidence)
        toolbox.call({"tool": "lookup_registry", "arguments": {"event_ids": ["event_0"]}}, set(), {"event_0"})
        node = next(iter(evidence.nodes))
        with self.assertRaises(ValueError):
            toolbox.call({"tool": "expand_knowledge", "arguments": {"node_ids": [node]}}, set(), {"event_0"})
        toolbox.call({"tool": "expand_knowledge", "arguments": {"node_ids": [node]}}, {node}, {"event_0"})

    def test_pruning_keeps_whole_remaining_node_claims(self):
        repository, evidence = KnowledgeRepository(), Evidence()
        evidence.add(repository.lookup(registry()), "event_0")
        packet = evidence.packet()
        before = copy.deepcopy(packet["nodes"])
        self.assertTrue(prune_one(packet))
        self.assertEqual(packet["nodes"], before[:-1])
        self.assertEqual(packet["omitted_node_ids"], [before[-1]["id"]])

    def test_transport_configuration_rejects_public_or_credential_urls(self):
        self.assertFalse(check_origin("http://192.168.50.10:8000"))
        self.assertTrue(check_origin("http://127.0.0.1:8000"))
        for origin in ["http://8.8.8.8:8000", "http://key:secret@127.0.0.1", "http://localhost/v1"]:
            with self.assertRaises(ValueError):
                check_origin(origin)

    def test_adapter_tokenization_and_generation_protocol(self):
        class Transport:
            def __init__(self):
                self.requests = []

            def request(self, path, payload=None):
                self.requests.append((path, payload))
                if path == "/tokenize":
                    return {"count": 20}
                return {"choices": [{"message": {"content": "{}"}, "finish_reason": "stop"}],
                        "usage": {"prompt_tokens": 20, "completion_tokens": 2, "total_tokens": 22}}

        transport = Transport()
        adapter = VllmAdapter({"served_model": "registry-slm"}, transport)
        messages = [{"role": "user", "content": "synthetic input"}]
        self.assertEqual(adapter.count_tokens(messages), 20)
        self.assertEqual(adapter.count_tokens(messages), 20)
        self.assertEqual(len(transport.requests), 1)
        reply = adapter.generate(messages, {"type": "object"}, 512)
        self.assertEqual(reply.prompt_tokens, 20)
        request = transport.requests[-1][1]
        self.assertFalse(request["chat_template_kwargs"]["enable_thinking"])
        self.assertEqual(request["response_format"]["type"], "json_schema")


if __name__ == "__main__":
    unittest.main()
