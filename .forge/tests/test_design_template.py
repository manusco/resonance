import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class DesignTemplateTests(unittest.TestCase):
    def test_public_scaffold_matches_canonical_template(self):
        canonical = (ROOT / ".forge/templates/05_design.md").read_bytes()
        public = (ROOT / ".resonance/05_design.md").read_bytes()
        self.assertEqual(public, canonical)

    def test_template_is_optional_and_supports_pointer_adoption(self):
        text = (ROOT / ".forge/templates/05_design.md").read_text(encoding="utf-8")
        self.assertIn("Optional project-owned entry point", text)
        self.assertIn("not a design source or evidence of approval", text)
        self.assertIn("**Status:** [PROPOSED | APPROVED | POINTER]", text)
        self.assertIn("exact path to the maintained canonical source", text)
        self.assertIn("Do not copy its rules here", text)
        self.assertIn("Approved default and reference", text)
        self.assertIn("observable selector", text)

    def test_template_contains_no_resonance_style_decisions(self):
        text = (ROOT / ".forge/templates/05_design.md").read_text(encoding="utf-8").lower()
        for value in ("#3b82f6", "drawer", "toolbar", "neutral palette", "base-8"):
            with self.subTest(value=value):
                self.assertNotIn(value, text)


if __name__ == "__main__":
    unittest.main()
