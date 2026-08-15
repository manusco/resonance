#!/usr/bin/env python3
"""Versioned contract helpers for Resonance evidence receipts."""
from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
ID_RE = re.compile(r"^(act|apr|exe|evd|run)-[a-z0-9][a-z0-9-]*$")
SHA_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class ContractError(ValueError):
    pass


def _reject_nan(data: Any) -> None:
    if isinstance(data, float) and (math.isnan(data) or math.isinf(data)):
        raise ContractError("contract JSON must not contain NaN or Infinity")
    if isinstance(data, dict):
        for v in data.values():
            _reject_nan(v)
    if isinstance(data, list):
        for v in data:
            _reject_nan(v)


def stable_json(data: Any) -> str:
    _reject_nan(data)
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def hash_data(data: Any) -> str:
    return "sha256:" + hashlib.sha256(stable_json(data).encode("utf-8")).hexdigest()


def hash_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(value: str) -> dict[str, Any]:
    path = Path(value)
    text = path.read_text(encoding="utf-8") if path.exists() else value
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ContractError("contract must be a JSON object")
    return data


def require_schema(data: dict[str, Any], name: str) -> None:
    version = data.get("schema_version")
    if version != SCHEMA_VERSION:
        raise ContractError(f"{name} schema_version must be {SCHEMA_VERSION}")


def require_id(value: Any, prefix: str, field: str) -> None:
    if not isinstance(value, str) or not ID_RE.match(value) or not value.startswith(prefix + "-"):
        raise ContractError(f"{field} must be a {prefix}- id")


def require_hash(value: Any, field: str) -> None:
    if not isinstance(value, str) or not SHA_RE.match(value):
        raise ContractError(f"{field} must be a sha256 hash")


def require_timestamp(value: Any, field: str) -> None:
    if not isinstance(value, str) or not TS_RE.match(value):
        raise ContractError(f"{field} must be UTC ISO-8601 seconds")


def validate_goal_contract(data: dict[str, Any]) -> None:
    if not isinstance(data.get("outcome"), str) or not data["outcome"].strip():
        raise ContractError("goal contract missing outcome")
    checks = data.get("acceptance_checks")
    if not isinstance(checks, list) or not checks:
        raise ContractError("goal contract acceptance_checks must be a non-empty list")
    if any(not isinstance(x, str) or not x.strip() for x in checks):
        raise ContractError("goal contract acceptance_checks must contain non-empty strings")


def validate_approval(data: dict[str, Any]) -> None:
    require_schema(data, "approval")
    for field in ("approval_id", "action_id", "actor", "scope_hash", "decision", "created_at"):
        if not data.get(field):
            raise ContractError(f"approval missing {field}")
    if data["decision"] != "approved":
        raise ContractError("approval decision must be approved")
    require_id(data["approval_id"], "apr", "approval_id")
    require_id(data["action_id"], "act", "action_id")
    require_hash(data["scope_hash"], "scope_hash")
    require_timestamp(data["created_at"], "created_at")


def validate_action(data: dict[str, Any]) -> None:
    require_schema(data, "action")
    for field in ("action_id", "run_id", "skill_id", "goal_revision", "source_revision",
                  "inputs", "requested_effects", "authority_required", "operation_key"):
        if field not in data or data[field] in ("", None):
            raise ContractError(f"action missing {field}")
    require_id(data["action_id"], "act", "action_id")
    require_id(data["run_id"], "run", "run_id")
    require_hash(data["operation_key"], "operation_key")


def validate_execution(data: dict[str, Any]) -> None:
    require_schema(data, "execution")
    for field in ("execution_id", "action_id", "provider_profile", "command_or_tool",
                  "normalized_arguments", "working_directory", "started_at", "finished_at",
                  "exit_code", "stdout_hash", "stderr_hash", "before_manifest_hash",
                  "after_manifest_hash", "artifact_hashes", "runner"):
        if field not in data or data[field] in ("", None):
            raise ContractError(f"execution missing {field}")
    require_id(data["execution_id"], "exe", "execution_id")
    require_id(data["action_id"], "act", "action_id")
    require_timestamp(data["started_at"], "started_at")
    require_timestamp(data["finished_at"], "finished_at")
    for field in ("stdout_hash", "stderr_hash", "before_manifest_hash", "after_manifest_hash"):
        require_hash(data[field], field)
    if not isinstance(data["exit_code"], int):
        raise ContractError("execution exit_code must be an integer")
    if data["exit_code"] != 0:
        raise ContractError("execution exit_code must be 0 for accepted evidence")
    if data["runner"] != "resonance-kernel-runner/1":
        raise ContractError("execution runner must be resonance-kernel-runner/1")


def validate_evidence(data: dict[str, Any]) -> None:
    require_schema(data, "evidence")
    for field in ("evidence_id", "run_id", "goal_revision", "contract_hash",
                  "plan_hash", "slice_id", "criterion_id", "verifier", "result",
                  "created_at"):
        if field not in data or data[field] in ("", None):
            raise ContractError(f"evidence missing {field}")
    if data["result"] not in ("accepted", "rejected", "overridden"):
        raise ContractError("evidence result must be accepted, rejected, or overridden")
    require_id(data["evidence_id"], "evd", "evidence_id")
    require_id(data["run_id"], "run", "run_id")
    require_hash(data["contract_hash"], "contract_hash")
    require_hash(data["plan_hash"], "plan_hash")
    require_timestamp(data["created_at"], "created_at")
    if "execution_receipts" not in data or not isinstance(data["execution_receipts"], list) or not data["execution_receipts"]:
        raise ContractError("evidence requires at least one execution receipt")
