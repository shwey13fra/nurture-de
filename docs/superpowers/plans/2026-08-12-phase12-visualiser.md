# Phase 12 — Pipeline Visualiser Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A single self-contained, theme-aware HTML page that makes NurtureDE's decision pipeline legible to a stranger in ninety seconds — rendered entirely from pre-recorded trace JSON, no server, no clone, no wait.

**Architecture:** Two units, one direction of flow. An **offline generator** (`src/tools/build_visualiser_traces.py`) runs the four canonical scenarios through the existing `graph.run()`, builds the cross-lingual before/after hero via direct retriever calls, extracts the strip figures from the eval JSONs, and writes everything to `docs/visualiser/traces.json`; it then injects that JSON into a hand-authored template to produce the self-contained `docs/visualiser/index.html`. The **page** only renders what was persisted — it never computes. Pure serialisation / figure-extraction logic is factored into `src/tools/visualiser_serialize.py` so it is unit-testable without any API call.

**Tech Stack:** Python 3.11 (`.venv/Scripts/python.exe`), `unittest` (repo convention — NOT pytest), existing `graph.py` + `retrieval.py` (unchanged), plain HTML + inline CSS + inline vanilla JS (no framework, no build step beyond the generator).

## Global Constraints

- **Test runner:** `unittest`, invoked as `.venv/Scripts/python.exe -m unittest tests.test_visualiser -v`. Match `tests/test_graph_routing.py` style (add `src/` and repo root to `sys.path`).
- **Reuse, no retrofit:** `graph.py` and `retrieval.py` are consumed **unchanged**. Do not modify them.
- **Self-contained page:** `index.html` makes **zero external requests** (Artifact CSP + `file://` both must work). All CSS/JS inline; the trace data embedded in a `<script id="traces" type="application/json">` block.
- **Every number traces to a file:** no metric literal (`0.75`, `0.85`, `0.90`, `38%`, `58%`, `65%`, `69%`, `77%`, `86%`) may be hand-typed in `template.html`. Every displayed figure arrives via `traces.json`, which the generator computes from `eval/*.json` / `BUILD_JOURNAL.md`. A test enforces this. If a figure has no file behind it, it is dropped, not rounded.
- **Strip basis (verbatim from spec):** `hybrid_rerank`, answerable subset, **n=26 (same 26 case ids in both runs, verified)**. recall `0.75 → 0.90`; behaviour `38% → 58%` (as measured), `58% → 69%` (after five golden-label corrections). `0.85` and the all-43 `65%→77%` are NOT used.
- **Delivery:** `index.html` + `traces.json` committed to the repo; `index.html` is also publishable as an Artifact (theme-token CSS already satisfies the Artifact contract).
- **Cost:** `--generate` costs ~$0.23 API + ~10 min CPU rerank; run once. `--reuse` (design iteration) and all figure extraction are free/offline.

---

## File Structure

- `src/tools/visualiser_serialize.py` — **pure** functions: dataclass→dict serialisers, eval-figure extractors, hero assembly, template injection. No API, no models. Fully unit-tested.
- `src/tools/build_visualiser_traces.py` — CLI orchestrator. Runs scenarios (API) + hero (models), assembles the traces dict via `visualiser_serialize`, writes `traces.json`, injects into `template.html` → `index.html`. `--reuse` skips the API and only re-injects.
- `docs/visualiser/template.html` — hand-authored page: structure + inline theme-aware CSS + inline render JS, with a `<script id="traces" type="application/json">/*__TRACES__*/</script>` placeholder. Contains **no metric literals**.
- `docs/visualiser/traces.json` — generated data (versioned; the page's only data source, and the audit-friendly readable copy).
- `docs/visualiser/index.html` — generated self-contained page (versioned; the shippable/Artifact artifact).
- `tests/test_visualiser.py` — unittest suite for the pure layer + the no-hand-typed-numbers guard + embed-sync.

---

## Task 1: Trace serialisers (pure)

**Files:**
- Create: `src/tools/visualiser_serialize.py`
- Test: `tests/test_visualiser.py`

**Interfaces:**
- Consumes: `retrieval.RetrievedChunk`, `retrieval.RetrievalTrace`, `graph.GraphTrace` (existing dataclasses).
- Produces:
  - `chunk_summary(chunk: RetrievedChunk) -> dict` → `{chunk_id, source_id, language, authority, last_verified, score}`
  - `serialize_retrieval_trace(rt: RetrievalTrace) -> dict` → the funnel dict (query, mode, filters, dense, sparse, fused, filter_exclusions, both, rerank, final_context, context_tokens, underfilled, timings_ms)
  - `serialize_graph_trace(tr: GraphTrace) -> dict` → `{nodes, branch_intent, branch_profile, retries, final_node, filter_starved, node_timings, retrievals: [serialize_retrieval_trace(r) ...]}`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_visualiser.py
import sys, unittest
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))

from retrieval import RetrievedChunk, RetrievalTrace          # noqa: E402
from graph import GraphTrace                                  # noqa: E402
from tools.visualiser_serialize import (                      # noqa: E402
    chunk_summary, serialize_retrieval_trace, serialize_graph_trace)


