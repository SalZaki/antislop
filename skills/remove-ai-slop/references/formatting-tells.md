# Formatting tells

The shape of the text, not the words. These are the most reliable AI giveaways at a glance.

## Em-dash overuse

Em-dashes aren't bad. Multiple em-dashes in a short paragraph — especially as the only form of parenthetical punctuation — are a tell.

Rules of thumb:

- **0–1 em-dash per paragraph** is normal.
- **2+ in one paragraph** is worth checking.
- **3+ in one paragraph** is almost certainly AI; replace at least one with parentheses, a comma, or a full stop.

Also watch for the specific construction `clause — short emphatic restatement`, which LLMs over-use:

> This is the future of work — fast, distributed, collaborative.

Replace either the punctuation or the restatement.

## Bullet-and-bold soup

Every other sentence rendered as `- **Bold key**: explanation`. When this happens across a whole section, the user likely wanted prose.

**Fix:** Convert short bullets into a paragraph. Keep bullets only where a list is genuinely a list — parallel items, three or more, no inherent prose flow.

## Title Case In Every Heading

When the rest of the document is sentence case, AI output often defaults to title casing all headings. Flatten to sentence case unless house style says otherwise.

## Excessive bolding

Every key term bolded the first time it's mentioned, like a textbook. Strip to nothing unless the bold has a specific purpose (a UI label, a function name, a column header in a table).

## Redundant summary sections

A `## Conclusion` or `## Key Takeaways` or `## Summary` section that just restates the previous sections. Delete it. If the body is good it doesn't need a recap; if it isn't, a recap won't save it.

## Co-occurrence rule

**Threshold for forced action:** if 2+ formatting tells appear in the same document, fix all of them. They cluster.
