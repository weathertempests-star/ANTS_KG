"""Model reply contract shared by real and deterministic test adapters."""

from dataclasses import dataclass


@dataclass
class ModelReply:
    content: str
    prompt_tokens: int
    completion_tokens: int
    finish_reason: str = "stop"
    latency_seconds: float = 0.0
    raw_response: dict = None


class InferenceError(RuntimeError):
    def __init__(self, message, may_have_generated=True, response=None):
        super().__init__(message)
        self.may_have_generated = may_have_generated
        self.response = response


class BudgetExceeded(RuntimeError):
    pass
