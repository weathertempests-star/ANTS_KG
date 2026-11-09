"""Anchor-conditioned sparse event encoder and stochastic membership masks.

GSAT-inspired Bernoulli bottleneck, not an implementation of the GSAT paper's
classification objective. Raw identities are used only to construct adjacency.
"""
import hashlib
import math

import torch
from torch import nn

FEATURE_DIM = 128


def bucket(value, width):
    return int.from_bytes(hashlib.sha256(value.encode()).digest()[:8], 'big') % width


def encode(graph, use_kg=True):
    events = graph['events']
    x = torch.zeros(len(events), FEATURE_DIM)
    anchor = next(i for i, e in enumerate(events) if e['event_id'] == graph['anchor_event_id'])
    # Consecutive interactions per endpoint: sparse, bidirectional message edges.
    # Directional ordering is encoded in separate forward/reverse channels.
    endpoints = {}
    for i, e in enumerate(events):
        for value in ('op:' + e['op'], 'src:' + e['src_type'], 'dst:' + e['dst_type']):
            x[i, bucket(value, 64)] += 1
        if use_kg and e.get('knowledge'):
            for key in e['knowledge']['node_ids']:
                x[i, 64 + bucket(key, 48)] = 1
        x[i, 112] = i == anchor
        ao, eo = events[anchor]['ord'], e['ord']
        if ao is not None and eo is not None:
            x[i, 113] = math.copysign(math.log1p(abs(eo - ao)), eo - ao) if eo != ao else 0
            x[i, 114] = eo == ao
        else:
            x[i, 115] = 1
        for endpoint in {e['src'], e['dst']}:
            endpoints.setdefault(endpoint, []).append(i)
    edges = set()
    for indices in endpoints.values():
        ordered = sorted((i for i in indices if events[i]['ord'] is not None), key=lambda i: (events[i]['ord'], events[i]['row']))
        # Ties do not establish temporal precedence.
        for left, right in zip(ordered, ordered[1:]):
            if events[left]['ord'] < events[right]['ord']:
                edges.add((left, right))
    edge = torch.tensor(sorted(edges), dtype=torch.long).t().contiguous() if edges else torch.empty((2, 0), dtype=torch.long)
    return x, edge, anchor


class Selector(nn.Module):
    def __init__(self, hidden=64):
        super().__init__()
        self.hidden = hidden
        self.input = nn.Linear(FEATURE_DIM, hidden)
        self.layers = nn.ModuleList([nn.Linear(hidden * 3, hidden) for _ in range(2)])
        self.score = nn.Sequential(nn.Linear(hidden * 3, hidden), nn.ReLU(), nn.Linear(hidden, 1))

    def representations(self, x, edges):
        h = self.input(x).relu()
        for layer in self.layers:
            channels = [h]
            for source, target in (edges, edges.flip(0)):
                aggregate = torch.zeros_like(h)
                degree = torch.zeros(len(h), device=h.device)
                aggregate.index_add_(0, target, h[source])
                degree.index_add_(0, target, torch.ones(len(target), device=h.device))
                channels.append(aggregate / degree.clamp_min(1).unsqueeze(1))
            h = layer(torch.cat(channels, dim=1)).relu()
        return h

    def forward(self, x, edges, anchor):
        h = self.representations(x, edges)
        a = h[anchor].expand_as(h)
        return self.score(torch.cat([h, a, abs(h - a)], dim=1)).flatten()


def stochastic_mask(logits, temperature=0.67, training=True):
    if temperature <= 0:
        raise ValueError('temperature must be positive')
    if not training:
        return logits.sigmoid()
    u = torch.rand_like(logits).clamp(1e-6, 1 - 1e-6)
    return ((logits + u.log() - torch.log1p(-u)) / temperature).sigmoid()


def bernoulli_kl(logits, prior=0.2):
    if not 0 < prior < 1:
        raise ValueError('prior must be in (0,1)')
    p = logits.sigmoid().clamp(1e-6, 1 - 1e-6)
    return (p * (p.log() - math.log(prior)) + (1-p) * (torch.log1p(-p) - math.log1p(-prior))).mean()
