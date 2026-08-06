# BUILD_JOURNAL — NurtureDE

The build narrative and its **problem register**. Problems are first-class content
here: what broke, how it surfaced, and why we responded the way we did. The terse
engineering record lives in `knowledge/sessions/`; the decision log in
`knowledge/decisions.md`; the plain-language tour in `PHASES.md`. This file is the
place to understand *why the corpus looks the way it does*.

## Phase status

| Phase | What | Status |
|-------|------|--------|
| 1  | Corpus acquisition & provenance (`sources.yaml`, `fetch.py`, robots) | done |
| 1b | Clean re-extraction (`extract.py`, per-domain selectors → Markdown)  | done |
| 1c | Statute reclassified `superseded` (TOC, not law text)                | done |
| 2  | Heading-aware chunking (`chunk.py` → `data/chunks.jsonl`)             | done |
| 3  | Metadata annotation (`annotate.py`: topic/subtopic/user_type/insurance) | **done** |
| 3b | Environment migration (3.11 venv, CPU torch, requirements.txt)        | **done** |
| 4  | Embedding & vector index (E5 + Chroma + BM25)                         | **done** — validated (3-test gate green; E5 512-cap enforced → P7) |
| 5  | Retrieval (`search()`: dense+sparse+RRF, metadata pre-filter, trace)  | **done** — 6-query validation + filtering proof (→ P8) |

---

## Phase 2 — Heading-aware chunking

**Output:** 22 active docs → **198 chunks** → `data/chunks.jsonl` (git-ignored,
derived). Each chunk carries denormalized provenance (`source_id`, `url`,
`authority`, `authority_tier`, `language`, `last_verified_date`), retrieval fields
(`heading_path`, `section_slug`, `content_kind`, `merge_policy`, `question_ratio`,
`token_count`, `parent_section_id`), the nullable metadata fields (filled Phase 3+),
and both `text` (displayed/cited) and `embed_text` (`[Authority › H1 › H2] + body`,
embedded).

### Key decision — one splitter, two merge policies (not two splitters)

The spec proposed a Q&A splitter and a prose splitter chosen per document. The
corpus argued otherwise: the cut boundary is the **heading** either way; what
differs is **merge permission**. So we run one heading-aware splitter and select a
policy per *section*: a question-anchored section never merges (distinct intents);
adjacent prose sections merge toward the token floor. This is the only shape that
handles the hybrids (e.g. `fam_mutterschutz`: mostly questions, some statement
headings). Rationale in full: `knowledge/decisions.md`.

### Token measurement (Step 0, before chunking)

- **Tokenizer:** cl100k (pure-Python reimpl with exact tiktoken parity — tiktoken
  ships **no Python 3.7 wheel**, and 3.7.8 is the only interpreter here). Recorded
  as `tokenizer` per chunk. A multilingual sentence-transformer will count German
  differently (order ~15–20%); **250 / 500 / 800 are heuristics, not thresholds
  anything breaks at**, so a shift that size does not invalidate the chunking.
- **German is ~19% denser:** `fam_mutterschutz` (de) 3.66 chars/tok vs
  `tk_maternity_pay` (en) 4.37. This is why char-windows were rejected for real
  tokenization. (`Beschäftigungsverbot` = 7 tokens, one word.)
- **Windows validated against reality:** raw section median 188 tok, p90 649, max
  1308; the 800 cap leaves headroom below the mass. Final chunk distribution:
  median **360**, p75 474, p90 581, **max 791 (0 over cap)**, 63 below the 250
  floor (accepted short Q&A answers).

### Overflow cascade & parent retrieval

Oversized sections split at **absorbed sub-part headings → paragraph → sentence**
(never an arbitrary mid-content cut). Every sub-chunk shares `heading_path` and
`parent_section_id`; `parent_section_id` exists so Day-3 can retrieve a small chunk
and return its larger parent section to the model without a re-chunk.

### Bespoke by design

Question-anchoring reads a convention specific to Familienportal (see P1). It would
**not** transfer to a differently-structured client — and that is the job, not a
weakness. A generic splitter would have produced quietly worse retrieval on this
corpus with no signal as to why.

---

## Phase 3 — Metadata annotation

**Output:** all 201 chunks carry `topic` / `subtopic` / `user_type` /
`insurance_type` (0 nulls), filled by `src/annotate.py` — a **deterministic**
annotator (default-by-source + `(source_id, slug)` override tables + ordered
keyword rules), not per-chunk model calls. Idempotent: a re-run reproduces the
same distribution exactly, which is the property worth more than a one-off pass.

