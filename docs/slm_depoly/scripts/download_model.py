"""Download an immutable HF snapshot and hash it; run on the deployment host."""

import argparse
import hashlib
import json
import re
from pathlib import Path


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="Qwen/Qwen3.5-27B")
    parser.add_argument("--revision", default="main")
    parser.add_argument("--dest", required=True, type=Path,
                        help="Separate directory for this model/revision; interrupted downloads can resume")
    args = parser.parse_args()
    from huggingface_hub import HfApi, snapshot_download

    dest = args.dest.expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)
    request_path = dest / "download-request.json"
    if request_path.exists():
        request = json.loads(request_path.read_text())
        if request["repo"] != args.repo or request["requested_revision"] != args.revision:
            raise SystemExit("Use another --dest for a different repo or requested revision")
    else:
        if any(dest.iterdir()):
            raise SystemExit("Destination must be empty or contain this script's download-request.json")
        revision = HfApi().model_info(args.repo, revision=args.revision).sha
        if not revision or not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise SystemExit("Hub did not return a full commit SHA")
        request = {"repo": args.repo, "requested_revision": args.revision, "revision": revision}
        with request_path.open("x") as stream:
            json.dump(request, stream, indent=2)
            stream.write("\n")

    model_dir = dest / "model"
    snapshot_download(repo_id=request["repo"], revision=request["revision"], local_dir=model_dir)
    files = {}
    for path in sorted(model_dir.rglob("*")):
        relative = path.relative_to(model_dir)
        if path.is_file() and ".cache" not in relative.parts:
            files[str(relative)] = {"bytes": path.stat().st_size, "sha256": file_hash(path)}
    if "config.json" not in files or not any(name.endswith(".safetensors") for name in files):
        raise SystemExit("Expected a Transformers config and safetensors weights")
    manifest = {"schema": "slm-model-lock-1", **request, "model_dir": str(model_dir), "files": files}
    lock = dest / "model.lock.json"
    if lock.exists():
        if json.loads(lock.read_text()) != manifest:
            raise SystemExit("Snapshot differs from existing lock; inspect it, do not silently overwrite")
    else:
        with lock.open("x") as stream:
            json.dump(manifest, stream, indent=2)
            stream.write("\n")
    print(json.dumps({"repo": request["repo"], "revision": request["revision"],
                      "model_dir": str(model_dir), "lock": str(lock), "files": len(files)}))


if __name__ == "__main__":
    main()
