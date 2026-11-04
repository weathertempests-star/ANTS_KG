"""Validate frozen input identities without requiring today's executable revision."""

from pathlib import Path

from ..common.files import file_hash, object_hash, read_json
from ..common.artifacts import verify_files


def evaluation_inputs(dataset, selection, run):
    dataset, selection, run = map(Path, (dataset, selection, run))
    data = read_json(dataset / "source_manifest.json")
    targets = read_json(selection / "manifest.json")
    frozen = read_json(run / "config.json")
    if not data["complete"] or not targets["complete"]:
        raise ValueError("Dataset and selection must be complete")
    if targets["dataset_hash"] != data["dataset_hash"] or frozen["dataset_hash"] != data["dataset_hash"]:
        raise ValueError("Dataset identity mismatch")
    if object_hash({k: v for k, v in frozen.items() if k != "config_hash"}) != frozen["config_hash"]:
        raise ValueError("Frozen configuration hash mismatch")
    if file_hash(dataset / "source_manifest.json") != frozen["source_manifest_sha256"]:
        raise ValueError("Source manifest changed")
    verify_files(dataset, data["files"])
    for name, key in (("targets.jsonl", "targets_sha256"), ("split_manifest.json", "split_sha256")):
        if targets[key] != frozen[key]:
            raise ValueError("Selection identity mismatch")
        verify_files(selection, {name: targets[key]})
    manifest_path = run / "manifest.json"
    if manifest_path.exists():
        manifest = read_json(manifest_path)
        if not manifest.get("complete") or manifest["config_hash"] != frozen["config_hash"]:
            raise ValueError("Invalid run manifest")
        verify_files(run, manifest["files"])
        if "predictions.jsonl" not in manifest["files"]:
            raise ValueError("Run manifest does not cover predictions")
    else:
        # Interrupted runs can be scored; missing predictions stay unresolved.
        manifest = None
    return frozen, manifest
