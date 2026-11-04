"""Bounded, read-only tool dispatch. Model arguments can reference only supplied IDs."""

import copy


class ToolBox:
    def __init__(self, repository, events, evidence, template_candidates=False, dynamic_history=None):
        self.repository = repository
        self.events = events
        self.evidence = evidence
        self.template_candidates = template_candidates
        self.dynamic_history = dynamic_history
        self.requests = 0
        self.seen = set()

    def call(self, call, supplied_nodes, supplied_events):
        self.requests += 1
        if self.requests > 4:
            raise ValueError("Tool request budget exhausted")
        if not isinstance(call, dict) or set(call) != {"tool", "arguments"}:
            raise ValueError("Tool call requires tool and arguments only")
        tool, args = call["tool"], call["arguments"]
        if not isinstance(args, dict):
            raise ValueError("Tool arguments must be an object")
        if tool == "lookup_registry":
            ids = self._ids(args, "event_ids", supplied_events, 4)
            results = []
            for alias in ids:
                event = self.events[alias]
                if "registry" not in event["facts"]:
                    raise ValueError("lookup_registry requires a Registry event")
                result = self.repository.lookup(event["facts"]["registry"], self.template_candidates)
                results.append({"event_id": alias, **result})
            for result in results:
                self.evidence.add(result, result["event_id"])
            return {"results": results}
        if tool == "expand_knowledge":
            ids = self._ids(args, "node_ids", supplied_nodes, 6)
            result = self.repository.expand(ids)
            self.evidence.add(result)
            return result
        if tool == "get_prior_context" and self.dynamic_history is not None:
            if set(args) != {"k"} or type(args["k"]) is not int or not 0 <= args["k"] <= 16:
                raise ValueError("History k must be an integer in [0,16]")
            return {"history": copy.deepcopy(self.dynamic_history[-args["k"]:] if args["k"] else [])}
        raise ValueError("Unavailable tool")

    @staticmethod
    def _ids(args, field, allowed, maximum):
        if set(args) != {field}:
            raise ValueError("Unexpected tool arguments")
        ids = args[field]
        if not isinstance(ids, list) or not 1 <= len(ids) <= maximum or not all(isinstance(v, str) for v in ids):
            raise ValueError("Invalid ID list")
        if len(set(ids)) != len(ids) or not set(ids) <= set(allowed):
            raise ValueError("IDs must be distinct and already supplied to the model")
        return ids
