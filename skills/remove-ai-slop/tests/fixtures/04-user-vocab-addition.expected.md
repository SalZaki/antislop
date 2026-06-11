---
fixture: 04-user-vocab-addition
expects: "utilize" flagged via override
overrides: required
---

We use a Postgres replica for read-heavy analytical queries. The replica is updated via logical replication, which we configured to minimize lag.

---

## What the test is checking

- "utilize" is **replaced** with "use" — even though "utilize" is not in the default vocabulary
- The rest of the sentence (which is clean) is untouched
- No "heavy rewrite" warning, since only one word changed

Failure mode: "utilize" survives. That means the skill is ignoring the user-vocabulary override file.
