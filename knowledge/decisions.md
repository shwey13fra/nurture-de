# Decision Log — NurtureDE

## 2026-08-03 — Day 1

- **No new dependencies for fetch/extraction.** Use stdlib `html.parser` for text
  extraction (content hash + SPA heuristic). Rationale: good enough for a *stable
  hash* and *size heuristic*; high-quality boilerplate-stripped extraction is a
  Day-2 concern where we'll propose trafilatura/bs4. Trade-off: crude extraction
  now, but zero install and reproducible.

- **Comment-safe writeback to sources.yaml via targeted in-place line edits**
  (keyed on `id`), not `pyyaml.dump`. Rationale: the YAML is hand-authored with
  explanatory comments that dump would destroy. Alternative considered: sidecar
  `manifest.json` (rejected — spec says write to sources.yaml) and `ruamel.yaml`
  round-trip (rejected — new dependency).

- **Do not bypass access controls.** frankfurt.de returns 403 to our research UA;
  we do NOT spoof a browser UA to evade it. A provenance/citation project should
  fetch only what sources permit us to fetch as ourselves. Manual capture is the
  allowed escape hatch if city-specific detail is needed later.

- **Birth-registration sourced from Familienportal, not the municipal/portal pages.**
  verwaltung.bund.de is a SPA (uncrawlable via simple GET); frankfurt.de 403s.
  Familienportal `anmeldung-standesamt` is clean, federal, same well-behaved domain.

- **pairs_with used to stage register-distinction evals.** `bmas_mutterschutzgesetz`
  (statute/employer register) ↔ `fam_mutterschutz` (plain-language register), and
  the TK Mutterschaftsgeld pages ↔ `fam_mutterschaftsleistungen` (federal rule vs
  insurer process). Purpose: Day-3 test that the system cites the right register.

## 2026-08-03 — Day 2

- **beautifulsoup4 for extraction (new dep, approved).** Three sites use
  incompatible containers and TK uses custom elements — needs a queryable tree +
  subtree deletion + custom-tag traversal. Chose bs4 (explicit, auditable
  per-domain selectors) over stdlib (would hand-roll a DOM) and over trafilatura
  (heuristic/non-deterministic; can't target TK's `<tkds-*>`). Provenance projects
  want auditable selection, not "a model guessed the main block."

- **Output clean Markdown, hash from the clean text.** Day-1's flattened text was
  unusable for chunking. Re-extract from cached `data/raw/` (no re-fetch) to
  `data/processed/*.md`; recompute all `content_hash` from Markdown. Intentional —
  old hashes fingerprinted boilerplate. `last_verified_date` unchanged (not re-fetched).

- **Unwrap, don't delete, structural wrappers that carry headings.** gesund nests
  `<h2>` in `<button>` and `<h1>` in `<header>`; deleting the tag deletes the
  heading. Unwrap keeps contents. General lesson: strip chrome by class/role, not
  by structural tag name.

- **Decode by the page's declared charset, never a hardcoded encoding.**
  gesetze-im-internet.de is ISO-8859-1; a fixed UTF-8 read corrupted the statute
  title. Reuse header→meta→utf-8→latin-1 detection everywhere bytes are decoded.

- **`authority_tier: primary-law` + lifecycle fields (`status`/`superseded_by`).**
  When the BMAS "statute" proved to be a 140-char stub, re-pointed to the real law
  on gesetze-im-internet.de as `primary-law` (ranks above `federal`, a Day-3
  ranking signal). Kept the old entry as `superseded_by` the new id — correct a
  source by superseding with a record, never silently swap. Superseded entries are
  not ingested.

- **Stub tripwire in extraction.** Flag any source whose clean extraction is <500
  chars as a probable stub / JS-rendered page needing manual review. Abstracts the
  BMAS-stub mistake into a check that catches the whole class automatically.

## 2026-08-04 — Phase 1c

- **`gii_muschg_2018` reclassified `superseded` (not fetched deeper).** The
  gesetze-im-internet.de statute root is a table-of-contents frame (§§ 1-34 titles,
  ~2.8k chars, no normative text); the real text is on 34 per-§ pages. Chose NOT to
  crawl them: (1) 34 URLs is a crawl, not curation; (2) it adds a fourth site-specific
  boilerplate family; (3) legalese is the wrong register for the user — the federal
  portal (`fam_mutterschutz`) is the authoritative plain-language source. Statute
  citation moves to the README roadmap as a supporting-EVIDENCE layer, never
  user-facing. `superseded_by: fam_mutterschutz`; retained as a provenance record.
  Active corpus is now **22** (federal 18, statutory-insurer 4, primary-law 0);
  superseded 2 (`bmas_mutterschutzgesetz`, `gii_muschg_2018`); 24 entries total.

