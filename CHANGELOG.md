# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); versions track `.claude-plugin/plugin.json`.

## [0.3.3] - 2026-06-13

### Changed
- Override docs: clarified that the parser strips HTML comments (`<!-- ... -->`) and
  their contents before reading tables/bullets, so commented-out example rows never
  count as live entries.
- README install: documented that the `detect`/`score` suite needs the whole plugin
  (shared engine at the plugin root); only `remove-ai-slop` is single-skill-copyable.

## [0.3.2] - 2026-06-13

### Added
- **CI** (`.github/workflows/ci.yml`): runs the `shared/` unit tests and a SKILL.md
  frontmatter validator on every pull request and push to `main`.
- **`scripts/check_frontmatter.py`**: validates each skill's YAML frontmatter (PyYAML in
  CI, heuristic fallback locally). Guards against the `0.2.0` colon-space break recurring.

### Changed
- README and `tests/README.md` now describe two test tiers: the deterministic engine is
  CI-tested; the LLM-judged fixtures stay hand-run (the rewrite is non-deterministic).

## [0.3.1] - 2026-06-13

Two engine bugs caught by dogfooding the suite on a real AI-marketing blurb.

### Fixed
- **Double-count:** a longer vocabulary phrase and its bare sub-term both fired on the
  same span (e.g. `navigate the complexities of` also flagged `navigate`), because the
  vocab table splits `/`-variants into separate terms. The longer match now suppresses
  any sub-term contained within its span.
- **Span quality:** a finding's `quoted_text` grabbed 20 trailing characters and
  truncated mid-word (e.g. `"fosteri"`). It is now the exact matched term.
- Added regression tests for both (no-double-count, longest-phrase-wins, clean
  `quoted_text`). Suite is 24 tests.

### Known
- Inflections not listed in the vocab table (e.g. `empowers` when the table has
  `empower`/`empowering`) are left to the LLM judged tier; a table pass is deferred.

## [0.3.0] - 2026-06-13

The third lens lands. `score-ai-slop` gives an aggregate quality-pass read over the same
engine: a per-category breakdown plus a plain-language publish-readiness call.

### Added
- **`score-ai-slop` skill** — the breakdown lens. Runs the deterministic script for
  per-category counts, adds judged notes for the meaning-dependent categories, and
  returns a readiness call (clean / light / heavy). Deliberately no single 0-10 number,
  because one number invites gaming. Located findings stay in `detect-ai-slop`; rewriting
  stays in `remove-ai-slop`.
- A `summarize()` unit test covering the per-category aggregation `score-ai-slop` relies on.

### Changed
- README skills table: the suite (`remove` / `detect` / `score`) is complete.

## [0.2.1] - 2026-06-13

### Fixed
- `detect-ai-slop` `SKILL.md` frontmatter failed to parse ("mapping values are not
  allowed in this context"): the `description:` value contained an unquoted
  colon-space (`report lens: it returns`), which YAML read as a nested mapping.
  Reworded to drop the colon (and an em-dash). The skill now loads. 0.2.0 shipped this
  break to `main`; 0.2.1 is the hotfix.

## [0.2.0] - 2026-06-13

The suite grows a second lens and a shared engine. `detect-ai-slop` reports *where*
the AI tells are without rewriting, and a zero-dependency Python tier counts the
deterministic ones so the same input gives the same answer every run.

### Added
- **`detect-ai-slop` skill** — the report lens. Returns located findings (category,
  severity, the offending text by paragraph) instead of a rewrite or a single score.
  For editorial / pre-publish review.
- **Shared detection engine.** `shared/spec.md` is the single source of truth for the
  category enum, fixed per-category severity, override-merge order, the unified
  co-occurrence threshold, and the finding schema. `shared/slop_count.py` is a
  zero-dependency Python 3 script that counts the deterministic tells (vocabulary-table
  hits, em-dash density, fixed templates, bold/bullet soup, scaffolding phrases) and is
  the sole parser of the override files. When `python3` is absent the skill degrades to
  an LLM-only pass tagged `unstable`.
- **`shared/test_slop_count.py`** — 19 stdlib unit tests covering paragraph splitting,
  vocabulary + word boundaries, allow-list suppression, formatting and template tells,
  the false-positive guard, and the determinism contract.

### Changed
- Reconciled the co-occurrence threshold across the suite to one unified rule (2+ tells
  of any category in a paragraph, or 3+ vocabulary-table words), defined once in
  `shared/spec.md` and referenced by `remove-ai-slop`.
- README documents the shared engine and that the suite ships together via
  `/plugin install`.

### Notes
- The score is deliberately a per-category breakdown, not a single 0-10 number, to keep
  the tool editor-shaped rather than a bypass-optimizer target.
- Weighted scoring, a CI gate (Direction C), and a voice editor (Direction B) are
  deferred until there is real usage data.

## [0.1.0]

- Initial release: `remove-ai-slop` skill (rewrite lens) with progressive-disclosure
  references and a user/project override system.
