"""Sequential, resumable experiment execution; only public event views reach models."""

import fcntl
from pathlib import Path

from ..agent.session import AgentSession
from ..common.files import append_jsonl, file_hash, jsonl, object_hash, read_json, write_json
from ..data.context import experiment_context
from ..data.store import EventStore
from ..knowledge.repository import DEFAULT_SNAPSHOT, KnowledgeRepository
from ..models.mock import MockAdapter
from ..models.vllm import VllmAdapter
from .conditions import fixed_evidence, unrelated_evidence
from .config import freeze, load_config
from .journal import RunJournal
from .targets import selected_targets
from .replay import ReplaySource
from .telemetry import summarize


def prepare_session(adapter, repository, store, target_id, config, trace):
    condition = config["condition"]
    context, events, candidates = experiment_context(store, target_id, config)
    session = AgentSession(adapter, repository, context, events, config, trace)
    session.toolbox.dynamic_history = candidates
    if condition in {"text", "graph", "flat", "unrelated", "budget"}:
        session.evidence = fixed_evidence(repository, events, config.get("template_candidates", False))
        if condition == "unrelated":
            session.evidence = unrelated_evidence(repository, session.evidence, context, config.get("seed", 20261026))
        session.toolbox.evidence = session.evidence
    session.mode = {"text": "text", "flat": "flat"}.get(condition, "graph")
    return session


def execute_run(config_path, dataset, selection, output, snapshot=DEFAULT_SNAPSHOT, progress=None, adapter=None):
    config = load_config(config_path)
    frozen = freeze(config, dataset, selection, snapshot)
    replay = None
    if config["condition"] == "replay":
        if not config.get("replay_run"):
            raise ValueError("Replay requires replay_run in its configuration")
        source_path = Path(config["replay_run"])
        if not source_path.is_absolute():
            source_path = Path(config_path).resolve().parent / source_path
        replay = ReplaySource(source_path, frozen)
        frozen.pop("config_hash")
        frozen["replay_source"] = replay.identity
        frozen["config_hash"] = object_hash(frozen)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    with (output / ".run.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("This output directory already has an active runner") from None
        if not (output / "config.json").exists() and any(p.name != ".run.lock" for p in output.iterdir()):
            raise FileExistsError("Output must be empty or belong to this runner")
        previous = None
        if (output / "manifest.json").exists():
            previous = read_json(output / "manifest.json")
            for name, expected in previous["files"].items():
                if not (output / name).is_file() or file_hash(output / name) != expected:
                    raise ValueError("Generated run artifact changed; preserve edits and use a new output directory: " + name)
        config_file = output / "config.json"
        if config_file.exists():
            if read_json(config_file) != frozen:
                raise ValueError("Output belongs to a different frozen run; use a new directory")
        else:
            if (output / "journal.sqlite").exists():
                raise ValueError("Journal without configuration; inspect incomplete output")
            write_json(config_file, frozen)
        if previous and previous.get("complete"):
            # A verified complete run is immutable; do not rewrite its journal or exports.
            return previous
        adapter = adapter or (MockAdapter() if config["model"]["backend"] == "mock" else VllmAdapter(config["model"]))
        if adapter.backend != config["model"]["backend"]:
            raise ValueError("Adapter/backend mismatch")
        preflight = adapter.preflight()
        write_json(output / "preflight.json", preflight, replace=True)
        store = EventStore(Path(dataset) / "events.sqlite")
        repository = KnowledgeRepository(snapshot, output / "kg_cache.sqlite")
        journal = RunJournal(output / "journal.sqlite", frozen["config_hash"])
        count = executed = 0
        try:
            for target in selected_targets(selection, config):
                count += 1
                target_id = target["event_id"]
                if journal.completed(target_id):
                    continue
                journal.begin(target_id)
                session = prepare_session(adapter, repository, store, target_id, config,
                    lambda kind, payload, event_id=target_id: journal.trace(event_id, kind, payload))
                journal.restore(target_id, session)
                available, replay_metadata = replay.prepare(session, target_id) if replay else (True, None)
                result = (session.execute(config["condition"], config.get("orchestrator", "native")) if available
                          else session.result("replay_source_unavailable", error="Source agent never delivered a final decision packet"))
                if replay:
                    result["replay"] = replay_metadata
                journal.finish(target_id, result)
                executed += 1
                if progress:
                    progress({"processed": count, "executed_now": executed, "status": result["status"]})
            if not count:
                raise ValueError("No targets match this run")
            journal.export(output)
            write_json(output / "usage.json", summarize(journal), replace=True)
            from ..agent.schemas import DECISION, action_schema
            write_json(output / "schemas.json", {"decision": DECISION,
                       "action": action_schema(config.get("dynamic_history", False))}, replace=True)
            manifest = {"schema": "ants-run-1", "complete": True, "config_hash": frozen["config_hash"],
                        "target_count": count, "engineering_only": frozen["engineering_only"],
                        "files": {name: file_hash(output / name) for name in (
                            "predictions.jsonl", "evidence_packets.jsonl", "prompts.jsonl", "tool_calls.jsonl", "usage.jsonl",
                            "usage.json", "schemas.json", "journal.sqlite", "config.json", "preflight.json", "kg_cache.sqlite")}}
            write_json(output / "manifest.json", manifest, replace=True)
            return manifest
        finally:
            journal.close()
            repository.close()
            store.close()
