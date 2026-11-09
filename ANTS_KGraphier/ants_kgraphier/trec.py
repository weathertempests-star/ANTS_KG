"""TREC §3.1.2-inspired event-centred, ordinal-monotone branch sampling.

Adaptations: fixed Registry anchor instead of highest-degree anomalous process;
explicit operation POIs instead of learned GNN/iForest NOIs; event-transition
hops instead of entity hops; bounded fanout and total events. Retain every
visited probe including non-POI events, as in the paper's visited-node policy.
"""
POI_OPERATIONS = frozenset({
    'RegSetValue', 'RegCreateKey', 'RegDeleteKey', 'RegDeleteValue',
    'Process Create',
})
VERSION = 'trec-event-1'


def sample(db, rec, anchor, hops, fanout, budget, mode):
    from .extract import neighbors
    selected = {anchor['row']: anchor}
    reasons = {anchor['row']: dict(reason='anchor', parent_row=None, direction='anchor', hop=0)}
    stats = dict(policy_version=VERSION, poi_operations=sorted(POI_OPERATIONS),
                 poi_hits=0, branch_stops=0, fanout_truncations=0, budget_truncated=False,
                 expanded_states=0)
    if anchor['ord'] is None:
        return selected, reasons, stats
    directions = ['before', 'after'] if mode == 'offline' else ['before']
    # Independent branch stacks interleaved across directions to avoid exhausting
    # the whole budget on the first temporal direction. DFS within each side.
    stacks = {d:[(anchor, 0, 0)] for d in directions}
    expanded = {}
    while any(stacks.values()):
        for direction in directions:
            if not stacks[direction]:
                continue
            parent, gap, depth = stacks[direction].pop()
            key = (parent['row'], direction)
            if gap >= hops:
                stats['branch_stops'] += 1
                continue
            if key in expanded and expanded[key] <= gap:
                continue
            expanded[key] = gap
            stats['expanded_states'] += 1
            found = {}
            for endpoint in sorted({parent['src'], parent['dst']}):
                rows = neighbors(db, rec, endpoint, parent['ord'], direction, fanout+1)
                stats['fanout_truncations'] += len(rows) > fanout
                for row in rows[:fanout]:
                    found.setdefault(row['row'], (row, endpoint))
            candidates = sorted(found.values(), key=lambda item: (abs(item[0]['ord']-anchor['ord']), item[0]['row']))
            pending = []
            for candidate, via in candidates:
                rid = candidate['row']
                poi = candidate['op'] in POI_OPERATIONS
                next_gap = 0 if poi else gap+1
                if rid not in selected:
                    if len(selected) >= budget:
                        stats['budget_truncated'] = True
                        continue
                    selected[rid] = candidate
                    stats['poi_hits'] += poi
                    reasons[rid] = dict(reason='poi' if poi else 'probe_context',
                                        parent_row=parent['row'], via=via, direction=direction,
                                        hop=depth+1, gap_since_poi=next_gap)
                pending.append((candidate,next_gap,depth+1))
            stacks[direction].extend(reversed(pending))
    return selected, reasons, stats
