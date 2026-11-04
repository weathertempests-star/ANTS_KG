"""Aggregate recorded costs and policy outcomes without inspecting ground truth."""

from collections import Counter
import json


def percentile(values, fraction):
    if not values:
        return None
    values = sorted(values)
    index = (len(values) - 1) * fraction
    lower = int(index)
    upper = min(lower + 1, len(values) - 1)
    return values[lower] + (values[upper] - values[lower]) * (index - lower)


def summarize(journal):
    usage, statuses, tools, replay_usage = Counter(), Counter(), Counter(), Counter()
    latencies = []
    synthetic = False
    for _, result in journal.results():
        usage.update(result["usage"])
        statuses[result["status"]] += 1
        tools["requests"] += result["tool_requests"]
        synthetic |= result.get("synthetic", False)
        if result.get("replay"):
            replay_usage.update(result["replay"]["acquisition_usage"])
    for kind, payload in journal.connection.execute("SELECT kind,payload FROM traces ORDER BY ordinal"):
        item = json.loads(payload)
        if kind == "model_reply":
            if item.get("latency_seconds") is not None:
                latencies.append(item["latency_seconds"])
        elif kind in {"tool_reply", "tool_error"}:
            tools["successful" if kind == "tool_reply" else "rejected"] += 1
            tools["duplicate_requests"] += int(item.get("duplicate", False))
        elif kind == "invalid_action":
            tools["invalid_action_requests"] += item.get("requested_tool_count", 0)
    count = sum(statuses.values())
    def rate(numerator, denominator):
        return numerator / denominator if denominator else None
    return {"schema": "ants-usage-1", "synthetic": synthetic, "completed_targets": count,
            "status_counts": dict(statuses), "usage": dict(usage), "tools": dict(tools),
            "tool_success_rate": rate(tools["successful"], tools["requests"]),
            "tool_rejection_rate": rate(tools["rejected"] + tools["invalid_action_requests"], tools["requests"]),
            "duplicate_request_rate": rate(tools["duplicate_requests"], tools["requests"]),
            "final_validated_output_rate": rate(statuses["valid"] + statuses["abstained"], count),
            "abstention_rate": rate(statuses["abstained"], count),
            "budget_exhaustion_rate": rate(statuses["budget_exhausted"], count),
            "known_reply_latency_seconds": {"count": len(latencies), "p50": percentile(latencies, .5),
                                            "p95": percentile(latencies, .95), "sum": sum(latencies)},
            "replay_acquisition_usage": dict(replay_usage),
            "limitations": "Latencies cover returned model calls only, excluding interrupted/failed calls and client overhead. Mock latencies and tokens are synthetic. Unknown usage is a reserved upper bound, not measured usage. Final validation does not establish human evidence support."}
