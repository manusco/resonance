import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class NecessityLifecycleTests(unittest.TestCase):
    def source(self, path):
        return (ROOT / ".forge/skills" / path / "skill.tmpl.md").read_text(encoding="utf-8")

    def test_refactor_review_and_ship_share_one_protocol(self):
        for path in ("ops/refactor", "ops/reviewer", "ops/ship"):
            with self.subTest(path=path):
                text = self.source(path)
                self.assertIn("Necessity Protocol", text)
                self.assertIn("../core/references/necessity_protocol.md", text)

    def test_order_prefers_existing_lower_layers_before_new_code(self):
        protocol = (ROOT / ".forge/skills/ops/core/references/necessity_protocol.md").read_text(encoding="utf-8")
        terms = (
            "Delete or decline",
            "Reuse the codebase",
            "Use the language runtime",
            "Use the native platform",
            "Use an installed dependency",
            "Write the smallest local implementation",
        )
        positions = [protocol.index(term) for term in terms]
        self.assertEqual(sorted(positions), positions)

    def test_root_lock_links_to_canonical_protocol_and_matches_resolver(self):
        root_lock = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        resolver = (ROOT / ".forge/resolvers/locks.md").read_text(encoding="utf-8")
        link = ".agents/skills/ops/core/references/necessity_protocol.md"
        self.assertTrue((ROOT / link).is_file())
        self.assertNotIn(".forge/skills/ops/core/references/necessity_protocol.md", root_lock)
        self.assertIn(f"]({link})", root_lock)
        root_rule = next(line for line in root_lock.splitlines() if line.startswith("- **Simplicity.**"))
        resolver_rule = next(line for line in resolver.splitlines() if line.startswith("- **Simplicity.**"))
        root_rule = root_rule.replace(f"[shared Necessity Protocol]({link})", "shared Necessity Protocol")
        self.assertEqual(root_rule.lower(), resolver_rule.lower())

    def test_safety_and_canonical_severity_survive_simplification(self):
        protocol = (ROOT / ".forge/skills/ops/core/references/necessity_protocol.md").read_text(encoding="utf-8")
        for protected in ("validation", "authorization", "accessibility", "data loss", "observability", "tests"):
            with self.subTest(protected=protected):
                self.assertIn(protected.lower(), protocol.lower())
        reviewer = self.source("ops/reviewer")
        self.assertIn("canonical taxonomy", reviewer)
        self.assertIn("P0-P3", reviewer)


if __name__ == "__main__":
    unittest.main()