The reviewed taxonomy proposal was produced in a prior session that was **never
journaled to disk** and was gone on a cold boot — so it was **reconstructed** from
the corpus + recorded decisions and every divergence flagged, rather than
fabricating the lost "19 / 3-4" counts (the re-derived count came out 16). This is
PM-1: a review artifact must be written to `knowledge/` at creation. Full reasoning
(split-vs-collapse by cost-of-wrong; `any`-is-correct; thin-value-vs-thin-corpus)
in `knowledge/sessions/2026-08-05-day3-metadata.md` and `knowledge/decisions.md`.

`data/chunks.jsonl` is now **tracked** (reversing the Day-2 ignore): derived data is
ignored when it can't be redistributed OR is large — not merely because it's derived.

## Phase 3b — Environment migration (the interpreter was the blocker)

**Lesson (version floor is a project-wide gate, not a per-feature dependency).** The
build ran on **Python 3.7.8**, which ships no wheel for tiktoken (worked around in
Phase 2) and — more importantly — **cannot install chromadb, the MCP SDK, or
LangGraph** (all require ≥3.10). That interpreter silently blocked half the remaining
roadmap, not one feature. The right move was to migrate **before** embedding, while
201 chunks existed and nothing was embedded yet — the cheapest possible moment.

**What was done:** a dedicated `.venv` on **Python 3.11.9**, installed **alongside**
the 3.7 stack (that pinned torch 1.13.1 / transformers 4.30.2 environment looks
deliberate — likely another project — and was left untouched). Torch is the
**CPU-only** wheel (`2.13.0+cpu`, CUDA build `None`, no GPU here) from the PyTorch CPU
index. Everything pinned in `requirements.txt` (with the CPU index embedded); Python
floor recorded there and in the README. Guard verified before proceeding: interpreter
3.11.9, active venv is the project's own, sentence-transformers 5.6.1, chromadb 1.5.9,
rank-bm25 0.2.2. (The venv + deps had in fact been set up in an un-journaled prior
session — another instance of PM-1's "work lives in context, not on disk"; Phase 3b's
real deliverables were the durable ones: `requirements.txt`, README floor, this entry.)

## Phase 4 — Embedding & vector index (E5 + Chroma + BM25)

**Output:** **225 chunks** embedded to a 1024-dim Chroma collection (cosine) + a BM25
sparse index, behind one swappable `search()` interface (`src/retrieval.py`). The
three-test validation gate passed post-reboot (P6 was the environment, not the model).

**Model — `intfloat/multilingual-e5-large`, kept deliberately.** The whole EN/DE design
rests on a cross-lingual space: an English query must retrieve a German passage with
zero shared words. Test 1 measured it directly — parallel `gesund_vorsorge_de` ↔
`gesund_vorsorge_en` content, **mean best-match cosine 0.864** (gate: >0.85; ~0.5 would
have meant the multilingual space collapsed and the test design with it). Loaded in
**fp16** (~1.1 GB, no fp32 peak) at **batch 8** — genuine footprint reductions, not a
model downgrade (see P6/PM-4). Vectors are cast to fp32 and L2-normalised, so cosine ==
inner product. Note: fp16 on this CPU has no hardware acceleration, so a full 225-chunk
build takes ~35 min — a runtime cost, not a quality one.

