"""Bounded event-centred, overlapping windows and temporal ego graphs."""
from collections import defaultdict
import json
from pathlib import Path
import random
import time

from .io import canonical, fingerprint, write_json
from .store import event, recordings


def neighbors(db, rec, node, order, direction, limit):
    """Nearest events by ordinal position, not elapsed time. Exclude ties."""
    sign, sort = ("<", "DESC") if direction == "before" else (">", "ASC")
    found = {}
    for column in ("src", "dst"):
        sql = (f"SELECT * FROM events WHERE rec=? AND {column}=? AND ord {sign} ? "
               f"ORDER BY ord {sort},row {sort} LIMIT ?")
        for row in db.execute(sql, (rec, node, order, limit)):
            found[row["row"]] = dict(row)
    # Rank by order only; row breaks ties deterministically for budget selection,
    # never creates a PRECEDES edge between tied events.
    return sorted(found.values(), key=lambda r: (
        -r["ord"] if direction == "before" else r["ord"],
        -r["row"] if direction == "before" else r["row"]))[:limit]


def extract(db, rec, row, knowledge, method="temporal", hops=2,
            fanout=8, budget=33, mode="offline"):
    if method not in {"window", "temporal", "trec"} or mode not in {"offline", "past"}:
        raise ValueError("unsupported extractor or mode")
    if min(hops, fanout, budget) < 1:
        raise ValueError("hops, fanout and budget must be positive")
    anchor = event(db, rec, row)
    if anchor["dst_type"] != "Registry":
        raise ValueError("anchor must be a Registry operation event")
    selected = {row: anchor}
    reasons = {row: {"reason": "anchor", "parent_row": None, "direction": "anchor", "hop": 0}}
    directions = ["before", "after"] if mode == "offline" else ["before"]
    clipped = False
    diagnostics = None
    if method == "trec":
        from .trec import sample
        selected, reasons, diagnostics = sample(db, rec, anchor, hops, fanout, budget, mode)
        clipped = bool(diagnostics["budget_truncated"] or diagnostics["fanout_truncations"])
    elif anchor["ord"] is not None:
        frontier = [(anchor["src"], anchor["ord"], row, d) for d in directions]
        if method == "temporal":
            frontier += [(anchor["dst"], anchor["ord"], row, d) for d in directions]
        visited = set()
        for hop in range(1, (hops if method == "temporal" else 1) + 1):
            following = []
            for node, boundary, parent, direction in frontier:
                state = (node, boundary, direction)
                if state in visited:
                    continue
                visited.add(state)
                candidates = neighbors(db, rec, node, boundary, direction, fanout + 1)
                clipped |= len(candidates) > fanout
                for candidate in candidates[:fanout]:
                    rid = candidate["row"]
                    if rid not in selected:
                        if len(selected) >= budget:
                            clipped = True
                            continue
                        selected[rid] = candidate
                        reasons[rid] = {"reason": "shared_endpoint", "via": node,
                                        "parent_row": parent, "direction": direction, "hop": hop}
                    if method == "temporal":
                        for endpoint in (candidate["src"], candidate["dst"]):
                            following.append((endpoint, candidate["ord"], rid, direction))
            frontier = following
    events = []
    for rid in sorted(selected):
        item = dict(selected[rid])
        item["event_id"] = f"{rec}:{rid}"
        item["selection"] = reasons[rid]
        item["knowledge"] = knowledge.annotate(item["raw_key"], item["op"]) if item["dst_type"] == "Registry" else None
        events.append(item)
    settings = dict(method=method, hops=hops, fanout=fanout, budget=budget, mode=mode)
    graph = {"schema": "kgraphier-subgraph-1", "recording_sha256": rec,
             "anchor_row": row, "anchor_event_id": f"{rec}:{row}",
             "settings": settings, "kg_sha256": knowledge.sha256,
             "events": events, "budget_truncated": clipped,
             "order_unknown": anchor["ord"] is None}
    if diagnostics is not None:
        graph["sampling_diagnostics"] = diagnostics
    graph["id"] = fingerprint([rec, row, settings, knowledge.sha256] +
                              ([diagnostics["policy_version"]] if diagnostics else []))
    return graph


def symbolic(graph):
    """Incidence graph: operation nodes preserve direction and parallel events.

    No IDs, names, times, row numbers or labels are features. Only symbolic
    types, operation categories, anchor flag and matched KG prefix IDs.
    """
    nodes, edges = {}, []
    by_actor = defaultdict(list)
    for e in graph["events"]:
        en = "event:" + str(e["row"])
        nodes[en] = {"kind": "Event", "operation": e["op"],
                     "anchor": e["row"] == graph["anchor_row"], "knowledge": []}
        for side in ("src", "dst"):
            nid = e[side]
            kg = e["knowledge"]["node_ids"] if side == "dst" and e.get("knowledge") else []
            old = nodes.get(nid)
            # The same raw target under uncertain value operations must not gain
            # a stronger annotation from another event in this subgraph.
            if old:
                kg = sorted(set(old["knowledge"]) & set(kg))
            nodes[nid] = {"kind": e[side + "_type"], "operation": "",
                          "anchor": False, "knowledge": kg}
        edges += [(e["src"], en, 0), (en, e["dst"], 1)]
        if e["ord"] is not None:
            by_actor[e["src"]].append(e)
    for events in by_actor.values():
        groups = defaultdict(list)
        for e in events:
            groups[e["ord"]].append(e)
        ordered = sorted(groups)
        for left, right in zip(ordered, ordered[1:]):
            for a in groups[left]:
                for b in groups[right]:
                    edges.append(("event:" + str(a["row"]), "event:" + str(b["row"]), 2))
    return {"nodes": nodes, "edges": edges}


