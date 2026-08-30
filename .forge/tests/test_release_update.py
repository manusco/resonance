"""Offline integration tests for the release-to-updater boundary."""
import contextlib
import http.client
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("release_update_helper", ROOT / ".forge/releases.py")
releases = importlib.util.module_from_spec(spec)
spec.loader.exec_module(releases)


class ReleaseUpdateTests(unittest.TestCase):
    def test_cache_never_falls_back_into_project_local_temp(self):
        with mock.patch.object(releases.sys, "platform", "linux"), \
                mock.patch.dict(releases.os.environ, {"XDG_CACHE_HOME": str(self.target / "cache")}), \
                mock.patch.object(releases.tempfile, "gettempdir", return_value=str(self.target / "tmp")):
            self.assertFalse(releases.cache_file(self.target).resolve().is_relative_to(self.target.resolve()))

    def test_malformed_http_is_a_quiet_cached_failure(self):
        cache = self.root / "cache.json"
        self.fetch.side_effect = http.client.BadStatusLine("invalid response")
        result = releases.check_update(self.target, cache_path=cache, now=100000)
        self.assertEqual(result["status"], "unavailable")
        self.assertFalse(result["notify"])
        releases.check_update(self.target, cache_path=cache, now=100001)
        self.fetch.assert_called_once()

    def test_windows_apply_command_is_powershell_safe(self):
        args = ["C:\\Program Files\\Python\\python.exe", "C:\\Users\\O'Brien\\$project\\releases.py",
                "update", "--apply"]
        self.assertEqual(releases.format_command(args, windows=True),
                         "& 'C:\\Program Files\\Python\\python.exe' "
                         "'C:\\Users\\O''Brien\\$project\\releases.py' 'update' '--apply'")

    def test_session_and_wake_entrypoints_run_quiet_check(self):
        for name in ("AGENTS.md", "resonance.sh", "resonance.ps1"):
            with self.subTest(name=name):
                self.assertIn("releases.py", (ROOT / name).read_text())
                self.assertIn("check --quiet", (ROOT / name).read_text())

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "upstream"
        self.target = self.root / "project"
        (self.source / ".forge").mkdir(parents=True)
        (self.source / ".agents/skills/example").mkdir(parents=True)
        (self.source / ".agents/skills/example/SKILL.md").write_text("example")
        (self.target / ".resonance").mkdir(parents=True)
        (self.target / ".resonance/framework-manifest.json").write_text(
            json.dumps({"schema": 1, "version": "2.5.2", "files": {}}))
        (self.source / "package.json").write_text(json.dumps(
            {"name": "@manusco/resonance", "version": "2.6.0"}))
        for name in ("AGENTS.md", "resonance.sh", "resonance.ps1"):
            (self.source / name).write_text("fixture")
        (self.source / ".forge/update.py").write_text(
            "import json, sys\n"
            "from pathlib import Path\n"
            "target = Path(sys.argv[sys.argv.index('--target') + 1])\n"
            "if '--apply' in sys.argv: (target / 'applied').write_text('yes')\n"
            "print(json.dumps({'version': '2.6.0', 'writes': [], 'removes': [], 'conflicts': []}))\n")
        self.git("init")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.test")
        self.git("add", ".")
        self.git("commit", "-m", "fixture")
        self.git("tag", "v2.6.0")
        self.revision = self.git("rev-parse", "HEAD").stdout.strip()
        self.release = {"version": "2.6.0", "tag": "v2.6.0",
                        "url": "https://github.com/manusco/resonance/releases/tag/v2.6.0"}
        real_run = subprocess.run

        def local_clone(args, **kwargs):
            args = [str(self.source) if arg == releases.REPOSITORY else arg for arg in args]
            return real_run(args, **kwargs)

        self.run_mock = mock.patch.object(releases.subprocess, "run", side_effect=local_clone)
        self.run_mock.start()
        self.addCleanup(self.run_mock.stop)
        self.fetch = mock.patch.object(releases, "fetch_release", return_value=self.release).start()
        self.addCleanup(mock.patch.stopall)

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.source, check=True,
                              capture_output=True, text=True)

    def test_preview_does_not_write_target_and_prints_exact_apply_pin(self):
        before = sorted(p.relative_to(self.target) for p in self.target.rglob("*"))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(releases.run_update(self.target), 0)
        self.assertIn(self.revision, out.getvalue())
        self.assertIn("--version 2.6.0", out.getvalue())
        self.assertIn("--revision", out.getvalue())
        self.assertEqual(before, sorted(p.relative_to(self.target) for p in self.target.rglob("*")))

    def test_apply_requires_exact_version_and_revision_before_network(self):
        for version, revision in (("latest", self.revision), ("2.6.0", None),
                                  ("2.6.0", "HEAD")):
            with self.subTest(version=version, revision=revision), self.assertRaises(ValueError):
                releases.run_update(self.target, version, apply=True, revision=revision)
        self.fetch.assert_not_called()

    def test_apply_runs_the_previewed_release_updater(self):
        self.assertEqual(releases.run_update(self.target, "2.6.0", apply=True,
                                            revision=self.revision), 0)
        self.assertEqual((self.target / "applied").read_text(), "yes")

    def test_moved_tag_cannot_execute_another_updater(self):
        with self.assertRaisesRegex(ValueError, "commit|revision"):
            releases.run_update(self.target, "2.6.0", apply=True, revision="0" * 40)
        self.assertFalse((self.target / "applied").exists())

    def test_missing_manifest_requires_adoption_without_network(self):
        (self.target / ".resonance/framework-manifest.json").unlink()
        with self.assertRaisesRegex(ValueError, "adopt|installed"):
            releases.run_update(self.target)
        self.fetch.assert_not_called()

    def test_newer_install_is_not_downgraded_by_latest(self):
        (self.target / ".resonance/framework-manifest.json").write_text(
            json.dumps({"schema": 1, "version": "3.0.0", "files": {}}))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(releases.run_update(self.target), 0)
        self.assertFalse((self.target / "applied").exists())

    def test_incomplete_source_is_rejected_before_execution(self):
        (self.source / "AGENTS.md").unlink()
        self.git("add", ".")
        self.git("commit", "-m", "incomplete")
        self.git("tag", "-f", "v2.6.0")
        with self.assertRaisesRegex(ValueError, "source|missing|incomplete"):
            releases.run_update(self.target)

    def test_package_version_mismatch_is_rejected(self):
        (self.source / "package.json").write_text(
            '{"name":"@manusco/resonance","version":"2.7.0"}')
        self.git("add", ".")
        self.git("commit", "-m", "wrong version")
        self.git("tag", "-f", "v2.6.0")
        with self.assertRaisesRegex(ValueError, "version"):
            releases.run_update(self.target)


if __name__ == "__main__":
    unittest.main()
