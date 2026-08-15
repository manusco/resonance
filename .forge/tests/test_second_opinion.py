"""Tests for the second-opinion dispatch gate.

The script must not claim an independent review when the reviewer is missing,
same-identity, empty, failed, oversized, or unsafe to dispatch.
"""
import importlib.util
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("second_opinion", ROOT / "second_opinion.py")
second_opinion = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(second_opinion)


class SecondOpinionDispatchTest(unittest.TestCase):
    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        self._env = os.environ.copy()
        os.environ.pop("RESONANCE_REVIEW_CMD", None)
        os.environ.pop("RESONANCE_REVIEWER_ID", None)
        os.environ.pop("RESONANCE_AUTHOR_ID", None)

    def tearDown(self):
        os.chdir(self._cwd)
        os.environ.clear()
        os.environ.update(self._env)
        self._tmp.cleanup()

    def _run(self, *argv) -> tuple[int, str]:
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = second_opinion.main(list(argv))
        return rc, buf.getvalue()

    def _model_cmd(self, body: str) -> str:
        path = Path(self._tmp.name) / f"model_{abs(hash(body))}.py"
        path.write_text(body, encoding="utf-8")
        return f'"{sys.executable}" "{path}"'

    def test_missing_command_is_incomplete(self):
        rc, out = self._run("--diff", "diff --git a/x b/x\n+ok\n")
        self.assertEqual(rc, 3)
        self.assertIn("INCOMPLETE", out)
        self.assertIn("Artifact hash", out)

    def test_same_identity_is_not_independent(self):
        rc, out = self._run("--diff", "diff --git a/x b/x\n+ok\n",
                            "--model-cmd", self._model_cmd("print('ok')\n"),
                            "--author-id", "same", "--reviewer-id", "same")
        self.assertEqual(rc, 3)
        self.assertIn("matches author", out)

    def test_secret_blocks_dispatch(self):
        secret_line = "+ " + "api" + "_key = 'abcdefghijklmnopqrstuvwxyz'\n"
        rc, out = self._run("--diff", secret_line,
                            "--model-cmd", self._model_cmd("print('ok')\n"),
                            "--reviewer-id", "reviewer")
        self.assertEqual(rc, 2)
        self.assertIn("secret", out.lower())

    def test_oversize_blocks_dispatch(self):
        rc, out = self._run("--diff", "x" * 20, "--max-chars", "5",
                            "--model-cmd", self._model_cmd("print('ok')\n"),
                            "--reviewer-id", "reviewer")
        self.assertEqual(rc, 2)
        self.assertIn("too large", out)

    def test_empty_output_fails(self):
        rc, out = self._run("--diff", "diff --git a/x b/x\n+ok\n",
                            "--model-cmd", self._model_cmd(""),
                            "--reviewer-id", "reviewer")
        self.assertEqual(rc, 1)
        self.assertIn("empty output", out)

    def test_decision_mode_succeeds_with_identity_and_output(self):
        rc, out = self._run("--mode", "decision", "--artifact", "Adopt X because Y",
                            "--model-cmd", self._model_cmd("print('assumptions: ok')\n"),
                            "--reviewer-id", "reviewer")
        self.assertEqual(rc, 0)
        self.assertIn("mode=decision", out)
        self.assertIn("assumptions: ok", out)


if __name__ == "__main__":
    unittest.main()
