"""Evidence union and representation controls; retain complete claims with their limits."""

import copy

from ..common.files import canonical, object_hash


class Evidence:
    def __init__(self):
        self.nodes = {}
        self.relations = {}
        self.lookups = []

    def add(self, result, event_id=None):
        for node in result.get("nodes", []):
            self.nodes[node["id"]] = copy.deepcopy(node)
        for edge in result.get("relations", []):
            self.relations[object_hash(edge)] = copy.deepcopy(edge)
        if event_id:
            self.lookups.append({"event_id": event_id, **{k: copy.deepcopy(v) for k, v in result.items() if k not in {"nodes", "relations"}}})

    def packet(self, mode="graph"):
        nodes = sorted(self.nodes.values(), key=lambda n: (-n["depth"], n["id"]))
        edges = [v for _, v in sorted(self.relations.items())]
        packet = {"lookups": copy.deepcopy(self.lookups), "nodes": copy.deepcopy(nodes),
                  "relations": copy.deepcopy(edges), "omitted_node_ids": []}
        if mode == "text":
            packet["nodes"] = [{k: n[k] for k in ("id", "explanation", "explanation_sources")} for n in nodes]
            packet["relations"] = []
        elif mode == "flat":
            # Preserve every factual field; change representation, not evidence content.
            packet["nodes"] = [{"id": n["id"], "facts_text": canonical(n)} for n in nodes]
            packet["relations"] = [{"facts_text": canonical(e)} for e in edges]
        elif mode != "graph":
            raise ValueError("Unknown knowledge representation")
        return packet


def prune_one(packet):
    """Remove one entire node and incident edges, explicitly recording the omission."""
    if not packet["nodes"]:
        return False
    removed = packet["nodes"].pop()
    node_id = removed["id"]
    packet["omitted_node_ids"].append(node_id)
    packet["relations"] = [edge for edge in packet["relations"] if
                           node_id not in (edge.get("source"), edge.get("target")) and
                           node_id not in edge.get("facts_text", "")]
    return True
