"""vLLM generation and server-tokenizer adapter; no guessed token counts."""

import time

from .contracts import InferenceError, ModelReply
from .http import HttpTransport


class VllmAdapter:
    backend = "vllm"

    def __init__(self, config, transport=None):
        self.config = dict(config)
        self.transport = transport or HttpTransport(config["base_url"], timeout=config.get("timeout", 300))
        self.alias = config["served_model"]
        self._token_cache = {}

    def preflight(self):
        self.transport.request("/health")
        models = self.transport.request("/v1/models")
        if self.alias not in {item["id"] for item in models.get("data", [])}:
            raise ValueError("Configured model alias is not available")
        # Actual revision is operator-attested in the frozen config; the alias alone cannot prove it.
        return {"models": models, "identity_proof": "operator_attested_deployment_manifest_required"}

    def count_tokens(self, messages):
        from ..common.files import object_hash
        key = object_hash(messages)
        if key not in self._token_cache:
            result = self.transport.request("/tokenize", {"model": self.alias, "messages": messages,
                "add_generation_prompt": True, "chat_template_kwargs": {"enable_thinking": False}})
            count = result.get("count")
            if type(count) is not int or count < 0:
                raise InferenceError("Server tokenizer did not return a valid count", may_have_generated=False)
            if len(self._token_cache) >= 1024:
                self._token_cache.clear()
            self._token_cache[key] = count
        return self._token_cache[key]

    def generate(self, messages, schema, max_tokens):
        request = {"model": self.alias, "messages": messages, "max_tokens": max_tokens, "stream": False,
                   "temperature": self.config.get("temperature", 0.7), "top_p": self.config.get("top_p", 0.8),
                   "top_k": self.config.get("top_k", 20), "seed": self.config.get("seed", 20261026),
                   "chat_template_kwargs": {"enable_thinking": False},
                   "response_format": {"type": "json_schema", "json_schema": {
                       "name": "registry_result", "strict": True, "schema": schema}}}
        started = time.perf_counter()
        raw = self.transport.request("/v1/chat/completions", request)
        elapsed = time.perf_counter() - started
        try:
            choice = raw["choices"][0]
            message = choice["message"]
            usage = raw["usage"]
            for field in ("prompt_tokens", "completion_tokens", "total_tokens"):
                if type(usage[field]) is not int or usage[field] < 0:
                    raise ValueError("invalid usage")
            if usage["total_tokens"] != usage["prompt_tokens"] + usage["completion_tokens"]:
                raise ValueError("inconsistent usage")
            if message.get("reasoning_content") or message.get("reasoning"):
                raise ValueError("thinking must be disabled")
            if not isinstance(message["content"], str):
                raise ValueError("missing final content")
            return ModelReply(message["content"], usage["prompt_tokens"], usage["completion_tokens"],
                              choice["finish_reason"], elapsed, raw)
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise InferenceError("Invalid server response: " + str(exc), response=raw) from exc
