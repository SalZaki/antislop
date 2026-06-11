# Contributing to antislop

Thanks for taking the time. This repo holds a small, focused set of Claude Code skills for keeping writing free of AI-generated tells. Contributions of any size are welcome, from a single vocabulary word to a whole new skill.

## Ways to contribute

- **Vocabulary additions** — propose new slop words for `references/overused-vocabulary.md`, or new phrases for any other reference file.
- **Bug fixes** — wrong fix recipe, missing edge case, a tell the skill misses or over-flags.
- **New skills** — sibling skills under `skills/` (e.g. `score-ai-slop`, `detect-ai-slop`) that fit the plugin's theme.
- **Tests** — additional fixtures in any skill's `tests/fixtures/` that catch regressions or pin down a tricky edge case.
- **Documentation** — clarifications to `SKILL.md`, the references, or the top-level README.

If you're unsure whether a contribution fits, open an issue first.

## Repo orientation

```
.claude-plugin/plugin.json    # Plugin manifest
skills/<skill-name>/          # One directory per skill
  SKILL.md                    # Slim guide (loaded when skill triggers)
  references/                 # Heavy reference data (loaded on demand)
  overrides/                  # User/project customisation stubs + format spec
  examples/                   # Worked before/after rewrites
  tests/                      # Hand-runnable fixtures
```

The top-level [README](./README.md) has a fuller layout diagram and the "Why this structure" rationale.

## Modifying an existing skill

1. Make the change in the smallest file that owns it.
   - New slop word → add a row to the relevant table in `references/`.
   - New tell category → consider whether it belongs in an existing reference or warrants a new one.
   - Behavioural change (e.g. tighter threshold for forced rewrite) → update `SKILL.md` and explain *why* in the commit message.
2. Add or update a fixture in `tests/fixtures/` that demonstrates the change. If the change shouldn't affect existing fixtures, run them by hand to confirm they still pass.
3. Update `examples/before-after.md` if the change introduces a new category of fix.

## Adding a new skill

1. Create `skills/<new-skill>/SKILL.md`.
2. Write a trigger-focused `description:` in the frontmatter — list the phrases users will actually say, not what the skill does. Keep the whole frontmatter under 1024 characters.
3. Keep the body slim (target under 500 words). Move heavy data into `references/`.
4. Add `overrides/` only if the skill has user-configurable behaviour.
5. Add at least two fixtures in `tests/fixtures/`: one happy-path (skill should act) and one restraint (skill should *not* act on clean input).
6. Add a row to the Skills table in the top-level README.

Sibling skills can share `~/.claude/config/<skill>/` conventions but should otherwise stand alone — no cross-skill dependencies inside `references/`.

## Running tests

There's no harness. Each skill's `tests/README.md` explains how to run its fixtures by hand: paste the `.input.md` body into a Claude session with the skill installed, then diff against the matching `.expected.md`.

Exact wording will vary between runs. Tests check intent (was the slop caught? was clean text left alone?), not strings. The `## What the test is checking` block in each `.expected.md` documents the actual pass condition.

## Conventions

**Commit messages** use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat(skill): add detect-ai-slop sibling skill`
- `fix(skill): correct fix recipe for em-dash overuse`
- `docs: clarify override merge order in README`
- `refactor(skill): split references for progressive disclosure`
- `test(skill): add fixture for allow-list precedence`

**Signed commits** are required on `main`. If you don't have a GPG key set up, see [GitHub's docs on signing commits](https://docs.github.com/en/authentication/managing-commit-signature-verification). If GPG isn't realistic for you, mention it in the PR and a maintainer can review and merge.

**Branch naming**: `feat/<short-description>`, `fix/<short-description>`, `docs/<short-description>`. Not strict, but it helps reviewers.

**Writing style**: the project eats its own dogfood. Apply the `remove-ai-slop` skill to your own documentation before opening a PR. No "comprehensive solutions", no "robust frameworks", no recap outros.

## Pull request process

1. Fork the repo, create a branch off `main`.
2. Make your change. Run the fixtures for any skill you touched.
3. Open a PR with:
   - A short description of *what* changed and *why* (the underlying need or bug, not just the diff).
   - Notes on any fixtures you added or had to update.
   - A flag if your change affects an existing user-facing default (vocabulary removal, threshold tightening, etc.).
4. Reviewers will check: does the change fit the skill's principles? Is there a test for it? Does it preserve the surgical-not-stylistic posture (for `remove-ai-slop`)?

## Code of conduct

Be kind, be specific, assume good faith. Disagreements about a vocabulary word, a fix recipe, or a structural choice are normal — argue the substance, not the person. Maintainers reserve the right to close issues or PRs that aren't engaging in good faith.

## License

Contributions are released under the repo's [MIT licence](./LICENSE). By opening a PR you confirm you have the right to release the contribution under that licence.
