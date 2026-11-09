"""Pair generation, exact verification and learned order-embedding retrieval."""
from collections import Counter
import copy
from pathlib import Path
import random
import time

from .backbone import Features, make_model, MODEL_SHA256, UPSTREAM_COMMIT
from .extract import symbolic
from .io import digest, fingerprint, jsonl, write_json


def nxgraph(graph):
    import networkx as nx
    result = nx.DiGraph()
    for key, node in graph["nodes"].items():
        result.add_node(key, **node)
    for a, b, relation in graph["edges"]:
        result.add_edge(a, b, relation=relation)
    return result


def contains(target, query):
    """Typed directed subgraph monomorphism; target may have extra edges.

    Query KG requirements are a subset of target annotations. Anchor matching
    pins the query to the candidate Registry operation. No labels are used.
    """
    from networkx.algorithms.isomorphism import DiGraphMatcher
    def match(a, b):
        return (a["kind"] == b["kind"] and a["operation"] == b["operation"]
                and a["anchor"] == b["anchor"]
                and set(b["knowledge"]).issubset(a["knowledge"]))
    return DiGraphMatcher(target, query, node_match=match,
                          edge_match=lambda a, b: a["relation"] == b["relation"]).subgraph_is_monomorphic()


def subset_query(graph, rng, max_events=3):
    full = symbolic(graph)
    events = {e["row"]: e for e in graph["events"]}
    selected = {graph["anchor_row"]}
    options = sorted(set(events) - selected)
    rng.shuffle(options)
    # Expand a connected event set. This is synthetic containment supervision,
    # not a claim of analyst relevance or a complete attack chain.
    while len(selected) < max_events:
        entities = {events[i][k] for i in selected for k in ("src", "dst")}
        candidate = next((i for i in options if i not in selected and
                          (events[i]["src"] in entities or events[i]["dst"] in entities)), None)
        if candidate is None:
            break
        selected.add(candidate)
    names = {"event:" + str(i) for i in selected}
    names.update(events[i][k] for i in selected for k in ("src", "dst"))
    return {"nodes": {k: v for k, v in full["nodes"].items() if k in names},
            "edges": [e for e in full["edges"] if e[0] in names and e[1] in names]}


def train(graph_path, knowledge, vendor, output, epochs=10, pairs=600,
          seed=7, hidden=32, layers=2, use_kg=True):
    import torch
    from torch_geometric.data import Batch
    torch.set_num_threads(2)
    torch.manual_seed(seed)
    rng = random.Random(seed)
    output = Path(output)
    if min(epochs, pairs, hidden, layers) < 1:
        raise ValueError("training parameters must be positive")
    if output.exists():
        raise FileExistsError(output)
    graphs = [g for g in jsonl(graph_path) if g["split"] == "train"]
    if len(graphs) < 2:
        raise ValueError("at least two training candidates required")
    if any(g["kg_sha256"] != knowledge.sha256 for g in graphs):
        raise ValueError("KG snapshot differs")
    syms = [symbolic(g) for g in graphs]
    nx = [nxgraph(g) for g in syms]
    features = Features(knowledge.nodes, {e["op"] for g in graphs for e in g["events"]}, use_kg)
    tensors = [features.encode(s) for s in syms]
    training = []
    attempted = 0
    start = time.perf_counter()
    for _ in range(pairs):
        idx = rng.randrange(len(graphs))
        query = subset_query(graphs[idx], rng)
        nq = nxgraph(query)
        tq = features.encode(query)
        training.append((idx, tq, 1))
        for neg in rng.sample(range(len(graphs)), min(30, len(graphs))):
            attempted += 1
            if not contains(nx[neg], nq):
                training.append((neg, tq, 0))
                break
    if not any(p[2] == 0 for p in training):
        raise ValueError("no verified negative pairs")
    model = make_model(vendor, features.dim, hidden, layers)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
    losses = []
    for epoch in range(epochs):
        model.train()
        rng.shuffle(training)
        total = 0.0
        for start_idx in range(0, len(training), 32):
            chunk = training[start_idx:start_idx + 32]
            targets = Batch.from_data_list([tensors[i] for i, _, _ in chunk])
            queries = Batch.from_data_list([q for _, q, _ in chunk])
            labels = torch.tensor([label for _, _, label in chunk])
            optimizer.zero_grad()
            result = model(model.emb_model(targets), model.emb_model(queries))
            loss = model.criterion(result, labels) / len(chunk)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            total += float(loss.detach()) * len(chunk)
        losses.append(total / len(training))
        print({"epoch": epoch + 1, "loss": losses[-1]}, flush=True)
    output.mkdir(parents=True)
    config = {"features": features.config(), "hidden": hidden, "layers": layers,
              "seed": seed, "epochs": epochs, "upstream_commit": UPSTREAM_COMMIT,
              "upstream_model_sha256": MODEL_SHA256, "kg_sha256": knowledge.sha256,
              "graphs_sha256": digest(graph_path),
              "training_groups": sorted({g["dependency_group"] for g in graphs}),
              "training_graphs": len(graphs), "pairs": len(training),
              "negative_checks": attempted, "losses": losses,
              "seconds": time.perf_counter() - start,
              "supervision": "synthetic containment; exact verified negatives; no malicious labels"}
    torch.save(model.state_dict(), output / "weights.pt")
    config["weights_sha256"] = digest(output / "weights.pt")
    write_json(output / "model.json", config)
    return config


