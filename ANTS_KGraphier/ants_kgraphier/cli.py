import argparse
import json
from pathlib import Path

from .io import jsonl, write_json

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent


def main(argv=None):
    parser = argparse.ArgumentParser(description="Registry subgraph extraction and analyst retrieval")
    parser.add_argument("--kg", type=Path, default=REPO / "artifacts/knowledge-vault/kg.json")
    parser.add_argument("--vendor", type=Path, default=ROOT / "vendor/ProvG-Searcher")
    subs = parser.add_subparsers(dest="command", required=True)
    p = subs.add_parser("ingest")
    p.add_argument("--data", type=Path, default=REPO / "data")
    p.add_argument("--sources", type=Path, default=ROOT / "configs/sources.json")
    p.add_argument("--output", type=Path, required=True)
    p = subs.add_parser("extract")
    p.add_argument("--store", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--splits", type=Path, default=ROOT / "configs/splits.json")
    p.add_argument("--per-recording", type=int, default=400, help="0 extracts every Registry anchor")
    p.add_argument("--prefix", help="Exhaustive query-conditioned extraction; requires --operation")
    p.add_argument("--operation")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--method", choices=["window", "temporal", "trec"], default="temporal")
    p.add_argument("--mode", choices=["offline", "past"], default="offline")
    p.add_argument("--hops", type=int, default=2)
    p.add_argument("--fanout", type=int, default=8)
    p.add_argument("--budget", type=int, default=33)
    p = subs.add_parser("validate")
    p.add_argument("--store", type=Path, required=True)
    p.add_argument("--graphs", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p = subs.add_parser("train")
    p.add_argument("--graphs", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--epochs", type=int, default=10)
    p.add_argument("--pairs", type=int, default=600)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--no-kg", action="store_true")
    for command in ("index", "evaluate", "search"):
        p = subs.add_parser(command)
        p.add_argument("--graphs", type=Path, required=True)
        p.add_argument("--model", type=Path, required=True)
        p.add_argument("--output", type=Path, required=True)
        if command != "index":
            p.add_argument("--index", type=Path, required=True)
        if command == "evaluate":
            p.add_argument("--queries", type=int, default=40)
            p.add_argument("--gallery-size", type=int, default=500)
        if command == "search":
            group = p.add_mutually_exclusive_group(required=True)
            group.add_argument("--query", type=Path)
            group.add_argument("--prefix")
            p.add_argument("--operation", default="RegSetValue")
            p.add_argument("--topk", type=int, default=10)
            p.add_argument("--shortlist", type=int, default=100)
    p = subs.add_parser("trace")
    p.add_argument("--store", type=Path, required=True)
    p.add_argument("--recording", required=True, help="source SHA-256")
    p.add_argument("--row", type=int, required=True, help="zero-based parsed event ordinal")
    p.add_argument("--data", type=Path, default=REPO / "data")
    p.add_argument("--output", type=Path, required=True)
    p = subs.add_parser("render")
    p.add_argument("--result", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    from .knowledge import Knowledge
    from .store import connect, ingest, recordings
    from .extract import export_candidates, validate_graph
    result = None
    if args.command == "ingest":
        result = ingest(args.data, json.loads(args.sources.read_text()), args.output)
    elif args.command == "extract":
        with connect(args.store) as db:
            settings = dict(method=args.method, hops=args.hops, fanout=args.fanout,
                            budget=args.budget, mode=args.mode)
            if bool(args.prefix) != bool(args.operation):
                parser.error("--prefix and --operation must be supplied together")
            if args.prefix:
                from .extract import export_query_candidates
                result = export_query_candidates(db, Knowledge(args.kg), args.output,
                    json.loads(args.splits.read_text()), args.prefix, args.operation, **settings)
            else:
                result = export_candidates(db, Knowledge(args.kg), args.output,
                                           json.loads(args.splits.read_text()), args.per_recording, args.seed, **settings)
    elif args.command == "validate":
        kg = Knowledge(args.kg)
        count = 0
        groups = {}
        with connect(args.store) as db:
            authoritative_groups = {r["store_id"]: r["dependency_group"] for r in recordings(db)}
            for graph in jsonl(args.graphs):
                validate_graph(graph, db, kg)
                group, split = graph["dependency_group"], graph["split"]
                if group != authoritative_groups[graph["recording_sha256"]]:
                    raise ValueError("candidate dependency group differs from source manifest")
                if split not in {"train", "validation", "test"}:
                    raise ValueError("unrecognized split")
                if group in groups and groups[group] != split:
                    raise ValueError("dependency group spans splits")
                groups[group] = split
                count += 1
        result = {"validated": count, "dependency_groups": groups, "kg_sha256": kg.sha256}
        write_json(args.output, result)
    elif args.command == "train":
        from .retrieval import train
        result = train(args.graphs, Knowledge(args.kg), args.vendor, args.output,
                       epochs=args.epochs, pairs=args.pairs, seed=args.seed, use_kg=not args.no_kg)
    elif args.command == "index":
        from .retrieval import build_index
        result = build_index(args.graphs, args.model, args.vendor, args.output)
    elif args.command == "evaluate":
        from .retrieval import evaluate
        result = evaluate(args.graphs, args.model, args.index, args.vendor, args.output,
                          query_count=args.queries, gallery_size=args.gallery_size)
    elif args.command == "search":
        from .analyst import functional_query, search
        kg = Knowledge(args.kg)
        config = json.loads((args.model / "model.json").read_text())
        if config["kg_sha256"] != kg.sha256:
            raise ValueError("query KG snapshot differs from model")
        query = json.loads(args.query.read_text()) if args.query else functional_query(kg, args.prefix, args.operation)
        report = search(args.graphs, args.model, args.index, args.vendor, query, args.output, args.topk, args.shortlist)
        result = {"matches": len(report["results"]), "output": str(args.output)}
    elif args.command == "trace":
        from .analyst import trace
        with connect(args.store) as db:
            result = trace(db, args.recording, args.row, args.data)
        write_json(args.output, result)
        result = {"source": result["source"], "row": args.row, "verified": True}
    elif args.command == "render":
        from .analyst import render
        render(args.result, args.output)
        result = {"output": str(args.output)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
