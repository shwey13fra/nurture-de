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

Day 1 — corpus acquisition and provenance. See `DAY1_LOG.md`.

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
