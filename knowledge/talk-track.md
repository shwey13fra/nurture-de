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