def load_model(directory, vendor):
    import json
    import torch
    directory = Path(directory)
    config = json.loads((directory / "model.json").read_text())
    if config["upstream_commit"] != UPSTREAM_COMMIT or config["upstream_model_sha256"] != MODEL_SHA256:
        raise ValueError("checkpoint was built with another upstream backbone")
    if digest(directory / "weights.pt") != config["weights_sha256"]:
        raise ValueError("checkpoint integrity failure")
    model = make_model(vendor, Features(**config["features"]).dim, config["hidden"], config["layers"])
    model.load_state_dict(torch.load(directory / "weights.pt", map_location="cpu", weights_only=True))
    model.eval()
    return model, Features(**config["features"]), config


def embeddings(model, features, graphs):
    import torch
    from torch_geometric.data import Batch
    with torch.no_grad():
        chunks = []
        for i in range(0, len(graphs), 64):
            batch = Batch.from_data_list([features.encode(g) for g in graphs[i:i + 64]])
            chunks.append(model.emb_model(batch))
        return torch.cat(chunks) if chunks else torch.empty((0, 0))


def build_index(graph_path, model_dir, vendor, output):
    import numpy as np
    import torch
    torch.set_num_threads(2)
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    model, features, config = load_model(model_dir, vendor)
    graphs = list(jsonl(graph_path))
    if not graphs or any(g["kg_sha256"] != config["kg_sha256"] for g in graphs):
        raise ValueError("empty candidates or mismatched KG")
    start = time.perf_counter()
    vectors = embeddings(model, features, [symbolic(g) for g in graphs]).numpy()
    output.mkdir(parents=True)
    np.save(output / "embeddings.npy", vectors)
    write_json(output / "ids.json", [g["id"] for g in graphs])
    manifest = {"schema": "kgraphier-index-1", "count": len(graphs),
                "dimension": vectors.shape[1], "seconds": time.perf_counter() - start,
                "graphs_sha256": digest(graph_path), "weights_sha256": config["weights_sha256"],
                "embeddings_sha256": digest(output / "embeddings.npy"),
                "ids_sha256": digest(output / "ids.json"),
                "kg_sha256": config["kg_sha256"],
                "ranking": "ascending sum(relu(query-target)^2); exact vector scan"}
    write_json(output / "manifest.json", manifest)
    return manifest


def score_vectors(targets, query):
    import numpy as np
    return np.square(np.maximum(0, query - targets)).sum(axis=1)


def feature_counts(graph):
    return Counter((n["kind"], n["operation"], k) for n in graph["nodes"].values()
                   for k in (n["knowledge"] or [""]))


