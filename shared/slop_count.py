#!/usr/bin/env python3
"""Deterministic countable-tell scorer for the antislop suite.

This is the deterministic tier described in shared/spec.md. It counts only the
COUNTABLE tells (vocabulary-table hits, em-dash density, fixed templates,
bold/bullet soup, fixed scaffolding phrases). Meaning-dependent categories
(padding, elegant variation, contextual register) are left to the LLM judged
tier — this script never guesses at meaning.

Contract: same input + same merged override set => byte-identical JSON output.
Zero third-party dependencies (Python 3 stdlib only). When this script is
absent at runtime, the skill degrades to LLM-only and tags output `unstable`;
this script always emits `stability: "stable"`.

  echo "text" | python3 slop_count.py
  python3 slop_count.py --file doc.md --vocab path/to/overused-vocabulary.md \
      --allow-list a.md --allow-list b.md --extra-vocab c.md

Output: JSON { "findings": [...], "summary": {category: count}, "stability": "stable" }
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

# Fixed per-category severity (mirrors shared/spec.md). A constant label, never
# a tuned weight — so it does not reintroduce the deferred weighted scoring.
SEVERITY = {
    "overused-vocabulary": "low",
    "formulaic-constructions": "high",
    "formatting-tells": "med",
    "scaffolding-and-recap": "high",
}

EM_DASH = "—"

# Fixed templates (formulaic-constructions). Each (rule_id, compiled regex).
TEMPLATE_RULES = [
    ("not-just-x-its-y", re.compile(r"\bit'?s\s+not\s+just\b.*?,\s*it'?s\b", re.I | re.S)),
    ("not-x-its-y", re.compile(r"\bit'?s\s+not\b(?!\s+just).*?,\s*it'?s\b", re.I | re.S)),
    ("not-only-but-also", re.compile(r"\bnot\s+only\b.*?\bbut\s+also\b", re.I | re.S)),
    # Copula substitutions NOT already in the vocab table (serves as / stands as /
    # testament to live there, so they are counted once as overused-vocabulary).
    ("copula-represents-a", re.compile(r"\brepresents\s+a\b", re.I)),
    ("copula-embodies", re.compile(r"\bembodies\b", re.I)),
    ("copula-acts-as", re.compile(r"\bacts\s+as\b", re.I)),
]

# Fixed scaffolding phrases (scaffolding-and-recap).
SCAFFOLD_RULES = [
    ("scaffold-certainly", re.compile(r"^\s*certainly[!,]", re.I | re.M)),
    ("scaffold-hope-helps", re.compile(r"\bI\s+hope\s+this\s+helps\b", re.I)),
    ("scaffold-let-me-know", re.compile(r"\blet\s+me\s+know\s+if\b", re.I)),
    ("scaffold-in-conclusion", re.compile(r"\bin\s+conclusion\b", re.I)),
    ("scaffold-in-summary", re.compile(r"\bin\s+summary\b", re.I)),
]

# Bold-bullet soup: a list item that is `- **Key**: ...`
BOLD_BULLET = re.compile(r"^\s*[-*]\s+\*\*.+?\*\*\s*:", re.M)


def strip_html_comments(text: str) -> str:
    """Remove <!-- ... --> so commented-out example rows never parse as data."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def _table_terms(markdown: str) -> list[str]:
    """Extract the first column of every markdown table row as a slop term.

    Skips the header row and the `|---|` separator. Splits `/`-separated
    variants and drops `(parenthetical)` annotations.
    """
    terms: list[str] = []
    for line in markdown.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells:
            continue
        first = cells[0]
        # skip header / separator / empty
        if not first or set(first) <= set("-: "):
            continue
        if first.lower() in ("slop word", "word", "construction", "phrase"):
            continue
        for variant in first.split("/"):
            variant = re.sub(r"\(.*?\)", "", variant).strip().lower()
            if variant:
                terms.append(variant)
    return terms


def _allow_terms(markdown: str) -> set[str]:
    """Allow-list entries are bullet lines; take the first word of each."""
    out: set[str] = set()
    for line in markdown.splitlines():
        m = re.match(r"^\s*[-*]\s+(.+)$", line)
        if not m:
            continue
        word = m.group(1).strip().split()[0].strip("`*").lower()
        if word:
            out.add(word)
    return out


