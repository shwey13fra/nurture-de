# DAY 1 LOG — Corpus Acquisition & Provenance

**Date:** 2026-08-03 (fetch executed 2026-08-03, Day 2 morning)
**Objective:** Convert a list of official German information pages into a small,
trusted, fingerprinted corpus with full provenance — the foundation the retrieval
and answer layers will stand on.

> Companion docs: `PHASES.md` (plain-English tour), `knowledge/decisions.md`
> (decision log), `knowledge/sessions/2026-08-03-day1.md` (session journal).

---

## Objective in one line
Answer three questions defensibly for every page: *Are we allowed to use it?
What exactly did it say, and when? How do we prove that later?*

---

## What was built

| Artifact | Purpose |
|----------|---------|
| Repo scaffold (`git init` first) | README, NOTES, `.gitignore`, `data/{raw,processed}`, `src/tools`, `eval`, `tests` |
| `src/tools/check_robots.py` | One-time permission audit of every candidate URL against its `robots.txt` |
| `data/sources.yaml` | Hand-authored catalogue of **citable documents** (23 entries), the corpus source of truth |
| `data/referrals.yaml` | Catalogue of **action endpoints** (interactive tools) — linked, never fetched/cited |
| `src/fetch.py` | The pipeline: download → extract text → SHA-256 fingerprint → write hash+date back into `sources.yaml` |

---

## Key decisions (rationale)

1. **Dependency-free extraction.** Used stdlib `html.parser`, not bs4/trafilatura.
   Good enough for a *stable content hash* and a size heuristic today; high-quality
   boilerplate stripping is deferred to Day 2. Trade-off: crude text now, zero
   install, fully reproducible.

2. **Hash the extracted TEXT, not the raw HTML.** Raw HTML churns every fetch (ads,
   tokens, timestamps). Hashing visible text yields a fingerprint that changes only
   when the *information* changes — enabling "unchanged → skip re-processing."

3. **Comment-safe writeback.** Hashes/dates are written via targeted in-place line
   edits keyed on `id` (`set_fields_for_id`), never `yaml.dump`, so the hand-written
   explanatory comments in `sources.yaml` survive.

4. **Do not bypass access controls.** `frankfurt.de` returns HTTP 403 to our honest
   research User-Agent though its robots.txt permits us. We did **not** spoof a
   browser UA to evade it — a provenance project fetches only what a source permits
   it to fetch *as itself*. Page dropped; birth-registration sourced from the clean
   federal Familienportal instead.

5. **Citable documents vs. action endpoints.** Interactive directories (e.g. midwife
   search by postcode) live in `referrals.yaml` and are never ingested — their value
   is the live lookup, not quotable prose. Keeps "here is a cited fact" cleanly
   separate from "go do this action here."

6. **`pairs_with` cross-links** federal rule pages with insurer process pages on the
   same topic, to stage a Day-3 eval: does the system cite the correct *register*
   for the question asked?

---

## Fetch run results (2026-08-03)

```
py src/fetch.py --dry-run   → 23 selected, 0 disallowed, wrote nothing
py src/fetch.py             → fetched=23  failed=0  suspicious=0  hash-changed=23
```

- **23/23 pages fetched**, politely (≥2s between requests, robots re-checked per URL).
- Created `data/raw/*.html` (23) and `data/processed/*.txt` (23).
- Wrote all 23 `content_hash` + `last_verified_date` back into `sources.yaml`
  (**0 nulls remaining**).
- Text sizes ranged **1,501 → 78,871 chars**; smallest cleared the 600-char
  "suspicious" floor, so **nothing requires manual capture**.

---

## Mechanisms (how it works)

- **Fetching:** HTTP GET via stdlib `urllib` with an honest identifying User-Agent
  and a 25s timeout. Bytes decoded using charset from HTTP header → `<meta>` →
  utf-8 → latin-1 (German umlauts must survive).
