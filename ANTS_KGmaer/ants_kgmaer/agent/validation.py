"""Validate the restricted schema vocabulary and only actually supplied citations."""

import json

from .schemas import DECISION


def validate_schema(value, schema, path="$ "):
    """Validate our fixed schema subset, rejecting unsupported schema keywords."""
    supported = {"type", "enum", "anyOf", "properties", "required", "additionalProperties", "items",
                 "minItems", "maxItems", "maxLength", "minimum", "maximum"}
    if set(schema) - supported:
        raise ValueError("Unsupported output-schema keyword")
    if "anyOf" in schema:
        for candidate in schema["anyOf"]:
            try:
                validate_schema(value, candidate, path)
                return
            except ValueError:
                pass
        raise ValueError(path + "does not match an allowed variant")
    kind = schema.get("type")
    types = {"object": dict, "array": list, "string": str, "integer": int, "null": type(None)}
    if kind and (kind not in types or type(value) is not types[kind]):
        raise ValueError(path + "has incorrect type")
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(path + "is not an allowed value")
    if isinstance(value, dict) and kind == "object":
        properties = schema["properties"]
        if set(schema["required"]) - value.keys() or (not schema["additionalProperties"] and value.keys() - properties.keys()):
            raise ValueError(path + "has missing or extra fields")
        for key, item in value.items():
            validate_schema(item, properties[key], path + key + ".")
    if isinstance(value, list) and kind == "array":
        if not schema.get("minItems", 0) <= len(value) <= schema.get("maxItems", float("inf")):
            raise ValueError(path + "has invalid list length")
        for item in value:
            validate_schema(item, schema["items"], path + "item.")
    if isinstance(value, str) and len(value) > schema.get("maxLength", float("inf")):
        raise ValueError(path + "string is too long")
    if type(value) is int and not schema.get("minimum", -float("inf")) <= value <= schema.get("maximum", float("inf")):
        raise ValueError(path + "integer is out of range")


def parse_output(text, schema):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate JSON field: " + key)
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError("Non-finite JSON value: " + value)

    value = json.loads(text, object_pairs_hook=unique_pairs, parse_constant=invalid_constant)
    validate_schema(value, schema)
    return value


def decision(text, event_ids, node_ids):
    result = parse_output(text, DECISION)
    if not set(result["evidence_event_ids"]) <= set(event_ids):
        raise ValueError("Unknown or not-delivered event citation")
    if not set(result["knowledge_node_ids"]) <= set(node_ids):
        raise ValueError("Unknown or not-delivered knowledge citation")
    allowed = set(event_ids) | set(node_ids)
    for claim in result["claims"]:
        if not claim["evidence_ids"] or not set(claim["evidence_ids"]) <= allowed:
            raise ValueError("Claims require valid delivered evidence citations")
    if result["prediction"] != "insufficient_evidence":
        if "event_0" not in result["evidence_event_ids"] or not result["claims"]:
            raise ValueError("A definite prediction requires a cited target event and a brief supported claim")
    elif not result["unknowns"]:
        raise ValueError("Abstention requires an explicit missing-evidence explanation")
    return result
