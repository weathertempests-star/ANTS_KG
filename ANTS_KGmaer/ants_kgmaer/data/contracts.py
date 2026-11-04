"""Explicit key/value encoding contracts; ambiguity is data, never a guess."""

from ..common.files import object_hash, read_json


class RelationContract:
    def __init__(self, path):
        self.document = read_json(path)
        self.hash = object_hash(self.document)
        if self.document.get("schema") != "ants-relations-1":
            raise ValueError("Unsupported relation contract")
        for rule in list(self.document["relations"].values()) + [
            r for group in self.document.get("recording_overrides", {}).values() for r in group.values()
        ]:
            if rule["encoding"] not in {"key_path", "unresolved", "last_component", "separate_field"}:
                raise ValueError("Unsupported Registry encoding")
            if rule["encoding"] in {"last_component", "separate_field"} and not rule.get("evidence"):
                raise ValueError("Confirmed value encoding requires a provenance/evidence description")

    def adapt(self, relation, target, recording_id):
        default = {"operation": "unknown", "encoding": "unresolved"}
        rule = self.document.get("recording_overrides", {}).get(recording_id, {}).get(
            relation, self.document["relations"].get(relation, default))
        raw = target.get("Key")
        result = {"operation": rule["operation"], "operation_result": "not_recorded",
                  "key_path": None, "value_name": None, "lookup_target": raw if isinstance(raw, str) else None,
                  "boundary_status": "unresolved", "path_format": "canonical", "view": "not_recorded"}
        if not isinstance(raw, str) or not raw:
            result["boundary_status"] = "missing_target"
            return result
        if raw.lower().startswith(("\\registry\\machine", "\\registry\\user\\")):
            result["path_format"] = "nt_native"
        encoding = rule["encoding"]
        if encoding == "key_path":
            result.update(key_path=raw, boundary_status="key_confirmed")
        elif encoding == "separate_field":
            name = target.get(rule.get("value_name_field", "ValueName"))
            if isinstance(name, str):
                result.update(key_path=raw, value_name=name, boundary_status="value_confirmed")
        elif encoding == "last_component":
            # Only explicitly confirmed recordings may opt in; no name heuristics.
            if "\\" in raw:
                key, name = raw.rsplit("\\", 1)
                if name in rule.get("unnamed_value_markers", []):
                    name = ""
                result.update(key_path=key, value_name=name, boundary_status="value_confirmed")
        result["lookup_target"] = result["key_path"] or raw
        return result
