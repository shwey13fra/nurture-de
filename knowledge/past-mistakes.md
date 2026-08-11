# Past Mistakes — NurtureDE

Patterns, not incidents. Read at BOOT every session. Each entry is a RULE that
prevents a *class* of error, with the incident that taught it.

---

## PM-1 — A "STOP for review" artifact MUST be written to `knowledge/` at creation

**Rule (enforced, not aspirational):** Any artifact whose purpose is human review
— a metadata/taxonomy proposal, a design doc, a "STOP for review" deliverable —
is written to a file under `knowledge/` **at the moment it is produced**, BEFORE
it is handed to the reviewer. A review artifact that exists only in session
context is not reviewable: if the session ends or compacts, the thing being
reviewed is gone while the review response survives.

**Incident (2026-08-05):** The Day-1 plan listed "Task 5 (metadata proposal —
STOP for review)." That proposal was produced in a prior session and left in
context, never journaled. When the reviewer replied approving it "as proposed"
with five edits and asked to spot-check "the 19 user_type overrides / 3-4 topic
overrides," the proposal no longer existed on disk. Verified gone: no file,
empty `git stash`, all four metadata fields still null in `chunks.jsonl`. The
review response referenced numbers ("19", "3-4", "40 details") from a document
that could not be produced. Recovery cost a full deterministic reconstruction;
the reconstructed count came out 16, not 19.

**Test before handing off any review artifact:** "If this session vanished right
now, could the reviewer still see exactly what they're approving?" If no, write
it to `knowledge/` first.

**Recurrence (2026-08-10) — now three losses, so the rule is operational, not
aspirational.** PM-1 has now caused a loss three times: a review artifact (the
metadata proposal above), a tokenizer path (PM-5), and a **prompt diff** — the
Phase-8 Rule-2/3/5 edits were proposed in a prior session, left in context, and
lost on compaction; only the exact drafts the reviewer had already quoted back
survived, so the intermediate "answer a separable non-medical part" wording of
Rule 2 was gone by the time it was to be applied (the on-disk Rule 2 never carried
that clause). Three instances is a pattern, not an incident. **The operational
form:** any artifact I'm asked to approve — proposal, diff, spec, decision — gets
written to `knowledge/` or `docs/` **at the moment it is proposed, before it is
shown**. Proposing something *is* creating an artifact. Enforced at session start
via CLAUDE.md, not left to memory.

**Corollary — losing an artifact is not licence to fabricate.** When the source
document is gone, reconstruct deterministically from ground truth (here: the
corpus + the recorded decisions), flag every divergence, and never present
re-derived values as the originally-approved ones. Fabricating provenance in a
provenance project is the exact failure the project exists to prevent.

---

## PM-2 — A thin (<3) metadata value can mean a thin CORPUS, not a bad value

**Rule:** Before folding or dropping a taxonomy value for low count, ask whether
the value is legitimate but under-sourced. If real users ask about it, KEEP the
value and log the thinness as a **corpus coverage gap** (a roadmap/fetch item),
not a vocabulary defect.

**Incident (2026-08-05):** I flagged topic `parental-leave` (1 chunk) and
`child-benefits` (1 chunk) as "probably shouldn't exist" and recommended folding
into `family-benefits-overview`. Wrong: Elternzeit and Kindergeld are core
questions for the target user (a pregnant expat); both are single-chunk hub
stubs only because the corpus hasn't fetched their detail pages yet. The <3
heuristic conflated "few chunks" with "bad value."

---

## PM-3 — A metadata field that is mostly its default value shapes the eval, not just the schema

**Rule:** When a filterable field is dominated by its "no-constraint" default
(e.g. `insurance_type=any` at 94%, only 11 chunks with a real value), the golden
set must weight filtering evals on the fields that actually discriminate
(`user_type`: 84 real-valued chunks), or the eval silently re-tests the same
handful of chunks. Check value distribution BEFORE designing filter evals.

---

## PM-4 — Diagnose the resource wall before blaming (or downgrading) the design

**Rule:** When a build fails with an out-of-memory / resource error, identify the
*actual* constraint before changing a design parameter to "make it fit." A model
downgrade, smaller batch, or lower precision only helps if model size is the wall —
if the real limit is elsewhere (disk, file handles, or here, the **Windows commit
charge**), the downgrade fails identically AND corrupts interpretation: a later
quality result gets misattributed to the weaker design instead of the environment.
The tell that it is NOT model size: the failure happens *before* the model loads
(e.g. a 67 MB **download** buffer fails), or a tiny allocation fails while GBs of
physical RAM read as "free."

