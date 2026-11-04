"""Validate authored definitions and inventory provenance."""
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from .constants import (SCHEMA, LEGACY_SNAPSHOT_SCHEMA, CATALOG_SCHEMA, DEFINITION_FIELDS,
                        RESEARCH_FIELDS, HIVES, NT_NATIVE_SOURCE, GUID_TEMPLATE_NAMES,
                        GUID_COMPONENT, SID_COMPONENT)
from .paths import _components, _identity

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

