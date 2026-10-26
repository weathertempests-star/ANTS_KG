"""Deterministic Markdown projection of shared prefix knowledge, with guarded refresh."""

import hashlib
import html
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import quote

from .knowledge import KnowledgeBase, SCHEMA

FORMAT_VERSION = 3
RESERVED = ("kg.json", "INDEX.md", "REVIEW_QUEUE.md", "CONCEPTS.md", "manifest.json", "notes")


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def _hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def note_path(node_id):
    """Stable filename from the canonical prefix ID, never from display text."""
    if not re.fullmatch(r"knowledge:[0-9a-f]{24}", node_id):
        raise ValueError("invalid knowledge node ID")
    return "notes/" + node_id.replace(":", "-") + ".md"


def _safe(value):
    text = html.escape(str(value), quote=True)
    for character in "\\[]*_`|":
        text = text.replace(character, "&#" + str(ord(character)) + ";")
    return text.replace("\r", "").replace("\n", "<br>")


def _block(text):
    fence = "~" * max(3, max((len(s) for s in re.findall(r"~+", text)), default=0) + 1)
    return fence + "text\n" + text + "\n" + fence


def _link(node, within_note=False, full_path=False):
    target = note_path(node["id"])
    if within_note:
        target = Path(target).name
    return "[" + _safe(node["path"] if full_path else node["label"]) + "](" + target + ")"


def _source_lines(sources):
    return ["- [" + _safe(s) + "](<" + quote(s, safe=":/?#=&%+-._~") + ">)" for s in sources] or ["None recorded."]


def _node_lines(node, nodes, children, link):
    lines = ["# " + _safe(node["label"]), "", "## Full prefix", "", _block(node["path"]), "",
             "- Domain: " + node["domain"], "- Depth: L" + str(node["depth"]),
             "- Node ID: `" + node["id"] + "`", "",
             "## Hierarchy", "",
             "Parent: " + (link(nodes[node["parent_id"]]) if node["parent_id"] else "Root"), "", "Children:", ""]
    lines += ["- " + link(child) for child in children[node["id"]]] or ["None in this inventory."]
    lines += ["", "## Functional explanation", "", "Status: **" + node["status"] + "**", ""]
    if node["status"] != "pending":
        lines += ["Role: " + _safe(node["role"]), "", _safe(node["explanation"]), ""]
    else:
        lines += ["Pending research; the functional explanation and role are empty in the snapshot.", ""]
    research = node.get("research", {})
    if research:
        lines += ["## Atomic claim", "", _safe(research["summary"]), "",
                  "Scope: **" + research["scope"] + "**", "",
                  "## Meaning in system-level logs", "", _safe(research["log_context"]), "",
                  "### What the path cannot establish", ""]
        lines += ["- " + _safe(limit) for limit in research["cannot_infer"]]
        lines += ["", "### Applicability", "", _safe(research["applicability"]), ""]
        if research["value_semantics"]:
            lines += ["### Selected values and subkeys", "",
                      "These are documented examples, not an exhaustive schema or observed data.", ""]
            for value in research["value_semantics"]:
                label = '(unnamed value)' if value['kind'] == 'value' and value['name'] == '' else value['name']
                lines += ["- **" + _safe(label) + "** (" + value["kind"] + "): " + _safe(value["meaning"])]
        lines += ["", "### Claim-level evidence", ""]
        for evidence in research["evidence"]:
            lines += ["- **" + evidence["support"] + "** — " + _safe(evidence["claim"]),
                      "  Section: " + _safe(evidence["section"]) + "."]
            lines += ["  " + line for line in _source_lines([evidence["url"]])]
        lines.append("")
    if node.get("_semantic_links"):
        lines += ["## Related knowledge", "",
                  "Each relation has an explicit meaning; it does not assert identical keys or observed causation.", ""]
        for edge in node["_semantic_links"]:
            other_id = edge["target"] if edge["source"] == node["id"] else edge["source"]
            direction = "outgoing" if edge["source"] == node["id"] else "incoming"
            lines += ["- **" + edge["type"] + "** (" + direction + "): " + link(nodes[other_id]),
                      "  " + _safe(edge["explanation"])]
            lines += ["  " + line for line in _source_lines(edge["sources"])]
        lines.append("")
    lines += ["### Explanation sources", ""] + _source_lines(node["explanation_sources"])
    lines += ["", "## Path evidence", "",
              "These citations support the path or an ancestor prefix only; they do not establish its function.", "",
              "Explicitly listed in inventory: " + str(node["explicitly_listed"]).lower(), ""]
    lines += _source_lines(node["path_sources"])
    lines += ["", "## Templates and candidate tags", "",
              "- Placeholder component: " + str(node["is_placeholder"]).lower(),
              "- Template-dependent prefix: " + str(node["template_dependent"]).lower()]
    if node["template_dependent"]:
        lines += ["", "This prefix contains a placeholder or descends from one. Template matching is not implemented."]
    lines += ["", "Candidate tags: `[]`. Tagging has not been performed.", ""]
    return lines


