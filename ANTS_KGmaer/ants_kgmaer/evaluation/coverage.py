"""Independent coverage summaries and identity-checked evaluation joins."""

from collections import defaultdict
import csv
from pathlib import Path
import sqlite3

from ..common.files import canonical, jsonl, read_json
from ..data.store import readonly
from ..common.artifacts import verify_files


def write_coverage_report(dataset, records, output):
    from .scoring import sample_weight
    groups = defaultdict(lambda: [0, 0.0, 0, 0])
    answers = readonly(Path(dataset) / "answers.sqlite")
    try:
        for row in jsonl(records):
            label = answers.execute("SELECT label_binary,recording_id FROM labels WHERE event_id=?", (row["event_id"],)).fetchone()
            if label is None or label[0] not in (0, 1) or label[1] != row["recording_id"]:
                raise ValueError("Coverage requires approved matching annotations")
            key = (row["recording_id"], label[0], row["match"], row["boundary_status"])
            values = groups[key]
            values[0] += 1
            values[1] += sample_weight(row)
            values[2] += int(row["path_complete"])
            values[3] += int(row["explanations_complete"])
    finally:
        answers.close()
    with Path(output).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["recording_id", "truth", "match", "boundary_status", "raw_events", "weighted_events",
                         "path_complete_events", "explanations_complete_events"])
        for key, values in sorted(groups.items()):
            writer.writerow([*key, *values])


def stage_coverage(connection, directory, frozen):
    directory = Path(directory)
    manifest = read_json(directory / "manifest.json")
    config = read_json(directory / "config.json")
    if manifest.get("schema") != "ants-preparation-1" or not manifest.get("complete"):
        raise ValueError("Complete preparation is required")
    for name in ("config.json", "coverage_events.jsonl"):
        if name not in manifest["files"]:
            raise ValueError("Preparation manifest missing " + name)
    verify_files(directory, manifest["files"])
    for key in ("dataset_hash", "targets_sha256", "split_sha256", "snapshot_sha256"):
        if config[key] != frozen[key]:
            raise ValueError("Preparation identity differs: " + key)
    for key, default in (("template_candidates", False), ("split", None), ("engineering_limit", None)):
        if config["configuration"].get(key, default) != frozen["configuration"].get(key, default):
            raise ValueError("Preparation configuration differs: " + key)
    connection.execute("CREATE TABLE coverage(event_id TEXT PRIMARY KEY, payload TEXT, consumed INTEGER DEFAULT 0)")
    for row in jsonl(directory / "coverage_events.jsonl"):
        try:
            connection.execute("INSERT INTO coverage(event_id,payload) VALUES (?,?)", (row["event_id"], canonical(row)))
        except sqlite3.IntegrityError:
            raise ValueError("Duplicate coverage target") from None
