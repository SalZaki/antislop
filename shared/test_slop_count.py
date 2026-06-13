#!/usr/bin/env python3
"""Deterministic-tier tests for slop_count.py (stdlib unittest, zero deps).

Run: python3 -m unittest discover -s shared
These cover every countable codepath plus the false-positive guard and the
determinism contract from shared/spec.md.
"""
import json
import os
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slop_count as sc  # noqa: E402

VOCAB = sc._default_vocab_path()
TERMS, _ = sc.load_terms(VOCAB, [], [])


def cats(findings):
    return [f["category"] for f in findings]


class TestParagraphSplit(unittest.TestCase):
    def test_blank_line_blocks(self):
        self.assertEqual(len(sc.split_paragraphs("a\n\nb\n\nc")), 3)

    def test_excludes_code_fence(self):
        text = "real prose with delve\n\n```\ndelve delve delve\n```\n"
        paras = sc.split_paragraphs(text)
        self.assertTrue(all("delve delve delve" not in p for p in paras))

    def test_excludes_table_rows(self):
        text = "prose\n\n| delve | x |\n| --- | --- |\n"
        paras = sc.split_paragraphs(text)
        self.assertTrue(all("|" not in p for p in paras))


class TestVocab(unittest.TestCase):
    def test_detects_delve(self):
        f = sc.scan("Let us delve into the topic.", TERMS)
        self.assertIn("overused-vocabulary", cats(f))

    def test_case_insensitive(self):
        self.assertTrue(sc.scan("DELVE into it", TERMS))

    def test_word_boundary_no_substring(self):
        # "robustness" should not match the term "robust"
        f = [x for x in sc.scan("the robustness of it", TERMS)
             if x["rule_id"] == "vocab:robust"]
        self.assertEqual(f, [])

    def test_code_fence_vocab_not_counted(self):
        f = sc.scan("clean line\n\n```\ndelve delve\n```", TERMS)
        self.assertEqual(cats(f), [])

    def test_no_double_count_on_overlapping_phrase(self):
        # "navigate the complexities of" must not ALSO fire bare "navigate"
        f = [x for x in sc.scan("we navigate the complexities of compliance", TERMS)
             if x["category"] == "overused-vocabulary"]
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0]["rule_id"], "vocab:navigate-the-complexities-of")

    def test_quoted_text_is_clean_term(self):
        # "delve here" (no "into") so only the bare term matches
        f = [x for x in sc.scan("we delve here", TERMS)
             if x["rule_id"] == "vocab:delve"]
        self.assertEqual(f[0]["quoted_text"], "delve")  # no trailing truncation

    def test_longer_phrase_wins_over_bare_term(self):
        f = [x for x in sc.scan("let us delve into the topic", TERMS)
             if x["category"] == "overused-vocabulary"]
        self.assertEqual([x["rule_id"] for x in f], ["vocab:delve-into"])


class TestAllowList(unittest.TestCase):
    def test_allow_list_suppresses_robust(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
            fh.write("## allow\n- robust\n")
            allow_path = fh.name
        terms, allow = sc.load_terms(VOCAB, [], [allow_path])
        os.unlink(allow_path)
        self.assertIn("robust", allow)
        self.assertNotIn("robust", terms)
        f = sc.scan("a robust and reliable system", terms)
        self.assertEqual([x for x in f if x["rule_id"] == "vocab:robust"], [])

    def test_strips_html_comments(self):
        # commented-out rows must not parse as live data
        md = "## x\n<!--\n- robust\n-->\n- crucial\n"
        allow = sc._allow_terms(sc.strip_html_comments(md))
        self.assertIn("crucial", allow)
        self.assertNotIn("robust", allow)


class TestFormatting(unittest.TestCase):
    def test_emdash_density(self):
        f = sc.scan("This is the future — fast — distributed — collaborative.", TERMS)
        em = [x for x in f if x["rule_id"] == "emdash-density"]
        self.assertEqual(len(em), 1)
        self.assertGreaterEqual(em[0]["count"], 2)

    def test_single_emdash_ok(self):
        f = sc.scan("A normal sentence — with one aside.", TERMS)
        self.assertEqual([x for x in f if x["rule_id"] == "emdash-density"], [])

    def test_bold_bullet_soup(self):
        text = "- **One**: a\n- **Two**: b\n- **Three**: c"
        f = sc.scan(text, TERMS)
        self.assertTrue([x for x in f if x["rule_id"] == "bold-bullet-soup"])


class TestTemplates(unittest.TestCase):
    def test_not_just_x_its_y(self):
        f = sc.scan("It's not just a phone, it's a way of life.", TERMS)
        self.assertIn("formulaic-constructions", cats(f))

    def test_not_only_but_also(self):
        f = sc.scan("The library is not only fast but also memory-efficient.", TERMS)
        self.assertIn("formulaic-constructions", cats(f))


class TestScaffolding(unittest.TestCase):
    def test_in_conclusion(self):
        f = sc.scan("In conclusion, we shipped it.", TERMS)
        self.assertIn("scaffolding-and-recap", cats(f))


class TestFalsePositiveGuard(unittest.TestCase):
    def test_clean_prose_scores_zero(self):
        clean = ("The parser reads each file once and returns a list of words. "
                 "If a file is missing it is skipped. Tests cover the empty case.")
        self.assertEqual(sc.scan(clean, TERMS), [])

    def test_allow_list_active_scores_zero(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
            fh.write("- robust\n- leverage\n")
            allow_path = fh.name
        terms, _ = sc.load_terms(VOCAB, [], [allow_path])
        os.unlink(allow_path)
        text = "We leverage a robust pipeline."
        bad = [x for x in sc.scan(text, terms)
               if x["rule_id"] in ("vocab:robust", "vocab:leverage")]
        self.assertEqual(bad, [])


class TestDeterminism(unittest.TestCase):
    def test_same_input_same_output(self):
        text = "Let us delve into this robust, ever-evolving tapestry."
        a = sc.scan(text, TERMS)
        b = sc.scan(text, TERMS)
        self.assertEqual(a, b)

    def test_cli_emits_stable_json(self):
        proc = subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(__file__), "slop_count.py")],
            input="Let us delve into the tapestry.", capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        self.assertEqual(out["stability"], "stable")
        self.assertIn("overused-vocabulary", out["summary"])


class TestSummary(unittest.TestCase):
    def test_summary_aggregates_counts_by_category(self):
        text = ("Let us delve into the robust tapestry. In conclusion, "
                "it's not just X, it's Y.")
        findings = sc.scan(text, TERMS)
        summary = sc.summarize(findings)
        for cat in summary:
            self.assertEqual(
                summary[cat],
                sum(f["count"] for f in findings if f["category"] == cat))
        self.assertIn("overused-vocabulary", summary)
        self.assertIn("scaffolding-and-recap", summary)

    def test_summary_empty_for_clean_text(self):
        self.assertEqual(sc.summarize(sc.scan("A plain, clear sentence.", TERMS)), {})


if __name__ == "__main__":
    unittest.main()
