"""Build a query-conditioned analyst demo without changing research evaluation."""
import argparse
from pathlib import Path

from ants_kgraphier.analyst import functional_query, render, search
from ants_kgraphier.extract import export_query_candidates
from ants_kgraphier.io import canonical, digest, jsonl, write_json
from ants_kgraphier.knowledge import Knowledge
from ants_kgraphier.retrieval import build_index
from ants_kgraphier.store import connect
import json

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--research", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--store", type=Path, default=ROOT / "artifacts/events.sqlite")
    args = p.parse_args()
    if args.output.exists():
        p.error("output must not already exist")
    args.output.mkdir(parents=True)
    kg = Knowledge(ROOT.parent / "artifacts/knowledge-vault/kg.json")
    prefix, operation = "HKLM\\SYSTEM\\CurrentControlSet\\Services", "RegSetValue"
    with connect(args.store) as db:
        export_query_candidates(db, kg, args.output / "targeted", json.loads((ROOT / "configs/splits.json").read_text()),
                                prefix, operation, method="temporal", hops=2, fanout=8, budget=33, mode="offline")
    paths = [args.research / "temporal/graphs.jsonl", args.output / "targeted/graphs.jsonl"]
    output = args.output / "graphs.jsonl"
    seen = set()
    with output.open("w") as f:
        for path in paths:
            for graph in jsonl(path):
                if graph["id"] not in seen:
                    seen.add(graph["id"])
                    f.write(canonical(graph) + "\n")
    write_json(args.output / "manifest.json", {"scope": "Demo union; not an unbiased evaluation corpus",
               "sources": [{"path": str(path), "sha256": digest(path)} for path in paths],
               "count": len(seen), "graphs_sha256": digest(output)})
    model = args.research / "temporal/model-kg"
    vendor = ROOT / "vendor/ProvG-Searcher"
    build_index(output, model, vendor, args.output / "index")
    search(output, model, args.output / "index", vendor, functional_query(kg, prefix, operation),
           args.output / "services.json", topk=10, shortlist=1000)
    render(args.output / "services.json", args.output / "services.html")


if __name__ == "__main__":
    main()
