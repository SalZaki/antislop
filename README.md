# antislop

A [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) plugin for keeping writing free of AI-generated tells. Three lenses over one detection engine: rewrite the text, flag where the tells are, or get a quality-pass breakdown. Mix and match.

## Skills

| Skill | Status | What it does |
|---|---|---|
| [`remove-ai-slop`](./skills/remove-ai-slop) | ✅ Shipped | Rewrites pasted text to remove specific AI tells while preserving the author's meaning, register, and voice. Surgical, not stylistic. |
| [`detect-ai-slop`](./skills/detect-ai-slop) | ✅ Shipped | Reports *where* the AI tells are, as located findings by category and severity. No rewrite, no single score. For editorial and pre-publish review. |
| [`score-ai-slop`](./skills/score-ai-slop) | ✅ Shipped | A per-category breakdown quality pass: deterministic counts plus judged notes and a plain-language readiness call. No headline number, because a number invites gaming. |

The three lenses share one engine, so they never drift on what counts as slop.

## How it works

[`shared/spec.md`](./shared/spec.md) is the single source of truth: the category list, the fixed per-category severity, the override-merge order, the co-occurrence threshold, and the finding schema.

Detection runs in two tiers:

- **Deterministic tier.** [`shared/slop_count.py`](./shared/slop_count.py) is a zero-dependency Python 3 script that counts the *countable* tells (vocabulary-table hits, em-dash density, fixed templates, bullet-and-bold soup, scaffolding phrases). Same input plus the same overrides gives the same output every run.
- **Judged tier.** The Claude model handles the meaning-dependent tells (promotional padding, copula avoidance, register, whether `robust` is actually the wrong word here). This part reads, so it is advisory, not byte-stable.

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

`remove-ai-slop` is self-contained, so you can drop `skills/remove-ai-slop/` into your project's `.claude/skills/` on its own. `detect-ai-slop` and `score-ai-slop` depend on the shared engine at the plugin root (`shared/`), so the suite is not single-skill-copyable: install the whole plugin with `/plugin install`, or clone the repo, to use them.

## Usage

The right lens triggers from how you ask.

**Rewrite** with `remove-ai-slop`:

- *"Make this less AI."* / *"Humanize this."* / *"Edit out the AI tells but keep my voice."*

It returns the rewritten text in the same format as the input, with no preamble and no diff. To see what changed, ask *"what did you change?"* or *"show me the diff."*

**Detect** with `detect-ai-slop`:

- *"Where are the AI tells?"* / *"Flag the slop, don't change it."* / *"Check this before I publish it."*

It returns located findings (category, severity, and the offending text by paragraph). No rewrite, no single score.

**Score** with `score-ai-slop`:

- *"How sloppy is this?"* / *"Give me a slop breakdown."* / *"Is this ready to publish?"*

It returns a per-category breakdown plus a plain-language readiness call (clean / light / heavy). No 0-10 number.

## Customisation

You can add your own slop words, or exempt words from being flagged, without forking. The shared engine reads two override files, so all three skills pick up the same customisation.

**Personal overrides** (survive plugin updates):

```bash
mkdir -p ~/.claude/config/remove-ai-slop
```

Then add either or both:

- `~/.claude/config/remove-ai-slop/user-vocabulary.md` for extra words to flag
- `~/.claude/config/remove-ai-slop/user-allow-list.md` for words to never flag

**Project overrides** (shipped with your repo, shared with your team):

- `.claude/skills/remove-ai-slop/overrides/user-vocabulary.md`
- `.claude/skills/remove-ai-slop/overrides/user-allow-list.md`

Format spec and examples live in [`skills/remove-ai-slop/overrides/README.md`](./skills/remove-ai-slop/overrides/README.md). The allow-list wins ties, so you can keep a domain term the tool would otherwise flag (say `robust` for server reliability) without disabling the skill.

## Continuous integration

Every pull request runs [`.github/workflows/ci.yml`](./.github/workflows/ci.yml):

