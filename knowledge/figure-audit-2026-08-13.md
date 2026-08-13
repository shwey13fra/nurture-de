# Figure audit — every number quoted this session, checked against disk (2026-08-13)

Prompted by the `0.85` incident (a recall figure carried for phases that the on-disk baseline
contradicts). Scope: **every quantitative claim made in the Phase 11→12 working session**, checked
against files on disk — not memory. Status is one of **SOURCED** (a committed file backs it,
ideally reproducibly), **PROSE-ONLY** (exists only in `BUILD_JOURNAL.md`/journal narrative; the raw
data was throwaway/scratchpad and never committed), or **CONTRADICTED** (a committed file says
something different). Read before quoting any figure in a README or public post.

## A. Eval quality — SOURCED and reproducible (safe to quote)

| figure | value | on-disk source |
|---|---|---|
| recall@5 baseline (hybrid_rerank, answerable, n=26) | **0.75** | `eval/last_run.json` (filter config=hybrid_rerank, answerable) |
| recall@5 after (pool-100 + rerank) | **0.90** | `eval/last_run_phase8b.json` / `eval/phase8b_findings.md` l.19,90; `py eval/rescore.py` |
| behaviour-match answerable, as measured | **38% → 58%** | baseline `eval/last_run.json`; after `eval/last_run_phase8b.json` (both n=26) |
| behaviour-match answerable, labels corrected | **58% → 69%** | `eval/phase8b_findings.md` l.89; `py eval/rescore.py` |
| behaviour-match all-43 | **65% → 77%** | `eval/phase8b_findings.md` l.17,88; `py eval/rescore.py` |
| citation validity | **219/220 ≈ 100%** (1 unsupported, L20) | `eval/phase8b_findings.md` l.20 |
| eval cost (phase-8b run) | **$2.41** | `eval/phase8b_findings.md` l.5 |
| corpus size | **225 chunks** | `data/chunks.jsonl` (`wc -l` = 225) |
| user_type vocab | any 133, employee 76, self-employed 5, student 7, unemployed 3, civil-servant 1 | `data/chunks.jsonl` (facet count) |
| insurance_type vocab | any 214, statutory 5, non-statutory 4, none 1, private 1 | `data/chunks.jsonl` (facet count) |
| hero ranks (cross-lingual before/after) | **rank 6 → rank 0** | `docs/visualiser/traces.json` `hero.before/after.answer_rank` |
| retry loop | **2 retries, 3 attempts** (hard cap 2) | `docs/visualiser/traces.json` `scenarios.retry`; `MAX_RETRIES` in `src/graph.py` |
| RERANK_POOL / K_CONTEXT / MAX_RETRIES | **100 / 4 / 2** | `src/retrieval.py`, `src/graph.py` (code constants) |

## B. Latency & cost — PROSE-ONLY (do NOT quote the absolute numbers as-is)

The Phase-11 latency/cost story came from `measure_phase11.py`, whose output
(`phase11_measurements.json`) was **scratchpad/throwaway and never committed**
(`git ls-files` confirms: no measurement harness or its JSON is tracked). So these numbers exist
only as `BUILD_JOURNAL.md` prose:

| figure (as quoted in the Phase-11 journal) | status | note |
|---|---|---|
| full-path latency **191 s**, retrieve **165 s (86%)**, gen **19 s (10%)** | PROSE-ONLY | no committed data file |
| 2-retry latency **356 s**, retrieve **316 s (88%)**, gen **17 s (5%)** | PROSE-ONLY | no committed data file |
| medical **1.75 s**, missing **3.19 s** | PROSE-ONLY | no committed data file |
| per-scenario cost **$0.0026 / $0.0079 / $0.081 / $0.134**, total **~$0.23** | PROSE-ONLY | no committed data file |
| `verify_citations` flagged **1 of 2** cases that reached it | PROSE-ONLY | not stored in traces.json |
| "**5 of 6** cross-lingual cases recovered into top-4" | PROSE-ONLY | `scratchpad/pool_probe.py` was never committed; the hero in `traces.json` demonstrates ONE such recovery, file-backed |
| Phase-13 rerank table (pool 20/50/100 = **29.4/70.2/117.8 s**, "median of 7 trials") | PROSE-ONLY | pre-existing journal note; trial data not committed |

**A committed, reproducible ALTERNATIVE exists for the latency *split*** (not the absolute seconds):
`docs/visualiser/traces.json` `scenarios.full/retry.node_timings` gives, for its own generation run,
full total **243 s**, retrieve **216 s (89%)**, gen **20.9 s (9%)**; retry total **287 s**, retrieve
**251 s (88%)**, gen **16.8 s (6%)**. Note these differ from the journal's 191/165/356 s — **CPU
wall-clock varies run-to-run**, so no single absolute is canonical.

**Recommendation for public posts:** quote the **percentage split** (retrieval ~86–89% of latency,
generation ~5–10%) — it is robust across both runs and file-backed in `traces.json`. Do **not**
quote a specific second count (191 s, 165 s) as a fact; if you want an absolute, cite the committed
`traces.json` numbers and call them "one run on a CPU dev box." The cost figures and "verify flagged
1 of 2" have **no committed source** — either re-run and commit the harness, or caveat them as
one-off measurements.

## C. CONTRADICTED — do NOT quote

| figure | quoted as | on-disk truth | source |
|---|---|---|---|
| recall@5 baseline | **0.85** | **0.75** (hybrid_rerank, answerable) | `eval/last_run.json`; the 0.85 survives only in `BUILD_JOURNAL.md` l.403 prose, against a since-corrected ruler. It *understated* the improvement (0.75→0.90 is a bigger delta). Logged: `knowledge/past-mistakes.md` PM-1 sixth instance. |
| behaviour-match baseline | **35%** | **37–38%** (37% of all 27; 38% of answerable 26) | `eval/last_run.json` (hybrid_rerank) |

## Bottom line

The **eval-quality** claims (recall, behaviour, citation validity, corpus/vocab stats, hero ranks,
retry structure) are all file-backed and safe. The **latency/cost** claims — the most rhetorically
striking Phase-11 findings — are **prose-only from an uncommitted harness**; quote the percentage
split (file-backed) and treat absolute seconds/dollars as illustrative, not sourced. Two figures
(**0.85**, **35%**) are contradicted by disk and must not be repeated.
