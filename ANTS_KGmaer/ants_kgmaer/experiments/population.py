"""Audit every Registry event while retrieving each distinct query only once."""

import json
from pathlib import Path
import sqlite3

from ..common.files import canonical, file_hash, object_hash, read_json, write_json
from ..data.store import readonly
from ..common.artifacts import verify_files
from ..knowledge.repository import DEFAULT_SNAPSHOT, KnowledgeRepository
from .config import source_hash


def audit_population(dataset, output, snapshot=DEFAULT_SNAPSHOT, templates=False, progress=None):
    dataset, output = Path(dataset), Path(output)
    source = read_json(dataset / "source_manifest.json")
    if not source.get("complete"):
        raise ValueError("Complete dataset required")
    verify_files(dataset, source["files"])
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "manifest.json", {"schema": "ants-population-coverage-1", "complete": False})
    identity = {"dataset_hash": source["dataset_hash"], "source_manifest_sha256": file_hash(dataset / "source_manifest.json"),
                "snapshot_sha256": file_hash(snapshot), "code_sha256": source_hash(), "template_candidates": templates}
    write_json(output / "config.json", identity)
    events = readonly(dataset / "events.sqlite")
    repository = KnowledgeRepository(snapshot, output / "kg_cache.sqlite")
    index = sqlite3.connect(output / "coverage.sqlite")
    index.executescript("""
        CREATE TABLE queries(query_id TEXT PRIMARY KEY, registry TEXT, match TEXT,
            boundary_status TEXT, path_complete INTEGER, explanations_complete INTEGER,
            matched_nodes INTEGER, deepest_level INTEGER);
        CREATE TABLE events(event_id TEXT PRIMARY KEY, recording_id TEXT, query_id TEXT);
    """)
    known, count = set(), 0
    try:
        for row in events.execute("SELECT event_id,recording_id,facts FROM events WHERE target_type='Registry' ORDER BY recording_id,row_index"):
            registry = json.loads(row["facts"])["registry"]
            query_id = object_hash(registry)
            if query_id not in known:
                result = repository.lookup(registry, templates)
                index.execute("INSERT INTO queries VALUES(?,?,?,?,?,?,?,?)", (
                    query_id, canonical(registry), result["match"], result["boundary_status"],
                    result["path_complete"], result["explanations_complete"], len(result["nodes"]),
                    max((node["depth"] for node in result["nodes"]), default=0)))
                known.add(query_id)
            index.execute("INSERT INTO events VALUES(?,?,?)", (row["event_id"], row["recording_id"], query_id))
            count += 1
            if count % 25000 == 0:
                index.commit()
                if progress:
                    progress({"registry_events": count, "unique_queries": len(known)})
        index.commit()
    finally:
        index.close()
        repository.close()
        events.close()
    from ..evaluation.population import summarize_population
    summary = summarize_population(dataset, output / "coverage.sqlite", output / "coverage_report.csv")
    if summary["registry_events"] != count:
        raise ValueError("Population coverage denominator mismatch")
    write_json(output / "summary.json", summary)
    names = ("config.json", "coverage.sqlite", "kg_cache.sqlite", "coverage_report.csv", "summary.json")
    manifest = {"schema": "ants-population-coverage-1", "complete": True, **identity,
                "registry_events": count, "unique_queries": len(known),
                "files": {name: file_hash(output / name) for name in names}}
    write_json(output / "manifest.json", manifest, replace=True)
    return manifest
