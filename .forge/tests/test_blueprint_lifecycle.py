import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class BlueprintLifecycleTests(unittest.TestCase):
    def source(self, path):
        return (ROOT / ".forge/skills" / path / "skill.tmpl.md").read_text(encoding="utf-8")

    def test_material_architecture_changes_are_checked_at_delivery_gates(self):
        for path in ("strategy/plan", "ops/reviewer", "ops/audit", "ops/ship"):
            with self.subTest(path=path):
                text = self.source(path)
                self.assertIn(".resonance/04_systems.md", text)
                self.assertIn("/blueprint check", text)
                self.assertIn("SYS-*", text)

    def test_local_changes_can_skip_with_evidence(self):
        for path in ("strategy/plan", "ops/reviewer", "ops/audit", "ops/ship"):
            with self.subTest(path=path):
                text = self.source(path).lower()
                self.assertIn("local", text)
                self.assertIn("skip", text)

    def test_audit_uses_canonical_severity_for_blueprint_drift(self):
        text = self.source("ops/audit")
        self.assertIn("resonance-strategy-blueprint", text)
        self.assertIn("same P0-P3 taxonomy", text)


if __name__ == "__main__":
    unittest.main()
