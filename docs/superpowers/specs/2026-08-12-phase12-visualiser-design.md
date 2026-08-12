# Phase 12 — the pipeline visualiser (design)

**Date:** 2026-08-12 · **Status:** design, pending review · **Prev phase:** 11 (LangGraph workflow + trace)

## One job

Make three weeks of invisible work visible in **ninety seconds**, to a stranger, from a **static
page** — no clone, no server, no 165-second wait. This is a **portfolio piece for reviewers**, not
a debug tool: `src/ask.py --trace` already *is* the debug tool (it found two real bugs), so this
does not duplicate it. It optimises for narrative legibility, not information density.

## Decisions made in this spec (react to these first)

1. **Delivery: a self-contained HTML file committed to the repo, also publishable as an Artifact.**
   Static, theme-aware, one file. In-repo satisfies the "in the repo, not behind someone else's UI"
   ethos (the LangSmith call); the Artifact gives a shareable URL a stranger opens in 5 seconds.
2. **Data: pre-recorded trace JSON, embedded in the page.** An Artifact's CSP blocks external
   fetch, and the goal is "opens instantly with no backend," so the traces are generated **offline**
   and inlined. No live graph call, ever, on the page.
3. **Recall on the page is `0.75 → 0.90`, not `0.85 → 0.90`.** The delta is the story (found a
   ranking failure, diagnosed it as a top-4 discard not a retrieval miss, raised the pool, moved the
   number); a lone `0.90` can't show improvement. `0.85` is a figure I carried since the first Phase-8
   report and never sourced — the on-disk baseline is `0.75`, so the unsourced number was
   *understating* the improvement. See *Numbers* below.

## The screen (approved layout)

Single 1440×900 screen. No scroll, no click required for the core story. Three horizontal bands.

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│  NurtureDE — how the system decides           [ Medical ] [ Missing ] [ Full ● ] [ Retry ] │  BAND 1
│   ● classify → ● profile → ● retrieve ↻ → ● grade → ● timeline → ● generate → ● verify     │  ribbon
│     medical ⤵ safe_referral ⊗        missing ⤵ request_attributes ⊗                        │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│   "When do I have to tell my employer I'm pregnant?"        English question → German answer│  BAND 2
│    BEFORE — pool 20, top-4                      AFTER — pool 100 + cross-encoder rerank      │  (hero)
│    0 EN tk_maternity_pay                         0 DE fam_mutterschutz ◀ ANSWER              │
│    1 EN tk_maternity_pay                         1 EN tk_maternity_pay                       │
│    2 EN tk_maternity_benefits                    2 DE fam_mutterschutz                       │
│    3 EN tk_maternity_pay                         3 EN tk_maternity_benefits                  │
│    ───── top-4 cutoff ─────                                                                  │
│    6 DE fam_mutterschutz ◀ discarded, the actual answer                                      │
│    "Retrieved at rank 6, cut by the top-4 window. The system reported no information         │
│     while it was holding the answer."                                                        │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│  LATENCY retrieval ████████████████▏86%  gen ██▏8%  judges ▏   ANSWER ▸ …cited fam_mutter…  │  BAND 3
│  recall@5 0.75 → 0.90    behaviour 38%→58% (measured), 58%→69% (labels fixed)  [⌄ retry]    │  (strip)
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

**Band 1 — ribbon + scenario switcher.** Four buttons re-light the ribbon to that scenario's path.
Default: **Full answer**. The two early-exit paths are the point, not a footnote:
- *Medical* → `classify_intent → safe_referral ⊗` — terminates after **2 nodes, no retrieval ran**.
- *Missing* → `classify_intent → check_profile → request_attributes ⊗` — asks instead of guessing.

  When a terminating scenario is selected, **Band 2 swaps** from the retrieval hero to a single
  legible statement of the safety behaviour: *"Terminated after 2 nodes. No retrieval, no model
  answer — it refused to assess a medical question and referred to a doctor / 112."* That safety
  behaviour is worth as much visual weight as the retrieval story.

**Band 2 — the hero (cross-lingual before/after).** The headline is the rank-6 discard, not the
retry loop. Two columns from a **real trace**: BEFORE = pool 20, top-4 (the answer sits below the
cut); AFTER = pool 100 + cross-encoder rerank (the answer is promoted to rank 0). Language chips
(EN/DE) carry the cross-lingual point without words. One caption line. This is a bug, a diagnosis,
and a fix in one image, and it needs no interaction to read.

**Band 3 — thin strip, three items.** (1) A **per-scenario** latency bar that updates with the
selected scenario — full answer = retrieval ~86% / gen ~8% / judges; *medical* = ~1.75 s, all
judge, **no retrieval bar at all** (which is itself the point: refusing is nearly free). (2) The
final answer + its citations for that scenario. (3) The two **system-level** headline metrics as
before→after deltas (recall@5 `0.75 → 0.90`; behaviour `38% → 58%` measured, then `58% → 69%` after
five golden-label corrections) — eval-wide, so they stay **constant across scenario buttons**,
unlike (1) and (2). The delta carries the story; a single number can't. If the strip is too tight
for all three items, **drop the answer snippet, never the numbers**.

**Behind `⌄ retry detail` (not default).** The retry small-multiples (3 attempts, ~1/4 of slots
churn per round, grade stays insufficient, hits the cap). Honest but not a headline — it explored,
couldn't invent absent information, degraded correctly. It gets a toggle, not the stage.

## Architecture — two units, one direction of flow

The page never computes; a generator computes and persists; the page renders what was persisted.
This also satisfies the escalated **PM-1** rule (the generator writes figures to a versioned file).

### Unit A — `src/tools/build_visualiser_traces.py` (offline generator)

