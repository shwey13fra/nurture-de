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
| 2  | Heading-aware chunking (`chunk.py` → `data/chunks.jsonl`)             | **done** |
| 3  | Embedding & vector index                                             | next |

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
