"""Shared prefix knowledge, independent of audit events.

Catalog authoring is explicit. Resolving an input never adds knowledge or events.
"""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re

from .command_parser import parse_command

SCHEMA = "prefix-knowledge-3"
LEGACY_SNAPSHOT_SCHEMA = "prefix-knowledge-2"
CATALOG_SCHEMA = "prefix-knowledge-1"
DEFINITION_FIELDS = {"domain", "path", "role", "explanation", "explanation_sources",
                     "status", "path_sources", "explicitly_listed", "candidate_tags", "research"}
RESEARCH_FIELDS = {"summary", "scope", "log_context", "cannot_infer", "value_semantics", "applicability", "evidence"}
HIVES = {"hklm": "hkey_local_machine", "hkcu": "hkey_current_user",
         "hku": "hkey_users", "hkcr": "hkey_classes_root", "hkcc": "hkey_current_config"}
NT_NATIVE_SOURCE = "https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/registry-key-object-routines"
GUID_TEMPLATE_NAMES = {"<appid_guid>", "<clsid>", "<iid>", "<productcodeguid>",
                       "<setupclassguid>", "<interfaceclassguid>"}
GUID_COMPONENT = re.compile(r"\{[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}", re.I)
SID_COMPONENT = re.compile(r"s-1-\d+(?:-\d+)+", re.I)


def split_input(raw, domain):
    if not isinstance(raw, str):
        raise TypeError("input must be a string")
    if domain not in {"registry", "file", "command"}:
        raise ValueError("domain must be registry, file or command")
    if domain == "command":
        parsed = parse_command(raw, dialect="windows")
        parts = [{"raw": t["raw"], "value": t["value"], "source_span": [t["start"], t["end"]],
                  "syntax_role": t["role"]} for t in parsed["tokens"]]
        warnings = parsed["warnings"]
    else:
        # Registry '/' is a legal key-name character, not a registry separator.
        pattern = r"[^\\]+" if domain == "registry" else r"[^\\/]+"
        parts = [{"raw": m.group(), "value": m.group(), "source_span": [m.start(), m.end()]}
                 for m in re.finditer(pattern, raw)]
        warnings = []
        if domain == "registry" and parts and parts[0]["value"].casefold() not in set(HIVES) | set(HIVES.values()):
            warnings.append("Unrecognized registry root; native and remote aliases require an explicit adapter.")
        if domain == "file" and not re.match(r"^[A-Za-z]:[\\/]", raw):
            raise ValueError("file input currently requires an absolute Windows drive path")
    canonical = []
    for i, part in enumerate(parts):
        value = part["value"]
        if domain == "registry":
            value = value.casefold()
            if i == 0:
                value = HIVES.get(value, value)
        elif domain == "file":
            value = value.casefold()
        # Command arguments retain case; executable/subcommand aliases require explicit knowledge.
        canonical.append(value)
        part["canonical_components"] = list(canonical)
    return parts, warnings


def _identity(domain, components):
    encoded = json.dumps([domain, components], ensure_ascii=False, separators=(",", ":"))
    return "knowledge:" + hashlib.sha256(encoded.encode()).hexdigest()[:24]


def adapt_registry_path(raw, path_format="canonical"):
    """Explicitly adapt a key path without guessing values, users, views or templates."""
    if not isinstance(raw, str):
        raise TypeError("input must be a string")
    if path_format == "canonical":
        return {"input": raw, "path_format": path_format, "canonical_path": raw,
                "adapted": False, "source": None,
                "notes": ["Input already uses a supported predefined-hive form."]}
    if path_format != "nt_native":
        raise ValueError("path_format must be canonical or nt_native")
    parts = raw.split("\\")
    if not parts or any(part == "" for part in parts[1:-1]):
        raise ValueError("invalid NT native Registry path")
    while parts and parts[0] == "":
        parts.pop(0)
    if len(parts) < 2 or parts[0].casefold() != "registry":
        raise ValueError("NT native Registry paths must start with \\Registry\\Machine or \\Registry\\User")
    root = parts[1].casefold()
    if root == "machine":
        hive = "HKLM"
    elif root == "user":
        hive = "HKU"
    else:
        raise ValueError("unsupported NT native Registry root: " + parts[1])
    remainder = [part for part in parts[2:] if part]
    return {"input": raw, "path_format": path_format,
            "canonical_path": "\\".join([hive, *remainder]), "adapted": True,
            "source": NT_NATIVE_SOURCE,
            "notes": ["The adapter maps only documented object-manager roots.",
                      "A USER SID remains under HKU; it is not silently rewritten to HKCU.",
                      "The adapter does not infer a value name, Registry view, account identity or key existence."]}


