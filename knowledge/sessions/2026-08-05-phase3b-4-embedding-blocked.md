# Session Journal — 2026-08-05 (evening): Phase 3b DONE, Phase 4 BLOCKED on commit-OOM

## ⏭️ RESUME TOMORROW — read this first

**One decision is open, and it is NOT about the model or the code.** Both choices
just free Windows *commit charge* (which is maxed at 98.7%). Pick one:

- **A. Reboot (recommended).** Clears ~44 GB of leaked/unattributable committed
  memory at the root; leaves the machine healthy for the rest of the project
  (LangGraph / MCP / embedding all need headroom). This CLI session ends on reboot;
  reopen Claude Code here and I reload from this folder (that's the BOOT design).
- **B. Close Chrome (41 procs, 7.57 GB private commit).** Frees ~7.5 GB commit →
  ~8 GB headroom, enough to build **without** rebooting. Machine stays fragile
  (44 GB still leaked) but the build will fit. Keeps this session alive.

**Then, whichever you picked, run (in the project venv):**
```
# 0) sanity: confirm we actually have commit headroom now (want > ~3 GB)
powershell "((Get-Counter '\Memory\Commit Limit').CounterSamples.CookedValue - (Get-Counter '\Memory\Committed Bytes').CounterSamples.CookedValue)/1GB"

# 1) build dense (Chroma) + sparse (BM25) indexes — e5-large, fp16, batch 8
.venv/Scripts/python.exe src/index.py

# 2) run the validation gate (cross-lingual / prefix / smoke)
.venv/Scripts/python.exe tests/validate_phase4.py
```
If both pass → update `BUILD_JOURNAL.md` (model choice + reasoning, E5 prefix gotcha,
cross-lingual numbers, E5-vs-cl100k token comparison) and **commit Phase 4**.

---

## ✅ Done and COMMITTED today
- **Phase 3** (`788181a`) — deterministic metadata annotation; `data/chunks.jsonl`
  now tracked (ignore-policy reversal logged in `decisions.md`). 201 chunks, 0 nulls.
- **Phase 3b** (`7260b74`) — migrated to a dedicated **Python 3.11.9** venv, **CPU-only**
  torch (`2.13.0+cpu`), `requirements.txt` pinned (embeds the PyTorch CPU index),
  README Python-floor note. Guard passed: sentence-transformers 5.6.1, chromadb 1.5.9,
  rank-bm25 0.2.2. (The venv had been built in an un-journaled prior session; the
  durable artifacts — requirements.txt, README, journal — were the real 3b deliverable.)

## 📝 WRITTEN but NOT committed (on disk — survives reboot; unvalidated by design)
Phase 4 commit is intentionally deferred until the validation gate passes.
- `src/retrieval.py` — the single `search(query, k, filters) -> list[RetrievedChunk]`
  interface. Swappable **Embedder** (E5) + **VectorStore** (Chroma) + **SparseIndex**
  (BM25) behind it, for the prod swap (hosted endpoint + Supabase pgvector). RRF hybrid
  fusion. Optional `RetrievalTrace` (off by default) with dense/sparse/RRF/filter-
  exclusion/timings for the Phase-12 visualiser. `E5Embedder` loads **fp16** directly
  (`model_kwargs torch_dtype=float16`, ~1.1 GB, no fp32 peak), **batch 8**, casts
  vectors to fp32 for storage. German BM25 tokenizer: casefold (ß→ss), umlauts kept,
  compounds NOT split (documented — dense index covers sub-compounds).
- `src/index.py` — builds both indexes (Chroma cosine, upsert-idempotent on chunk_id;
  BM25 over `text` NOT embed_text), prints dim + vector count, and the E5-vs-cl100k
  token report that **flags any chunk > 512 E5 tokens (truncation)**.
- `tests/validate_phase4.py` — the 3-test gate (see below).
- `.gitignore` — added `data/bm25.pkl` (derived, rebuildable).

## 🔴 The blocker (diagnosed thoroughly, NOT guessed — do not re-litigate)
`src/index.py` OOM'd **twice**: `memory allocation of 67 MB failed` during the model
*download* (Rust `hf-xet` buffer), before the model even loaded.

| metric | value |
|---|---|
| commit limit | 63.7 GB (RAM 15.7 + pagefile 48) |
| **committed** | **62.9 GB = 98.7%** → only **0.82 GB headroom** |
| physical RAM free | 1.3 GB (NOT the constraint) |
| kernel pool (paged+nonpaged) | 2.3 GB (normal — no pool leak) |
| sum of ALL process private bytes | 18.9 GB |
| **unattributed commit** | **44.0 GB** (no process, no pool) |
| C: free | 163 GB (disk NOT full) |

**Why model downgrade is useless here:** the 67 MB *download* buffer failed — e5-base
or e5-small would fail identically. The wall is commit exhaustion, not model size.
This is why we did NOT downgrade: a weak Test-1 result would be misread as a design
failure (768-dim too weak) when the real cause is a full commit charge. Diagnose the
resource wall before touching the design. (→ PM-4.)

## Fallback ladder (only after commit is freed)
1. Retry **e5-large fp16 / batch 8** (already coded). With real headroom it should fit
   in < 2 GB peak.
2. Only if e5-large *still* OOMs **with** headroom → drop to **multilingual-e5-base**,
   and **record in the journal that the choice was memory-forced, not quality-driven**,
   so Test 1's cosine numbers are interpreted against the right baseline.

## Validation gate — Phase 4 is NOT "done" until all three pass
- **Test 1 — cross-lingual alignment** (HARD): cosine between parallel
  `gesund_vorsorge_de` (4) ↔ `gesund_vorsorge_en` (9). Expect **> 0.85**; **~0.5 = STOP**
  (multilingual space failed → the whole EN/DE test design collapses). NOTE: the TK↔fam
  pairs are *register* pairs (rule vs process), NOT translations — not valid for Test 1.
- **Test 2 — prefix verification:** same passage with vs without `passage: ` must
  differ measurably (proves prefixing is applied, not assumed).
- **Test 3 — smoke retrieval:** dense-only top-5 for 5 queries (2 DE, 2 EN, 1 Hebamme),
  scores + heading paths. Visual sanity, not a metric.

## Carried forward (unchanged from Day-3)
- Golden-set: weight filtering evals on `user_type` (84 real values), not
  `insurance_type` (94% `any`).
- `parental-leave` / `child-benefits` single-chunk stubs = corpus-coverage gap, not a
  taxonomy fix.
