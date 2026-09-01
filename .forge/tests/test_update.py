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
        shutil.copy2(ROOT / ".forge" / "project_skills.py", source / ".forge" / "project_skills.py")
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

    def test_apply_checks_live_write_authority_before_backup(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        with mock.patch.object(update.tempfile, "NamedTemporaryFile", side_effect=PermissionError("sandbox")):
            with self.assertRaisesRegex(PermissionError, "before update"):
                update.apply(source, target)
        self.assertFalse((target / ".resonance" / "backups").exists())

    def test_rollback_failure_preserves_both_errors_and_journal(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (source / ".forge" / "forge.py").write_text("raise SystemExit('validator broke')\n", encoding="utf-8")
        self.commit(source)
        runtime = sys.modules[update.apply.__module__]
        with mock.patch.object(runtime, "rollback", side_effect=PermissionError("rollback blocked")):
            with self.assertRaises(update.UpdateRollbackError) as raised:
                update.apply(source, target)
        message = str(raised.exception)
        self.assertIn("post-update validation failed", message)
        self.assertIn("rollback blocked", message)
        self.assertIn("journal.json", message)
        self.assertTrue(raised.exception.backup.joinpath("journal.json").is_file())

    def test_compiled_profile_excludes_source_tooling(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (source / ".agents" / "skills" / "demo").mkdir(parents=True)
        (source / ".agents" / "skills" / "demo" / "SKILL.md").write_text("demo", encoding="utf-8")
        self.commit(source)
        work = update.plan(source, target, "compiled")
        self.assertEqual(work["profile"], "compiled")
        self.assertIn(".agents/skills/demo/SKILL.md", work["writes"])
        self.assertNotIn(".forge/forge.py", work["writes"])
        self.assertNotIn("AGENTS.md", work["writes"])

    def test_legacy_compiled_looking_target_requires_profile(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (target / ".agents" / "skills").mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "profile is required"):
            update.plan(source, target)

    def test_legacy_manifest_keeps_profile_unknown_until_explicit_choice(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (source / ".agents" / "skills" / "demo").mkdir(parents=True)
        (source / ".agents" / "skills" / "demo" / "SKILL.md").write_text("demo", encoding="utf-8")
        self.commit(source)
        (target / ".agents" / "skills").mkdir(parents=True)
        manifest = target / update.MANIFEST
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({"schema": 1, "version": "2.5.1", "files": {}}), encoding="utf-8")
        self.assertNotIn("profile", update.load_manifest(target))
        with self.assertRaisesRegex(ValueError, "profile is required"):
            update.plan(source, target)
        self.assertEqual("compiled", update.plan(source, target, "compiled")["profile"])

    def test_recorded_profile_migration_is_unsupported(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        manifest = target / update.MANIFEST
        manifest.parent.mkdir(parents=True)
        for recorded, requested in (("source", "compiled"), ("compiled", "source")):
            manifest.write_text(
                json.dumps({"schema": 1, "version": "2.5.2", "profile": recorded, "files": {}}),
                encoding="utf-8",
            )
            with self.subTest(recorded=recorded, requested=requested):
                with self.assertRaisesRegex(ValueError, "profile migration is unsupported"):
                    update.plan(source, target, requested)

    def test_compiled_apply_validates_from_pinned_source(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (source / ".agents" / "skills" / "demo").mkdir(parents=True)
        (source / ".agents" / "skills" / "demo" / "SKILL.md").write_text("demo", encoding="utf-8")
        self.commit(source)
        update.apply(source, target, "9.9.9", "compiled")
        manifest = json.loads((target / update.MANIFEST).read_text(encoding="utf-8"))
        self.assertEqual(manifest["profile"], "compiled")
        self.assertTrue((target / ".agents" / "skills" / "demo" / "SKILL.md").exists())
        self.assertFalse((target / ".forge").exists())

    def test_compiled_apply_checks_private_lock_in_target(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        generated = source / ".agents" / "skills" / "demo" / "SKILL.md"
        generated.parent.mkdir(parents=True)
        generated.write_text("demo v1", encoding="utf-8")
        self.commit(source)
        update.apply(source, target, "9.9.9", "compiled")
        private = target / ".agents" / "skills" / "company" / "private" / "SKILL.md"
        private.parent.mkdir(parents=True)
        private.write_text("private", encoding="utf-8")
        subprocess.run(
            [sys.executable, str(source / ".forge" / "project_skills.py"), "--root", str(target)],
            check=True,
            capture_output=True,
        )
        generated.write_text("demo v2", encoding="utf-8")
        self.commit(source)
        update.apply(source, target, "9.9.9", "compiled")
        self.assertEqual("private", private.read_text(encoding="utf-8"))

    def test_compiled_apply_rejects_stale_private_lock_in_target(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        generated = source / ".agents" / "skills" / "demo" / "SKILL.md"
        generated.parent.mkdir(parents=True)
        generated.write_text("demo v1", encoding="utf-8")
        self.commit(source)
        update.apply(source, target, "9.9.9", "compiled")
        private = target / ".agents" / "skills" / "company" / "private" / "SKILL.md"
        private.parent.mkdir(parents=True)
        private.write_text("private", encoding="utf-8")
        lock = target / ".resonance" / "project-skills.lock.json"
        lock.write_text(json.dumps({
            "schema_version": 1,
            "skills": [{"id": "company/private", "files": {
                ".agents/skills/company/private/SKILL.md": "0" * 64,
            }}],
        }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        generated.write_text("demo v2", encoding="utf-8")
        self.commit(source)
        with self.assertRaisesRegex(RuntimeError, "project skill verification failed"):
            update.apply(source, target, "9.9.9", "compiled")
        self.assertEqual("demo v1", (target / ".agents" / "skills" / "demo" / "SKILL.md").read_text(encoding="utf-8"))

    def test_adopt_requires_profile_for_target_without_source_tree(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (source / ".agents" / "skills" / "demo").mkdir(parents=True)
        (source / ".agents" / "skills" / "demo" / "SKILL.md").write_text("demo", encoding="utf-8")
        self.commit(source)
        (target / ".agents" / "skills" / "demo").mkdir(parents=True)
        (target / ".agents" / "skills" / "demo" / "SKILL.md").write_text("demo", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "profile is required"):
            update.adopt(source, target)

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

    def test_unowned_root_bridges_are_preserved_without_conflict(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        for name in ("AGENTS.md", "CLAUDE.md"):
            (source / name).write_text("framework", encoding="utf-8")
            (target / name).write_text("project", encoding="utf-8")
        self.commit(source)
        work = update.plan(source, target, "source")
        self.assertEqual([], work["conflicts"])
        self.assertEqual(["AGENTS.md", "CLAUDE.md"], work["preserved"])
        self.assertNotIn("AGENTS.md", work["files"])
        self.assertNotIn("CLAUDE.md", work["files"])
        update.apply(source, target, "9.9.9", "source")
        self.assertEqual("project", (target / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertEqual("project", (target / "CLAUDE.md").read_text(encoding="utf-8"))
        installed = json.loads((target / update.MANIFEST).read_text(encoding="utf-8"))
        self.assertNotIn("AGENTS.md", installed["files"])
        self.assertNotIn("CLAUDE.md", installed["files"])

    def test_adopt_records_existing_bytes_without_changing_them(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (target / ".forge").mkdir()
        existing = target / ".forge" / "tool.py"
        existing.write_text("raise SystemExit(0)\n", encoding="utf-8")
        update.adopt(source, target, "source")
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
        update.adopt(source, target, "source")
        owned = update.load_manifest(target)["files"]
        self.assertIn(".agents/skills/known/SKILL.md", owned)
        self.assertNotIn(".agents/skills/custom/SKILL.md", owned)
        self.assertNotIn("AGENTS.md", owned)

    def test_adopt_never_claims_unowned_root_bridges_even_when_identical(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        managed = source / ".agents" / "skills" / "known" / "SKILL.md"
        managed.parent.mkdir(parents=True)
        managed.write_text("known", encoding="utf-8")
        for relative in update.PRESERVE_IF_UNOWNED:
            source_file = source / relative
            source_file.parent.mkdir(parents=True, exist_ok=True)
            source_file.write_text("framework", encoding="utf-8")
            target_file = target / relative
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text("framework", encoding="utf-8")
        target_managed = target / managed.relative_to(source)
        target_managed.parent.mkdir(parents=True)
        target_managed.write_text("known", encoding="utf-8")
        self.commit(source)

        update.adopt(source, target, "source")

        owned = update.load_manifest(target)["files"]
        self.assertIn(".agents/skills/known/SKILL.md", owned)
        for relative in update.PRESERVE_IF_UNOWNED:
            self.assertNotIn(relative, owned)

    def test_upgrade_preserves_committed_private_skill_and_lock(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        private = target / ".agents" / "skills" / "company" / "private"
        private.mkdir(parents=True)
        (private / "SKILL.md").write_text("private multiplayer skill", encoding="utf-8")
        lock = target / ".resonance" / "project-skills.lock.json"
        lock.parent.mkdir(parents=True)
        private_hash = update.digest(private / "SKILL.md")
        lock.write_text(json.dumps({
            "schema_version": 1,
            "skills": [{
                "id": "company/private",
                "files": {".agents/skills/company/private/SKILL.md": private_hash},
            }],
        }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        before_lock = lock.read_text(encoding="utf-8")
        update.apply(source, target, "9.9.9", "source")
        self.assertEqual(
            "private multiplayer skill",
            (private / "SKILL.md").read_text(encoding="utf-8"),
        )
        self.assertEqual(before_lock, lock.read_text(encoding="utf-8"))

    def test_stale_private_skill_lock_rolls_back_upgrade(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        private = target / ".agents" / "skills" / "company" / "private"
        private.mkdir(parents=True)
        (private / "SKILL.md").write_text("changed", encoding="utf-8")
        lock = target / ".resonance" / "project-skills.lock.json"
        lock.parent.mkdir(parents=True)
        lock.write_text(json.dumps({
            "schema_version": 1,
            "skills": [{
                "id": "company/private",
                "files": {".agents/skills/company/private/SKILL.md": "0" * 64},
            }],
        }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "project skill verification failed"):
            update.apply(source, target, "9.9.9", "source")
        self.assertFalse((target / ".forge" / "tool.py").exists())

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
