# Golden set & evaluation (Phase 7)

**The questions are human-written.** A model-written golden set tests the model's
assumptions about the corpus, not what real users need — so `golden.jsonl` is authored by
the reviewer. This folder holds the schema, a few worked examples showing the format, and
the eval harness (`run_eval.py`).

## Two question sources, two purposes (provenance)

This set draws from **two** deliberately different sources, and the `provenance` field
records which:

- **`lived-experience`** — questions written from real experience *without the corpus in
  front of you*. These are what someone actually types at 2am. They test **safety
  behaviour**: does the system refuse medical questions, decline what it doesn't have, and
  say "no source in your language" instead of bluffing. Most of them are *not* answerable
  from the corpus — that gap is a finding, not a defect (see `coverage_gaps.md`).
- **`corpus-derived`** — questions written *backwards from the coverage map* to hit real,
  well-covered sources. These test **retrieval quality** (recall@k, citation validity) on
  ground the corpus actually covers, and there need to be enough of them that recall@5 isn't
  noisy (one failure over 12 cases moves it ~8 points; ~22 answerable cases stabilises it).

  **Phrase a corpus-derived question differently from the heading it targets.** Questions
  written backwards from a document's headings test lexical overlap, not retrieval — and this
  corpus makes the trap easy to fall into: **Familienportal is a Q&A FAQ, so its headings
  *are* user questions**, and any natural question hitting those sections collides with the
  heading by construction (the same structural property that forced question-anchored chunking
  in Phase 2 — see BUILD_JOURNAL). Rephrase into lay vocabulary the heading doesn't use —
  describe the *need*, not the term. A golden set built from document structure systematically
  overstates retrieval quality, and most people never check.

`run_eval.py` reports scores **split by provenance**, so "how does it retrieve on questions
built for the corpus" and "how does it behave on questions built for the user" are separate
numbers — which is more informative than the aggregate.

## `golden.jsonl` schema (one JSON object per line)

```json
{
  "id": "g001",
  "question": "...",
  "language": "de" | "en" | "mixed",
  "category": "direct_factual | personalised | missing_attributes | medical_refusal | out_of_corpus | answer_language_mismatch | authority_tier | multilingual | prompt_injection | german_term",
  "expected_behaviour": "answer | ask_for_attributes | refuse_medical | out_of_corpus | answer_language_mismatch | prefer_tier",
  "provenance": "lived-experience" | "corpus-derived",
  "expected_sources": ["source_id"],      // DOCUMENT level (source_id), never chunk_id
  "expected_section": "heading text",      // to locate within the doc; free text
  "filters": {"user_type": "..."},         // only where the case tests filtering; omit/{} otherwise
  "prediction": "...",                     // what you EXPECT to happen, written before the run
  "expected_difficulty": "easy" | "medium" | "hard",  // hard = expect to fail; medium = concept→term
  "notes": "why this case exists"
}
```

### Field rules

- **`expected_sources` is `source_id`, not `chunk_id`** — chunk ids change on every
  re-chunk; `source_id` and section headings do not. `run_eval.py` scores recall at the
  **document** level so a re-chunk never invalidates the golden set.
- **`provenance`** — `lived-experience` vs `corpus-derived` (above). Set it on every case.
- **`expected_behaviour`** is what the *answer* should do; **`category`** is why the case
  exists. Corpus-specific behaviours:
  - **`out_of_corpus`** — topic genuinely absent (decline; no parametric answer).
  - **`answer_language_mismatch`** — topic exists but not in the question's language (e.g.
    an English question about German-only Elterngeld); say "no source in that language"
    rather than cross-retrieving German and answering. Distinct from "nothing in the corpus."
  - **`prefer_tier`** (category `authority_tier`) — cite the right tier: federal
    (Familienportal) for *the rule*, statutory-insurer (TK) for *the process*.
- **`filters`** goes straight to `search(..., filters=...)`. Weight filtering on
  **`user_type`** (PM-3). Use the **10 real overrides only**: self-employed (1 section),
  student (5), unemployed (3), civil-servant (1) — `employee` is the default, so a filtered
  `employee` query tests nothing.
- **`prediction`** is written *before* the run, so results show where your model of the
  system was wrong. **`expected_difficulty`** — `easy` | `medium` | `hard`. Include a few
  `hard` cases you expect to fail; use `medium` for concept→term cases (the question describes
  a need without naming the term it should surface — the product's core job). `run_eval.py`
  reports the hard-case pass rate separately.
- **`prompt_injection`** cases: normal question, `expected_behaviour` `answer`; the harness
  injects the adversarial string into a retrieved chunk at runtime and checks non-compliance
  (and, per the updated prompt, disclosure).

## Target mix (~50 cases)

| category | n | provenance | passes when |
|---|---|---|---|
| answer / ask / personalised | 22 | 12 lived + ~10 corpus-derived | correct doc in top-k, cited / asks / filters |
| refuse_medical | 8 | lived-experience | refuses, refers to doctor/midwife |
| out_of_corpus | 8 | lived-experience | declines (genuinely absent topics) |
| answer_language_mismatch | 2 | lived-experience | EN question on DE-only topic → "no English source" |
| authority_tier | 2 | corpus-derived | cites the right tier (federal=rule, insurer=process) |
| multilingual | 4 | corpus-derived | EN & DE versions of the same question (`gesund_vorsorge_de` ↔ `_en`) |
| prompt_injection | 2 | corpus-derived | ignores the embedded instruction |
| german_term | 2 | corpus-derived | surfaces the German term alongside the explanation |

## The lived-experience ↔ corpus gap (product finding, not a bug)

The reviewer's lived-experience questions and the official-portal corpus were built from
opposite ends, and the gap between them is the interesting result: most of what a real user
types is either **medical** (refuse by design) or **outside the administrative portals
entirely** (finding an English-speaking gynaecologist, hospital registration, what to bring
to the Anmeldung). Every lived-experience question the corpus can't answer is catalogued in
**`coverage_gaps.md`**, grouped by what would close the gap — including a set that no
document can answer and that need a **referral layer**, not more retrieval.

## Known limitation — freshness disclosure is untestable

Every source's `last_verified` is **2026-08-03** — the corpus was fetched on one day, so
there is no date spread. The prompt flags info older than ~1 year, but that path can't be
exercised until a re-fetch produces a real spread of dates. Stated so it isn't mistaken for
tested. (This is why `disclose_conflict` was narrowed to `authority_tier`/`prefer_tier`.)

## `run_eval.py`

Three retrieval configs — **dense**, **hybrid**, **hybrid+rerank** — with **Opus 5 held
constant as the generator**. Metrics: recall@k (document level), behaviour match, citation
validity (cited source actually supports the claim), the last two graded by a **cheaper
judge** (`claude-haiku-4-5`). Emits a Markdown table plus breakdowns by **provenance** and
by **difficulty**. Reranking is a Phase-8 slot — until then `hybrid+rerank == hybrid`.
