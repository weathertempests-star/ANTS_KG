"""Build canonical internal records and strict public facts independently of labels."""

from ..common.files import object_hash


def normalize(row, source, row_index, redactor, contract):
    src = row.get("srcNode") if isinstance(row.get("srcNode"), dict) else {}
    dst = row.get("dstNode") if isinstance(row.get("dstNode"), dict) else {}
    event_id = source["sha256"] + ":" + str(row_index)
    identity = src.get("UUID") if src.get("Type") == "Process" else None
    identity_known = isinstance(identity, str) and bool(identity)
    actor_id = object_hash([source["id"], identity if identity_known else event_id])
    order = row.get("timestamp")
    order = order if type(order) is int and -(2**63) <= order < 2**63 else None
    relation = row.get("relation")
    relation = relation if isinstance(relation, str) else "unknown"
    facts = {"relation": redactor.text(relation), "actor": redactor.actor(src),
             "actor_identity_known": identity_known, "target": redactor.target(dst)}
    if dst.get("Type") == "Registry":
        registry = contract.adapt(relation, dst, source["id"])
        for field in ("key_path", "value_name", "lookup_target"):
            registry[field] = redactor.text(registry[field])
        facts["registry"] = registry
        # Kept outside the common-field public event view; opt-in only.
        facts["optional_value_data"] = redactor.text(dst.get("Value"))
    signature = object_hash({k: v for k, v in row.items() if k not in {"label", "timestamp_raw"}})
    normalized = object_hash({k: v for k, v in facts.items() if k != "optional_value_data"})
    return {"event_id": event_id, "recording_id": source["id"], "row_index": row_index,
            "actor_id": actor_id, "order_ref": order, "target_type": facts["target"]["type"],
            "facts": facts, "exact_signature": signature, "normalized_signature": normalized}
