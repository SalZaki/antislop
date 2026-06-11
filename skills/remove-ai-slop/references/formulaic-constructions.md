# Formulaic sentence constructions

The constructions themselves are the tell, regardless of what they're describing.

## "It's not just X, it's Y" / "It's not X, it's Y"

> It's not just a phone, it's a way of life.

The construction itself is the tell. Rewrite as a direct claim:

> It's a phone built around a particular philosophy.
> *(Or just: "It's a phone with a strong design point of view.")*

## "Not only X, but also Y"

> The library is not only fast, but also memory-efficient.

Replace with a plain conjunction:

> The library is fast and memory-efficient.

## Copula avoidance

LLMs often dodge "is" by substituting `serves as`, `stands as`, `represents`, `marks`, `embodies`:

> The exhibition serves as a testament to the city's enduring creativity.

Replace with the verb the sentence is afraid of:

> The exhibition shows the city's creativity.

Common substitutions to flatten back to `is` / `shows` / `proves`:

- `serves as` → is, works as
- `stands as` → is
- `represents a` → is, marks, makes
- `marks a` → is
- `embodies` → is, shows
- `acts as` → is

## Rule of three used as filler

Three synonymous adjectives, three near-identical clauses. Cut to one if the three say the same thing.

> The product is fast, efficient, and performant.

→ The product is fast.

The rule of three is fine when each item adds genuinely different information. It's slop when the three are reaching for the same idea.

## Custom additions

The default constructions above are the most common, but user overrides under `overrides/user-vocabulary.md` can add construction patterns the user wants flagged. Same merge rule applies: allow-list always wins.