## 2026-08-05 — Day 3 (metadata annotation)

- **Metadata applied by a deterministic annotator, not per-chunk model calls.**
  `src/annotate.py`: default-by-source + explicit `(source_id, slug)` override
  tables for topic/user_type/insurance_type; ordered keyword rules for subtopic.
  Rationale: matches the project's auditable-selection ethos (Phase-1b), is
  idempotent/re-runnable, and makes every override spot-checkable. `chunks.jsonl`
  is derived/git-ignored, so regeneration is safe.

- **Taxonomy reconstructed after the reviewed proposal was lost.** The proposal
  the reviewer approved was produced in an un-journaled prior session and was
  not on disk. Chose to reconstruct from corpus + the five decisions and flag
  the baseline + re-derived override lists as reconstructed, rather than
  fabricate "the 19 / the 3-4" as if retrieved. Fabricating provenance in a
  provenance project is the failure mode the corpus exists to prevent. Lesson →
  Past Mistakes: a "STOP for review" artifact (Task 5 metadata proposal) must be
  written to `knowledge/` at creation, not left in session context.

- **Split vs collapse is decided by cost-of-wrong, not by count.** `Beamtin` got
  its own `civil-servant` value at ~1 section (distinct legal regime; wrong
  regime = wrong answer); `Schülerin` collapsed into `student` at similar count
  (overlapping guidance, out of persona scope; only cost is a missed nuance).
  Same governing principle, opposite outcomes — recorded in full in the Day-3
  session journal because being able to explain the asymmetry is what shows the
  vocabulary was reasoned, not transcribed.

- **`any` as the majority user_type/insurance value is correct, not a defect.**
  It denotes "no persona/insurance filter applies." A >40% *topic* value would
  be non-discriminating; a >40% `any` is the expected absence-of-constraint
  bucket that every filtered query falls back to.

- **Near-zero boilerplate reduction is itself a stub signal.** `gii_muschg_2018`
  *grew* under clean extraction (-9.2%: TOC → Markdown table). Generalized: a
  document that loses almost nothing to boilerplate stripping probably has no prose
  content. Pair "reduction ≈ 0% or negative" with the existing <500-char floor as a
  two-pronged corpus-validation heuristic — either alone misses cases the other
  catches (a long TOC passes the char floor; a short real snippet has high reduction).

- **Ignore policy reversal: `data/chunks.jsonl` is now TRACKED.** Day-2 ignored it
  as "derived." Corrected: derived-ness alone is not the criterion. `data/raw/` and
  `data/processed/` are ignored because they redistribute **someone else's fetched
  content** — `chunks.jsonl` carries no such constraint, is small (748K), and its
  whole value this phase is that the taxonomy is *reasoned*. If reading a chunk's
  tags required installing Python 3.11 + 2.2GB of model weights, that reasoning is
  invisible in the repo; tracking it also makes tag changes **diffable** (a re-chunk
  shows which tags moved, not just a distribution delta). New rule: **derived data is
  ignored when it can't be redistributed OR is large — not merely because it's
  derived.** (The `chroma_db/` vector store stays ignored: large + rebuildable.)

## 2026-08-06 — Phase 4 (embedding + index; E5 512-cap fix)