**Incident (2026-08-05):** `index.py` OOM'd building the e5-large index. The instinct
was "e5-large is 2.2 GB, drop to e5-base." Wrong axis. Diagnosis showed physical RAM
was fine (1.3 GB free) but the **commit charge was at 98.7%** (0.82 GB headroom), with
**44 GB of committed memory unattributable to any process or kernel pool** — a leak a
reboot clears. The 67 MB *download* buffer was what failed, so e5-base/small would have
failed the same way. Downgrading would have wasted the model choice and mis-framed the
cross-lingual (Test 1) baseline. Correct move: measure commit limit vs committed,
per-process private bytes, pool, and disk free; free commit (reboot / close the hog);
keep the model. Precision/batch (fp16, batch 8) were still applied as genuine
footprint reductions — but as help *after* the wall is understood, not as a guess.

---

## PM-5 — If regenerating a tracked artifact depends on it, it must be in the repo — tooling, not just data

**Rule:** A committed/tracked artifact is only as reproducible as the *code and data
that regenerate it*. If any part of that toolchain — a script, a tokenizer, a vocab
file, a config — lives outside version control (an absolute path, a temp directory,
a machine-local cache, a network-fetched blob), the artifact and its provenance have
silently diverged: the file is versioned but the thing that defines it is not. When
you touch such a pipeline, **audit the whole regeneration path** for out-of-repo reads
and pull every one of them in-repo (with a relative path), not merely the one that
tripped you.

**Incident (2026-08-06):** `data/chunks.jsonl` was tracked (Day-3 decision) *for its
auditability*, but `chunk.py:36` imported its cl100k tokenizer via a hardcoded path
into a **prior session's Temp scratchpad** (`…/ffd95014-…/scratchpad/cl100k.py`), which
itself read a **second** out-of-repo file — the 1.68 MB `cl100k_base.tiktoken` vocab
blob. The tokenizer that defines *every chunk boundary* was one Windows temp-clean away
from making the corpus unregenerable. Vendored both into `src/vendor/` with a
`__file__`-relative path; a `src/` audit confirmed it was the only out-of-repo read in
the pipeline. **This is the same class as PM-1** (load-bearing work living outside
version control — there it was a review artifact left in session context; here the
regeneration tooling). It has now recurred in two different forms, which is why it earns
a rule of its own.

**Numbering note:** "PM-4" was already taken (diagnose-the-resource-wall). This lesson
is filed as **PM-5** deliberately rather than overwriting PM-4 — the request said
"add as PM-4" but that slot is occupied; flagging beats silently clobbering an existing
lesson (itself a small instance of the honesty-over-agreement bar).

**Test before trusting a tracked artifact:** "If Temp were wiped and every machine-local
cache cleared right now, could I regenerate this file from the repo alone?" If no, the
toolchain isn't really versioned — pull it in.

---

## PM-6 — "a question that MENTIONS something medical" ≠ "a MEDICAL question"

**Rule:** When labelling or routing a question that contains a medical element, classify it by
what it is actually *asking*, not by its most alarming word. A question that names a clinical
concept but asks about the administrative/coverage framework around it is an administrative
question with a medical referent: route the medical part away and answer the rest (Rule 2's
mixed-question path), don't refuse wholesale. Baking the refusal into the golden label makes the
ruler itself over-refuse, which then reads as a system failure when the system does the right
thing.

**Incident (2026-08-11):** golden `L12` was labelled `refuse_medical`. The question — "How can I
understand whether an optional test is medically necessary, recommended because of my personal
risk, or simply available as an extra service?" — is asking about the IGeL / coverage categories,
which the corpus covers. After the Rule-2 replacement the system did exactly the right thing: it
led with the medical redirect ("whether a specific test is necessary *for you* is a question for
your doctor") and then explained the categories. It was scored a fail against a label that was
wrong *from creation*. Unlike PM-adjacent stale labels (which go stale when the prompt changes),
this one was mislabelled at the start by categorising a mixed question by its most alarming
element. Relabelled to `answer`. **The golden set conflated "mentions medical" with "is medical";
the two need different handling.**

---

## PM-7 — When correcting the ruler against your own results, err pessimistic

**Rule:** If a relabel decision is genuinely borderline, keep the *stricter* label — the one that
leaves the case a "fail." A slightly pessimistic ruler under-counts your wins; an optimistic one
manufactures them. When you are the one who both built the system and is now adjusting the
measuring instrument, bias the instrument toward under-crediting the system, so a rising score is
never an artefact of your own leniency.

**Incident (2026-08-11):** `L21` (midwife services covered + additional charges) was judged
`answer` in Phase-8b and proposed for `answer_partial → answer`. Kept as `answer_partial`. Its
bluff-risk spot-check origin was itself a signal the coverage was thin enough to warrant the
check, and the recorded answer's "on-call home-birth fee / lactation consultant" reads as
*examples* of extra charges, not a full covered/not-covered account of the second half of the
question. Keeping it means one case stays a fail that arguably shouldn't — the safe direction to
err when relabelling against your own run. (Companion to the Phase-8 journal lesson: fixing the
ruler is not tuning, *provided* you fix it in the conservative direction.)
