"""One target's bounded research session; no evaluator or label access."""

from dataclasses import asdict
import json

from ..common.files import object_hash
from ..models.contracts import BudgetExceeded, InferenceError
from .budget import Budget
from .evidence import Evidence
from .prompts import fit
from .schemas import DECISION, action_schema
from .tools import ToolBox
from .validation import decision, parse_output
from .history import reveal_history


class AgentSession:
    def __init__(self, adapter, repository, context, events, config, trace=None):
        self.adapter, self.repository = adapter, repository
        self.context, self.events = context, events
        self.config = config
        self.budget = Budget(**config.get("limits", {}))
        self.evidence = Evidence()
        self.toolbox = ToolBox(repository, events, self.evidence, config.get("template_candidates", False))
        self.trace = trace or (lambda kind, payload: None)
        self.observations = []
        self.rounds = 0
        self.retrieval_done = False
        self.delivered = self.evidence.packet()
        self.final_input = None
        self.mode = "graph"
        self.replay_packet = None
        self.decision_calls = 0
        self.pending_decision = None

    def infer(self, task, schema, reserve_calls=0, repair=None):
        packet = self.replay_packet if self.replay_packet is not None else self.evidence.packet(self.mode)
        if repair and self.final_input is not None:
            packet = self.final_input["knowledge"]
        messages, delivered, count = fit(self.adapter, self.context, packet, schema,
                                         self.budget.max_input, task, self.observations, repair)
        if (self.replay_packet is not None or repair) and delivered != packet:
            raise BudgetExceeded("Replay or repair would change delivered evidence; refusing to prune")
        self.budget.allow(count, reserve_calls)
        self.delivered = delivered
        if task == "decision":
            self.final_input = {"context": self.context, "knowledge": delivered,
                                "tool_observations": self.observations}
        self.budget.start()
        if task == "decision":
            self.decision_calls += 1
        call_index = self.budget.calls
        self.trace("model_request", {"call_index": call_index, "task": task, "messages": messages,
                                    "schema": schema, "input_tokens_preflight": count})
        try:
            reply = self.adapter.generate(messages, schema, self.budget.max_output)
        except InferenceError as exc:
            if exc.may_have_generated:
                self.budget.uncertain()
            self.trace("model_error", {"call_index": call_index, "error": str(exc),
                                      "unknown_usage": exc.may_have_generated, "response": exc.response})
            raise
        self.trace("model_reply", {"call_index": call_index, **asdict(reply)})
        self.budget.finish(reply)
        if reply.finish_reason != "stop":
            raise ValueError("Incomplete model output: " + str(reply.finish_reason))
        return reply.content

    def retrieve_once(self):
        self.rounds += 1
        text = ""
        try:
            schema = action_schema(self.toolbox.dynamic_history is not None)
            text = self.infer("action", schema, reserve_calls=2)
            action = parse_output(text, schema)
        except BudgetExceeded as exc:
            self.retrieval_done = True
            self.trace("retrieval_budget_stop", {"error": str(exc)})
            return
        except ValueError as exc:
            requested = 0
            try:
                invalid = json.loads(text)
                if isinstance(invalid, dict) and isinstance(invalid.get("calls"), list):
                    requested = len(invalid["calls"])
            except ValueError:
                pass
            self.toolbox.requests += requested
            self.observations.append({"status": "invalid_action", "error": str(exc)})
            self.trace("invalid_action", {"error": str(exc), "requested_tool_count": requested})
            self.retrieval_done = True
            return
        if action["action"] == "finalize":
            self.retrieval_done = True
            return
        # Freeze visibility for the entire batch: no same-round dependent requests.
        supplied_nodes = {n["id"] for n in self.delivered["nodes"]}
        supplied_events = {self.context["target"]["id"]} | {e["id"] for e in self.context["history"]}
        for call in action["calls"]:
            fingerprint = object_hash(call)
            duplicate = fingerprint in self.toolbox.seen
            self.toolbox.seen.add(fingerprint)
            try:
                result = self.toolbox.call(call, supplied_nodes, supplied_events)
                observation = {"tool": call["tool"], "arguments": call["arguments"], "status": "ok", "duplicate": duplicate}
                self.trace("tool_reply", {**observation, "result": result})
                if call["tool"] == "get_prior_context":
                    reveal_history(self, result["history"])
            except (ValueError, KeyError) as exc:
                observation = {"tool": call["tool"], "arguments": call["arguments"], "status": "rejected", "error": str(exc), "duplicate": duplicate}
                self.trace("tool_error", observation)
            self.observations.append(observation)

    def classify(self):
        errors = []
        while self.pending_decision is not None or self.decision_calls < 2:
            try:
                if self.pending_decision is not None:
                    reply, packet = self.pending_decision
                    self.pending_decision = None
                    self.delivered = packet["knowledge"]
                    self.final_input = packet
                    if reply["prompt_tokens"] > self.budget.max_input or reply["completion_tokens"] > self.budget.max_output:
                        raise BudgetExceeded("Checkpointed response exceeded per-call budget")
                    if reply["finish_reason"] != "stop":
                        raise ValueError("Incomplete checkpointed model output")
                    text = reply["content"]
                else:
                    text = self.infer("decision", DECISION, repair=errors[-1] if errors else None)
                events = {self.context["target"]["id"]} | {e["id"] for e in self.context["history"]}
                nodes = {n["id"] for n in self.delivered["nodes"]}
                answer = decision(text, events, nodes)
                return self.result("abstained" if answer["prediction"] == "insufficient_evidence" else "valid", answer)
            except ValueError as exc:
                errors.append(str(exc))
                self.trace("validation_error", {"attempt": self.decision_calls - 1, "error": str(exc)})
        return self.result("invalid_output", error="; ".join(errors) or "Decision attempt allowance exhausted before checkpoint completion")

    def result(self, status, answer=None, error=None):
        return {"status": status, "answer": answer, "error": error, "usage": self.budget.usage(),
                "tool_requests": self.toolbox.requests, "retrieval_rounds": self.rounds,
                "tool_observations": self.observations, "final_input": self.final_input,
                "backend": self.adapter.backend, "synthetic": self.adapter.backend == "mock"}

    def execute(self, condition, orchestrator="native"):
        try:
            if self.budget.input_tokens + self.budget.output_tokens + self.budget.reserved_unknown > self.budget.max_total:
                raise BudgetExceeded("Checkpointed usage exceeded total budget")
            if self.decision_calls:
                # A final decision was already attempted; never restart retrieval/review.
                return self.classify()
            if condition == "agent":
                if orchestrator == "langgraph":
                    from .graph import execute_graph
                    return execute_graph(self)
                if orchestrator != "native":
                    raise ValueError("Unknown orchestrator")
                while self.rounds < 2 and not self.retrieval_done:
                    self.retrieve_once()
            elif condition == "budget":
                for _ in range(2):
                    # Fixed review schedule, no autonomous retrieval; replies are provisional observations.
                    try:
                        text = self.infer("review", DECISION, reserve_calls=2)
                        review = decision(text, {"event_0"} | {e["id"] for e in self.context["history"]},
                                          {n["id"] for n in self.delivered["nodes"]})
                        self.observations.append({"status": "provisional_review", "review": review})
                    except ValueError as exc:
                        self.observations.append({"status": "invalid_review", "error": str(exc)})
                    except BudgetExceeded:
                        break
            return self.classify()
        except BudgetExceeded as exc:
            return self.result("budget_exhausted", error=str(exc))
        except InferenceError as exc:
            return self.result("inference_error", error=str(exc))
