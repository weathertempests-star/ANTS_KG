"""Freeze input/code/model identities before any experiment request."""

from pathlib import Path
import re

from ..common.files import file_hash, object_hash, read_json
from .conditions import CONDITIONS


def source_hash():
    package = Path(__file__).resolve().parents[1]
    return object_hash({str(p.relative_to(package)): file_hash(p) for p in sorted(package.rglob("*.py"))})


def load_config(path):
    config = read_json(path)
    allowed = {"schema", "condition", "history_k", "template_candidates", "include_value_data", "model",
               "orchestrator", "limits", "seed", "split", "engineering_limit", "replay_run", "dynamic_history"}
    if config.get("schema") != "ants-run-config-1" or set(config) - allowed:
        raise ValueError("Unsupported run configuration or unexpected fields")
    if config["condition"] not in CONDITIONS:
        raise ValueError("Unsupported condition")
    if config.get("orchestrator", "native") not in {"native", "langgraph"}:
        raise ValueError("Unsupported orchestrator")
    for key in ("template_candidates", "include_value_data", "dynamic_history"):
        if key in config and type(config[key]) is not bool:
            raise ValueError(key + " must be boolean")
    if config.get("dynamic_history") and (config["condition"] not in {"agent", "replay"} or config.get("history_k", 0) != 0):
        raise ValueError("Dynamic history is a secondary agent/replay condition with initial history_k=0")
    if "seed" in config and (type(config["seed"]) is not int or config["seed"] < 0):
        raise ValueError("seed must be a nonnegative integer")
    if config.get("split") not in {None, "development", "validation", "test", "evaluation"}:
        raise ValueError("Unsupported split")
    if type(config.get("history_k", 0)) is not int or config.get("history_k", 0) not in (0, 8, 16, 32):
        raise ValueError("History k must be 0/8/16/32; 8/32 are sensitivity analyses")
    limits = config.get("limits", {})
    if set(limits) - {"max_input", "max_output", "max_calls", "max_total"} or any(
        type(value) is not int or value < 1 for value in limits.values()
    ):
        raise ValueError("Limits must be positive integer maxima, not mutable usage counters")
    maxima = {"max_input": 4096, "max_output": 512, "max_calls": 4, "max_total": 18432}
    if any(value > maxima[key] for key, value in limits.items()):
        raise ValueError("Run limits cannot exceed the frozen research protocol maxima")
    model = config["model"]
    allowed_model = {"backend", "base_url", "served_model", "repo", "revision", "tokenizer_revision", "image_digest",
                     "precision", "temperature", "top_p", "top_k", "seed", "timeout"}
    if not isinstance(model, dict) or set(model) - allowed_model:
        raise ValueError("Unsupported model field; credentials belong only in environment variables")
    if model["backend"] not in {"vllm", "mock"}:
        raise ValueError("Unsupported model backend")
    if model["backend"] == "vllm":
        from ..models.http import check_origin
        check_origin(model["base_url"])
        for key in ("revision", "tokenizer_revision"):
            if not re.fullmatch(r"[0-9a-f]{40}", model.get(key, "")):
                raise ValueError("Real inference requires a fixed model and tokenizer commit SHA")
        if not re.fullmatch(r".+@sha256:[0-9a-f]{64}", model.get("image_digest", "")):
            raise ValueError("Real inference requires the deployment image digest")
        if not model.get("repo") or not model.get("precision"):
            raise ValueError("Real inference requires repo and precision")
    if config.get("engineering_limit") is not None:
        if type(config["engineering_limit"]) is not int or config["engineering_limit"] < 1:
            raise ValueError("engineering_limit must be a positive integer")
    return config


def freeze(config, dataset, selection, snapshot):
    dataset, selection = Path(dataset), Path(selection)
    data = read_json(dataset / "source_manifest.json")
    targets = read_json(selection / "manifest.json")
    if not data["complete"] or not targets["complete"] or targets["dataset_hash"] != data["dataset_hash"]:
        raise ValueError("Incomplete or mismatched dataset/selection")
    if file_hash(selection / "targets.jsonl") != targets["targets_sha256"]:
        raise ValueError("Target list has changed")
    if file_hash(selection / "split_manifest.json") != targets["split_sha256"]:
        raise ValueError("Split manifest has changed")
    for name, expected in data["files"].items():
        if file_hash(dataset / name) != expected:
            raise ValueError("Dataset artifact has changed: " + name)
    frozen = {"configuration": config, "dataset_hash": data["dataset_hash"],
              "source_manifest_sha256": file_hash(dataset / "source_manifest.json"),
              "targets_sha256": targets["targets_sha256"], "split_sha256": targets["split_sha256"],
              "snapshot_sha256": file_hash(snapshot), "code_sha256": source_hash(),
              "engineering_only": config["model"]["backend"] == "mock" or bool(config.get("engineering_limit"))}
    return {**frozen, "config_hash": object_hash(frozen)}
