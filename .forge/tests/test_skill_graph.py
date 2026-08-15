"""Freshness test for the rendered skill-dependency graph (stdlib only).

docs/SKILL_GRAPH.md is generated from the invokes: frontmatter. If someone adds
or renames an edge and forgets to regenerate, this fails, the same way doc_drift
guards the command counts. Runs from the repo root (tests/run.py and the ship
gate both do).
"""
import sys
import unittest
from pathlib import Path

FORGE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FORGE_DIR))
import skill_graph  # noqa: E402
from kernel import manifest as skill_manifest  # noqa: E402


class SkillGraphTest(unittest.TestCase):
    def test_doc_is_fresh(self):
        out = Path("docs/SKILL_GRAPH.md")
        self.assertTrue(out.is_file(),
                        "docs/SKILL_GRAPH.md missing; run: py .forge/skill_graph.py")
        self.assertEqual(
            out.read_text(encoding="utf-8"), skill_graph.render(),
            "docs/SKILL_GRAPH.md is out of date; run: py .forge/skill_graph.py")

    def test_core_orchestrator_present(self):
        edges = dict(skill_graph.collect())
        self.assertIn("resonance-ops-goal", edges)
        self.assertIn("resonance-engineering-build", edges["resonance-ops-goal"])

    def test_manifest_contracts_are_valid(self):
        data = skill_manifest.manifest()
        self.assertGreaterEqual(len(data), 60)
        self.assertEqual([], skill_manifest.validate(data))

    def test_orchestration_contracts_are_declared(self):
        data = skill_manifest.manifest()
        orchestrators = [entry for entry in data if entry["archetype"] == "orchestration"]
        self.assertGreaterEqual(len(orchestrators), 9)
        for entry in orchestrators:
            with self.subTest(skill=entry["id"]):
                self.assertEqual("consequential", entry["authority"])
                self.assertEqual("stop", entry["failure_policy"])
                self.assertTrue(entry["invokes"])
                self.assertIn("may_coordinate_work", entry["side_effects"])

    def test_cycles_are_rejected(self):
        data = [
            {
                "schema_version": 1,
                "id": "resonance-a",
                "path": "a/SKILL.md",
                "archetype": "orchestration",
                "owner": "a",
                "activation": "manual",
                "authority": "consequential",
                "triggers": ["a"],
                "negative_triggers": [],
                "inputs": ["user_request"],
                "outputs": ["plan"],
                "invokes": ["resonance-b"],
                "side_effects": ["may_coordinate_work"],
                "write_sets": [],
                "failure_policy": "stop",
            },
            {
                "schema_version": 1,
                "id": "resonance-b",
                "path": "b/SKILL.md",
                "archetype": "orchestration",
                "owner": "b",
                "activation": "manual",
                "authority": "consequential",
                "triggers": ["b"],
                "negative_triggers": [],
                "inputs": ["user_request"],
                "outputs": ["plan"],
                "invokes": ["resonance-a"],
                "side_effects": ["may_coordinate_work"],
                "write_sets": [],
                "failure_policy": "stop",
            },
        ]
        self.assertTrue(any("cycle detected" in issue for issue in skill_manifest.validate(data)))


if __name__ == "__main__":
    unittest.main()
