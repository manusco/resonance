#!/usr/bin/env python3
"""Transactional Resonance installer and updater."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

MANIFEST = ".resonance/framework-manifest.json"
MANAGED_ROOTS = (".agents", ".forge", ".claude/skills", ".cursor/skills",
                 ".cursor/rules/resonance.mdc", ".opencode/commands", "AGENTS.md",
                 "CLAUDE.md", "resonance.ps1", "resonance.sh")
LEGACY_ROOTS = (".codex/prompts", ".opencode/command")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(root: Path, path: Path) -> Path:
    root = root.resolve()
    resolved = path.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes target: {path}") from exc
    return resolved


def source_files(source: Path, include_legacy: bool = False) -> dict[str, Path]:
    source = source.resolve()
    clean = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=source,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
    if clean.returncode != 0 or clean.stdout.strip():
        raise ValueError("source checkout must be clean; use a pinned tag or commit with no local changes")
    result = subprocess.run(["git", "ls-files", "-z"], cwd=source, capture_output=True)
    if result.returncode != 0:
        raise ValueError("source must be a Git checkout; install from a pinned tag or commit")
    tracked = [p.decode("utf-8", "strict") for p in result.stdout.split(b"\0") if p]
    files = {}
    for rel in tracked:
        roots = MANAGED_ROOTS + (LEGACY_ROOTS if include_legacy else ())
        if any(rel == root or rel.startswith(root.rstrip("/") + "/") for root in roots):
            path = source / rel
            if path.is_file():
                files[Path(rel).as_posix()] = path
    return files


def load_manifest(target: Path) -> dict:
    p = target / MANIFEST
    if not p.is_file():
        return {"schema": 1, "files": {}}
    data = json.loads(p.read_text(encoding="utf-8"))
    if data.get("schema") != 1 or not isinstance(data.get("files"), dict):
        raise ValueError(f"invalid ownership manifest: {p}")
    return data


def version(source: Path) -> str:
    return str(json.loads((source / "package.json").read_text(encoding="utf-8"))["version"])


def adopt(source: Path, target: Path) -> Path:
    """Record the exact bytes of a pre-manifest installation without changing them."""
    target = target.resolve()
    if (target / MANIFEST).exists():
        raise ValueError("ownership manifest already exists")
    incoming = source_files(source, include_legacy=True)
    files = {rel: target / rel for rel, src in incoming.items()
             if (target / rel).is_file() and digest(target / rel) == digest(src)}
    if not files:
        raise ValueError("no recognizable Resonance files found to adopt")
    manifest = {"schema": 1, "version": "adopted", "files": {r: digest(p) for r, p in files.items()}}
    path = target / MANIFEST
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return path


def plan(source: Path, target: Path) -> dict:
    source, target = source.resolve(), target.resolve()
    if source == target:
        raise ValueError("source and target must differ")
    current = load_manifest(target)
    incoming = source_files(source)
    conflicts, writes, removes = [], [], []
    for rel, src in incoming.items():
        dst = inside(target, target / rel)
        prior = current["files"].get(rel)
        if dst.exists() and (not prior or digest(dst) != prior):
            conflicts.append(rel)
        elif not dst.exists() or digest(dst) != digest(src):
            writes.append(rel)
    for rel, prior in current["files"].items():
        dst = inside(target, target / rel)
        if rel not in incoming and dst.is_file():
            if digest(dst) == prior:
                removes.append(rel)
            else:
                conflicts.append(rel)
    return {"version": version(source), "writes": sorted(writes),
            "removes": sorted(removes), "conflicts": sorted(set(conflicts)),
            "files": {rel: digest(src) for rel, src in incoming.items()}}


def apply(source: Path, target: Path, expected_version: str | None = None) -> Path:
    source, target = source.resolve(), target.resolve()
    work = plan(source, target)
    if expected_version and work["version"] != expected_version.lstrip("v"):
        raise ValueError(f"source version {work['version']} does not match requested {expected_version}")
    if work["conflicts"]:
        raise ValueError("user-owned or modified managed files block update: " + ", ".join(work["conflicts"]))
    required = (".forge/forge.py", ".forge/validate_skill.py", ".forge/eval_integrity.py")
    missing = [rel for rel in required if rel not in work["files"]]
    if missing:
        raise ValueError("source is incomplete; missing required validators: " + ", ".join(missing))
    stamp = time.strftime("%Y%m%d-%H%M%S") + f"-{time.time_ns() % 1_000_000_000:09d}"
    backup = target / ".resonance" / "backups" / f"resonance-update-{stamp}"
    backup.mkdir(parents=True, exist_ok=False)
    journal = {"schema": 1, "status": "backing-up", "version": work["version"],
               "target": str(target), "entries": []}
    journal_path = backup / "journal.json"
    journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")
    touched = work["writes"] + work["removes"] + [MANIFEST]
    for rel in touched:
        dst = inside(target, target / rel)
        existed = dst.is_file()
        if existed:
            saved = backup / "files" / rel
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, saved)
        journal["entries"].append({"path": rel, "existed": existed})
        journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")
    journal["status"] = "applying"
    journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")
    stage_root = target / ".resonance" / "tmp"
    stage_root.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="resonance-stage-", dir=stage_root))
    try:
        for rel in work["writes"]:
            staged = stage / rel
            staged.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / rel, staged)
        for rel in work["writes"]:
            dst = inside(target, target / rel)
            dst.parent.mkdir(parents=True, exist_ok=True)
            os.replace(stage / rel, dst)
        for rel in work["removes"]:
            inside(target, target / rel).unlink(missing_ok=True)
        checks = [target / ".forge" / "forge.py", target / ".forge" / "validate_skill.py",
                  target / ".forge" / "eval_integrity.py"]
        commands = [
            [sys.executable, str(checks[0]), "build", "--all", "--host", "all", "--dry-run"],
            [sys.executable, str(checks[1]), "--all", "--strict", str(target / ".agents" / "skills")],
            [sys.executable, str(checks[2])],
        ]
        for tool, command in zip(checks, commands):
            if not tool.is_file():
                raise RuntimeError(f"post-update validator missing: {tool}")
            result = subprocess.run(command, cwd=target, capture_output=True, text=True,
                                    encoding="utf-8", errors="replace", timeout=180)
            if result.returncode != 0:
                raise RuntimeError(f"post-update validation failed: {' '.join(command)}\n"
                                   f"{result.stdout}\n{result.stderr}")
        manifest = {"schema": 1, "version": work["version"], "files": work["files"]}
        mp = target / MANIFEST
        mp.parent.mkdir(parents=True, exist_ok=True)
        tmp = mp.with_suffix(".tmp")
        tmp.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, mp)
        journal["status"] = "complete"
        journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")
        return backup
    except BaseException:
        rollback(backup)
        raise
    finally:
        shutil.rmtree(stage, ignore_errors=True)


def doctor(source: Path, target: Path) -> dict:
    try:
        work = plan(source, target)
        pending = []
        root = target / ".resonance" / "backups"
        for journal in root.glob("resonance-update-*/journal.json") if root.is_dir() else []:
            try:
                if json.loads(journal.read_text(encoding="utf-8")).get("status") not in ("complete", "rolled-back"):
                    pending.append(str(journal.parent))
            except Exception:
                pending.append(str(journal.parent))
        return {"ok": not work["conflicts"] and not pending, "pending_recovery": pending, **work}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def rollback(backup: Path) -> None:
    backup = backup.resolve()
    journal_path = backup / "journal.json"
    journal = json.loads(journal_path.read_text(encoding="utf-8"))
    target = Path(journal["target"]).resolve()
    for entry in reversed(journal.get("entries", [])):
        rel, existed = entry["path"], entry["existed"]
        dst = inside(target, target / rel)
        saved = backup / "files" / rel
        if existed and saved.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(saved, dst)
        elif not existed and dst.is_file():
            dst.unlink()
    journal["status"] = "rolled-back"
    journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Preview or apply a transactional Resonance update")
    ap.add_argument("--source", type=Path)
    ap.add_argument("--target", type=Path)
    ap.add_argument("--version")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--doctor", action="store_true")
    ap.add_argument("--adopt", action="store_true",
                    help="record a pre-manifest installation without changing framework files")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rollback", type=Path, help="restore a backup whose journal is applying")
    args = ap.parse_args(argv)
    if args.rollback:
        rollback(args.rollback)
        print(f"rolled back: {args.rollback}")
        return 0
    if not args.source or not args.target:
        ap.error("--source and --target are required unless --rollback is used")
    if args.adopt:
        print(f"adopted ownership: {adopt(args.source, args.target)}")
        return 0
    result = doctor(args.source, args.target) if args.doctor else plan(args.source, args.target)
    if args.json or args.doctor or not args.apply:
        print(json.dumps(result, indent=2))
    if args.doctor:
        return 0 if result["ok"] else 1
    if not args.apply:
        return 1 if result["conflicts"] else 0
    backup = apply(args.source, args.target, args.version)
    print(f"updated to {version(args.source)}; backup: {backup}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
