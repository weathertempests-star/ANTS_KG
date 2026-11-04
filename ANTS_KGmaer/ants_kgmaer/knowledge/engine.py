"""Shared knowledge snapshots and read-only contextual lookup."""
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from .constants import (SCHEMA, LEGACY_SNAPSHOT_SCHEMA, CATALOG_SCHEMA, DEFINITION_FIELDS,
                        RESEARCH_FIELDS, HIVES, NT_NATIVE_SOURCE, GUID_TEMPLATE_NAMES,
                        GUID_COMPONENT, SID_COMPONENT)
from .paths import _components, _identity, _template_bindings, split_input, adapt_registry_path
from .schema import _definition, _sources, _inventory_definitions

class KnowledgeBase:
    """A prefix graph: identity is domain + full canonical prefix, never event ID."""

    def __init__(self, definitions, provenance=None, relations=None, schema=None):
        if not isinstance(definitions, list):
            raise ValueError("definitions must be a list")
        # Ordinary inventory/catalog builds retain the pending-knowledge format.
        # Research extensions opt in through their data or an explicit schema.
        if schema is None:
            schema = SCHEMA if relations or any(isinstance(d, dict) and d.get("research") for d in definitions) else LEGACY_SNAPSHOT_SCHEMA
        self._nodes = {}
        self._edges = []
        self._semantic_edges = []
        self._schema = schema
        if schema not in {SCHEMA, LEGACY_SNAPSHOT_SCHEMA}:
            raise ValueError("unsupported graph schema")
        self._provenance = copy.deepcopy(provenance if provenance is not None else {})
        if not isinstance(self._provenance, dict) or set(self._provenance) - {"catalog_sha256", "inventory_sha256"}:
            raise ValueError("unsupported graph provenance")
        if any(not isinstance(v, str) or not re.fullmatch(r"[0-9a-f]{64}", v) for v in self._provenance.values()):
            raise ValueError("provenance requires SHA-256 digests")
        for definition in definitions:
            definition = _definition(definition)
            domain, path = definition["domain"], definition["path"]
            parts = _components(path, domain)
            components = parts[-1]["canonical_components"]
            key = _identity(domain, components)
            if key in self._nodes:
                raise ValueError("duplicate canonical knowledge path: " + path)
            self._nodes[key] = {"id": key, **definition, "label": parts[-1]["value"],
                                "canonical_components": components, "depth": len(components),
                                "is_placeholder": domain == "registry" and bool(re.fullmatch(r"<[^<>]+>", components[-1])),
                                "template_dependent": domain == "registry" and any(bool(re.fullmatch(r"<[^<>]+>", p)) for p in components),
                                "parent_id": _identity(domain, components[:-1]) if len(components) > 1 else None}
        for node in self._nodes.values():
            parent = node["parent_id"]
            if parent is not None:
                if parent not in self._nodes:
                    raise ValueError("missing explicit parent definition for " + node["path"])
                self._edges.append({"source": parent, "target": node["id"],
                                    "type": "NEXT_SYNTAX_COMPONENT" if node["domain"] == "command" else "HAS_CHILD"})
        if relations is not None and not isinstance(relations, list):
            raise ValueError("semantic relations must be a list")
        seen = set()
        for relation in relations or []:
            fields = {"source_path", "target_path", "relation", "explanation", "sources"}
            if not isinstance(relation, dict) or set(relation) != fields:
                raise ValueError("invalid semantic relation fields")
            if any(not isinstance(relation[k], str) or not relation[k].strip() for k in fields - {"sources"}):
                raise ValueError("semantic relation fields must be nonempty strings")
            if not re.fullmatch(r"[A-Z][A-Z_]+", relation["relation"]):
                raise ValueError("semantic relation names must use UPPER_SNAKE_CASE")
            _sources(relation["sources"], required=True)
            source, target = [_identity("registry", _components(relation[k], "registry")[-1]["canonical_components"])
                              for k in ("source_path", "target_path")]
            if source not in self._nodes or target not in self._nodes or source == target:
                raise ValueError("semantic relations require two distinct existing nodes")
            key = (source, relation["relation"], target)
            if key in seen:
                raise ValueError("duplicate semantic relation")
            seen.add(key)
            self._semantic_edges.append({"source": source, "target": target, "type": relation["relation"],
                                         "explanation": relation["explanation"], "sources": copy.deepcopy(relation["sources"])})
        if schema == LEGACY_SNAPSHOT_SCHEMA and (self._semantic_edges or any(n["research"] for n in self._nodes.values())):
            raise ValueError("research and semantic edges require snapshot schema 3")

    @classmethod
    def load_catalog(cls, path, inventory=None):
        catalog_bytes = Path(path).read_bytes()
        data = json.loads(catalog_bytes)
        if not isinstance(data, dict) or data.get("schema") not in {CATALOG_SCHEMA, LEGACY_SNAPSHOT_SCHEMA, SCHEMA}:
            raise ValueError("unsupported knowledge catalog schema")
        if not isinstance(data["definitions"], list):
            raise ValueError("catalog definitions must be a list")
        definitions = [_definition(d) for d in data["definitions"]]
        provenance = {"catalog_sha256": hashlib.sha256(catalog_bytes).hexdigest()}
        relations = data.get("relations", [])
        schema = SCHEMA if data["schema"] == SCHEMA else None
        if inventory is None:
            return cls(definitions, provenance, relations, schema)
        inventory_bytes = Path(inventory).read_bytes()
        base = _inventory_definitions(json.loads(inventory_bytes))
        provenance["inventory_sha256"] = hashlib.sha256(inventory_bytes).hexdigest()
        by_id = {_identity(d["domain"], _components(d["path"], d["domain"])[-1]["canonical_components"]): d for d in base}
        seen = set()
        for definition in definitions:
            key = _identity(definition["domain"], _components(definition["path"], definition["domain"])[-1]["canonical_components"])
            if key in seen or key not in by_id:
                raise ValueError("duplicate catalog path or catalog path outside inventory: " + definition["path"])
            seen.add(key)
            # Keep inventory spelling and path evidence; enrich only from authored knowledge.
            for field in ("role", "explanation", "explanation_sources", "status", "candidate_tags", "research"):
                by_id[key][field] = definition[field]
        return cls(base, provenance, relations, schema)

    def to_dict(self):
        result = {"schema": self._schema, "provenance": copy.deepcopy(self._provenance),
                  "nodes": copy.deepcopy(list(self._nodes.values())), "edges": copy.deepcopy(self._edges)}
        if self._schema == SCHEMA:
            result["semantic_edges"] = copy.deepcopy(self._semantic_edges)
        else:
            for node in result["nodes"]:
                node.pop("research")
        return result

    def save(self, path):
        Path(path).write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    @classmethod
    def load(cls, path):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("schema") not in {SCHEMA, LEGACY_SNAPSHOT_SCHEMA}:
            raise ValueError("unsupported knowledge graph schema; rebuild from catalog")
        fields = DEFINITION_FIELDS if data["schema"] == SCHEMA else DEFINITION_FIELDS - {"research"}
        nodes = {n["id"]: n for n in data["nodes"]}
        relations = [{"source_path": nodes[e["source"]]["path"], "target_path": nodes[e["target"]]["path"],
                      "relation": e["type"], "explanation": e["explanation"], "sources": e["sources"]}
                     for e in data.get("semantic_edges", [])]
        graph = cls([{k: n[k] for k in fields} for n in data["nodes"]], data["provenance"], relations, data["schema"])
        # JSON comparison also rejects bool-for-int substitutions in computed metadata.
        if json.dumps(graph.to_dict(), sort_keys=True) != json.dumps(data, sort_keys=True):
            raise ValueError("graph nodes or edges disagree with canonical knowledge definitions")
        return graph

    def resolve(self, raw, domain, template_candidates=False):
        """Read-only prefix walk with optional, explicitly labeled template candidates."""
        if type(template_candidates) is not bool:
            raise TypeError("template_candidates must be a boolean")
        parts, warnings = split_input(raw, domain)
        steps = []
        for index, part in enumerate(parts):
            key = _identity(domain, part["canonical_components"])
            node = self._nodes.get(key)
            match = "literal_template" if node and node["template_dependent"] else "known" if node else "unknown"
            bindings = None
            candidates = []
            if node is None and template_candidates and domain == "registry":
                for candidate in self._nodes.values():
                    candidate_bindings = _template_bindings(
                        candidate["canonical_components"], part["canonical_components"],
                        [item["raw"] for item in parts[:index + 1]])
                    if candidate_bindings is not None:
                        candidates.append((candidate, candidate_bindings))
                if len(candidates) == 1:
                    node, bindings = candidates[0]
                    key, match = node["id"], "template_candidate"
                elif len(candidates) > 1:
                    match = "ambiguous_template"
            steps.append({**part, "node_id": key if node else None,
                          "match": match, "template_bindings": copy.deepcopy(bindings or {}),
                          "candidate_node_ids": [candidate["id"] for candidate, _ in candidates] if len(candidates) > 1 else [],
                          "explanation_status": node["status"] if node else "unknown",
                          "knowledge": copy.deepcopy(node) if node else None})
        ids = [step["node_id"] for step in steps]
        traversed = [edge for edge in self._edges
                     if any(edge["source"] == a and edge["target"] == b for a, b in zip(ids, ids[1:]))]
        path_complete = bool(steps) and all(ids) and not any(s["match"] == "template_candidate" for s in steps)
        pattern_complete = bool(steps) and all(ids)
        explanations_complete = path_complete and all(s["explanation_status"] != "pending" for s in steps)
        pattern_explanations_complete = pattern_complete and all(s["explanation_status"] != "pending" for s in steps)
        if any(s["match"] == "literal_template" for s in steps):
            warnings.append("Literal template notation matched; no concrete name was bound and no Registry instance is asserted.")
        if any(s["match"] == "template_candidate" for s in steps):
            warnings.append("A constrained template candidate matched. It supplies pattern knowledge only and does not assert that the concrete key exists, is loaded, or has the documented values.")
        if any(s["match"] == "ambiguous_template" for s in steps):
            warnings.append("More than one template candidate matched; no template knowledge was selected.")
        bindings = {}
        for step in steps:
            bindings.update(step["template_bindings"])
        return {"input": raw, "domain": domain, "steps": steps,
                "path_node_ids": ids, "edges": copy.deepcopy(traversed),
                "path_complete": path_complete, "explanations_complete": explanations_complete,
                "pattern_complete": pattern_complete,
                "pattern_explanations_complete": pattern_explanations_complete,
                "template_bindings": bindings,
                "complete": explanations_complete, "warnings": warnings,
                "interpretation": "Knowledge lookup only; no event, execution, value data, or intent is inferred."}

    def markdown(self):
        """Single-file preview using the same per-node rendering as the vault."""
        from .zettelkasten import render_markdown
        return render_markdown(self)

    def model_context(self, raw, value_name=None, path_format="canonical", template_candidates=False):
        """Compact, cited retrieval for a registry key; value names stay a separate field."""
        if value_name is not None and not isinstance(value_name, str):
            raise TypeError("value_name must be a string or None")
        adaptation = adapt_registry_path(raw, path_format)
        result = self.resolve(adaptation["canonical_path"], "registry", template_candidates)
        matched_steps = [s for s in result["steps"] if s["knowledge"] is not None]
        matched = [s["knowledge"] for s in matched_steps]
        terminal = result["steps"][-1]["knowledge"] if result["steps"] else None
        values = []
        if value_name is not None and terminal:
            values = [v for v in terminal.get("research", {}).get("value_semantics", [])
                      if v["kind"] == "value" and v["name"].casefold() == value_name.casefold()]
        matched_ids = {n["id"] for n in matched}
        relations = [e for e in self._semantic_edges if e["source"] in matched_ids or e["target"] in matched_ids]
        related_ids = {e[k] for e in relations for k in ("source", "target")} - matched_ids
        prefix_knowledge = []
        for step in matched_steps:
            node = step["knowledge"]
            prefix_knowledge.append({**{k: node[k] for k in ("id", "path", "depth", "status", "explanation", "explanation_sources", "research", "template_dependent")},
                                     "lookup_match": step["match"],
                                     "template_bindings": copy.deepcopy(step["template_bindings"])})
        return {"schema": "registry-model-context-2", "input_key": raw,
                "query_key": adaptation["canonical_path"], "path_adaptation": adaptation,
                "value_name": value_name,
                "path_complete": result["path_complete"], "explanations_complete": result["explanations_complete"],
                "pattern_complete": result["pattern_complete"],
                "pattern_explanations_complete": result["pattern_explanations_complete"],
                "template_bindings": copy.deepcopy(result["template_bindings"]),
                "prefix_knowledge": prefix_knowledge,
                "unknown_components": [s["raw"] for s in result["steps"] if s["node_id"] is None],
                "value_knowledge": copy.deepcopy(values), "semantic_edges": copy.deepcopy(relations),
                "related_nodes": [{"id": key, "path": self._nodes[key]["path"]} for key in sorted(related_ids)],
                "warnings": result["warnings"],
                "inference_boundary": "This is path knowledge, not an event interpretation. Provider, event type, operation, outcome, identity, time, value type/data and platform context must come from the actual log. Never infer execution, policy enforcement or intent from the key name alone."}

