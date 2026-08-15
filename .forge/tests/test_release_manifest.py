"""Tests for deterministic release evidence generation."""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

FORGE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FORGE))

import release_manifest  # noqa: E402


class ReleaseManifestTest(unittest.TestCase):
    def test_manifest_is_commit_deterministic(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            cwd = os.getcwd()
            try:
                os.chdir(root)
                subprocess.run(["git", "init"], check=True, stdout=subprocess.DEVNULL)
                subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
                subprocess.run(["git", "config", "user.name", "Test"], check=True)
                Path("package.json").write_text('{"version":"9.9.9"}\n', encoding="utf-8")
                Path("tracked.txt").write_text("first\n", encoding="utf-8")
                subprocess.run(["git", "add", "package.json", "tracked.txt"], check=True)
                env = {
                    **os.environ,
                    "GIT_AUTHOR_DATE": "2026-08-15T00:00:00+00:00",
                    "GIT_COMMITTER_DATE": "2026-08-15T00:00:00+00:00",
                }
                subprocess.run(["git", "commit", "-m", "fixture"], check=True, env=env,
                               stdout=subprocess.DEVNULL)

                release_manifest.main(["--output", "dist/one.json", "--checksums", "dist/one.SHA256SUMS"])
                first = Path("dist/one.json").read_bytes()
                Path("tracked.txt").write_text("dirty worktree ignored for release tree\n", encoding="utf-8")
                release_manifest.main(["--output", "dist/two.json", "--checksums", "dist/two.SHA256SUMS"])
                second = Path("dist/two.json").read_bytes()
                self.assertEqual(first, second)
            finally:
                os.chdir(cwd)


if __name__ == "__main__":
    unittest.main()
