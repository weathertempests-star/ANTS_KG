"""Join identical event sets before computing dependency-block paired intervals."""

from collections import defaultdict
import csv
import json
from pathlib import Path
import sqlite3
import tempfile

from ..common.files import canonical, file_hash, jsonl, read_json, write_json
from ..common.artifacts import verify_files
from .metrics import Accumulator
from .paired import paired_bootstrap


def verified_evaluation(path):
    path = Path(path)
    manifest = read_json(path / "manifest.json")
    if manifest.get("schema") != "ants-evaluation-1" or not manifest.get("complete"):
        raise ValueError("A complete evaluation is required")
    for name in ("metrics.json", "scored_events.jsonl"):
        if name not in manifest["files"]:
            raise ValueError("Evaluation manifest does not cover " + name)
    verify_files(path, manifest["files"])
    return manifest


def paired_rows(connection, left, right):
    connection.execute("CREATE TABLE events(event_id TEXT PRIMARY KEY, payload TEXT, paired INTEGER DEFAULT 0)")
    for row in jsonl(Path(left) / "scored_events.jsonl"):
        try:
            connection.execute("INSERT INTO events(event_id,payload) VALUES(?,?)", (row["event_id"], canonical(row)))
        except sqlite3.IntegrityError:
            raise ValueError("Duplicate left event") from None
    for row in jsonl(Path(right) / "scored_events.jsonl"):
        match = connection.execute("SELECT payload,paired FROM events WHERE event_id=?", (row["event_id"],)).fetchone()
        if match is None or match[1]:
            raise ValueError("Target sets differ or right event is duplicated")
        previous = json.loads(match[0])
        for key in ("truth", "recording_id", "cohort", "dependency_group", "split", "inclusion_probability", "weight"):
            if previous[key] != row[key]:
                raise ValueError("Paired target metadata differs: " + key)
        connection.execute("UPDATE events SET paired=1 WHERE event_id=?", (row["event_id"],))
        yield previous, row
    if connection.execute("SELECT COUNT(*) FROM events WHERE paired=0").fetchone()[0]:
        raise ValueError("Right evaluation is missing targets")


def compare_evaluations(left, right, output, repetitions=2000, seed=20261026):
    output = Path(output)
    csv_path = output.with_suffix(".csv")
    if output == csv_path or output.exists() or csv_path.exists():
        raise FileExistsError("Comparison JSON and companion CSV paths must be distinct and new")
    manifests = [verified_evaluation(path) for path in (left, right)]
    groups = defaultdict(lambda: [Accumulator(), Accumulator()])
    recordings = defaultdict(lambda: [Accumulator(), Accumulator()])
    count = 0
    with tempfile.TemporaryDirectory(prefix="ants-paired-") as temporary:
        connection = sqlite3.connect(Path(temporary) / "join.sqlite")
        try:
            for previous, row in paired_rows(connection, left, right):
                for accumulator, item in zip(groups[row["dependency_group"]], (previous, row)):
                    accumulator.add(item["truth"], item["prediction"], item["weight"], item["status"])
                for accumulator, item in zip(recordings[row["recording_id"]], (previous, row)):
                    accumulator.add(item["truth"], item["prediction"], item["weight"], item["status"])
                count += 1
        finally:
            connection.close()
    result = {"schema": "ants-comparison-1", "engineering_only": any(m["engineering_only"] for m in manifests),
              "paired_events": count, "left_config_hash": manifests[0]["config_hash"],
              "right_config_hash": manifests[1]["config_hash"],
              "evaluation_manifest_sha256": [file_hash(Path(p) / "manifest.json") for p in (left, right)],
              "bootstrap": paired_bootstrap({key: [a.matrix for a in pair] for key, pair in groups.items()}, repetitions, seed)}
    output.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["recording_id", "events", "left_BA_all", "right_BA_all", "delta_right_minus_left"])
        for name, pair in sorted(recordings.items()):
            a, b = (item.result() for item in pair)
            av, bv = a["BA_all"], b["BA_all"]
            writer.writerow([name, a["raw_events"], av, bv, bv - av if av is not None and bv is not None else None])
    result["paired_deltas_csv"] = {"file": csv_path.name, "sha256": file_hash(csv_path)}
    write_json(output, result)
    return result
