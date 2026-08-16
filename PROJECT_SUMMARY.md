# NurtureDE — Project Summary

A cited, official-source Q&A assistant for pregnancy, *Mutterschutz*, and family benefits in
Germany. It reports what official German sources say and **cites every claim**, answers English
questions from German sources (cross-lingual), refuses medical questions, and computes dates in
Python — never deciding eligibility. Built as a portfolio project across **14 phases**.

- **Live demo:** https://huggingface.co/spaces/Shwey13/nurture-de
- **Pipeline visualiser (90-second overview):** https://claude.ai/code/artifact/368eeb82-901d-411e-9725-b7a8f840f0d4
- **Full narrative:** `README.md` · **build log & problem register:** `BUILD_JOURNAL.md` · **lessons:** `knowledge/past-mistakes.md`

---

## The phases

| # | Phase | What shipped |
|---|---|---|
| 1 | Corpus & provenance | 22 official sources, robots-checked fetch, SHA-256 fingerprints, honest exclusions (e.g. frankfurt.de WAF-blocked → not spoofed) |
| 1b | Clean extraction | Structure-preserving Markdown from cached HTML |
| 2 | Chunking | **Question-anchored** chunking (the FAQ corpus encodes hierarchy by convention, not markup) → 225 chunks |
| 3 | Metadata | `topic / user_type / insurance_type / …` taxonomy per chunk |
| 4 | Indexing | Dense (multilingual-E5, Chroma) + sparse (BM25) indexes; **silent E5 truncation caught & fixed** |
| 5 | Retrieval | One `search()` interface: hybrid dense+sparse, RRF fusion, metadata pre-filter, full trace |
| 6 | Generation | Grounded, cited answers behind the answer prompt |
| 7 | Eval harness | Golden set (56 cases), 3 configs, LLM judge; golden-set integrity fixes |
| 8 | First clean eval | Measured, nothing tuned; **starved-reranker retraction**; `RERANK_POOL=100` |
| 9 | Timeline tool | Deterministic Mutterschutz dates in **Python** (not the model) |
| 10 | MCP server | 3 tools / 1 resource / 1 prompt over stdio |
| 11 | Orchestration | **LangGraph workflow** (not an agent): routing + bounded retry + verify, instrumented per node |
| 12 | Visualiser | Self-contained static page rendering the trace — the 90-second story |
| 13 | Deployment | **Live** on HuggingFace Spaces (thin slice; reranker offloaded to Jina) |
| 14 | Packaging | README as portfolio narrative; repo hygiene; figure audit |

---

## Key features

- **Cited answers only** — every claim traces to a source chunk with authority + verification date; `verify_citations` checks faithfulness.
- **Cross-lingual** — an English question retrieves the German source that holds the answer (the core feature).
- **Safety by design** — refuses medical questions (→ doctor/midwife/112); asks for missing attributes instead of guessing; never states eligibility or amounts as entitlements.
- **Deterministic dates** — Mutterschutz timeline computed in Python, not hallucinated.
- **Workflow, not agent** — fixed code paths, two routing branches, one bounded (≤2) retry loop; every stage traced.
- **Stores nothing** — no logging/analytics/persistence (GDPR Art. 9 inputs).

---

## Results (all figures traceable to a file — see `knowledge/figure-audit-2026-08-13.md`)

| metric | before → after | source |
|---|---|---|
| recall@5 (answerable, n=26) | **0.75 → 0.90** | `eval/last_run.json` → `eval/last_run_phase8b.json`, `eval/results.md` |
| behaviour match (measured) | **38% → 58%** | prompt fix + rerank pool 100 |
| behaviour match (ruler corrected) | **58% → 69%** | after 5 golden-label corrections |
| citation validity | **219/220 ≈ 100%** | `eval/phase8b_findings.md` |
| latency split (production) | retrieval ~86–89%, generation ~5–10% | `docs/visualiser/traces.json` |

Latency is reported as a **share**, never absolute seconds (CPU wall-clock varies run to run).

---

## Notable findings & corrections (the interesting engineering)

