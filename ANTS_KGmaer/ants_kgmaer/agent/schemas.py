"""Small explicit output schemas shared by the server and local validation."""


def obj(properties):
    return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}


def strings(maximum=32):
    return {"type": "array", "maxItems": maximum, "items": {"type": "string", "maxLength": 2000}}


DECISION = obj({
    "prediction": {"type": "string", "enum": ["benign", "malicious", "insufficient_evidence"]},
    "evidence_event_ids": strings(33), "knowledge_node_ids": strings(32),
    "claims": {"type": "array", "maxItems": 4, "items": obj({
        "statement": {"type": "string", "maxLength": 1000}, "evidence_ids": strings(32)})},
    "unknowns": strings(8), "score": {"type": "null"},
})


def action_schema(dynamic_history=False):
    calls = [
        obj({"tool": {"enum": ["lookup_registry"]}, "arguments": obj({"event_ids": {
            "type": "array", "minItems": 1, "maxItems": 4, "items": {"type": "string"}}})}),
        obj({"tool": {"enum": ["expand_knowledge"]}, "arguments": obj({"node_ids": {
            "type": "array", "minItems": 1, "maxItems": 6, "items": {"type": "string"}}})}),
    ]
    if dynamic_history:
        calls.append(obj({"tool": {"enum": ["get_prior_context"]},
                          "arguments": obj({"k": {"type": "integer", "minimum": 0, "maximum": 16}})}))
    return {"anyOf": [obj({"action": {"enum": ["finalize"]}}),
                      obj({"action": {"enum": ["retrieve"]}, "calls": {
                          "type": "array", "minItems": 1, "maxItems": 2, "items": {"anyOf": calls}}})]}
