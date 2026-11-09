"""Human/instance supervision contract. Attack labels are never membership labels.

One record describes reviewed membership in a candidate graph. Unreviewed
events remain unknown; annotators may list required events outside the candidate
to expose the candidate generator's recall ceiling.
"""
import math

ROLES = frozenset({"core", "context", "unrelated", "unknown"})
PROVENANCE = frozenset({"human", "generator_instance", "weak_rule"})


def template(graph):
    return {
        "schema": "kgraphier-membership-1",
        "graph_id": graph["id"],
        "recording_sha256": graph["recording_sha256"],
        "anchor_event_id": graph["anchor_event_id"],
        "episode_id": None,
        "provenance": "human",
        "reviewer": None,
        "complete": False,
        "memberships": [],
        "required_outside_candidate": [],
    }


def validate(annotation, graph):
    if annotation.get("schema") != "kgraphier-membership-1":
        raise ValueError("unsupported annotation schema")
    for key, graph_key in (("graph_id", "id"), ("recording_sha256", "recording_sha256"),
                           ("anchor_event_id", "anchor_event_id")):
        if annotation.get(key) != graph[graph_key]:
            raise ValueError("annotation binding mismatch: " + key)
    if annotation.get("provenance") not in PROVENANCE:
        raise ValueError("unknown supervision provenance")
    if not isinstance(annotation.get("complete"), bool):
        raise ValueError("complete must be boolean")
    known = {e["event_id"] for e in graph["events"]}
    seen = set()
    for member in annotation["memberships"]:
        eid, role = member["event_id"], member["role"]
        if eid not in known or eid in seen:
            raise ValueError("unknown or duplicate membership event")
        seen.add(eid)
        if role not in ROLES:
            raise ValueError("unknown membership role")
        weight = member.get("confidence", 1.0)
        if isinstance(weight, bool) or not isinstance(weight, (int, float)) or not math.isfinite(weight) or not 0 < weight <= 1:
            raise ValueError("confidence must be finite and in (0,1]")
        if eid == graph["anchor_event_id"] and role == "unrelated":
            raise ValueError("anchor cannot be unrelated")
    if annotation["complete"] and (seen != known or any(m["role"] == "unknown" for m in annotation["memberships"])):
        raise ValueError("complete review must explicitly classify every candidate")
    outside = annotation["required_outside_candidate"]
    prefix = graph["recording_sha256"] + ":"
    if len(set(outside)) != len(outside) or any(
        not isinstance(e, str) or not e.startswith(prefix) or
        not e[len(prefix):].isdigit() or e in known for e in outside
    ):
        raise ValueError("invalid outside-candidate event reference")
    if seen and (not annotation.get("episode_id") or not annotation.get("reviewer")):
        raise ValueError("supervision requires episode and reviewer/source identifiers")
    return annotation


def targets(annotation, graph):
    """Return targets and weights; unknowns have zero weight, never negative."""
    validate(annotation, graph)
    by_id = {m["event_id"]: m for m in annotation["memberships"]}
    labels, weights = [], []
    for event in graph["events"]:
        item = by_id.get(event["event_id"], {"role": "unknown"})
        role = item["role"]
        labels.append(float(role in {"core", "context"}))
        weights.append(0.0 if role == "unknown" else float(item.get("confidence", 1.0)))
    return labels, weights


def validate_splits(graphs):
    """Prevent recording and declared dependency group leakage before training."""
    groups, recordings = {}, {}
    for graph in graphs:
        split = graph["split"]
        if split not in {"train", "validation", "test"}:
            raise ValueError("unknown split")
        for table, key in ((groups, graph["dependency_group"]),
                           (recordings, graph["recording_sha256"])):
            if key in table and table[key] != split:
                raise ValueError("recording or dependency group spans splits")
            table[key] = split
    return groups