- **robots.txt:** each domain's `robots.txt` fetched once and cached; parsed by
  `RobotFileParser`; `can_fetch()` gates every download, `crawl_delay()` is honored.
  A disallowed URL is skipped, never fetched.
- **Fingerprint:** SHA-256 of the extracted visible text = a dated, tamper-evident
  provenance receipt per source.
- **Idempotent/incremental:** re-runs skip pages that already have a file + hash;
  `--update`, `--force`, `--only`, `--remove` flags support targeted refreshes.

---

## Day 2 — Clean re-extraction (`src/extract.py`)

The Day-1 extractor (stdlib `html.parser`) collapsed all whitespace, destroying
every heading and leaving boilerplate inline — unusable for chunking. Replaced
with a beautifulsoup4-based pass that runs **against the cached `data/raw/`**
(no re-fetch) and writes clean Markdown to `data/processed/{id}.md`.

- **New dependency (approved):** `beautifulsoup4` (html.parser backend, no lxml).
  Chosen over stdlib (needs a queryable tree for per-domain selectors + subtree
  deletion) and over trafilatura (heuristic/non-deterministic; can't target TK's
  custom elements). Explicit selectors = auditable, which a provenance project needs.
- **Per-domain content selectors:** `familienportal.de → <main id="main">`,
  `gesund.bund.de → <article>`, `tk.de → <main id="tkde-maincontent">`,
  `bmas.de → <article>/<main>/<body>` fallback.
- **Boilerplate stripped** for all four domain families (cookie/Matomo/nav header,
  footers, feedback/teaser/nav-menu widgets) — not just the ≥5-doc ones.
- **Bugs found & fixed during validation** (prediction ≠ reality each time):
  1. gesund `<h2>`s nest inside `<button>` accordions, and the title `<h1>` inside
     `<header>` — blanket-deleting those tags destroyed the headings. Fix: *unwrap*
     buttons/headers (keep contents, drop wrapper).
  2. TK body text sits bare inside `<tkds-text>` (no `<p>`). Fix: emit text from
     any container with no block-level descendants.
  3. gesund section-nav leaked as a list (`<div class="p-lifepath__nav">`, not a
     `<nav>` tag) and a bookmark/cookie toolbar (`article-header__buttons`) leaked
     after the header unwrap. Fix: class-based drops (`__nav`, `header__buttons`).
- **TK heading levels preserved:** `<tkds-headline>` carries an explicit `level`
  attribute (1/2/3) — read directly, so TK keeps h1→h2→h3 nesting (verified).

### ⚠️ content_hash intentionally recomputed — NOT corruption
All 23 `content_hash` values in `sources.yaml` **changed** in this pass and now
fingerprint the **clean Markdown**, not the old boilerplate-laden text. This is
correct and expected. `last_verified_date` is unchanged (the live source was not
re-fetched, only re-extracted from cache).

### ⚠️→✅ Corpus finding & resolution — the "statute" was a referral stub
Clean extraction of the BMAS page's `<article>` yielded only **~140 chars**: a
title and "Der Gesetzestext auf den Seiten der juris GmbH." The BMAS page does
**not** contain the statute — it links out to juris GmbH. The ~12k chars the
Day-1 fetch captured were the BMAS mega-menu/footer, not law.

**A URL that *looked* authoritative (a federal ministry, `/Gesetze/…`) was in
fact a 140-char pointer.** Lesson operationalized (below).

**Resolved — re-pointed to primary law:**
- New source `gii_muschg_2018` → `https://www.gesetze-im-internet.de/muschg_2018/`
  (the official federal law portal), **single consolidated URL only — individual
  `§` subpages are NOT crawled**. robots.txt verified allow-all (2026-08-03).
- New `authority_tier: primary-law`, documented to rank **above** `federal`
  plain-language sources — intended as a Day-3 retrieval ranking signal.
- Old `bmas_mutterschutzgesetz` kept with `status: superseded` +
  `superseded_by: gii_muschg_2018` — a provenance record of the correction, not a
  silent swap. `extract.py` skips superseded entries (not ingested/cited).
