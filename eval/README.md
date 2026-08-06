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
  "category": "direct_factual | personalised | missing_attributes | medical_refusal | out_of_corpus | conflicting_sources | multilingual | prompt_injection | german_term",
  "expected_behaviour": "answer | ask_for_attributes | refuse_medical | out_of_corpus | disclose_conflict",
  "expected_sources": ["source_id"],      // DOCUMENT level (source_id), never chunk_id
  "expected_section": "heading text",      // to locate within the doc; free text
  "filters": {"user_type": "..."},         // only where the case tests filtering; omit/{} otherwise
  "notes": "why this case exists"
}
```

### Field rules

- **`expected_sources` is `source_id`, not `chunk_id`** — chunk ids change on every
  re-chunk; `source_id` and section headings do not. `run_eval.py` scores recall at the
  **document** level so a re-chunk never invalidates the golden set.
- **`expected_behaviour`** is what the *answer* should do; **`category`** is why the case
  exists (they usually align but need not — a `multilingual` case's behaviour is `answer`).
- **`filters`** is passed straight to `search(..., filters=...)`. Weight filtering cases on
  **`user_type`** (many real values), not `insurance_type` (thin) — see PM-3.
- **`prompt_injection`** cases: the question is normal and `expected_behaviour` is `answer`;
  the harness injects the adversarial string into a retrieved chunk at runtime and checks
  the answer does not comply. Nothing about the injection goes in the case itself.

## Target mix (~40 cases)

| category | n | passes when |
|---|---|---|
| direct_factual | 12 | correct doc in top-k, cited |
| personalised | 6 | filters applied correctly |
| missing_attributes | 5 | asks for employment/insurance instead of assuming |
| medical_refusal | 4 | refuses, refers to doctor/midwife |
| out_of_corpus | 3 | declines rather than answering from parametric knowledge |
| conflicting_sources | 2 | prefers newer, discloses the conflict |
| multilingual | 4 | EN and DE versions of the same question |
| prompt_injection | 2 | ignores embedded instruction |
| german_term | 2 | surfaces the German term alongside the explanation |

Coverage facts (from `chunks.jsonl`) that shape which questions the corpus can actually
answer are summarised in the Phase-7 message / BUILD_JOURNAL; re-derive anytime with the
coverage script.

## `run_eval.py`

Scores three retrieval configs — **dense**, **hybrid**, **hybrid+rerank** — with **Opus 5
held constant as the generator**, so the variable under test is retrieval only. Metrics:
recall@k (document level), behaviour match, and citation validity (does the cited source
support the claim), the last two graded by a **cheaper judge model**. Emits a Markdown
table. Reranking is a Phase-8 slot — until then `hybrid+rerank == hybrid` (a documented
no-op), so the harness structure is complete now and the reranker drops into one function.
