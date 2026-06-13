#!/usr/bin/env python3
"""Validate every skills/*/SKILL.md YAML frontmatter.

Guards against the v0.2.0 break: an unquoted colon-space in the `description`
made YAML read a nested mapping ("mapping values are not allowed in this
context") and the skill would not load. CI runs this so that class of error
cannot reach main again.

Uses PyYAML when available (a real parse, as CI does after `pip install pyyaml`).
Falls back to a heuristic when PyYAML is absent so it still runs locally with
zero dependencies. Exits non-zero on the first failure.

  python3 scripts/check_frontmatter.py
"""
from __future__ import annotations

import glob
import os
import re
import sys

try:
    import yaml  # type: ignore
    HAVE_YAML = True
except Exception:
    HAVE_YAML = False

REQUIRED_KEYS = ("name", "description")


def frontmatter(text: str) -> str | None:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else None


def check(path: str) -> list[str]:
    fm = frontmatter(open(path, encoding="utf-8").read())
    if fm is None:
        return ["no YAML frontmatter found"]
    errors: list[str] = []
    if HAVE_YAML:
        try:
            data = yaml.safe_load(fm)
        except yaml.YAMLError as e:  # the exact failure class we are guarding
            return [f"YAML parse error: {e}"]
        if not isinstance(data, dict):
            return ["frontmatter is not a mapping"]
        for key in REQUIRED_KEYS:
            if key not in data:
                errors.append(f"missing required key: {key}")
    else:
        keys = set()
        for i, line in enumerate(fm.splitlines(), 1):
            m = re.match(r"^(\w[\w-]*):\s+(.*)$", line)
            if not m:
                continue
            keys.add(m.group(1))
            value = m.group(2)
            if value[:1] not in ('"', "'") and ": " in value:
                col = value.index(": ")
                errors.append(
                    f"line {i}: unquoted colon-space in '{m.group(1)}' value "
                    f"(near col {col}) — wrap the value in quotes or remove the colon")
        for key in REQUIRED_KEYS:
            if key not in keys:
                errors.append(f"missing required key: {key}")
    return errors


def main() -> int:
    paths = sorted(glob.glob("skills/*/SKILL.md"))
    if not paths:
        print("no skills/*/SKILL.md found", file=sys.stderr)
        return 1
    failed = False
    for path in paths:
        errs = check(path)
        if errs:
            failed = True
            print(f"FAIL {path}")
            for e in errs:
                print(f"     - {e}")
        else:
            print(f"OK   {path}")
    print(f"\nparser: {'PyYAML' if HAVE_YAML else 'heuristic (PyYAML not installed)'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