**Failures that produced *plausible output*, caught by reading intermediate artifacts (PM-9):**
- **Rank-6 discard** — the correct German chunk was retrieved but cut by the top-4 window; the system said "no info" while holding the answer. Fix: `RERANK_POOL=100` (recovered 5 of 6 cross-lingual cases).
- **Starved-reranker retraction** — "reranking barely helps" was a measurement bug (10-candidate pool starved the reranker); the component was fine.
- **Filter-vocabulary mismatch** — `employment_status="employed"` mapped to a `user_type` value the corpus tags `"employee"`, silently emptying the pool. Fix: `assert_filter_vocab()` **fails the build** if any filter value matches zero chunks — and it immediately caught a *second* latent case (`family-insured`).
- **A test that overwrote the deployed artifact** with fixture data — no error; caught by a `git status` diff. Fix: tests write to a temp dir.

**Provenance discipline (PM-10): "a measurement not written to a file is a memory of one, and memories drift toward the number you wanted."**
- A recall figure (`0.85`) carried across several phases was contradicted by disk (`0.75`) — and it *understated* the real improvement (0.75→0.90 is a bigger jump). Caught by refusing to publish an unsourced number.
- Fixes made structural: `eval/rescore.py` now writes `eval/results.md` every run; a no-hand-typed-numbers **test** guards the visualiser; a full figure audit checks every quoted number against disk.

**Silent E5 truncation (P7)** — 21 chunks exceeded E5's 512-token limit and were truncated before the model saw them (the chunker sized in a proxy tokenizer that undercounts German). Fixed by sizing against the real tokenizer; zero truncated.

**Question-anchored chunking (P1/P7)** — the corpus's FAQ convention forced chunking on questions, and later biased eval questions toward being too easy: one corpus trait, two consequences.

---

## Deployment (Phase 13) — what was built and every fix along the way

**Decision:** deploy a **thin slice** — a public URL a user can type into — on **HuggingFace Spaces (free CPU)** over Vercel+Supabase (Vercel serverless can't hold the 2.2 GB E5 model; pgvector is unnecessary for 225 vectors on one instance). It was first *deliberately skipped* on value, then reversed: a live URL is worth building even though the visualiser explains the system better.

**The one production swap:** the reranker → **Jina** (`jina-reranker-v2-base-multilingual`), because CPU reranking was 86–89% of query latency. Chosen over Cohere as the multilingual cross-encoder closest to the local `bge` model; **pre-ship gate verified** it recovers all 4 EN→DE cases to rank 0. Everything else runs in-container; `graph.py` is unchanged (the reranker is injected at startup).

**Fixes made during the deploy:**
- **HF requires binaries in LFS** → shipped the index as **text** (`data/embeddings.jsonl`) and rebuild Chroma+BM25 in-container at startup (seconds, no 45-min embed; also fixes Windows→Linux portability).
- **Dependency conflict** → unpinned pydantic (gradio 6.24.0's mcp extra caps it ≤2.12.5).
- **First-boot startup** → model warmup moved to a background thread so the web port binds immediately.
- **Latency felt slow** → generation switched **Opus → Sonnet** (~2–3× faster; the generate step dominates once reranking is hosted — confirming the Phase-11 prediction). Swappable via `GEN_MODEL`.
- **UX** → progress "⏳ Working…" message + the Ask button disables during a request; sources moved into a **collapsible panel**; Soft theme + constrained width.

**Cost:** ~$0.05–0.06/query (mostly generation), **$0 idle** on the free tier; Jina rerank free within its tier. Secrets live in Space settings, never in the repo.

---

## Honest limitations

- Prototype scale — 22 sources, 225 chunks, **56 eval cases (not 500)**.
- **Cross-lingual gap:** recall@5 is **0.94 on German** but **~0.30 on English** questions about German-only topics — the real defect, stated openly.
- Freshness disclosure is implemented but **untestable** (whole corpus fetched on one day — no date spread).
- The live demo's behaviour figures were measured on **Opus**; the demo now runs **Sonnet** (retrieval recall is model-independent, so recall stands; answer-quality on Sonnet is un-re-evaluated by choice).

---

## Roadmap

Parent-document retrieval · a referral layer for questions no document can answer · at scale: Supabase pgvector + a hosted embedder (costed in `knowledge/phase13-deployment-plan.md`, deferred on purpose).
