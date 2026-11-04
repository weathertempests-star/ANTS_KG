"""Score selected events, never just the subset with successful predictions."""

from collections import defaultdict
import csv
import json
import math
from pathlib import Path
import sqlite3
import tempfile

from ..common.files import canonical, file_hash, jsonl, write_json
from ..data.store import readonly
from ..experiments.targets import selected_targets
from .inputs import evaluation_inputs
from .metrics import Accumulator, from_matrix, prediction_value
from .exports import export_tables


def stage_predictions(connection, path):
    connection.execute("CREATE TABLE predictions(event_id TEXT PRIMARY KEY, payload TEXT, consumed INTEGER DEFAULT 0)")
    if not path.exists():
        return
    for item in jsonl(path):
        if not isinstance(item, dict) or not isinstance(item.get("event_id"), str):
            raise ValueError("Prediction requires an event_id")
        try:
            connection.execute("INSERT INTO predictions(event_id,payload) VALUES (?,?)",
                               (item["event_id"], canonical(item)))
        except sqlite3.IntegrityError:
            raise ValueError("Duplicate prediction ID: " + item["event_id"]) from None
    connection.commit()


def sample_weight(target):
    probability = target.get("inclusion_probability")
    if (isinstance(probability, bool) or not isinstance(probability, (float, int))
            or not math.isfinite(probability) or not 0 < probability <= 1):
        raise ValueError("Each target needs an inclusion probability in (0,1]")
    return 1.0 / probability


def case_kind(truth, prediction):
    if prediction is None:
        return "unresolved"
    return {(0, 0): "TN", (0, 1): "FP", (1, 0): "FN", (1, 1): "TP"}[truth, prediction]


def accumulate(connection, answers, selection, config, output, with_coverage=False):
    overall = Accumulator()
    strata = {key: defaultdict(Accumulator) for key in ("recording_id", "cohort", "dependency_group", "split", "technique")}
    if with_coverage:
        strata.update({key: defaultdict(Accumulator) for key in ("match", "boundary_status")})
    connection.execute("CREATE TABLE evaluated(event_id TEXT PRIMARY KEY)")
    count = 0
    with (output / "scored_events.jsonl").open("w", encoding="utf-8") as stream:
        for target in selected_targets(selection, config):
            target = dict(target)
            event_id = target["event_id"]
            if with_coverage:
                coverage = connection.execute("SELECT payload FROM coverage WHERE event_id=?", (event_id,)).fetchone()
                if coverage is None:
                    raise ValueError("Coverage is missing selected target: " + event_id)
                coverage = json.loads(coverage[0])
                if any(coverage[key] != value for key, value in target.items()):
                    raise ValueError("Coverage target metadata differs")
                target.update({key: coverage[key] for key in ("match", "boundary_status")})
                connection.execute("UPDATE coverage SET consumed=1 WHERE event_id=?", (event_id,))
            try:
                connection.execute("INSERT INTO evaluated VALUES(?)", (event_id,))
            except sqlite3.IntegrityError:
                raise ValueError("Duplicate selected target: " + event_id) from None
            label = answers.execute("SELECT recording_id,label_binary,technique FROM labels WHERE event_id=?", (event_id,)).fetchone()
            if label is None or label["label_binary"] not in (0, 1) or label["recording_id"] != target["recording_id"]:
                raise ValueError("Missing, quarantined, or mismatched target annotation: " + event_id)
            target["technique"] = label["technique"] or "no_technique_annotation"
            row = connection.execute("SELECT payload FROM predictions WHERE event_id=?", (event_id,)).fetchone()
            result = json.loads(row[0]) if row else None
            if row:
                connection.execute("UPDATE predictions SET consumed=1 WHERE event_id=?", (event_id,))
            truth, weight = label["label_binary"], sample_weight(target)
            prediction = prediction_value(result)
            status = result.get("status", "invalid_output") if result else "missing_prediction"
            overall.add(truth, prediction, weight, status)
            for key, groups in strata.items():
                groups[target[key]].add(truth, prediction, weight, status)
            stream.write(canonical({**target, "truth": truth, "prediction": prediction,
                                    "status": status, "weight": weight, "case": case_kind(truth, prediction)}) + "\n")
            count += 1
    if not count:
        raise ValueError("No targets match this run")
    extra = connection.execute("SELECT COUNT(*) FROM predictions WHERE consumed=0").fetchone()[0]
    if extra:
        raise ValueError(f"Predictions contain {extra} IDs outside the selected run targets")
    if with_coverage and connection.execute("SELECT COUNT(*) FROM coverage WHERE consumed=0").fetchone()[0]:
        raise ValueError("Coverage includes targets outside this run")
    groups = {key: {name: value.result() for name, value in sorted(values.items())} for key, values in strata.items()}
    defined = [value["BA_all"] for value in groups["recording_id"].values() if value["BA_all"] is not None]
    return {"weighted": overall.result(), "unweighted": from_matrix(overall.raw), "strata": groups,
            "recording_macro_BA": {"value": sum(defined) / len(defined) if defined else None,
                                   "defined_recordings": len(defined),
                                   "total_recordings": len(groups["recording_id"]),
                                   "single_class_policy": "BA is undefined; report recall and FPR separately"}}