- the deterministic engine's unit tests (`python -m unittest discover -s shared`),
- a `SKILL.md` frontmatter validator ([`scripts/check_frontmatter.py`](./scripts/check_frontmatter.py)) so a malformed skill can't land, and
- a **report-only slop gate** ([`scripts/slop_gate.py`](./scripts/slop_gate.py)) that scores changed author-facing markdown and surfaces clusters as a step summary and inline annotations. It is advisory: it never fails the build. Flipping it to a blocking check later is a one-line change (`--enforce`).

## Project structure

```
antislop/
├── .claude-plugin/
│   └── plugin.json                  # Plugin manifest (version lives here)
├── .github/workflows/
│   └── ci.yml                       # Tests + frontmatter validation + report-only slop gate
├── shared/                          # The detection engine, shared by all skills
│   ├── spec.md                      # Single source of truth: categories, severity, threshold, schema
│   ├── slop_count.py                # Zero-dependency deterministic scorer
│   ├── test_slop_count.py           # Engine unit tests
│   └── test_slop_gate.py            # Gate unit tests
├── scripts/
│   ├── slop_gate.py                 # Report-first CI gate over the engine
│   └── check_frontmatter.py         # SKILL.md frontmatter validator
├── skills/
│   ├── remove-ai-slop/              # Rewrite lens
│   │   ├── SKILL.md                 # Slim guide: principles, decisions, output rules
│   │   ├── references/              # Detailed tells and fix recipes (loaded on demand)
│   │   ├── overrides/               # User/project customisation (stubs + format spec)
│   │   ├── examples/                # Worked rewrites per category
│   │   └── tests/fixtures/          # Hand-runnable input/expected pairs
│   ├── detect-ai-slop/SKILL.md      # Located-findings lens
│   └── score-ai-slop/SKILL.md       # Breakdown lens
├── CHANGELOG.md
├── CONTRIBUTING.md
├── README.md
└── LICENSE
```

## Why this structure

A few choices worth pointing out, since they affect day-to-day cost and editability:

**Progressive disclosure.** `SKILL.md` is slim (~150 lines). The bulky vocabulary tables and category-specific fix recipes live in `references/` and only load when the skill actually needs them. Baseline session cost drops roughly 3x versus a monolithic skill file.

**One engine, three lenses.** Rewrite, detect, and score all read `shared/spec.md` and run `shared/slop_count.py`, so they agree on what slop is by construction. Adding a fourth lens is a new `SKILL.md`, not a new copy of the rules.

**Deterministic where it can be, honest where it can't.** The countable tells are scored by code (stable, testable, the basis for the CI gate). The meaning-dependent tells are judged by the model and labelled as such. The score is a per-category breakdown, never a single 0-10 number, so there is nothing to game.

**User customisation without forking.** Personal overrides at `~/.claude/config/<skill>/` survive plugin updates. Project overrides at `.claude/skills/<skill>/overrides/` travel with the repo so teammates inherit them. The allow-list always wins, so a domain term stays put without disabling the skill.

**Two test tiers.** The deterministic engine has stdlib unit tests that run in CI on every PR. The LLM-judged fixtures in `tests/fixtures/` stay hand-runnable, since the rewrite is non-deterministic: paste each input into a Claude session and diff against the expected output.

## Adding a new skill

Rough sketch for a new lens in this repo:

1. `mkdir skills/<new-skill>` and create `SKILL.md` with frontmatter `name:` and a trigger-focused `description:` (keep the description free of an unquoted `: ` so the YAML parses).
2. Reference `shared/spec.md` and the shared engine rather than re-describing the rules.
3. Add `references/` only if you have heavy data that shouldn't load every session.
4. Add tests under `shared/` if you add deterministic logic.
5. Update this README's Skills table.

The `writing-skills` conventions from Anthropic's superpowers plugin are the reference for skill structure; this repo follows them.

## Contributing

Contributions are welcome: vocabulary additions, bug fixes, new lenses, tests, or docs. See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full guide, including the dogfood rule (run `remove-ai-slop` on your own prose before opening a PR). CI runs the unit tests, the frontmatter validator, and the report-only slop gate on every PR.

If you're unsure whether something fits, open an issue first.

## License

[MIT](./LICENSE)
