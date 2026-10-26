"""Audit the Registry KG as a reproducible research dataset."""
import argparse
from collections import Counter
from datetime import date, datetime
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import urldefrag

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.assemble_registry_research import BATCHES, assemble
from scripts.prepare_registry_evaluation import validate_evaluation
from standardizer_pkg import KnowledgeBase
from standardizer_pkg.model_data import audit_graph, validate_model_data
from standardizer_pkg.zettelkasten import _atomic_write, validate_vault


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def audit(as_of):
    as_of_date = datetime.strptime(as_of, "%Y-%m-%d").date()
    catalog_path = ROOT / "knowledge/windows_registry.json"
    inventory_path = ROOT / "artifacts/registry-inventory/inventory.json"
    vault_path = ROOT / "artifacts/knowledge-vault"
    model_path = ROOT / "artifacts/model-data"
    source_path = ROOT / "knowledge/research/source_reviews.json"
    semantics_path = ROOT / "knowledge/registry_log_semantics.json"
    catalog, source_reviews = assemble()
    if catalog != json.loads(catalog_path.read_text(encoding="utf-8")):
        raise ValueError("catalog differs from reviewed research batches")
    if source_reviews != json.loads(source_path.read_text(encoding="utf-8")):
        raise ValueError("source review ledger differs from reviewed research batches")
    graph = KnowledgeBase.load_catalog(catalog_path, inventory_path)
    saved = KnowledgeBase.load(vault_path / "kg.json")
    if graph.to_dict() != saved.to_dict():
        raise ValueError("saved vault graph differs from catalog and inventory")
    data = graph.to_dict()
    content = audit_graph(graph)
    if not content["valid"]:
        raise ValueError("graph content audit failed")
    peer_review_counts = {}
    reviewed = set()
    peer_names = {"core": "core_peer.json", "user_zones": "user_zones_peer.json",
                  "machine_policy": "machine_policy_peer.json"}
    for batch in BATCHES:
        assigned = json.loads((ROOT / "knowledge/research/assignments" / (batch + ".json")).read_text())
        report = json.loads((ROOT / "knowledge/research/reviews" / peer_names[batch]).read_text())
        assigned_paths = {row["path"].casefold() for row in assigned["nodes"]}
        reviewed_paths = {path.casefold() for path in report["reviewed_paths"]}
        if reviewed_paths != assigned_paths:
            raise ValueError(batch + " peer review does not cover its exact assignment")
        if reviewed & reviewed_paths:
            raise ValueError("peer review assignments overlap")
        reviewed |= reviewed_paths
        peer_review_counts[batch] = len(reviewed_paths)
    node_paths = {node["path"].casefold() for node in data["nodes"]}
    if reviewed != node_paths:
        raise ValueError("peer reviews do not cover every graph node")
    source_ages = []
    reviewed_sources = set()
    for row in source_reviews["sources"]:
        reviewed_sources.add(urldefrag(row["url"])[0])
        for review in row["reviews"]:
            checked = datetime.strptime(review["checked_on"], "%Y-%m-%d").date()
            if checked > as_of_date:
                raise ValueError("source review date is later than audit date")
            source_ages.append((as_of_date - checked).days)
    cited_sources = {urldefrag(url)[0] for node in data["nodes"] for url in node["explanation_sources"]}
    cited_sources |= {urldefrag(url)[0] for edge in data["semantic_edges"] for url in edge["sources"]}
    if not cited_sources <= reviewed_sources:
        raise ValueError("some cited sources lack a reviewed-source record")
    semantics = json.loads(semantics_path.read_text(encoding="utf-8"))
    semantics_reviews = {urldefrag(row["url"])[0]: row for row in semantics["source_reviews"]}
    semantics_sources = {
        urldefrag(url)[0]
        for principle in semantics["principles"]
        for url in principle.get("sources", [])
    } | {urldefrag(provider["source"])[0] for provider in semantics["providers"]}
    if semantics_sources != set(semantics_reviews):
        raise ValueError("provider interpretation sources and reviews differ")
    for row in semantics_reviews.values():
        checked = datetime.strptime(row["checked_on"], "%Y-%m-%d").date()
        if checked > as_of_date:
            raise ValueError("provider source review date is later than audit date")
        source_ages.append((as_of_date - checked).days)
    rows = [json.loads(line) for line in (model_path / "node-records.jsonl").read_text().splitlines()]
    family_splits = {}
    for row in rows:
        family_splits.setdefault(row["split_family"], set()).add(row["split"])
    if any(len(splits) != 1 for splits in family_splits.values()):
        raise ValueError("a model split family crosses partitions")
    node_index = json.loads((model_path / "graph/node-index.json").read_text())
    for edge in json.loads((model_path / "graph/train-edge-index.json").read_text()):
        if node_index[edge["source"]]["split"] != "train" or node_index[edge["target"]]["split"] != "train":
            raise ValueError("train edge includes a held-out endpoint")
    evaluation = validate_evaluation(ROOT / "evaluation")
    forbidden_node_fields = {"event_id", "event", "trace", "malicious_example", "benign_example", "attack_id"}
    if any(forbidden_node_fields & set(node) or node["candidate_tags"] for node in data["nodes"]):
        raise ValueError("knowledge nodes contain event instances or unreviewed tags")
    metrics = {"nodes": len(data["nodes"]), "hierarchy_edges": len(data["edges"]),
               "semantic_edges": len(data["semantic_edges"]),
               "status_counts": dict(Counter(node["status"] for node in data["nodes"])),
               "scopes": dict(Counter(node["research"]["scope"] for node in data["nodes"])),
               "template_dependent_nodes": sum(node["template_dependent"] for node in data["nodes"]),
               "placeholder_nodes": sum(node["is_placeholder"] for node in data["nodes"]),
               "reviewed_source_pages": len(reviewed_sources),
               "provider_source_pages": len(semantics_reviews),
               "max_source_review_age_days": max(source_ages, default=0),
               "peer_reviewed_nodes": peer_review_counts,
               "model_records": len(rows),
               "sft_examples": sum(len((model_path / "sft" / (split + ".jsonl")).read_text(
                   encoding="utf-8").splitlines()) for split in ("train", "validation", "test")),
               "evaluation_cases": evaluation["cases"]}
    artifacts = [catalog_path, inventory_path, vault_path / "kg.json", vault_path / "manifest.json",
                 model_path / "manifest.json", ROOT / "evaluation/evaluation-manifest.json",
                 ROOT / "evaluation/rubric.json", semantics_path]
    return {"schema": "registry-research-audit-1", "as_of": as_of,
            "result": "valid_for_declared_research_scope", "metrics": metrics,
            "checks": {"assembly_matches": True, "vault": validate_vault(vault_path),
                       "model_data": validate_model_data(graph, model_path), "evaluation": evaluation,
                       "all_nodes_researched": all(node["research"] and node["status"] != "pending" for node in data["nodes"]),
                       "all_citations_reviewed": True, "peer_review_exact_coverage": True,
                       "family_split_isolation": True, "train_edges_have_train_endpoints": True,
                       "no_event_instances_or_unreviewed_tags": True},
            "artifact_sha256": {str(path.relative_to(ROOT)): _sha(path) for path in artifacts},
            "research_limits": [
                "The inventory is a cross-version documentation sample, not a complete Windows baseline or live-host snapshot.",
                "Structural nodes are explicit inferences from documented descendants.",
                "Template matches are candidate schema matches and do not prove a concrete key exists.",
                "The NT-native adapter maps documented roots only and never guesses HKCU, value boundaries or Registry views.",
                "Family splits reduce direct concept leakage but remain a small transductive pilot with shared ancestors and sources.",
                "The authored evaluation is synthetic and not an independent real-log benchmark.",
                "The synthesis is AI-authored and agent-reviewed, not independent human annotation or measured model performance."],
            "refresh_policy": "Re-run source review when max_source_review_age_days exceeds the study's protocol or before a time-sensitive release."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    report = audit(args.as_of)
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        _atomic_write(args.output, text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
