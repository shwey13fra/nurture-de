# Session Journal — 2026-08-05 (Day 3: Metadata annotation of chunks)

## Where we stopped (resume here)
**Phase 3 metadata applied.** All 201 chunks in `data/chunks.jsonl` now carry
`topic`, `subtopic`, `user_type`, `insurance_type` (0 nulls). Applied by
`src/annotate.py` (deterministic, idempotent, re-runnable with `--write`).
Next action: reviewer spot-check of the override tables, then embedding + index.

    py src/annotate.py            # dry-run: prints all reports, writes nothing
    py src/annotate.py --write    # regenerates the four fields in chunks.jsonl

## PROVENANCE / HONESTY NOTE — the reviewed proposal was not recoverable
The reviewer's message was a **review response** approving a metadata proposal
"as proposed" with five modifications, and asked to spot-check "the 19 user_type
overrides" and "the 3-4 topic overrides." That proposal was produced in a prior
session that was **never journaled to disk**, and this session booted cold.
Verified gone: no taxonomy/proposal file in repo, empty `git stash`, all four
fields null in `chunks.jsonl`, journals cover Phases 1-2 only.

Decision: **reconstruct** the taxonomy from the corpus + the five decisions,
apply, and **flag the reconstructed baseline + re-derived override lists
explicitly** rather than fabricate "the 19 / the 3-4" and present invented data
as the reviewed lists. Fabricating provenance in a provenance project is the
exact failure mode the corpus exists to prevent ("tag what the source says").
Consequence to expect: my re-derived counts need NOT match the proposal's
stated numbers — see divergences below. Those are the numbers to verify.

## What was applied (reconstructed taxonomy)
- **topic** (10 values): default by `source_id`; 4 chunk-level overrides.
- **subtopic** (8 values): keyword rules on the folded heading, ordered so
  `special-circumstances` wins first (decision 5).
- **user_type** (6): default `employee` for employment-linked sources
  (mutterschutz, mutterschaftsleistungen, elternzeit, tk_maternity_pay[_apply]),
  `any` elsewhere; 16 persona overrides.
- **insurance_type** (5): default `any`; 11 overrides.

## Divergences from the proposal's stated numbers (reviewer to arbitrate)
- **user_type overrides: 16 chunks / 10 sections**, not 19. I found 16
  defensibly persona-specific sections. The missing ~3 are most likely
  edge-employment cases the proposal may have counted as personas — `geringfügig
  beschäftigt (Minijob)`, `gekündigt während der Schwangerschaft`, `befristeter
  Vertrag endet` — or a **second Beamtin section**. I found only ONE dedicated
  Beamtin section (`fam_mutterschutz`), though the reviewer described "two."
  The `fam_elterngeld_antrag` Nachweise chunk has a Beamtin/Soldatin subsection
  but is multi-persona, so I left it at default (tagging it civil-servant would
  wrongly exclude employees). Point me at the intended second section.
- **topic overrides: 4** (matches "3-4"): tk_maternity_pay Mutterschutzfrist →
  maternity-protection (reviewer-named anchor); fam_mutterschutz "befristete
  Stelle endet" → maternity-benefits; tk_maternity_benefits on-call-midwifery →
  birth-preparation and postnatal-care → postnatal-care.
- **details = 70, NOT ~25.** Decision 5 said: if details stays above ~25 after
  the split, TELL you rather than guess again. Telling you. Root cause: the
  functional subtopic axis (definition/eligibility/amount/duration/application/
  protections) was shaped around the *benefit* topics; the care/prep/
  registration topics (prenatal check-ups, midwife tasks, birthing class,
  Wochenbett, Standesamt) don't fit it and fall through to `details`. This is
  the weakest part of the reconstruction — I had the least signal for subtopic
  (only `details` and `special-circumstances` were named). Options for you:
  (a) a `care-information` / `logistics` subtopic for the care topics; (b) make
  subtopic topic-relative; (c) accept a large details for non-benefit topics.
  Not guessing further per your instruction.

## Flags (as requested)
- `<3`: topic `parental-leave` (1), topic `child-benefits` (1),
  user_type `civil-servant` (1), insurance `private` (1), insurance `none` (1).
  - `parental-leave`/`child-benefits` are one-chunk hub/teaser stubs
    (`fam_elternzeit`, `fam_kindergeld`) — Phase-2 flagged these as link-list
    hubs. Recommend folding both into `family-benefits-overview` OR dropping the
    hub stubs from the corpus; your call.
  - `private` and `none` are **intentionally retained despite <3** (decision 3:
    keep in vocabulary for future precision).
  - `civil-servant` at 1 is the deliberate decision-1 call (below).
