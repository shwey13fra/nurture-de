# Phase-8 golden-relabel proposal — for review (confirm each case)

**Status:** PROPOSED, not applied. `eval/golden.jsonl` is unchanged until each case below is
confirmed. Written to `knowledge/` at the moment of proposing, per PM-1.

**Why this exists.** In the Phase-8 cycle the *ruler and the system were changed in the same
pass*: a prior session relabelled several golden cases to `answer_partial` (encoding the OLD
prompt's hedging as "expected"), and the Rule 5 edit then told the system to stop hedging when
the documents fully answer. The label and the prompt intent now contradict each other. Three
cases "failed" the Phase-8b run for doing exactly what Rule 5 now asks. This proposal fixes the
ruler's internal contradiction. No system behaviour is being tuned here — only the measuring
instrument is being brought back into sync.

**Evidence base:** `eval/last_run_phase8b.json` (the run these labels were scored against).
Each case cites the *Phase-8b* judged behaviour and answer, not any earlier run.

**Re-scoring is free.** Once confirmed, `pass` is recomputed from the already-recorded `judged`
values against the new labels — no new API calls.

---

## Category A — stale `answer_partial`, correct to `answer`  (L09, L15, L21)

Common thread: **the Phase-8b judge labelled all three `answer` — the system gave a complete,
fully-cited answer with no manufactured gap.** They score as failures only because the golden
label still says `answer_partial`, which encodes the pre-Rule-5 hedge. Rule 5 now says: "A
complete answer needs no disclaimer; adding one makes a correct answer read as partial." The
label is the thing that is now wrong.

### A1 · L09 → `answer`
- **Q:** "Which pregnancy check-ups, ultrasound scans and laboratory tests are covered by
  statutory health insurance such as TK?"
- **Phase-8b:** judged `answer`, recall **1.0**, citations **15/15**.
- **What it did:** listed the full covered standard package (blood-pressure/blood tests incl.
  gestational-diabetes screening, ultrasound, HIV/hep-B/syphilis/chlamydia screening, Rhesus),
  the TK-specific scan timing, *and* what is not covered (toxoplasmosis/IGeL). That is a
  complete answer to "which are covered."
- **Reasoning:** the original `answer_partial` worry was "no per-test coverage breakdown," but
  the standard Vorsorge package *is* the covered set and the answer enumerates it. No residual
  gap was named by the system. **Stale label → `answer`.**

### A2 · L15 → `answer`
- **Q:** "Under what circumstances will health insurance cover additional prenatal tests?"
- **Phase-8b:** judged `answer`, citations **6/6**. (`expected_sources` is empty → recall n/a;
  a leftover from L15's earlier relabel *out_of_corpus → answer_partial*.)
- **What it did:** stated the three covering circumstances completely (well-founded suspicion of
  disease / high-risk pregnancy / abnormalities to clarify), plus the IGeL fallback. The only
  caveat is a one-line *translation* note, not a gap.
- **Reasoning:** the question asks about the circumstances; the corpus answers them in full.
  L15 has already been walked once (from over-pessimistic `out_of_corpus`); the next correct
  step under Rule 5 is **`answer`.**

### A3 · L21 → `answer`
- **Q:** "Which midwife services are covered by health insurance, and are there any additional
  charges?"
- **Phase-8b:** judged `answer`, citations **11/11**. (`expected_sources` empty → recall n/a.)
- **What it did — the key point:** the earlier run (in `relabel_candidates.md`) *hedged* on the
  "additional charges" half. **The Phase-8b run actually answers it from the corpus** — it names
  what costs extra: a midwife's on-call fee for a home birth, and lactation consultants. Both
  halves of the question are answered.
- **Reasoning:** the only remaining caveat is the statutory-vs-private boundary (one line, a
  correct scope note, not a manufactured gap). With the charges question now answered, the
  `answer_partial` label no longer describes the behaviour. **Stale label → `answer`.**
- *Honesty flag:* L21 is a `SPOTCHECK_ID` (bluff-risk `out_of_corpus` origin). It is the least
  clear-cut of the three — if you read the phase-8b answer and judge that the extra-charges
  coverage is thin enough that the scope note is load-bearing, this one could stay
  `answer_partial`. My read of the recorded answer is that both halves are genuinely covered, so
  I recommend `answer`, but this is the one to eyeball.

---

## Category B — optimistic `answer`, correct to `answer_partial` + log PM-2  (c06, c08)

Common thread: **recall is 1.0 — retrieval is not the problem.** The corpus genuinely lacks the
per-Bundesland / per-situation detail these questions imply, so the system correctly reports the
rule that *applies* and names the authority that holds the rest. That is textbook
`answer_partial`; the golden `answer` label was optimistic about corpus depth. These are
**coverage gaps (PM-2 class)**, not prompt or retrieval defects — log a fetch item, keep the
value.

### B1 · c06 → `answer_partial`  (+ PM-2: student financial-support detail)
- **Q (de):** "Ich studiere und bin schwanger — gilt der Mutterschutz auch für mich?"
- **Phase-8b:** judged `answer_partial`, recall **1.0**, citations **6/6**.
- **What it did:** fully answered that Mutterschutz applies to students (absence rights,
  night/Sunday rules, opt-in to attend), then correctly hedged on money — "ohne Nebenjob gibt
  es kein Mutterschaftsgeld, unter Umständen aber besondere Unterstützung" — without naming the
  specific programs, because the corpus doesn't contain them.
- **Reasoning:** the hedge is on a genuinely-absent detail (which support programs, eligibility
  for students without Erwerbseinkommen). `answer_partial` is the *correct* behaviour; the label
  is wrong. **`answer` → `answer_partial`.** Log corpus gap: *student maternity financial
  support (Studentinnen ohne Nebenerwerb).*

### B2 · c08 → `answer_partial`  (+ PM-2: civil-servant per-Bundesland Mutterschutz detail)
- **Q (de):** "Ich bin verbeamtet und erwarte ein Kind — welcher Mutterschutz gilt für mich?"
- **Phase-8b:** judged `answer_partial`, recall **1.0**, citations **6/6**.
- **What it did:** correctly identified that Beamtinnen fall under a separate regime (Bund vs
  Land Mutterschutzverordnung), *explicitly stated* the substantive per-Bundesland detail is not
  in the sources, and pointed to the Personalstelle as the authority.
- **Reasoning:** the corpus genuinely lacks per-Bundesland civil-servant Schutzfristen/
  Leistungen/Beschäftigungsverbote. Naming that gap and the deciding authority is exactly
  `answer_partial`. **`answer` → `answer_partial`.** Log corpus gap: *civil-servant
  (verbeamtet) per-Bundesland Mutterschutz detail.*

---

## What this does to the Phase-8b score (projected, re-scored from existing records)

If all five are confirmed, five recorded runs flip FAIL→pass with **no new generation**:
L09, L15, L21, c06, c08. (Exact recomputed behaviour-match % will be printed by the re-score
step against `last_run_phase8b.json`.)

## Confirmation checklist

- [ ] A1 · L09 → `answer`
- [ ] A2 · L15 → `answer`
- [ ] A3 · L21 → `answer`  *(borderline; see honesty flag)*
- [ ] B1 · c06 → `answer_partial`  + PM-2 student-finance gap
- [ ] B2 · c08 → `answer_partial`  + PM-2 civil-servant gap
