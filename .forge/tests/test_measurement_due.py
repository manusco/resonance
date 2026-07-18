"""Tests for measurement_due.py: the pull that closes DONE_PENDING_OUTCOME.

Builds a temp ledger, chdirs in, and asserts that only active entries whose due
date has arrived are surfaced, and that a missing ledger or nothing-due is silent.
Stdlib only.
"""
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

FORGE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FORGE_DIR))
import measurement_due  # noqa: E402

METRICS = (
    "# Metrics\nschema: resonance-ledger/1\n\n"
    "## met-arr-q3: ARR check\ntype: metric\ncreated: 2026-07-01\nstatus: active\n"
    "value: 0\nunit: eur\nas_of: 2026-07-01\nsource: stripe\ndue: 2026-08-01\n\n"
    "## met-later: not yet\ntype: metric\ncreated: 2026-07-01\nstatus: active\n"
    "value: 0\nunit: eur\nas_of: 2026-07-01\nsource: stripe\ndue: 2026-12-01\n\n"
    "## met-closed: already in\ntype: metric\ncreated: 2026-07-01\nstatus: closed\n"
    "value: 100\nunit: eur\nas_of: 2026-07-31\nsource: stripe\ndue: 2026-07-01\n"
)


def _write(root: Path, metrics: str) -> None:
    ldir = root / ".resonance" / "ledger"
    ldir.mkdir(parents=True)
    (ldir / "metrics.md").write_text(metrics, encoding="utf-8")
    (ldir / "experiments.md").write_text("# Experiments\nschema: resonance-ledger/1\n", encoding="utf-8")


class MeasurementDueTest(unittest.TestCase):
    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def _run(self, date):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = measurement_due.main(["--date", date])
        return code, buf.getvalue()

    def test_due_entry_surfaces(self):
        _write(Path(self._tmp.name), METRICS)
        code, out = self._run("2026-08-01")
        self.assertEqual(code, 0)
        self.assertIn("met-arr-q3", out)          # due 2026-08-01, arrived
        self.assertNotIn("met-later", out)         # due 2026-12-01, not yet
        self.assertNotIn("met-closed", out)        # already closed

    def test_silent_when_nothing_due(self):
        _write(Path(self._tmp.name), METRICS)
        code, out = self._run("2026-07-15")        # before the first due date
        self.assertEqual(code, 0)
        self.assertEqual(out, "")

    def test_silent_without_ledger(self):
        code, out = self._run("2026-08-01")        # no .resonance/ledger here
        self.assertEqual(code, 0)
        self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()
