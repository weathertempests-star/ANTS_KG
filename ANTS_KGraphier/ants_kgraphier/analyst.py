"""Functional queries, verified shortlist and standalone evidence rendering."""
import html
import json
from pathlib import Path
import time

from .extract import symbolic
from .io import digest, fingerprint, jsonl, rows, write_json
from .knowledge import components
from .retrieval import contains, embeddings, load_model, nxgraph, score_vectors
from .store import event, recordings


def functional_query(knowledge, prefix, operation):
    node = knowledge.by_prefix.get(components(prefix))
    if node is None:
        raise ValueError("query prefix must be an explicit concrete KG node")
    return {"nodes": {
        "process": {"kind": "Process", "operation": "", "anchor": False, "knowledge": []},
        "operation": {"kind": "Event", "operation": operation, "anchor": True, "knowledge": []},
        "registry": {"kind": "Registry", "operation": "", "anchor": False, "knowledge": [node["id"]]}},
        "edges": [("process", "operation", 0), ("operation", "registry", 1)]}


def search(graph_path, model_dir, index_dir, vendor, query, output, topk=10, shortlist=100):
    import numpy as np
    import torch
    torch.set_num_threads(2)
    if topk < 1 or shortlist < topk:
        raise ValueError("require 1 <= topk <= shortlist")
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    graphs = list(jsonl(graph_path))
    model, features, config = load_model(model_dir, vendor)
    index_dir = Path(index_dir)
    manifest = json.loads((index_dir / "manifest.json").read_text())
    if (manifest["graphs_sha256"] != digest(graph_path) or
            manifest["weights_sha256"] != config["weights_sha256"] or
            manifest["embeddings_sha256"] != digest(index_dir / "embeddings.npy") or
            manifest["ids_sha256"] != digest(index_dir / "ids.json")):
        raise ValueError("incompatible or modified index")
    if json.loads((index_dir / "ids.json").read_text()) != [g["id"] for g in graphs]:
        raise ValueError("index ID order mismatch")
    start = time.perf_counter()
    vector = embeddings(model, features, [query]).numpy()[0]
    matrix = np.load(index_dir / "embeddings.npy", allow_pickle=False)
    scores = score_vectors(matrix, vector)
    ranking = np.argsort(scores, kind="stable")[:shortlist]
    nq = nxgraph(query)
    selected, rejected, merged = [], 0, 0
    for i in ranking:
        graph = graphs[int(i)]
        if not contains(nxgraph(symbolic(graph)), nq):
            rejected += 1
            continue
        # Merge highly overlapping results only when the anchor operation and
        # raw Registry target agree. Preserve the omitted anchor IDs explicitly.
        anchor = next(e for e in graph["events"] if e["row"] == graph["anchor_row"])
        ids = {e["event_id"] for e in graph["events"]}
        duplicate = None
        for previous in selected:
            pa = previous["anchor"]
            prev_ids = {e["event_id"] for e in previous["graph"]["events"]}
            if (anchor["op"], anchor["raw_key"]) == (pa["op"], pa["raw_key"]) and len(ids & prev_ids) / len(ids | prev_ids) >= 0.8:
                duplicate = previous
                break
        if duplicate is not None:
            duplicate["merged_anchor_ids"].append(graph["anchor_event_id"])
            merged += 1
        else:
            selected.append({"id": graph["id"], "order_violation": float(scores[i]),
                             "verified_match": True, "anchor": anchor,
                             "merged_anchor_ids": [], "graph": graph})
    result = {"schema": "kgraphier-search-1", "query": query, "results": selected[:topk],
              "shortlist_checked": len(ranking), "rejected_by_exact_verifier": rejected,
              "merged_duplicates": merged, "seconds": time.perf_counter() - start,
              "index_manifest": manifest,
              "scope": "Approximate shortlist then exact typed structural verification; not a maliciousness score.",
              "completeness": "Only indexed sampled candidates searched; shortlist can miss matches."}
    write_json(output, result)
    return result


def trace(db, rec, row, data_root):
    stored = event(db, rec, row)
    source = next(r for r in recordings(db) if r["store_id"] == rec)
    path = Path(data_root) / source["path"]
    if digest(path) != rec:
        raise ValueError("raw source changed")
    for i, raw in enumerate(rows(path, source["format"])):
        if i == row:
            if fingerprint(raw) != stored["raw_sha"]:
                raise ValueError("raw event differs from indexed event")
            return {"source": source["path"], "source_sha256": rec,
                    "row_zero_based": row, "raw_sha256": stored["raw_sha"], "raw_event": raw}
    raise ValueError("source row missing")


def render(result_path, output):
    result = json.loads(Path(result_path).read_text())
    sections = []
    for rank, item in enumerate(result["results"], 1):
        rows_html = []
        for e in item["graph"]["events"]:
            fields = [e["row"], e["ord"], e["op"], e["src"], e["raw_key"] or e["dst"],
                      e["selection"], (e.get("knowledge") or {}).get("match", "")]
            rows_html.append("<tr>" + "".join("<td>" + html.escape(str(x)) + "</td>" for x in fields) + "</tr>")
        sections.append(f"<section><h2>{rank}. {html.escape(item['anchor']['raw_key'])}</h2>"
                        f"<p>Order violation: {item['order_violation']:.6g}; verified structural match. "
                        f"Anchor: {html.escape(item['graph']['anchor_event_id'])}</p>"
                        "<table><tr><th>Source row</th><th>Order reference</th><th>Operation</th><th>Actor</th>"
                        "<th>Target</th><th>Extraction reason</th><th>KG match</th></tr>" + "".join(rows_html) + "</table></section>")
    page = """<!doctype html><html lang="en"><meta charset="utf-8"><title>Registry investigation entry points</title>
    <style>body{font:15px system-ui;margin:2rem;background:#f7f8fa;color:#172b4d}section{background:white;padding:1rem;margin:1rem 0;overflow:auto}table{border-collapse:collapse}td,th{border:1px solid #ccc;padding:.4rem;max-width:32rem;overflow-wrap:anywhere}h1{font-size:1.7rem}</style>
    <h1>Registry investigation entry points</h1><p>These are relevant activity fragments, not malicious verdicts. Order references are not elapsed time. Equal values have unknown order.</p>"""
    page += "<pre>" + html.escape(json.dumps(result["query"], indent=2)) + "</pre>" + "".join(sections) + "</html>"
    if Path(output).exists():
        raise FileExistsError(output)
    Path(output).write_text(page)
