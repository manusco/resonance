import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


guard = load("guard_gates", ROOT / ".forge" / "hooks" / "guard.py")


class StagedBlobTests(unittest.TestCase):
    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, check=True,
                              capture_output=True, text=True)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.git("init")
        self.git("config", "user.email", "test@example.test")
        self.git("config", "user.name", "Test")

    def tearDown(self):
        self.tmp.cleanup()

    def test_staged_bad_worktree_clean_scans_staged_blob(self):
        p = self.repo / "config.toml"
        field = "to" + "ken"
        sample_value = "abcdefgh" + "ijklmnop"
        p.write_text(f'{field} = "{sample_value}"\n', encoding="utf-8")
        self.git("add", "config.toml")
        p.write_text("clean = true\n", encoding="utf-8")
        old = Path.cwd()
        os.chdir(self.repo)
        try:
            problems = []
            guard.check("config.toml", problems, text=guard.staged_text("config.toml"))
        finally:
            os.chdir(old)
        self.assertTrue(any("secret" in p for p in problems))

    def test_staged_clean_worktree_bad_does_not_block(self):
        p = self.repo / "settings"
        p.write_text("clean=true\n", encoding="utf-8")
        self.git("add", "settings")
        field = "to" + "ken"
        sample_value = "abcdefgh" + "ijklmnop"
        p.write_text(f'{field}="{sample_value}"\n', encoding="utf-8")
        old = Path.cwd()
        os.chdir(self.repo)
        try:
            problems = []
            guard.check("settings", problems, text=guard.staged_text("settings"))
        finally:
            os.chdir(old)
        self.assertEqual(problems, [])

    def test_utf16_staged_secret_is_scanned(self):
        p = self.repo / ".env"
        field = "to" + "ken"
        sample_value = "abcdefgh" + "ijklmnop"
        p.write_text(f'{field}="{sample_value}"\n', encoding="utf-16")
        self.git("add", ".env", "--force")
        old = Path.cwd()
        os.chdir(self.repo)
        try:
            problems = []
            guard.check(".env", problems, text=guard.staged_text(".env"))
        finally:
            os.chdir(old)
        self.assertTrue(any("secret" in problem for problem in problems))


class DiscoveryFailureTests(unittest.TestCase):
    @mock.patch.object(guard.subprocess, "run")
    def test_staged_file_discovery_fails_closed(self, run):
        run.return_value = subprocess.CompletedProcess([], 1, "", "git failed")
        with self.assertRaises(RuntimeError):
            guard.staged_files()


if __name__ == "__main__":
    unittest.main()
