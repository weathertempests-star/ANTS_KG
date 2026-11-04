"""Offline, escaped HTML with bounded case excerpts and no external resources."""

from collections import Counter
from html import escape
import json
from pathlib import Path

from ..common.files import file_hash, jsonl, read_json, write_json
from ..evaluation.comparison import verified_evaluation
from ..common.artifacts import verify_files


def display(value):
    return "N/A" if value is None else f"{value:.4f}"


def details(title, value):
    return "<details><summary>" + escape(title) + "</summary><pre>" + escape(
        json.dumps(value, ensure_ascii=False, indent=2)
    ) + "</pre></details>"


def metric_table(metrics):
    keys = ("BA_all", "macro_F1", "malicious_recall", "FPR", "coverage")
    header = "<tr><th>Recording</th>" + "".join("<th>" + key + "</th>" for key in keys) + "</tr>"
    rows = []
    for name, values in [("ALL (weighted)", metrics["weighted"]), *metrics["strata"]["recording_id"].items()]:
        rows.append("<tr><td>" + escape(name) + "</td>" + "".join("<td>" + display(values[k]) + "</td>" for k in keys) + "</tr>")
    return "<table>" + header + "".join(rows) + "</table>"


def render_report(evaluation, run, output, cases_per_type=5):
    if type(cases_per_type) is not int or not 1 <= cases_per_type <= 100:
        raise ValueError("cases_per_type must be in [1,100]")
    evaluation, run, output = map(Path, (evaluation, run, output))
    manifest = verified_evaluation(evaluation)
    config = read_json(run / "config.json")
    if config["config_hash"] != manifest["config_hash"]:
        raise ValueError("Report run and evaluation do not match")
    prediction_path = run / "predictions.jsonl"
    prediction_hash = file_hash(prediction_path) if prediction_path.exists() else None
    if prediction_hash != manifest["prediction_sha256"]:
        raise ValueError("Predictions changed after evaluation")
    if (run / "manifest.json").exists():
        verify_files(run, read_json(run / "manifest.json")["files"])
    metrics = read_json(evaluation / "metrics.json")
    chosen, counts, selected_counts = {}, Counter(), Counter()
    for row in jsonl(evaluation / "scored_events.jsonl"):
        kind = row["case"]
        counts[kind] += 1
        if selected_counts[kind] < cases_per_type:
            chosen[row["event_id"]] = {"score": row}
            selected_counts[kind] += 1
    for name, key in (("predictions.jsonl", "model_result"), ("evidence_packets.jsonl", "delivered_evidence")):
        if (run / name).exists():
            for row in jsonl(run / name):
                if row["event_id"] in chosen:
                    chosen[row["event_id"]][key] = row
    sections = []
    for kind in ("TP", "TN", "FP", "FN", "unresolved"):
        sections.append(f"<h2>{kind}: {counts[kind]} events</h2>")
        if not counts[kind]:
            sections.append("<p>No observed cases in this run; no cases have been fabricated.</p>")
        for row in chosen.values():
            if row["score"]["case"] == kind:
                score = row["score"]
                sections.append("<article><h3>" + escape(score["event_id"]) + "</h3>" +
                                details("Score and sampling metadata — evaluator only", score) +
                                details("Delivered model evidence", row.get("delivered_evidence")) +
                                details("Model output and recorded cost", row.get("model_result")) + "</article>")
    designation = "ENGINEERING / MOCK — not detection performance" if metrics["engineering_only"] else "Research evaluation"
    document = """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">
<title>ANTS KGmaer experiment report</title>
<style>body{font-family:system-ui;margin:2rem;max-width:1100px}table{border-collapse:collapse}
td,th{padding:.5rem;border:1px solid #aaa;text-align:left}pre{white-space:pre-wrap;overflow-wrap:anywhere}
article{border:1px solid #aaa;padding:1rem;margin:1rem 0}h3{overflow-wrap:anywhere}summary{cursor:pointer}</style>
<h1>ANTS KGmaer experiment report</h1>""" + "<p><strong>" + escape(designation) + "</strong></p>"
    document += "<p>Missing, invalid and abstained predictions remain in the denominators. Single-class BA is N/A. "
    document += "Case excerpts are the first events of each outcome in frozen selection order, not a random audit sample. "
    document += "Valid citation IDs do not establish that claims are supported; human review is separate.</p>"
    document += metric_table(metrics) + details("Frozen configuration", config) + "".join(sections) + "</html>"
    output.mkdir(parents=True, exist_ok=False)
    (output / "report.html").write_text(document, encoding="utf-8")
    from .discussion import write_discussion
    write_discussion(output, metrics, config, counts)
    result = {"schema": "ants-report-1", "complete": True, "engineering_only": metrics["engineering_only"],
              "evaluation_manifest_sha256": file_hash(evaluation / "manifest.json"),
              "files": {name: file_hash(output / name) for name in ("report.html", "EXPERIMENT_REPORT.md", "per_recording_ba.svg")}}
    write_json(output / "manifest.json", result)
    return result
