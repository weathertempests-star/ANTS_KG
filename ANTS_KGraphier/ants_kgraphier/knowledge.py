"""Conservative prefix annotation. No guessed value boundary or template match."""
import json
from functools import lru_cache
from pathlib import Path

from .io import digest

HIVES = {"hklm": "hkey_local_machine", "hkcu": "hkey_current_user",
         "hku": "hkey_users", "hkcr": "hkey_classes_root", "hkcc": "hkey_current_config"}


def components(raw):
    parts = [p.casefold() for p in raw.split("\\") if p]
    if parts[:2] == ["registry", "machine"]:
        parts = ["hkey_local_machine"] + parts[2:]
    elif parts[:2] == ["registry", "user"]:
        parts = ["hkey_users"] + parts[2:]
    elif parts:
        parts[0] = HIVES.get(parts[0], parts[0])
    return tuple(parts)


class Knowledge:
    def __init__(self, path):
        self.path = Path(path)
        self.sha256 = digest(path)
        self.graph = json.loads(self.path.read_text())
        self.nodes = {n["id"]: n for n in self.graph["nodes"] if n["domain"] == "registry"}
        self.by_prefix = {tuple(n["canonical_components"]): n for n in self.nodes.values()
                          if not n.get("template_dependent")}

    @lru_cache(maxsize=100000)
    def annotate(self, raw, operation):
        parts = components(raw)
        # Value operation encoding is unconfirmed in the supplied recordings.
        # Prefixes before the last component are usable as conservative context;
        # a last-component hit remains a lexical candidate, not confirmed key identity.
        uncertain = "value" in operation.casefold()
        hits = [self.by_prefix[parts[:i]]["id"] for i in range(1, len(parts) + 1)
                if parts[:i] in self.by_prefix]
        usable = [nid for nid in hits if not uncertain or self.nodes[nid]["depth"] < len(parts)]
        return {"node_ids": usable, "lexical_node_ids": hits,
                "match": "unknown" if not usable else
                ("exact_key" if not uncertain and parts in self.by_prefix else "prefix_context"),
                "boundary": "unresolved" if uncertain else "key_path",
                "raw_target": raw, "canonical_components": list(parts),
                "template_matching": False}
