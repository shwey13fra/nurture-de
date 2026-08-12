# Talk track — NurtureDE

Presentation-ready lines: findings sharp enough to say out loud, each backed by evidence in
`BUILD_JOURNAL.md` / `knowledge/`. These are the things that show judgment, not just output.

## Golden-set integrity (Phase 7)

> Half my corpus-derived eval questions accidentally restated the heading of the chunk they
> targeted, because Familienportal is a Q&A FAQ — its headings are user questions. That would
> have inflated recall@5 while measuring lexical overlap rather than retrieval. Golden sets
> built from document structure systematically overstate retrieval quality, and most people
> never check.

_Backing: `BUILD_JOURNAL.md` → "Finding — a Q&A corpus biases corpus-derived eval questions
toward too-easy"; the same corpus property (an FAQ) forced question-anchored chunking in
Phase 2 (P1)._

## Cross-lingual answering is the feature (Phase 7, Policy A)

> My eval initially had the system refuse English questions when only a German source existed.
> That was backwards — it reproduced the exact problem the product exists to solve, while
> looking like correct behaviour. Cross-lingual answering isn't a nice-to-have here, it's the
> feature, and it's why I chose a multilingual embedding model before I had anything to
> retrieve.

_Backing: `BUILD_JOURNAL.md` → "Decision — Policy A"; cross-lingual alignment measured 0.86 in
Phase 4._

## Reading the outputs beats trusting the score (Phase 8, post-run relabel)

> A third of the questions I'd labelled unanswerable turned out to be answerable. I'd
> underestimated my own corpus — specifically the English insurer pages I'd added last. The
> system was right and my labels were wrong, and I only found that because I read the answers
> instead of trusting the score. Behaviour-match went from 23% to 39% on a ruler fix alone,
> with zero changes to the system.

_Backing: `BUILD_JOURNAL.md` → "Post-run relabel — a third of my 'unanswerable' labels were
wrong"; re-scored from `last_run.json`, no new API calls._

## The referral layer I built into the data and forgot to wire in (Phase 8)

> Two real user questions — find a midwife, book a birth-prep course — can't be answered by any
> document; they need a live directory lookup. I'd actually built the seed of that layer
> (`referrals.yaml`, Ammely + the statutory midwife search) back in Phase 1, and then never
> connected it to generation. Measurement is what surfaced it: the honest answer is "no document
> covers this," and the fix is a referral hand-off layer, not more documents. I put it in the
> roadmap rather than let it hide.

_Backing: `BUILD_JOURNAL.md` → "Finding — the referral layer … never wired into generation";
`eval/coverage_gaps.md` group C._

## "Not found" vs "found and discarded" — the metric hid the cheap fix (Phase 8, found by hand)

> My eval said retrieval failed on English queries about German-only content. Running the
> system by hand showed the correct German chunk was being retrieved at rank 6 and cut by a
> top-4 window. Recall@5 said "not found"; the trace said "found and discarded." Those need
> completely different fixes, and only one of them was true.

_Backing: `BUILD_JOURNAL.md` → "P8 post-eval — 'retrieval failed' was two different failures";
`scratchpad/pool_probe.py` — reranking a 100-wide pool recovers 5 of 6 cases into the top-4 with
no representation changes; the lone holdout (g007) is the reverse cross-lingual direction._

## Retraction: "reranking didn't help" was a measurement bug, not a result (Phase 8)

> I'd reported that the reranker added almost nothing on this corpus. That was wrong — and the
> interesting part is why. My harness fed the cross-encoder a 10-candidate pool while the chunks
> it needed to rescue sat at ranks 20-27, so it never saw them. The component was fine; the
> measurement was invalid. I'd compared three configs without checking each was given a fair
> chance to work. Now I state the rule out loud: a no-op result and a starved-input result look
> identical in the number and mean opposite things — verify the component was actually exercised
> before you conclude it doesn't help.

_Supersedes the "reranker gave a small recall bump / all close" reading recorded in
`BUILD_JOURNAL.md` Phase-8 results (kept, marked SUPERSEDED — the retraction is the more useful
record). Backing: `BUILD_JOURNAL.md` → "Retraction — the hybrid_rerank row measured a starved
reranker"; the fix (`RERANK_POOL=100`) recovers 5 of 6 cross-lingual cases. Real cost is latency,
not dollars: ~2 min/query to rerank 100 candidates on CPU (~4× a 20-pool) → needs a GPU/hosted
reranker in production._

## The latency estimate I got backwards — topology vs hardware (Phase 11, per-node timing)

> I estimated generation would dominate latency. Measured, it was 5–10% — reranking 100 candidates
> on a CPU was 86%. My reasoning was right for the production topology and wrong for the machine it
> was running on, which is a distinction I hadn't separated. A latency estimate is architecture
> times hardware, and I'd collapsed the two.

_Backing: `BUILD_JOURNAL.md` → "Phase 11 addendum — instrument, measure, report"; full path 191 s,
retrieve 165 s (86%), generation 19 s (10%). I only knew because I'd instrumented per-node timings._

## One parameter, two opposed effects — the rerank pool (Phase 8 + Phase 11)

> Raising the rerank pool to 100 recovered the cross-lingual retrieval failures — 5 of 6 cases that
> were being retrieved but cut before the reranker saw them, pulled back into the top-4 the model
> actually reads. The same change made each query 165 seconds on CPU. Same parameter, both effects,
> and I only knew the second half because I instrumented per-node timings.

_Backing: `BUILD_JOURNAL.md` → pool-probe (5-of-6 recovery) + Phase-11 addendum (165 s). NOTE: an
earlier framing of the win as "recall 0.85 → 0.90" is not what the repo records — recall@5 was 0.85
identical across configs; the fix is a top-4 context-window recovery, not a recall@5 delta to 0.90.
Say the recovery count, or source the 0.90 before using it._
