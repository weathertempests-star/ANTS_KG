"""Join annotations only after population retrieval is complete."""

from collections import Counter
import csv
from pathlib import Path

from ..data.store import readonly


def summarize_population(dataset, index, output):
    connection = readonly(index)
    connection.execute("ATTACH DATABASE ? AS answers", ((Path(dataset) / "answers.sqlite").resolve().as_uri() + "?mode=ro",))
    counts, matches, by_truth = Counter(), Counter(), {}
    try:
        missing = connection.execute("SELECT COUNT(*) FROM events e LEFT JOIN answers.labels l USING(event_id) "
                                     "WHERE l.event_id IS NULL OR e.recording_id!=l.recording_id").fetchone()[0]
        if missing:
            raise ValueError("Population annotations missing or mismatched")
        query = """SELECT e.recording_id,l.label_binary,q.match,q.boundary_status,COUNT(*) n,
            SUM(q.path_complete) path_complete,SUM(q.explanations_complete) explanations_complete,
            SUM(q.matched_nodes=0) no_nodes,SUM(q.deepest_level<=1) at_most_hive
            FROM events e JOIN queries q USING(query_id) JOIN answers.labels l USING(event_id)
            GROUP BY e.recording_id,l.label_binary,q.match,q.boundary_status
            ORDER BY e.recording_id,l.label_binary,q.match,q.boundary_status"""
        with Path(output).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(["recording_id", "truth", "match", "boundary_status", "events", "path_complete_events",
                             "explanations_complete_events", "no_nodes_events", "at_most_hive_events"])
            for row in connection.execute(query):
                truth = "quarantined" if row["label_binary"] is None else str(row["label_binary"])
                writer.writerow([row["recording_id"], truth, *(row[key] for key in
                    ("match", "boundary_status", "n", "path_complete", "explanations_complete", "no_nodes", "at_most_hive"))])
                counts[truth] += row["n"]
                matches[row["match"]] += row["n"]
                by_truth.setdefault(truth, Counter())[row["match"]] += row["n"]
    finally:
        connection.close()
    return {"schema": "ants-population-summary-1", "registry_events": sum(counts.values()),
            "truth_counts": dict(counts), "match_counts": dict(matches),
            "match_by_truth": {key: dict(value) for key, value in by_truth.items()},
            "scope": "All Registry events, including quarantined annotations; no sampling and no model inference"}
