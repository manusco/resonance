import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("project_skills", ROOT / ".forge" / "project_skills.py")
project_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(project_skills)


class ProjectSkillLockTests(unittest.TestCase):
    def fixture(self):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        skills = root / ".agents" / "skills"
        official = skills / "ops" / "official"
        private = skills / "company" / "private"
        official.mkdir(parents=True)
        private.mkdir(parents=True)
        (official / "SKILL.md").write_text("official", encoding="utf-8")
        (private / "SKILL.md").write_text("private", encoding="utf-8")
        (private / "reference.md").write_text("shared", encoding="utf-8")
        return temporary, skills

    def test_lock_contains_only_repo_owned_skills(self):
        temporary, skills = self.fixture()
        self.addCleanup(temporary.cleanup)
        owned = {".agents/skills/ops/official/SKILL.md"}
        lock = project_skills.project_skill_lock(skills, owned)
        self.assertEqual(["company/private"], [entry["id"] for entry in lock["skills"]])
        self.assertEqual(2, len(lock["skills"][0]["files"]))

    def test_private_skill_change_makes_lock_stale(self):
        temporary, skills = self.fixture()
        self.addCleanup(temporary.cleanup)
        owned = {".agents/skills/ops/official/SKILL.md"}
        before = project_skills.project_skill_lock(skills, owned)
        (skills / "company" / "private" / "SKILL.md").write_text("changed", encoding="utf-8")
        self.assertNotEqual(before, project_skills.project_skill_lock(skills, owned))

    def test_mixed_ownership_fails_closed(self):
        temporary, skills = self.fixture()
        self.addCleanup(temporary.cleanup)
        owned = {".agents/skills/company/private/SKILL.md"}
        with self.assertRaisesRegex(ValueError, "mixed framework/project ownership"):
            project_skills.project_skill_lock(skills, owned)


if __name__ == "__main__":
    unittest.main()
