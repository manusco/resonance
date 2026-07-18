"""Tests for field_report.py: a field report becomes a lesson + a stub eval.

This is the mechanical half of the Ratchet: a real-world miss compounds into a
permanent eval case instead of being solved once and forgotten. Stdlib only.
"""
import json
import sys
import unittest
from pathlib import Path

FORGE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FORGE_DIR))
import field_report  # noqa: E402

REPORT = {
    "skill": "resonance-ops-qa",
    "id": "qa-missed-empty",
    "summary": "qa skipped the zero-item path",
    "scenario": "list view with zero items rendered nothing and no test covered it",
    "expected": ["cover the zero-item edge", "write a failing test for the empty state first"],
}


class FieldReportTest(unittest.TestCase):
    def test_lesson_block_is_a_valid_ledger_entry(self):
        block = field_report.lesson_block(REPORT, "2026-07-18")
        self.assertIn("## les-qa-missed-empty:", block)
        self.assertIn("type: lesson", block)
        self.assertIn("created: 2026-07-18", block)
        self.assertIn("resonance-ops-qa", block)

    def test_eval_stub_has_required_fields(self):
        stub = field_report.eval_stub(REPORT)
        self.assertEqual(stub["skill"], "resonance-ops-qa")
        self.assertTrue(stub["query"])
        self.assertEqual(stub["expected_behavior"], REPORT["expected"])
        self.assertEqual(stub["_status"], "needs-eval")

    def test_stub_serializes_dash_free_but_decodes_to_dashes(self):
        stub = field_report.eval_stub(REPORT)
        text = json.dumps(stub, ensure_ascii=True, indent=2)
        # no literal dash bytes in the file text
        self.assertEqual(text.count(chr(0x2014)) + text.count(chr(0x2013)), 0)
        # but the parsed check still targets the dash character class
        back = json.loads(text)
        self.assertIn(chr(0x2014), back["checks"][0]["value"])

    def test_slug_is_clean(self):
        self.assertEqual(field_report._slug("QA missed: the Empty!! path"), "qa-missed-the-empty-path")
        self.assertEqual(field_report._slug(""), "field-report")

    def test_id_falls_back_to_summary_slug(self):
        rep = {"skill": "resonance-ops-qa", "summary": "No id given here", "expected": ["x"]}
        block = field_report.lesson_block(rep, "2026-07-18")
        self.assertIn("## les-no-id-given-here:", block)


if __name__ == "__main__":
    unittest.main()
