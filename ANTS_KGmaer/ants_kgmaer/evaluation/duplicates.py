"""Observed-sample duplicate sensitivity, without pooling recordings or processes."""

import json
from pathlib import Path
import sqlite3
import tempfile

from ..common.files import canonical, file_hash, jsonl, object_hash, read_json, write_json
from ..data.store import readonly
from .comparison import verified_evaluation
from ..common.artifacts import verify_files
from .metrics import Accumulator


def equivalence_key(event, mode):
    if mode == "exact":
        signature = event["exact_signature"]
    elif mode == "normalized":
        # Normalization signature excludes Value data and order: restore both to
        # avoid collapsing different values or noncontemporaneous observations.
        facts = json.loads(event["facts"])
        signature = [event["normalized_signature"], event["order_ref"], facts.get("optional_value_data")]
    else:
        raise ValueError("Unknown duplicate sensitivity mode")
    return object_hash([event["recording_id"], event["actor_id"], signature])


def grouped_metrics(connection, mode):
    connection.execute("DROP TABLE IF EXISTS groups")
    connection.execute("CREATE TABLE groups AS SELECT group_id,COUNT(*) n,SUM(weight) mass,MIN(truth) lo,MAX(truth) hi "
                       "FROM members WHERE mode=? GROUP BY group_id", (mode,))
    connection.execute("CREATE UNIQUE INDEX group_identity ON groups(group_id)")
    score = Accumulator()
    for truth, prediction, weight, status, mass, lo, hi in connection.execute(
        "SELECT m.truth,m.prediction,m.weight,m.status,g.mass,g.lo,g.hi FROM members m "
        "JOIN groups g ON m.group_id=g.group_id WHERE m.mode=?", (mode,)
    ):
        # Conflicting annotations cannot be merged; retain each event separately.
        score.add(truth, prediction, 1.0 if lo != hi else weight / mass, status)
    groups, repeated, conflicts, conflict_events = connection.execute(
        "SELECT COUNT(*),SUM(n>1),SUM(lo!=hi),SUM(CASE WHEN lo!=hi THEN n ELSE 0 END) FROM groups"
    ).fetchone()
    return {"metrics": score.result(), "observed_groups": groups, "repeated_groups": repeated or 0,
            "conflicting_groups": conflicts or 0, "conflicting_events_kept_individual": conflict_events or 0}


def duplicate_sensitivity(dataset, evaluation, output):
    dataset, evaluation = Path(dataset), Path(evaluation)
    evaluation_manifest = verified_evaluation(evaluation)
    data = read_json(dataset / "source_manifest.json")
    if not data.get("complete") or data["dataset_hash"] != evaluation_manifest.get("dataset_hash"):
        raise ValueError("Evaluation does not identify this dataset; regenerate evaluation with current tooling")
    if file_hash(dataset / "source_manifest.json") != evaluation_manifest.get("source_manifest_sha256"):
        raise ValueError("Evaluation source manifest mismatch")
    verify_files(dataset, data["files"])
    events = readonly(dataset / "events.sqlite")
    try:
        with tempfile.TemporaryDirectory(prefix="ants-duplicates-") as temporary:
            connection = sqlite3.connect(Path(temporary) / "groups.sqlite")
            try:
                connection.execute("CREATE TABLE members(mode TEXT,event_id TEXT,group_id TEXT,truth INTEGER,"
                                   "prediction INTEGER,weight REAL,status TEXT,PRIMARY KEY(mode,event_id))")
                for row in jsonl(evaluation / "scored_events.jsonl"):
                    event = events.execute("SELECT * FROM events WHERE event_id=?", (row["event_id"],)).fetchone()
                    if event is None or event["recording_id"] != row["recording_id"]:
                        raise ValueError("Scored event provenance mismatch")
                    for mode in ("exact", "normalized"):
                        connection.execute("INSERT INTO members VALUES(?,?,?,?,?,?,?)", (
                            mode, row["event_id"], equivalence_key(event, mode), row["truth"],
                            row["prediction"], row["weight"], row["status"]))
                connection.commit()
                metrics = {mode: grouped_metrics(connection, mode) for mode in ("exact", "normalized")}
            finally:
                connection.close()
    finally:
        events.close()
    result = {"schema": "ants-duplicate-sensitivity-1", "engineering_only": evaluation_manifest["engineering_only"],
              "evaluation_manifest_sha256": file_hash(evaluation / "manifest.json"), "results": metrics,
              "scope": "Observed evaluated targets only; not an unbiased estimate of all population equivalence groups",
              "grouping": "Within recording and process; normalized groups also require same order and optional Value data",
              "weighting": "Each nonconflicting observed group has mass one; inverse selection weights distribute its mass. Conflicting groups retain each event with mass one.",
              "limitations": "Unsampled members can contain additional annotation conflicts. Main event-weighted results are unchanged. No contexts are compressed."}
    write_json(output, result)
    return result
