# Shared detection spec

Single source of truth for the antislop suite. `remove-ai-slop`, `detect-ai-slop`,
and (PR2) `score-ai-slop` all reference this file instead of re-describing the rules,
so the three skills cannot drift. The deterministic script `shared/slop_count.py`
implements the countable half of this spec.

## Category enum

These exact names are used by every skill and by the script's JSON output.

| Category | Countable? | Fixed severity | Notes |
|---|---|---|---|
| `overused-vocabulary` | yes (table hits) | low | Source table: `skills/remove-ai-slop/references/overused-vocabulary.md`. A single hit is low; clusters are what matter. |
| `formulaic-constructions` | yes (fixed templates) | high | "It's not just X, it's Y", "not only X but also Y", copula substitutions. |
| `formatting-tells` | yes (em-dash density, bold/bullet) | med | Counted structurally. |
| `scaffolding-and-recap` | partly (fixed phrases) | high | "Certainly!", "I hope this helps!", "In conclusion", "In summary". |
| `padding-and-filler` | no (meaning) | med | Judged tier only. |
| `elegant-variation` | no (meaning) | low | Judged tier only. |

**Tier split.** Countable categories are scored by the script (deterministic, stable).
Meaning-dependent categories (`padding-and-filler`, `elegant-variation`, and the
contextual parts of the others) are surfaced by the LLM (judged tier, non-deterministic).

**Severity is a fixed constant, not a weight.** The severity column above is a fixed
per-category label. It is byte-stable and never tuned against usage data, so it does
NOT reintroduce the deferred weighted scoring.

## Override merge order

The script is the sole parser of override files when it runs. Merge order:

1. Defaults: `skills/remove-ai-slop/references/overused-vocabulary.md` (the vocab table).
2. Personal: `~/.claude/config/remove-ai-slop/user-vocabulary.md`, `user-allow-list.md`.
3. Project: `.claude/skills/remove-ai-slop/overrides/user-vocabulary.md`, `user-allow-list.md`.

**Allow-list wins everything:** a word on any allow-list is never counted, even if it is
in the defaults. The parser strips HTML comments (`<!-- ... -->`) before reading tables
and bullets.

## Co-occurrence threshold (forced action, for the rewrite lens)

Forced action when, in a single paragraph:
- **2+ tells of any category** appear, OR
- **3+ vocabulary-table words** appear.

`detect-ai-slop` reports raw findings and does not apply this threshold; the threshold
is the rewrite lens's forced-action rule.

## Finding schema

```
{ rule_id, category, tier, paragraph_index, quoted_text, severity, count, stability, suggested_fix? }
```

- `tier`: `deterministic` (script) or `judged` (LLM).
- `paragraph_index` + `quoted_text`: the durable anchor. A codepoint offset, if present,
  is a best-effort convenience field, not the source of truth.
- `stability`: `stable` when the script produced it, `unstable` on the LLM-only fallback.
- `suggested_fix`: present for the rewrite lens, omitted by `detect-ai-slop`.

## Paragraph definition

A paragraph is a blank-line-delimited block. Fenced code blocks (```) and markdown
tables are excluded from counting.