def write_confusion(path, metrics):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["weighting", "truth", "benign", "malicious", "unresolved"])
        for mode in ("weighted", "unweighted"):
            for truth, row in zip(("benign", "malicious"), metrics[mode]["confusion_matrix"]):
                writer.writerow([mode, truth, *row])


def evaluate_run(dataset, selection, run, output, prepared=None):
    """Produce an immutable report directory; only this layer opens answers.sqlite."""
    frozen, manifest = evaluation_inputs(dataset, selection, run)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "manifest.json", {"schema": "ants-evaluation-1", "complete": False})
    answers = readonly(Path(dataset) / "answers.sqlite")
    try:
        with tempfile.TemporaryDirectory(prefix="ants-score-") as temporary:
            connection = sqlite3.connect(Path(temporary) / "join.sqlite")
            try:
                stage_predictions(connection, Path(run) / "predictions.jsonl")
                if prepared:
                    from .coverage import stage_coverage
                    stage_coverage(connection, prepared, frozen)
                metrics = accumulate(connection, answers, selection, frozen["configuration"], output, bool(prepared))
            finally:
                connection.close()
    finally:
        answers.close()
    metrics.update({"schema": "ants-metrics-1", "engineering_only": frozen["engineering_only"],
                    "run_complete": manifest is not None, "config_hash": frozen["config_hash"],
                    "metric_definition": "BA_all = mean(correct predictions / all selected truth-class events); unresolved remain in denominators",
                    "weighting": "inverse event inclusion probability within recording"})
    metrics["coverage_preparation_manifest_sha256"] = file_hash(Path(prepared) / "manifest.json") if prepared else None
    if manifest and manifest["target_count"] != metrics["weighted"]["raw_events"]:
        raise ValueError("Run target count differs from the frozen selection")
    write_json(output / "metrics.json", metrics)
    write_confusion(output / "confusion.csv", metrics)
    write_confusion(output / "confusion_matrices.csv", metrics)
    export_tables(output, metrics)
    result = {"schema": "ants-evaluation-1", "complete": True, "config_hash": frozen["config_hash"],
              "dataset_hash": frozen["dataset_hash"], "source_manifest_sha256": frozen["source_manifest_sha256"],
              "engineering_only": frozen["engineering_only"],
              "prediction_sha256": file_hash(Path(run) / "predictions.jsonl") if (Path(run) / "predictions.jsonl").exists() else None,
              "files": {name: file_hash(output / name) for name in ("metrics.json", "scored_events.jsonl", "confusion.csv",
                        "confusion_matrices.csv", "per_recording.csv", "error_cases.jsonl")}}
    write_json(output / "manifest.json", result, replace=True)
    return result
