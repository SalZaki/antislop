# Overused vocabulary

Words that have become statistical signatures of LLM output. Their presence isn't damning individually — *clusters* of them in the same passage are. Prefer plainer alternatives unless the word is genuinely the right one.

## Default table

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
| landscape (as metaphor) | field, world, market, scene |
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

## Co-occurrence rule

This is not a banned-words list. Use these words when they're the right word.

**Threshold for forced action (unified rule, see `../../../shared/spec.md`):** rewrite a paragraph when 3+ words from this table appear in it, OR when 2+ tells of any category co-occur in it — even if individually each use looks defensible.