def _template_bindings(pattern, concrete, display=None):
    """Return constrained component bindings, or None when a template does not match."""
    if len(pattern) != len(concrete):
        return None
    bindings = {}
    display = concrete if display is None else display
    for expected, actual, original in zip(pattern, concrete, display):
        if not re.fullmatch(r"<[^<>]+>", expected):
            if expected != actual:
                return None
            continue
        if expected in GUID_TEMPLATE_NAMES:
            valid = bool(GUID_COMPONENT.fullmatch(actual))
        elif expected == "<userhive>":
            valid = bool(SID_COMPONENT.fullmatch(actual))
        elif expected == "<fileextension>":
            valid = actual.startswith(".") and len(actual) > 1 and "<" not in actual and ">" not in actual
        else:
            valid = bool(actual) and "<" not in actual and ">" not in actual
        if not valid or (expected in bindings and bindings[expected].casefold() != original.casefold()):
            return None
        bindings[expected] = original
    return bindings or None


def _components(path, domain):
    # A volume root is the one exception to file input's absolute path requirement.
    parts, _ = split_input(path + "\\" if domain == "file" and re.fullmatch(r"[A-Za-z]:", path) else path, domain)
    if not parts:
        raise ValueError("empty knowledge path")
    return parts


def _sources(value, required=False):
    if not isinstance(value, list) or (required and not value) or any(
            not isinstance(s, str) or not s.startswith("https://") or any(c.isspace() for c in s)
            for s in value):
        raise ValueError("sources must be a list of HTTPS documentation URLs")


def _definition(value):
    if not isinstance(value, dict):
        raise ValueError("definition must be an object")
    value = copy.deepcopy(value)
    legacy = {"domain", "path", "role", "explanation", "sources", "status"}
    if set(value) - {"research"} == legacy:
        value["explanation_sources"] = value.pop("sources")
        value.update(path_sources=[], explicitly_listed=False, candidate_tags=[])
    value.setdefault("research", {})
    if set(value) != DEFINITION_FIELDS:
        raise ValueError("unexpected or missing knowledge definition fields")
    for field in ("domain", "path", "role", "explanation", "status"):
        if not isinstance(value[field], str):
            raise ValueError("definition text fields must be strings")
    if not value["path"].strip() or value["status"] not in {"documented", "structural", "conventional", "pending"}:
        raise ValueError("invalid knowledge path or status")
    pending = value["status"] == "pending"
    if pending:
        if value["explanation"] or value["role"] or value["explanation_sources"]:
            raise ValueError("pending knowledge must leave explanation, role and explanation sources empty")
    elif not value["role"].strip() or not value["explanation"].strip():
        raise ValueError("explained knowledge requires a role and explanation")
    _sources(value["explanation_sources"], required=not pending)
    _sources(value["path_sources"])
    if type(value["explicitly_listed"]) is not bool:
        raise ValueError("explicitly_listed must be a boolean")
    if value["candidate_tags"] != []:
        raise ValueError("candidate_tags must remain empty until tagging is implemented")
    _research(value["research"], value["explanation_sources"], pending)
    return value


def _research(research, sources, pending):
    """Validate author evidence separately from inventory citations and event facts."""
    if not isinstance(research, dict):
        raise ValueError("research must be an object")
    if not research:
        return  # Original catalogs remain readable, but are not model-export ready.
    if pending or set(research) != RESEARCH_FIELDS:
        raise ValueError("research requires explained knowledge and all research fields")
    for name in ("summary", "scope", "log_context", "applicability"):
        if not isinstance(research[name], str) or not research[name].strip():
            raise ValueError("research text fields must be nonempty strings")
    if research["scope"] not in {"machine", "user", "logical_view", "user_template", "mixed"}:
        raise ValueError("unsupported research scope")
    limits = research["cannot_infer"]
    if not isinstance(limits, list) or len(limits) < 2 or any(not isinstance(s, str) or not s.strip() for s in limits):
        raise ValueError("research needs at least two explicit interpretation limits")
    if not isinstance(research["value_semantics"], list):
        raise ValueError("value_semantics must be a list")
    for item in research["value_semantics"]:
        if not isinstance(item, dict) or set(item) != {"name", "kind", "meaning", "source"}:
            raise ValueError("invalid value/subkey semantics record")
        if (any(not isinstance(v, str) for v in item.values())
                or any(not item[k].strip() for k in ('kind', 'meaning', 'source'))
                or (not item['name'].strip() and not (item['kind'] == 'value' and item['name'] == ''))):
            raise ValueError("value/subkey semantics need nonempty text fields")
        if item["kind"] not in {"value", "subkey", "value_collection"} or item["source"] not in sources:
            raise ValueError("value/subkey semantics require a valid kind and explanation source")
    evidence = research["evidence"]
    if not isinstance(evidence, list) or not evidence:
        raise ValueError("research needs claim-level evidence")
    for item in evidence:
        if not isinstance(item, dict) or set(item) != {"url", "section", "claim", "support"}:
            raise ValueError("invalid research evidence record")
        if any(not isinstance(v, str) or not v.strip() for v in item.values()):
            raise ValueError("evidence requires URL, section, claim and support")
        if item["url"] not in sources or item["support"] not in {"direct", "structural_inference"}:
            raise ValueError("research evidence must cite explanation sources and distinguish inference")


