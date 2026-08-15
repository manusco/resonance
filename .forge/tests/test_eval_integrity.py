import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("eval_integrity_tested", ROOT / ".forge" / "eval_integrity.py")
integrity = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = integrity
spec.loader.exec_module(integrity)


class EvalIntegrityTests(unittest.TestCase):
    def test_snapshot_covers_evals_and_tests(self):
        files = integrity.snapshot()
        self.assertTrue(any("/evals/" in p for p in files))
        self.assertTrue(any(p.endswith("test_eval_integrity.py") for p in files))

    def test_snapshot_detects_deleted_or_changed_oracle(self):
        current = integrity.snapshot()
        path = next(iter(current))
        altered = dict(current)
        altered[path] = "0" * 64
        self.assertTrue(any(path in problem for problem in integrity.verify(altered)))


if __name__ == "__main__":
    unittest.main()
