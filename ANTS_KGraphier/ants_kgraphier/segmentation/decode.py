"""Connected selection with explicit connectors and exact event provenance."""
from collections import deque
import math

from ..io import fingerprint


def decode(graph, scores, budget=32, threshold=0.5):
    if budget < 1 or not 0 <= threshold <= 1:
        raise ValueError('invalid budget or threshold')
    events = graph['events']
    if len(scores) != len(events) or any(not math.isfinite(s) or not 0 <= s <= 1 for s in scores):
        raise ValueError('one finite probability per event required')
    anchor = next(i for i, e in enumerate(events) if e['event_id'] == graph['anchor_event_id'])
    endpoints = {}
    for i, e in enumerate(events):
        for key in {e['src'], e['dst']}:
            endpoints.setdefault(key, []).append(i)
    # BFS over shared endpoints; endpoint expansion happens at most once.
    parents, queue, visited_endpoints = {anchor: None}, deque([anchor]), set()
    while queue:
        i = queue.popleft()
        for key in sorted({events[i]['src'], events[i]['dst']}):
            if key in visited_endpoints:
                continue
            visited_endpoints.add(key)
            for j in endpoints[key]:
                if j not in parents:
                    parents[j] = i
                    queue.append(j)
    selected, reasons = {anchor}, {anchor: 'anchor'}
    rejected = 0
    for i in sorted(range(len(events)), key=lambda j: (-scores[j], events[j]['row'])):
        if scores[i] < threshold or i in selected or i not in parents:
            continue
        path, current = [], i
        while current not in selected:
            path.append(current)
            current = parents[current]
        if len(selected) + len(path) > budget:
            rejected += 1
            continue
        for j in path:
            selected.add(j)
            reasons[j] = 'selected' if j == i else 'connector'
    output = dict(graph)
    output['events'] = [dict(e, learned_selection={'probability': float(scores[i]), 'role': reasons[i]})
                        for i, e in enumerate(events) if i in selected]
    output['schema'] = 'kgraphier-selected-subgraph-1'
    output['candidate_id'] = graph['id']
    output['selection_config'] = {'budget': budget, 'threshold': threshold}
    output['selection_diagnostics'] = {'candidate_events': len(events), 'selected_events': len(selected),
                                       'budget_rejections': rejected, 'unreachable_events': len(events)-len(parents)}
    output['id'] = fingerprint([graph['id'], output['selection_config'], [(e['event_id'], e['learned_selection']) for e in output['events']]])
    return output
