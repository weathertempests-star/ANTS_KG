"""Versioned, deterministic artifacts and streaming source readers."""
import hashlib
import json
from pathlib import Path


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def fingerprint(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def rows(path, fmt):
    if fmt == "json_array":
        import ijson
        with Path(path).open("rb") as f:
            yield from ijson.items(f, "item", use_float=True)
    elif fmt == "jsonl":
        with Path(path).open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)
    else:
        raise ValueError("unsupported source format: " + fmt)


def jsonl(path):
    return rows(path, "jsonl")