def _structure(graph):
    nodes = {n["id"]: n for n in graph.to_dict()["nodes"]}
    children = {key: [] for key in nodes}
    for node in nodes.values():
        if node["parent_id"]:
            children[node["parent_id"]].append(node)
    for group in children.values():
        group.sort(key=lambda n: (n["domain"], n["canonical_components"]))
    for edge in graph.to_dict().get("semantic_edges", []):
        for endpoint in ("source", "target"):
            nodes[edge[endpoint]].setdefault("_semantic_links", []).append(edge)
    return nodes, children


def render_markdown(graph):
    nodes, children = _structure(graph)
    lines = ["# Shared Prefix Knowledge", "", "Generated from the shared snapshot; research belongs in the catalog.", ""]
    link = lambda n: "[" + _safe(n["label"]) + "](#" + n["id"].replace(":", "-") + ")"
    for node in nodes.values():
        lines += ['<a id="' + node["id"].replace(":", "-") + '"></a>', ""]
        lines += _node_lines(node, nodes, children, link)
    return "\n".join(lines) + "\n"


def render_vault(graph):
    """Return all generated files from one graph. This function never touches disk."""
    nodes, children = _structure(graph)
    snapshot = _json(graph.to_dict())
    files = {"kg.json": snapshot}
    index = ["# Registry Shared Knowledge Vault", "",
             "Generated from inventory paths and authored catalog explanations. Each full prefix has one shared note.", "",
             "Edit research in the catalog and rebuild. Keep personal notes in `personal/`, outside generated `notes/`.", "",
             "[Shared snapshot](kg.json) · [Review queue](REVIEW_QUEUE.md)", "",
             f"Nodes: {len(nodes)}. Parent-child edges: {len(graph.to_dict()['edges'])}. "
             f"Explained: {sum(n['status'] != 'pending' for n in nodes.values())}. "
             f"Pending: {sum(n['status'] == 'pending' for n in nodes.values())}.", "",
             "## Enter by hive / root", ""]

    def branch(node, depth):
        index.append("  " * depth + "- " + _link(node) + " — L" + str(node["depth"]) + "; " + node["status"])
        for child in children[node["id"]]:
            branch(child, depth + 1)

    for node in sorted(nodes.values(), key=lambda n: (n["domain"], n["canonical_components"])):
        if node["parent_id"] is None:
            branch(node, 0)
    if graph.to_dict()["schema"] == SCHEMA:
        index += ["", "[Concept connections](CONCEPTS.md)", "",
                  "Documented claims and structural inferences retain distinct status and evidence. A complete explanation does not establish an event outcome."]
        concepts = ["# Concept Connections", "",
                    "Navigate by related system concepts as well as registry ancestry. Relations are authored, sourced, and separate from parent-child edges.", ""]
        for edge in graph.to_dict().get("semantic_edges", []):
            concepts += ["- " + _link(nodes[edge["source"]], full_path=True) + " **" + edge["type"] + "** " + _link(nodes[edge["target"]], full_path=True),
                         "  " + _safe(edge["explanation"])]
            concepts += ["  " + line for line in _source_lines(edge["sources"])]
        files["CONCEPTS.md"] = "\n".join(concepts) + "\n"
    files["INDEX.md"] = "\n".join(index) + "\n"
    queue = ["# Functional Explanation Review Queue", "",
             "Only pending nodes appear here. Path evidence is not functional evidence; explanations remain empty until authored and sourced.", ""]
    bands = [("L1–L4", 1, 4), ("L5–L7", 5, 7), ("L8–L9", 8, 9)]
    if any(n["depth"] > 9 and n["status"] == "pending" for n in nodes.values()):
        bands.append(("L10+", 10, max(n["depth"] for n in nodes.values())))
    for label, low, high in bands:
        all_group = [n for n in nodes.values() if low <= n["depth"] <= high]
        pending = sorted((n for n in all_group if n["status"] == "pending"), key=lambda n: (n["depth"], n["canonical_components"]))
        queue += ["## " + label, "", f"{len(pending)} pending / {len(all_group)} total nodes.", ""]
        queue += ["- " + _link(n, full_path=True) + f" — L{n['depth']}" +
                  ("; placeholder" if n["is_placeholder"] else "; template descendant" if n["template_dependent"] else "") for n in pending]
        queue.append("")
    files["REVIEW_QUEUE.md"] = "\n".join(queue) + "\n"
    for node in nodes.values():
        lines = ["---", "node_id: " + json.dumps(node["id"]), "generated: true", "---", ""]
        lines += _node_lines(node, nodes, children, lambda n: _link(n, within_note=True))
        lines += ["[Index](../INDEX.md) · [Review queue](../REVIEW_QUEUE.md)", ""]
        files[note_path(node["id"])] = "\n".join(lines)
    schema = graph.to_dict()["schema"]
    manifest = {"format_version": FORMAT_VERSION if schema == SCHEMA else 2, "graph_schema": schema, "graph_sha256": _hash(snapshot),
                "files": {name: _hash(content) for name, content in sorted(files.items())}}
    files["manifest.json"] = _json(manifest)
    return files


