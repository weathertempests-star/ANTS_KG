"""Portable streaming event export; answers remain in the separate source database."""

import csv
from pathlib import Path

from ..common.files import canonical, file_hash, read_json, write_json
from ..common.artifacts import verify_files
from .store import EventStore


def export_dataset(dataset, output):
    dataset, output = Path(dataset), Path(output)
    manifest = read_json(dataset / "source_manifest.json")
    if not manifest.get("complete"):
        raise ValueError("Complete dataset required")
    verify_files(dataset, manifest["files"])
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "manifest.json", {"schema": "ants-portable-data-1", "complete": False})
    store = EventStore(dataset / "events.sqlite")
    count = 0
    try:
        with (output / "events.jsonl").open("w", encoding="utf-8") as stream:
            for row in store.connection.execute("SELECT * FROM events ORDER BY recording_id,row_index"):
                stream.write(canonical(store.unpack(row)) + "\n")
                count += 1
    finally:
        store.close()
    with (output / "annotation_audit.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["recording_id", "registry_label", "events", "quarantined_labels_all_domains"])
        for row in manifest["recordings"]:
            for label, number in sorted(row["registry_labels"].items()):
                writer.writerow([row["recording_id"], label, number, row["quarantined_labels"]])
    result = {"schema": "ants-portable-data-1", "complete": True, "events": count,
              "source_manifest_sha256": file_hash(dataset / "source_manifest.json"),
              "dataset_hash": manifest["dataset_hash"],
              "warning": "Internal event/provenance export is not a model prompt. Use the context whitelist; annotation audit is evaluator-only.",
              "files": {name: file_hash(output / name) for name in ("events.jsonl", "annotation_audit.csv")}}
    write_json(output / "manifest.json", result, replace=True)
    return result
