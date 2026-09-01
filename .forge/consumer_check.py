#!/usr/bin/env python3
"""Run read-only health checks for an installed Resonance consumer."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


MANIFEST = ".resonance/framework-manifest.json"


def inside(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise ValueError(f"managed path must be relative: {relative}")
    path = (root / relative).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"managed path escapes consumer root: {relative}") from exc
    return path


def owned_files(root: Path) -> dict:
    path = root / MANIFEST
    if not path.is_file():
        raise ValueError(f"consumer ownership manifest is missing: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    files = data.get("files")
    if not isinstance(files, dict):
        raise ValueError("consumer ownership manifest has no file map")
    missing, mismatched = [], []
    for relative, expected in files.items():
        invalid_hash = (
            not isinstance(expected, str)
            or len(expected) != 64
            or any(character not in "0123456789abcdef" for character in expected)
        )
        if invalid_hash:
            raise ValueError(f"invalid managed hash: {relative}")
        target = inside(root, relative)
        if not target.is_file():
            missing.append(relative)
        elif hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            mismatched.append(relative)
    return {
        "name": "owned_files",
        "status": "pass" if not missing and not mismatched else "fail",
        "owned": len(files),
        "missing": missing,
        "mismatched": mismatched,
    }


def run_check(name: str, command: list[str], cwd: Path) -> dict:
    result = subprocess.run(
        command, cwd=cwd, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    check = {
        "name": name,
        "status": "pass" if result.returncode == 0 else "fail",
        "returncode": result.returncode,
    }
    if result.returncode != 0:
        check.update({"stdout": result.stdout, "stderr": result.stderr})
    return check


def check(root: Path) -> dict:
    root = root.resolve()
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    if manifest.get("schema") != 1:
        raise ValueError(f"unsupported consumer manifest schema: {manifest.get('schema')}")
    profile = manifest.get("profile")
    if profile not in ("source", "compiled"):
        raise ValueError(f"unknown consumer profile: {profile}")
    checks = [owned_files(root)]
    if profile == "source":
        checks.extend([
            run_check(
                "forge_dry_run",
                [sys.executable, str(root / ".forge/forge.py"), "build", "--all", "--host", "all", "--dry-run", "--consumer"],
                root,
            ),
            run_check(
                "skills",
                [sys.executable, str(root / ".forge/validate_skill.py"), "--all", "--strict", str(root / ".agents/skills")],
                root,
            ),
            run_check("eval_integrity", [sys.executable, str(root / ".forge/eval_integrity.py")], root),
        ])
    else:
        checks.append({"name": "source_validators", "status": "skipped", "reason": "compiled profile"})
    lock = root / ".resonance/project-skills.lock.json"
    if lock.is_file() and profile == "source":
        checks.append(run_check(
            "project_skills",
            [sys.executable, str(root / ".forge/project_skills.py"), "--check", "--root", str(root)],
            root,
        ))
    shell = root / "resonance.sh"
    bash = shutil.which("bash")
    checks.append(
        run_check("bash_syntax", [bash, "-n", str(shell)], root)
        if bash and shell.is_file()
        else {"name": "bash_syntax", "status": "skipped", "reason": "bash or launcher unavailable"}
    )
    powershell = shutil.which("pwsh") or shutil.which("powershell")
    ps1 = root / "resonance.ps1"
    checks.append(
        run_check(
            "powershell_syntax",
            [
                powershell, "-NoProfile", "-NonInteractive", "-Command",
                "$e=$null; [System.Management.Automation.Language.Parser]::ParseFile($args[0],[ref]$null,[ref]$e) > $null; if ($e.Count) { $e | Out-String | Write-Error; exit 1 }",
                str(ps1),
            ],
            root,
        )
        if powershell and ps1.is_file()
        else {"name": "powershell_syntax", "status": "skipped", "reason": "PowerShell runtime unavailable; release CI parses this launcher on Windows"}
    )
    failed = [item["name"] for item in checks if item["status"] == "fail"]
    return {"ok": not failed, "profile": profile, "failed": failed, "checks": checks}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run read-only checks for an installed Resonance consumer")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        result = check(args.root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"ok": False, "error": str(exc)}
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
