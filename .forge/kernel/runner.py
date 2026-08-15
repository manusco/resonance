#!/usr/bin/env python3
"""Trusted local execution receipt creator for the evidence kernel."""
from __future__ import annotations

import hashlib
import json
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .contracts import hash_text


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def manifest_hash(root: Path) -> str:
    parts = []
    paths: list[Path] = []
    try:
        tracked = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=str(root),
            capture_output=True,
            timeout=30,
            check=True,
        ).stdout.decode("utf-8", errors="replace")
        paths = [
            root / rel for rel in tracked.split("\0")
            if rel and not rel.startswith((".resonance/", "_input/"))
        ]
    except Exception:
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            if rel.startswith((".git/", ".resonance/", "_input/")):
                continue
            paths.append(path)
    for path in sorted(paths):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            continue
        parts.append(f"{rel}\0{digest}")
    return hash_text("\n".join(parts))


def run_execution(action_id: str, command: list[str], cwd: Path) -> dict:
    started = now()
    before = manifest_hash(cwd)
    result = subprocess.run(command, cwd=str(cwd), capture_output=True, text=True, shell=False)
    after = manifest_hash(cwd)
    finished = now()
    raw = json.dumps({
        "action_id": action_id,
        "command": command,
        "nonce": uuid.uuid4().hex,
        "started_at": started,
        "finished_at": finished,
        "stdout_hash": hash_text(result.stdout),
        "stderr_hash": hash_text(result.stderr),
    }, sort_keys=True)
    return {
        "schema_version": 1,
        "execution_id": "exe-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16],
        "action_id": action_id,
        "provider_profile": "local-shell",
        "command_or_tool": command[0] if command else "",
        "normalized_arguments": command[1:],
        "working_directory": ".",
        "started_at": started,
        "finished_at": finished,
        "exit_code": result.returncode,
        "stdout_hash": hash_text(result.stdout),
        "stderr_hash": hash_text(result.stderr),
        "before_manifest_hash": before,
        "after_manifest_hash": after,
        "artifact_hashes": [],
        "runner": "resonance-kernel-runner/1",
    }
