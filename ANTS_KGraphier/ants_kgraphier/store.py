"""SQLite event index; source content and labels never become model features."""
from collections import Counter
import json
import math
from pathlib import Path
import sqlite3
import time

from .io import canonical, digest, fingerprint, rows, write_json

SCHEMA = "kgraphier-store-1"


def connect(path):
    db = sqlite3.connect(f"file:{Path(path).resolve()}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    return db


def endpoint(node, recording, row, side):
    if not isinstance(node, dict):
        return f"{recording}:missing:{row}:{side}", "Missing", ""
    kind = str(node.get("Type", "Unknown"))
    raw = node.get("Key", "") if kind == "Registry" else ""
    raw = raw if isinstance(raw, str) else ""
    identity = node.get("UUID")
    # Keys/values must not collapse just because the exporter reused a UUID.
    identity = [identity, raw] if kind == "Registry" else identity
    if not identity:
        identity = ["unresolved", row, side]
    return recording + ":" + fingerprint([kind, identity])[:24], kind, raw


def ingest(data_root, sources, output):
    output = Path(output)
    if output.exists():
        raise FileExistsError("Refusing to replace event store: " + str(output))
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_suffix(".building.sqlite")
    if temp.exists():
        raise FileExistsError("Incomplete store exists; inspect it before restarting: " + str(temp))
    db = sqlite3.connect(temp)
    db.executescript("""
    PRAGMA journal_mode=WAL;
    CREATE TABLE recordings(id TEXT PRIMARY KEY, data TEXT NOT NULL);
    CREATE TABLE events(rec TEXT, row INTEGER, ord REAL, src TEXT, dst TEXT,
        src_type TEXT, dst_type TEXT, op TEXT, raw_key TEXT, raw_sha TEXT,
        PRIMARY KEY(rec,row));
    CREATE TABLE labels(rec TEXT, row INTEGER, label TEXT, PRIMARY KEY(rec,row));
    CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT);
    """)
    reports = []
    start = time.perf_counter()
    try:
        for source in sources["recordings"]:
            path = (Path(data_root) / source["path"]).resolve()
            if not path.is_relative_to(Path(data_root).resolve()):
                raise ValueError("source escapes data root")
            sha = digest(path)
            if sha != source["sha256"]:
                raise ValueError("source hash changed: " + str(path))
            rec = sha
            counts = Counter()
            batch, labels = [], []
            previous = None
            for index, raw in enumerate(rows(path, source["format"])):
                if not isinstance(raw, dict):
                    raise ValueError("non-object event")
                order = raw.get("timestamp")
                if not isinstance(order, (float, int)) or isinstance(order, bool) or not math.isfinite(order):
                    counts["invalid_order"] += 1
                    order = None
                if order is not None:
                    if previous is not None and order < previous:
                        counts["order_inversions"] += 1
                    previous = order
                src, st, _ = endpoint(raw.get("srcNode"), rec, index, "src")
                dst, dt, key = endpoint(raw.get("dstNode"), rec, index, "dst")
                op = str(raw.get("relation", "Unknown"))
                batch.append((rec, index, order, src, dst, st, dt, op, key, fingerprint(raw)))
                labels.append((rec, index, raw.get("label")))
                counts["events"] += 1
                counts["registry"] += dt == "Registry"
                counts["null_endpoint"] += "Missing" in (st, dt)
                if len(batch) == 10000:
                    db.executemany("INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?,?)", batch)
                    db.executemany("INSERT INTO labels VALUES(?,?,?)", labels)
                    batch.clear(); labels.clear()
            db.executemany("INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?,?)", batch)
            db.executemany("INSERT INTO labels VALUES(?,?,?)", labels)
            if counts["events"] != source["expected_records"]:
                raise ValueError("record count changed: " + str(path))
            record = dict(source, store_id=rec, counts=dict(counts))
            db.execute("INSERT INTO recordings VALUES(?,?)", (rec, canonical(record)))
            db.commit()
            reports.append(record)
            print(canonical({"ingested": source["id"], **counts}), flush=True)
        db.executescript("""
        CREATE INDEX by_src ON events(rec,src,ord,row);
        CREATE INDEX by_dst ON events(rec,dst,ord,row);
        CREATE INDEX registry_rows ON events(rec,dst_type,row);
        """)
        manifest = {"schema": SCHEMA, "recordings": reports,
                    "seconds": time.perf_counter() - start,
                    "source_manifest_sha256": fingerprint(sources),
                    "complete": True, "order_policy": "partial order only; ties unordered",
                    "model_fields": ["src_type", "dst_type", "op", "KG prefix IDs"]}
        db.execute("INSERT INTO metadata VALUES('manifest',?)", (canonical(manifest),))
        db.commit()
        db.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        db.close()
        temp.replace(output)
        write_json(output.with_suffix(".manifest.json"), manifest)
        return manifest
    except BaseException:
        db.close()
        raise


def recordings(db):
    return [json.loads(row[0]) for row in db.execute("SELECT data FROM recordings ORDER BY id")]


def event(db, rec, row):
    item = db.execute("SELECT * FROM events WHERE rec=? AND row=?", (rec, row)).fetchone()
    if item is None:
        raise KeyError((rec, row))
    return dict(item)
