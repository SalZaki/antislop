#!/usr/bin/env python3
"""Report-first slop gate over the deterministic scorer (Direction C).

Runs the shared/slop_count.py engine over the given markdown files, groups
findings per paragraph, and reports paragraphs that cluster slop. Report-only by
default (exit 0 even on breaches); pass --enforce to exit 1 on any breach, which
is the one-line flip from advisory to a blocking required check.

Gate rule (deliberately STRICTER than spec.md's rewrite-lens forced-action rule,
to avoid false-positive fatigue in CI — a red build is not a cheap nudge): a
paragraph BREACHES when it has
    (>=1 med/high-severity tell AND >=2 tells total)  OR  (>=3 overused-vocabulary tells)
A "tell" is one finding object (NOT the summed summary counts: em-dash density is
one finding carrying count=2). Two low-severity vocab words (robust + leverage)
do NOT breach; they stay advisory.

Zero third-party dependencies. The scorer stays a pure exit-0 reporter; only this
wrapper carries a verdict.

  python3 scripts/slop_gate.py [FILES...] [--paths-from list.txt] [--enforce]
      [--format text|github] [--vocab P] [--extra-vocab P]... [--allow-list P]...

Exit: 0 = clean OR report-only; 1 = breach AND --enforce; 2 = IO/usage error.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
import slop_count as sc  # noqa: E402

# Categories that may carry a blocking verdict (mirrors the fixed severities in
# shared/spec.md: formulaic + scaffolding = high, formatting = med).
MED_HIGH = {"formulaic-constructions", "scaffolding-and-recap", "formatting-tells"}

PARA_TELL_THRESHOLD = 2   # >=2 tells in a paragraph, when one is med/high
PARA_VOCAB_THRESHOLD = 3  # >=3 overused-vocabulary tells in a paragraph


def paragraph_breaches(findings: list[dict]) -> list[tuple[int, str, list[dict]]]:
    """Paragraphs that breach the gate rule, as (paragraph_index, reason, findings)."""
    by_para: dict[int, list[dict]] = {}
    for f in findings:
        by_para.setdefault(f["paragraph_index"], []).append(f)
    out = []
    for idx in sorted(by_para):
        fs = by_para[idx]
        vocab = [f for f in fs if f["category"] == "overused-vocabulary"]
        med_high = [f for f in fs if f["category"] in MED_HIGH]
        if med_high and len(fs) >= PARA_TELL_THRESHOLD:
            out.append((idx, f"{len(fs)} tells incl. {med_high[0]['category']}", fs))
        elif len(vocab) >= PARA_VOCAB_THRESHOLD:
            out.append((idx, f"{len(vocab)} vocabulary tells", fs))
    return out


def scan_file(path: str, terms: list[str]):
    """Returns (text, findings, error). error is non-None on IO/decode failure."""
    try:
        text = open(path, encoding="utf-8").read()
    except (OSError, UnicodeDecodeError) as e:
        return None, None, str(e)
    return text, sc.scan(text, terms), None


def _line_of(text: str, quoted: str) -> int:
    """1-based line of the first occurrence of quoted text (paragraph_index is not a line)."""
    idx = text.find(quoted)
    return text.count("\n", 0, idx) + 1 if idx >= 0 else 1


def _samples(fs: list[dict], n: int = 3) -> str:
    return "; ".join(f["quoted_text"] for f in fs[:n])


def report(results, fmt: str) -> None:
    """results: list of (path, text, breaches)."""
    total = sum(len(b) for _, _, b in results)
    if fmt == "github":
        lines = ["## Slop gate (report-only)\n"]
        if not results:
            lines.append("No slop clusters in the changed markdown.\n")
        else:
            lines.append(
                f"{total} paragraph(s) over the gate threshold across {len(results)} "
                "file(s). Advisory only, not failing the build.\n")
            lines += ["| File | Para | Why | Sample |", "|---|---|---|---|"]
            annotated = 0
            for path, text, breaches in results:
                for idx, reason, fs in breaches:
                    sample = _samples(fs).replace("|", r"\|")
                    lines.append(f"| `{path}` | {idx} | {reason} | {sample} |")
                    if annotated < 10:  # GitHub shows ~10 annotations/type; cap + collapse
                        msg = f"slop cluster: {reason} ({_samples(fs)})"
                        print(f"::warning file={path},line={_line_of(text, fs[0]['quoted_text'])},"
                              f"title=slop-gate::{msg}")
                        annotated += 1
            if total > 10:
                lines.append(f"\n_{total - 10} more not annotated inline (annotation cap); see table above._")
        out = "\n".join(lines) + "\n"
        summary = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary:
            with open(summary, "a", encoding="utf-8") as fh:
                fh.write(out)
        else:
            print(out)
    else:
        if not results:
            print("slop-gate: no clusters over threshold in the changed markdown.")
        for path, text, breaches in results:
            for idx, reason, fs in breaches:
                print(f"{path}: para {idx}: {reason} -- {_samples(fs)}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="antislop CI slop gate (report-first)")
    ap.add_argument("paths", nargs="*", help="markdown files to check")
    ap.add_argument("--paths-from", help="read newline-separated file paths from here")
    ap.add_argument("--vocab", default=sc._default_vocab_path())
    ap.add_argument("--extra-vocab", action="append", default=[])
    ap.add_argument("--allow-list", action="append", default=[])
    ap.add_argument("--enforce", action="store_true",
                    help="exit 1 on a breach (blocking). Default: report-only, exit 0.")
    ap.add_argument("--format", choices=["text", "github"], default="text")
    args = ap.parse_args(argv)

    paths = list(args.paths)
    if args.paths_from:
        try:
            with open(args.paths_from, encoding="utf-8") as fh:
                paths += [ln.strip() for ln in fh if ln.strip()]
        except OSError as e:
            print(f"slop-gate: cannot read --paths-from {args.paths_from}: {e}", file=sys.stderr)
            return 2
    if not paths:
        print("slop-gate: no files to check.")
        return 0

    terms, _ = sc.load_terms(args.vocab, args.extra_vocab, args.allow_list)
    results, io_error = [], False
    for p in paths:
        text, findings, err = scan_file(p, terms)
        if err is not None:  # IO/decode error is exit 2, never a fake breach
            print(f"slop-gate: cannot read {p}: {err}", file=sys.stderr)
            io_error = True
            continue
        breaches = paragraph_breaches(findings)
        if breaches:
            results.append((p, text, breaches))

    report(results, args.format)
    if io_error:
        return 2
    if results and args.enforce:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