- **Does:** runs the four canonical scenarios through `graph.run(...)` and serialises each
  `GraphState["trace"]` (`GraphTrace` + embedded `RetrievalTrace`s) to plain dicts; separately
  builds the **hero before/after** by calling the retriever twice directly (not via the graph):
  `Retriever.search(q, k=4, pool=20, mode="hybrid", trace=True)` for BEFORE and the pool-100 +
  rerank path (`graph._retrieve_reranked`) for AFTER. Writes everything to
  **`docs/visualiser/traces.json`** (versioned; the page's only data source).
- **Depends on:** `graph`, `retrieval` (both unchanged — Phase-11 promised "no retrofit"). Needs a
  serialiser for the two dataclasses (dataclasses → dict; `RetrievedChunk` → `{chunk_id, language,
  source_id, score}` — only what the page renders, not chunk text).
- **Cost:** the four scenarios cost API (~$0.23 total, measured in Phase 11) and ~10 min of CPU
  rerank. Run rarely, on demand; output is committed, so the page is free forever after.
- **Hero-query verification (build-time):** confirm `"When do I have to tell my employer I'm
  pregnant?"` actually reproduces the rank-6-below-cut → rank-0-after story. If it doesn't
  reproduce cleanly, use whichever golden cross-lingual case (`L24 / L28 / L29 / L30`) does, and
  record which in the traces JSON and the journal. **A real trace matters; the specific query does
  not.**

### Unit B — `docs/visualiser/index.html` (the page)

- **Does:** self-contained HTML + inline CSS + inline JS. On load, reads the embedded
  `traces.json`, renders Band 1/2/3, wires the four scenario buttons and the retry toggle. No
  network, no framework, no build step. Theme-aware (light/dark per the Artifact contract).
- **Depends on:** only the inlined `traces.json`. Nothing else.
- **Self-citation (fits a provenance project):** a footer names the source files behind each number
  (`eval/phase8b_findings.md`, `eval/last_run_phase8b.json`, `BUILD_JOURNAL.md` pool-probe) and the
  commit SHA — the page cites itself the way the assistant cites its sources.

`traces.json` is the interface between the two units: the page can be styled without re-running the
generator, and the generator can change without touching the page, as long as the shape holds.

## Numbers on the page — every figure traceable to a file, or dropped

**Rule (from the escalated PM-1):** every number the page shows must resolve to a file a script
wrote. If a figure can't, it is **dropped, not rounded or remembered**. The whole strip is on one
basis: **`hybrid_rerank`, answerable subset, n=26 — the same 26 case ids in both runs** (verified),
so before/after is genuinely apples-to-apples.

| slot | value | source (file; reproducible) |
|---|---|---|
| recall@5 (before → after) | **0.75 → 0.90** | before: `eval/last_run.json` (hybrid_rerank, answerable) · after: `eval/last_run_phase8b.json` / `eval/phase8b_findings.md`; `py eval/rescore.py` |
| cross-lingual recovery | **5 of 6 into top-4** | `BUILD_JOURNAL.md` pool-probe (P8 retraction) |
| behaviour (as measured) | **38% → 58%** | before: `eval/last_run.json` · after: `eval/last_run_phase8b.json` (both answerable n=26) |
| behaviour (labels fixed) | **58% → 69%** | `eval/phase8b_findings.md` l.89; `py eval/rescore.py` |
| latency split | retrieval ~86% / gen ~8% | Phase-11 per-node `GraphTrace.node_timings` (BUILD_JOURNAL addendum) |
| hero ranks / langs | from the trace | `docs/visualiser/traces.json` (generated) |

**Provenance gap to close in the build:** the baseline `0.75 / 38%` figures are correct but are
**not currently written by any script** — they were computed ad-hoc by filtering `last_run.json` to
`hybrid_rerank` + answerable. Per the rule above, that makes them terminal-only. So the generator
(Unit A) **must emit the baseline hybrid_rerank/answerable figures to `docs/visualiser/traces.json`
(and ideally `eval/results.md`)** so the page cites a file, not a remembered computation. This is
the same PM-1 discipline that produced the whole spec.

- **`0.85` is not used** (on-disk baseline is `0.75`; `0.85` survived only in journal prose, against
  a since-corrected ruler — it *understated* the improvement).
- The all-43 `65% → 77%` headline is **not** on the strip: the baseline never ran all 43, so the
  "as measured" before-number for that basis doesn't exist on disk — dropped rather than spliced.

## Testing / proof

- **Renders with no network:** open `index.html` from `file://` with devtools offline — full page,
  no failed requests.
- **Numbers match their source:** a check that every figure the page displays equals the value in
  `traces.json` / `rescore.py` output (no hand-typed numbers in the HTML).
- **Each scenario button lights the recorded path** (medical = 2 nodes, missing = 3, full = through
  verify, retry = the loop) — asserted against `traces.json` paths.
- **Hero reproduces the discard:** the generator asserts BEFORE has the answer chunk below rank 3
  and AFTER has it at rank 0; if not, it fails loudly and we pick another golden case.

## Scope guardrails (YAGNI)

- No live server, no backend, no framework. One HTML file + one JSON file.
- No interaction required for the core story; the only controls are 4 scenario buttons + 1 retry
  toggle.
- No per-chunk drill-down, no editable query, no funnel animation — those are debug-tool features
  and belong to `ask.py --trace`, not here.
- Retry small-multiples stay behind the toggle.

## Out of scope / follow-ups (tracked separately)

- `rescore.py` → `eval/results.md` persistence + a `BUILD_JOURNAL.md` figure audit (the escalated
  PM-1 work; tasks already filed).
