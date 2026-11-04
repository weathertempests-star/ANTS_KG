"""Registry path parsing, canonical identity, and constrained templates."""
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from .constants import (SCHEMA, LEGACY_SNAPSHOT_SCHEMA, CATALOG_SCHEMA, DEFINITION_FIELDS,
                        RESEARCH_FIELDS, HIVES, NT_NATIVE_SOURCE, GUID_TEMPLATE_NAMES,
                        GUID_COMPONENT, SID_COMPONENT)
from .command_parser import parse_command

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

