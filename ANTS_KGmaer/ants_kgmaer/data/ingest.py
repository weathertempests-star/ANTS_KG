"""Stream a verified manifest into physically separated event and answer stores."""

from collections import Counter
import os
from pathlib import Path
import re
import sqlite3

from ..common.files import canonical, file_hash, object_hash, read_json, write_json
from .contracts import RelationContract
from .normalize import normalize
from .redaction import Redactor
from .sources import rows, verify_sources
from .store import EVENT_INDEXES, EVENT_SCHEMA, LABEL_SCHEMA


def classify_label(row, mapping):
    label = row.get("label")
    if not isinstance(label, str) or label not in mapping:
        return None, label, None, "missing_or_unapproved_label"
    binary = mapping[label]
    if type(binary) is not int or binary not in (0, 1):
        raise ValueError("Label mapping must contain integer 0 or 1")
    if binary == 0 and label != "benign":
        raise ValueError("Only explicitly annotated benign maps to 0")
    match = re.fullmatch(r"(T\d{4}(?:\.\d{3})?)(?:_.+)?", label)
    if binary == 1 and not match:
        raise ValueError("Approved attack label must preserve a technique prefix")
    return binary, label, match[1] if match else None, None


def ingest(source_manifest, data_root, labels_path, contract_path, output, progress=None):
    sources = verify_sources(source_manifest, data_root)
    labels = read_json(labels_path)
    if labels.get("schema") != "ants-labels-1":
        raise ValueError("Unsupported label map")
    contract = RelationContract(contract_path)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    os.chmod(output, 0o700)
    fingerprint = object_hash({"sources": [{k: v for k, v in s.items() if k != "absolute_path"} for s in sources],
                               "labels": labels, "contract": contract.document, "redaction": Redactor.VERSION})
    manifest = {"schema": "ants-dataset-1", "dataset_hash": fingerprint, "complete": False,
                "sources": [{k: v for k, v in s.items() if k != "absolute_path"} for s in sources],
                "label_provenance": "manual_per_event", "redaction_version": Redactor.VERSION,
                "relation_contract_hash": contract.hash, "label_map_hash": object_hash(labels)}
    write_json(output / "source_manifest.json", manifest)
    write_json(output / "relation_contract.json", contract.document)
    write_json(output / "label_map.json", labels)
    events = sqlite3.connect(output / "events.sqlite")
    answers = sqlite3.connect(output / "answers.sqlite")
    reports = []
    try:
        events.executescript(EVENT_SCHEMA)
        answers.executescript(LABEL_SCHEMA)
        for source in sources:
            counts, boundaries, label_counts, operations = Counter(), Counter(), Counter(), Counter()
            redactor = Redactor(source["id"])
            previous = None
            events.execute("INSERT INTO recordings VALUES(?,?,?)", (source["id"], source["cohort"], source["dependency_group"]))
            for index, raw in enumerate(rows(source["absolute_path"], source["format"])):
                item = normalize(raw, source, index, redactor, contract)
                binary, original, technique, reason = classify_label(raw, labels["mapping"])
                counts["records"] += 1
                counts["quarantined_labels"] += reason is not None
                counts["missing_order"] += item["order_ref"] is None
                if item["order_ref"] is not None:
                    counts["adjacent_order_decreases"] += previous is not None and item["order_ref"] < previous
                    previous = item["order_ref"]
                if item["target_type"] == "Registry":
                    counts["registry_records"] += 1
                    label_counts[str(binary)] += 1
                    boundaries[item["facts"]["registry"]["boundary_status"]] += 1
                    operations[item["facts"]["relation"]] += 1
                events.execute("INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?)", (
                    item["event_id"], item["recording_id"], index, item["actor_id"], item["order_ref"],
                    item["target_type"], canonical(item["facts"]), item["exact_signature"], item["normalized_signature"]))
                answers.execute("INSERT INTO labels VALUES(?,?,?,?,?,?)", (
                    item["event_id"], item["recording_id"], binary,
                    original if isinstance(original, str) else canonical(original), technique, reason))
                if index and index % 25000 == 0:
                    events.commit()
                    answers.commit()
                    if progress:
                        progress({"recording": source["id"], "processed": index + 1})
            if counts["records"] != source["expected_records"]:
                raise ValueError("Source record count mismatch: " + source["id"])
            if file_hash(source["absolute_path"]) != source["sha256"]:
                raise ValueError("Source changed during ingestion: " + source["id"])
            events.commit()
            answers.commit()
            reports.append({"recording_id": source["id"], **dict(counts), "registry_labels": dict(label_counts),
                            "boundaries": dict(boundaries), "operations": dict(operations),
                            "redactions": redactor.counts})
            write_json(output / "ingest_progress.json", {"complete": False, "recordings": reports}, replace=True)
        events.executescript(EVENT_INDEXES)
        events.commit()
    finally:
        events.close()
        answers.close()
    # Completion manifest is written only after both databases and all audits are durable.
    manifest.update(complete=True, recordings=reports,
                    files={name: file_hash(output / name) for name in ("events.sqlite", "answers.sqlite", "relation_contract.json", "label_map.json")})
    write_json(output / "normalization_audit.json", {"recordings": [{k: v for k, v in r.items() if k != "redactions"} for r in reports]})
    write_json(output / "redaction_audit.json", {"version": Redactor.VERSION, "recordings": [
        {"recording_id": r["recording_id"], "substitution_counts": r["redactions"]} for r in reports]})
    write_json(output / "annotation_audit.json", {"provenance": "manual_per_event", "unknown_policy": "quarantine",
               "recordings": [{"recording_id": r["recording_id"], "registry_labels": r["registry_labels"],
                               "quarantined": r["quarantined_labels"]} for r in reports]})
    write_json(output / "ingest_progress.json", {"complete": True, "recordings": reports}, replace=True)
    for name in ("annotation_audit.json", "normalization_audit.json", "redaction_audit.json", "ingest_progress.json"):
        manifest["files"][name] = file_hash(output / name)
    write_json(output / "source_manifest.json", manifest, replace=True)
    return manifest
