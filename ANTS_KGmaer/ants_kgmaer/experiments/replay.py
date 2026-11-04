"""Replay exactly the agent's final delivered evidence with acquisition cost recorded."""

import json
from pathlib import Path

from ..agent.budget import Budget
from ..common.files import file_hash, object_hash, read_json
from ..data.store import readonly
from ..common.artifacts import verify_files


class ReplaySource:
    def __init__(self, path, frozen):
        self.path = Path(path)
        manifest = read_json(self.path / "manifest.json")
        source = read_json(self.path / "config.json")
        if not manifest.get("complete") or source["configuration"]["condition"] != "agent":
            raise ValueError("Replay requires a complete agent run")
        if manifest["config_hash"] != source["config_hash"] or object_hash(
            {k: v for k, v in source.items() if k != "config_hash"}
        ) != source["config_hash"]:
            raise ValueError("Replay source configuration identity mismatch")
        if "journal.sqlite" not in manifest["files"]:
            raise ValueError("Replay source journal is not integrity-covered")
        verify_files(self.path, manifest["files"])
        for key in ("dataset_hash", "targets_sha256", "split_sha256", "snapshot_sha256"):
            if source[key] != frozen[key]:
                raise ValueError("Replay input identity differs: " + key)
        defaults = {"history_k": 0, "template_candidates": False, "include_value_data": False,
                    "dynamic_history": False,
                    "model": None, "limits": {}, "split": None, "engineering_limit": None}
        for key, default in defaults.items():
            if source["configuration"].get(key, default) != frozen["configuration"].get(key, default):
                raise ValueError("Replay configuration differs: " + key)
        self.identity = {"config_hash": source["config_hash"], "manifest_sha256": file_hash(self.path / "manifest.json")}
        self.limits = source["configuration"].get("limits", {})

    def prepare(self, session, event_id):
        connection = readonly(self.path / "journal.sqlite")
        try:
            row = connection.execute("SELECT result FROM targets WHERE event_id=? AND status='complete'", (event_id,)).fetchone()
            if row is None:
                raise ValueError("Replay source is missing a selected target")
            result = json.loads(row[0])
            packet = result["final_input"]
            acquisition = Budget(**self.limits)
            calls = {}
            for kind, payload in connection.execute("SELECT kind,payload FROM traces WHERE event_id=? ORDER BY ordinal", (event_id,)):
                payload = json.loads(payload)
                if kind == "model_request" and payload["task"] == "action":
                    calls[payload["call_index"]] = None
                elif kind in {"model_reply", "model_error"} and payload["call_index"] in calls:
                    calls[payload["call_index"]] = (kind, payload)
            for reply in calls.values():
                acquisition.start()
                if reply and reply[0] == "model_reply":
                    acquisition.input_tokens += reply[1]["prompt_tokens"]
                    acquisition.output_tokens += reply[1]["completion_tokens"]
                elif reply is None or reply[1].get("unknown_usage", True):
                    acquisition.uncertain()
        finally:
            connection.close()
        metadata = {"source": self.identity, "source_status": result["status"],
                    "acquisition_usage": acquisition.usage(), "source_total_usage": result["usage"],
                    "source_tool_requests": result["tool_requests"],
                    "delivered_packet_sha256": object_hash(packet) if packet is not None else None}
        if packet is not None:
            from ..agent.history import adopt_replay_context
            adopt_replay_context(session, packet["context"])
            session.replay_packet = packet["knowledge"]
            session.observations = packet["tool_observations"]
        return packet is not None, metadata
