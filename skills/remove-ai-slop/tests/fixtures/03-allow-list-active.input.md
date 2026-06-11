---
fixture: 03-allow-list-active
expects: rewritten, but "robust" preserved
overrides: required
---

## Setup before running

Create `~/.claude/config/remove-ai-slop/user-allow-list.md` with:

```markdown
## Never flag these for me

- robust
```

Remove the file after running this fixture.

## Input

The new replication layer is robust against network partitions and survives a full leader loss without data loss. It's worth noting that we leverage Raft for consensus.
