# Tests

Lightweight fixtures for verifying that edits to the skill don't regress core behaviour. These are the LLM-judged tier: run them by hand, pasting each input into Claude and diffing against the expected output. The deterministic engine has automated unit tests in `shared/` that run in CI; these fixtures stay manual because the rewrite is non-deterministic.

## How to run

For each fixture pair under `fixtures/`:

1. Open the `.input.md` file. Copy its body (everything below the `---` header).
2. In a Claude Code session with the skill installed, paste it and say: **"Apply the remove-ai-slop skill to this."**
3. Compare Claude's output against the matching `.expected.md` file.

If Claude's output differs from the expected output in a way that *changes the meaning of the test* (e.g., 01 should rewrite slop-heavy text, but Claude returns it unchanged), the change to the skill regressed something.

Minor wording differences in the rewrite are fine — these tests check intent, not exact strings.

## Fixtures

| # | File | Tests |
|---|---|---|
| 01 | `marketing-blurb` | Default vocabulary and padding get flagged and rewritten. |
| 02 | `clean-text` | Clean prose is returned unchanged with the no-changes note. |
| 03 | `allow-list-active` | A word in the default vocabulary (`robust`) is preserved when the user's allow-list contains it. |
| 04 | `user-vocab-addition` | A word *not* in defaults (`utilize`) gets flagged when added via user-vocabulary. |

## Setup for fixtures 03 and 04

Fixtures 03 and 04 require override files to be present. Each fixture's `.input.md` header tells you which override file to create and what to put in it before running.

After running the fixture, delete or revert the override file so it doesn't pollute later tests.
