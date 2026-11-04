"""Disk-backed overlap audit and conservative recording dependency components."""

from collections import Counter
from itertools import combinations, groupby

from .store import readonly


def signature_overlap(connection, column):
    if column not in {"exact_signature", "normalized_signature"}:
        raise ValueError("Unsupported overlap signature")
    query = f"SELECT {column}, recording_id, COUNT(*) FROM events GROUP BY {column}, recording_id ORDER BY {column}, recording_id"
    pairs, duplicates = Counter(), Counter()
    for _, members in groupby(connection.execute(query), key=lambda row: row[0]):
        recordings = []
        for _, recording_id, count in members:
            recordings.append(recording_id)
            duplicates[recording_id] += count - 1
        for pair in combinations(recordings, 2):
            pairs[pair] += 1
    return {"pairs": [{"left": a, "right": b, "unique_shared": count} for (a, b), count in sorted(pairs.items())],
            "within_recording_repetitions": dict(duplicates)}


def dependency_groups(sources, overlaps):
    parent = {s["id"]: s["id"] for s in sources}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        parent[max(find(a), find(b))] = min(find(a), find(b))

    declared = {}
    for source in sources:
        key = source["dependency_group"]
        if key in declared:
            union(source["id"], declared[key])
        declared[key] = source["id"]
    for overlap in overlaps:
        union(overlap["left"], overlap["right"])
    groups = {}
    for recording in parent:
        groups.setdefault(find(recording), []).append(recording)
    return [sorted(members) for _, members in sorted(groups.items())]


def audit_overlap(events_path, sources):
    connection = readonly(events_path)
    try:
        exact = signature_overlap(connection, "exact_signature")
        normalized = signature_overlap(connection, "normalized_signature")
    finally:
        connection.close()
    return {"schema": "ants-overlap-1", "exact": exact, "normalized": normalized,
            "dependency_groups": dependency_groups(sources, exact["pairs"]),
            "limits": ["Exact signatures exclude label and timestamp_raw but retain UUID and order reference.",
                       "Normalized overlap is a background-pattern warning, not proof of shared recording origin.",
                       "Declared and exact-overlap components are minimum dependencies, not proof of independence."]}
