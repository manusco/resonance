#!/usr/bin/env python3
"""Append-only evidence store and receipt validation."""
from __future__ import annotations

import json
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .contracts import ContractError, hash_data, read_json, validate_approval, validate_evidence, validate_execution
from .transitions import require_transition


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def create_receipt(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    fd = os.open(str(path), flags)
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


@contextmanager
def file_lock(path: Path):
    lock = path.with_suffix(path.suffix + ".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise ContractError(f"state is locked: {lock}") from exc
    try:
        os.write(fd, str(os.getpid()).encode("ascii"))
        os.close(fd)
        yield
    finally:
        try:
            lock.unlink()
        except FileNotFoundError:
            pass


def load_state(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def append_attempt(state: dict[str, Any], entry: dict[str, Any]) -> dict[str, Any]:
    out = dict(state)
    out.setdefault("attempts", [])
    out["attempts"] = list(out["attempts"]) + [entry]
    out.setdefault("iterations", [])
    out["iterations"] = list(out["iterations"]) + [entry]
    return out


def accept_evidence(state: dict[str, Any], evidence: dict[str, Any], approval: dict[str, Any] | None) -> dict[str, Any]:
    validate_evidence(evidence)
    if not state.get("contract"):
        raise ContractError("cannot accept evidence without an active contract")
    if evidence.get("contract_hash") != state.get("contract_hash"):
        raise ContractError("stale evidence: contract hash mismatch")
    if evidence.get("plan_hash") != state.get("plan_hash"):
        raise ContractError("stale evidence: plan hash mismatch")
    if evidence.get("goal_revision") != state.get("goal_revision", 1):
        raise ContractError("stale evidence: goal revision mismatch")
    if evidence.get("run_id") != state.get("run_id"):
        raise ContractError("stale evidence: run id mismatch")
    known = {e.get("evidence_id") for e in state.get("evidence", [])}
    if evidence["evidence_id"] in known:
        raise ContractError("duplicate evidence_id")
    criteria = state.get("criterion_ids", [])
    if evidence.get("criterion_id") not in criteria:
        raise ContractError("unknown criterion_id")
    for receipt in evidence.get("execution_receipts", []):
        if not isinstance(receipt, dict):
            raise ContractError("execution receipt must be an object")
        validate_execution(receipt)
        known_exec = {e.get("execution_id") for e in state.get("executions", [])}
        if receipt["execution_id"] not in known_exec:
            raise ContractError("execution receipt was not recorded by this goal run")
    if evidence["result"] == "overridden":
        if not approval:
            raise ContractError("override evidence requires approval")
        validate_approval(approval)
        if approval["scope_hash"] != hash_data(evidence):
            raise ContractError("approval scope_hash does not match evidence")
    out = dict(state)
    out.setdefault("evidence", [])
    out["evidence"] = list(out["evidence"]) + [evidence]
    out.setdefault("evidence_receipts", [])
    out["evidence_receipts"] = list(out["evidence_receipts"]) + [
        f".resonance/evidence/{evidence['evidence_id']}.json"
    ]
    return out


def require_achievement(state: dict[str, Any]) -> None:
    if not state.get("contract"):
        raise ContractError("cannot achieve goal without a contract")
    latest: dict[str, str] = {}
    for e in state.get("evidence", []):
        latest[e.get("criterion_id", "")] = e.get("result", "")
    missing = [cid for cid in state.get("criterion_ids", []) if latest.get(cid) not in ("accepted", "overridden")]
    if missing:
        raise ContractError("cannot achieve goal without accepted evidence for: " + ", ".join(missing))


def transition_goal(state: dict[str, Any], target: str) -> dict[str, Any]:
    current = state.get("status", "active")
    require_transition(current, target)
    if target == "achieved":
        require_achievement(state)
    out = dict(state)
    out["status"] = target
    out["updated_at"] = now()
    return out


def read_receipt(value: str) -> dict[str, Any]:
    try:
        return read_json(value)
    except json.JSONDecodeError as exc:
        raise ContractError(f"receipt is not valid JSON: {exc}") from exc
