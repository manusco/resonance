#!/usr/bin/env python3
"""Immutable, redacted evidence manifests for Forge evaluation runners."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import subprocess
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = 1
STORAGE_POLICY = {
    "retention": "append-only until the governing evaluation contract expires the run",
    "access": "limit raw artifacts to evaluation operators and dataset custodians",
    "redaction": "store redacted command fingerprints and hashes of raw model responses",
    "backup": "back up the external evidence root separately from the public repository",
    "garbage_collection": "remove only expired runs under the governing contract; never rewrite a run",
}
SECRET_NAME = re.compile(r"(?i)(token|secret|password|passwd|api[_-]?key|credential|auth)")
INLINE_SECRET = re.compile(
    r"(?i)(\b(?:token|secret|password|passwd|api[_-]?key|credential|authorization)\b\s*[=:]\s*)([^\s,;]+)"
)
BEARER = re.compile(r"(?i)(\bbearer\s+)([^\s,;]+)")
AUTH_BEARER = re.compile(r"(?i)(\bauthorization\s*[:=]\s*bearer\s+)([^\s,;]+)")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def hash_item(identifier: str, value: bytes | str | Path | Any) -> dict[str, str]:
    if isinstance(value, Path):
        digest = sha256_file(value)
    elif isinstance(value, bytes):
        digest = sha256_bytes(value)
    elif isinstance(value, str):
        digest = sha256_bytes(value.encode("utf-8"))
    else:
        digest = sha256_bytes(canonical_bytes(value))
    return {"id": identifier, "hash": digest}


def redact_command(command: str | Iterable[str]) -> str:
    """Return a stable command representation with common secret forms removed."""
    if isinstance(command, str):
        command = AUTH_BEARER.sub(r"\1[REDACTED]", command)
        parts = command.split()
    else:
        parts = list(command)
    redacted: list[str] = []
    hide_next = False
    for part in parts:
        if hide_next:
            redacted.append("[REDACTED]")
            hide_next = False
            continue
        key = part.lstrip("-").split("=", 1)[0]
        if SECRET_NAME.search(key):
            if "=" in part:
                redacted.append(part.split("=", 1)[0] + "=[REDACTED]")
            else:
                redacted.append(part)
                hide_next = True
            continue
        cleaned = INLINE_SECRET.sub(r"\1[REDACTED]", part)
        cleaned = BEARER.sub(r"\1[REDACTED]", cleaned)
        redacted.append(cleaned)
    return " ".join(redacted)


def command_item(identifier: str, command: str | Iterable[str]) -> tuple[dict[str, str], str]:
    redacted = redact_command(command)
    return hash_item(identifier, redacted), redacted


def git_state(repo: Path) -> tuple[dict[str, Any], dict[str, str]]:
    def git(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args], cwd=str(repo), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=30,
        )

    head = git("rev-parse", "HEAD")
    status = git("status", "--porcelain=v1", "-z", "--untracked-files=all")
    if head.returncode != 0 or status.returncode != 0:
        raise RuntimeError("cannot capture git provenance")
    paths: list[str] = []
    entries = status.stdout.split("\0")
    i = 0
    while i < len(entries):
        entry = entries[i]
        i += 1
        if not entry:
            continue
        path = entry[3:] if len(entry) >= 4 else entry
        if entry[:2] in {"R ", "C ", "RM", "CM"} and i < len(entries):
            path = entries[i]
            i += 1
        paths.append(path.replace("\\", "/"))
    paths = sorted(set(paths))
    hashes: dict[str, str] = {}
    for rel in paths:
        candidate = repo / rel
        if candidate.is_file():
            hashes[rel] = sha256_file(candidate)
        else:
            hashes[rel] = "MISSING"
    return {
        "git_sha": head.stdout.strip().lower(),
        "dirty": bool(paths),
        "changed_paths": paths,
    }, hashes


def environment_fingerprint() -> dict[str, str]:
    values = {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
    }
    values["hash"] = sha256_bytes(canonical_bytes(values))
    return values


def validate_evidence_root(root: Path, repo: Path, explicit: bool) -> Path:
    resolved = root.expanduser().resolve(strict=False)
    repo_resolved = repo.resolve()
    try:
        relative = resolved.relative_to(repo_resolved)
    except ValueError:
        return resolved
    if not explicit:
        raise ValueError("repository-local evidence roots must be explicitly supplied")
    forbidden = (".resonance", ".agents", ".claude", ".cursor", ".opencode")
    if relative.parts and relative.parts[0].lower() in forbidden:
        raise ValueError("evidence root cannot be a memory scaffold or generated host surface")
    if len(relative.parts) >= 2 and relative.parts[:2] == (".forge", "skills"):
        raise ValueError("evidence root cannot be a generated-source directory")
    return resolved


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class EvidenceRun:
    """Collect and atomically persist one independently addressable run."""

    def __init__(self, *, root: Path, repo: Path, runner: Path, runner_id: str,
                 baseline_id: str = "", explicit_root: bool = True) -> None:
        self.root = validate_evidence_root(root, repo, explicit_root)
        self.repo = repo.resolve()
        self.runner = runner.resolve()
        self.runner_id = runner_id
        self.baseline_id = baseline_id
        self.started_at = utc_now()
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        self.run_id = f"{runner_id}-{stamp}-{uuid.uuid4().hex[:12]}"

    def write(self, *, exit_state: str, cases: list[dict[str, str]],
              skills: list[dict[str, str]], instructions_hash: str,
              models: dict[str, str], commands: list[dict[str, str]],
              command_fingerprints: dict[str, str], repetitions: int,
              thresholds: dict[str, Any], host: str, tool_profile: str,
              permission_profile: str, results: list[dict[str, str]] | None,
              summary: dict[str, Any], latency_ms: int = 0,
              cost_currency: str = "USD", cost_amount: float = 0.0,
              result_payloads: dict[str, Any] | None = None) -> Path:
        repository, changed_hashes = git_state(self.repo)
        replay = dict(summary.get("replay_envelope", {}))
        replay.update({
            "baseline_id": self.baseline_id or None,
            "changed_path_hashes": changed_hashes,
            "environment": environment_fingerprint(),
            "command_fingerprints": command_fingerprints,
        })
        summary = dict(summary)
        summary["replay_envelope"] = replay
        summary.setdefault("storage_policy", STORAGE_POLICY)
        run_dir = self.root / "runs" / self.run_id
        manifest_path = run_dir / "manifest.json"
        run_dir.mkdir(parents=True, exist_ok=False)
        result_items = list(results or [])
        for name, value in sorted((result_payloads or {}).items()):
            safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip(".") or "result"
            result_path = run_dir / safe_name
            payload = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
            flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
            fd = os.open(str(result_path), flags)
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(payload)
            result_items.append(hash_item(safe_name, result_path))
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.run_id,
            "started_at": self.started_at,
            "ended_at": utc_now(),
            "repository": repository,
            "runner": hash_item(self.runner_id, self.runner),
            "cases": cases,
            "skills": skills,
            "instructions": instructions_hash,
            "models": models,
            "commands": commands,
            "execution": {
                "repetitions": max(1, repetitions),
                "thresholds": thresholds,
                "host": host,
                "tool_profile": tool_profile,
                "permission_profile": permission_profile,
                "cost": {"currency": cost_currency, "amount": max(0.0, cost_amount)},
                "latency_ms": max(0, latency_ms),
            },
            "results": result_items,
            "summary": summary,
            "exit_state": exit_state,
        }
        payload = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        fd = os.open(str(manifest_path), flags)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
        pointer = {
            "schema_version": 1,
            "run_id": self.run_id,
            "manifest": manifest_path.relative_to(self.root).as_posix(),
            "manifest_hash": sha256_file(manifest_path),
        }
        atomic_json(self.root / "latest.json", pointer)
        return manifest_path


def require_promotion_provenance(*, evidence_root: str, baseline_id: str,
                                 identities: dict[str, str], revisions: dict[str, str]) -> None:
    missing = []
    if not evidence_root:
        missing.append("evidence root")
    if not baseline_id:
        missing.append("baseline ID")
    missing.extend(f"{name} identity" for name, value in identities.items() if not value)
    missing.extend(f"{name} provider revision" for name, value in revisions.items() if not value)
    if missing:
        raise ValueError("promotion evidence is incomplete: " + ", ".join(missing))
