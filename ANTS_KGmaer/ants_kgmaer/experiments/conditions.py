"""Deterministic retrieval controls, kept separate from autonomous tool policy."""

from ..common.files import object_hash
from ..agent.evidence import Evidence

CONDITIONS = ("raw", "normalized", "text", "graph", "flat", "unrelated", "agent", "replay", "budget")


def fixed_evidence(repository, events, templates=False):
    evidence = Evidence()
    candidates = ["event_0"] + list(reversed([key for key in events if key != "event_0"]))
    candidates = [key for key in candidates if "registry" in events[key]["facts"]][:4]
    for alias in candidates:
        evidence.add(repository.lookup(events[alias]["facts"]["registry"], templates), alias)
    seeds = sorted(evidence.nodes, key=lambda key: (-evidence.nodes[key]["depth"], key))[:6]
    if seeds:
        evidence.add(repository.expand(seeds))
    return evidence


def unrelated_evidence(repository, matched, event_facts, seed):
    excluded = set(matched.nodes)
    excluded.update(n["id"] for n in repository.expand(list(excluded))["nodes"])
    candidates = sorted(set(repository.nodes) - excluded,
                        key=lambda node_id: object_hash([seed, event_facts, node_id]))
    evidence = Evidence()
    for node_id in candidates[:len(matched.nodes)]:
        evidence.nodes[node_id] = repository.node(node_id)
    return evidence
