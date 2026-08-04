# Decision Log — NurtureDE

## 2026-08-03 — Day 1

- **No new dependencies for fetch/extraction.** Use stdlib `html.parser` for text
  extraction (content hash + SPA heuristic). Rationale: good enough for a *stable
  hash* and *size heuristic*; high-quality boilerplate-stripped extraction is a
  Day-2 concern where we'll propose trafilatura/bs4. Trade-off: crude extraction
  now, but zero install and reproducible.

- **Comment-safe writeback to sources.yaml via targeted in-place line edits**
  (keyed on `id`), not `pyyaml.dump`. Rationale: the YAML is hand-authored with
  explanatory comments that dump would destroy. Alternative considered: sidecar
  `manifest.json` (rejected — spec says write to sources.yaml) and `ruamel.yaml`
  round-trip (rejected — new dependency).

- **Do not bypass access controls.** frankfurt.de returns 403 to our research UA;
  we do NOT spoof a browser UA to evade it. A provenance/citation project should
  fetch only what sources permit us to fetch as ourselves. Manual capture is the
  allowed escape hatch if city-specific detail is needed later.

- **Birth-registration sourced from Familienportal, not the municipal/portal pages.**
  verwaltung.bund.de is a SPA (uncrawlable via simple GET); frankfurt.de 403s.
  Familienportal `anmeldung-standesamt` is clean, federal, same well-behaved domain.

- **pairs_with used to stage register-distinction evals.** `bmas_mutterschutzgesetz`
  (statute/employer register) ↔ `fam_mutterschutz` (plain-language register), and
  the TK Mutterschaftsgeld pages ↔ `fam_mutterschaftsleistungen` (federal rule vs
  insurer process). Purpose: Day-3 test that the system cites the right register.

## 2026-08-03 — Day 2

- **beautifulsoup4 for extraction (new dep, approved).** Three sites use
  incompatible containers and TK uses custom elements — needs a queryable tree +
  subtree deletion + custom-tag traversal. Chose bs4 (explicit, auditable
  per-domain selectors) over stdlib (would hand-roll a DOM) and over trafilatura
  (heuristic/non-deterministic; can't target TK's `<tkds-*>`). Provenance projects
  want auditable selection, not "a model guessed the main block."

- **Output clean Markdown, hash from the clean text.** Day-1's flattened text was
  unusable for chunking. Re-extract from cached `data/raw/` (no re-fetch) to
  `data/processed/*.md`; recompute all `content_hash` from Markdown. Intentional —
  old hashes fingerprinted boilerplate. `last_verified_date` unchanged (not re-fetched).

- **Unwrap, don't delete, structural wrappers that carry headings.** gesund nests
  `<h2>` in `<button>` and `<h1>` in `<header>`; deleting the tag deletes the
  heading. Unwrap keeps contents. General lesson: strip chrome by class/role, not
  by structural tag name.

- **Decode by the page's declared charset, never a hardcoded encoding.**
  gesetze-im-internet.de is ISO-8859-1; a fixed UTF-8 read corrupted the statute
  title. Reuse header→meta→utf-8→latin-1 detection everywhere bytes are decoded.

- **`authority_tier: primary-law` + lifecycle fields (`status`/`superseded_by`).**
  When the BMAS "statute" proved to be a 140-char stub, re-pointed to the real law
  on gesetze-im-internet.de as `primary-law` (ranks above `federal`, a Day-3
  ranking signal). Kept the old entry as `superseded_by` the new id — correct a
  source by superseding with a record, never silently swap. Superseded entries are
  not ingested.

- **Stub tripwire in extraction.** Flag any source whose clean extraction is <500
  chars as a probable stub / JS-rendered page needing manual review. Abstracts the
  BMAS-stub mistake into a check that catches the whole class automatically.
