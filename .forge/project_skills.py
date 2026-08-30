#!/usr/bin/env python3
"""Lock and verify repository-owned skills without claiming framework files."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".agents" / "skills"
FRAMEWORK_MANIFEST = ROOT / ".resonance" / "framework-manifest.json"
LOCK = ROOT / ".resonance" / "project-skills.lock.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def framework_files(path: Path = FRAMEWORK_MANIFEST) -> set[str]:
    if not path.is_file():
        raise ValueError(
            f"framework ownership manifest is required before locking project skills: {path}"
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != 1 or not isinstance(data.get("files"), dict):
        raise ValueError(f"invalid framework ownership manifest: {path}")
    return set(data["files"])


def project_skill_lock(skills: Path = SKILLS, owned: set[str] | None = None) -> dict:
    owned = framework_files() if owned is None else owned
    entries = []
    if not skills.is_dir():
        return {"schema_version": 1, "skills": []}
    repo = skills.parent.parent
    for skill_md in sorted(skills.glob("**/SKILL.md")):
        directory = skill_md.parent
        files = sorted(path for path in directory.rglob("*") if path.is_file())
        rels = [path.relative_to(repo).as_posix() for path in files]
        claimed = [rel in owned for rel in rels]
        if any(claimed) and not all(claimed):
            raise ValueError(
                f"mixed framework/project ownership in {directory.relative_to(skills).as_posix()}"
            )
        if all(claimed):
            continue
        entries.append({
            "id": directory.relative_to(skills).as_posix(),
            "files": {rel: digest(path) for rel, path in zip(rels, files)},
        })
    return {"schema_version": 1, "skills": entries}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="repository root whose framework manifest and project skills are checked",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    skills = root / ".agents" / "skills"
    manifest = root / ".resonance" / "framework-manifest.json"
    output = args.output or (root / ".resonance" / "project-skills.lock.json")
    payload = json.dumps(
        project_skill_lock(skills, framework_files(manifest)),
        indent=2,
        sort_keys=True,
    ) + "\n"
    if args.check:
        if not output.is_file() or output.read_text(encoding="utf-8") != payload:
            print(f"project skill lock is missing or stale: {output}")
            return 1
        print(f"project skill lock is current: {output}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(payload, encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
