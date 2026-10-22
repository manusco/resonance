import importlib.util
import contextlib
import io
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

integrity_spec = importlib.util.spec_from_file_location(
    "eval_integrity_for_source_profile_test", ROOT / ".forge" / "eval_integrity.py"
)
integrity = importlib.util.module_from_spec(integrity_spec)
sys.modules[integrity_spec.name] = integrity
integrity_spec.loader.exec_module(integrity)


class UpdateTests(unittest.TestCase):
    def commit(self, source):
        subprocess.run(["git", "add", "."], cwd=source, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "fixture"], cwd=source, check=True, capture_output=True)

    def init_git(self, root):
        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.test"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)

    def commit_target(self, target):
        subprocess.run(["git", "add", "."], cwd=target, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "installed framework"], cwd=target, check=True, capture_output=True)

    def fixture(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        source, target = root / "source", root / "target"
        (source / ".forge").mkdir(parents=True)
        target.mkdir()
        (source / "AGENTS.md").write_text("framework instructions\n", encoding="utf-8")
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

    def test_compiled_profile_alias_installs_complete_runtime(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (source / ".agents" / "skills" / "demo").mkdir(parents=True)
        (source / ".agents" / "skills" / "demo" / "SKILL.md").write_text("demo", encoding="utf-8")
        self.commit(source)
        work = update.plan(source, target, "compiled")
        self.assertEqual(work["profile"], "source")
        self.assertIn(".agents/skills/demo/SKILL.md", work["writes"])
        self.assertIn(".forge/forge.py", work["writes"])
        self.assertIn("AGENTS.md", work["writes"])

    def test_legacy_compiled_looking_target_defaults_to_complete_install(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (target / ".agents" / "skills").mkdir(parents=True)
        work = update.plan(source, target)
        self.assertEqual("source", work["profile"])
        self.assertIn(".forge/forge.py", work["writes"])

    def test_legacy_manifest_without_profile_defaults_to_complete_install(self):
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
        self.assertEqual("source", update.plan(source, target)["profile"])
        self.assertEqual("source", update.plan(source, target, "compiled")["profile"])

    def test_legacy_compiled_manifest_upgrades_to_complete_install_without_profile(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (source / ".agents" / "skills" / "demo").mkdir(parents=True)
        (source / ".agents" / "skills" / "demo" / "SKILL.md").write_text("demo\n", encoding="utf-8")
        self.commit(source)
        old_skill = source / ".agents" / "skills" / "demo" / "SKILL.md"
        target_skill = target / ".agents" / "skills" / "demo" / "SKILL.md"
        target_skill.parent.mkdir(parents=True)
        target_skill.write_bytes(old_skill.read_bytes())
        manifest = target / update.MANIFEST
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({
            "schema": 1, "version": "9.9.8", "profile": "compiled",
            "files": {".agents/skills/demo/SKILL.md": update.digest(old_skill)},
        }), encoding="utf-8")

        update.apply(source, target)

        installed = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual("source", installed["profile"])
        self.assertIn(".forge/forge.py", installed["files"])
        self.assertTrue((target / ".forge/forge.py").is_file())

    def test_unknown_new_forge_path_collision_is_blocked_and_preserved(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        collision = source / ".forge" / "new_tool.py"
        collision.write_text("framework tool\n", encoding="utf-8")
        self.commit(source)
        user_file = target / ".forge" / "new_tool.py"
        user_file.parent.mkdir(parents=True)
        user_file.write_text("user file\n", encoding="utf-8")

        work = update.plan(source, target)

        self.assertIn(".forge/new_tool.py", work["conflicts"])
        self.assertEqual("user file\n", user_file.read_text(encoding="utf-8"))
        with self.assertRaisesRegex(ValueError, "block update"):
            update.apply(source, target)
        self.assertEqual("user file\n", user_file.read_text(encoding="utf-8"))

    def test_missing_profile_stale_hash_reconciles_only_from_exact_tag_baseline(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        old_tool = source / ".forge" / "tool.py"
        old_tool.write_text("released old tool\n", encoding="utf-8")
        (source / "package.json").write_text('{"version":"9.9.8"}', encoding="utf-8")
        self.commit(source)
        subprocess.run(["git", "tag", "v9.9.8"], cwd=source, check=True, capture_output=True)
        old_revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=source, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        installed_tool = target / ".forge" / "tool.py"
        installed_tool.parent.mkdir(parents=True)
        installed_tool.write_bytes(old_tool.read_bytes())
        manifest = target / update.MANIFEST
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({
            "schema": 1, "version": "9.9.8",
            "files": {".forge/tool.py": "0" * 64},
        }), encoding="utf-8")
        old_tool.write_text("released new tool\n", encoding="utf-8")
        (source / "package.json").write_text('{"version":"9.9.9"}', encoding="utf-8")
        self.commit(source)

        work = update.plan(source, target)

        self.assertEqual(old_revision, work["baseline_revision"])
        self.assertNotIn(".forge/tool.py", work["conflicts"])
        self.assertIn(".forge/tool.py", work["writes"])
        self.assertEqual("matches_installed_release", work["reasons"][".forge/tool.py"]["code"])

    def test_compiled_historical_scope_cannot_authorize_forge_overwrite(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        old_tool = source / ".forge" / "tool.py"
        old_tool.write_text("old forge tool\n", encoding="utf-8")
        (source / "package.json").write_text('{"version":"9.9.8"}', encoding="utf-8")
        self.commit(source)
        subprocess.run(["git", "tag", "v9.9.8"], cwd=source, check=True, capture_output=True)
        old_tool.write_text("new forge tool\n", encoding="utf-8")
        (source / "package.json").write_text('{"version":"9.9.9"}', encoding="utf-8")
        self.commit(source)
        installed_tool = target / ".forge" / "tool.py"
        installed_tool.parent.mkdir(parents=True)
        installed_tool.write_text("old forge tool\n", encoding="utf-8")
        manifest = target / update.MANIFEST
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({
            "schema": 1, "version": "9.9.8", "profile": "compiled",
            "files": {".forge/tool.py": "0" * 64},
        }), encoding="utf-8")

        work = update.plan(source, target)

        self.assertIn(".forge/tool.py", work["conflicts"])
        self.assertEqual("old forge tool\n", installed_tool.read_text(encoding="utf-8"))

    def test_recorded_profile_aliases_normalize_to_complete_install(self):
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
                self.assertEqual("source", update.plan(source, target, requested)["profile"])

    def test_compiled_apply_installs_and_validates_complete_runtime(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (source / ".agents" / "skills" / "demo").mkdir(parents=True)
        (source / ".agents" / "skills" / "demo" / "SKILL.md").write_text("demo", encoding="utf-8")
        self.commit(source)
        update.apply(source, target, "9.9.9", "compiled")
        manifest = json.loads((target / update.MANIFEST).read_text(encoding="utf-8"))
        self.assertEqual(manifest["profile"], "source")
        self.assertTrue((target / ".agents" / "skills" / "demo" / "SKILL.md").exists())
        self.assertTrue((target / ".forge" / "forge.py").exists())

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

    def test_adopt_defaults_to_complete_install_without_source_tree(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        (source / ".agents" / "skills" / "demo").mkdir(parents=True)
        (source / ".agents" / "skills" / "demo" / "SKILL.md").write_text("demo", encoding="utf-8")
        self.commit(source)
        (target / ".agents" / "skills" / "demo").mkdir(parents=True)
        (target / ".agents" / "skills" / "demo" / "SKILL.md").write_text("demo", encoding="utf-8")
        manifest_path = update.adopt(source, target)
        adopted = json.loads(manifest_path.read_text())
        self.assertEqual("source", adopted["profile"])
        self.assertIn(".agents/skills/demo/SKILL.md", adopted["files"])

    def test_apply_records_ownership_and_blocks_user_change(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        update.apply(source, target, "9.9.9")
        manifest = json.loads((target / update.MANIFEST).read_text(encoding="utf-8"))
        self.assertIn(".forge/tool.py", manifest["files"])
        (target / ".forge" / "tool.py").write_text("user edit", encoding="utf-8")
        self.assertIn(".forge/tool.py", update.plan(source, target)["conflicts"])

    def test_incoming_byte_equality_repairs_stale_ownership_without_conflict(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        update.apply(source, target, "9.9.9")
        manifest_path = target / update.MANIFEST
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"][".forge/tool.py"] = "0" * 64
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        work = update.plan(source, target)

        self.assertNotIn(".forge/tool.py", work["conflicts"])
        self.assertNotIn(".forge/tool.py", work["writes"])

    def test_committed_customization_is_still_a_conflict(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        update.apply(source, target, "9.9.9")
        self.init_git(target)
        self.commit_target(target)
        (target / ".forge" / "tool.py").write_text("committed local change\n", encoding="utf-8")
        self.commit_target(target)

        work = update.plan(source, target)

        self.assertIn(".forge/tool.py", work["conflicts"])

    def test_stale_hash_matching_verified_old_release_can_upgrade(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        branch = subprocess.run(
            ["git", "branch", "--show-current"], cwd=source, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        old_tool = source / ".forge" / "tool.py"
        old_tool.write_text("released old tool\n", encoding="utf-8")
        package = source / "package.json"
        package.write_text('{"version":"9.9.8"}', encoding="utf-8")
        self.commit(source)
        subprocess.run(["git", "tag", "v9.9.8"], cwd=source, check=True, capture_output=True)
        old_revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=source, check=True,
            capture_output=True, text=True,
        ).stdout.strip()

        self.init_git(target)
        subprocess.run(["git", "checkout", "--detach", "v9.9.8"], cwd=source, check=True, capture_output=True)
        update.apply(source, target, "9.9.8")
        self.commit_target(target)

        subprocess.run(["git", "switch", branch], cwd=source, check=True, capture_output=True)
        old_tool.write_text("released new tool\n", encoding="utf-8")
        package.write_text('{"version":"9.9.9"}', encoding="utf-8")
        self.commit(source)
        manifest_path = target / update.MANIFEST
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"][".forge/tool.py"] = "0" * 64
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.commit_target(target)

        work = update.plan(source, target)

        self.assertNotIn(".forge/tool.py", work["conflicts"])
        self.assertIn(".forge/tool.py", work["writes"])
        self.assertEqual(old_revision, manifest.get("source_revision"))

    def test_second_identical_apply_does_not_create_transaction(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        first = update.apply(source, target, "9.9.9")
        second = update.apply(source, target, "9.9.9")

        self.assertIsNotNone(first)
        self.assertIsNone(second)
        transactions = list((target / ".resonance").glob("updates/*/journal.json"))
        backups = list((target / ".resonance").glob("backups/resonance-update-*/journal.json"))
        self.assertEqual(1, len(transactions))
        self.assertEqual([], backups)

        work = update.plan(source, target)
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            self.assertEqual(0, update.main([
                "--source", str(source), "--target", str(target), "--apply", "--json",
                "--version", work["version"], "--revision", work["revision"],
                "--plan-digest", work["plan_digest"],
            ]))
        self.assertEqual("already_current", json.loads(stdout.getvalue())["status"])
        self.assertEqual("", stderr.getvalue())

    def test_git_preimages_use_journal_without_copied_payload_and_restore_modes(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        repo = target
        target = repo / "consumer"
        target.mkdir()
        update.apply(source, target, "9.9.9")
        self.init_git(repo)
        tool = target / ".forge" / "tool.py"
        tool.chmod(0o640)
        self.commit_target(repo)
        old_bytes = tool.read_bytes()

        tool_source = source / ".forge" / "tool.py"
        tool_source.write_text("updated tool\n", encoding="utf-8")
        (source / ".forge" / "new.py").write_text("new file\n", encoding="utf-8")
        (source / "package.json").write_text('{"version":"9.9.10"}', encoding="utf-8")
        self.commit(source)
        transaction = update.apply(source, target, "9.9.10")
        journal = json.loads((transaction / "journal.json").read_text(encoding="utf-8"))

        self.assertEqual(2, journal["schema"])
        self.assertEqual(repo.resolve(), Path(journal["git_root"]).resolve())
        self.assertEqual("consumer", journal["git_prefix"])
        self.assertEqual("git", next(e for e in journal["entries"] if e["path"] == ".forge/tool.py")["source"])
        self.assertFalse((transaction / "files").exists())
        self.assertFalse((target / ".resonance" / "backups").exists())

        journaled_commit = journal["git_commit"]
        branch = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"], cwd=repo,
                                check=True, capture_output=True, text=True).stdout.strip()
        empty_tree = subprocess.run(["git", "mktree"], cwd=repo, input=b"", check=True,
                                    capture_output=True).stdout.decode().strip()
        unrelated = subprocess.run(["git", "commit-tree", empty_tree, "-m", "unrelated head"],
                                   cwd=repo, check=True, capture_output=True, text=True).stdout.strip()
        subprocess.run(["git", "update-ref", f"refs/heads/{branch}", unrelated], cwd=repo, check=True)
        subprocess.run(["git", "reflog", "expire", "--expire=now", "--all"], cwd=repo, check=True)
        subprocess.run(["git", "gc", "--prune=now"], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "cat-file", "-e", journaled_commit], cwd=repo, check=True)
        update.rollback(transaction)

        self.assertEqual(old_bytes, tool.read_bytes())
        self.assertEqual(0o640, tool.stat().st_mode & 0o777)
        self.assertFalse((target / ".forge" / "new.py").exists())

    def test_manifest_only_reconciliation_copies_only_dirty_manifest_preimage(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        update.apply(source, target, "9.9.9")
        self.init_git(target)
        self.commit_target(target)
        manifest_path = target / update.MANIFEST
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"][".forge/tool.py"] = "0" * 64
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        prior_manifest = manifest_path.read_bytes()
        work = update.plan(source, target)

        self.assertEqual([], work["writes"])
        self.assertEqual([], work["conflicts"])
        self.assertTrue(work["manifest_write"])
        transaction = update.apply(source, target, "9.9.9")
        journal = json.loads((transaction / "journal.json").read_text(encoding="utf-8"))
        self.assertEqual([update.MANIFEST], [entry["path"] for entry in journal["entries"]])
        self.assertEqual("file", journal["entries"][0]["source"])
        self.assertEqual(prior_manifest, (transaction / "files" / update.MANIFEST).read_bytes())
        self.assertFalse((target / ".resonance" / "backups").exists())
        update.rollback(transaction)
        self.assertEqual(prior_manifest, manifest_path.read_bytes())

    def test_clean_git_stale_hash_reconciliation_uses_manifest_blob_without_file_copies(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        update.apply(source, target, "9.9.9")
        manifest_path = target / update.MANIFEST
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"][".forge/tool.py"] = "0" * 64
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.init_git(target)
        self.commit_target(target)
        work = update.plan(source, target)

        self.assertEqual([], work["conflicts"])
        self.assertEqual([], work["writes"])
        transaction = update.apply(source, target, "9.9.9")
        journal = json.loads((transaction / "journal.json").read_text(encoding="utf-8"))

        self.assertEqual([update.MANIFEST], [entry["path"] for entry in journal["entries"]])
        self.assertEqual("git", journal["entries"][0]["source"])
        self.assertFalse((transaction / "files").exists())
        self.assertFalse((target / ".resonance" / "backups").exists())

    def test_rollback_validates_every_preimage_before_restoring_any(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        one = target / ".forge" / "one.py"
        two = target / ".forge" / "two.py"
        one.parent.mkdir(parents=True)
        one.write_text("changed", encoding="utf-8")
        two.write_text("changed", encoding="utf-8")
        transaction = target / ".resonance" / "updates" / "broken"
        saved = transaction / "files" / ".forge" / "one.py"
        saved.parent.mkdir(parents=True)
        saved.write_text("original", encoding="utf-8")
        journal = {"schema": 2, "status": "applying", "transaction_id": "broken",
                   "target": str(target), "entries": [
            {"path": ".forge/one.py", "existed": True, "source": "file",
             "sha256": update.digest(saved), "mode": 0o644},
            {"path": ".forge/two.py", "existed": True, "source": "file",
             "sha256": "0" * 64, "mode": 0o644},
        ]}
        (transaction / "journal.json").write_text(json.dumps(journal), encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "preimage is missing"):
            update.rollback(transaction)

        self.assertEqual("changed", one.read_text(encoding="utf-8"))

    def test_rollback_rejects_invalid_mode_before_restoring_any(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        one = target / ".forge" / "one.py"
        two = target / ".forge" / "two.py"
        one.parent.mkdir(parents=True)
        one.write_text("changed", encoding="utf-8")
        two.write_text("changed", encoding="utf-8")
        transaction = target / ".resonance" / "updates" / "bad-mode"
        for rel in ("one.py", "two.py"):
            saved = transaction / "files" / ".forge" / rel
            saved.parent.mkdir(parents=True, exist_ok=True)
            saved.write_text("original", encoding="utf-8")
        entries = []
        for rel in ("one.py", "two.py"):
            saved = transaction / "files" / ".forge" / rel
            entries.append({"path": f".forge/{rel}", "existed": True, "source": "file",
                            "sha256": update.digest(saved), "mode": 0o644})
        entries[1]["mode"] = True
        journal = {"schema": 2, "status": "applying", "transaction_id": "bad-mode",
                   "target": str(target), "entries": entries}
        (transaction / "journal.json").write_text(json.dumps(journal), encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "invalid saved mode"):
            update.rollback(transaction)

        self.assertEqual("changed", one.read_text(encoding="utf-8"))

    def test_cli_summary_and_apply_errors_are_concise(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        update.apply(source, target, "9.9.9")
        (target / ".forge" / "tool.py").write_text("local change", encoding="utf-8")
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            self.assertEqual(1, update.main([
                "--source", str(source), "--target", str(target), "--summary",
            ]))
        self.assertIn("Plan: blocked", stdout.getvalue())
        self.assertIn(".forge/tool.py", stdout.getvalue())
        self.assertNotIn('"files"', stdout.getvalue())
        self.assertEqual("", stderr.getvalue())

        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            self.assertEqual(1, update.main([
                "--source", str(source), "--target", str(target), "--apply",
                "--version", "9.9.9", "--revision", update.source_revision(source),
                "--plan-digest", "0" * 64,
            ]))
        self.assertIn("update blocked:", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_invalid_project_skill_lock_fails_closed(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        lock = target / ".resonance" / "project-skills.lock.json"
        lock.parent.mkdir(parents=True)
        lock.write_text('{"schema_version":0,"skills":[]}', encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "project skill lock"):
            update.plan(source, target)

        self.assertFalse((target / ".forge").exists())

    def test_apply_rejects_symlinked_staging_or_recovery_parent(self):
        for name in ("tmp", "updates"):
            with self.subTest(parent=name):
                td, source, target = self.fixture()
                self.addCleanup(td.cleanup)
                outside = Path(td.name) / "outside"
                outside.mkdir()
                resonance = target / ".resonance"
                resonance.mkdir()
                (resonance / name).symlink_to(outside, target_is_directory=True)

                with self.assertRaisesRegex(ValueError, "path escapes target|symlink"):
                    update.apply(source, target, "9.9.9")

                self.assertEqual([], list(outside.iterdir()))

    def test_manifest_cannot_remove_application_code_outside_profile(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)
        update.apply(source, target, "9.9.9")
        app = target / "application.py"
        app.write_text("application data\n", encoding="utf-8")
        manifest_path = target / update.MANIFEST
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"]["application.py"] = update.digest(app)
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        work = update.plan(source, target)

        self.assertIn("application.py", work["conflicts"])
        self.assertNotIn("application.py", work["removes"])
        self.assertEqual("application data\n", app.read_text(encoding="utf-8"))

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

    def test_consumer_design_entry_survives_source_upgrade(self):
        for design_entry in (
            "# Product design contract\n\nApproved workspace patterns.\n",
            "# Design source\n\nCanonical: `DESIGN.md` (approved by product owner).\n",
        ):
            with self.subTest(design_entry=design_entry):
                td, source, target = self.fixture()
                self.addCleanup(td.cleanup)
                source_template = source / ".resonance" / "05_design.md"
                source_template.parent.mkdir(parents=True)
                source_template.write_text("# Optional consumer design contract\n", encoding="utf-8")
                self.commit(source)
                design = target / ".resonance" / "05_design.md"
                design.parent.mkdir(parents=True)
                design.write_text(design_entry, encoding="utf-8")

                initial_plan = update.plan(source, target, "source")
                self.assertNotIn(".resonance/05_design.md", initial_plan["files"])
                self.assertNotIn(".resonance/05_design.md", initial_plan["writes"])
                update.apply(source, target, "9.9.9", "source")
                (source / ".forge" / "tool.py").write_text("raise SystemExit('v2')\n", encoding="utf-8")
                self.commit(source)

                work = update.plan(source, target, "source")
                self.assertNotIn(".resonance/05_design.md", work["writes"])
                self.assertNotIn(".resonance/05_design.md", work["removes"])
                self.assertNotIn(".resonance/05_design.md", work["conflicts"])
                update.apply(source, target, "9.9.9", "source")

                self.assertEqual(design_entry, design.read_text(encoding="utf-8"))

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

    def test_source_profile_packages_required_eval_fixtures_and_oracle(self):
        td, source, target = self.fixture()
        self.addCleanup(td.cleanup)

        oracle_paths = integrity.oracle_files()
        for original in oracle_paths:
            relative = original.relative_to(ROOT)
            destination = source / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, destination)
        shutil.copy2(ROOT / ".forge" / "eval_fixture_manifest.json",
                     source / ".forge" / "eval_fixture_manifest.json")
        self.commit(source)

        source_package = update.source_files(source, profile="source")
        required_fixtures = {
            dependency
            for case_path in (ROOT / ".forge" / "skills").glob("**/evals/*.json")
            for dependency in json.loads(case_path.read_text(encoding="utf-8")).get("files", [])
            if not json.loads(case_path.read_text(encoding="utf-8")).get("fixture_optional", False)
        }
        self.assertTrue(required_fixtures)
        self.assertTrue(all(path.startswith(".forge/fixtures/") for path in required_fixtures))
        self.assertTrue(required_fixtures.issubset(source_package))

        for relative, original in source_package.items():
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, destination)
        checked = subprocess.run(
            [sys.executable, str(target / ".forge" / "eval_integrity.py")],
            cwd=target, capture_output=True, text=True,
        )
        self.assertEqual(0, checked.returncode, checked.stdout + checked.stderr)
        self.assertIn("0 problem(s)", checked.stdout)

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
