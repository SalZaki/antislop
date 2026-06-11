# Overrides

User and project customisations for the `remove-ai-slop` skill. Two files do the work:

- **`user-vocabulary.md`** — words and phrases you want flagged in addition to the defaults
- **`user-allow-list.md`** — words you *never* want flagged, even if they appear in the defaults

## Where overrides live

The skill checks three locations in priority order. Later entries override earlier ones; allow-list always wins.

| Priority | Path | Scope | Survives plugin updates? |
|---|---|---|---|
| 1 (defaults) | `<skill-dir>/overrides/` (this directory) | Bundled stubs, ship with skill | n/a |
| 2 (personal) | `~/.claude/config/remove-ai-slop/` | All your sessions | Yes |
| 3 (project) | `.claude/skills/remove-ai-slop/overrides/` in CWD | Just this project | n/a (in your repo) |

**Recommended:** Put your personal preferences in `~/.claude/config/remove-ai-slop/` so they survive plugin updates. Put per-project tweaks in the project's `.claude/` directory so the rest of the team gets them too.

## File format

Both files are plain markdown. The skill parses the tables and bullets — comments and section headings are fine, they're just ignored.

### `user-vocabulary.md`

```markdown
## Additional slop to flag

| Word | Plain alternative |
|---|---|
| utilize | use |
| pinpoint | find, identify |
| at scale | (often delete) |
```

The columns are the same as the default vocabulary table. Plain alternative can be blank if you just want the word flagged.

### `user-allow-list.md`

```markdown
## Never flag these for me

- robust   <!-- we use it technically for server reliability -->
- crucial  <!-- our editorial style permits this -->
- leverage <!-- finance domain — "leverage an asset" is the term -->
```

Bullet list. Optional HTML comments document *why* (useful for project files shared with a team).

## Merge order

1. Start with the bundled defaults in `references/`
2. Merge in personal additions from `~/.claude/config/remove-ai-slop/user-vocabulary.md`
3. Merge in project additions from `.claude/skills/remove-ai-slop/overrides/user-vocabulary.md`
4. Remove anything that appears in any `user-allow-list.md` — allow-list beats every layer above
