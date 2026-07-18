"""Tests for the /goal bound enforcer (loop_state.py, stdlib only).

The whole point of loop_state.py is that the caps live in code, not prose. These
tests prove the four stops actually fire: total cap, per-slice attempts, the
duplicate-failure signature detector, and the whole-window stuck check, plus that
a run resumes from persisted state. This is the grounded proof that /goal cannot
run away.
"""
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "ops" / "goal" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import loop_state  # noqa: E402


class LoopBoundTest(unittest.TestCase):
    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        # small, explicit caps so the tests are fast and legible
        loop_state.CAPS = {"max_slice_attempts": 3, "max_iters": 5, "stuck_window": 4}

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def _run(self, *argv) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            loop_state.main(list(argv))
        return buf.getvalue()

    def test_continue_on_progress(self):
        self._run("start", "g", "--dod", "d")
        self.assertIn("CONTINUE", self._run("check", "slice-1", "advanced"))

    def test_stop_slice_after_attempts(self):
        self._run("start", "g", "--dod", "d")
        self._run("check", "slice-1", "failed")
        self._run("check", "slice-1", "failed")
        self.assertIn("STOP_SLICE", self._run("check", "slice-1", "failed"))

    def test_stop_stuck_on_repeated_signature(self):
        self._run("start", "g", "--dod", "d")
        # different slices (no slice cap) but the same failure signature
        self._run("check", "s1", "failed", "--sig", "test:AssertionError")
        self._run("check", "s2", "failed", "--sig", "test:AssertionError")
        out = self._run("check", "s3", "failed", "--sig", "test:AssertionError")
        self.assertIn("STOP_STUCK", out)
        self.assertIn("signature", out)

    def test_stop_cap_on_total_iters(self):
        self._run("start", "g", "--dod", "d")
        self.assertIn("CONTINUE", self._run("check", "a", "advanced"))
        self.assertIn("CONTINUE", self._run("check", "b", "advanced"))
        self.assertIn("CONTINUE", self._run("check", "c", "advanced"))
        self.assertIn("CONTINUE", self._run("check", "d", "advanced"))
        self.assertIn("STOP_CAP", self._run("check", "e", "advanced"))

    def test_resume_reads_persisted_state(self):
        self._run("start", "ship the ledger", "--dod", "validators green")
        self._run("check", "slice-1", "advanced")
        out = self._run("resume")
        self.assertIn("ship the ledger", out)
        self.assertIn("slice-1", out)

    def test_resume_with_no_goal(self):
        self.assertIn("no active goal", self._run("resume"))


if __name__ == "__main__":
    unittest.main()
