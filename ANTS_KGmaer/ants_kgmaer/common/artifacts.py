"""Integrity validation of published artifact bundles, including required coverage."""

from pathlib import Path

from .files import file_hash, object_hash, read_json


REQUIRED = {
    "ants-dataset-1": {"events.sqlite", "answers.sqlite", "relation_contract.json", "label_map.json",
                       "annotation_audit.json", "normalization_audit.json", "redaction_audit.json", "ingest_progress.json"},
    "ants-targets-1": {"targets.jsonl", "split_manifest.json", "overlap_audit.json"},
    "ants-run-1": {"config.json", "preflight.json", "kg_cache.sqlite", "journal.sqlite", "predictions.jsonl",
                   "evidence_packets.jsonl", "prompts.jsonl", "tool_calls.jsonl", "usage.jsonl", "usage.json", "schemas.json"},
    "ants-preparation-1": {"config.json", "contexts.jsonl", "coverage_events.jsonl", "kg_context_cache.jsonl",
                           "kg_cache.sqlite", "coverage_report.csv"},
    "ants-evaluation-1": {"metrics.json", "scored_events.jsonl", "confusion.csv", "confusion_matrices.csv",
                          "per_recording.csv", "error_cases.jsonl"},
    "ants-population-coverage-1": {"config.json", "coverage.sqlite", "kg_cache.sqlite", "coverage_report.csv", "summary.json"},
    "ants-report-1": {"report.html", "EXPERIMENT_REPORT.md", "per_recording_ba.svg"},
    "ants-portable-data-1": {"events.jsonl", "annotation_audit.csv"},
    "ants-review-1": {"blind/packets.jsonl", "blind/reviews.csv", "blind/README.md", "internal/assignments.jsonl"},
}


def verify_files(directory, files):
    root = Path(directory).resolve()
    for name, expected in files.items():
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file() or file_hash(path) != expected:
            raise ValueError("Missing or changed artifact: " + name)


def verify_directory(directory):
    root = Path(directory).resolve()
    manifest_path = root / ("source_manifest.json" if (root / "source_manifest.json").exists() else "manifest.json")
    manifest = read_json(manifest_path)
    schema = manifest.get("schema")
    if schema not in REQUIRED or not manifest.get("complete"):
        raise ValueError("Unsupported or incomplete artifact bundle")
    files = manifest.get("files", {})
    missing = REQUIRED[schema] - files.keys()
    if missing:
        raise ValueError("Manifest does not checksum required artifacts (legacy bundle may need regeneration): " + ", ".join(sorted(missing)))
    verify_files(root, files)
    if schema in {"ants-run-1", "ants-preparation-1"}:
        frozen = read_json(root / "config.json")
        if object_hash({k: v for k, v in frozen.items() if k != "config_hash"}) != frozen["config_hash"] or frozen["config_hash"] != manifest["config_hash"]:
            raise ValueError("Frozen configuration identity mismatch")
    return {"verified": True, "schema": schema, "manifest_sha256": file_hash(manifest_path),
            "verified_files": len(files), "scope": "Required artifact hashes and frozen configuration identity; not a claim of model quality"}
