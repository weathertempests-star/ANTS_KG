"""Load the pinned upstream model definitions without its DARPA data loaders.

The AST class bodies are executed unchanged. Only dependency namespaces are
supplied locally: utils.get_device (CPU), feature augmentation (disabled).
This is an adapter to real upstream classes, not a replacement toy encoder.
"""
import ast
from pathlib import Path
from types import SimpleNamespace

from .io import digest

UPSTREAM_COMMIT = "ac85b4e4e6f387cbf3bd8b94c87c62015f7440bb"
MODEL_SHA256 = "163be3867a12135afbefe18c981a4323b9cde326fc9b07c70253d48a225d6988"
CLASSES = {"OrderEmbedder", "SkipLastGNN", "ConvEdgeType", "SAGEConv", "GINConv"}


def load_classes(vendor):
    import torch
    import torch_geometric.nn as pyg_nn
    import torch_geometric.utils as pyg_utils
    import pickle
    path = Path(vendor) / "common/models.py"
    if digest(path) != MODEL_SHA256:
        raise ValueError("upstream model hash differs from audited commit")
    tree = ast.parse(path.read_text(), filename=str(path))
    bodies = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name in CLASSES]
    if {node.name for node in bodies} != CLASSES:
        raise ValueError("upstream model definitions incomplete")
    namespace = {"torch": torch, "nn": torch.nn, "F": torch.nn.functional,
                 "pyg_nn": pyg_nn, "pyg_utils": pyg_utils, "pc": pickle,
                 "utils": SimpleNamespace(get_device=lambda: torch.device("cpu")),
                 "feature_preprocess": SimpleNamespace(FEATURE_AUGMENT=[])}
    exec(compile(ast.Module(body=bodies, type_ignores=[]), str(path), "exec"), namespace)
    return namespace


def make_model(vendor, input_dim, hidden=32, layers=2):
    ns = load_classes(vendor)
    args = SimpleNamespace(dropout=0.0, n_layers=layers, conv_type="SAGE_typed",
                           skip="learnable", n_edge_type=3, pool="mean",
                           batch_size=32, margin=1.0)
    return ns["OrderEmbedder"](input_dim, hidden, args)


class Features:
    def __init__(self, kg_ids, operations, use_kg=True):
        self.kg_ids = sorted(kg_ids)
        self.operations = sorted(operations)
        self.use_kg = use_kg
        self.kinds = ["Event", "Process", "Registry", "File", "Network", "Missing", "Unknown"]
        self.kg_map = {v: i for i, v in enumerate(self.kg_ids)}
        self.op_map = {v: i for i, v in enumerate(self.operations)}
        self.dim = 1 + len(self.kinds) + len(self.operations) + 1 + len(self.kg_ids)

    def config(self):
        return dict(kg_ids=self.kg_ids, operations=self.operations, use_kg=self.use_kg)

    def encode(self, graph):
        import torch
        from torch_geometric.data import Data
        names = sorted(graph["nodes"])
        indices = {name: i for i, name in enumerate(names)}
        x = torch.zeros((len(names), self.dim))
        op_start = 1 + len(self.kinds)
        kg_start = op_start + len(self.operations) + 1
        for i, name in enumerate(names):
            node = graph["nodes"][name]
            x[i, 0] = float(node["anchor"])
            kind = node["kind"] if node["kind"] in self.kinds else "Unknown"
            x[i, 1 + self.kinds.index(kind)] = 1
            if node["kind"] == "Event":
                x[i, op_start + self.op_map.get(node["operation"], len(self.operations))] = 1
            if self.use_kg:
                for kid in node["knowledge"]:
                    if kid in self.kg_map:
                        x[i, kg_start + self.kg_map[kid]] = 1
        edges = graph["edges"]
        edge_index = torch.tensor([[indices[a], indices[b]] for a, b, _ in edges], dtype=torch.long).t().contiguous()
        if not edges:
            edge_index = torch.empty((2, 0), dtype=torch.long)
        return Data(node_feature=x, edge_index=edge_index,
                    type_edge=torch.tensor([t for _, _, t in edges], dtype=torch.long), num_nodes=len(names))
