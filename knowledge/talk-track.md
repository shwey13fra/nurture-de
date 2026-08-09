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
