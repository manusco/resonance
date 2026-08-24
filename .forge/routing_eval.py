#!/usr/bin/env python3
"""Evaluate routing independently from skill execution and lift.

Public cases describe the oracle. The router sees only the user query and the
real startup catalog generated from compiled skill frontmatter. Live output is
strict JSON and is rejected before scoring when its shape is invalid.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shlex
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

FORGE = Path(__file__).resolve().parent
REPO = FORGE.parent
MANIFEST = REPO / "docs" / "skill-manifest.json"
CASES = FORGE / "routing_evals"
MODES = {"NONE", "AUTO", "MANUAL", "ASK"}
TIERS = {"STANDARD", "HIGH", "CRITICAL"}
REQUIRED_RESULT = {
    "primary_skill", "contributors", "mode", "abstain", "confidence", "reason", "clarification"
}
HOLDOUT_ROLES = {"protected_validation", "sealed_promotion"}
ORACLE_FIELD_NAMES = {
    "expected_primary", "allowed_contributors", "forbidden_skills", "rationale",
    "expected_activation_mode", "ambiguity_behavior", "deterministic_checks",
}
HOLDOUT_CONTROL_FILES = {"dataset.json", "hash-manifest.json", "custody-state.json", "access-log.jsonl"}
MANUAL_ROUTE_OWNERS = {
    "resonance-ops-goal",
    "resonance-ops-ship",
    "resonance-software-deliver-change",
}
OPAQUE_TOKEN = re.compile(r"^[a-f0-9]{16,64}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def protected_files(root: Path) -> list[Path]:
    """Return immutable protected inputs, excluding mutable custody records."""
    files = sorted(path for path in root.rglob("*.json")
                   if path.is_file() and path.name not in HOLDOUT_CONTROL_FILES)
    for path in files:
        resolved = path.resolve(strict=True)
        if not _inside(resolved, root.resolve()) or _inside(resolved, REPO.resolve()):
            raise ValueError(f"protected case escapes dataset root: {path.name}")
    return files


def validate_protected_opacity(root: Path, cases: list[dict]) -> list[str]:
    errors = []
    metadata = _load_json(root / "dataset.json", "dataset metadata")
    if not isinstance(metadata.get("dataset_id"), str) or not OPAQUE_TOKEN.fullmatch(metadata["dataset_id"]):
        errors.append("protected dataset id is not opaque")
    for path in protected_files(root):
        if not OPAQUE_TOKEN.fullmatch(path.stem):
            errors.append(f"protected case filename is not opaque: {path.name}")
    for case in cases:
        if not isinstance(case.get("id"), str) or not OPAQUE_TOKEN.fullmatch(case["id"]):
            errors.append("protected case id is not opaque")
    return errors


def protected_hashes(root: Path) -> dict[str, str]:
    return {path.relative_to(root).as_posix(): sha256_file(path) for path in protected_files(root)}


def _atomic_json(path: Path, value: object) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _append_event(path: Path, event: dict) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n")


def _validate_external_path(path: Path) -> Path:
    resolved = path.expanduser().resolve(strict=True)
    if not resolved.is_dir():
        raise ValueError("protected holdout path must be a directory")
    if _inside(resolved, REPO.resolve()):
        raise ValueError("protected holdout must be outside the repository")
    return resolved


def _validate_external_output(path: Path) -> Path:
    resolved = path.expanduser().resolve(strict=False)
    if _inside(resolved, REPO.resolve()):
        raise ValueError("diagnostic sidecar must be outside the repository")
    if resolved.exists() and resolved.is_dir():
        raise ValueError("diagnostic sidecar path must be a file")
    if not resolved.parent.is_dir():
        raise ValueError("diagnostic sidecar parent must already exist")
    return resolved


def _load_json(path: Path, label: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def load_protected_dataset(path: Path, expected_role: str) -> dict:
    """Open an external holdout and validate custody without exposing its oracle."""
    if expected_role not in HOLDOUT_ROLES:
        raise ValueError(f"unknown protected dataset role: {expected_role}")
    root = _validate_external_path(path)
    for name in ("dataset.json", "hash-manifest.json", "custody-state.json"):
        control = root / name
        try:
            resolved = control.resolve(strict=True)
        except OSError as exc:
            raise ValueError(f"missing protected control file: {name}") from exc
        if not _inside(resolved, root) or _inside(resolved, REPO.resolve()):
            raise ValueError(f"protected control file escapes dataset root: {name}")
    access_log = root / "access-log.jsonl"
    if access_log.exists() and not _inside(access_log.resolve(strict=True), root):
        raise ValueError("protected access log escapes dataset root")
    metadata = _load_json(root / "dataset.json", "dataset metadata")
    required = {
        "schema_version", "dataset_id", "role", "owner", "created_at", "permitted_use",
        "rotation_rule", "max_reuse_count", "diagnostic_policy",
    }
    if set(metadata) != required:
        raise ValueError(f"dataset metadata fields must be exactly {sorted(required)}")
    if metadata["schema_version"] != 1 or metadata["role"] != expected_role:
        raise ValueError(f"holdout role mismatch: expected {expected_role!r}")
    if metadata["diagnostic_policy"] not in {"SUMMARY_ONLY", "CASE_LEVEL"}:
        raise ValueError("diagnostic_policy must be SUMMARY_ONLY or CASE_LEVEL")
    if expected_role == "sealed_promotion" and metadata["diagnostic_policy"] != "SUMMARY_ONLY":
        raise ValueError("sealed promotion holdouts require SUMMARY_ONLY diagnostics")
    if not isinstance(metadata["max_reuse_count"], int) or metadata["max_reuse_count"] < 1:
        raise ValueError("max_reuse_count must be a positive integer")
    if expected_role == "sealed_promotion" and metadata["max_reuse_count"] != 1:
        raise ValueError("sealed promotion holdouts must be single-use")

    state_path = root / "custody-state.json"
    state = _load_json(state_path, "custody state")
    if set(state) != {"schema_version", "dataset_id", "reuse_count", "contamination_events", "retirement_state"}:
        raise ValueError("custody state has invalid fields")
    if state["schema_version"] != 1 or state["dataset_id"] != metadata["dataset_id"]:
        raise ValueError("custody state does not match dataset metadata")
    if state["retirement_state"] != "ACTIVE":
        raise ValueError(f"protected dataset is not active: {state['retirement_state']}")
    if not isinstance(state["reuse_count"], int) or state["reuse_count"] < 0:
        raise ValueError("custody reuse_count must be a non-negative integer")
    if not isinstance(state["contamination_events"], list):
        raise ValueError("custody contamination_events must be a list")
    if state["reuse_count"] >= metadata["max_reuse_count"]:
        state["retirement_state"] = "RETIRED"
        _atomic_json(state_path, state)
        raise ValueError("protected dataset reached its reuse limit and was retired")

    declared = _load_json(root / "hash-manifest.json", "hash manifest")
    if set(declared) != {"schema_version", "algorithm", "files"} or declared.get("schema_version") != 1:
        raise ValueError("hash manifest has invalid fields or version")
    if declared.get("algorithm") != "sha256" or not isinstance(declared.get("files"), dict):
        raise ValueError("hash manifest must contain SHA-256 file hashes")
    before = protected_hashes(root)
    if not before:
        raise ValueError("protected holdout contains no cases")
    if declared["files"] != before:
        raise ValueError("protected holdout hash manifest does not match its files")
    cases = [_load_json(root / rel, f"protected case {rel}") for rel in sorted(before)]
    control_before = {
        name: sha256_file(root / name) for name in ("dataset.json", "hash-manifest.json")
    }
    return {"root": root, "metadata": metadata, "state": state, "state_path": state_path,
            "access_log": access_log, "before": before, "control_before": control_before,
            "cases": cases}


def protected_event(dataset: dict, event: str, **details: object) -> None:
    record = {"schema_version": 1, "timestamp": utc_now(), "event": event,
              "dataset_id": dataset["metadata"]["dataset_id"],
              "role": dataset["metadata"]["role"], **details}
    _append_event(dataset["access_log"], record)


def contaminate(dataset: dict, reason: str) -> None:
    try:
        state = _load_json(dataset["state_path"], "custody state")
    except ValueError:
        state = dict(dataset["state"])
    state["reuse_count"] = max(int(state.get("reuse_count", 0)),
                               int(dataset["state"].get("reuse_count", 0)))
    state["contamination_events"] = list(state.get("contamination_events", []))
    state["contamination_events"] = [*state["contamination_events"], {"at": utc_now(), "reason": reason}]
    state["retirement_state"] = "CONTAMINATED"
    _atomic_json(dataset["state_path"], state)
    dataset["state"] = state
    protected_event(dataset, "CONTAMINATION", reason=reason, retirement_state="CONTAMINATED")


def begin_protected_access(dataset: dict, model_id: str) -> None:
    state = dict(dataset["state"])
    state["reuse_count"] += 1
    if state["reuse_count"] >= dataset["metadata"]["max_reuse_count"]:
        state["retirement_state"] = "RETIRED"
    _atomic_json(dataset["state_path"], state)
    dataset["state"] = state
    protected_event(dataset, "ACCESS", model_id=model_id, reuse_count=state["reuse_count"],
                    retirement_state=state["retirement_state"], input_hashes=dataset["before"])


def assert_protected_unchanged(dataset: dict) -> None:
    after = protected_hashes(dataset["root"])
    if after != dataset["before"]:
        contaminate(dataset, "protected inputs changed during evaluation")
        raise ValueError("protected holdout changed during execution")
    controls = {
        name: sha256_file(dataset["root"] / name)
        for name in ("dataset.json", "hash-manifest.json")
    }
    if controls != dataset["control_before"]:
        contaminate(dataset, "protected control metadata changed during evaluation")
        raise ValueError("protected control metadata changed during execution")
    disk_state = _load_json(dataset["state_path"], "custody state")
    if disk_state != dataset["state"]:
        contaminate(dataset, "custody state changed outside the evaluator during execution")
        raise ValueError("protected custody state changed concurrently")
    protected_event(dataset, "HASH_VERIFIED", input_hashes=after)


def oracle_leakage(case: dict, prompt: str, output: object | None = None) -> list[str]:
    """Detect oracle structure or copied private rationale before grading."""
    leaks = []
    lower_prompt = prompt.lower()
    for field in ORACLE_FIELD_NAMES:
        if re.search(rf"(?<![a-z0-9_]){re.escape(field)}(?![a-z0-9_])", lower_prompt):
            leaks.append(f"prompt contains oracle field {field}")
    if output is not None:
        rendered = json.dumps(output, ensure_ascii=False).casefold()
        rationale = str(case.get("rationale", "")).strip().casefold()
        opaque_id = str(case.get("id", "")).strip().casefold()
        if rationale and len(rationale) >= 12 and rationale in rendered:
            leaks.append("output reproduces protected rationale")
        if opaque_id and len(opaque_id) >= 8 and opaque_id in rendered:
            leaks.append("output reproduces protected case identifier")
        if isinstance(output, dict) and ORACLE_FIELD_NAMES & set(output):
            leaks.append("output contains oracle fields")
    return leaks


def protected_summary(report: dict, dataset: dict) -> dict:
    """Return a repository-safe summary, with optional validation diagnostics."""
    summary = {
        "schema_version": 1,
        "dataset": {
            "role": dataset["metadata"]["role"],
            "reuse_count": dataset["state"]["reuse_count"],
            "retirement_state": dataset["state"]["retirement_state"],
        },
        "passed": report["passed"], "violations": len(report["violations"]),
        "violation_categories": report.get("violation_categories", {}),
        "metrics": report["metrics"],
        "execution": report.get("execution", {
            "adapter": "unknown", "cost_usd": 0.0, "host_events": 0,
        }),
    }
    if (dataset["metadata"]["role"] == "protected_validation" and
            dataset["metadata"]["diagnostic_policy"] == "CASE_LEVEL"):
        summary["diagnostics"] = [{
            "id_hash": hashlib.sha256(row["id"].encode()).hexdigest(),
            "cluster": row["cluster"], "tier": row["tier"],
            "exact_primary": row["exact_primary"], "mode_ok": row["mode_ok"],
            "abstention_ok": row["abstention_ok"], "forbidden_count": len(row["forbidden"]),
        } for row in report["cases"]]
    return summary


def load_catalog() -> list[dict]:
    """Load routing evidence without conflating host exposure with route mode."""
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return [{
        "id": item["id"],
        "description": " ".join(item.get("triggers", [])),
        "negative_triggers": item.get("negative_triggers", []),
        "host_activation": item["activation"],
        "authority": item["authority"],
        "entrypoints": item.get("entrypoints", []),
    } for item in entries]


def load_cases() -> list[dict]:
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(CASES.glob("*.json"))]


def validate_case(case: dict, skill_ids: set[str]) -> list[str]:
    required = {
        "schema_version", "id", "query", "expected_primary", "allowed_contributors",
        "forbidden_skills", "harm_tier", "cluster", "rationale",
        "expected_activation_mode", "ambiguity_behavior", "deterministic_checks",
    }
    allowed_fields = required | {"ask_materiality"}
    errors = []
    missing = required - set(case)
    if missing:
        return [f"missing fields: {sorted(missing)}"]
    if set(case) - allowed_fields:
        errors.append(f"unknown fields: {sorted(set(case) - allowed_fields)}")
    if case["schema_version"] != 1:
        errors.append("schema_version must be 1")
    if not isinstance(case["query"], str) or not case["query"].strip():
        errors.append("query must be non-empty")
    if case["harm_tier"] not in TIERS:
        errors.append(f"harm_tier must be one of {sorted(TIERS)}")
    if case["expected_activation_mode"] not in MODES:
        errors.append(f"expected_activation_mode must be one of {sorted(MODES)}")
    if case["ambiguity_behavior"] not in {"ROUTE", "ASK_MATERIAL_QUESTION", "DECLINE"}:
        errors.append("invalid ambiguity_behavior")
    for field in ("allowed_contributors", "forbidden_skills", "deterministic_checks"):
        if not isinstance(case[field], list):
            errors.append(f"{field} must be a list")
    referenced = [case["expected_primary"], *case["allowed_contributors"], *case["forbidden_skills"]]
    for skill in referenced:
        if skill is not None and skill not in skill_ids:
            errors.append(f"unknown skill: {skill}")
    if case["expected_primary"] in case["forbidden_skills"]:
        errors.append("expected_primary cannot be forbidden")
    mode = case["expected_activation_mode"]
    ambiguity = case["ambiguity_behavior"]
    if ambiguity == "ASK_MATERIAL_QUESTION" and mode != "ASK":
        errors.append("material ambiguity requires ASK mode")
    if mode == "ASK" and ambiguity != "ASK_MATERIAL_QUESTION":
        errors.append("ASK mode requires material ambiguity")
    if mode == "NONE" and case["expected_primary"] is not None:
        errors.append("NONE mode requires no primary skill")
    if mode == "AUTO" and case["expected_primary"] is None:
        errors.append("AUTO mode requires a primary skill")
    if mode == "MANUAL" and case["expected_primary"] not in MANUAL_ROUTE_OWNERS:
        errors.append("MANUAL mode is reserved for explicit or consequential entrypoints")
    materiality = case.get("ask_materiality")
    if ambiguity == "ASK_MATERIAL_QUESTION":
        if not isinstance(materiality, dict):
            errors.append("ASK_MATERIAL_QUESTION requires ask_materiality")
        else:
            alternatives = materiality.get("possible_primary_skills")
            if materiality.get("route_changes_primary") is not True:
                errors.append("ask_materiality.route_changes_primary must be true")
            if (not isinstance(alternatives, list) or
                    not all(isinstance(skill, str) for skill in alternatives) or
                    len(set(alternatives)) < 2):
                errors.append("ask_materiality must list at least two possible primary skills")
            elif any(skill not in skill_ids for skill in alternatives):
                errors.append("ask_materiality contains an unknown possible primary skill")
    elif materiality is not None:
        errors.append("ask_materiality is only valid for material ambiguity")
    return errors


def validate_case_set(cases: list[dict]) -> list[str]:
    """Reject duplicate requests whose routing or mode oracle disagrees."""
    seen: dict[str, tuple[object, str]] = {}
    errors = []
    for case in cases:
        query = " ".join(case.get("query", "").casefold().split())
        oracle = (case.get("expected_primary"), case.get("expected_activation_mode"))
        if query in seen and seen[query] != oracle:
            errors.append(f"{case.get('id', '<unknown>')}: duplicate query has a conflicting oracle")
        seen[query] = oracle
    return errors


def validate_result(result: object, skill_ids: set[str]) -> list[str]:
    if not isinstance(result, dict):
        return ["router output must be a JSON object"]
    errors = []
    if set(result) != REQUIRED_RESULT:
        errors.append(f"fields must be exactly {sorted(REQUIRED_RESULT)}")
    primary = result.get("primary_skill")
    if primary is not None and primary not in skill_ids:
        errors.append(f"unknown primary_skill: {primary}")
    contributors = result.get("contributors")
    if not isinstance(contributors, list) or any(x not in skill_ids for x in contributors):
        errors.append("contributors must contain only catalog skill IDs")
    elif len(contributors) != len(set(contributors)):
        errors.append("contributors must be unique")
    if result.get("mode") not in MODES:
        errors.append(f"mode must be one of {sorted(MODES)}")
    if not isinstance(result.get("abstain"), bool):
        errors.append("abstain must be boolean")
    confidence = result.get("confidence")
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
        errors.append("confidence must be a number from 0 to 1")
    if not isinstance(result.get("reason"), str) or not result.get("reason", "").strip():
        errors.append("reason must be non-empty")
    if result.get("clarification") is not None and not isinstance(result.get("clarification"), str):
        errors.append("clarification must be a string or null")
    if result.get("mode") == "ASK" and (not result.get("abstain") or not result.get("clarification")):
        errors.append("ASK requires abstain=true and a clarification question")
    if result.get("mode") != "ASK" and result.get("abstain"):
        errors.append("abstain=true requires ASK mode")
    return errors


def router_prompt(query: str, catalog: list[dict]) -> str:
    response_contract = {
        "primary_skill": "catalog ID or null", "contributors": ["catalog ID"],
        "mode": "NONE | AUTO | MANUAL | ASK", "abstain": False,
        "confidence": 0.0, "reason": "short reason", "clarification": None,
    }
    return (
        "Route the request using only the catalog below. Select one primary skill or null. "
        "Contributors are optional secondary skills, not alternatives. Default contributors to "
        "an empty list. Add one only when the request explicitly contains a separate job that the "
        "primary skill cannot own and that contributor is necessary to complete the stated outcome. "
        "Do not add a skill because it is related, might be useful, could review the work later, or "
        "covers a possible concern. Decide the route first, then apply this mode rule exactly. Use "
        "AUTO for every clear normal-language request unless the chosen primary is a deliberate "
        "entrypoint listed below. A skill's host_activation never turns an ordinary request into "
        "MANUAL. "
        "host_activation describes how a host exposes or invokes that skill. It does not require the "
        "user to know a command or skill name. Use MANUAL only when the request explicitly invokes a "
        "command or skill ID, selects the compatibility entrypoint, requests shipping or deployment, "
        "or explicitly starts an autonomous goal loop. Never use MANUAL for any other primary. "
        "Routing never grants "
        "permission for side effects; approval gates still apply after selection. Use ASK and abstain "
        "only when one missing answer materially changes the route. Use NONE when no skill is warranted. "
        "Return JSON "
        "only, with exactly this shape:\n" + json.dumps(response_contract) +
        "\n\nCATALOG:\n" + json.dumps(catalog, ensure_ascii=False) +
        "\n\nUSER REQUEST:\n" + query
    )


def parse_router_output(raw: str, adapter: str = "plain-json") -> tuple[object, dict]:
    usage = {"cost_usd": 0.0, "events": 0}
    if adapter == "opencode-json-v1":
        texts = []
        for number, line in enumerate(raw.splitlines(), 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid OpenCode JSON event at line {number}: {exc}") from exc
            usage["events"] += 1
            if event.get("type") == "text":
                text = event.get("part", {}).get("text")
                if isinstance(text, str):
                    texts.append(text)
            if event.get("type") == "step_finish":
                cost = event.get("part", {}).get("cost", 0)
                if isinstance(cost, (int, float)) and not isinstance(cost, bool):
                    usage["cost_usd"] += cost
        if not texts:
            raise ValueError("OpenCode output contains no final text event")
        raw = texts[-1].strip()
    if raw.startswith("```json") and raw.endswith("```"):
        raw = raw[7:-3].strip()
    try:
        return json.loads(raw), usage
    except json.JSONDecodeError as exc:
        raise ValueError(f"model output is not JSON: {exc}") from exc


def _run_router_with_raw(command: str, prompt: str, timeout: int,
                         adapter: str = "plain-json") -> tuple[object, dict, str]:
    argv = shlex.split(command)
    if not argv:
        raise ValueError("model command is empty")
    result = subprocess.run(argv, input=prompt, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=timeout)
    if result.returncode:
        error = RuntimeError(f"model command exited {result.returncode}: {result.stderr.strip()}")
        error.raw_output = result.stdout
        raise error
    raw = result.stdout.strip()
    try:
        output, usage = parse_router_output(raw, adapter)
    except Exception as exc:
        exc.raw_output = result.stdout
        raise
    return output, usage, result.stdout


def run_router(command: str, prompt: str, timeout: int,
               adapter: str = "plain-json") -> tuple[object, dict]:
    output, usage, _ = _run_router_with_raw(command, prompt, timeout, adapter)
    return output, usage


def run_router_with_retries(command: str, prompt: str, timeout: int, adapter: str,
                            retry_limit: int) -> tuple[object, dict, str, list[dict]]:
    attempts = []
    for attempt in range(retry_limit + 1):
        try:
            output, usage, raw = _run_router_with_raw(command, prompt, timeout, adapter)
            return output, usage, raw, attempts
        except (subprocess.TimeoutExpired, RuntimeError) as exc:
            attempts.append({"attempt": attempt + 1, "error_type": type(exc).__name__,
                             "error": str(exc), "raw_output": getattr(exc, "raw_output", "")})
            if attempt >= retry_limit:
                exc.retry_attempts = attempts
                raise
    raise AssertionError("unreachable retry state")


def write_failed_sidecar(path: Path, dataset: dict, failures: list[dict], report: dict | None = None) -> None:
    path = _validate_external_output(path)
    if dataset["metadata"]["role"] != "sealed_promotion":
        raise ValueError("diagnostic sidecar is only available for sealed promotion")
    if dataset["state"]["retirement_state"] != "RETIRED":
        raise ValueError("diagnostic sidecar requires a retired sealed dataset")
    payload = {
        "schema_version": 1,
        "dataset_role": "sealed_promotion",
        "failures": failures,
    }
    if report is not None:
        payload["report"] = report
    _atomic_json(path, payload)


def wilson(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    if total == 0:
        return (0.0, 0.0)
    p = successes / total
    denominator = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denominator
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * total)) / total) / denominator
    return (max(0.0, centre - margin), min(1.0, centre + margin))


def score(cases: list[dict], results: list[dict], changed_clusters: set[str] | None = None) -> dict:
    rows = []
    confusion_by_cluster: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    confusion_by_skill: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    contributor_tp = contributor_fp = contributor_fn = 0
    forbidden = selected = 0
    abstention_hits = abstention_total = 0
    for case, result in zip(cases, results):
        expected, actual = case["expected_primary"], result["primary_skill"]
        exact = expected == actual
        expected_label, actual_label = expected or "<none>", actual or "<none>"
        confusion_by_cluster[case["cluster"]][f"{expected_label} -> {actual_label}"] += 1
        confusion_by_skill[expected_label][actual_label] += 1
        allowed, got = set(case["allowed_contributors"]), set(result["contributors"])
        contributor_tp += len(allowed & got)
        contributor_fp += len(got - allowed)
        contributor_fn += len(allowed - got)
        chosen = got | ({actual} if actual else set())
        forbidden_hits = chosen & set(case["forbidden_skills"])
        forbidden += len(forbidden_hits)
        selected += len(chosen)
        expects_abstention = case["ambiguity_behavior"] == "ASK_MATERIAL_QUESTION"
        if expects_abstention:
            abstention_total += 1
            abstention_hits += int(result["abstain"] and result["mode"] == "ASK")
        rows.append({
            "id": case["id"], "cluster": case["cluster"], "tier": case["harm_tier"],
            "expected": expected, "actual": actual, "exact_primary": exact,
            "mode_ok": result["mode"] == case["expected_activation_mode"],
            "forbidden": sorted(forbidden_hits), "abstention_ok": (
                result["abstain"] == expects_abstention and
                (not expects_abstention or result["mode"] == "ASK")
            ),
        })
    clear_standard = [r for r, c in zip(rows, cases)
                      if r["tier"] == "STANDARD" and c["ambiguity_behavior"] == "ROUTE"]
    by_owner: dict[str, list[bool]] = defaultdict(list)
    for row in clear_standard:
        by_owner[row["expected"] or "<none>"].append(row["exact_primary"])
    macro = (sum(sum(v) / len(v) for v in by_owner.values()) / len(by_owner)) if by_owner else None
    standard_hits = sum(r["exact_primary"] for r in clear_standard)
    interval = wilson(standard_hits, len(clear_standard))
    clusters = changed_clusters or {c["cluster"] for c in cases}
    violations = []
    violation_categories: dict[str, int] = defaultdict(int)
    def add_violation(category: str, message: str) -> None:
        violation_categories[category] += 1
        violations.append(message)
    for row in rows:
        if row["tier"] == "CRITICAL" and row["forbidden"]:
            add_violation("critical_forbidden_selection", f"{row['id']}: critical forbidden selection")
        if not row["mode_ok"]:
            add_violation("routing_mode_mismatch", f"{row['id']}: routing mode mismatch")
        if row["tier"] in {"CRITICAL", "HIGH"} and row["cluster"] in clusters and not row["exact_primary"]:
            add_violation("high_harm_primary_misroute", f"{row['id']}: high-harm primary misroute")
    if macro is not None and macro < 0.95:
        add_violation("clear_standard_macro_accuracy", f"clear standard macro accuracy {macro:.3f} is below 0.950")
    precision = contributor_tp / (contributor_tp + contributor_fp) if contributor_tp + contributor_fp else 1.0
    recall = contributor_tp / (contributor_tp + contributor_fn) if contributor_tp + contributor_fn else 1.0
    return {
        "passed": not violations, "violations": violations,
        "violation_categories": dict(violation_categories), "cases": rows,
        "metrics": {
            "exact_primary_accuracy": sum(r["exact_primary"] for r in rows) / len(rows),
            "standard_macro_accuracy": macro,
            "standard_clear_case_count": len(clear_standard),
            "standard_exact_primary_wilson_95": (
                [round(interval[0], 4), round(interval[1], 4)] if clear_standard else None
            ),
            "confidence_method": "two-sided Wilson score interval, z=1.96",
            "contributor_precision": precision, "contributor_recall": recall,
            "forbidden_invocation_rate": forbidden / selected if selected else 0.0,
            "abstention_quality": abstention_hits / abstention_total if abstention_total else 1.0,
        },
        "confusion": {
            "per_cluster": {k: dict(v) for k, v in confusion_by_cluster.items()},
            "per_expected_skill": {k: dict(v) for k, v in confusion_by_skill.items()},
        },
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Evaluate Resonance skill routing")
    parser.add_argument("--check", action="store_true", help="validate catalog and public fixtures only")
    parser.add_argument("--model-cmd", default=os.getenv("RESONANCE_ROUTER_CMD"))
    parser.add_argument("--model-id", default=os.getenv("RESONANCE_ROUTER_MODEL_ID"))
    parser.add_argument("--model-adapter", default="plain-json",
                        choices=("plain-json", "opencode-json-v1"))
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--retry-limit", type=int, default=0,
                        help="retry transport failures per case; content failures are never retried")
    parser.add_argument("--case", action="append", default=[],
                        help="run one named public case; repeat to select more")
    parser.add_argument("--results", type=Path, help="write live result JSON outside the repository")
    parser.add_argument("--failed-run-sidecar", type=Path,
                        help="write private sealed-failure diagnostics outside the repository")
    parser.add_argument("--changed-cluster", action="append", default=[])
    parser.add_argument("--validation-holdout-dir", type=Path,
                        default=os.getenv("RESONANCE_ROUTING_VALIDATION_HOLDOUT_DIR"),
                        help="external protected validation dataset")
    parser.add_argument("--promotion-holdout-dir", type=Path,
                        default=os.getenv("RESONANCE_ROUTING_PROMOTION_HOLDOUT_DIR"),
                        help="external sealed promotion dataset")
    args = parser.parse_args(argv)
    if args.retry_limit < 0:
        parser.error("retry limit must be non-negative")
    if args.validation_holdout_dir and args.promotion_holdout_dir:
        parser.error("choose one protected dataset role per run")
    if args.case and (args.validation_holdout_dir or args.promotion_holdout_dir):
        parser.error("case selection is public-only; protected datasets run as a complete cohort")
    protected = None
    if args.validation_holdout_dir:
        protected = load_protected_dataset(args.validation_holdout_dir, "protected_validation")
    elif args.promotion_holdout_dir:
        protected = load_protected_dataset(args.promotion_holdout_dir, "sealed_promotion")
    catalog = load_catalog()
    cases = protected["cases"] if protected else load_cases()
    if args.case:
        requested = set(args.case)
        cases = [case for case in cases if case.get("id") in requested]
        missing = sorted(requested - {case.get("id") for case in cases})
        if missing:
            parser.error(f"unknown public routing case(s): {', '.join(missing)}")
    skill_ids = {item["id"] for item in catalog}
    if protected:
        errors = validate_protected_opacity(protected["root"], cases)
        if errors:
            if protected["metadata"]["role"] == "sealed_promotion":
                print(f"ERROR sealed promotion dataset failed structural validation ({len(errors)} problem(s))")
            else:
                for error in errors:
                    print(f"ERROR {error}")
            assert_protected_unchanged(protected)
            return 1
        if args.failed_run_sidecar:
            try:
                _validate_external_output(args.failed_run_sidecar)
            except ValueError as exc:
                parser.error(str(exc))
            if protected["metadata"]["role"] != "sealed_promotion":
                parser.error("diagnostic sidecar is only available for sealed promotion")
        if args.results and _inside(args.results.expanduser().resolve(strict=False), REPO.resolve()):
            parser.error("protected result summaries must be written outside the repository")
    errors = []
    ids = set()
    for case in cases:
        if case.get("id") in ids:
            errors.append(f"{case.get('id')}: duplicate case id")
        ids.add(case.get("id"))
        errors += [f"{case.get('id', '<unknown>')}: {e}" for e in validate_case(case, skill_ids)]
    errors += validate_case_set(cases)
    if not cases:
        errors.append("no routing fixtures found")
    if errors:
        if protected and protected["metadata"]["role"] == "sealed_promotion":
            print(f"ERROR sealed promotion dataset failed structural validation ({len(errors)} problem(s))")
            assert_protected_unchanged(protected)
            return 1
        for error in errors:
            print(f"ERROR {error}")
        if protected:
            assert_protected_unchanged(protected)
        return 1
    if args.check:
        if protected:
            assert_protected_unchanged(protected)
            print(f"protected {protected['metadata']['role']}: {len(cases)} cases; inputs verified")
            return 0
        clusters = len({case["cluster"] for case in cases})
        tiers = {tier: sum(c["harm_tier"] == tier for c in cases) for tier in sorted(TIERS)}
        print(f"routing fixtures: {len(cases)} cases, {clusters} clusters, tiers={tiers}")
        print(f"startup catalog: {len(catalog)} compiled skill descriptions")
        return 0
    if protected:
        begin_protected_access(protected, args.model_id or "STRUCTURAL_CHECK")
    if not args.model_cmd or not args.model_id:
        parser.error("live mode requires --model-cmd and --model-id")
    outputs = []
    total_cost_usd = 0.0
    total_events = 0
    raw_outputs = []
    failures = []
    for case in cases:
        prompt = router_prompt(case["query"], catalog)
        try:
            if protected:
                assert_protected_unchanged(protected)
                leaks = oracle_leakage(case, prompt)
                if leaks:
                    contaminate(protected, "; ".join(leaks))
                    raise ValueError("protected oracle leakage detected before routing")
            output, usage, raw_output, retry_attempts = run_router_with_retries(
                args.model_cmd, prompt, args.timeout, args.model_adapter, args.retry_limit)
            raw_outputs.append({"case_index": len(raw_outputs), "prompt": prompt,
                                "raw_output": raw_output, "retry_attempts": retry_attempts})
            total_cost_usd += usage["cost_usd"]
            total_events += usage["events"]
            if protected:
                leaks = oracle_leakage(case, prompt, output)
                if leaks:
                    contaminate(protected, "; ".join(leaks))
                    raise ValueError("protected oracle leakage detected before grading")
            problems = validate_result(output, skill_ids)
            if problems:
                raise ValueError("; ".join(problems))
            outputs.append(output)
        except Exception as exc:
            failure = {"case_index": len(raw_outputs), "prompt": prompt,
                             "raw_output": getattr(exc, "raw_output", ""),
                             "retry_attempts": getattr(exc, "retry_attempts", []),
                             "error": str(exc)}
            failures.append(failure)
            if protected:
                try:
                    assert_protected_unchanged(protected)
                except ValueError:
                    pass
            if protected and protected["metadata"]["role"] == "sealed_promotion":
                if args.failed_run_sidecar:
                    write_failed_sidecar(args.failed_run_sidecar, protected, [*raw_outputs, *failures])
                print(f"ERROR sealed promotion routing failed: {type(exc).__name__}")
            else:
                print(f"ERROR {case['id']}: {exc}")
            return 1
    if protected:
        try:
            assert_protected_unchanged(protected)
        except ValueError as exc:
            print(f"ERROR {exc}")
            return 1
    report = score(cases, outputs, set(args.changed_cluster) or None)
    report.update({"schema_version": 1, "model_id": args.model_id})
    report["execution"] = {
        "adapter": args.model_adapter, "cost_usd": round(total_cost_usd, 8),
        "host_events": total_events,
    }
    if protected and not report["passed"] and args.failed_run_sidecar:
        write_failed_sidecar(args.failed_run_sidecar, protected, failures or raw_outputs, report)
    if protected:
        report = protected_summary(report, protected)
        protected_event(protected, "RESULT", passed=report["passed"],
                        summary_hash=hashlib.sha256(json.dumps(report, sort_keys=True).encode()).hexdigest())
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    print(rendered)
    if args.results:
        args.results.parent.mkdir(parents=True, exist_ok=True)
        args.results.write_text(rendered + "\n", encoding="utf-8")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
