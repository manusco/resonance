#!/usr/bin/env python3
"""Hash and verify files that define the eval oracle."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from pathlib import PureWindowsPath

FORGE = Path(__file__).resolve().parent
REPO = FORGE.parent
MANIFEST = FORGE / "eval_fixture_manifest.json"
SENSITIVE_NAMES = {".env", ".npmrc", ".pypirc", "credentials", "credentials.json"}
SENSITIVE_SUFFIXES = {".key", ".pem", ".p12", ".pfx"}
ALLOWED_FIXTURE_ROOTS = {"src", "docs", "tests", "fixtures", "examples"}


def contained_fixture(relpath: str, repo_root: Path = REPO) -> Path:
    """Resolve a public eval input under an approved repository fixture root."""
    if not isinstance(relpath, str) or not relpath.strip():
        raise ValueError("eval file path must be a non-empty repository-relative path")
    candidate = Path(relpath)
    windows = PureWindowsPath(relpath)
    if (candidate.is_absolute() or windows.is_absolute() or windows.drive
            or ".." in candidate.parts or "\\" in relpath):
        raise ValueError(f"eval file escapes repository: {relpath}")
    framework_fixture = len(candidate.parts) >= 3 and candidate.parts[:2] == (".forge", "fixtures")
    if not candidate.parts or (candidate.parts[0] not in ALLOWED_FIXTURE_ROOTS and not framework_fixture):
        raise ValueError(f"eval file is outside approved fixture roots: {relpath}")
    repo_root = Path(repo_root).resolve()
    resolved = (repo_root / candidate).resolve(strict=False)
    try:
        resolved.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(f"eval file escapes repository: {relpath}") from exc
    if framework_fixture:
        fixture_root = repo_root / ".forge" / "fixtures"
        if (repo_root / ".forge").is_symlink() or fixture_root.is_symlink():
            raise ValueError(f"eval fixture namespace traverses a symlink: {relpath}")
        try:
            resolved.relative_to(fixture_root)
        except ValueError as exc:
            raise ValueError(f"eval fixture escapes framework fixture namespace: {relpath}") from exc
    if resolved.name.lower() in SENSITIVE_NAMES or resolved.suffix.lower() in SENSITIVE_SUFFIXES:
        raise ValueError(f"eval file is sensitive and cannot be sent to a model: {relpath}")
    return resolved


def repository_candidate_files() -> list[Path]:
    """Return tracked and non-ignored untracked files, with a non-Git test fallback."""
    listed = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=REPO, capture_output=True,
    )
    if listed.returncode == 0:
        return [REPO / raw.decode("utf-8", errors="strict")
                for raw in listed.stdout.split(b"\0") if raw]
    files = []
    for root, dirs, names in os.walk(REPO):
        dirs[:] = [name for name in dirs if name not in {".git", "node_modules", "__pycache__"}]
        files.extend(Path(root) / name for name in names)
    return files


def oracle_files() -> list[Path]:
    # Protected validation and sealed promotion datasets stay external by contract.
    # Only their public runner and security tests belong in this repository oracle.
    files = list((FORGE / "skills").glob("**/evals/*.json"))
    files += list((FORGE / "tests").glob("test_*.py"))
    files += list((FORGE / "orch_evals").glob("*.json"))
    files += list((FORGE / "routing_evals").glob("*.json"))
    files += [FORGE / "run_evals.py", FORGE / "eval_integrity.py", FORGE / "orch_eval.py",
              FORGE / "routing_eval.py"]
    result = {p.resolve() for p in files if p.is_file()}
    problems = []
    for case_path in (FORGE / "skills").glob("**/evals/*.json"):
        try:
            case = json.loads(case_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            problems.append(f"invalid eval case {case_path.relative_to(REPO).as_posix()}: {exc}")
            continue
        if not isinstance(case, dict):
            problems.append(f"invalid eval case {case_path.relative_to(REPO).as_posix()}: expected object")
            continue
        dependencies = case.get("files", [])
        if dependencies is None:
            dependencies = []
        if not isinstance(dependencies, list):
            problems.append(f"invalid eval files list: {case_path.relative_to(REPO).as_posix()}")
            continue
        for relpath in dependencies:
            try:
                fixture = contained_fixture(relpath, REPO)
            except (OSError, ValueError) as exc:
                problems.append(f"invalid eval fixture in {case_path.relative_to(REPO).as_posix()}: {exc}")
                continue
            if not fixture.is_file():
                if case.get("fixture_optional") is True:
                    continue
                problems.append(
                    f"missing required eval fixture {relpath} referenced by "
                    f"{case_path.relative_to(REPO).as_posix()}"
                )
                continue
            result.add(fixture)
    if problems:
        raise ValueError("; ".join(problems))
    return sorted(result)


def snapshot() -> dict[str, str]:
    return {p.relative_to(REPO).as_posix(): hashlib.sha256(
                p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
            for p in oracle_files()}


def tier(path: Path) -> str:
    if "/routing_evals/" in path.as_posix():
        return "T1-routing"
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


def repository_protected_dataset_problems() -> list[str]:
    """Reject private routing custody envelopes accidentally placed in the repository."""
    problems = []
    for metadata_path in REPO.rglob("dataset.json"):
        if ".git" in metadata_path.parts:
            continue
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(metadata, dict) and metadata.get("role") in {
                "protected_validation", "sealed_promotion"}:
            problems.append(
                f"protected routing dataset must live outside repository: "
                f"{metadata_path.relative_to(REPO).as_posix()}"
            )
    return problems


def repository_private_eval_artifact_problems() -> list[str]:
    """Reject live evaluation records accidentally placed in the public repository."""
    problems = []
    for path in repository_candidate_files():
        if not path.is_file():
            continue
        rel = path.relative_to(REPO).as_posix()
        if rel.startswith(".forge/schemas/") or rel.startswith(".forge/tests/"):
            continue
        name = path.name.lower()
        if name in {"access-log.jsonl", "access.jsonl", "canary-cost-ledger.json"}:
            problems.append(f"private evaluation artifact must live outside repository: {rel}")
            continue
        if path.suffix.lower() == ".json":
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if (isinstance(data, dict)
                    and data.get("approval", {}).get("state") == "APPROVED"
                    and "datasets" in data and "canary" in data):
                problems.append(f"approved evaluation contract must live outside repository: {rel}")
            elif (isinstance(data, dict) and "recorded_total" in data
                  and isinstance(data.get("sessions"), list)):
                problems.append(f"private evaluation cost ledger must live outside repository: {rel}")
        elif path.suffix.lower() == ".jsonl":
            try:
                sample = path.read_text(encoding="utf-8", errors="replace")[:8192]
            except OSError:
                continue
            if '"type":"tool_use"' in sample.replace(" ", ""):
                problems.append(f"raw host trace must live outside repository: {rel}")
    return problems


def verify(expected: dict[str, str] | None = None) -> list[str]:
    expected = load() if expected is None else expected
    try:
        actual = snapshot()
    except (OSError, ValueError) as exc:
        return [f"invalid eval oracle: {exc}"]
    problems = []
    for path in sorted(set(expected) | set(actual)):
        if path not in actual:
            problems.append(f"deleted oracle file: {path}")
        elif path not in expected:
            problems.append(f"unregistered oracle file: {path}")
        elif actual[path] != expected[path]:
            problems.append(f"changed oracle file: {path}")
    problems.extend(repository_protected_dataset_problems())
    problems.extend(repository_private_eval_artifact_problems())
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
        try:
            write()
        except (OSError, ValueError) as exc:
            print(f"ERROR cannot update eval oracle: {exc}")
            return 1
        print(f"wrote {MANIFEST.relative_to(REPO)}")
        return 0
    problems = verify()
    for problem in problems:
        print(f"ERROR {problem}")
    print(f"eval oracle: {len(snapshot())} files, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
