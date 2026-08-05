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

Phases 1–3 done — corpus acquisition & provenance, clean extraction, heading-aware
chunking, and deterministic metadata annotation (201 chunks). See `BUILD_JOURNAL.md`
and `PHASES.md`. Next: embedding + hybrid (dense + BM25) vector index.

## Requirements & setup

**Python 3.11+** (floor is 3.10, verified on 3.11.9). The earlier 3.7.8 stack could
not run chromadb, the MCP SDK, or LangGraph — hence the migration in Phase 3b. Torch
is pinned to the **CPU-only** wheel (no GPU on this machine).

```bash
py -3.11 -m venv .venv                 # dedicated venv; leave any 3.7 stack untouched
.venv/Scripts/python -m pip install -r requirements.txt
# (requirements.txt embeds the PyTorch CPU index for the +cpu torch wheel)
```

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
