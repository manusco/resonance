"""Tests for validate_skill.py (stdlib only, no deps).

The eval-floor check runs on every skill, so if it raises instead of reporting an
error, one malformed skill takes down the whole validation run. These tests hold
it to reporting cleanly, and cover the frontmatter parser and the Report API.
"""
import sys
import tempfile
import unittest
from pathlib import Path

# Import the module under test (.forge/validate_skill.py).
FORGE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FORGE_DIR))
import validate_skill  # noqa: E402

SKILL_MD = """---
name: resonance-fixture-floor
description: A fixture skill for the eval-floor regression test. Use when exercising the validator eval-floor path.
archetype: knowledge
---

# fixture floor

Body text so the structure checks have something to read.
"""

EVAL_CASE = '{"skill": "resonance-fixture-floor", "query": "q", "expected_behavior": ["x"]}\n'


def _make_skill(tmp: Path, n_evals: int) -> Path:
    skill_md = tmp / "SKILL.md"
    skill_md.write_text(SKILL_MD, encoding="utf-8")
    evals = tmp / "evals"
    evals.mkdir()
    for i in range(n_evals):
        (evals / f"{i:02d}.json").write_text(EVAL_CASE, encoding="utf-8")
    return skill_md


class EvalFloorTest(unittest.TestCase):
    def test_too_few_evals_reports_not_raises(self):
        """The regression: fewer than 3 evals must produce an error, not raise."""
        with tempfile.TemporaryDirectory() as d:
            skill_md = _make_skill(Path(d), n_evals=2)
            r = validate_skill.Report(str(skill_md))
            # Must not raise (the old bug raised AttributeError here).
            validate_skill.validate(skill_md, r)
            self.assertFalse(r.ok, "a 2-eval skill must fail validation")
            self.assertTrue(
                any("eval" in e.lower() for e in r.errors),
                f"expected an eval-floor error, got: {r.errors}",
            )

    def test_zero_evals_reports_not_raises(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            (tmp / "SKILL.md").write_text(SKILL_MD, encoding="utf-8")
            (tmp / "evals").mkdir()
            skill_md = tmp / "SKILL.md"
            r = validate_skill.Report(str(skill_md))
            validate_skill.validate(skill_md, r)
            self.assertFalse(r.ok)
            self.assertTrue(any("eval" in e.lower() for e in r.errors))

    def test_three_evals_clears_the_floor(self):
        """Exactly 3 evals must not raise the eval-floor error."""
        with tempfile.TemporaryDirectory() as d:
            skill_md = _make_skill(Path(d), n_evals=3)
            r = validate_skill.Report(str(skill_md))
            validate_skill.validate(skill_md, r)
            self.assertFalse(
                any("cannot carry any measurement" in e for e in r.errors),
                f"3 evals should clear the floor, got: {r.errors}",
            )

    def test_report_has_no_error_method(self):
        """Guard the exact typo: Report exposes err/warn, never error."""
        r = validate_skill.Report("x")
        self.assertTrue(hasattr(r, "err"))
        self.assertFalse(hasattr(r, "error"))


class FrontmatterListTest(unittest.TestCase):
    """Frontmatter may carry list-valued fields (invokes:). The parser must
    return them as a list, and must not crash on a bare key that has no value."""

    def test_list_field_parses_without_crash(self):
        text = ("---\nname: resonance-x-y\ndescription: Use when testing lists.\n"
                "archetype: orchestration\ninvokes:\n  - resonance-a-b\n"
                "  - resonance-c-d\n---\n\n# body\n")
        fm, _, _ = validate_skill.split_frontmatter(text)
        self.assertEqual(fm.get("invokes"), ["resonance-a-b", "resonance-c-d"])

    def test_bare_key_stays_empty_string(self):
        text = "---\nname: x\ndescription: y\nnotes:\n---\n\nbody\n"
        fm, _, _ = validate_skill.split_frontmatter(text)
        self.assertEqual(fm.get("notes"), "")


if __name__ == "__main__":
    unittest.main()
