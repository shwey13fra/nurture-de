"""Phase-12 pure helpers: serialise traces, extract eval figures, assemble the hero, inject the
page data. No API and no models — all unit-testable. The generator (build_visualiser_traces.py)
is the only thing that touches the graph, the retriever, and the eval run files."""
from __future__ import annotations
from dataclasses import asdict


def chunk_summary(chunk) -> dict:
    m = chunk.metadata or {}
    return {"chunk_id": chunk.chunk_id, "source_id": m.get("source_id", ""),
            "language": m.get("language", ""), "authority": m.get("authority", ""),
            "last_verified": m.get("last_verified_date", ""), "score": round(float(chunk.score), 4)}


def serialize_retrieval_trace(rt) -> dict:
    d = asdict(rt)                       # RetrievalTrace is a plain dataclass of lists/dicts
    return d


def serialize_graph_trace(tr) -> dict:
    return {"nodes": tr.nodes, "branch_intent": tr.branch_intent,
            "branch_profile": tr.branch_profile, "retries": tr.retries,
            "final_node": tr.final_node, "filter_starved": tr.filter_starved,
            "node_timings": tr.node_timings,
            "retrievals": [serialize_retrieval_trace(r) for r in tr.retrievals]}
