# Design — E5 token-cap enforcement in the chunker (Phase 4 fix)

_Date: 2026-08-06 · Status: approved, pre-implementation_

## Problem

The index build (`src/index.py`) succeeded but its E5-token report flagged **21 of
201 chunks over E5's 512-token truncation limit** (worst: `tk_maternity_pay` "How
much is maternity pay", 906 E5 tokens — ~43% of a core answer silently dropped from
its dense vector). `transformers` confirmed it at build time (`524 > 512`).

### Root cause

The chunker (`src/chunk.py`) sizes chunks in **cl100k** tokens (`CAP = 800`), but the
corpus is embedded with **multilingual-e5-large**, whose tokenizer truncates at
**512**. cl100k was a Phase-2 proxy (chosen before the embedding model existed; a
pure-Python reimpl because tiktoken has no Py3.7 wheel). The chunker header assumed
"a multilingual tokenizer shifts German counts ~15-20%, which the headroom absorbs."
That held for ~90% of chunks and failed for 21.

### The finding — a falsified prediction (record as such)

The prediction was: cl100k **over**-splits German compounds, so it would **over**count
relative to E5 — the *safe* direction to be wrong in (over-splitting only makes chunks
smaller than needed). Measurement showed the opposite **at the tail**: for the longest
chunks cl100k **under**counts (max cl100k 791 vs max E5 906) — the *unsafe* direction,
which is exactly what let chunks past the real limit. A wrong prediction caught by
measurement is the entry worth keeping. Generalized lesson (→ register P7): **a proxy
tokenizer cannot bound the real one; if a hard limit exists downstream, measure against
the actual tokenizer that enforces it.**

## Approaches considered

- **A — Surgical E5-aware post-split in `chunk.py` (CHOSEN).** Keep the cl100k cascade
  for all structure; add a final pass that re-splits only chunks whose *embedded
  string* exceeds a safe E5 budget. Blast radius = the 21 oversized parents only; the
  other 180 chunks stay byte-identical.
- **B — Re-tune the whole chunker to E5 units.** One tokenizer, conceptually clean, but
  re-tuning FLOOR/TARGET/CAP shifts *every* boundary → all 201 chunks change → full
  re-annotation and re-review. Over-engineered for "fix 21 truncated chunks." Rejected.
- **C — External one-off split script.** Creates a second authority on chunk boundaries
  that `chunk.py --write` would silently undo; violates the reproducible/auditable
  ethos. Rejected.

Priority order (Correct → Simple → Maintainable → …) selects **A**.

## Design (Approach A)

### 1. E5 tokenizer in `chunk.py`
Load `transformers.AutoTokenizer.from_pretrained("intfloat/multilingual-e5-large")` —
**tokenizer only, no 2.2 GB weights**. Lazy module-level singleton. `chunk.py` already
runs under the 3.11 venv (verified: it reproduces the committed `chunks.jsonl`
byte-for-byte), and the venv has `transformers`.

### 2. `enforce_e5_cap(texts, prefix)` — runs after `split_texts` in `build_chunks`
- **Budget measured on the FULL embedded string**, never on `text` alone:
  `PASSAGE_PREFIX + embed_text` where `embed_text = prefix + "\n" + text` and
  `prefix = "[" + " › ".join(heading_path) + "]"`. This is exactly what `index.py`'s
  report and the model itself tokenize. Measuring `text`-only would reintroduce the
  same class of error one layer down.
- **Threshold `E5_SAFE = 500`** (12-token margin under 512 for special tokens).
- For any text over budget: `n = ceil(tokens / E5_SAFE)`; greedy-pack paragraphs (then
  sentences, reusing the existing `_split_block`-style cascade but measured in E5
  tokens) toward `total / n` **balanced** pieces, so no tiny sub-floor tail is created
  (a 524-token chunk splits into ~262/262, not 500/24).
- Texts already ≤ `E5_SAFE` pass through untouched.
- Edge case: if a single sentence alone still embeds > 512 (not expected in this
  corpus), leave it whole and let the existing `index.py` report flag it, rather than
  hard-splitting mid-sentence (worse for retrieval). Verification asserts 0 such cases.

### 3. Store `e5_token_count` per chunk
`chunks.jsonl` is tracked *for auditability*; recording the real E5 count makes "no
chunk truncates" checkable from the file itself, not only from a build run.

### 4. Re-annotation is automatic
`annotate.py` keys overrides on `(source_id, section_slug)` and derives `subtopic` from
`heading_path`. Sub-chunks inherit both, so new pieces receive correct metadata with no
table changes.

### 5. Re-index from a wiped store
`ChromaStore.upsert` keys on `chunk_id` and **never deletes**. New sub-chunks get new
ids, so the 21 old truncated vectors would linger. Re-index must start from a wiped
`chroma_db/` (gitignored, rebuildable). `bm25.pkl` is fully rebuilt by
`SparseIndex.build`, so it needs no special handling.

### 6. Vendor `cl100k.py` into the repo — provenance fix, not tidy-up
The tracked `chunks.jsonl` currently regenerates **only** via a hardcoded Temp path
from a dead session (`chunk.py:36` → `…/ffd95014-…/scratchpad/cl100k.py`). The artifact
is versioned but the tokenizer defining every boundary is not — artifact and provenance
have diverged, and a Windows temp-clean would make the corpus unregenerable. Same class
as PM-1 (load-bearing thing outside version control), now recurred → **PM-5**.

- Move `cl100k.py` to `src/vendor/cl100k.py` (add `src/vendor/__init__.py`).
- Replace the `sys.path.insert(...Temp...)` hack with a normal package import.
- **Audit result (done):** the cl100k path is the *only* unversioned/absolute-path
  dependency in `src/`. Every other module resolves paths via `__file__` or uses
  stdlib/venv packages. No other holes.

## Blast radius
- `chunks.jsonl`: 201 → ~222 chunks (exact count reported post-run). Only the 21
  oversized parents change; the other 180 chunk_ids/texts are byte-identical.
- Code: `src/chunk.py` (E5 cap + import fix), new `src/vendor/cl100k.py` +
  `__init__.py`. No change to `annotate.py`, `retrieval.py`, `index.py`,
  `validate_phase4.py`.

## Verification gate (all must pass before commit)
1. `chunk.py --guards` — absorption / zero-question / split-rate invariants hold.
2. `annotate.py` count report — value distribution unchanged in character, **0 nulls**,
   no vocab regressions.
3. `index.py` token report — **assert 0 chunks > 512 E5 tokens**.
4. `validate_phase4.py` — Test 1 (cross-lingual ≥ 0.85), Test 2 (prefix), Test 3
   (smoke) all pass.

### Reports to produce (requested)
- Final chunk count; how many of the 21 parents split, and into how many pieces.
- Confirmation the other 180 chunks are byte-identical to the committed version.
- Whether Test 1 cross-lingual similarity **moved** after re-chunking (either direction)
  — does splitting the long chunks change alignment.

## Knowledge updates (part of this change)
- **PM-5** (`knowledge/past-mistakes.md`): "If regenerating a tracked artifact depends
  on it, it must be in the repo — including tooling, not just data." Note that PM-4 was
  already taken (resource-wall lesson); this is PM-5, numbering flagged not overwritten.
- **P7** (`BUILD_JOURNAL.md` problem register): the proxy-tokenizer finding + the
  falsified prediction, plus the Phase-4 truncation fix narrative and cross-lingual
  before/after.
- `decisions.md`: cl100k vendored; E5 512-cap now enforced in the chunker.