def evaluate(graph_path, model_dir, index_dir, vendor, output, query_count=40, gallery_size=500, seed=91):
    """Held-out structural retrieval benchmark, not human relevance evaluation."""
    import json
    import numpy as np
    import torch
    torch.set_num_threads(2)
    output = Path(output)
    if min(query_count, gallery_size) < 1:
        raise ValueError("query and gallery sizes must be positive")
    if output.exists():
        raise FileExistsError(output)
    model, features, config = load_model(model_dir, vendor)
    graphs = list(jsonl(graph_path))
    index_dir = Path(index_dir)
    manifest = json.loads((index_dir / "manifest.json").read_text())
    for name, key in [("embeddings.npy", "embeddings_sha256"), ("ids.json", "ids_sha256")]:
        if digest(index_dir / name) != manifest[key]:
            raise ValueError("index integrity failure")
    if manifest["graphs_sha256"] != digest(graph_path) or manifest["weights_sha256"] != config["weights_sha256"]:
        raise ValueError("index/model/candidates mismatch")
    ids = json.loads((index_dir / "ids.json").read_text())
    if ids != [g["id"] for g in graphs]:
        raise ValueError("index ordering mismatch")
    all_vectors = np.load(index_dir / "embeddings.npy", allow_pickle=False)
    eligible = [i for i, g in enumerate(graphs) if g["split"] == "test"]
    if any(graphs[i]["dependency_group"] in config["training_groups"] for i in eligible):
        raise ValueError("test dependency group leaked into training")
    rng = random.Random(seed)
    gallery = sorted(rng.sample(eligible, min(gallery_size, len(eligible))))
    if not gallery:
        raise ValueError("no held-out gallery")
    syms = [symbolic(graphs[i]) for i in gallery]
    nx = [nxgraph(s) for s in syms]
    counts = [feature_counts(s) for s in syms]
    vectors = all_vectors[gallery]
    sources = rng.sample(range(len(gallery)), min(query_count, len(gallery)))
    reports = []
    for source in sources:
        query = subset_query(graphs[gallery[source]], rng)
        nq = nxgraph(query)
        start = time.perf_counter()
        relevant = [i for i, target in enumerate(nx) if contains(target, nq)]
        exact_seconds = time.perf_counter() - start
        if source not in relevant:
            raise AssertionError("generated query not contained in source")
        start = time.perf_counter()
        vector = embeddings(model, features, [query]).numpy()[0]
        encoding_seconds = time.perf_counter() - start
        start = time.perf_counter()
        scores = score_vectors(vectors, vector)
        order = np.argsort(scores, kind="stable").tolist()
        vector_seconds = time.perf_counter() - start
        qc = feature_counts(query)
        baseline = sorted(range(len(gallery)), key=lambda i: sum((qc - counts[i]).values()))
        methods = {}
        for name, ranking in [("provg_order", order), ("feature_count", baseline)]:
            row = {}
            for k in (1, 5, 10, 50):
                top = ranking[:k]
                hits = len(set(top) & set(relevant))
                row[f"recall@{k}"] = hits / len(relevant)
                row[f"precision@{k}"] = hits / len(top)
            row["reciprocal_rank"] = 1 / (next(j for j, i in enumerate(ranking) if i in relevant) + 1)
            methods[name] = row
        reports.append({"source_id": graphs[gallery[source]]["id"], "query": query,
                        "relevant_count": len(relevant), "methods": methods,
                        "exact_seconds": exact_seconds, "query_encoding_seconds": encoding_seconds,
                        "vector_scan_seconds": vector_seconds,
                        "top10": [{"id": graphs[gallery[i]]["id"], "order_violation": float(scores[i]),
                                   "verified_match": i in relevant} for i in order[:10]]})
    summary = {}
    for method in ("provg_order", "feature_count"):
        summary[method] = {metric: sum(r["methods"][method][metric] for r in reports) / len(reports)
                           for metric in reports[0]["methods"][method]}
    result = {"schema": "kgraphier-retrieval-eval-1", "seed": seed,
              "gallery_size": len(gallery), "query_count": len(reports),
              "gallery_ids": [graphs[i]["id"] for i in gallery], "summary": summary,
              "queries": reports, "index_manifest": manifest,
              "limitations": ["Synthetic held-out containment queries, not analyst relevance labels.",
                              "The source candidate remains in the gallery; this is containment retrieval, not novel-behavior discovery.",
                              "Candidate anchors are sampled, not all Registry events.",
                              "No maliciousness classification or clinical-style sensitivity claim."]}
    write_json(output, result)
    return {"summary": summary, "gallery_size": len(gallery), "query_count": len(reports)}
