import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class GoalDoneDoctrineTests(unittest.TestCase):
    def test_done_requires_executed_evidence_without_bypass(self):
        reference = (ROOT / ".forge/skills/ops/goal/references/done_conditions.md").read_text(encoding="utf-8")
        eval_text = (ROOT / ".forge/skills/ops/goal/evals/08_admin_metadata_not_done.json").read_text(encoding="utf-8")
        combined = f"{reference}\n{eval_text}"
        self.assertRegex(combined, r"(?i)executed check|test|validator")
        self.assertIn("dashboard", combined.lower())
        for forbidden in ("continue manually", "ignore stop", "bypass gate", "bypass evidence"):
            self.assertNotIn(forbidden, reference.lower())


if __name__ == "__main__":
    unittest.main()
