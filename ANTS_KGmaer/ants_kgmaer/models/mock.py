"""Deterministic engineering adapter; never a substitute for measured model quality."""

import json

from ..common.files import canonical
from .contracts import ModelReply


class MockAdapter:
    backend = "mock"

    def __init__(self, responses=None):
        self.responses = list(responses or [])
        self.requests = []

    def preflight(self):
        return {"synthetic": True, "warning": "Engineering test adapter, not malicious-detection evidence"}

    def count_tokens(self, messages):
        # Deterministic synthetic units only; never used with a real model.
        return max(1, len(canonical(messages).encode()) // 4)

    def generate(self, messages, schema, max_tokens):
        self.requests.append(messages)
        if self.responses:
            response = self.responses.pop(0)
            if isinstance(response, Exception):
                raise response
            content = response if isinstance(response, str) else canonical(response)
        else:
            body = json.loads(messages[-1]["content"])
            if "anyOf" in schema:
                response = {"action": "finalize"} if body["knowledge"]["nodes"] else {
                    "action": "retrieve", "calls": [{"tool": "lookup_registry", "arguments": {"event_ids": ["event_0"]}}]}
            else:
                response = {"prediction": "insufficient_evidence", "evidence_event_ids": ["event_0"],
                            "knowledge_node_ids": [], "claims": [],
                            "unknowns": ["Synthetic adapter deliberately makes no real detection claim."], "score": None}
            content = canonical(response)
        size = max(1, len(content.encode()) // 4)
        return ModelReply(content, self.count_tokens(messages), min(max_tokens, size),
                          finish_reason="length" if size > max_tokens else "stop", raw_response={"synthetic": True})
