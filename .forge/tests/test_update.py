import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("resonance_update", ROOT / ".forge" / "update.py")
update = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = update
spec.loader.exec_module(update)


class UpdateTests(unittest.TestCase):
    def commit(self, source):
        subprocess.run(["git", "add", "."], cwd=source, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "fixture"], cwd=source, check=True, capture_output=True)

    def fixture(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        source, target = root / "source", root / "target"
        (source / ".forge").mkdir(parents=True)
        target.mkdir()
        (source / "package.json").write_text('{"version":"9.9.9"}', encoding="utf-8")
        for name in ("tool.py", "forge.py", "validate_skill.py", "eval_integrity.py"):
            (source / ".forge" / name).write_text("raise SystemExit(0)\n", encoding="utf-8")
        subprocess.run(["git", "init"], cwd=source, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.test"], cwd=source, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=source, check=True)
        self.commit(source)
        return td, source, target

    def test_preview_does_not_write(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        result = update.plan(source, target)
        self.assertIn(".forge/tool.py", result["writes"])
        self.assertFalse((target / ".forge").exists())

    def test_apply_records_ownership_and_blocks_user_change(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        update.apply(source, target, "9.9.9")
        manifest = json.loads((target / update.MANIFEST).read_text(encoding="utf-8"))
        self.assertIn(".forge/tool.py", manifest["files"])
        (target / ".forge" / "tool.py").write_text("user edit", encoding="utf-8")
        self.assertIn(".forge/tool.py", update.plan(source, target)["conflicts"])

    def test_user_owned_agents_file_is_never_overwritten(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (source / ".agents").mkdir()
        (source / ".agents" / "owned.md").write_text("framework", encoding="utf-8")
        self.commit(source)
        (target / ".agents").mkdir()
        (target / ".agents" / "owned.md").write_text("user", encoding="utf-8")
        with self.assertRaises(ValueError):
            update.apply(source, target)
        self.assertEqual((target / ".agents" / "owned.md").read_text(), "user")

    def test_adopt_records_existing_bytes_without_changing_them(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (target / ".forge").mkdir()
        existing = target / ".forge" / "tool.py"
        existing.write_text("raise SystemExit(0)\n", encoding="utf-8")
        update.adopt(source, target)
        self.assertEqual(existing.read_text(encoding="utf-8"), "raise SystemExit(0)\n")
        self.assertEqual(update.plan(source, target)["conflicts"], [])

    def test_durable_rollback_restores_old_and_removes_new_files(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (target / ".forge").mkdir()
        old = target / ".forge" / "old.py"
        old.write_text("old", encoding="utf-8")
        backup = target / ".resonance" / "backups" / "resonance-update-test"
        (backup / "files" / ".forge").mkdir(parents=True)
        (backup / "files" / ".forge" / "old.py").write_text("old", encoding="utf-8")
        new = target / ".forge" / "new.py"
        new.write_text("new", encoding="utf-8")
        old.write_text("changed", encoding="utf-8")
        journal = {"schema": 1, "status": "applying", "target": str(target),
                   "entries": [{"path": ".forge/old.py", "existed": True},
                               {"path": ".forge/new.py", "existed": False}]}
        (backup / "journal.json").write_text(json.dumps(journal), encoding="utf-8")
        update.rollback(backup)
        self.assertEqual(old.read_text(encoding="utf-8"), "old")
        self.assertFalse(new.exists())

    def test_adopt_does_not_claim_custom_skill_or_agents(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (source / ".agents" / "skills" / "known").mkdir(parents=True)
        (source / ".agents" / "skills" / "known" / "SKILL.md").write_text("known", encoding="utf-8")
        self.commit(source)
        (target / ".agents" / "skills" / "known").mkdir(parents=True)
        (target / ".agents" / "skills" / "known" / "SKILL.md").write_text("known", encoding="utf-8")
        (target / ".agents" / "skills" / "custom").mkdir(parents=True)
        (target / ".agents" / "skills" / "custom" / "SKILL.md").write_text("custom", encoding="utf-8")
        (target / "AGENTS.md").write_text("project", encoding="utf-8")
        update.adopt(source, target)
        owned = update.load_manifest(target)["files"]
        self.assertIn(".agents/skills/known/SKILL.md", owned)
        self.assertNotIn(".agents/skills/custom/SKILL.md", owned)
        self.assertNotIn("AGENTS.md", owned)

    def test_adopt_does_not_claim_customized_known_file(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (source / ".agents" / "skills" / "known").mkdir(parents=True)
        (source / ".agents" / "skills" / "known" / "SKILL.md").write_text("released", encoding="utf-8")
        self.commit(source)
        (target / ".forge").mkdir()
        (target / ".forge" / "tool.py").write_text("raise SystemExit(0)\n", encoding="utf-8")
        (target / ".agents" / "skills" / "known").mkdir(parents=True)
        (target / ".agents" / "skills" / "known" / "SKILL.md").write_text("customized", encoding="utf-8")
        update.adopt(source, target)
        self.assertNotIn(".agents/skills/known/SKILL.md", update.load_manifest(target)["files"])

    def test_incomplete_backup_journal_never_deletes_unrecorded_original(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        original = target / ".forge" / "original.py"
        original.parent.mkdir()
        original.write_text("original", encoding="utf-8")
        backup = target / ".resonance" / "backups" / "resonance-update-test"
        backup.mkdir(parents=True)
        journal = {"schema": 1, "status": "backing-up", "target": str(target), "entries": []}
        (backup / "journal.json").write_text(json.dumps(journal), encoding="utf-8")
        update.rollback(backup)
        self.assertEqual(original.read_text(encoding="utf-8"), "original")

    def test_source_rejects_untracked_files(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        leaked = source / ".forge" / "eval_results.json"
        leaked.write_text("private", encoding="utf-8")
        with self.assertRaises(ValueError):
            update.source_files(source)

    def test_source_rejects_modified_or_deleted_tracked_files(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        tool = source / ".forge" / "tool.py"
        tool.write_text("modified", encoding="utf-8")
        with self.assertRaises(ValueError):
            update.source_files(source)
        subprocess.run(["git", "restore", ".forge/tool.py"], cwd=source, check=True)
        tool.unlink()
        with self.assertRaises(ValueError):
            update.source_files(source)

    def test_source_clean_check_ignores_git_stderr_warnings(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        real_run = subprocess.run

        def noisy_status(args, **kwargs):
            if args[:3] == ["git", "status", "--porcelain=v1"]:
                return subprocess.CompletedProcess(
                    args,
                    0,
                    stdout=b"",
                    stderr=b"warning: unable to access global excludes file\n",
                )
            return real_run(args, **kwargs)

        with mock.patch.object(update.subprocess, "run", side_effect=noisy_status):
            files = update.source_files(source)
        self.assertIn(".forge/tool.py", files)


if __name__ == "__main__":
    unittest.main()
