# antislop

A [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) plugin for keeping writing free of AI-generated tells. One install gets you a growing set of focused skills you can mix and match.

## Skills

| Skill | Status | What it does |
|---|---|---|
| [`remove-ai-slop`](./skills/remove-ai-slop) | ✅ Shipped | Rewrites pasted text to remove specific AI tells while preserving the author's meaning, register, and voice. Surgical, not stylistic. |
| `score-ai-slop` | 🚧 Planned | Returns a slop score (0–10) plus a category breakdown without rewriting. For "check before publishing" use. |
| `detect-ai-slop` | 🚧 Planned | Flags positions of AI tells without rewriting. Suited for editorial review and CI gates. |

Adding a new skill is just a new directory under `skills/`. The plugin manifest discovers them automatically.

## Install

### As a Claude Code plugin (recommended)

```bash
/plugin install SalZaki/antislop
```

### Manual install

```bash
git clone https://github.com/SalZaki/antislop.git ~/.claude/skills/antislop
```

Claude Code discovers the skills on the next session.

### Project-scoped

Drop the relevant `skills/<skill-name>/` directory into your project's `.claude/skills/`. The skill ships with the project.

## Usage (remove-ai-slop)

Once installed, paste text and ask:

- *"Make this less AI."*
- *"Humanize this."*
- *"Check this for slop before I publish it."*
- *"Edit out the AI tells but don't rewrite my voice."*

The skill returns the rewritten text in the same format as the input. No preamble, no diff, no "Here's the revised version:". To see what changed, ask *"What did you change?"* or *"Show me the diff."*

## Customisation

You can add your own slop words, or exempt words from being flagged, without forking. Each skill that uses vocabulary reads two override files.

**Personal overrides** (survive plugin updates):

```bash
mkdir -p ~/.claude/config/remove-ai-slop
```

Then add either or both:

- `~/.claude/config/remove-ai-slop/user-vocabulary.md` — extra words to flag
- `~/.claude/config/remove-ai-slop/user-allow-list.md` — words to never flag

**Project overrides** (shipped with your repo, shared with your team):

- `.claude/skills/remove-ai-slop/overrides/user-vocabulary.md`
- `.claude/skills/remove-ai-slop/overrides/user-allow-list.md`

Format spec and examples live in [`skills/remove-ai-slop/overrides/README.md`](./skills/remove-ai-slop/overrides/README.md). Allow-list wins ties, so you can keep a domain-specific term (`robust` for server reliability, `leverage` for finance) without disabling the skill.

## Project structure

```
antislop/
├── .claude-plugin/
│   └── plugin.json                  # Plugin manifest
├── skills/
│   └── remove-ai-slop/
│       ├── SKILL.md                 # Slim guide — principles, decisions, output rules
│       ├── references/              # Detailed tells & fix recipes (loaded on demand)
│       │   ├── overused-vocabulary.md
│       │   ├── formulaic-constructions.md
│       │   ├── padding-and-filler.md
│       │   ├── formatting-tells.md
│       │   ├── scaffolding-and-recap.md
│       │   └── elegant-variation.md
│       ├── overrides/               # User/project customisation (stubs + format spec)
│       │   ├── README.md
│       │   ├── user-vocabulary.md
│       │   └── user-allow-list.md
│       ├── examples/
│       │   └── before-after.md      # Worked rewrites per category
│       └── tests/
│           ├── README.md
│           └── fixtures/            # Hand-runnable input/expected pairs
├── README.md
├── LICENSE
└── .gitignore
```

Future skills (`score-ai-slop`, `detect-ai-slop`, …) will sit alongside `remove-ai-slop` under `skills/` with the same internal shape.

## Why this structure

A few choices worth pointing out, since they affect day-to-day cost and editability:

**Progressive disclosure.** `SKILL.md` is slim (~150 lines, ~1100 tokens). The bulky vocabulary tables and category-specific fix recipes live in `references/` and only load when the skill actually needs them. Baseline session cost drops roughly 3× versus a monolithic skill file.

**User customisation without forking.** Personal overrides at `~/.claude/config/<skill>/` survive plugin updates. Project overrides at `.claude/skills/<skill>/overrides/` travel with the repo so teammates inherit them. No need to fork the skill, edit upstream, and chase merges.

**Allow-list beats hard rules.** Domain-specific terms (`robust` for servers, `leverage` for finance, `crucial` in editorial style) can be exempted per-user or per-project. The skill stays opinionated by default but gets out of your way when you know the word is right.

**Hand-runnable tests.** `tests/fixtures/` holds input/expected pairs you can paste into a Claude session by hand and diff. No harness, no CI required — but enough structure to catch regressions when editing the skill or adding a new one.

**Room to grow.** Each new skill is a sibling directory under `skills/`. Shared assets (override locations, format conventions) are already named in a skill-scoped way (`~/.claude/config/<skill>/`), so adding `score-ai-slop` doesn't require renaming anything.

## Adding a new skill

Rough sketch for future skills in this repo:

1. `mkdir skills/<new-skill>` and create `SKILL.md` with frontmatter `name:` and a trigger-focused `description:` (under 1024 chars total).
2. Add `references/` only if you have heavy data that shouldn't be loaded every session.
3. Add `overrides/` only if the skill has user-configurable behaviour.
4. Add `tests/fixtures/` with at least one happy-path and one restraint fixture (input that should *not* be touched).
5. Update this README's Skills table.

The `writing-skills` conventions from Anthropic's superpowers plugin are the reference for skill structure; this repo follows them.

## License

[MIT](./LICENSE)
