# NurtureDE

Source-grounded RAG over official German information about pregnancy, maternity
protection, and family benefits — built for internationals living in Germany who
can't find, or don't know the German terms for, information that officially exists.

> **⚠️ Not medical or legal advice — prototype for portfolio purposes.**
> NurtureDE never determines eligibility and never submits applications. Every
> substantive claim is cited back to an official source. For decisions, consult
> the responsible authority or a qualified professional.

## What it does

- Retrieves answers only from a curated corpus of official German sources
  (federal portals, statutory insurers, Land/municipal authorities).
- Cites every substantive claim back to its source page.
- Surfaces official **action endpoints** (e.g. midwife directories) as next steps,
  clearly separated from citable information.

## Status

Day 1–2 — corpus acquisition, provenance, clean extraction. See `DAY1_LOG.md`
and `PHASES.md`. Next: heading-aware chunking.

## Roadmap

- **Statute text as a supporting-evidence layer.** The corpus answers from
  official *plain-language* sources; primary law (e.g. MuSchG on
  gesetze-im-internet.de) is intentionally out of the user-facing retrieval set —
  its register is wrong for the reader. A later layer may cite specific paragraphs
  as *supporting evidence* beneath a plain-language answer, not as the answer.

## Layout

```
data/sources.yaml     Citable documents (fetched, chunked, retrieved)
data/referrals.yaml   Action endpoints (surfaced, never ingested)
data/raw/             Fetched HTML (git-ignored)
data/processed/       Extracted/chunked text (git-ignored)
src/                  Pipeline code (fetch, chunk, index, retrieve)
eval/                 Evaluation cases
tests/                Tests
```
