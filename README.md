# antislop

A [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) skill that strips the tells of AI-generated writing — overused vocabulary, formulaic constructions, em-dash overuse, hedging filler, recap intros, "Despite challenges..." closers, bullet-and-bold soup, and leftover assistant scaffolding.

It's surgical, not stylistic: it removes specific giveaways while preserving the author's meaning, register, and voice.

## What it does

Triggers automatically when you paste text and ask Claude to make it "less AI", "more human", "humanize", "de-slop", "remove AI giveaways", or "check before publishing" — or when the pasted text shows multiple co-occurring AI tells even without being asked.

Covers:

- Overused vocabulary (`delve`, `tapestry`, `robust`, `pivotal`, `vibrant`, `leverage`, `navigate`, `underscore`, `garner`, `foster`, `seamless`, `holistic`, `myriad`, `realm`, …)
- Formulaic constructions (`it's not just X, it's Y`; `not only X but also Y`)
- Copula avoidance (`serves as`, `stands as a testament to`, `represents a`)
- Em-dash overuse
- Promotional padding (`stands as a testament to`, `leaves an indelible mark`)
- Recap intros and "In conclusion" outros
- Hedging filler (`it's worth noting that`, `needless to say`)
- Superficial-analysis `-ing` tails
- Leftover assistant scaffolding (`Certainly!`, `I hope this helps!`)
- Formatting tells (bullet-and-bold soup, excessive bolding, redundant "Key Takeaways" sections)
- Elegant variation

It leaves alone things that aren't slop: a single em-dash, list-shaped content, formal register where formality is required, long sentences that earn their length.

## Install

### Option 1 — As a Claude Code plugin (recommended)

```bash
/plugin install SalZaki/antislop
```

### Option 2 — Manual install

Clone the skill directly into your Claude config:

```bash
git clone https://github.com/SalZaki/antislop.git ~/.claude/skills/antislop
```

Claude Code discovers the skill on the next session.

### Option 3 — Project-scoped

Drop `skills/remove-ai-slop/` into your project's `.claude/skills/` directory. The skill ships with the project.

## Usage

Once installed, just paste text and ask:

- *"Make this less AI."*
- *"Humanize this."*
- *"Check this for slop before I publish it."*
- *"Edit out the AI tells but don't rewrite my voice."*

The skill returns the rewritten text. No preamble, no diff, no "Here's the revised version:" — just the cleaner text in the same format as the input.

Want to see what changed? Ask: *"What did you change?"* or *"Show me the diff."*

## Principles

It preserves meaning (no new claims, no dropped facts) and register: formal stays formal, casual stays casual. It cuts rather than rewrites when it can — most slop is padding, and deleting usually beats rephrasing.

If the input is already clean, the skill returns it unchanged.

## License

[MIT](./LICENSE)