- `fam_mutterschutz`'s `pairs_with` re-pointed to `gii_muschg_2018` so the
  register-distinction eval uses the real statute.
- Extracted content = the MuSchG **Inhaltsübersicht** (official title + all
  §§ 1–34 with section headings). The single URL is a table of contents, not the
  full normative prose (that lives on the per-§ subpages we don't follow).

### ⚠️ KNOWN ISSUE for Day-3 eval — statute vs plain-language register
`gii_muschg_2018` is dense legalese that will **match strongly on the exact
German terms users search**, but it is the **wrong register to surface to a
pregnant user**. Expect it to compete with `fam_mutterschutz` in retrieval. Plan:
prefer plain-language sources for user-facing answers and cite the statute only as
supporting basis, using `authority_tier` as the ranking signal. **Not built yet —
noted as a known issue.**

### New corpus-validation step (from the stub lesson)
`extract.py` now flags any source whose clean extraction is **under
`STUB_MIN_CHARS` (500) chars** as a probable stub / JS-rendered page needing
manual review — printed inline (`<-- STUB?`), in the run summary, and as a
`STUB?` flag in `--stats`. This would have caught the BMAS stub automatically.
(Currently 0 active sources flag; the smallest, `gesund_fruehe_hilfen_de`, is 923.)

### Encoding fix — decode by the page's own charset
`gesetze-im-internet.de` is **ISO-8859-1**, not UTF-8. `extract.py` was reading
raw files as hardcoded UTF-8, which mangled the statute title (the "ü" in
"Müttern" became a replacement char). Fixed to reuse `fetch.decode_bytes`
(HTTP header → `<meta>` →
utf-8 → latin-1). Verified: title renders "Müttern"; no replacement chars in any
output. The 22 UTF-8 files were byte-identical after the change (no regression).

### Validation evidence (all five requested checks passed)
- Heading trees render correctly for `fam_mutterschutz` (de, question-headed),
  `gesund_wochenbett_de` (de prose), `tk_maternity_pay` (en, h1→h2→h3).
- Smallest file `gesund_fruehe_hilfen_de.md`: title + body + `Stand:` date, no chrome.
- `fam_elterngeld_faq.md`: question headings preserved as `##` with answers beneath.
- Before/after: 9.8% reduction on the FAQ up to ~88% on hub pages (index pages that
  are mostly link lists — verified complete, not truncated).
- All 23 files contain newlines and ≥1 Markdown heading; 0 failures. No output file
  contains "Matomo" or the cookie-consent string (asserted in code, fails loudly).

---

## Known limitations / carried forward
- ~~Crude extraction~~ — DONE (see Day 2 above). Clean Markdown in `data/processed/*.md`.
- gesund `<h1>` titles keep a breadcrumb prefix (e.g. "Kindheit Was sind Frühe
  Hilfen?") — cosmetic, harmless for chunking.
- `bmas_mutterschutzgesetz` referral-stub decision (above).
- `frankfurt.de` (403) and `verwaltung.bund.de` (JS SPA, ~318 chars) excluded by
  design; would need manual browser capture if municipal detail is later required.
- `authority_tier` enum has no `municipal` value yet — decide map→`land` or extend
  if a municipal page is ever added.
- Fields still `null` by design: `topic / subtopic / user_type / insurance_type`
  (Day-2 metadata step).

---

## Next
1. **Chunking** — split the clean `data/processed/*.md` (23 active docs) into
   retrievable passages, using the preserved `##`/`###` headings as section
   boundaries. Special cases: the hub/index pages (link lists) and `gii_muschg_2018`
   (a §-TOC table, not prose).
2. **Metadata** — propose `topic/subtopic/user_type/insurance_type`, stop for review
   (can follow chunking).
3. **Day-3 eval** — build the statute-vs-plain-language ranking (known issue above).