**The E5 prefix gotcha (why it's verified, not assumed).** E5 is *asymmetric*: passages
must be embedded with `passage: ` and queries with `query: `; omitting a prefix does not
error, it silently degrades retrieval. So the applied prefix is recorded per vector
(`embed_prefix`) and Test 2 proves it changes the vector (`cosine(with, without) =
0.97 < 1`, retrieval delta measurable). This is the same "verify, don't trust a
self-report" discipline as P4.

**E5 vs cl100k tokens (the sizing the chunker asked to confirm — and it didn't hold).**
The chunker sizes in cl100k as a proxy; the model truncates in E5 at 512. Across the
225 chunks the two are close on average (**mean E5/cl100k ratio 0.97**; E5 median 301
vs cl100k 315; E5 DE-median 299, EN-median 320 — German's compounds keep DE token
counts *below* EN even in E5). But "close on average" is not "bounded": the first build
flagged **21 chunks over 512 E5 tokens** (worst 906, ~43% of a core maternity-pay answer
dropped from its dense vector), because at the long tail cl100k *undercounts* relative
to E5 — the opposite of the assumed safe direction. Fixed by enforcing E5's real limit
in the chunker (→ P7); post-fix **max E5 = 500, 0 chunks truncated**.

**Hybrid, not dense-only.** Dense (E5) carries cross-lingual + sub-compound semantics;
BM25 over the *displayed* `text` carries exact rare-token matches (whole compounds like
`Mutterschutzfrist`). Fused with Reciprocal Rank Fusion (rank-based, so the two
incomparable score scales are never normalised against each other). Smoke retrieval
(Test 3) confirmed the split works: DE queries surface DE sources, EN→EN, and
"Wie finde ich eine Hebamme?" returns the midwife-support pages.

## Phase 5 — Retrieval

**Output:** one entry point — `search(query, k=10, filters=None, trace=False)` in
`src/retrieval.py` — every caller goes through it; embedder and vector store stay
swappable behind it. Hybrid by construction: dense (E5 `query: ` prefix, top-20 from
Chroma) + sparse (BM25 over `text`, top-20) fused with RRF, optional metadata
pre-filter, and a full `RetrievalTrace` when `trace=True` (dense/sparse ranks+scores,
chunks-in-both, per-chunk RRF detail, filter exclusions+reasons, assembled-context
cl100k token count, underfill flag, per-stage timings). The trace is built as data is
produced so the Phase-12 visualiser needs no retrofit.

### RRF and why k=60

`rrf_fuse` is six lines, written not imported, so the constant is explainable: a chunk's
fused score is the sum over the lists it appears in of `1/(k + rank)`. **k=60 dampens the
top of each list** — a rank-0 hit contributes `1/60 = 0.0167`, rank-1 `1/61 = 0.0164`,
nearly the same — so one index's single #1 outlier cannot dominate; a chunk both indexes
rank *reasonably* (two `1/(k+rank)` terms) outscores one that either index ranks #1
alone. Smaller k → the very top rank dominates; larger k → flatter. Rank-based, so BM25's
unbounded scores and cosine's [-1,1] are never normalised against each other.

### Pre-filtering tradeoff + the `any`-passthrough (the recall trap)

Filtering is a **pre-filter** (candidates dropped before fusion), so — unlike a
post-filter — an aggressive filter can leave the fused pool below k. Handled explicitly:
`trace.underfilled` records `{requested, available, reason}` rather than silently
returning short (demonstrated: `topic=child-benefits`, a 1-chunk topic → returns 1,
underfilled reported, 38 exclusions logged). **The load-bearing rule:** `user_type=any`
and `insurance_type=any` are the *no-constraint* values, so a chunk tagged `any` must
survive a filter for any *specific* value — `_passes` unions `{any}` into the requested
set for those two fields. Omitting this silently halves recall: `user_type=any` is 59% of
the corpus, `insurance_type=any` 95%. `topic`/`language` have no `any` bucket → exact
match.

### Validation — six queries, dense vs sparse vs fused (`tests/phase5_retrieval.py`)

The honest headline is a **falsified expectation** (→ P8): the a-priori hybrid argument
was "on a bare legal term (`Mutterschutzfrist`, query 3) BM25 will *beat* dense, because
dense blurs rare terms." It did **not** play out that way. E5 is multilingual and
compound-aware, so dense gave the bare compound tight, confident scores (0.90/0.89/0.89)
and put the duration chunk ("Wie lange besteht der Mutterschutz vor der Geburt") at rank
3; BM25 ranked that exact chunk #0 but with a *weak* absolute signal (~4.3, because the
compound is one rare un-split token, not many matching terms). So BM25 had a mild
precision edge on the exact term, not a decisive win — a strong multilingual embedder
largely closes the classic "dense fails on rare terms" gap.

**Where hybrid demonstrably earns its place on this corpus** is the opposite mechanism —
BM25 *rescuing a literally-matching chunk that dense buries*:
- **Query 4** "Wie beantrage ich Elterngeld?": the Elterngeld overview hub ("Was Sie zum
  Elterngeld wissen müssen") sits at **dense rank 11** (outside a dense-only top-10) but
  **BM25 rank 1**; fusion promotes it to **#3**. That chunk only makes the answer because
  of BM25.
- **Query 1** "Wann beginnt die Mutterschutzfrist?": the twins-specific regulation
  ("Welche Regelungen gelten, wenn ich Zwillinge…", which literally contains
  Mutterschutzfrist) is **dense 12 / BM25 0** — again surfaced only by the sparse side.

Cross-lingual still holds (query 2, EN→German-derived TK content top-5; the corpus's
prenatal EN pages rank correctly). Steady-state latency: dense ~0.2–0.5 s, sparse <1 ms,
fusion/filter ~0 ms; the first query of a process shows ~17 s because the E5 model loads
lazily on first embed — a one-time warmup, not per-query cost.

### Filtering proof — query 5, with vs without `user_type=self-employed`

Without a filter, "I am self-employed, do I get maternity pay?" returns **all 10
employee-tagged** `tk_maternity_pay` chunks and **zero self-employed-specific** content —
exactly the silent recall failure the passthrough rule exists to prevent. With
`filters={"user_type": "self-employed"}`: 8 employee chunks drop, the **3 dedicated
`fam_mutterschaftsleistungen` "…wenn ich selbständig bin" chunks surface**, and `any`
chunks are correctly retained alongside them (the filtered set still includes
`user_type=any` prep/benefits pages). Filtering visibly changes the set — and the
passthrough keeps the everyone-content while adding the persona-specific content.

---

## Problem register

### P1 — Hierarchy encoded by convention, not markup (the headline finding)

Per-document Q&A/prose classification by heading-ratio **failed**: the flagship
FAQ (`fam_elterngeld_faq`) scored 0.43 and misclassified as prose. Root cause:
Familienportal marks **every** heading `<h2>` and encodes hierarchy *semantically*
— a trailing "?" means a new topic, a statement heading means a sub-part of the
question above. The structure was never in the markup levels; it was in a
convention. **Response:** replaced the ratio gate with **question-anchored
sectioning**, which reads that convention directly. This is the inverse of the
Phase-1b class of bug (there, structure existed in the HTML and extraction
destroyed it; here, structure was never in the markup to begin with).

### P2 — Guard 1 tripped; we changed the split rule, not the anchoring

The absorption-run guard (a question absorbing >5 following headings) tripped on
2 sections. Investigation: one (`Wie lange kann ich Elterngeld bekommen?`, 6
absorbed) was a *correct* rich answer; the other (`fam_leistungen_ueberblick`, 8)
was 6 real sub-parts + 2 promo teasers. Neither was the failure the guard watched
for — an *unbounded* run producing arbitrary splits (the run was bounded, max 8,
short tail). **Response:** adopted **split-at-heading-boundary** as the primary
overflow cascade (so run length can no longer produce a bad split), and
**re-purposed guard 1 as a canary** (ceiling raised 5 → 12, printed every run) —
it now flags an upstream *shift* in the distribution, not a bad chunk. We changed
the split rule, not the anchoring.

### P3 — Three chunk-quality defects: the chunking/extraction split

Cold-read validation (20 random chunks, `text` only) failed the bar on first pass.
The valuable part was separating causes:

- **Chunking-fixable (fixed this phase):** (a) footer noise packaged as a chunk
  (`"Contact / date"`) → drop sub-5-word bodies; (b) dangling contentless intro
  (`"…neue Regelungen:"`) → fold a thin section-root into its first sub-chunk;
  (c) lists severed from their lead-in → never break a colon lead-in from what it
  introduces, and never let a chunk start with a bare list (backward-glue). Post-
  fix: 0 orphaned list-starts, 0 stubs, 0 footer-chunks.
- **Extraction-rooted (deferred, see P4/P5):** flattened tables. Not a chunker bug.

### P4 — The table contradiction: don't trust a component's self-report

Phase 1b reported "table handler included but defensive (corpus has 0 tables)."
Phase 2 found 4 documents with flattened benefit-calc tables. Both can't be true of
`<table>` markup. Investigation: the markup **is** real `<table><tr><td>`, and
`_table_md` renders it perfectly when handed the node — but these tables are nested
**inside `<p>`** (invalid HTML Familienportal ships anyway), and `collect_blocks`
flattens a `<p>` via `get_text()`, swallowing the nested table before the table
branch is reached. The statute's table was a direct child of the root, so it
rendered fine. **Lesson:** the "0 tables" self-report came from a handler that only
sees top-level tables; it was a component reporting confidently about data it
didn't understand. **Interim response:** tag these chunks `content_kind:
table-degraded` (6 chunks) — findable and down-weightable on Day 3. There is also a
**safety** reason to down-weight: the system is designed *not* to state benefit
amounts, and a flattened number-wall is a hallucination hazard pointing at exactly
that content. Fixing (recurse into `<p>`; re-extract, new hashes) is a deferred
Phase-1b decision.

**Resolved (Phase-1b amendment):** `collect_blocks` now detects a block nested in
a `<p>` and processes the `<p>`'s children in document order (`_emit_mixed`),
flushing inline text before each block so the existing `_table_md` renders it. All
four `<p>`-nested tables recovered into Markdown pipe tables. The `table-degraded`
heuristic had over-fired on the *recovered* tables and on number-heavy prose;
tightened to a single-line, non-pipe, currency-dense run-on. **1 residual**
(`fam_mutterschaftsleistungen`, "Wie hoch ist der Arbeitgeberzuschuss…"): the
source wrote that worked example as **prose with no `<table>` element** — nothing
to recover, it was never a table; kept tagged as a benefit-amount number-wall for
the safety reason above. Broader lesson for Day 3: benefit-amount safety is now
**decoupled from table structure** (recovered pipe tables still contain amounts) —
"don't state amounts" belongs at the retrieval/answer-policy layer, not a
structural `content_kind`.

### P5 — Second extraction-rooted leak: TK `Contact / date` footer

Surfaced in the same cold read: 3 TK chunks (`tk_find_midwife`,
`tk_maternity_benefits`, `tk_maternity_pay_apply`) open with leaked
`"Contact\n\n<date>"` boilerplate the per-domain selector missed. Same class as
P4 (extraction-rooted, not chunking). Deliberately **not** patched in the chunker
— a per-page chrome blocklist is the maintenance burden curation was meant to
avoid. Deferred to the same extraction-fix decision as P4. Residual impact: ~1.5%
of chunks carry a cosmetic prefix; content remains meaningful; overall cold-read
failure rate ≤4.5%, under the 10–15% bar.

**Resolved (Phase-1b amendment):** `DROP_ATTR_PATTERNS` extended with
`contact-button` (the floating `<tkds-floating-action-button>` "Contact") and
`data-and-author` (the `<time>` publish date in `article-header__data-and-author`).
Re-extraction: **0 leaked prefixes** remain across all TK docs. Especially worth
fixing pre-embedding because the leak sat at the *head* of `embed_text`, where it
distorts the vector most.

### P6 — Phase 4 OOM was the environment, not the model (commit-charge exhaustion)

`src/index.py` OOM'd **twice** building the e5-large index — but the failure was
`memory allocation of 67 MB failed` during the model **download** (the Rust `hf-xet`
buffer), *before the model was ever loaded*. That tell is the whole finding: a 67 MB
allocation cannot fail for lack of room for a 2.2 GB model, so **model size was never
the wall**. Measurement located the real one: physical RAM was fine (1.3 GB free), but
Windows **commit charge sat at 98.7%** (limit 63.7 GB = 15.7 RAM + 48 pagefile; only
0.82 GB headroom), with **44 GB of committed memory unattributable to any process or
kernel pool** — the signature of leaked commit from badly-exited processes, which a
reboot clears.

**Why this belongs in the register and not just the model notes:** the reflexive fix
was "e5-large is big, drop to e5-base." That would have *failed identically* (the
download buffer fails the same at any model size) **and** poisoned interpretation — a
subsequently weak cross-lingual Test 1 would have been blamed on 768-dim being too weak
for the EN/DE design, when the true cause was a full commit charge. Downgrading before
diagnosing degrades cross-lingual alignment for no reason and then mis-attributes the
result to the design. **Response:** keep e5-large; reduce genuine footprint anyway
(fp16 load, batch 8) as help *after* understanding the wall, not as a guess; free
commit by rebooting; re-verify commit headroom *before* loading anything post-reboot.
The lesson as a reusable rule is PM-4 (diagnose the resource wall before blaming the
design). Phase 4 code is committed **unrun** at `0442c86`; the three-test validation
gate is still outstanding, to run once the box has headroom (`knowledge/sessions/2026-08-05-phase3b-4-embedding-blocked.md`).

**Resolved (2026-08-06):** rebooted → free commit 0.82 GB → 43 GB; the build ran with no
OOM (headroom, not a smaller model, was the fix — as P6 predicted). Gate green: Test 1
cross-lingual **0.864** (>0.85), Test 2 prefix verified, Test 3 smoke sane. Phase 4 is
**done**. The build's E5-token report then surfaced a *new* problem → P7.

### P7 — A proxy tokenizer can't bound the real one (E5 512-token truncation)

The chunker (`chunk.py`) sizes chunks in **cl100k** tokens (a Phase-2 proxy, chosen
before the embedding model existed); the corpus is embedded with **multilingual-e5-large**,
whose tokenizer **truncates at 512**. The first index build's E5-token report flagged
**21 chunks over 512** — worst `tk_maternity_pay` "How much is maternity pay" at **906**
E5 tokens, ~43% of a core answer silently dropped from its dense vector (a citation
project losing the back half of a "how much do I get paid" answer is the exact failure
the corpus exists to prevent). BM25 over the full `text` cushioned it, but only on
literal word overlap, not meaning.

**The falsified prediction (the part worth keeping).** The Phase-2 assumption was that
cl100k *over*-splits German compounds, so it would *over*count vs E5 — the *safe*
direction to be wrong in (over-splitting only makes chunks smaller than the real limit).
Measurement showed the reverse **at the tail**: for the longest chunks cl100k
*under*counts (max cl100k 791 vs E5 906) — the *unsafe* direction, which is precisely
what let 21 chunks past the real limit. On average the two are close (ratio 0.97), which
is exactly the trap: closeness-in-the-mean is not a bound-at-the-tail. **A wrong
prediction caught by measurement is a better register entry than a right one that was
never tested.**

**Response.** Add an E5-aware final split in the chunker (`enforce_e5_cap`), measured on
the **full embedded string** — `"passage: " + [heading breadcrumb] + text`, exactly what
the model tokenizes — never on `text` alone (that would reintroduce the same error one
layer down). Any chunk over a safe **500**-token budget (12-token margin under 512) is
re-split into *balanced* pieces (`n = ceil(tok/500)`, packed toward `total/n`, so a
524-token chunk becomes ~262/262, not 500/24). Structure still comes from the cl100k
cascade; E5 only enforces the hard truncation limit. Surgical by construction: **179 of
201 chunks unchanged byte-for-byte**, **22 re-split → 46 pieces** (the 22nd was in the
501–512 over-margin band, split though not yet truncating), total **225**. Post-fix
**max E5 = 500, 0 truncated**; re-annotation was automatic (`annotate.py` keys on
`section_slug`/`heading_path`, which sub-chunks inherit); guards pass, 0 nulls; Test 1
moved **0.867 → 0.864** (−0.003, within noise — splitting the 2 EN chunks of the Test-1
pair left cross-lingual alignment intact). Each chunk now stores `e5_token_count`, so
"nothing truncates" is checkable from the tracked `chunks.jsonl` itself.

**Reusable rule:** a proxy tokenizer cannot bound the real one. If a hard limit exists
downstream, measure against the actual tokenizer that enforces it — not a proxy that
merely correlates. (The same build also surfaced PM-5: the cl100k proxy itself lived
outside the repo, so the tracked corpus wasn't reproducible; both were fixed together.)

### P8 — Hybrid helps, but not for the reason we argued (BM25 vs dense on a bare legal term)

The a-priori case for hybrid retrieval was: a bare German legal term like
`Mutterschutzfrist` (validation query 3) would **defeat dense** — a rare compound blurs
in the embedding space — and **BM25's exact-token match would beat it**, justifying the
sparse index. The validation was run specifically to *see* this. It didn't happen. E5 is
multilingual and compound-aware: dense returned the bare compound with tight, confident
cosines (0.90/0.89/0.89) and ranked the exact duration chunk at #3, while BM25's absolute
signal on the single un-split token was *weak* (~4.3 vs ~30 on a multi-term query). BM25
had only a mild precision edge (the exact chunk at #0 vs dense's #3), not the decisive win
predicted.

**Why keep BM25 anyway — the real, measured justification.** Hybrid earns its place
through the *opposite* mechanism: BM25 rescues a literally-matching chunk that dense
buries below the cut. Query 4 (Elterngeld) — the overview hub is **dense 11 / BM25 1**,
fusion lifts it to #3; query 1 — the twins-specific Mutterschutzfrist regulation is
**dense 12 / BM25 0**. Neither reaches a dense-only top-10 on its own. So the sparse index
is justified by evidence, just not the evidence we expected to cite.

**Reusable lesson:** run the experiment that could *falsify* your architectural argument,
not the one that confirms it, and let the result rewrite the claim. A strong multilingual
embedder narrows the classic "dense fails on rare terms" gap; the sparse index's value on
this corpus is *rank rescue of exact/edge matches*, and that is the claim to make out
loud — because it's the one the data supports. (Same discipline as P7's falsified
tokenizer prediction: a wrong prediction caught by measurement beats an untested right
one.)
