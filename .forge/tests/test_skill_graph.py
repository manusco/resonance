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


if __name__ == "__main__":
    unittest.main()