- **The chunker now enforces E5's real 512-token limit, not a cl100k proxy.** cl100k
  (Phase-2's tokenizer) tracks E5 closely on average (ratio 0.97) but *undercounts* at
  the long tail, letting 21 chunks truncate at embed time (worst 906 E5 tokens). Added
  `enforce_e5_cap` in `chunk.py`: a final split measured on the **full embedded string**
  (`"passage: " + heading breadcrumb + text`) that balances any >500-token chunk into
  pieces under the limit. Kept cl100k for the structural cascade (re-tuning everything to
  E5 would shift all 201 boundaries — rejected for blast radius); E5 only guards the hard
  cap. Surgical: 179/201 chunks unchanged, 22 re-split → 46, total 225, 0 truncated.
  Each chunk now stores `e5_token_count`. Full reasoning in `BUILD_JOURNAL.md` P7. (→ PM-5
  reusable rule: measure against the tokenizer that actually enforces the limit.)

- **cl100k is vendored in-repo (`src/vendor/`), not imported from a Temp scratchpad.**
  The tracked `chunks.jsonl` previously regenerated only via a hardcoded path into a dead
  session's Temp dir (`chunk.py:36`), which itself read an out-of-repo 1.68 MB vocab blob
  — the tokenizer defining every chunk boundary was outside version control. Vendored both
  with a `__file__`-relative path (chose the self-contained pure-Python reimpl + blob over
  adding `tiktoken`, which would re-download the vocab to an out-of-repo cache — worse for
  offline reproducibility). A `src/` audit confirmed it was the only out-of-repo read.
  Rule → PM-5.

- **`chroma_db/` must be wiped before a re-index, not upserted onto.** `ChromaStore.upsert`
  keys on `chunk_id` and never deletes; after a re-split the old truncated vectors would
  linger under their old ids. Rebuilds start from a clean `chroma_db/` (gitignored,
  rebuildable). `bm25.pkl` is fully overwritten by `SparseIndex.build`, so it needs no
  special handling.

## 2026-08-06 — Phase 5 (retrieval)

- **`any` is a filter-passthrough, not a filter value.** `user_type=any` /
  `insurance_type=any` mean "no persona/insurance constraint applies," so `_passes`
  unions `{any}` into the requested set for those two fields — a chunk tagged `any`
  survives a filter for any specific value. Exact-match here would silently halve recall
  (`any` is 59% / 95% of the corpus). `topic`/`language` have no `any` bucket → exact.

- **Filtering is a pre-filter, and underfill is surfaced, not hidden.** Candidates are
  dropped before RRF fusion (records exclusion reasons for the trace), which means an
  aggressive filter can leave the pool below k — unlike a post-filter. `trace.underfilled`
  reports `{requested, available, reason}` instead of returning short silently. Cost of
  pre- over post-filter: recall risk when POOL (20/index) is small vs. an aggressive
  filter; accepted for now (corpus is 225 chunks) and visible in the trace. Server-side
  Chroma `where` is the swap if pre-filter recall ever bites — but it would hide the
  exclusion reasons the visualiser wants.

- **RRF written, not imported (k=60).** Six lines, so the damping constant is explainable
  and ownable; k=60 flattens the top so no single index's #1 dominates. Rank-based fusion
  avoids normalising BM25's unbounded scores against cosine.

- **Sparse index justified by rank-rescue, not by beating dense on legal terms.** The
  validation falsified the a-priori "BM25 beats dense on a bare compound" argument (E5 is
  compound-aware); BM25's measured value is surfacing exact/edge chunks dense buries
  (query 4: dense 11 → fused 3). Full evidence + lesson in `BUILD_JOURNAL.md` P8.

## 2026-08-06 — Phase 6 (generation)

- **The answer-policy system prompt is a human-owned file, not code.** It lives in
  `src/prompts/answer_system_prompt.md` and `generate.py` loads it per call. The judgment
  layer (what to refuse, when to ask, how to cite) belongs to the reviewer; the code owns
  everything around it. Editing the file changes behaviour with no code change.

- **Report-vs-determine, not blanket amount-refusal.** "Never state a benefit amount"
  contradicts "answer only from context" — a source-stated figure is a corpus fact, and
  suppressing it makes the tool useless for the highest-demand questions. Shipped rule:
  report what a source says (amounts/durations/conditions included, cited), never tell a
  user what applies to *them* (no "you will receive €X", no "you are eligible"). Send
  personal determinations to the deciding authority (insurer/employer/office).

- **Retrieved content is untrusted data, wrapped and escaped.** Chunks go in the user turn
  inside `<retrieved_documents>`/`<document>`; text is HTML-escaped so a chunk cannot forge
  a document boundary; the system prompt declares the block is data, never instructions.
  Chosen from the start (not retrofitted) because the corpus contains real promotional/hub
  text. A poisoned chunk was defeated in validation.

- **Model: Claude Opus 5 for generation, adaptive thinking, system prompt cached.** Opus 5
  is the generator (held constant so Phase-8 can vary retrieval config cleanly). The
  refuse/ask/answer decision benefits from adaptive thinking. `stop_reason == "refusal"`
  (classifier) is handled before reading content. The **LLM-as-judge for Phase 8 will be a
  cheaper model** — faithfulness checking doesn't need frontier reasoning, and a different
  judge model avoids grading-its-own-homework bias (recorded in the Phase-8 forward note).

- **Context order: top-4 post-RRF, most-relevant LAST.** Models attend most reliably to the
  end of context, so rank-1 is the final document. The Phase-8 reranker replaces the plain
  top-4 slice at this seam. Assembled size reported in cl100k tokens (vendored tokenizer,
  no API round-trip).
