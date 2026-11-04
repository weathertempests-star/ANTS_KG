"""Explicit source manifests, streamed JSONL, and incremental JSON-array parsing."""

import json
from pathlib import Path

from ..common.files import file_hash, jsonl, read_json


def stream_array(path, chunk_size=1024 * 1024):
    """Parse JSON arrays without retaining entire recordings in memory."""
    decoder = json.JSONDecoder()
    with Path(path).open(encoding="utf-8-sig") as stream:
        buffer, position, eof = "", 0, False

        def refill():
            nonlocal buffer, position, eof
            part = stream.read(chunk_size)
            buffer = buffer[position:] + part
            position = 0
            eof = not part

        def skip_space():
            nonlocal position
            while True:
                while position < len(buffer) and buffer[position].isspace():
                    position += 1
                if position < len(buffer) or eof:
                    return
                refill()

        refill()
        skip_space()
        if buffer[position:position + 1] != "[":
            raise ValueError(f"Expected JSON array: {path}")
        position += 1
        first = True
        while True:
            skip_space()
            if buffer[position:position + 1] == "]":
                position += 1
                break
            if not first:
                if buffer[position:position + 1] != ",":
                    raise ValueError(f"Expected comma in {path}")
                position += 1
                skip_space()
            while True:
                try:
                    item, end = decoder.raw_decode(buffer, position)
                    break
                except json.JSONDecodeError:
                    if eof:
                        raise ValueError(f"Incomplete or invalid JSON array: {path}") from None
                    refill()
            position = end
            if not isinstance(item, dict):
                raise ValueError("Every event must be an object")
            yield item
            first = False
        skip_space()
        if position != len(buffer):
            raise ValueError(f"Trailing content after array: {path}")


def rows(path, format_name):
    if format_name == "json_array":
        yield from stream_array(path)
    elif format_name == "jsonl":
        for row in jsonl(path):
            if not isinstance(row, dict):
                raise ValueError("Every event must be an object")
            yield row
    else:
        raise ValueError("Unsupported recording format: " + str(format_name))


def verify_sources(manifest_path, data_root):
    manifest = read_json(manifest_path)
    if manifest.get("schema") != "ants-sources-1":
        raise ValueError("Unsupported sources manifest")
    root = Path(data_root).resolve()
    seen, sources = set(), []
    for item in manifest["recordings"]:
        path = (root / item["path"]).resolve()
        if not path.is_relative_to(root) or ".ipynb_checkpoints" in path.parts:
            raise ValueError("Source escapes data root or is a notebook checkpoint")
        if item["id"] in seen:
            raise ValueError("Duplicate recording ID")
        seen.add(item["id"])
        actual = file_hash(path)
        if actual != item["sha256"]:
            raise ValueError("Source SHA-256 mismatch: " + item["path"])
        sources.append({**item, "absolute_path": str(path), "bytes": path.stat().st_size})
    if not sources:
        raise ValueError("Empty source manifest")
    return sources
