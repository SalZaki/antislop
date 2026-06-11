---
name: remove-ai-slop
description: Rewrite text to remove the tells of AI generation — overused vocabulary (delve, tapestry, robust, pivotal, vibrant, navigate, leverage), formulaic constructions ("it's not just X, it's Y"; "not only X but also Y"), copula avoidance ("serves as", "stands as a testament to", "represents a"), em-dash overuse, promotional padding, recap intros, "Despite challenges..." closers, hedging filler ("it's worth noting that"), bullet-and-bold soup, and leftover assistant scaffolding ("Certainly!", "I hope this helps!"). Use whenever the user pastes text and asks to make it "less AI", "less ChatGPT", "less slop", "more human", "humanize", "de-slop", "de-AI", "edit out the AI tells", "remove AI giveaways", "clean up this generated copy", "this sounds AI-generated", or asks to check writing before publishing. Also trigger when the user pastes draft copy with multiple co-occurring AI tells, even if they haven't named the problem.
---

# Remove AI Slop

Take a piece of text and rewrite it so it no longer reads as machine-generated, while preserving the author's intended meaning, register, and voice.

## Goal: surgical, not stylistic

The user's text might be partly good. Don't impose a new voice — remove specific tells. Change as little as possible while still fixing the giveaways. Over-rewriting (e.g., turning every sentence into a different one to "humanize" the text) defeats the purpose: it produces a different piece of writing, not a cleaner version of the user's.

Three principles:

1. **Preserve meaning.** No new claims, no dropped facts, no editorializing.
2. **Preserve register.** If the input is formal, keep it formal — just less floridly formal. If it's casual, keep it casual.
3. **Cut, don't rewrite, when you can.** A lot of slop is *padding*. Deleting "It is important to note that" is usually better than rephrasing it.

## Default output

Return **the rewritten text only**, in the same format as the input (plain text, markdown, etc.). No preamble. No "Here is the rewritten version:". No bullet list of changes.

**Explanation is opt-in.** Only explain what you changed if the user asks ("what did you change", "show me the diff", "explain the edits", "annotate"). If asked, follow with a short bulleted list under a `## Changes` heading — one bullet per category of change, not one per edit.

If the input was so saturated with slop that the rewrite is materially different, end with a single line: `*Heavy rewrite — original meaning preserved but most sentences restructured.*` This warns the user to sanity-check.

## The tells, with how to fix each

These are the patterns that reliably mark AI output. When you spot one, apply the fix. When two or more co-occur in the same paragraph, the paragraph almost certainly needs work even if no single sentence reads badly in isolation.

### 1. Overused vocabulary

A short list of words that have become statistical signatures of LLM output. Their presence isn't damning individually — *clusters* of them in the same passage are. Prefer plainer alternatives unless the word is genuinely the right one.

| Slop word | Plain alternative |
|---|---|
| delve / delve into | look at, examine, get into |
| tapestry / rich tapestry | mix, range, history |
| robust | strong, solid, reliable |
| pivotal | key, central, important |
| crucial | important, necessary |
| vibrant | lively, busy, colourful |
| nestled | located, sits, is in |
| navigate / navigate the complexities of | deal with, handle, work through |
| leverage (as verb) | use |
| underscore / underscores | shows, makes clear |
| testament to | shows, proves |
| meticulous / meticulously | careful, carefully |
| garner | get, attract, win |
| foster / fostering | build, encourage, support |
| showcase | show, display |
| ever-evolving / ever-changing | changing |
| in today's fast-paced world | (delete entirely) |
| landscape (as metaphor: "the AI landscape") | field, world, market, scene |
| interplay | interaction, mix |
| intricate / intricacies | complex, details |
| boast / boasts (meaning "has") | has |
| commitment to | (often delete, or: "works on") |
| diverse array of | range of, mix of |
| groundbreaking | new, important |
| seamless / seamlessly | smooth, smoothly |
| holistic | whole, complete |
| empower / empowering | let, enable, help |
| paradigm shift | big change |
| game-changer / game-changing | important, new |
| at the forefront of | leading, ahead in |
| stands as | is |
| serves as | is, works as |
| myriad | many |
| plethora | lots of, many |
| realm | world, field |

This is not a banned-words list. Use these words when they're the right word. But if a passage stacks four of them in two sentences, that's slop.

### 2. Formulaic sentence constructions

**"It's not just X, it's Y" / "It's not X, it's Y"**

> It's not just a phone, it's a way of life.

The construction itself is the tell. Rewrite as a direct claim:

> It's a phone built around a particular philosophy. *(Or just: "It's a phone with a strong design point of view.")*

**"Not only X, but also Y"**

> The library is not only fast, but also memory-efficient.

Replace with a plain conjunction:

> The library is fast and memory-efficient.

**Copula avoidance** — LLMs often dodge "is" by substituting "serves as", "stands as", "represents", "marks", "embodies":

> The exhibition serves as a testament to the city's enduring creativity.

Replace with the verb the sentence is afraid of:

> The exhibition shows the city's creativity.

**Rule of three** used as filler — three synonymous adjectives, three near-identical clauses. Cut to one if the three say the same thing.

> The product is fast, efficient, and performant. → The product is fast.

### 3. Em-dash overuse

Em-dashes aren't bad. Multiple em-dashes in a short paragraph — especially as the only form of parenthetical punctuation — are a tell. Rules of thumb:

- **0–1 em-dash per paragraph** is normal.
- **2+** is worth checking.
- **3+** is almost certainly AI; replace at least one with parentheses, a comma, or a full stop.

