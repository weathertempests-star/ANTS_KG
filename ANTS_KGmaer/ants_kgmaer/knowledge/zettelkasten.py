"""Standalone human-readable shared-knowledge rendering, without event nodes."""

from html import escape
import json


def render_markdown(knowledge):
    graph = knowledge.to_dict()
    nodes = sorted(graph["nodes"], key=lambda n: (n["depth"], n["path"]))
    by_id = {node["id"]: node for node in nodes}
    children = {}
    for node in nodes:
        children.setdefault(node["parent_id"], []).append(node)
    def link(node):
        return '[' + node["path"].replace('[', r'\[').replace(']', r'\]') + '](#node-' + node["id"] + ')'
    lines = ["# Shared Registry knowledge", "",
             "This is functional path knowledge, not event interpretation or an attack classification.", "",
             f"Nodes: {len(nodes)}; hierarchy edges: {len(graph['edges'])}; semantic relations: {len(graph.get('semantic_edges', []))}.", "",
             "## Hive entry points", ""]
    lines += ["- " + link(node) for node in children.get(None, [])]
    for node in nodes:
        parent = by_id.get(node["parent_id"])
        lines += ["", '<a id="node-' + escape(node["id"], quote=True) + '"></a>', "",
                  "## " + node["path"], "", f"Level: {node['depth']}; explanation status: {node['status']}.", "",
                  "Parent: " + (link(parent) if parent else "Root"), "",
                  "Children: " + (", ".join(link(child) for child in children.get(node["id"], [])) or "None"), "",
                  "Template dependent: " + str(node["template_dependent"]).lower() + ".", "",
                  node["explanation"] or "No functional explanation supplied.", ""]
        for title, key in (("Functional explanation sources", "explanation_sources"), ("Path sources", "path_sources"),
                           ("Research scope and limits", "research")):
            lines += ["### " + title, "", "```json", json.dumps(node[key], ensure_ascii=False, indent=2), "```", ""]
    lines += ["## Semantic relations", "", "```json", json.dumps(graph.get("semantic_edges", []), ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)
