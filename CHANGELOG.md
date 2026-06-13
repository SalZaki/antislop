# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); versions track `.claude-plugin/plugin.json`.

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