def _inventory_definitions(data):
    """Validate the saved hierarchy and counts; path citations never become explanations."""
    if not isinstance(data, dict):
        raise ValueError("inventory must be an object")
    nodes = data["nodes"]
    if not isinstance(nodes, list):
        raise ValueError("inventory nodes must be a list")
    definitions, identities = [], set()
    counts = Counter()
    for row in nodes:
        parts = _components(row["path"], "registry")
        components = parts[-1]["canonical_components"]
        identity = tuple(components)
        if components[0] not in HIVES.values() or identity in identities:
            raise ValueError("invalid or duplicate inventory prefix")
        identities.add(identity)
        placeholder = bool(re.fullmatch(r"<[^<>]+>", components[-1]))
        template = any(re.fullmatch(r"<[^<>]+>", p) for p in components)
        if (type(row["depth"]) is not int or row["depth"] != len(parts)
                or row["label"] != parts[-1]["value"]
                or row["is_placeholder"] is not placeholder
                or row["template_dependent"] is not template):
            raise ValueError("inventory depth, label or template metadata disagrees with path")
        parent = row["parent_path"]
        if len(parts) == 1:
            if parent is not None:
                raise ValueError("inventory root cannot have a parent")
        elif not parent or _components(parent, "registry")[-1]["canonical_components"] != components[:-1]:
            raise ValueError("inventory parent disagrees with full prefix")
        _sources(row["sources"], required=True)
        definitions.append(dict(domain="registry", path=row["path"], role="", explanation="", status="pending",
                                explanation_sources=[], path_sources=row["sources"],
                                explicitly_listed=row["explicitly_listed"], candidate_tags=[]))
        counts["nodes"] += 1
        counts["edges"] += int(parent is not None)
        counts["roots"] += int(parent is None)
        counts["fixed_nodes"] += int(not template)
        counts["template_dependent_nodes"] += int(template)
        counts["placeholder_nodes"] += int(placeholder)
    expected_depths = []
    for depth in sorted({n["depth"] for n in nodes}):
        group = [n for n in nodes if n["depth"] == depth]
        expected_depths.append(dict(depth=depth, fixed_nodes=sum(not n["template_dependent"] for n in group),
                                    template_dependent_nodes=sum(n["template_dependent"] for n in group),
                                    placeholder_nodes=sum(n["is_placeholder"] for n in group), total_nodes=len(group)))
    roots = Counter(next(k for k, v in HIVES.items() if v == p[0]).upper() for p in identities)
    if (any(data["summary"].get(k) != v for k, v in counts.items())
            or data["summary"].get("by_root") != dict(roots) or data["by_depth"] != expected_depths):
        raise ValueError("inventory statistics disagree with hierarchy")
    # Reconstruct the evidence union for every prefix, including implicit ancestors.
    evidence_sources, explicit = {}, set()
    for row in data["explicit_paths"]:
        components = tuple(_components(row["path"], "registry")[-1]["canonical_components"])
        if components in explicit or not row["evidence"]:
            raise ValueError("duplicate or unsupported explicit inventory path")
        explicit.add(components)
        for evidence in row["evidence"]:
            if tuple(_components(evidence["path"], "registry")[-1]["canonical_components"]) != components:
                raise ValueError("inventory evidence belongs to a different path")
            for depth in range(1, len(components) + 1):
                evidence_sources.setdefault(components[:depth], set()).add(evidence["source"])
    if set(evidence_sources) != identities or data["summary"]["accepted_unique_paths"] != len(explicit):
        raise ValueError("inventory nodes disagree with accepted path evidence")
    for row, definition in zip(nodes, definitions):
        key = tuple(_components(row["path"], "registry")[-1]["canonical_components"])
        if set(row["sources"]) != evidence_sources[key] or row["explicitly_listed"] is not (key in explicit):
            raise ValueError("inventory path sources or listing status disagree with evidence")
    return definitions


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
