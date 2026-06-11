---
fixture: 02-clean-text
expects: unchanged
overrides: none
---

The migration completed at 03:14 UTC. We rolled three services and caught one regression in the canary phase. The postmortem is in the shared doc; the action items are assigned.

*No changes — text reads as written by a human.*

---

## What the test is checking

- Skill recognises clean prose and doesn't invent slop to fix
- The no-changes note is present
- No paraphrasing, no synonym swaps, no "improvements"

Failure mode: the skill returns a "cleaner" version anyway. That means it's over-rewriting and would damage user text in production.
