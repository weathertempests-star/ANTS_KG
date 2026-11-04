"""Tabular research artifacts derived from scored events, not separate calculations."""

import csv

from ..common.files import canonical, jsonl


def export_tables(output, metrics):
    keys = ("BA_all", "macro_F1", "malicious_recall", "malicious_precision", "FPR", "coverage")
    with (output / "per_recording.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["recording_id", "raw_events", "benign_support", "malicious_support", *keys])
        for name, values in metrics["strata"]["recording_id"].items():
            writer.writerow([name, values["raw_events"], values["support"]["benign"], values["support"]["malicious"],
                             *(values[key] for key in keys)])
    with (output / "error_cases.jsonl").open("w", encoding="utf-8") as stream:
        for row in jsonl(output / "scored_events.jsonl"):
            if row["case"] in {"FP", "FN", "unresolved"}:
                stream.write(canonical(row) + "\n")
