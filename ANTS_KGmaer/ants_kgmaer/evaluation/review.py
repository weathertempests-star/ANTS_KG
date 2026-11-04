"""Blinded claim packets and strict import of human support judgments."""

from collections import Counter
import csv
import json
from pathlib import Path
import random

from ..common.files import canonical, file_hash, jsonl, object_hash, read_json, write_json
from ..data.store import readonly
from ..common.artifacts import verify_files
from .metrics import divide


def sample_claims(run, limit, seed):
    randomizer = random.Random(seed)
    selected, population, statuses = [], 0, Counter()
    connection = readonly(run / "journal.sqlite")
    try:
        for event_id, payload in connection.execute("SELECT event_id,result FROM targets WHERE status='complete' ORDER BY event_id"):
            result = json.loads(payload)
            statuses[result["status"]] += 1
            if result["status"] not in {"valid", "abstained"} or not result.get("final_input"):
                continue
            for index, claim in enumerate((result.get("answer") or {}).get("claims", [])):
                population += 1
                item = {"event_id": event_id, "claim_index": index, "claim": claim, "packet": result["final_input"]}
                if len(selected) < limit:
                    selected.append(item)
                else:
                    replace = randomizer.randrange(population)
                    if replace < limit:
                        selected[replace] = item
    finally:
        connection.close()
    randomizer.shuffle(selected)
    return selected, population, dict(statuses)


def export_review(run, output, limit=100, seed=20261026):
    if type(limit) is not int or limit < 1:
        raise ValueError("Review sample size must be a positive integer")
    run, output = Path(run), Path(output)
    manifest = read_json(run / "manifest.json")
    if not manifest.get("complete") or "journal.sqlite" not in manifest["files"]:
        raise ValueError("Review requires a complete integrity-covered run journal")
    verify_files(run, manifest["files"])
    selected, population, statuses = sample_claims(run, limit, seed)
    output.mkdir(parents=True, exist_ok=False)
    (output / "blind").mkdir()
    (output / "internal").mkdir()
    with (output / "blind/packets.jsonl").open("w", encoding="utf-8") as packets, \
            (output / "internal/assignments.jsonl").open("w", encoding="utf-8") as assignments, \
            (output / "blind/reviews.csv").open("w", newline="", encoding="utf-8") as form:
        writer = csv.writer(form)
        writer.writerow(["review_id", "judgment", "reviewer", "note"])
        for index, item in enumerate(selected):
            review_id = "review_" + object_hash([seed, index, manifest["config_hash"]])[:20]
            packet = item["packet"]
            allowed = {packet["context"]["target"]["id"]} | {e["id"] for e in packet["context"]["history"]}
            allowed |= {node["id"] for node in packet["knowledge"]["nodes"]}
            citations_valid = bool(item["claim"]["evidence_ids"]) and set(item["claim"]["evidence_ids"]) <= allowed
            packets.write(canonical({"review_id": review_id, "claim": item["claim"],
                                     "events": packet["context"], "knowledge": packet["knowledge"]}) + "\n")
            assignments.write(canonical({"review_id": review_id, "event_id": item["event_id"],
                                         "claim_index": item["claim_index"], "citations_valid": citations_valid,
                                         "inclusion_probability": len(selected) / population}) + "\n")
            writer.writerow([review_id, "", "", ""])
    (output / "blind/README.md").write_text(
        "# Human evidence-support review\n\n"
        "Review only whether the cited observations and supplied knowledge support the claim. "
        "Registry function alone does not prove malicious intent or successful execution. "
        "Use supported, unsupported, or uncertain; enter a reviewer ID and a brief note. "
        "Do not infer the hidden ground truth or fill in missing evidence from memory.\n\n"
        "Copy reviews.csv to a separate location before editing. Leave pending judgments empty. "
        "Return that copy for review-import. Model, condition, prediction, provenance, and ground truth are hidden; "
        "the evidence representation or claim wording may still suggest the method, so blinding is not guaranteed.\n",
        encoding="utf-8")
    names = ("blind/packets.jsonl", "blind/reviews.csv", "blind/README.md", "internal/assignments.jsonl")
    result = {"schema": "ants-review-1", "complete": True, "engineering_only": manifest["engineering_only"],
              "run_manifest_sha256": file_hash(run / "manifest.json"), "population_claims": population,
              "sampled_claims": len(selected), "seed": seed, "run_status_counts": statuses,
              "sampling": "Uniform without replacement over claims in valid or abstained outputs with final evidence",
              "files": {name: file_hash(output / name) for name in names}}
    write_json(output / "manifest.json", result)
    return result


def import_review(review, annotations, output):
    review = Path(review)
    manifest = read_json(review / "manifest.json")
    if manifest.get("schema") != "ants-review-1" or not manifest.get("complete"):
        raise ValueError("Complete review export required")
    verify_files(review, manifest["files"])
    assignments = {row["review_id"]: row for row in jsonl(review / "internal/assignments.jsonl")}
    counts, seen = Counter(), set()
    with Path(annotations).open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["review_id", "judgment", "reviewer", "note"]:
            raise ValueError("Unexpected review CSV columns")
        for row in reader:
            review_id = row["review_id"]
            if review_id not in assignments or review_id in seen:
                raise ValueError("Unknown or duplicated review ID")
            seen.add(review_id)
            judgment = row["judgment"].strip()
            if judgment not in {"", "supported", "unsupported", "uncertain"}:
                raise ValueError("Invalid human judgment")
            if judgment and (not row["reviewer"].strip() or not row["note"].strip()):
                raise ValueError("Completed human judgments require reviewer and note")
            counts[judgment or "pending"] += 1
    counts["pending"] += len(assignments) - len(seen)
    reviewed = sum(counts[key] for key in ("supported", "unsupported", "uncertain"))
    result = {"schema": "ants-human-support-1", "engineering_only": manifest["engineering_only"],
              "review_manifest_sha256": file_hash(review / "manifest.json"), "annotations_sha256": file_hash(annotations),
              "population_claims": manifest["population_claims"], "sampled_claims": len(assignments),
              "judgments": dict(counts), "reviewed": reviewed,
              "completion_rate": divide(reviewed, len(assignments)),
              "human_support_rate_reviewed": divide(counts["supported"], reviewed),
              "citation_id_validity_rate_sampled": divide(sum(row["citations_valid"] for row in assignments.values()), len(assignments)),
              "limitations": "Citation validity is separate from human support. Pending claims are not supported. Partial review may be biased; no automatic correctness claim."}
    write_json(output, result)
    return result
