"""Tests for validate_skill.py (stdlib only, no deps).

The eval-floor check runs on every skill, so if it raises instead of reporting an
error, one malformed skill takes down the whole validation run. These tests hold
it to reporting cleanly, and cover the frontmatter parser and the Report API.
"""
import subprocess
import json
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
    tmp.mkdir(parents=True, exist_ok=True)
    skill_md = tmp / "SKILL.md"
    skill_md.write_text(SKILL_MD, encoding="utf-8")
    evals = tmp / "evals"
    evals.mkdir()
    for i in range(n_evals):
        (evals / f"{i:02d}.json").write_text(EVAL_CASE, encoding="utf-8")
    return skill_md


class EvalFloorTest(unittest.TestCase):
    def test_alias_validation_resolves_manifest_when_called_outside_repo(self):
        skill_md = FORGE_DIR.parent / ".agents/skills/software/deliver-change/SKILL.md"
        with tempfile.TemporaryDirectory() as cwd:
            result = subprocess.run(
                [sys.executable, str(FORGE_DIR / "validate_skill.py"), str(skill_md), "--strict"],
                cwd=cwd, capture_output=True, text=True, check=False,
            )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_too_few_evals_reports_not_raises(self):
        """Fewer than 6 evals must produce an error, not raise."""
        with tempfile.TemporaryDirectory() as d:
            skill_md = _make_skill(Path(d), n_evals=5)
            r = validate_skill.Report(str(skill_md))
            # Must not raise (the old bug raised AttributeError here).
            validate_skill.validate(skill_md, r)
            self.assertFalse(r.ok, "a 5-eval skill must fail validation")
            self.assertTrue(
                any("evals: found 5 case(s)" in e and ">= 6 golden" in e for e in r.errors),
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

    def test_six_evals_clears_the_floor(self):
        """Exactly 6 evals must not raise the eval-floor error."""
        with tempfile.TemporaryDirectory() as d:
            skill_md = _make_skill(Path(d), n_evals=6)
            r = validate_skill.Report(str(skill_md))
            validate_skill.validate(skill_md, r)
            self.assertFalse(
                any(e.startswith("evals:") for e in r.errors),
                f"6 evals should clear the floor, got: {r.errors}",
            )

    def test_framework_manifest_applies_six_case_floor_only_to_owned_skills(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            owned = root / ".agents/skills/framework/SKILL.md"
            owned_short = root / ".agents/skills/framework-short/SKILL.md"
            private = root / ".agents/skills/company/SKILL.md"
            private_short = root / ".agents/skills/company-short/SKILL.md"
            for skill_md, count in ((owned, 6), (owned_short, 5), (private, 3), (private_short, 2)):
                skill_md.parent.mkdir(parents=True)
                skill_md.write_text(SKILL_MD, encoding="utf-8")
                evals = skill_md.parent / "evals"
                evals.mkdir()
                for i in range(count):
                    (evals / f"{i:02d}.json").write_text(EVAL_CASE, encoding="utf-8")
            manifest = root / ".resonance/framework-manifest.json"
            manifest.parent.mkdir()
            manifest.write_text(
                json.dumps({"schema": 1, "files": {
                    ".agents/skills/framework/SKILL.md": "0" * 64,
                    ".agents/skills/framework-short/SKILL.md": "1" * 64,
                }}),
                encoding="utf-8",
            )

            owned_report = validate_skill.validate(owned, validate_skill.Report(str(owned)))
            owned_short_report = validate_skill.validate(owned_short, validate_skill.Report(str(owned_short)))
            private_report = validate_skill.validate(private, validate_skill.Report(str(private)))
            private_short_report = validate_skill.validate(private_short, validate_skill.Report(str(private_short)))

            self.assertFalse(any(e.startswith("evals:") for e in owned_report.errors))
            self.assertTrue(any("evals: found 5 case(s)" in e and ">= 6 golden" in e for e in owned_short_report.errors))
            self.assertFalse(any(e.startswith("evals:") for e in private_report.errors))
            self.assertTrue(any("evals: found 2 case(s)" in e and ">= 3 golden" in e for e in private_short_report.errors))

    def test_malformed_framework_manifest_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            skill_md = root / ".agents/skills/company/SKILL.md"
            _make_skill(skill_md.parent, n_evals=3)
            manifest = root / ".resonance/framework-manifest.json"
            manifest.parent.mkdir()
            manifest.write_text('{"schema": 1, "files": {}}', encoding="utf-8")
            report = validate_skill.validate(skill_md, validate_skill.Report(str(skill_md)))
            self.assertTrue(any("ownership: invalid framework manifest" in e for e in report.errors))
            self.assertTrue(any("evals: found 3 case(s)" in e and ">= 6 golden" in e for e in report.errors))

    def test_invalid_utf8_framework_manifest_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            skill_md = root / ".agents/skills/company/SKILL.md"
            _make_skill(skill_md.parent, n_evals=3)
            manifest = root / ".resonance/framework-manifest.json"
            manifest.parent.mkdir()
            manifest.write_bytes(b"\xff")
            report = validate_skill.validate(skill_md, validate_skill.Report(str(skill_md)))
            self.assertTrue(any("ownership: invalid framework manifest" in e for e in report.errors))
            self.assertTrue(any("evals: found 3 case(s)" in e and ">= 6 golden" in e for e in report.errors))

    def test_consumer_manifest_does_not_weaken_nested_source_skill_floor(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            skill_md = root / ".forge/skills/example/SKILL.md"
            _make_skill(skill_md.parent, n_evals=3)
            manifest = root / ".resonance/framework-manifest.json"
            manifest.parent.mkdir()
            manifest.write_text(json.dumps({
                "schema": 1,
                "files": {".agents/skills/framework/SKILL.md": "0" * 64},
            }), encoding="utf-8")
            report = validate_skill.validate(skill_md, validate_skill.Report(str(skill_md)))
            self.assertTrue(any("evals: found 3 case(s)" in e and ">= 6 golden" in e for e in report.errors))

    def test_symlinked_consumer_manifest_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            skill_md = root / ".agents/skills/company/SKILL.md"
            _make_skill(skill_md.parent, n_evals=3)
            outside = root / "outside.json"
            outside.write_text(json.dumps({"schema": 1, "files": {}}), encoding="utf-8")
            manifest = root / ".resonance/framework-manifest.json"
            manifest.parent.mkdir()
            try:
                manifest.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks are unavailable on this host")
            report = validate_skill.validate(skill_md, validate_skill.Report(str(skill_md)))
            self.assertTrue(any("ownership: invalid framework manifest" in e for e in report.errors))
            self.assertTrue(any("evals: found 3 case(s)" in e and ">= 6 golden" in e for e in report.errors))

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
