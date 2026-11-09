"""Train-only masked operation reconstruction over streamed candidate events.

Includes all entity types in each candidate. Does not claim to cover events
outside the candidate corpus. Labels and membership annotations are not read.
"""
import torch
from torch.nn import functional as F
from ..io import jsonl
from .model import encode, bucket


def pretrain(model, graph_path, epochs, use_kg=True, device='cpu', lr=.001):
    if epochs < 0:
        raise ValueError('pretrain epochs cannot be negative')
    if not epochs:
        return []
    head = torch.nn.Linear(model.hidden, 64).to(device)
    parameters = list(model.input.parameters()) + list(model.layers.parameters()) + list(head.parameters())
    optimizer = torch.optim.Adam(parameters, lr=lr)
    history = []
    for epoch in range(epochs):
        model.train()
        total_loss, count, events = 0., 0, 0
        for graph in jsonl(graph_path):
            if graph['split'] != 'train':
                continue
            x, edges, _ = encode(graph, use_kg)
            x, edges = x.to(device), edges.to(device)
            mask = torch.rand(len(x), device=device) < .2
            if not mask.any():
                mask[torch.randint(len(x), (1,), device=device)] = True
            # Entire categorical block removed to prevent the operation target
            # leaking through the hashed source/destination feature collisions.
            x[mask, :64] = 0
            labels = torch.tensor([bucket('op:'+e['op'],64) for e in graph['events']], device=device)
            optimizer.zero_grad()
            logits = head(model.representations(x, edges))
            loss = F.cross_entropy(logits[mask], labels[mask])
            loss.backward()
            torch.nn.utils.clip_grad_norm_(parameters, 5.)
            optimizer.step()
            total_loss += float(loss.detach()); count += 1; events += len(x)
        if not count:
            raise ValueError('no training candidates for pretraining')
        history.append(dict(epoch=epoch+1, loss=total_loss/count, graphs=count, event_occurrences=events))
    return history
