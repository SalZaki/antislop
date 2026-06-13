# antislop

A [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) plugin for keeping writing free of AI-generated tells. One install gets you a growing set of focused skills you can mix and match.

## Skills

| Skill | Status | What it does |
|---|---|---|
| [`remove-ai-slop`](./skills/remove-ai-slop) | ✅ Shipped | Rewrites pasted text to remove specific AI tells while preserving the author's meaning, register, and voice. Surgical, not stylistic. |
| [`detect-ai-slop`](./skills/detect-ai-slop) | ✅ Shipped | Reports *where* the AI tells are, as located findings by category and severity, no rewrite and no single score. For editorial / pre-publish review. |
| [`score-ai-slop`](./skills/score-ai-slop) | ✅ Shipped | A per-category breakdown quality pass: deterministic counts plus judged notes and a plain-language readiness call. No headline number (a number invites gaming). |

The suite shares one detection engine: [`shared/spec.md`](./shared/spec.md) holds the
rules, and [`shared/slop_count.py`](./shared/slop_count.py) is a zero-dependency Python 3
script that counts the deterministic tells (the LLM judges the meaning-dependent ones).
Because the skills share that engine, the suite ships together via `/plugin install`.

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

`remove-ai-slop` is self-contained, so you can drop `skills/remove-ai-slop/` into your project's `.claude/skills/` on its own. `detect-ai-slop` and `score-ai-slop` depend on the shared engine at the plugin root (`shared/`), so the suite is not single-skill-copyable: install the whole plugin with `/plugin install` (or clone the repo) to use them.

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

**Two test tiers.** The deterministic engine (`shared/`) has stdlib unit tests plus a SKILL.md frontmatter validator, both run in CI on every PR (`.github/workflows/ci.yml`). The LLM-judged fixtures in `tests/fixtures/` stay hand-runnable, since the rewrite is non-deterministic: paste each input into a Claude session and diff against the expected output.

**Room to grow.** Each new skill is a sibling directory under `skills/`. Shared assets (override locations, format conventions) are already named in a skill-scoped way (`~/.claude/config/<skill>/`), so adding `score-ai-slop` doesn't require renaming anything.

## Adding a new skill

Rough sketch for future skills in this repo:

1. `mkdir skills/<new-skill>` and create `SKILL.md` with frontmatter `name:` and a trigger-focused `description:` (under 1024 chars total).
2. Add `references/` only if you have heavy data that shouldn't be loaded every session.
3. Add `overrides/` only if the skill has user-configurable behaviour.
4. Add `tests/fixtures/` with at least one happy-path and one restraint fixture (input that should *not* be touched).
5. Update this README's Skills table.

The `writing-skills` conventions from Anthropic's superpowers plugin are the reference for skill structure; this repo follows them.

## Contributing

Contributions are welcome — vocabulary additions, bug fixes, new sibling skills, tests, or docs. See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full guide: repo orientation, how to modify or add a skill, how to run the fixtures, commit and PR conventions, and the dogfood rule (apply `remove-ai-slop` to your own prose before opening a PR).

If you're unsure whether something fits, open an issue first.

## License

[MIT](./LICENSE)
