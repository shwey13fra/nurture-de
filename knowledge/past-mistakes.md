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
