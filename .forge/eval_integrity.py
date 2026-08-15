#!/usr/bin/env python3
"""Hash and verify files that define the eval oracle."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

FORGE = Path(__file__).resolve().parent
REPO = FORGE.parent
MANIFEST = FORGE / "eval_fixture_manifest.json"


def oracle_files() -> list[Path]:
    files = list((FORGE / "skills").glob("**/evals/*.json"))
    files += list((FORGE / "tests").glob("test_*.py"))
    files += list((FORGE / "orch_evals").glob("*.json"))
    files += [FORGE / "run_evals.py", FORGE / "eval_integrity.py", FORGE / "orch_eval.py"]
    return sorted(p for p in files if p.is_file())


def snapshot() -> dict[str, str]:
    return {p.relative_to(REPO).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in oracle_files()}


def tier(path: Path) -> str:
    if "/evals/" not in path.as_posix():
        return "T1-tooling"
    try:
        case = json.loads(path.read_text(encoding="utf-8"))
        return "T2-deterministic" if case.get("checks") else "T1-structural"
    except Exception:
        return "T0-invalid"


def load() -> dict[str, str]:
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        return data["files"]
    except Exception:
        return {}


def verify(expected: dict[str, str] | None = None) -> list[str]:
    expected = load() if expected is None else expected
    actual = snapshot()
    problems = []
    for path in sorted(set(expected) | set(actual)):
        if path not in actual:
            problems.append(f"deleted oracle file: {path}")
        elif path not in expected:
            problems.append(f"unregistered oracle file: {path}")
        elif actual[path] != expected[path]:
            problems.append(f"changed oracle file: {path}")
    return problems


def write() -> None:
    MANIFEST.write_text(json.dumps({"schema": 1, "algorithm": "sha256", "files": snapshot(),
                                    "tiers": {p.relative_to(REPO).as_posix(): tier(p)
                                              for p in oracle_files()}},
                                   indent=2) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Verify immutable eval fixtures")
    ap.add_argument("--update", action="store_true", help="record an intentional fixture change")
    args = ap.parse_args(argv)
    if args.update:
        write()
        print(f"wrote {MANIFEST.relative_to(REPO)}")
        return 0
    problems = verify()
    for problem in problems:
        print(f"ERROR {problem}")
    print(f"eval oracle: {len(snapshot())} files, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
