"""Durable per-target checkpoints and attempt accounting, independent of model state."""

import json
import os
from pathlib import Path
import sqlite3
import tempfile
import time

from ..common.files import canonical, object_hash


class RunJournal:
    def __init__(self, path, config_hash):
        self.connection = sqlite3.connect(path)
        self.connection.executescript("""
            CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT);
            CREATE TABLE IF NOT EXISTS targets (event_id TEXT PRIMARY KEY, status TEXT, result TEXT);
            CREATE TABLE IF NOT EXISTS traces (
                ordinal INTEGER PRIMARY KEY, event_id TEXT, kind TEXT, payload TEXT, wall_time REAL
            );
            CREATE INDEX IF NOT EXISTS trace_target ON traces(event_id, ordinal);
        """)
        row = self.connection.execute("SELECT value FROM metadata WHERE key='config_hash'").fetchone()
        if row and row[0] != config_hash:
            self.connection.close()
            raise ValueError("Cannot resume with a different run configuration")
        self.connection.execute("INSERT OR IGNORE INTO metadata VALUES('config_hash',?)", (config_hash,))
        self.connection.commit()

    def close(self):
        self.connection.close()

    def completed(self, event_id):
        row = self.connection.execute("SELECT status FROM targets WHERE event_id=?", (event_id,)).fetchone()
        return row is not None and row[0] == "complete"

    def begin(self, event_id):
        self.connection.execute("INSERT OR IGNORE INTO targets VALUES(?,'running',NULL)", (event_id,))
        self.connection.commit()

    def trace(self, event_id, kind, payload):
        self.connection.execute("INSERT INTO traces(event_id,kind,payload,wall_time) VALUES(?,?,?,?)",
                                (event_id, kind, canonical(payload), time.time()))
        self.connection.commit()

    def history(self, event_id):
        return [(kind, json.loads(payload)) for kind, payload in self.connection.execute(
            "SELECT kind,payload FROM traces WHERE event_id=? ORDER BY ordinal", (event_id,))]

    def restore(self, event_id, session):
        """Account for every earlier attempt, including interrupted in-flight requests."""
        calls = {}
        for kind, payload in self.history(event_id):
            if kind == "model_request":
                calls[payload["call_index"]] = {"request": payload}
            elif kind in {"model_reply", "model_error"}:
                calls.setdefault(payload["call_index"], {})[kind] = payload
            elif kind == "tool_reply":
                session.toolbox.requests += 1
                session.toolbox.seen.add(object_hash({"tool": payload["tool"], "arguments": payload["arguments"]}))
                session.observations.append({k: v for k, v in payload.items() if k != "result"})
                result = payload["result"]
                if payload["tool"] == "lookup_registry":
                    for item in result["results"]:
                        session.evidence.add(item, item["event_id"])
                elif payload["tool"] == "expand_knowledge":
                    session.evidence.add(result)
                elif payload["tool"] == "get_prior_context":
                    from ..agent.history import reveal_history
                    reveal_history(session, result["history"])
            elif kind == "tool_error":
                session.toolbox.requests += 1
                if "arguments" in payload:
                    session.toolbox.seen.add(object_hash({"tool": payload["tool"], "arguments": payload["arguments"]}))
                session.observations.append(payload)
            elif kind == "invalid_action":
                session.toolbox.requests += payload.get("requested_tool_count", 0)
        for _, call in sorted(calls.items()):
            session.budget.start()
            task = call["request"]["task"]
            if task == "action":
                session.rounds += 1
            elif task == "decision":
                session.decision_calls += 1
                session.pending_decision = None
                if call.get("model_reply"):
                    body = json.loads(call["request"]["messages"][-1]["content"])
                    session.pending_decision = (call["model_reply"], {
                        "context": body["events"], "knowledge": body["knowledge"],
                        "tool_observations": body["tool_observations"]})
            reply = call.get("model_reply")
            if reply:
                session.budget.input_tokens += reply["prompt_tokens"]
                session.budget.output_tokens += reply["completion_tokens"]
            elif call.get("model_error", {}).get("unknown_usage", True):
                session.budget.uncertain()
        if calls:
            self.trace(event_id, "resumed", {"previous_calls": len(calls), "usage": session.budget.usage()})

    def finish(self, event_id, result):
        self.connection.execute("UPDATE targets SET status='complete',result=? WHERE event_id=?", (canonical(result), event_id))
        self.connection.commit()

    def results(self):
        for event_id, payload in self.connection.execute("SELECT event_id,result FROM targets WHERE status='complete' ORDER BY event_id"):
            yield event_id, json.loads(payload)

    def export(self, directory):
        directory = Path(directory)
        names = ("predictions", "evidence_packets", "prompts", "tool_calls", "usage")
        staged, streams = {}, {}
        for name in names:
            descriptor, path = tempfile.mkstemp(prefix="." + name, suffix=".jsonl", dir=directory)
            staged[name] = Path(path)
            streams[name] = os.fdopen(descriptor, "w", encoding="utf-8")
        try:
            for event_id, result in self.results():
                streams["predictions"].write(canonical({"event_id": event_id, **{k: v for k, v in result.items() if k != "final_input"}}) + "\n")
                streams["evidence_packets"].write(canonical({"event_id": event_id, "final_input": result["final_input"]}) + "\n")
                streams["usage"].write(canonical({"event_id": event_id, **result["usage"]}) + "\n")
            for event_id, kind, payload, wall_time in self.connection.execute("SELECT event_id,kind,payload,wall_time FROM traces ORDER BY ordinal"):
                record = {"event_id": event_id, "kind": kind, "wall_time": wall_time, **json.loads(payload)}
                name = "prompts" if kind.startswith("model_") else "tool_calls"
                streams[name].write(canonical(record) + "\n")
            for stream in streams.values():
                stream.flush()
                os.fsync(stream.fileno())
                stream.close()
            for name, path in staged.items():
                os.replace(path, directory / (name + ".jsonl"))
        finally:
            for stream in streams.values():
                stream.close()
            for path in staged.values():
                path.unlink(missing_ok=True)
