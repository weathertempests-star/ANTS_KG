"""Evaluator-side target sampling; inclusion probabilities never enter model views."""

from collections import Counter
from pathlib import Path
import random

from ..common.files import append_jsonl, file_hash, object_hash, read_json, write_json
from .overlap import audit_overlap
from .store import readonly


def validate_splits(sources, groups, assignment):
    expected = {s["id"] for s in sources}
    if set(assignment) != expected or any(v not in {"development", "validation", "test", "evaluation"} for v in assignment.values()):
        raise ValueError("Split assignment must cover every recording exactly once")
    for group in groups:
        if len({assignment[r] for r in group}) != 1:
            raise ValueError("Dependent recordings must not cross splits: " + ", ".join(group))


def select_targets(dataset_dir, output, negatives=2000, seed=20261026, split_path=None):
    if negatives is not None and (type(negatives) is not int or negatives < 1):
        raise ValueError("Negative cap must be positive, or None for the full population")
    dataset_dir, output = Path(dataset_dir), Path(output)
    manifest = read_json(dataset_dir / "source_manifest.json")
    if not manifest["complete"]:
        raise ValueError("Dataset ingestion is incomplete")
    output.mkdir(parents=True, exist_ok=False)
    overlaps = audit_overlap(dataset_dir / "events.sqlite", manifest["sources"])
    write_json(output / "overlap_audit.json", overlaps)
    assignment = read_json(split_path) if split_path else {s["id"]: "evaluation" for s in manifest["sources"]}
    validate_splits(manifest["sources"], overlaps["dependency_groups"], assignment)
    groups = {r: "group_" + str(i) for i, group in enumerate(overlaps["dependency_groups"]) for r in group}
    write_json(output / "split_manifest.json", {
        "schema": "ants-splits-1", "assignment": assignment, "dependency_groups": overlaps["dependency_groups"],
        "protocol": "explicit_group_assignment" if split_path else "fixed_model_retrospective_evaluation_not_blind_test",
    })
    connection = readonly(dataset_dir / "events.sqlite")
    connection.execute("ATTACH DATABASE ? AS answers", ((dataset_dir / "answers.sqlite").resolve().as_uri() + "?mode=ro",))
    reports = []
    targets_path = output / "targets.jsonl"
    targets_path.touch(exist_ok=False)
    try:
        for source in manifest["sources"]:
            randomizer = random.Random(int(object_hash([seed, source["id"]]), 16))
            positive, negative, counts = [], [], Counter()
            query = ("SELECT e.event_id,e.row_index,l.label_binary FROM events e JOIN answers.labels l USING(event_id) "
                     "WHERE e.target_type='Registry' AND e.recording_id=? ORDER BY e.row_index")
            for event_id, row_index, label in connection.execute(query, (source["id"],)):
                counts[str(label)] += 1
                if label == 1:
                    positive.append((event_id, row_index))
                elif label == 0:
                    if negatives is None or len(negative) < negatives:
                        negative.append((event_id, row_index))
                    else:
                        position = randomizer.randrange(counts["0"])
                        if position < negatives:
                            negative[position] = (event_id, row_index)
            probability = len(negative) / counts["0"] if counts["0"] else None
            selected = [(eid, row, 1.0) for eid, row in positive] + [(eid, row, probability) for eid, row in negative]
            for event_id, _, inclusion in sorted(selected, key=lambda item: item[1]):
                append_jsonl(targets_path, {"event_id": event_id, "recording_id": source["id"],
                    "cohort": source["cohort"], "dependency_group": groups[source["id"]],
                    "split": assignment[source["id"]], "inclusion_probability": inclusion})
            reports.append({"recording_id": source["id"], "population": dict(counts),
                            "selected_positive": len(positive), "selected_negative": len(negative),
                            "negative_inclusion_probability": probability})
    finally:
        connection.close()
    result = {"schema": "ants-targets-1", "complete": True, "dataset_hash": manifest["dataset_hash"],
              "seed": seed, "negative_cap": negatives, "sampling": "all_positive_uniform_negative_per_recording",
              "targets_sha256": file_hash(targets_path), "recordings": reports,
              "split_sha256": file_hash(output / "split_manifest.json"),
              "files": {name: file_hash(output / name) for name in ("targets.jsonl", "split_manifest.json", "overlap_audit.json")}}
    write_json(output / "manifest.json", result)
    return result