Also watch for the specific construction `clause — short emphatic restatement`, which LLMs over-use:

> This is the future of work — fast, distributed, collaborative.

### 4. Promotional / undue-significance padding

Phrases that inflate ordinary statements into Important Statements:

- "stands as a testament to"
- "represents a watershed moment in"
- "embodies the spirit of"
- "speaks to the broader / deeper"
- "underscores the importance of"
- "highlights the need for"
- "reflects a broader trend toward"
- "is a reminder that"
- "sets the stage for"
- "leaves an indelible mark"

These add no information. Delete the phrase and keep the underlying claim (if there is one).

### 5. Recap intros and "in conclusion" outros

Telltale openers: *"In this article, we'll explore..."*, *"Let's dive into..."*, *"In today's [topic] landscape..."*.

Telltale closers: *"In conclusion,"*, *"All in all,"*, *"To sum up,"*, *"Ultimately,"* (when meaning "in summary"), and the **"Despite challenges, X continues to..."** formula.

Cut these. If the body is good, it doesn't need a recap; if it isn't, a recap won't save it.

### 6. Hedging filler

Phrases that announce a claim instead of just making it:

- "It's worth noting that..."
- "It's important to remember that..."
- "It's interesting to note that..."
- "One could argue that..."
- "It goes without saying that..."
- "Needless to say,"
- "As we all know,"

Delete the phrase. Keep the claim.

### 7. Superficial-analysis tells

Trailing `-ing` clauses tacked onto a noun to imply analysis that isn't there:

> The protocol uses end-to-end encryption, **underscoring its commitment to user privacy.**

> The new tax policy reduces rates, **reflecting a shift in fiscal philosophy.**

These look analytical but say nothing the main clause didn't already imply. Cut the participle phrase.

Same applies to vague attribution: *"experts say"*, *"observers argue"*, *"industry reports suggest"*, *"some critics have noted"*. If there's no source, drop the phrase or replace with a direct claim. If there is one, name it.

### 8. Leftover assistant scaffolding

Bare AI-isms that escape into pasted text:

- "Certainly!" / "Sure!" / "Absolutely!" at the start
- "I hope this helps!" / "Let me know if you have any other questions!" at the end
- "Here's a breakdown:" / "Here's a summary:" preceding the body
- "As an AI language model, I..." (rare but happens)
- "As of my last knowledge update / training data,"
- Mid-text apologies: "I apologize for the confusion."

Delete on sight.

### 9. Formatting tells

**Bullet-and-bold soup** — every other sentence rendered as `- **Bold key**: explanation`. When this happens across a whole section, the user likely wanted prose. Convert short bullets into a paragraph; keep bullets only where a list is genuinely a list (parallel items, three or more, no inherent prose flow).

**Title Case In Every Heading** when the rest of the document is sentence case — flatten to sentence case unless house style says otherwise.

**Excessive bolding** — every key term bolded the first time it's mentioned, like a textbook. Strip to nothing unless the bold has a specific purpose (a UI label, a function name).

**A "## Conclusion" or "## Key Takeaways" section** that just restates the previous sections. Delete it.

### 10. Elegant variation

LLMs avoid repeating a noun in consecutive sentences by reaching for a synonym. Humans usually don't:

> The dog ran across the field. The canine then **leaped** over the fence. The pooch was **enthused**.

If repetition would be clearer than the variation, restore the repetition.

## Things that are **not** slop

Resist the temptation to "fix" these:

- A single em-dash in a paragraph.
- One use of "robust" or "leverage" when it's the right word (sometimes a server really is robust; sometimes you really are leveraging an asset).
- Lists, when the content is genuinely list-shaped.
- Formal register, when the context demands formality (legal, academic, regulatory).
- The Oxford comma, semicolons, or any other punctuation choice that's just a style preference.
- Long sentences. Long sentences are fine. Slop is *empty* sentences, not long ones.

If the input is already clean, return it unchanged and say: `*No changes — text reads as written by a human.*`

## When the user gives you a file

If asked to clean a file (`.md`, `.txt`, `.docx` source), preserve all non-prose elements unchanged: code blocks, frontmatter, tables, image references, links. Only touch the prose. If the prose is intertwined with structural markdown, edit in place and keep the markdown structure.

## Edge cases

- **The user wrote it themselves and is asking for a check.** Same workflow — return the rewrite. Don't apologise or hedge ("This may have been written by a human, but..."). They asked.
- **The user wants only specific fixes** (e.g., "just remove the em-dashes"). Do only that. Don't expand scope.
- **The user pastes very short text** (a single sentence). Still apply the principles. If there's nothing to fix, say so in one line — don't invent problems.
- **The text is a translation or transcription.** Some tells (formal register, slight stiffness) are translation artifacts, not AI tells. Be conservative.
- **The text is intentionally in an AI voice** (parody, satire, a quote of AI output). Ask before editing.

## Example

**Input:**

> In today's rapidly evolving technological landscape, it's not just about building software — it's about crafting experiences that truly resonate with users. Our team's commitment to excellence, combined with our robust engineering practices, serves as a testament to our enduring dedication to delivering groundbreaking solutions. It's worth noting that we leverage cutting-edge technologies to navigate the complexities of modern development. In conclusion, our holistic approach empowers teams to thrive in an ever-changing world.

**Output:**

> We build software people want to use. Our team is good at engineering and we care about the work. We use modern tools because they help us ship.

(Most of the input was empty. The rewrite says what the original would have said if it had been written by someone with nothing to prove.)
