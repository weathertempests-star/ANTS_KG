"""Versioned Registry retrieval with public one-hop expansion and label-free caching."""

import copy
import json
from pathlib import Path
import sqlite3

from ..common.files import canonical, file_hash, object_hash
from .engine import KnowledgeBase

DEFAULT_SNAPSHOT = Path(__file__).resolve().parents[1] / "resources/kg.json"


class KnowledgeRepository:
    def __init__(self, snapshot=DEFAULT_SNAPSHOT, cache_path=None):
        self.snapshot = Path(snapshot)
        self.hash = file_hash(snapshot)
        self.engine = KnowledgeBase.load(snapshot)
        graph = self.engine.to_dict()
        self.nodes = {n["id"]: n for n in graph["nodes"]}
        self.edges = graph.get("semantic_edges", [])
        self.cache = None
        if cache_path:
            Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
            self.cache = sqlite3.connect(cache_path)
            self.cache.execute("CREATE TABLE IF NOT EXISTS knowledge_cache (key TEXT PRIMARY KEY, payload TEXT, payload_hash TEXT)")
            self.cache.commit()

    def close(self):
        if self.cache:
            self.cache.close()

    def node(self, node_id):
        node = self.nodes[node_id]
        return copy.deepcopy({k: node[k] for k in ("id", "path", "depth", "parent_id", "status", "explanation",
                             "explanation_sources", "path_sources", "research", "template_dependent")})

    def lookup(self, registry, template_candidates=False):
        query = {"snapshot": self.hash, "registry": registry, "template_candidates": template_candidates,
                 "adapter_version": "knowledge-repository-1"}
        key = object_hash(query)
        if self.cache:
            cached = self.cache.execute("SELECT payload,payload_hash FROM knowledge_cache WHERE key=?", (key,)).fetchone()
            if cached:
                result = json.loads(cached[0])
                if object_hash(result) != cached[1]:
                    raise ValueError("Knowledge cache payload integrity failure")
                return result
        target = registry.get("lookup_target")
        if not target:
            result = {"snapshot_hash": self.hash, "match": "missing_target", "nodes": [], "relations": [],
                      "path_complete": False, "explanations_complete": False, "boundary_status": registry["boundary_status"]}
        else:
            context = self.engine.model_context(target, value_name=registry.get("value_name"),
                                               path_format=registry["path_format"], template_candidates=template_candidates)
            ambiguous = registry["boundary_status"] not in {"key_confirmed", "value_confirmed"}
            if ambiguous:
                match = "boundary_unresolved"
            elif context["path_complete"]:
                match = "exact"
            elif context["pattern_complete"]:
                match = "template"
            else:
                match = "ancestor" if context["prefix_knowledge"] else "unknown"
            result = {"snapshot_hash": self.hash, "match": match, "boundary_status": registry["boundary_status"],
                      **{k: context[k] for k in ("path_complete", "explanations_complete", "pattern_complete",
                           "pattern_explanations_complete", "template_bindings", "unknown_components", "warnings", "value_knowledge", "inference_boundary")},
                      "nodes": [self.node(n["id"]) for n in context["prefix_knowledge"]],
                      "relations": copy.deepcopy(context["semantic_edges"])}
            if ambiguous:
                result["raw_prefix_path_complete"] = result["path_complete"]
                result["path_complete"] = False
                result["pattern_complete"] = False
                result["explanations_complete"] = False
                result["pattern_explanations_complete"] = False
                result["warnings"].append("Key/value boundary unconfirmed; prefix knowledge does not establish the terminal key or value semantics.")
        if self.cache:
            self.cache.execute("INSERT OR REPLACE INTO knowledge_cache VALUES(?,?,?)", (key, canonical(result), object_hash(result)))
            self.cache.commit()
        return result

    def expand(self, seed_ids):
        if not set(seed_ids) <= self.nodes.keys():
            raise ValueError("Unknown knowledge seed")
        seeds = set(seed_ids)
        edges = [e for e in self.edges if e["source"] in seeds or e["target"] in seeds]
        neighbors = {e[endpoint] for e in edges for endpoint in ("source", "target")}
        return {"snapshot_hash": self.hash, "nodes": [self.node(n) for n in sorted(neighbors)],
                "relations": copy.deepcopy(edges), "hops": 1}
