import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class SystemsTemplateTests(unittest.TestCase):
    def test_public_scaffold_matches_canonical_template(self):
        canonical = (ROOT / ".forge/templates/04_systems.md").read_bytes()
        scaffold = (ROOT / ".resonance/04_systems.md").read_bytes()
        self.assertEqual(canonical, scaffold)

    def test_template_preserves_constitution_contract(self):
        text = (ROOT / ".forge/templates/04_systems.md").read_text()
        required = (
            "# Part I: Architecture constitution",
            "# Part II: System record",
            "**Approval evidence:**",
            "A current implementation fact becomes",
            "| SYS-### | Success and failure semantics |",
            "| Rule ID | Constraint | Why it is binding | Accountable role or group | Verification |",
            "| Rule ID | Rank | Concern | Decision rule | Accountable role or group |",
            "### Five-minute orientation",
            "### Domain vocabulary",
            "Screen every approved implementation plan before `/build`",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, text)
        self.assertLess(
            text.index("# Part I: Architecture constitution"),
            text.index("# Part II: System record"),
        )


if __name__ == "__main__":
    unittest.main()
