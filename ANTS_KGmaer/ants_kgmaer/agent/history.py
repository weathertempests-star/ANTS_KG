"""Reveal only precomputed strictly-prior events under the secondary history policy."""

import copy


def reveal_history(session, history):
    candidates = session.toolbox.dynamic_history
    if candidates is None:
        raise ValueError("Dynamic history is not enabled")
    allowed = {event["id"]: event for event in candidates}
    if any(event.get("id") not in allowed or event != allowed[event["id"]] for event in history):
        raise ValueError("History contains an event outside the permitted prior context")
    ids = {event["id"] for event in session.context["history"]} | {event["id"] for event in history}
    session.context["history"] = [copy.deepcopy(event) for event in candidates if event["id"] in ids]


def adopt_replay_context(session, context):
    if session.toolbox.dynamic_history is None:
        if context != session.context:
            raise ValueError("Replay event context differs from source")
        return
    if {k: v for k, v in context.items() if k != "history"} != {
        k: v for k, v in session.context.items() if k != "history"
    }:
        raise ValueError("Replay event context differs from source")
    reveal_history(session, context["history"])
    if session.context != context:
        raise ValueError("Replay history differs from the permitted source ordering")
