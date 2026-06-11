---
fixture: 04-user-vocab-addition
expects: "utilize" flagged via override
overrides: required
---

## Setup before running

Create `~/.claude/config/remove-ai-slop/user-vocabulary.md` with:

```markdown
## Additional slop to flag

| Word | Plain alternative |
|---|---|
| utilize | use |
```

Remove the file after running this fixture.

## Input

We utilize a Postgres replica for read-heavy analytical queries. The replica is updated via logical replication, which we configured to minimize lag.