def load_terms(vocab_path: str, extra_vocab: list[str], allow_lists: list[str]):
    """Build (terms, allow_list). Allow-list wins: allow-listed terms are dropped."""
    terms: list[str] = []
    for p in [vocab_path, *extra_vocab]:
        if p and os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                terms.extend(_table_terms(strip_html_comments(fh.read())))
    allow: set[str] = set()
    for p in allow_lists:
        if p and os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                allow |= _allow_terms(strip_html_comments(fh.read()))
    # dedupe preserving order; allow-list wins (drop if first word is allow-listed)
    seen, kept = set(), []
    for t in terms:
        if t in seen:
            continue
        seen.add(t)
        if t.split()[0] in allow:
            continue
        kept.append(t)
    return kept, allow


def split_paragraphs(text: str) -> list[str]:
    """Blank-line-delimited blocks, excluding fenced code blocks and table rows."""
    lines = text.splitlines()
    kept, in_fence = [], False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            kept.append("")  # fence boundary acts as a separator
            continue
        if in_fence:
            continue
        if line.lstrip().startswith("|"):  # table row
            continue
        kept.append(line)
    blocks, cur = [], []
    for line in kept:
        if line.strip() == "":
            if cur:
                blocks.append("\n".join(cur))
                cur = []
        else:
            cur.append(line)
    if cur:
        blocks.append("\n".join(cur))
    return blocks


def _finding(rule_id, category, idx, quoted, count=1):
    return {
        "rule_id": rule_id,
        "category": category,
        "tier": "deterministic",
        "paragraph_index": idx,
        "quoted_text": quoted[:120],
        "severity": SEVERITY[category],
        "count": count,
        "stability": "stable",
    }


def scan(text: str, terms: list[str]) -> list[dict]:
    findings: list[dict] = []
    paragraphs = split_paragraphs(text)
    for idx, para in enumerate(paragraphs):
        low = para.lower()
        # overused vocabulary. Collect matches, then drop any span fully contained
        # in a longer match so "navigate the complexities of" does not ALSO fire the
        # bare "navigate" (the vocab table splits "/"-variants into both terms).
        vmatches = []  # (start, end, term)
        for term in terms:
            for m in re.finditer(r"(?<!\w)" + re.escape(term) + r"(?!\w)", low):
                vmatches.append((m.start(), m.end(), term))
        vmatches.sort(key=lambda t: (t[0], -(t[1] - t[0])))  # earliest, longest first
        kept = []  # (start, end)
        for s, e, term in vmatches:
            if any(s >= ks and e <= ke for ks, ke in kept):
                continue
            kept.append((s, e))
            # quoted_text is the exact matched term in original case — clean, no
            # mid-word truncation.
            findings.append(_finding("vocab:" + term.replace(" ", "-"),
                                     "overused-vocabulary", idx, para[s:e]))
        # formulaic constructions
        for rule_id, rx in TEMPLATE_RULES:
            for m in rx.finditer(para):
                findings.append(_finding(rule_id, "formulaic-constructions", idx,
                                         m.group(0)))
        # scaffolding
        for rule_id, rx in SCAFFOLD_RULES:
            for m in rx.finditer(para):
                findings.append(_finding(rule_id, "scaffolding-and-recap", idx,
                                         m.group(0)))
        # formatting: em-dash density (2+ in a paragraph is a tell)
        em = para.count(EM_DASH)
        if em >= 2:
            findings.append(_finding("emdash-density", "formatting-tells", idx,
                                     para, count=em))
        # formatting: bold-bullet soup (3+ across a paragraph block)
        bb = len(BOLD_BULLET.findall(para))
        if bb >= 3:
            findings.append(_finding("bold-bullet-soup", "formatting-tells", idx,
                                     para, count=bb))
    return findings


def summarize(findings: list[dict]) -> dict:
    out: dict[str, int] = {}
    for f in findings:
        out[f["category"]] = out.get(f["category"], 0) + f["count"]
    return out


def _default_vocab_path() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "..", "skills", "remove-ai-slop",
                        "references", "overused-vocabulary.md")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="antislop deterministic count tier")
    ap.add_argument("--file", help="read input from this file instead of stdin")
    ap.add_argument("--vocab", default=_default_vocab_path(),
                    help="path to the overused-vocabulary.md table")
    ap.add_argument("--extra-vocab", action="append", default=[],
                    help="additional user/project vocabulary file(s)")
    ap.add_argument("--allow-list", action="append", default=[],
                    help="allow-list file(s); listed words are never counted")
    args = ap.parse_args(argv)

    text = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    terms, _allow = load_terms(args.vocab, args.extra_vocab, args.allow_list)
    findings = scan(text, terms)
    out = {"findings": findings, "summary": summarize(findings), "stability": "stable"}
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