def export_candidates(db, knowledge, output, splits, per_recording=400, seed=7, **settings):
    if per_recording < 0:
        raise ValueError("sample size must be nonnegative (zero means all)")
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    output.mkdir(parents=True)
    reports = []
    start = time.perf_counter()
    with (output / "graphs.jsonl").open("w") as f:
        for recording in recordings(db):
            rec = recording["store_id"]
            group = recording["dependency_group"]
            split = splits[group]  # Unknown groups fail closed.
            count = db.execute("SELECT count(*) FROM events WHERE rec=? AND dst_type='Registry'", (rec,)).fetchone()[0]
            sample = (set(random.Random(str(seed) + rec).sample(range(count), min(count, per_recording)))
                      if per_recording else None)
            n = clipped = total_events = 0
            matched = defaultdict(int)
            for index, item in enumerate(db.execute("SELECT row FROM events WHERE rec=? AND dst_type='Registry' ORDER BY row", (rec,))):
                if sample is not None and index not in sample:
                    continue
                graph = extract(db, rec, item[0], knowledge, **settings)
                graph.update(split=split, dependency_group=group,
                             inclusion_probability=min(count, per_recording) / count if per_recording else 1.0)
                f.write(canonical(graph) + "\n")
                n += 1
                clipped += graph["budget_truncated"]
                total_events += len(graph["events"])
                anchor = next(e for e in graph["events"] if e["row"] == graph["anchor_row"])
                matched[anchor["knowledge"]["match"]] += 1
            report = {"recording": recording["id"], "population": count, "sampled": n,
                      "split": split, "clipped": clipped, "events_in_graphs": total_events,
                      "anchor_coverage": dict(matched)}
            reports.append(report)
            print(canonical(report), flush=True)
    from .io import digest
    manifest = {"schema": "kgraphier-candidates-1", "recordings": reports,
                "settings": settings, "seed": seed, "per_recording": per_recording,
                "sampling": "uniform without replacement; zero sample size means exhaustive; label independent",
                "kg_sha256": knowledge.sha256, "seconds": time.perf_counter() - start,
                "graphs_sha256": digest(output / "graphs.jsonl"), "splits": splits}
    write_json(output / "manifest.json", manifest)
    return manifest


def export_query_candidates(db, knowledge, output, splits, prefix, operation, **settings):
    """Exhaustively extract anchors matching a functional condition.

    This is a separate, query-conditioned corpus, never a replacement for the
    unbiased sampled evaluation corpus. Retains benign matches intentionally.
    """
    from .knowledge import components
    node = knowledge.by_prefix.get(components(prefix))
    if node is None:
        raise ValueError("query prefix must be a concrete KG node")
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    output.mkdir(parents=True)
    counts = []
    start = time.perf_counter()
    with (output / "graphs.jsonl").open("w") as f:
        for recording in recordings(db):
            rec = recording["store_id"]
            n = scanned = 0
            for e in db.execute("SELECT row,raw_key FROM events WHERE rec=? AND dst_type='Registry' AND op=? ORDER BY row", (rec, operation)):
                scanned += 1
                if node["id"] not in knowledge.annotate(e["raw_key"], operation)["node_ids"]:
                    continue
                graph = extract(db, rec, e["row"], knowledge, **settings)
                graph.update(split=splits[recording["dependency_group"]],
                             dependency_group=recording["dependency_group"],
                             inclusion_probability=1.0, query_conditioned=True)
                f.write(canonical(graph) + "\n")
                n += 1
            counts.append({"recording": recording["id"], "operation_population": scanned, "matched_anchors": n})
    from .io import digest
    manifest = {"schema": "kgraphier-query-candidates-1", "prefix": prefix, "operation": operation,
                "recordings": counts, "settings": settings, "kg_sha256": knowledge.sha256,
                "seconds": time.perf_counter() - start, "graphs_sha256": digest(output / "graphs.jsonl"),
                "scope": "All matching operation anchors in all sources; conservative KG prefix semantics, no labels."}
    write_json(output / "manifest.json", manifest)
    return manifest


def validate_graph(graph, db, knowledge):
    """Re-extract from the authoritative event store and compare all evidence."""
    expected = extract(db, graph["recording_sha256"], graph["anchor_row"], knowledge, **graph["settings"])
    for key, value in expected.items():
        if graph.get(key) != value:
            raise ValueError("subgraph integrity mismatch: " + key)
    return True