- `>40%`: user_type `any` (58%), insurance `any` (94%). Both are the "no filter
  applies" bucket — inherently large and CORRECT (absence of a persona/insurance
  constraint), unlike a *topic* value being >40%. Not a discrimination defect.

## THE CONTRAST THE REVIEWER ASKED ME TO RECORD — Beamtin split vs Schülerin collapse
Same governing principle ("a value earns its place if it changes what should be
retrieved"), opposite outcomes, and the difference is the whole point:

- **Beamtin → SPLIT into its own `civil-servant` value**, even at ~1-2 sections.
  Justification is *cost of being wrong*, not volume. Civil servants sit under a
  distinct legal regime (their own Mutterschutzverordnung, Länder-specific). A
  civil servant handed the employee rules gets substantively WRONG information
  about her own protections. Collapsing her into `employee` would make the
  filter actively mislead — the exact harm filtering exists to prevent. A thin
  value that prevents a wrong answer earns its place.

- **Schülerin → COLLAPSED into `student`.** Justification is *overlap +
  out-of-scope*. Pupils' practical guidance overlaps heavily with students', and
  pupils are far outside the assistant's persona scope (employed, publicly
  insured). A separate `pupil` value would split retrieval without changing the
  answer. Collapsing costs a *missed* nuance (a known, logged imprecision), not
  a *wrong* answer.

The asymmetry: **splitting is justified by the cost of a wrong answer;
collapsing is justified when the only cost is a missed nuance and the case is
out of scope.** Two sections is "thin" in both cases — volume did not decide
either call; consequence did. This is what makes the vocabulary *reasoned*
rather than *transcribed*: the same small count produced opposite decisions
because the retrieval consequences differed.

Known, accepted imprecisions (logged, not accidental):
- `Schülerin` and `Auszubildende` fold into `student`. Auszubildende are in fact
  employed + statutorily insured (closer to `employee`), but the source groups
  "Schülerin, Auszubildende oder Studentin" in one heading — so per decision 3's
  general rule ("tag what the source says, not what I wish it had said") the
  chunk is tagged `student`.

## RESOLUTIONS (reviewer, same session)
- **user_type overrides: 16 ACCEPTED as final.** Reviewer: the "19" was a number
  from my own lost proposal echoed back, never independently approved — "16
  derived deterministically from actual chunks beats 19 from a lost document."
  No hunt for the missing three. Second Beamtin section: leave the multi-persona
  `fam_elterngeld_antrag` chunk at default (tagging it civil-servant would
  wrongly exclude employees — the exact failure the field prevents).
- **details resolved via option (a).** Added two GLOBAL subtopic values,
  keyword-gated to CARE_TOPICS (prenatal/postnatal/birth-preparation/birth-
  registration) so care keywords can't leak into benefit/overview chunks:
    - `care-procedure` — what an appointment/class/service involves (fallback
      within care topics)  → 27 chunks
    - `logistics` — where to go / who to contact / what to bring / deadlines
      → 13 chunks
  Rejected (b) topic-relative vocab (breaks the cross-topic consistency that
  makes a filter usable) and (c) accept-large-details (35% catch-all = axis not
  working). **details: 70 → 31.** In the 30-40 gray zone; treated as done (NOT
  adding a third value, per instruction). The residual 31 are ALL benefit/
  overview/protection topics — legitimate "other benefit info" (taxation,
  insurance-during-benefit, planning, hub overviews, general scope), zero care
  leakage in or out. One acceptable edge: tk_maternity_pay_apply "insure your
  child free of charge" is logistics-flavored but sits under maternity-benefits
  (non-care topic), so it stays in details; not worth a rule.

## TWO REFRAMES (reviewer corrections to my heuristics)
1. **A <3 value is not automatically a taxonomy defect — it can mean the CORPUS
   is thin.** `parental-leave` (1) and `child-benefits` (1) are single-chunk hub
   stubs, but Elternzeit and Kindergeld are things a pregnant expat genuinely
   asks about. **KEEP the topic values**; the thinness is a **corpus coverage
   gap** (roadmap item), not a value to fold away. My original "fold/drop"
   recommendation was wrong: it treated a content gap as a vocabulary error.
   (Not fetching more sources now.)
2. **insurance_type=any at 94% is honest but has an EVAL consequence.** Only 11
   chunks carry a real insurance value. The golden set must put filtering weight
   on `user_type` (84 chunks with real, i.e. non-`any`, values) rather than
   `insurance_type`, or the eval will test the same 11 insurance chunks over and
   over. Record this as a golden-set design constraint for Day-4.

## Open / carried forward
- Embedding + vector index (Phase 3 next).
- `parental-leave` / `child-benefits`: corpus-coverage roadmap item (fetch
  Elternzeit/Kindergeld detail pages later), NOT a taxonomy fix.
- Golden-set constraint: weight filtering evals on user_type, not insurance_type.
