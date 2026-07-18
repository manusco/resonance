"""Tests for the state-ledger checks in validate_library.py (stdlib only).

The ledger is the typed layer of .resonance/. These tests build a temp ledger,
chdir into it (the checker reads .resonance/ledger relative to cwd), and assert
the deterministic rules: required fields, id grammar, wrong-file placement,
dangling edges, supersede reciprocity, the schema marker, and the grace rule
(no ledger dir means no checks).
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

FORGE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FORGE_DIR))
import validate_library  # noqa: E402

HEADER = "# {title}\nschema: resonance-ledger/1\n\n"

GOOD = {
    "decisions": HEADER.format(title="Decisions") + (
        "## dec-a: first call\ntype: decision\ncreated: 2026-07-18\n"
        "status: superseded\nsuperseded_by: dec-b\n\nold reasoning\n\n"
        "## dec-b: second call\ntype: decision\ncreated: 2026-07-19\n"
        "status: active\nsupersedes: dec-a\nevidences: met-x\n\nnew reasoning\n"
    ),
    "lessons": HEADER.format(title="Lessons"),
    "metrics": HEADER.format(title="Metrics") + (
        "## met-x: a reading\ntype: metric\ncreated: 2026-07-01\nstatus: closed\n"
        "value: 10\nunit: eur\nas_of: 2026-06-30\nsource: manual\n"
    ),
    "customers": HEADER.format(title="Customers"),
    "experiments": HEADER.format(title="Experiments"),
}


def _write_ledger(root: Path, files: dict) -> None:
    ldir = root / ".resonance" / "ledger"
    ldir.mkdir(parents=True)
    for name, content in files.items():
        (ldir / f"{name}.md").write_text(content, encoding="utf-8")


class LedgerCheckTest(unittest.TestCase):
    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def _run(self, files):
        _write_ledger(Path(self._tmp.name), files)
        errors, warnings = [], []
        validate_library._ledger_checks(errors, warnings)
        return errors

    def test_good_ledger_passes(self):
        self.assertEqual(self._run(GOOD), [])

    def test_grace_rule_no_ledger_dir(self):
        # No .resonance/ledger at all: legacy brain, zero checks, zero errors.
        errors, warnings = [], []
        validate_library._ledger_checks(errors, warnings)
        self.assertEqual(errors, [])

    def test_missing_required_field(self):
        f = dict(GOOD)
        f["metrics"] = HEADER.format(title="Metrics") + (
            "## met-x: a reading\ntype: metric\ncreated: 2026-07-01\nstatus: closed\n"
            "value: 10\nunit: eur\nas_of: 2026-06-30\n"  # no source
        )
        self.assertTrue(any("source" in e for e in self._run(f)))

    def test_missing_schema_marker(self):
        f = dict(GOOD)
        f["lessons"] = "# Lessons\n\nno marker here\n"
        self.assertTrue(any("marker" in e for e in self._run(f)))

    def test_wrong_file_placement(self):
        f = dict(GOOD)
        f["lessons"] = HEADER.format(title="Lessons") + (
            "## met-y: misplaced\ntype: metric\ncreated: 2026-07-01\nstatus: active\n"
        )
        self.assertTrue(any("belongs in met" in e for e in self._run(f)))

    def test_dangling_edge(self):
        f = dict(GOOD)
        f["decisions"] = HEADER.format(title="Decisions") + (
            "## dec-c: cites nothing real\ntype: decision\ncreated: 2026-07-18\n"
            "status: active\nevidences: met-does-not-exist\n"
        )
        self.assertTrue(any("missing id 'met-does-not-exist'" in e for e in self._run(f)))

    def test_supersede_without_backref(self):
        f = dict(GOOD)
        # dec-a is active (not superseded) and lacks superseded_by, but dec-b supersedes it.
        f["decisions"] = HEADER.format(title="Decisions") + (
            "## dec-a: first\ntype: decision\ncreated: 2026-07-18\nstatus: active\n\nx\n\n"
            "## dec-b: second\ntype: decision\ncreated: 2026-07-19\nstatus: active\n"
            "supersedes: dec-a\n"
        )
        errs = self._run(f)
        self.assertTrue(any("not status:superseded" in e for e in errs))
        self.assertTrue(any("superseded_by" in e for e in errs))

    def test_bad_status_enum(self):
        f = dict(GOOD)
        f["customers"] = HEADER.format(title="Customers") + (
            "## cus-z: acme\ntype: customer\ncreated: 2026-07-18\nstatus: vip\n"
        )
        self.assertTrue(any("status 'vip'" in e for e in self._run(f)))

    def test_bad_due_date_is_flagged(self):
        # A DONE_PENDING_OUTCOME entry keys the pull on due:; a typo'd due date
        # would silently never fire, so it must fail validation.
        f = dict(GOOD)
        f["experiments"] = HEADER.format(title="Experiments") + (
            "## exp-x: a pending test\ntype: experiment\ncreated: 2026-07-18\n"
            "status: active\nhypothesis: it lifts conversion\ndue: 2026-13-99\n"
        )
        self.assertTrue(any("due" in e and "ISO date" in e for e in self._run(f)))


if __name__ == "__main__":
    unittest.main()
