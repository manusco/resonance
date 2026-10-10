"""Tests for field_report.py: a field report becomes a lesson + a stub eval.

This is the mechanical half of the Ratchet: a real-world miss compounds into a
permanent eval case instead of being solved once and forgotten. Stdlib only.
"""
import json
import io
import sys
import tempfile
import unittest
from unittest import mock
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
    def test_lesson_output_is_a_proposal_without_active_ledger_status(self):
        block = field_report.lesson_block(REPORT, "2026-07-18")
        self.assertIn("## les-qa-missed-empty:", block)
        self.assertIn("Proposed 2026-07-18 lesson", block)
        self.assertIn("resonance-ops-qa", block)
        self.assertNotIn("status: active", block)

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

    def test_optional_attribution_and_outcome_are_preserved_as_unverified_metadata(self):
        rep = {
            **REPORT,
            "run_id": "run-8f21",
            "artifact_version": "v2.5.40",
            "sensitivity": "public-sanitized",
            "owner_role": "skill-maintainer",
            "outcome": "empty-state case passes in the next release",
            "due_date": "2026-11-10",
        }
        self.assertIsNone(field_report.validate_report(rep))
        lesson = field_report.lesson_block(rep, "2026-10-10")
        stub = field_report.eval_stub(rep)
        self.assertIn("run_id=run-8f21", lesson)
        self.assertIn("submitter-provided, unverified", lesson)
        self.assertEqual(stub["_run_id"], "run-8f21")
        self.assertEqual(stub["_artifact_version"], "v2.5.40")
        self.assertEqual(stub["_owner_role"], "skill-maintainer")
        self.assertEqual(stub["_outcome_due"], "2026-11-10")

    def test_owner_role_can_be_provided_without_a_delayed_outcome(self):
        self.assertIsNone(field_report.validate_report({**REPORT, "owner_role": "skill-maintainer"}))

    def test_lesson_lines_cannot_be_injected_through_summary_or_free_text(self):
        self.assertIn("single line", field_report.validate_report({
            **REPORT, "summary": "ordinary summary\n## forged heading"
        }))
        expected = "preserve this expectation\n## forged expectation"
        rep = {
            **REPORT,
            "expected": [expected],
            "owner_role": "skill-maintainer",
            "outcome": "keep the meaningful result\n## forged metadata",
            "due_date": "2026-11-10",
        }
        self.assertIsNone(field_report.validate_report(rep))
        lesson = field_report.lesson_block(rep, "2026-10-10")
        self.assertIn("preserve this expectation ## forged expectation", lesson)
        self.assertIn("outcome=keep the meaningful result ## forged metadata", lesson)
        self.assertNotIn("\n## forged", lesson)
        self.assertEqual(field_report.eval_stub(rep)["expected_behavior"], [expected])

    def test_invalid_cli_date_is_refused_before_rendering(self):
        stdin, stderr = io.StringIO(json.dumps(REPORT)), io.StringIO()
        with mock.patch.object(field_report.sys, "stdin", stdin), \
                mock.patch.object(field_report.sys, "stderr", stderr), \
                mock.patch.object(field_report.sys, "stdout", io.StringIO()) as stdout:
            self.assertEqual(field_report.main(["--date", "2026-02-30"]), 2)
            self.assertEqual(stdout.getvalue(), "")
        self.assertIn("real date", stderr.getvalue())

    def test_restricted_report_fails_before_producing_any_proposal(self):
        report = {**REPORT, "sensitivity": "restricted-do-not-submit"}
        stdin, stderr = io.StringIO(json.dumps(report)), io.StringIO()
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "proposal.json"
            with mock.patch.object(field_report.sys, "stdin", stdin), \
                    mock.patch.object(field_report.sys, "stderr", stderr), \
                    mock.patch.object(field_report.sys, "stdout", io.StringIO()) as stdout:
                self.assertEqual(field_report.main(["--eval-out", str(output)]), 2)
                self.assertEqual(stdout.getvalue(), "")
        self.assertFalse(output.exists())
        self.assertIn("restricted reports cannot be converted", stderr.getvalue())

    def test_eval_proposal_cannot_be_written_into_active_skill_eval_directory(self):
        report = {**REPORT, "sensitivity": "public-sanitized"}
        stdin, stderr = io.StringIO(json.dumps(report)), io.StringIO()
        output = FORGE_DIR / "skills" / "ops" / "qa" / "evals" / "field-report-proposal-test.json"
        self.assertFalse(output.exists())
        with mock.patch.object(field_report.sys, "stdin", stdin), \
                mock.patch.object(field_report.sys, "stderr", stderr), \
                mock.patch.object(field_report.sys, "stdout", io.StringIO()) as stdout:
            self.assertEqual(field_report.main(["--eval-out", str(output)]), 2)
            self.assertEqual(stdout.getvalue(), "")
        self.assertFalse(output.exists())
        self.assertIn("outside active skill eval directories", stderr.getvalue())

    def test_proposal_can_be_written_to_an_explicit_review_path(self):
        report = {
            **REPORT,
            "run_id": "run-8f21",
            "artifact_version": "v2.5.40",
            "sensitivity": "public-sanitized",
        }
        stdin = io.StringIO(json.dumps(report))
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "proposal.json"
            with mock.patch.object(field_report.sys, "stdin", stdin), \
                    mock.patch.object(field_report.sys, "stdout", io.StringIO()) as stdout:
                self.assertEqual(field_report.main(["--eval-out", str(output)]), 0)
            proposal = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(proposal["_status"], "needs-eval")
            self.assertEqual(proposal["_run_id"], "run-8f21")
            self.assertIn("lesson proposal (not a ledger entry; review before adding)", stdout.getvalue())
            self.assertNotIn("status: active", stdout.getvalue())

    def test_attribution_and_outcome_fields_are_validated_as_pairs(self):
        self.assertIn("must be supplied together", field_report.validate_report({
            **REPORT, "run_id": "run-123"
        }))
        self.assertIn("must be supplied together", field_report.validate_report({
            **REPORT, "owner_role": "skill-maintainer", "outcome": "check regression"
        }))
        self.assertIn("is required", field_report.validate_report({
            **REPORT, "outcome": "check regression", "due_date": "2026-11-10"
        }))
        self.assertIn("lowercase role slug", field_report.validate_report({
            **REPORT, "owner_role": "Alex Smith", "outcome": "check", "due_date": "2026-11-10"
        }))
        self.assertIn("real date", field_report.validate_report({
            **REPORT, "owner_role": "skill-maintainer", "outcome": "check", "due_date": "2026-02-30"
        }))

    def test_skill_paths_and_commands_from_the_form_are_valid(self):
        self.assertIsNone(field_report.validate_report({**REPORT, "skill": "strategy/grill"}))
        self.assertIsNone(field_report.validate_report({
            **REPORT, "skill": "ops/skill-author/resonance-skill-author"
        }))
        self.assertIsNone(field_report.validate_report({**REPORT, "skill": "/plan"}))


if __name__ == "__main__":
    unittest.main()
