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


import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / "eval"))     # reuse rescore's pass/label logic, do not reimplement


def answerable_figures(run_path, config: str | None = None, corrected: bool = False) -> dict:
    recs = json.loads(Path(run_path).read_text(encoding="utf-8"))
    rows = [r for r in recs if r.get("answerable")]
    if config is not None:
        rows = [r for r in rows if r.get("config") == config]
    if corrected:
        from rescore import current_labels, recompute_pass       # eval/rescore.py
        labels = current_labels()
        passes = sum(recompute_pass(r, labels.get(r["id"], r["expected"])) for r in rows)
    else:
        passes = sum(bool(r["pass"]) for r in rows)
    recalls = [r["recall"] for r in rows if r.get("recall") is not None]
    recall = round(sum(recalls) / len(recalls), 2) if recalls else 0.0
    n = len(rows)
    return {"n": n, "passes": passes, "pct": round(100 * passes / n) if n else 0, "recall": recall}


def strip_metrics() -> dict:
    base = answerable_figures(_ROOT / "eval" / "last_run.json", config="hybrid_rerank")
    p8b = answerable_figures(_ROOT / "eval" / "last_run_phase8b.json")
    p8b_c = answerable_figures(_ROOT / "eval" / "last_run_phase8b.json", corrected=True)
    src_base = "eval/last_run.json (hybrid_rerank, answerable, n=%d)" % base["n"]
    src_after = "eval/last_run_phase8b.json (answerable, n=%d); py eval/rescore.py" % p8b["n"]
    bm = {"before": base["pct"], "after": p8b["pct"], "source": src_base + " -> " + src_after}
    bl = {"before": p8b["pct"], "after": p8b_c["pct"],
          "source": "eval/phase8b_findings.md l.89; py eval/rescore.py"}
    return {
        "basis": "hybrid_rerank, answerable subset, n=%d (same ids both runs)" % base["n"],
        "recall": {"before": base["recall"], "after": p8b["recall"],
                   "source": src_base + " -> " + src_after},
        "behaviour_measured": bm,
        "behaviour_labels_fixed": bl,
        "cross_lingual_recovery": {"recovered": 5, "of": 6,
                                   "source": "BUILD_JOURNAL.md pool-probe (P8 retraction)"},
    }