class TestSerialisers(unittest.TestCase):
    def _chunk(self):
        return RetrievedChunk("fam_mutterschutz__x__abc", "text here", 0.4213,
                              {"source_id": "fam_mutterschutz", "language": "de",
                               "authority": "Familienportal", "last_verified_date": "2026-08-03"})

    def test_chunk_summary_picks_display_fields(self):
        s = chunk_summary(self._chunk())
        self.assertEqual(s["source_id"], "fam_mutterschutz")
        self.assertEqual(s["language"], "de")
        self.assertEqual(s["chunk_id"], "fam_mutterschutz__x__abc")
        self.assertEqual(s["score"], 0.4213)
        self.assertNotIn("text", s)          # never ship chunk text to the page

    def test_serialize_retrieval_trace_roundtrips_funnel(self):
        rt = RetrievalTrace(query="q", mode="hybrid")
        rt.final_context = ["a", "b"]
        rt.timings_ms = {"total_ms": 165000.0}
        d = serialize_retrieval_trace(rt)
        self.assertEqual(d["final_context"], ["a", "b"])
        self.assertEqual(d["timings_ms"]["total_ms"], 165000.0)
        self.assertEqual(d["query"], "q")

    def test_serialize_graph_trace_embeds_retrievals(self):
        tr = GraphTrace()
        tr.visit("classify_intent", branch="informational")
        tr.node_timings = [{"node": "classify_intent", "ms": 1900.0}]
        tr.final_node = "verify_citations"
        rt = RetrievalTrace(query="q", mode="hybrid"); rt.final_context = ["a"]
        tr.retrievals.append(rt)
        d = serialize_graph_trace(tr)
        self.assertEqual(d["final_node"], "verify_citations")
        self.assertEqual(d["node_timings"][0]["node"], "classify_intent")
        self.assertEqual(len(d["retrievals"]), 1)
        self.assertEqual(d["retrievals"][0]["final_context"], ["a"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe -m unittest tests.test_visualiser.TestSerialisers -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'tools.visualiser_serialize'`

- [ ] **Step 3: Write minimal implementation**

```python
# src/tools/visualiser_serialize.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python.exe -m unittest tests.test_visualiser.TestSerialisers -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add src/tools/visualiser_serialize.py tests/test_visualiser.py
git commit -m "Phase 12 Task 1: pure trace serialisers for the visualiser"
```

---

## Task 2: Eval-figure extractors (pure, against the real run files)

**Files:**
- Modify: `src/tools/visualiser_serialize.py`
- Modify: `tests/test_visualiser.py`

**Interfaces:**
- Consumes: `eval/last_run.json`, `eval/last_run_phase8b.json`, `eval/golden.jsonl`, `eval/rescore.py` (`recompute_pass`, `current_labels`).
- Produces:
  - `answerable_figures(run_path: Path, config: str | None = None, corrected: bool = False) -> dict` → `{"n": int, "passes": int, "pct": int, "recall": float}`. `corrected=True` recomputes `pass` against the CURRENT golden labels (mirrors `rescore.py`); otherwise uses the recorded `pass`.
  - `strip_metrics() -> dict` → the exact figures the page shows, each with a `source` string. Closes the "baseline 0.75/38% is terminal-only" gap by writing them to a file.

- [ ] **Step 1: Write the failing test**

```python
# add to tests/test_visualiser.py
from tools.visualiser_serialize import answerable_figures, strip_metrics   # noqa: E402
_EVAL = _ROOT / "eval"

class TestEvalFigures(unittest.TestCase):
    def test_baseline_hybrid_rerank_answerable(self):
        f = answerable_figures(_EVAL / "last_run.json", config="hybrid_rerank")
        self.assertEqual(f["n"], 26)
        self.assertEqual(f["pct"], 38)          # 10/26 as-measured
        self.assertEqual(f["recall"], 0.75)

    def test_phase8b_answerable_measured_and_corrected(self):
        m = answerable_figures(_EVAL / "last_run_phase8b.json")
        self.assertEqual(m["n"], 26)
        self.assertEqual(m["pct"], 58)          # 15/26 as-measured
        self.assertEqual(m["recall"], 0.90)
        c = answerable_figures(_EVAL / "last_run_phase8b.json", corrected=True)
        self.assertEqual(c["pct"], 69)          # 18/26 after 5 relabels

    def test_strip_metrics_shape_and_values(self):
        s = strip_metrics()
        self.assertEqual(s["recall"]["before"], 0.75)
        self.assertEqual(s["recall"]["after"], 0.90)
        self.assertEqual(s["behaviour_measured"], {"before": 38, "after": 58})
        self.assertEqual(s["behaviour_labels_fixed"], {"before": 58, "after": 69})
        self.assertEqual(s["cross_lingual_recovery"], {"recovered": 5, "of": 6})
        for k in ("recall", "behaviour_measured", "behaviour_labels_fixed"):
            self.assertIn("source", s[k])        # every figure names its file
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe -m unittest tests.test_visualiser.TestEvalFigures -v`
Expected: FAIL — `ImportError: cannot import name 'answerable_figures'`

- [ ] **Step 3: Write minimal implementation**

```python
# add to src/tools/visualiser_serialize.py
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
    return {
        "basis": "hybrid_rerank, answerable subset, n=%d (same ids both runs)" % base["n"],
        "recall": {"before": base["recall"], "after": p8b["recall"],
                   "source": src_base + " -> " + src_after},
        "behaviour_measured": {"before": base["pct"], "after": p8b["pct"]},
        "behaviour_labels_fixed": {"before": p8b["pct"], "after": p8b_c["pct"]},
        "cross_lingual_recovery": {"recovered": 5, "of": 6,
                                   "source": "BUILD_JOURNAL.md pool-probe (P8 retraction)"},
        "_source_measured": src_after, "_source_labels_fixed": src_after,
    }
```

Note: `behaviour_measured`/`behaviour_labels_fixed` carry their source via the top-level `_source_*` keys and `basis`; the test only checks `source` on `recall`, `behaviour_measured`, `behaviour_labels_fixed` — so add a `source` key to each of those three dicts:

```python
    bm = {"before": base["pct"], "after": p8b["pct"], "source": src_base + " -> " + src_after}
    bl = {"before": p8b["pct"], "after": p8b_c["pct"],
          "source": "eval/phase8b_findings.md l.89; py eval/rescore.py"}
    # ...and return bm / bl in place of the dicts above
```

Fold that into the returned dict (`"behaviour_measured": bm, "behaviour_labels_fixed": bl`).

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python.exe -m unittest tests.test_visualiser.TestEvalFigures -v`
Expected: PASS (3 tests). If `recall` shows `0.9` vs `0.90`: they are equal as floats — the test uses `0.90` which `== 0.9`.

- [ ] **Step 5: Commit**

```bash
git add src/tools/visualiser_serialize.py tests/test_visualiser.py
git commit -m "Phase 12 Task 2: eval-figure extractors — baseline 0.75/38% now written by a script (PM-1)"
```

---

## Task 3: Hero assembly (pure logic) + injection helper

**Files:**
- Modify: `src/tools/visualiser_serialize.py`
- Modify: `tests/test_visualiser.py`

**Interfaces:**
- Produces:
  - `assemble_hero(query, before_rt, after_chunks, answer_source_id, caption) -> dict` — from a *before* `RetrievalTrace` (fused ranks) and an *after* list of `RetrievedChunk`, build `{query, answer_source_id, before:{pool,items,cutoff,answer_rank}, after:{items,answer_rank}, caption}` where `items` are `chunk_summary`-shaped with an added `rank`. Raises `ValueError` unless `before.answer_rank > 3` and `after.answer_rank == 0` (the discard→recovery invariant).
  - `inject(template: str, traces: dict) -> str` — replace the `/*__TRACES__*/` placeholder inside the `<script id="traces">` block with `json.dumps(traces)`. Raises if the placeholder is absent.

- [ ] **Step 1: Write the failing test**

```python
# add to tests/test_visualiser.py
from tools.visualiser_serialize import assemble_hero, inject           # noqa: E402

class TestHeroAndInject(unittest.TestCase):
    def _c(self, cid, sid, lang, score):
        return RetrievedChunk(cid, "t", score, {"source_id": sid, "language": lang})

    def test_assemble_hero_finds_discard_and_recovery(self):
        before = RetrievalTrace(query="q", mode="hybrid")
        before.fused = [{"chunk_id": "tk__0"}, {"chunk_id": "tk__1"}, {"chunk_id": "tk__2"},
                        {"chunk_id": "tk__3"}, {"chunk_id": "x__4"}, {"chunk_id": "x__5"},
                        {"chunk_id": "fam__ans"}]                       # answer at rank 6
        before._chunks = {"tk__0": self._c("tk__0", "tk_maternity_pay", "en", .9),
                          "tk__1": self._c("tk__1", "tk_maternity_pay", "en", .8),
                          "tk__2": self._c("tk__2", "tk_maternity_benefits", "en", .7),
                          "tk__3": self._c("tk__3", "tk_maternity_pay", "en", .6),
                          "fam__ans": self._c("fam__ans", "fam_mutterschutz", "de", .5)}
        after = [self._c("fam__ans", "fam_mutterschutz", "de", .99),
                 self._c("tk__0", "tk_maternity_pay", "en", .5)]
        h = assemble_hero("q", before, after, "fam_mutterschutz", "cut by top-4")
        self.assertEqual(h["before"]["answer_rank"], 6)
        self.assertEqual(h["after"]["answer_rank"], 0)
        self.assertEqual(h["before"]["cutoff"], 4)
        self.assertEqual(h["after"]["items"][0]["source_id"], "fam_mutterschutz")

    def test_assemble_hero_rejects_non_reproducing_case(self):
        before = RetrievalTrace(query="q", mode="hybrid")
        before.fused = [{"chunk_id": "fam__ans"}]                       # answer already at rank 0
        before._chunks = {"fam__ans": self._c("fam__ans", "fam_mutterschutz", "de", .9)}
        after = [self._c("fam__ans", "fam_mutterschutz", "de", .9)]
        with self.assertRaises(ValueError):
            assemble_hero("q", before, after, "fam_mutterschutz", "c")

    def test_inject_replaces_placeholder(self):
        tpl = '<script id="traces" type="application/json">/*__TRACES__*/</script>'
        out = inject(tpl, {"a": 1})
        self.assertIn('{"a": 1}', out)
        self.assertNotIn("/*__TRACES__*/", out)

    def test_inject_requires_placeholder(self):
        with self.assertRaises(ValueError):
            inject("<html></html>", {"a": 1})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe -m unittest tests.test_visualiser.TestHeroAndInject -v`
Expected: FAIL — `ImportError: cannot import name 'assemble_hero'`

- [ ] **Step 3: Write minimal implementation**

```python
# add to src/tools/visualiser_serialize.py
_PLACEHOLDER = "/*__TRACES__*/"


def _rank_of_source(items_source_ids: list[str], source_id: str) -> int:
    for i, sid in enumerate(items_source_ids):
        if sid == source_id:
            return i
    return -1


def assemble_hero(query: str, before_rt, after_chunks, answer_source_id: str, caption: str) -> dict:
    # `before_rt._chunks` maps chunk_id -> RetrievedChunk (attached by the generator so this stays
    # pure). Build a ranked, display-only view; find the answer by source_id (chunk suffix varies).
    def item(rank, cid):
        c = before_rt._chunks.get(cid)
        base = chunk_summary(c) if c else {"chunk_id": cid, "source_id": "", "language": "",
                                           "authority": "", "last_verified": "", "score": 0.0}
        return {"rank": rank, **base}
    before_items = [item(i, f["chunk_id"]) for i, f in enumerate(before_rt.fused)]
    before_rank = _rank_of_source([it["source_id"] for it in before_items], answer_source_id)
    after_items = [{"rank": i, **chunk_summary(c)} for i, c in enumerate(after_chunks)]
    after_rank = _rank_of_source([it["source_id"] for it in after_items], answer_source_id)
    if not (before_rank > 3 and after_rank == 0):
        raise ValueError(f"hero invariant failed: before_rank={before_rank} (want >3), "
                         f"after_rank={after_rank} (want 0) for {answer_source_id!r}")
    return {"query": query, "answer_source_id": answer_source_id, "caption": caption,
            "before": {"pool": 20, "cutoff": 4, "answer_rank": before_rank,
                       "items": before_items[:max(before_rank + 1, 4)]},
            "after": {"pool": 100, "reranked": True, "answer_rank": after_rank,
                      "items": after_items[:4]}}


def inject(template: str, traces: dict) -> str:
    if _PLACEHOLDER not in template:
        raise ValueError("template is missing the /*__TRACES__*/ placeholder")
    return template.replace(_PLACEHOLDER, json.dumps(traces, ensure_ascii=False))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python.exe -m unittest tests.test_visualiser.TestHeroAndInject -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add src/tools/visualiser_serialize.py tests/test_visualiser.py
git commit -m "Phase 12 Task 3: hero assembly (discard->recovery invariant) + JSON injection"
```

---

## Task 4: The page template (structure, theme-aware CSS, render JS)

**Files:**
- Create: `docs/visualiser/template.html`
- Modify: `tests/test_visualiser.py`

**Interfaces:**
- Consumes: an embedded `traces` object of shape `{scenarios:{medical,missing,full,retry}, hero, metrics, generated_at, commit}`. Each scenario: `{path:[str], node_timings:[{node,ms}], final_node, terminated_after:int|null, retries:int, answer:{summary,citations:[str]}|null, retrievals:[...]}`.
- Produces: a static page. No exported symbols.

Load the **artifact-design** skill before the visual pass — this is a portfolio page and the visual bar matters. The code below is the functional-complete baseline; refine spacing/type/colour within these bones.

- [ ] **Step 1: Write the failing guard test**

```python
# add to tests/test_visualiser.py
_VIZ = _ROOT / "docs" / "visualiser"

class TestTemplateGuards(unittest.TestCase):
    FORBIDDEN = ["0.75", "0.85", "0.90", "0.9 ", "38%", "58%", "65%", "69%", "77%", "86%"]

    def test_template_exists_and_has_placeholder(self):
        tpl = (_VIZ / "template.html").read_text(encoding="utf-8")
        self.assertIn('id="traces"', tpl)
        self.assertIn("/*__TRACES__*/", tpl)

    def test_template_has_no_hand_typed_metric_numbers(self):
        tpl = (_VIZ / "template.html").read_text(encoding="utf-8")
        # strip the (empty) traces block defensively, then scan
        hits = [n for n in self.FORBIDDEN if n in tpl]
        self.assertEqual(hits, [], f"metric literals hand-typed in template: {hits}")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe -m unittest tests.test_visualiser.TestTemplateGuards -v`
Expected: FAIL — `FileNotFoundError` (template.html not created yet)

- [ ] **Step 3: Write the template**

Create `docs/visualiser/template.html`. This is the wrapped-page content (the Artifact publisher adds `<!doctype><head><body>`; for `file://` use the standalone form below with `<html>` included so it opens directly). Keep it one file.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NurtureDE Pipeline</title>
<style>
  :root{ --bg:#f7f7f5; --fg:#1c1c1a; --muted:#6b6b66; --line:#e0e0da; --card:#ffffff;
         --de:#2f6f4f; --en:#8a5a2b; --accent:#b4322a; --ok:#2f6f4f; --bar:#3a3a36; }
  :root:not([data-theme="light"]){ }
  @media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
         --bg:#17171a; --fg:#ececea; --muted:#9a9a94; --line:#2c2c30; --card:#1f1f23;
         --de:#7fc8a0; --en:#d6a86b; --accent:#e8756c; --ok:#7fc8a0; --bar:#c8c8c2; } }
  :root[data-theme="dark"]{ --bg:#17171a; --fg:#ececea; --muted:#9a9a94; --line:#2c2c30;
         --card:#1f1f23; --de:#7fc8a0; --en:#d6a86b; --accent:#e8756c; --ok:#7fc8a0; --bar:#c8c8c2; }
  *{ box-sizing:border-box; }
  html,body{ margin:0; }
  body{ background:var(--bg); color:var(--fg); font:15px/1.45 ui-sans-serif,system-ui,
        -apple-system,Segoe UI,Roboto,sans-serif; }
  .wrap{ max-width:1360px; margin:0 auto; padding:18px 22px; display:flex; flex-direction:column;
         gap:14px; min-height:100vh; }
  h1{ font-size:16px; font-weight:600; margin:0; letter-spacing:.2px; }
  .head{ display:flex; align-items:center; justify-content:space-between; gap:12px; }
  .btns{ display:flex; gap:6px; }
  .btns button{ font:inherit; font-size:13px; padding:5px 11px; border:1px solid var(--line);
        background:var(--card); color:var(--muted); border-radius:7px; cursor:pointer; }
  .btns button[aria-pressed="true"]{ color:var(--fg); border-color:var(--fg); font-weight:600; }
  /* Band 1 — ribbon */
  .ribbon{ display:flex; flex-wrap:wrap; align-items:center; gap:6px; padding:12px 14px;
        border:1px solid var(--line); border-radius:10px; background:var(--card); }
  .node{ font-size:12.5px; padding:4px 9px; border-radius:20px; border:1px solid var(--line);
        color:var(--muted); white-space:nowrap; }
  .node.on{ color:var(--fg); border-color:var(--fg); background:color-mix(in srgb,var(--fg) 6%,transparent); }
  .node.term{ color:var(--accent); border-color:var(--accent); }
  .sep{ color:var(--muted); font-size:12px; }
  /* Band 2 — hero */
  .hero{ flex:1; border:1px solid var(--line); border-radius:10px; background:var(--card);
        padding:16px 18px; display:flex; flex-direction:column; gap:10px; min-height:0; }
  .q{ font-size:17px; font-weight:600; }
  .qmeta{ color:var(--muted); font-size:12.5px; }
  .cols{ display:grid; grid-template-columns:1fr 1fr; gap:22px; }
  .col h3{ font-size:12px; text-transform:uppercase; letter-spacing:.6px; color:var(--muted);
        margin:0 0 6px; font-weight:600; }
  .row{ display:flex; align-items:center; gap:8px; padding:3px 0; font-size:13.5px; }
  .rk{ color:var(--muted); width:16px; text-align:right; font-variant-numeric:tabular-nums; }
  .lang{ font-size:10.5px; font-weight:700; padding:1px 5px; border-radius:4px; }
  .lang.de{ color:var(--de); border:1px solid var(--de); }
  .lang.en{ color:var(--en); border:1px solid var(--en); }
  .src{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:12.5px; }
  .cut{ border-top:1px dashed var(--line); color:var(--muted); font-size:11px; margin:5px 0;
        padding-top:4px; }
  .answer{ color:var(--accent); font-weight:600; }
  .promoted .src{ color:var(--ok); font-weight:600; }
  .caption{ font-size:13px; color:var(--fg); border-left:3px solid var(--accent);
        padding-left:10px; }
  .safety{ display:flex; flex-direction:column; gap:8px; justify-content:center; height:100%;
        text-align:center; }
  .safety .big{ font-size:20px; font-weight:600; }
  /* Band 3 — strip */
  .strip{ display:grid; grid-template-columns:1.3fr 1.4fr 1fr; gap:18px; border:1px solid var(--line);
        border-radius:10px; background:var(--card); padding:12px 16px; font-size:12.5px; }
  .lat{ display:flex; flex-direction:column; gap:5px; }
  .latbar{ display:flex; height:12px; border-radius:6px; overflow:hidden; border:1px solid var(--line); }
  .latbar span{ display:block; }
  .latbar .r{ background:var(--bar); } .latbar .g{ background:var(--en); }
  .latbar .j{ background:var(--muted); }
  .metrics b{ font-variant-numeric:tabular-nums; }
  .foot{ color:var(--muted); font-size:11px; text-align:right; }
  .retryPanel{ display:none; }
  .retryPanel.open{ display:block; }
  a.toggle{ color:var(--muted); cursor:pointer; font-size:12px; text-decoration:underline; }
</style>
</head>
<body>
<div class="wrap">
  <div class="head">
    <h1>NurtureDE — how the system decides</h1>
    <div class="btns" id="btns"></div>
  </div>
  <div class="ribbon" id="ribbon"></div>
  <div class="hero" id="hero"></div>
  <div class="strip" id="strip"></div>
  <div class="foot" id="foot"></div>
  <div class="retryPanel" id="retryPanel"></div>
</div>
<script id="traces" type="application/json">/*__TRACES__*/</script>
<script>
  const DATA = JSON.parse(document.getElementById("traces").textContent);
  const ORDER = [["medical","Medical"],["missing","Missing"],["full","Full"],["retry","Retry"]];
  const RIBBON = ["classify","profile","retrieve","grade","timeline","generate","verify"];
  let current = "full";

  function el(t, cls, txt){ const e=document.createElement(t); if(cls)e.className=cls;
    if(txt!=null)e.textContent=txt; return e; }

  function renderButtons(){
    const b=document.getElementById("btns"); b.innerHTML="";
    for(const [key,label] of ORDER){ const btn=el("button",null,label);
      btn.setAttribute("aria-pressed", key===current); btn.onclick=()=>{current=key; renderAll();};
      b.appendChild(btn); }
  }
  function renderRibbon(){
    const r=document.getElementById("ribbon"); r.innerHTML="";
    const path=(DATA.scenarios[current].path||[]).join(" ");
    RIBBON.forEach((name,i)=>{ if(i)r.appendChild(el("span","sep","→"));
      const on = path.includes(name==="profile"?"check_profile":name);
      const nd=el("span","node "+(on?"on":""), name); r.appendChild(nd); });
    const fn=DATA.scenarios[current].final_node||"";
    if(fn==="safe_referral"||fn==="request_attributes"){
      r.appendChild(el("span","sep","→")); r.appendChild(el("span","node term",fn+" ⊗")); }
  }
  function langChip(l){ const c=el("span","lang "+(l==="de"?"de":"en"), (l||"?").toUpperCase()); return c; }
  function renderHero(){
    const h=document.getElementById("hero"); h.innerHTML="";
    const sc=DATA.scenarios[current];
    if(sc.terminated_after){                       // medical / missing: safety swap
      const s=el("div","safety");
      s.appendChild(el("div","big","Terminated after "+sc.terminated_after+" nodes"));
      s.appendChild(el("div","qmeta", current==="medical"
        ? "No retrieval, no model answer — it refused to assess a medical question and referred to a doctor / 112."
        : "It asked for the missing attribute instead of guessing an answer that depends on it."));
      h.appendChild(s); return;
    }
    const H=DATA.hero;
    h.appendChild(el("div","q","“"+H.query+"”"));
    h.appendChild(el("div","qmeta","English question → German answer"));
    const cols=el("div","cols");
    const mk=(title, side, promoted)=>{ const c=el("div","col"); c.appendChild(el("h3",null,title));
      side.items.forEach(it=>{
        if(side.cutoff && it.rank===side.cutoff) c.appendChild(el("div","cut","top-4 cutoff"));
        const row=el("div","row"+(promoted&&it.rank===0?" promoted":""));
        row.appendChild(el("span","rk",it.rank));
        row.appendChild(langChip(it.language));
        const isAns = it.source_id===H.answer_source_id;
        const src=el("span","src"+(isAns&&!promoted&&it.rank>=side.cutoff?" answer":""), it.source_id);
        row.appendChild(src);
        if(isAns && promoted && it.rank===0) row.appendChild(el("span","answer"," ◀ ANSWER"));
        if(isAns && !promoted && it.rank>=side.cutoff) row.appendChild(el("span","answer"," ◀ discarded"));
        c.appendChild(row); });
      return c; };
    cols.appendChild(mk("Before — pool 20, top-4", H.before, false));
    cols.appendChild(mk("After — pool 100 + rerank", H.after, true));
    h.appendChild(cols);
    h.appendChild(el("div","caption", H.caption));
  }
  function renderStrip(){
    const s=document.getElementById("strip"); s.innerHTML="";
    const sc=DATA.scenarios[current], m=DATA.metrics;
    // latency (per scenario)
    const lat=el("div","lat"); lat.appendChild(el("div","qmeta","Latency (this path)"));
    const tot=(sc.node_timings||[]).reduce((a,t)=>a+t.ms,0)||1;
    const gen=(sc.node_timings||[]).filter(t=>t.node==="generate_structured_plan").reduce((a,t)=>a+t.ms,0);
    const ret=(sc.node_timings||[]).filter(t=>t.node==="retrieve").reduce((a,t)=>a+t.ms,0);
    const bar=el("div","latbar");
    const seg=(cls,ms)=>{ const x=el("span",cls); x.style.width=(100*ms/tot)+"%"; return x; };
    bar.appendChild(seg("r",ret)); bar.appendChild(seg("g",gen)); bar.appendChild(seg("j",tot-ret-gen));
    lat.appendChild(bar);
    lat.appendChild(el("div","qmeta", ret? ("retrieval "+Math.round(100*ret/tot)+"% · gen "+Math.round(100*gen/tot)+"%") : (Math.round(tot)+" ms — no retrieval")));
    s.appendChild(lat);
    // answer + citations (per scenario)
    const ans=el("div"); ans.appendChild(el("div","qmeta","Answer"));
    if(sc.answer){ ans.appendChild(el("div",null,(sc.answer.summary||"").slice(0,150)+"…"));
      ans.appendChild(el("div","src",(sc.answer.citations||[]).map(c=>c.split("__")[0]).join(", "))); }
    else ans.appendChild(el("div","qmeta","—"));
    s.appendChild(ans);
    // metrics (system-level, constant)
    const met=el("div","metrics"); met.appendChild(el("div","qmeta","System (eval)"));
    met.appendChild(el("div",null)).innerHTML =
      "recall@5 <b>"+m.recall.before+" → "+m.recall.after+"</b>";
    met.appendChild(el("div",null)).innerHTML =
      "behaviour <b>"+m.behaviour_measured.before+"% → "+m.behaviour_measured.after+"%</b> measured";
    met.appendChild(el("div",null)).innerHTML =
      "<b>"+m.behaviour_labels_fixed.before+"% → "+m.behaviour_labels_fixed.after+"%</b> labels fixed";
    const tg=el("a","toggle","⌄ retry detail");
    tg.onclick=()=>document.getElementById("retryPanel").classList.toggle("open");
    met.appendChild(tg);
    s.appendChild(met);
  }
  function renderFoot(){
    document.getElementById("foot").textContent =
      "sources: "+DATA.metrics.recall.source+" · generated "+(DATA.generated_at||"")+" · "+(DATA.commit||"");
  }
  function renderRetry(){
    const p=document.getElementById("retryPanel"); p.innerHTML="";
    const rt=DATA.scenarios.retry; if(!rt||!rt.retrievals) return;
    p.appendChild(el("h3",null,"Retry loop — 3 attempts (bounded, hard cap 2)"));
    rt.retrievals.forEach((r,i)=>{ const d=el("div");
      d.innerHTML="<b>attempt "+(i+1)+"</b>: "+(r.final_context||[]).map(c=>c.split("__")[0]).join(", ");
      p.appendChild(d); });
  }
  function renderAll(){ renderButtons(); renderRibbon(); renderHero(); renderStrip();
    renderFoot(); renderRetry(); }
  renderAll();
</script>
</body>
</html>
```

- [ ] **Step 4: Run the guard test**

Run: `.venv/Scripts/python.exe -m unittest tests.test_visualiser.TestTemplateGuards -v`
Expected: PASS (2 tests). If `test_..._no_hand_typed_metric_numbers` fails, a metric literal leaked into the template — move it into `traces.json` and read it via JS.

- [ ] **Step 5: Commit**

```bash
git add docs/visualiser/template.html tests/test_visualiser.py
git commit -m "Phase 12 Task 4: self-contained theme-aware page template (renders traces JSON)"
```

---

## Task 5: Generator CLI (`--generate` / `--reuse`) + embed-sync test

**Files:**
- Create: `src/tools/build_visualiser_traces.py`
- Modify: `tests/test_visualiser.py`

**Interfaces:**
- Consumes: `graph.run`, `graph._retrieve_reranked`, `graph.Reranker`, `retrieval.Retriever`, and everything in `visualiser_serialize`.
- Produces: `docs/visualiser/traces.json` and `docs/visualiser/index.html`. Functions: `build_traces() -> dict` (API/models), `write_outputs(traces: dict) -> None` (pure I/O + inject), `main(argv)`.

- [ ] **Step 1: Write the failing test (the offline `--reuse`/write path only — no API)**

```python
# add to tests/test_visualiser.py
import json as _json
from tools.visualiser_serialize import inject   # already imported above; safe

class TestWriteOutputs(unittest.TestCase):
    def test_reuse_injects_existing_traces_into_index(self):
        from tools.build_visualiser_traces import write_outputs
        traces = {"scenarios": {"medical": {"path": ["classify_intent","safe_referral"],
                  "final_node": "safe_referral", "terminated_after": 2, "node_timings": [],
                  "answer": None}}, "hero": {}, "metrics": {"recall": {"source": "x"}},
                  "generated_at": "2026-08-12", "commit": "deadbeef"}
        write_outputs(traces)                       # writes docs/visualiser/{traces.json,index.html}
        idx = (_ROOT/"docs"/"visualiser"/"index.html").read_text(encoding="utf-8")
        self.assertNotIn("/*__TRACES__*/", idx)     # placeholder consumed
        self.assertIn("deadbeef", idx)              # data embedded
        on_disk = _json.loads((_ROOT/"docs"/"visualiser"/"traces.json").read_text(encoding="utf-8"))
        self.assertEqual(on_disk["commit"], "deadbeef")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python.exe -m unittest tests.test_visualiser.TestWriteOutputs -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'tools.build_visualiser_traces'`

- [ ] **Step 3: Write the generator**

```python
# src/tools/build_visualiser_traces.py
"""Phase-12 offline generator. Runs the four canonical scenarios + the cross-lingual hero, extracts
the strip figures from the eval run files, and writes docs/visualiser/{traces.json,index.html}.

    py src/tools/build_visualiser_traces.py            # full: API (~$0.23) + ~10 min CPU rerank
    py src/tools/build_visualiser_traces.py --reuse    # re-inject existing traces.json into the page (no API)
"""
from __future__ import annotations
import argparse, json, subprocess, sys
from datetime import date
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / "src"))
sys.path.insert(0, str(_ROOT / "src" / "tools"))

from visualiser_serialize import (serialize_graph_trace, chunk_summary, assemble_hero,   # noqa: E402
                                  strip_metrics, inject)
_VIZ = _ROOT / "docs" / "visualiser"

# canonical scenarios (mirror the graph-decision verification plan)
SCENARIOS = {
    "medical":  ("Is cramping at 30 weeks normal?", None),
    "missing":  ("How much Mutterschaftsgeld will I get?", None),
    "full":     ("When does Mutterschutz start if I'm due 2027-03-15 and employed?",
                 {"employment_status": "employed", "due_date": "2027-03-15"}),
    "retry":    ("What are the specific Mutterschutz rules for civil servants (Beamtinnen) in Bavaria?",
                 {"employment_status": "civil-servant"}),
}
HERO_QUERY = "When do I have to tell my employer I'm pregnant?"
HERO_ANSWER_SOURCE = "fam_mutterschutz"
HERO_FALLBACKS = [   # golden cross-lingual cases, if the primary query doesn't reproduce rank-6
    ("When do I notify my employer about my pregnancy?", "fam_mutterschutz"),
    ("employer notification pregnancy deadline", "fam_mutterschutz"),
]


def _scenario_dict(state: dict) -> dict:
    tr = state["trace"]; g = serialize_graph_trace(tr)
    term = None
    if tr.final_node in ("safe_referral", "request_attributes"):
        term = len([n for n in tr.nodes])            # nodes visited before ending
    resp = state.get("response") or {}
    answer = None
    if resp.get("kind") == "plan":
        pl = resp["plan"]; answer = {"summary": pl.get("summary", ""),
                                     "citations": [c["chunk_id"] for c in pl.get("citations", [])]}
    return {"path": state["path"], "node_timings": g["node_timings"], "final_node": tr.final_node,
            "terminated_after": term, "retries": tr.retries,
            "retrievals": [{"query": r["query"], "final_context": r["final_context"]}
                           for r in g["retrievals"]],
            "answer": answer}


def _build_hero() -> dict:
    import graph
    from retrieval import Retriever
    R = graph.generate._get_retriever()
    for q, ans in [(HERO_QUERY, HERO_ANSWER_SOURCE)] + HERO_FALLBACKS:
        before, brt = R.search(q, k=20, filters=None, mode="hybrid", pool=20, trace=True)
        brt._chunks = {c.chunk_id: c for c in before}     # attach for pure assemble_hero
        after, _ = graph._retrieve_reranked(q, None)
        try:
            cap = ("Retrieved at rank {r}, cut by the top-4 window. The system reported no "
                   "information while it was holding the answer.")
            hero = assemble_hero(q, brt, after, ans, cap)
            hero["caption"] = cap.format(r=hero["before"]["answer_rank"])
            return hero
        except ValueError:
            continue
    raise SystemExit("no hero query reproduced the rank-6 discard; inspect traces manually")


def build_traces() -> dict:
    import graph
    scenarios = {}
    for key, (q, profile) in SCENARIOS.items():
        scenarios[key] = _scenario_dict(graph.run(q, profile=profile))
    hero = _build_hero()
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=_ROOT,
                            capture_output=True, text=True).stdout.strip()
    return {"scenarios": scenarios, "hero": hero, "metrics": strip_metrics(),
            "generated_at": str(date.today()), "commit": commit}


def write_outputs(traces: dict) -> None:
    _VIZ.mkdir(parents=True, exist_ok=True)
    (_VIZ / "traces.json").write_text(json.dumps(traces, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    tpl = (_VIZ / "template.html").read_text(encoding="utf-8")
    (_VIZ / "index.html").write_text(inject(tpl, traces), encoding="utf-8")


def main(argv=None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reuse", action="store_true", help="re-inject existing traces.json (no API)")
    args = ap.parse_args(argv)
    if args.reuse:
        traces = json.loads((_VIZ / "traces.json").read_text(encoding="utf-8"))
    else:
        traces = build_traces()
    write_outputs(traces)
    print("wrote", _VIZ / "traces.json", "and", _VIZ / "index.html")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python.exe -m unittest tests.test_visualiser.TestWriteOutputs -v`
Expected: PASS. (Uses `write_outputs` only — no API. This leaves a real `index.html`/`traces.json` on disk from the fixture; Task 6 overwrites them with the real run.)

- [ ] **Step 5: Commit**

```bash
git add src/tools/build_visualiser_traces.py tests/test_visualiser.py
git commit -m "Phase 12 Task 5: offline trace generator (--generate / --reuse) + embed-sync test"
```

---

## Task 6: End-to-end generation, verification, publish

**Files:**
- Modify (generated): `docs/visualiser/traces.json`, `docs/visualiser/index.html`

**Interfaces:** none (integration + verification task).

- [ ] **Step 1: Run the full suite (no API)**

Run: `.venv/Scripts/python.exe -m unittest tests.test_visualiser -v`
Expected: PASS (all classes). Fix any failure before generating.

- [ ] **Step 2: Generate for real (API + models, ~$0.23, ~10 min)**

First confirm the key is present WITHOUT printing it:
Run: `.venv/Scripts/python.exe -c "import os;p='.env';print('key set' if any(l.startswith('ANTHROPIC_API_KEY=') and l.split('=',1)[1].strip() for l in open(p,encoding='utf-8')) else 'MISSING')"`
Then: `.venv/Scripts/python.exe src/tools/build_visualiser_traces.py`
Expected: `wrote …/traces.json and …/index.html`. If it raises `no hero query reproduced the rank-6 discard`, inspect with `src/ask.py --trace` on the fallback queries and add a golden cross-lingual case (L24/L28/L29/L30) to `HERO_FALLBACKS`, then re-run. Record which query worked in the journal.

- [ ] **Step 3: Verify numbers match their sources (no hand-typed drift)**

Run: `.venv/Scripts/python.exe eval/rescore.py` and confirm phase8b answerable = 58% / recall 0.90 as-measured and 69% after correction.
Run: `.venv/Scripts/python.exe -c "import json;d=json.load(open('docs/visualiser/traces.json',encoding='utf-8'))['metrics'];print(d['recall'],d['behaviour_measured'],d['behaviour_labels_fixed'])"`
Expected: recall before/after 0.75/0.90; behaviour_measured 38→58; behaviour_labels_fixed 58→69. If any differ, the extractor and the strip are out of sync — stop and reconcile.

- [ ] **Step 4: Verify the page renders in one screen with no network**

Use the `claude-in-chrome` skill (or open `docs/visualiser/index.html` from `file://`): confirm at 1440×900 the default (Full) view shows ribbon + cross-lingual hero + strip with **no scroll**; the Medical/Missing buttons swap the hero to the safety statement and shorten the ribbon; the retry toggle reveals the 3-attempt list; devtools Network shows **zero requests**. Screenshot for the journal.

- [ ] **Step 5: Commit the generated artifacts**

```bash
git add docs/visualiser/traces.json docs/visualiser/index.html
git commit -m "Phase 12 Task 6: generated visualiser (real traces) — page renders the 90-second story"
```

- [ ] **Step 6: (Optional) publish as an Artifact**

Load `artifact-design`, then publish `docs/visualiser/index.html` via the Artifact tool (favicon e.g. 🔎, title "NurtureDE Pipeline"). It is self-contained, so it renders as-is. Hand the URL to the user; keep the file in-repo as the source of truth.

---

## Self-Review

**1. Spec coverage:**
- Single-screen, no-scroll, static, self-contained, theme-aware → Task 4 (CSS grid + theme tokens), Task 6 Step 4 (verified). ✓
- Ribbon + 4 scenario buttons re-lighting the path → Task 4 `renderRibbon/renderButtons`. ✓
- Cross-lingual hero (before/after, rank-6 discard, real trace) → Task 3 (assembly + invariant), Task 5 `_build_hero` (fallbacks), Task 6 Step 2. ✓
- Safety-behaviour swap for medical/missing → Task 4 `renderHero` (`terminated_after`), Task 5 `_scenario_dict`. ✓
- Strip: per-scenario latency + system recall 0.75→0.90 / behaviour 38→58→69 → Task 2 (`strip_metrics`), Task 4 `renderStrip`. ✓
- Retry small-multiples behind a toggle → Task 4 `renderRetry` + toggle. ✓
- Every number traces to a file; 0.85 dropped → Task 2 (extractors from eval JSON), Task 4 guard test, Global Constraints. ✓
- Generator persists baseline 0.75/38% (PM-1) → Task 2 `strip_metrics` writes them into traces.json. ✓
- Reuse graph/retrieval unchanged → Tasks 1/5 consume only; no modifications. ✓

**2. Placeholder scan:** No "TBD"/"handle appropriately". The `/*__TRACES__*/` string is an intentional injection marker, not a plan placeholder. Hero fallback path is concrete (defined list + documented manual step). ✓

**3. Type consistency:** `serialize_graph_trace` returns `node_timings`/`retrievals`/`final_node` — consumed by `_scenario_dict` (Task 5) and the JS (`renderStrip`/`renderRibbon`). `chunk_summary` fields (`source_id`,`language`,`rank`) — produced in Task 1, used by `assemble_hero` (Task 3) and `renderHero` (Task 4). `strip_metrics` keys (`recall`,`behaviour_measured`,`behaviour_labels_fixed`,`cross_lingual_recovery`) — Task 2, consumed by `renderStrip`/`renderFoot`. `inject`/`write_outputs`/`build_traces` signatures consistent across Tasks 3/5. ✓

---

## Notes for the executor

- The hero uses `source_id` (not full `chunk_id`) to locate the answer, because the chunk suffix varies between the pool-20 and pool-100 runs; the *document* is the invariant.
- `terminated_after` counts nodes visited before an early END (medical=2, missing=3); the JS keys the safety swap off its truthiness.
- If the one-screen budget is tight, the strip drops the **answer snippet** first (spec), never the numbers — do this by hiding the middle strip column at `max-height` breakpoints, not by removing metrics.
- Follow-ups already tracked and **out of scope here**: `rescore.py → eval/results.md`, and the journal-figure provenance audit.
