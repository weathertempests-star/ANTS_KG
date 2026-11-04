"""Per-target resource accounting; unresolved attempts reserve their upper bound."""

from dataclasses import dataclass

from ..models.contracts import BudgetExceeded


@dataclass
class Budget:
    max_input: int = 4096
    max_output: int = 512
    max_calls: int = 4
    max_total: int = 18432
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    unknown_attempts: int = 0
    reserved_unknown: int = 0

    def allow(self, input_count, reserve_calls=0):
        if input_count > self.max_input:
            raise BudgetExceeded("Prompt exceeds input-token limit")
        if self.calls + 1 + reserve_calls > self.max_calls:
            raise BudgetExceeded("Model call budget exhausted")
        required = input_count + self.max_output + reserve_calls * (self.max_input + self.max_output)
        if self.input_tokens + self.output_tokens + self.reserved_unknown + required > self.max_total:
            raise BudgetExceeded("Total token budget exhausted; required later calls are reserved")

    def start(self):
        self.calls += 1

    def finish(self, reply):
        self.input_tokens += reply.prompt_tokens
        self.output_tokens += reply.completion_tokens
        if reply.prompt_tokens > self.max_input or reply.completion_tokens > self.max_output:
            raise BudgetExceeded("Server-reported usage exceeded per-call limits")
        if self.input_tokens + self.output_tokens + self.reserved_unknown > self.max_total:
            raise BudgetExceeded("Server-reported usage exceeded total limit")

    def uncertain(self):
        self.unknown_attempts += 1
        self.reserved_unknown += self.max_input + self.max_output

    def usage(self):
        return {"calls": self.calls, "input_tokens": self.input_tokens, "output_tokens": self.output_tokens,
                "unknown_usage_attempts": self.unknown_attempts, "unknown_token_upper_bound": self.reserved_unknown}
