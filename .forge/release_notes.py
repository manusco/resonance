#!/usr/bin/env python3
"""Validate release metadata and extract notes from CHANGELOG.md. Pure stdlib."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def parse_version(value: str) -> tuple[int, int, int]:
    match = SEMVER.fullmatch(value)
    if not match:
        raise ValueError(f"version must use MAJOR.MINOR.PATCH: {value}")
    return tuple(int(part) for part in match.groups())


def package_version(root: Path = ROOT) -> str:
    data = json.loads((root / "package.json").read_text(encoding="utf-8"))
    version = str(data["version"])
    parse_version(version)
    return version


def extract_notes(changelog: str, version: str) -> str:
    lines = changelog.splitlines()
    heading = f"## v{version}"
    try:
        start = lines.index(heading) + 1
    except ValueError as exc:
        raise ValueError(f"CHANGELOG.md has no exact {heading} heading") from exc

    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## v"):
            end = index
            break

    notes = "\n".join(lines[start:end]).strip()
    if not notes:
        raise ValueError(f"{heading} has no release notes")
    return notes + "\n"


def existing_versions(root: Path = ROOT) -> list[tuple[int, int, int]]:
    result = subprocess.run(
        ["git", "tag", "--list", "v*"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    versions = []
    for tag in result.stdout.splitlines():
        match = SEMVER.fullmatch(tag.removeprefix("v"))
        if match:
            versions.append(tuple(int(part) for part in match.groups()))
    return versions


def validate_release(version: str, root: Path = ROOT) -> None:
    candidate = parse_version(version)
    versions = existing_versions(root)
    if candidate in versions:
        raise ValueError(f"tag v{version} already exists")
    if versions and candidate <= max(versions):
        latest = ".".join(str(part) for part in max(versions))
        raise ValueError(f"v{version} must be greater than existing tag v{latest}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate version and changelog notes")
    parser.add_argument("--check-release", action="store_true", help="also require a new increasing tag")
    parser.add_argument("--print-version", action="store_true", help="print the package version")
    parser.add_argument("--output", type=Path, help="write current release notes to this file")
    args = parser.parse_args(argv)

    try:
        version = package_version()
        notes = extract_notes((ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), version)
        if args.check_release:
            validate_release(version)
        if args.print_version:
            print(version)
        if args.output:
            args.output.write_text(notes, encoding="utf-8")
        if args.check or args.check_release:
            print(f"release metadata valid for v{version}")
    except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        print(f"release metadata invalid: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
