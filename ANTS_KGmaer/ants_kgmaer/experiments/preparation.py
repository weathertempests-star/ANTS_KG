"""Materialize label-free context and retrieval before independent coverage analysis."""

from pathlib import Path

from ..common.files import canonical, file_hash, write_json
from ..data.context import experiment_context
from ..data.store import EventStore
from ..knowledge.repository import DEFAULT_SNAPSHOT, KnowledgeRepository
from .config import freeze, load_config
from .targets import selected_targets


def coverage_record(target, result):
    return {**target, "match": result["match"], "boundary_status": result["boundary_status"],
            "path_complete": result["path_complete"], "explanations_complete": result["explanations_complete"],
            "pattern_complete": result.get("pattern_complete", False),
            "pattern_explanations_complete": result.get("pattern_explanations_complete", False),
            "matched_nodes": len(result["nodes"]),
            "deepest_matched_level": max((node["depth"] for node in result["nodes"]), default=0)}


def prepare_inputs(config_path, dataset, selection, output, snapshot=DEFAULT_SNAPSHOT, progress=None):
    config = load_config(config_path)
    frozen = freeze(config, dataset, selection, snapshot)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "manifest.json", {"schema": "ants-preparation-1", "complete": False})
    write_json(output / "config.json", frozen)
    store = EventStore(Path(dataset) / "events.sqlite")
    repository = KnowledgeRepository(snapshot, output / "kg_cache.sqlite")
    count = 0
    try:
        with (output / "contexts.jsonl").open("w", encoding="utf-8") as contexts, \
                (output / "coverage_events.jsonl").open("w", encoding="utf-8") as coverage:
            for target in selected_targets(selection, config):
                packet, aliases, _ = experiment_context(store, target["event_id"], config)
                # Provenance is an outer envelope, never included in packet sent to a model.
                contexts.write(canonical({"event_id": target["event_id"], "context": packet,
                                          "event_aliases": {key: value["event_id"] for key, value in aliases.items()}}) + "\n")
                registry = aliases["event_0"]["facts"]["registry"]
                result = repository.lookup(registry, config.get("template_candidates", False))
                coverage.write(canonical(coverage_record(target, result)) + "\n")
                count += 1
                if progress and count % 1000 == 0:
                    progress({"prepared_targets": count})
        if not count:
            raise ValueError("No selected targets")
        with (output / "kg_context_cache.jsonl").open("w", encoding="utf-8") as cache:
            for key, payload, checksum in repository.cache.execute(
                "SELECT key,payload,payload_hash FROM knowledge_cache ORDER BY key"
            ):
                cache.write('{"cache_key":' + canonical(key) + ',"payload_hash":' + canonical(checksum)
                            + ',"result":' + payload + '}\n')
    finally:
        repository.close()
        store.close()
    # Answer access is confined to a separate evaluation module, after packet generation.
    from ..evaluation.coverage import write_coverage_report
    write_coverage_report(dataset, output / "coverage_events.jsonl", output / "coverage_report.csv")
    names = ("config.json", "contexts.jsonl", "coverage_events.jsonl", "kg_context_cache.jsonl",
             "kg_cache.sqlite", "coverage_report.csv")
    manifest = {"schema": "ants-preparation-1", "complete": True, "target_count": count,
                "config_hash": frozen["config_hash"], "dataset_hash": frozen["dataset_hash"],
                "snapshot_sha256": frozen["snapshot_sha256"],
                "files": {name: file_hash(output / name) for name in names}}
    write_json(output / "manifest.json", manifest, replace=True)
    return manifest
