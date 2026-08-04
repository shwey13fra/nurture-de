# PHASES — NurtureDE, in plain English

A running, plain-language log of **what we build in each phase, step by step**:
what got done, which files were created and *why*, and what tools/software each
phase needs. Newest phase is added at the bottom as we go. For the terse
day-by-day engineering record see `knowledge/sessions/`; this file is the
human-readable tour.

**What NurtureDE is:** a question-answering assistant that only answers from a
curated set of *official* German sources about pregnancy, maternity protection,
and family benefits — and cites every claim back to the page it came from. Built
for internationals in Germany who can't find (or don't know the German words for)
information that officially exists. It never decides eligibility and never files
applications.

---

## Tools & software (whole project so far)

| Tool | What it's for | Do you need to install it? |
|------|---------------|----------------------------|
| **Python 3.7+** (run as `py` on this machine) | Runs all pipeline scripts | Already installed (3.7.8) |
| **PyYAML** (`import yaml`) | Reads the `sources.yaml` / `referrals.yaml` catalogues | Already installed (6.0) |
| **Python standard library** (`urllib`, `html.parser`, `hashlib`, `argparse`) | Downloading pages, extracting text, hashing, CLI flags — **no extra install** | Built in |
| **Git** | Version control; created *before* any files so the corpus history is tracked from line 1 | Already set up |
| A plain text editor / this session | Hand-authoring the source catalogues (kept human-readable with comments) | — |

Deliberately **no** heavy libraries yet (no bs4/trafilatura, no vector DB). Those
arrive in later phases when we actually need higher-quality text and search. See
`knowledge/decisions.md` for why.

---

## Phase 1 — Corpus acquisition & provenance (Day 1)

**Goal of the phase:** decide *which* official pages we're allowed to use, write
them down with full provenance, and build the tool that downloads them and
fingerprints their content — so later phases retrieve from a trusted, verifiable
set instead of the open web.

### Step 1 — Set up the project skeleton
- **Did:** ran `git init` **first** (before creating any file), then made the
  folder layout and starter docs.
- **Files created & why:**
  - `README.md` — what the project is, plus the "not medical/legal advice" notice.
  - `NOTES.md` — scratchpad for corpus-analysis prose (filled later in the phase).
  - `.gitignore` — keeps downloaded pages and generated data **out** of git
    (`data/raw/`, `data/processed/`, `chroma_db/`, `.venv`, `__pycache__`, `.env`).
  - Empty folders: `data/raw/`, `data/processed/`, `src/tools/`, `eval/`, `tests/`.
- **Why git first:** so the very first version of the source catalogue is tracked;
  nothing about which sources we chose is ever lost.

### Step 2 — Check we're *allowed* to fetch each page (robots.txt)
- **Did:** wrote and ran a checker that reads each website's `robots.txt` (the
  file where sites say what automated tools may access) for all 19 starting URLs.
- **File created & why:** `src/tools/check_robots.py` — automated, repeatable
  permission check, so the "are we allowed?" answer is evidence, not a guess.
- **Result:** all 19 URLs **allowed**. Some sites ask bots to wait 1 second
  between requests; noted so the fetcher can obey.

### Step 3 — Write the catalogue of citable documents
- **Did:** hand-authored the master list of pages we *will* fetch, chunk, and
  cite — 23 entries (the 19 given + 4 gap-fills we researched and you approved).
- **File created & why:** `data/sources.yaml` — the single source of truth for the
  corpus. Each entry records where it's from, who published it (federal / statutory
  insurer / Land), category, language, and cross-links. Written by hand (with
  comments) so a human can audit *why* each source is trusted.
- **Note:** some fields (`content_hash`, `topic`, etc.) are intentionally left
  `null` — they get filled by later phases, so blank ≠ missing.

### Step 4 — Separate "information" from "actions" (referrals)
- **Did:** listed interactive tools (e.g. "find a midwife by postcode") that are
  useful next steps but are **not** things we quote from.
