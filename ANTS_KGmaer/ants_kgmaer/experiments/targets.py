"""One target iterator shared by execution and independent evaluation."""

from pathlib import Path

from ..common.files import jsonl


def selected_targets(selection, config):
    count = 0
    for target in jsonl(Path(selection) / "targets.jsonl"):
        if config.get("split") and target["split"] != config["split"]:
            continue
        if config.get("engineering_limit") and count >= config["engineering_limit"]:
            break
        count += 1
        yield target
