"""Reproducible local research run. Each output stage refuses replacement.

Run from any directory with this project's venv. Use a new --output for each
experiment. The shared immutable event store may be supplied with --store.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--store", type=Path, default=ROOT / "artifacts/events.sqlite")
    parser.add_argument("--per-recording", type=int, default=400)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--pairs", type=int, default=600)
    parser.add_argument("--queries", type=int, default=30)
    parser.add_argument("--gallery-size", type=int, default=300)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must be a new directory")
    args.output.mkdir(parents=True)
    commands = []
    def run(*command):
        cmd = [sys.executable, "-m", "ants_kgraphier", *map(str, command)]
        commands.append(cmd)
        (args.output / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
        subprocess.run(cmd, check=True, cwd=ROOT.parent)
    if not args.store.exists():
        run("ingest", "--output", args.store)
    for method in ("window", "temporal"):
        candidates = args.output / method
        run("extract", "--store", args.store, "--output", candidates,
            "--method", method, "--per-recording", args.per_recording)
        graphs = candidates / "graphs.jsonl"
        run("validate", "--store", args.store, "--graphs", graphs,
            "--output", candidates / "validation.json")
        for use_kg in (False, True):
            model = candidates / ("model-kg" if use_kg else "model-no-kg")
            cmd = ["train", "--graphs", graphs, "--output", model,
                   "--epochs", args.epochs, "--pairs", args.pairs]
            if not use_kg:
                cmd += ["--no-kg"]
            run(*cmd)
            index = model / "index"
            run("index", "--graphs", graphs, "--model", model, "--output", index)
            run("evaluate", "--graphs", graphs, "--model", model, "--index", index,
                "--output", model / "evaluation.json", "--queries", args.queries,
                "--gallery-size", args.gallery_size)


if __name__ == "__main__":
    main()