def _check_paths(root):
    if root.is_symlink():
        raise ValueError("vault directory cannot be a symlink")
    for parent in root.parents:
        if parent.is_symlink():
            raise ValueError("vault parent cannot be a symlink")
    for name in RESERVED:
        path = root / name
        if path.is_symlink():
            raise ValueError("managed path cannot be a symlink: " + name)
    notes = root / "notes"
    if notes.exists():
        if not notes.is_dir():
            raise ValueError("notes must be a directory")
        if any(p.is_symlink() or not p.is_file() for p in notes.iterdir()):
            raise ValueError("notes must contain only generated regular files")


def _markdown_targets(text):
    """Read inline targets outside the generated fenced path blocks."""
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^(~{3,})", line)
        if marker:
            if fence is None:
                fence = marker.group(1)
            elif line.strip() == fence:
                fence = None
            continue
        if fence is None:
            yield from re.findall(r"\]\(([^)]+)\)", line)


def validate_vault(directory):
    """Re-render from JSON, detecting drift even if a file's manifest hash was edited."""
    root = Path(directory).absolute()
    _check_paths(root)
    graph = KnowledgeBase.load(root / "kg.json")
    expected = render_vault(graph)
    problems = []
    for name, content in expected.items():
        path = root / name
        if not path.is_file() or path.read_bytes() != content.encode("utf-8"):
            problems.append(name)
        if path.is_file() and name.endswith(".md"):
            for target in _markdown_targets(path.read_text(encoding="utf-8")):
                if target.startswith(("<https://", "https://")):
                    continue
                destination = (path.parent / target).resolve()
                if root.resolve() not in destination.parents or not destination.is_file():
                    problems.append(name + " -> broken generated link: " + target)
    extra = {"notes/" + p.name for p in (root / "notes").iterdir()} - set(expected) if (root / "notes").is_dir() else set()
    if problems or extra:
        raise ValueError("vault inconsistent; regenerate from canonical JSON into a new directory: " + ", ".join(sorted(set(problems) | extra)))
    return {"valid": True, "nodes": len(graph.to_dict()["nodes"]), "edges": len(graph.to_dict()["edges"]),
            "graph_sha256": _hash(expected["kg.json"]), "managed_files": len(expected)}


def _atomic_write(path, content):
    fd, temporary = tempfile.mkstemp(prefix=".ants-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def export_vault(graph, directory):
    """Create or refresh a consistent vault. Refuse to overwrite edited managed notes.

    Refresh is atomic per file, not per directory; a concurrent reader should call
    validate_vault and retry after a refresh. Personal files outside notes survive.
    """
    root = Path(directory).absolute()
    _check_paths(root)
    old_files = set()
    if (root / "manifest.json").exists():
        validate_vault(root)
        old_files = set(render_vault(KnowledgeBase.load(root / "kg.json")))
    elif any((root / name).exists() for name in RESERVED):
        raise ValueError("destination contains unmanaged reserved paths; choose a new vault directory")
    files = render_vault(graph)
    for name in set(files) - old_files:
        if (root / name).exists():
            raise ValueError("new generated file would overwrite an unmanaged path: " + name)
    root.mkdir(parents=True, exist_ok=True)
    (root / "notes").mkdir(exist_ok=True)
    for name, content in files.items():
        if name != "manifest.json":
            _atomic_write(root / name, content)
    for name in old_files - set(files):
        (root / name).unlink()
    _atomic_write(root / "manifest.json", files["manifest.json"])
    return validate_vault(root)
