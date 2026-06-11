---
fixture: 03-allow-list-active
expects: rewritten, but "robust" preserved
overrides: required
---

The new replication layer is robust against network partitions and survives a full leader loss without data loss. We use Raft for consensus.

---

## What the test is checking

- "robust" is **kept** (it's on the user's allow-list, even though it's in defaults)
- "It's worth noting that" is still removed (hedging filler)
- "leverage" is still replaced with "use" (in defaults, not allow-listed)

Failure mode: "robust" is replaced. That means the skill is ignoring the override file at `~/.claude/config/remove-ai-slop/`.
