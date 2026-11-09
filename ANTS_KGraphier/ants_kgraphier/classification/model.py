"""Allowlisted incidence features; two-layer relation-specific mean R-GCN."""
import numpy as np
import torch
from torch import nn
from ..extract import symbolic


def vocabulary(data):
    nodes = [n for g, _ in data if g['split'] == 'train' for n in symbolic(g)['nodes'].values()]
    return {key: ['<Unknown>'] + sorted({n[key] for n in nodes} - {'<Unknown>'})
            for key in ('kind', 'operation')} | {
                'knowledge': sorted({k for n in nodes for k in n['knowledge']})}


def encode(graph, vocab, use_kg=True):
    graph_view = symbolic(graph)
    nodes = graph_view['nodes']
    indices = {key: i for i, key in enumerate(nodes)}
    maps = {k: {v: i for i, v in enumerate(values)} for k, values in vocab.items()}
    width = sum(map(len, vocab.values())) + 1
    x = np.zeros((len(nodes), width), dtype=np.float32)
    events, anchor = [], None
    for key, node in nodes.items():
        i, offset = indices[key], 0
        for field in ('kind', 'operation'):
            x[i, offset + maps[field].get(node[field], 0)] = 1
            offset += len(vocab[field])
        if use_kg:
            for kg in node['knowledge']:
                if kg in maps['knowledge']:
                    x[i, offset + maps['knowledge'][kg]] = 1
        x[i, -1] = node['anchor']
        if node['kind'] == 'Event':
            events.append(i)
        if node['anchor']:
            anchor = i
    # Prefix context also belongs to its event, allowing the no-message/anchor
    # controls to use the same KG evidence without identities or raw strings.
    for e in graph['events']:
        if use_kg and e.get('knowledge'):
            for kg in e['knowledge']['node_ids']:
                if kg in maps['knowledge']:
                    x[indices['event:' + str(e['row'])], len(vocab['kind']) + len(vocab['operation']) + maps['knowledge'][kg]] = 1
    edges = [(indices[a], indices[b], r) for a, b, r in graph_view['edges']]
    edges += [(b, a, r + 3) for a, b, r in edges.copy()]
    edge = torch.tensor(edges, dtype=torch.long).T if edges else torch.empty(3, 0, dtype=torch.long)
    if anchor is None or not events:
        raise ValueError('graph requires an anchor event')
    return torch.from_numpy(x), edge, torch.tensor(events), anchor


class Classifier(nn.Module):
    def __init__(self, width, classes, mode='rgcn'):
        super().__init__()
        self.mode = mode
        if mode == 'counts':
            self.linear = nn.Linear(width, 1 + classes)
        else:
            self.input = nn.Linear(width, 64)
            self.self_layers = nn.ModuleList(nn.Linear(64, 64) for _ in range(2))
            self.relations = nn.ModuleList(nn.ModuleList(nn.Linear(64, 64, bias=False) for _ in range(6)) for _ in range(2))
            self.dropout = nn.Dropout(.2)
            self.binary = nn.Sequential(nn.Linear(192, 64), nn.ReLU(), nn.Linear(64, 1))
            self.technique = nn.Sequential(nn.Linear(192, 64), nn.ReLU(), nn.Linear(64, classes)) if classes else None

    def forward(self, encoded):
        return self.forward_batch([encoded])[0]

    def forward_batch(self, graphs):
        # Disjoint-union batching, with no padding or edges between graphs.
        device = next(self.parameters()).device
        xs, edges, event_indices, event_batches, node_batches, anchors = [], [], [], [], [], []
        offset = 0
        for batch, (x, edge, events, anchor) in enumerate(graphs):
            xs.append(x.to(device))
            shifted = edge.to(device).clone()
            shifted[:2] += offset
            edges.append(shifted)
            event_indices.append(events.to(device) + offset)
            event_batches.append(torch.full((len(events),), batch, dtype=torch.long, device=device))
            node_batches.append(torch.full((len(x),), batch, dtype=torch.long, device=device))
            anchors.append(anchor + offset)
            offset += len(x)
        x, edge = torch.cat(xs), torch.cat(edges, dim=1)
        event_index, event_batch = torch.cat(event_indices), torch.cat(event_batches)
        if self.mode == 'counts':
            counts = x.new_zeros((len(graphs), x.shape[1]))
            counts.index_add_(0, torch.cat(node_batches), x)
            return self.linear(counts)
        h = self.input(x).relu()
        if self.mode == 'rgcn':
            for own, relations in zip(self.self_layers, self.relations):
                updated = own(h)
                for r, layer in enumerate(relations):
                    source, target = edge[:2, edge[2] == r]
                    total = torch.zeros_like(h)
                    degree = torch.zeros(len(h), device=h.device)
                    total.index_add_(0, target, layer(h[source]))
                    degree.index_add_(0, target, torch.ones(len(target), device=h.device))
                    updated = updated + total / degree.clamp_min(1).unsqueeze(1)
                h = self.dropout(updated.relu())
        if self.mode == 'anchor':
            pooled = h[anchors].repeat(1, 3)
        else:
            event_h = h[event_index]
            mean = h.new_zeros((len(graphs), 64))
            mean.index_add_(0, event_batch, event_h)
            mean = mean / torch.bincount(event_batch, minlength=len(graphs)).unsqueeze(1)
            maximum = h.new_full((len(graphs), 64), float('-inf'))
            maximum.scatter_reduce_(0, event_batch.unsqueeze(1).expand(-1,64), event_h, reduce='amax')
            pooled = torch.cat((mean, maximum, h[anchors]), dim=1)
        return torch.cat((self.binary(pooled), self.technique(pooled) if self.technique else h.new_empty((len(graphs),0))), dim=1)


def targets(label, classes):
    values = [float(label['binary'] or 0)] + [float(t in label['techniques']) for t in classes]
    mask = [label['binary'] is not None] + [label['complete'] or t in label['techniques'] for t in classes]
    return torch.tensor(values), torch.tensor(mask, dtype=torch.float32)


def positive_weights(data, classes):
    pairs = [targets(a, classes) for _, a in data]
    y, mask = (torch.stack([p[i] for p in pairs]) for i in range(2))
    positive = (y * mask).sum(0)
    negative = ((1-y) * mask).sum(0)
    return (negative / positive.clamp_min(1)).clamp(max=20)
