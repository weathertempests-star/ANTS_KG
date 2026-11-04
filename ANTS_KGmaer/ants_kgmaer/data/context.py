"""Construct per-target aliases and partial-order history, without labels or provenance."""

import copy


def public_event(event, alias, order_group, normalized=True, include_value_data=False):
    facts = event["facts"]
    result = {"id": alias, "order_group": order_group, "relation": facts["relation"],
              "actor": {"id": "process_0", **copy.deepcopy(facts["actor"])},
              "target": copy.deepcopy(facts["target"])}
    if normalized and "registry" in facts:
        result["registry"] = copy.deepcopy(facts["registry"])
    if include_value_data and "registry" in facts:
        result["value_data"] = facts.get("optional_value_data")
    return result


def build_context(store, event_id, k=0, normalized=True, include_value_data=False):
    target = store.get(event_id)
    history = store.prior(target, k)
    orders = sorted({e["order_ref"] for e in history if e["order_ref"] is not None})
    group = {value: i for i, value in enumerate(orders)}
    events = {"event_0": target}
    public_history = []
    for index, event in enumerate(history, 1):
        alias = "event_" + str(index)
        events[alias] = event
        public_history.append(public_event(event, alias, group[event["order_ref"]], normalized, include_value_data))
    packet = {"target": public_event(target, "event_0", len(orders), normalized, include_value_data),
              "history": public_history,
              "context_limits": ["Same order_group means no known internal order.",
                                 "Only strictly prior events from the same recording and process are supplied.",
                                 "Order groups are not elapsed time; outcome is not recorded."]}
    if not target["facts"]["actor_identity_known"]:
        packet["context_limits"].append("Missing process identity; no history joined.")
    return packet, events


def experiment_context(store, event_id, config):
    dynamic = config.get("dynamic_history", False)
    packet, events = build_context(store, event_id, 16 if dynamic else config.get("history_k", 0),
                                   config["condition"] != "raw", config.get("include_value_data", False))
    candidates = packet["history"] if dynamic else None
    if dynamic:
        packet["history"] = []
    return packet, events, candidates
