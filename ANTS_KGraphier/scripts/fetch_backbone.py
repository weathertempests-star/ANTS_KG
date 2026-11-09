"""Fetch only the pinned research dependency; do not change existing checkouts."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from ants_kgraphier.backbone import MODEL_SHA256, UPSTREAM_COMMIT
from ants_kgraphier.io import digest

target = root / "vendor/ProvG-Searcher"
if not target.exists():
    subprocess.run(["git", "clone", "https://github.com/EnesAltinisik/ProvG-Searcher.git", str(target)], check=True)
    subprocess.run(["git", "-C", str(target), "checkout", "--detach", UPSTREAM_COMMIT], check=True)
head = subprocess.check_output(["git", "-C", str(target), "rev-parse", "HEAD"], text=True).strip()
if head != UPSTREAM_COMMIT or digest(target / "common/models.py") != MODEL_SHA256:
    raise SystemExit("Existing upstream checkout differs; refusing to overwrite it")
print(head)
