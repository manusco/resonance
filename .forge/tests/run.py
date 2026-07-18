"""Run the Forge tooling unit tests (stdlib only). Exit 1 on any failure.

Usage: py .forge/tests/run.py
Wired into the pre-push ship-gate so a tooling regression cannot ship silently.
"""
import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent


def main() -> int:
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(TESTS_DIR), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
