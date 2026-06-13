#!/usr/bin/env python3
"""Tests for scripts/slop_gate.py (stdlib unittest, zero deps).

Discovered by `python -m unittest discover -s shared` alongside the engine tests.
Covers the gate rule (tightened vs spec), report-only vs --enforce exit codes,
allow-list suppression, and IO-error handling.
"""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import slop_gate as gate  # noqa: E402

SCRIPT = os.path.join(HERE, "..", "scripts", "slop_gate.py")
BREACHY = "It's not just a tool, it's a robust solution we leverage."  # formulaic + 2 vocab
CLEAN = "The parser reads each file once and returns a list of words."


def F(category, idx=0):
    return {"category": category, "paragraph_index": idx, "quoted_text": category,
            "rule_id": "x", "severity": "low", "count": 1,
            "tier": "deterministic", "stability": "stable"}


class TestGateRule(unittest.TestCase):
    def test_three_vocab_breaches(self):
        self.assertTrue(gate.paragraph_breaches([F("overused-vocabulary")] * 3))

    def test_two_low_vocab_does_not_breach(self):
        # the key tightening: robust + leverage alone must NOT fail a build
        self.assertEqual(
            gate.paragraph_breaches([F("overused-vocabulary"), F("overused-vocabulary")]), [])

    def test_medhigh_plus_one_breaches(self):
        self.assertTrue(
            gate.paragraph_breaches([F("formulaic-constructions"), F("overused-vocabulary")]))

    def test_single_medhigh_does_not_breach(self):
        self.assertEqual(gate.paragraph_breaches([F("formulaic-constructions")]), [])

    def test_clean_no_breach(self):
        self.assertEqual(gate.paragraph_breaches([]), [])

    def test_rule_is_per_paragraph(self):
        # 2 vocab in para 0, 1 in para 1 -> no paragraph reaches the bar
        f = [F("overused-vocabulary", 0), F("overused-vocabulary", 0),
             F("overused-vocabulary", 1)]
        self.assertEqual(gate.paragraph_breaches(f), [])


class TestScanFile(unittest.TestCase):
    def test_io_error_returns_error_not_breach(self):
        text, findings, err = gate.scan_file("/no/such/file.md", [])
        self.assertIsNone(findings)
        self.assertIsNotNone(err)


class TestCLI(unittest.TestCase):
    def _write(self, body, suffix=".md"):
        fd, path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        return path

    def _run(self, *args):
        return subprocess.run([sys.executable, SCRIPT, *args],
                              capture_output=True, text=True)

    def test_report_only_exits_zero_on_breach(self):
        p = self._write(BREACHY)
        r = self._run(p)
        os.unlink(p)
        self.assertEqual(r.returncode, 0)  # report-only: breaches do not fail

    def test_enforce_exits_one_on_breach(self):
        p = self._write(BREACHY)
        r = self._run("--enforce", p)
        os.unlink(p)
        self.assertEqual(r.returncode, 1)

    def test_enforce_exits_zero_on_clean(self):
        p = self._write(CLEAN)
        r = self._run("--enforce", p)
        os.unlink(p)
        self.assertEqual(r.returncode, 0)

    def test_missing_file_exits_two(self):
        r = self._run("--enforce", "/no/such/x.md")
        self.assertEqual(r.returncode, 2)

    def test_allow_list_suppresses_breach(self):
        p = self._write("We use a robust, seamless, vibrant approach.")  # 3 vocab
        allow = self._write("- robust\n- seamless\n- vibrant\n")
        r = self._run("--enforce", "--allow-list", allow, p)
        os.unlink(p)
        os.unlink(allow)
        self.assertEqual(r.returncode, 0)  # all three allow-listed -> no breach


if __name__ == "__main__":
    unittest.main()