- **File created & why:** `data/referrals.yaml` — action endpoints we *link to*
  but never fetch, chunk, or cite. Keeps live-lookup tools cleanly separate from
  citable text so the assistant never blurs "here's a fact" with "go do this here."

### Step 5 — Build & run the fetcher ✅
- **Did:** wrote the downloader, then ran it (dry-run first, then for real).
- **File created & why:** `src/fetch.py` — for each source it downloads the page to
  `data/raw/{id}.html`, extracts readable text, computes a **SHA-256 hash** of that
  text, and writes the hash + today's date back into `sources.yaml`. Why the hash:
  it's a tamper-/change-detector, so re-runs can tell "this page changed" from
  "unchanged, skip it." It also re-checks robots.txt, waits politely between
  requests, and flags near-empty pages as "suspicious" (likely a JavaScript-only
  page we couldn't read).
- **Result of the run (Day 2):** all **23 pages fetched, 0 failed, 0 suspicious**.
  Created `data/raw/*.html` (23) and `data/processed/*.txt` (23); wrote all 23
  `content_hash` + `last_verified_date` values back into `sources.yaml` (0 nulls
  left). Smallest page was 1,501 text chars — comfortably above the 600-char
  "suspicious" floor, so nothing needs manual capture.

### Things we decided (and deliberately did *not* do) this phase
- **Didn't spoof a browser** to get past `frankfurt.de`, which blocks our honest
  research tool (HTTP 403). A provenance project fetches only what it's permitted
  to fetch as itself. That page was dropped; birth-registration info comes from the
  clean federal Familienportal instead.
- **Didn't ingest `verwaltung.bund.de`** — it's a JavaScript app that returns almost
  no text to a simple download, so it isn't usable as a citable document.
- **Crude text extraction on purpose** (standard library only). Good enough for a
  stable fingerprint now; high-quality extraction is a later-phase concern.

---

## Phase 1b — Clean re-extraction (Day 2)

**Goal:** the Day-1 text was unusable for chunking (all headings flattened,
boilerplate inline). Rebuild clean, structure-preserving text from the cached
raw HTML — no re-downloading.

- **File created & why:** `src/extract.py` — reads `data/raw/*.html`, selects the
  real article per site (different container on each of the 3 sites), deletes
  navigation/cookie/footer chrome, and writes clean **Markdown** with headings,
  lists, and paragraphs intact to `data/processed/{id}.md`. Then it recomputes the
  fingerprint from the *clean* text.
- **New tool:** `beautifulsoup4` (HTML parsing library) — needed because the three
  sites use incompatible page structures and TK uses custom elements; the plain
  standard library couldn't select/clean them reliably.
- **Result:** all 23 pages now clean Markdown with real heading hierarchy.
  Verified end-to-end (heading trees, smallest file, FAQ Q&A, before/after sizes,
  newline+heading check). All 23 fingerprints updated to match the clean text.
- **Found along the way:** `bmas_mutterschutzgesetz` is not the statute — it's a
  ~140-char page that links out to juris GmbH. Flagged as a corpus decision.

---

## ⏯️ Where we restart

**Phases 1 and 1b are complete** — the corpus is downloaded, cleanly extracted to
Markdown, and fingerprinted. The `bmas` stub was re-pointed to the real statute on
gesetze-im-internet.de (`gii_muschg_2018`, `authority_tier: primary-law`); the old
entry is kept as `superseded` for the record. Next:

1. **Chunking** — split the clean `data/processed/*.md` (23 active docs) into
   retrievable passages, using the preserved `##`/`###` headings as boundaries.
   Special cases: hub/index pages (link lists) and the statute §-TOC.
2. **Metadata** — propose `topic / subtopic / user_type / insurance_type` per
   source, then **stop for your review** (can come after chunking).

_Last updated: 2026-08-03, Day 2 — clean extraction (23/23) + statute re-pointed._
