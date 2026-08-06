# Golden set & evaluation (Phase 7)

**The questions are human-written.** A model-written golden set tests the model's
assumptions about the corpus, not what real users need — so `golden.jsonl` is authored by
the reviewer. This folder holds the schema, a few worked examples showing the format, and
the eval harness (`run_eval.py`).

## `golden.jsonl` schema (one JSON object per line)

```json
{
  "id": "g001",
  "question": "...",
  "language": "de" | "en" | "mixed",
  "category": "direct_factual | personalised | missing_attributes | medical_refusal | out_of_corpus | answer_language_mismatch | authority_tier | multilingual | prompt_injection | german_term",
  "expected_behaviour": "answer | ask_for_attributes | refuse_medical | out_of_corpus | answer_language_mismatch | prefer_tier",
  "expected_sources": ["source_id"],      // DOCUMENT level (source_id), never chunk_id
  "expected_section": "heading text",      // to locate within the doc; free text
  "filters": {"user_type": "..."},         // only where the case tests filtering; omit/{} otherwise
  "prediction": "...",                     // what you EXPECT to happen, written before the run
  "expected_difficulty": "easy" | "hard",  // deliberately include 3-4 hard cases you expect to FAIL
  "notes": "why this case exists"
}
```

### Field rules

- **`expected_sources` is `source_id`, not `chunk_id`** — chunk ids change on every
  re-chunk; `source_id` and section headings do not. `run_eval.py` scores recall at the
  **document** level so a re-chunk never invalidates the golden set.
- **`expected_behaviour`** is what the *answer* should do; **`category`** is why the case
  exists (they usually align but need not — a `multilingual` case's behaviour is `answer`).
  Two behaviours are corpus-specific:
  - **`out_of_corpus`** — the topic is genuinely absent (decline; do not answer from
    parametric knowledge).
  - **`answer_language_mismatch`** — the topic exists in the corpus but **not in the
    question's language** (e.g. an English question about Elterngeld, which is German-only).
    The system should say it has no source *in that language* rather than cross-retrieving
    German text and answering anyway. This is a distinct failure from "nothing in the corpus."
  - **`prefer_tier`** (category `authority_tier`) — answers and cites the **right authority
    tier**: the federal source (Familienportal) for *the rule*, the statutory-insurer source
    (TK) for *the process*. Replaces the old `disclose_conflict`: the corpus has no date
    spread (see below), so recency can't be tested, but tier-preference is a real design
    decision and is testable.
- **`filters`** is passed straight to `search(..., filters=...)`. Weight filtering cases on
  **`user_type`** (many real values), not `insurance_type` (thin) — PM-3. Use the **10 real
  overrides only** (`employee` is the default on the employment-linked sources, so a filtered
  `employee` query tests nothing): self-employed (1 section), student (5), unemployed (3),
  civil-servant (1).
- **`prediction`** is written *before* the eval runs, so the results tell you where your
  model of the system was wrong — not just what failed. `run_eval.py` does not consume it;
  it's for you to compare against.
- **`expected_difficulty`** — include ~3–4 `hard` cases you expect to fail (thin coverage,
  ambiguous phrasing, cross-document questions). If all 40 pass, the set is too easy to learn
  from. `run_eval.py` reports the pass rate on `hard` cases separately.
- **`prompt_injection`** cases: the question is normal and `expected_behaviour` is `answer`;
  the harness injects the adversarial string into a retrieved chunk at runtime and checks the
  answer does not comply (and, per the updated prompt, discloses it).

## Target mix (~40 cases; the counts below sum to 42)

| category | n | passes when |
|---|---|---|
| direct_factual | 12 | correct doc in top-k, cited |
| personalised | 6 | filters applied correctly (from the 10 real overrides only) |
| missing_attributes | 5 | asks for employment/insurance instead of assuming |
| medical_refusal | 4 | refuses, refers to doctor/midwife |
| out_of_corpus | 3 | declines (incl. genuinely absent topics) |
| answer_language_mismatch | 2 | EN question on a DE-only topic → says "no English source" |
| authority_tier | 2 | cites the right tier (federal=rule, insurer=process) |
| multilingual | 4 | EN and DE versions of the same question (`gesund_vorsorge_de` ↔ `_en` is the clean pair) |
| prompt_injection | 2 | ignores the embedded instruction |
| german_term | 2 | surfaces the German term alongside the explanation |

## Known limitation — freshness disclosure is implemented but untestable

Every source's `last_verified` is **2026-08-03** — the whole corpus was fetched on one day.
The answer prompt flags information older than ~1 year, but with no date spread that path
**cannot be exercised** by the golden set. It only becomes testable after a re-fetch months
later. Stated here so the freshness behaviour isn't mistaken for "tested."

## `run_eval.py`

Scores three retrieval configs — **dense**, **hybrid**, **hybrid+rerank** — with **Opus 5
held constant as the generator**, so the variable under test is retrieval only. Metrics:
recall@k (document level), behaviour match, and citation validity (does the cited source
support the claim), the last two graded by a **cheaper judge model** (`claude-haiku-4-5`).
Emits a Markdown table plus a `hard`-case breakdown. Reranking is a Phase-8 slot — until
then `hybrid+rerank == hybrid` (a documented no-op), so the harness structure is complete
now and the reranker drops into one function.
