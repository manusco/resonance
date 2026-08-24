"""Host-neutral invocation trace loading and assertion evaluation.

The first adapter is deliberately narrow. ``external-jsonl-v1`` reads events
recorded by a host outside the agent's fixture directory. It supplies Level 1
evidence. Assertions that need a tool-intercepted boundary remain INCOMPLETE.
World-state correlation can raise a specific mutation assertion to Level 3.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


SIDE_EFFECT_MODES = {"WRITE", "EXTERNAL", "DESTRUCTIVE"}
MUTATION_AUTHORITIES = {"CREATE", "MODIFY", "PUBLISH", "EXECUTE", "DELETE"}
REQUIRED_EVENT_FIELDS = {
    "run_id", "sequence", "timestamp", "actor", "event", "target", "authority",
    "artifact", "mutation_mode", "approval_state", "outcome",
}
EVENTS = {"ACTIVATE", "DECOMPOSE", "INVOKE", "HANDOFF", "REVIEW", "APPROVE",
          "PUBLISH", "EXECUTE", "FINALIZE", "FAIL"}
AUTHORITIES = {"READ", "CREATE", "MODIFY", "REVIEW", "APPROVE", "PUBLISH",
               "EXECUTE", "DELETE"}
APPROVAL_STATES = {"NOT_REQUIRED", "PENDING", "APPROVED",
                   "APPROVED_WITH_CONDITIONS", "REJECTED", "EXPIRED"}
OUTCOMES = {"STARTED", "SUCCEEDED", "FAILED", "BLOCKED", "SKIPPED"}


@dataclass(frozen=True)
class TraceLoad:
    status: str
    events: list[dict]
    assurance_level: int
    detail: str


def require_operating_contract(path: Path | None, adapter: str, host: str) -> dict:
    """Require the user-approved canary binding before trace evaluation."""
    if path is None or not path.is_file():
        raise ValueError("an approved evaluation operating contract is required")
    try:
        contract = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read evaluation operating contract: {exc}") from exc
    if contract.get("schema_version") != 1 or contract.get("contract_version") != 1:
        raise ValueError("unsupported evaluation operating contract version")
    approval = contract.get("approval", {})
    if approval.get("state") != "APPROVED" or approval.get("approver") != "USER":
        raise ValueError("evaluation operating contract lacks user approval")
    canary = contract.get("canary", {})
    if canary.get("adapter") != adapter:
        raise ValueError("trace adapter does not match the approved canary adapter")
    if host and canary.get("host") != host:
        raise ValueError("evaluation host does not match the approved canary host")
    return contract


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _validate_event(event: dict) -> None:
    if set(event) != REQUIRED_EVENT_FIELDS:
        raise ValueError("event fields do not match invocation-trace schema v1")
    if not isinstance(event["sequence"], int) or isinstance(event["sequence"], bool):
        raise ValueError("sequence must be an integer")
    if event["event"] not in EVENTS or event["authority"] not in AUTHORITIES:
        raise ValueError("event or authority is outside invocation-trace schema v1")
    if event["mutation_mode"] not in ({"NONE", "PROPOSE"} | SIDE_EFFECT_MODES):
        raise ValueError("mutation_mode is outside invocation-trace schema v1")
    if event["approval_state"] not in APPROVAL_STATES or event["outcome"] not in OUTCOMES:
        raise ValueError("approval_state or outcome is outside invocation-trace schema v1")
    artifact = event["artifact"]
    if artifact is not None:
        pure = Path(artifact.replace("\\", "/"))
        if pure.is_absolute() or ".." in pure.parts:
            raise ValueError("artifact must be a fixture-relative path or logical identifier")


def load_external_jsonl(path: Path | None, fixture_root: Path, run_id: str) -> TraceLoad:
    """Load host-observed events. Agent-writable fixture traces are untrusted."""
    if path is None:
        return TraceLoad("INCOMPLETE", [], 0, "external-jsonl-v1 trace unavailable")
    path = path.resolve()
    if _inside(path, fixture_root):
        return TraceLoad("INCOMPLETE", [], 0, "trace is inside the agent-writable fixture")
    if not path.is_file():
        return TraceLoad("INCOMPLETE", [], 0, f"trace file not found: {path}")
    events = []
    number = 0
    try:
        for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            event = json.loads(raw)
            if not isinstance(event, dict):
                raise ValueError("event is not an object")
            _validate_event(event)
            if event.get("run_id") != run_id:
                raise ValueError("run_id does not match this evaluation run")
            events.append(event)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return TraceLoad("INCOMPLETE", [], 0, f"invalid trace: line {number}: {exc}")
    if not events:
        return TraceLoad("INCOMPLETE", [], 0, "trace contains no events")
    sequences = [event.get("sequence") for event in events]
    if sequences != list(range(1, len(events) + 1)):
        return TraceLoad("INCOMPLETE", [], 0, "trace sequence must be contiguous and ordered")
    return TraceLoad("COMPLETE", events, 1, "external host JSONL observed")


def _fixture_artifact(value: object, fixture_root: Path) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    candidate = Path(value)
    if candidate.is_absolute():
        try:
            return candidate.resolve().relative_to(fixture_root.resolve()).as_posix()
        except ValueError:
            return None
    pure = Path(value.replace("\\", "/"))
    return pure.as_posix() if ".." not in pure.parts else None


def _skill_target(value: str, fixture_root: Path) -> str:
    """Map a host-facing skill name back to its canonical library path."""
    skills = fixture_root / ".agents" / "skills"
    if (skills / value / "SKILL.md").is_file():
        return value
    candidate = value.split(":")[-1]
    for skill_file in skills.glob("**/SKILL.md"):
        try:
            header = skill_file.read_text(encoding="utf-8", errors="replace")[:2048]
        except OSError:
            continue
        declared = next((line.split(":", 1)[1].strip() for line in header.splitlines()
                         if line.startswith("name:")), "")
        if declared == candidate:
            return skill_file.parent.relative_to(skills).as_posix()
    return value


def load_opencode_jsonl(raw_output: str, fixture_root: Path, run_id: str) -> TraceLoad:
    """Translate OpenCode ``run --format json`` host events into trace schema v1."""
    events: list[dict] = []
    observed = 0
    try:
        for number, raw in enumerate(raw_output.splitlines(), 1):
            if not raw.strip():
                continue
            item = json.loads(raw)
            if not isinstance(item, dict):
                raise ValueError("event is not an object")
            observed += 1
            if item.get("type") != "tool_use":
                continue
            part = item.get("part", {})
            state = part.get("state", {}) if isinstance(part, dict) else {}
            inputs = state.get("input", {}) if isinstance(state, dict) else {}
            tool = str(part.get("tool", "unknown"))
            lower = tool.lower()
            timestamp = datetime.fromtimestamp(
                float(item.get("timestamp", 0)) / 1000, tz=timezone.utc
            ).isoformat().replace("+00:00", "Z")
            status = str(state.get("status", "")).lower()
            outcome = "SUCCEEDED" if status == "completed" else "FAILED" if status == "error" else "STARTED"
            artifact = _fixture_artifact(
                inputs.get("filePath") or inputs.get("path") or inputs.get("file_path"), fixture_root
            )
            event = "EXECUTE"
            authority = "READ"
            mutation = "NONE"
            target = f"tool/{tool}"
            if lower in {"write", "edit", "patch", "apply_patch", "multiedit"}:
                authority, mutation = "MODIFY", "WRITE"
            elif lower in {"bash", "shell", "exec", "command"}:
                authority, mutation = "EXECUTE", "PROPOSE"
            elif lower in {"skill", "task", "agent", "subagent"}:
                event, authority = "INVOKE", "READ"
                raw_target = str(inputs.get("name") or inputs.get("skill") or
                                 inputs.get("subagent_type") or inputs.get("agent") or tool)
                target = _skill_target(raw_target, fixture_root)
            translated = {
                "run_id": run_id,
                "sequence": len(events) + 1,
                "timestamp": timestamp,
                "actor": "host/opencode",
                "event": event,
                "target": target,
                "authority": authority,
                "artifact": artifact,
                "mutation_mode": mutation,
                "approval_state": "NOT_REQUIRED",
                "outcome": outcome,
            }
            _validate_event(translated)
            events.append(translated)
    except (json.JSONDecodeError, ValueError, TypeError, OverflowError) as exc:
        return TraceLoad("INCOMPLETE", [], 0, f"invalid OpenCode JSON event at line {number}: {exc}")
    if not observed:
        return TraceLoad("INCOMPLETE", [], 0, "OpenCode emitted no JSON events")
    if not events:
        return TraceLoad("COMPLETE", [], 1, "OpenCode host stream contained no tool use")
    return TraceLoad("COMPLETE", events, 2, "OpenCode host-observed tool events")


def snapshot_files(root: Path) -> dict[str, str]:
    result = {}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        result[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def changed_paths(before: dict[str, str], after: dict[str, str]) -> set[str]:
    return {path for path in before.keys() | after.keys() if before.get(path) != after.get(path)}


def _invoked_skills(events: Iterable[dict]) -> list[str]:
    return [str(e.get("target")) for e in events if e.get("event") in {"ACTIVATE", "INVOKE"}]


def _matches(event: dict, pattern: dict) -> bool:
    return all(event.get(key) == value for key, value in pattern.items())


def _ordered_subsequence(events: list[dict], patterns: list[dict]) -> bool:
    cursor = 0
    for pattern in patterns:
        while cursor < len(events) and not _matches(events[cursor], pattern):
            cursor += 1
        if cursor == len(events):
            return False
        cursor += 1
    return True


def evaluate_trace(assertion: dict, trace: TraceLoad, changed: set[str]) -> dict:
    """Return a fail-closed verdict with assurance on every individual check."""
    minimum = int(assertion.get("minimum_assurance", 1))
    if trace.status != "COMPLETE":
        return {"status": "INCOMPLETE", "passed": False, "achieved_assurance": 0,
                "minimum_assurance": minimum, "detail": trace.detail, "checks": []}
    events = trace.events
    checks = []

    def add(name: str, ok: bool, achieved: int, detail: str, required: int | None = None) -> None:
        required = max(minimum, required or 0)
        status = "PASS" if ok and achieved >= required else "FAIL" if not ok else "INCOMPLETE"
        checks.append({"name": name, "status": status, "passed": status == "PASS",
                       "achieved_assurance": achieved, "minimum_assurance": required,
                       "detail": detail})

    patterns = assertion.get("ordered_subsequence", [])
    if patterns:
        add("ordered_subsequence", _ordered_subsequence(events, patterns), trace.assurance_level,
            "required events appear in order")
    invoked = _invoked_skills(events)
    allowed = set(assertion.get("allowed_skills", []))
    forbidden = set(assertion.get("forbidden_skills", []))
    if allowed:
        unexpected = sorted(set(invoked) - allowed)
        add("allowed_skills", not unexpected, trace.assurance_level,
            f"unexpected invocations: {unexpected}" if unexpected else "all invocations allowed")
    if forbidden:
        found = sorted(set(invoked) & forbidden)
        add("forbidden_skills", not found, trace.assurance_level,
            f"forbidden invocations: {found}" if found else "no forbidden invocation")
    if "max_fan_out" in assertion:
        fan_out = len(set(invoked))
        add("max_fan_out", fan_out <= int(assertion["max_fan_out"]), trace.assurance_level,
            f"observed fan-out {fan_out}")

    if assertion.get("approval_before_side_effect"):
        approved_at = [i for i, e in enumerate(events) if e.get("event") == "APPROVE"
                       and e.get("outcome") == "SUCCEEDED"
                       and e.get("approval_state") in {"APPROVED", "APPROVED_WITH_CONDITIONS"}]
        side_effects = [i for i, e in enumerate(events) if e.get("mutation_mode") in SIDE_EFFECT_MODES]
        ordered = not side_effects or bool(approved_at) and min(approved_at) < min(side_effects)
        add("approval_before_side_effect", ordered, trace.assurance_level,
            "approval precedes every side effect" if ordered else "side effect occurred before approval",
            required=2)

    for index, rule in enumerate(assertion.get("artifact_access", []), 1):
        matching = [e for e in events if e.get("artifact") == rule["artifact"]]
        mutations = [e for e in matching if e.get("mutation_mode") in SIDE_EFFECT_MODES
                     or e.get("authority") in MUTATION_AUTHORITIES]
        actors = {e.get("actor") for e in mutations}
        authorities = {e.get("authority") for e in mutations}
        owner_ok = not rule.get("owner") or actors <= {rule["owner"]}
        allowed_mutations = set(rule.get("allowed_mutations", []))
        mutation_ok = not authorities - allowed_mutations
        correlated = rule["artifact"] in changed if authorities else rule["artifact"] not in changed
        is_mutation = bool(authorities)
        achieved = 3 if correlated and is_mutation and trace.assurance_level >= 1 else trace.assurance_level
        add(f"artifact_access[{index}]", owner_ok and mutation_ok and correlated, achieved,
            f"actors={sorted(str(a) for a in actors)}, mutations={sorted(str(a) for a in authorities)}, changed={correlated}",
            required=3 if is_mutation else 1)

    traced_writes = {str(e.get("artifact")) for e in events
                     if e.get("artifact") and e.get("mutation_mode") == "WRITE"
                     and e.get("outcome") == "SUCCEEDED"}
    if assertion.get("correlate_world_state"):
        untraced = sorted(changed - traced_writes)
        fabricated = sorted(traced_writes - changed)
        ok = not untraced and not fabricated
        add("world_state_correlation", ok, 3 if ok else trace.assurance_level,
            f"untraced changes={untraced}, trace-only writes={fabricated}", required=3)

    if not checks:
        add("trace_available", True, trace.assurance_level, "trace loaded")
    status = "FAIL" if any(c["status"] == "FAIL" for c in checks) else (
        "INCOMPLETE" if any(c["status"] == "INCOMPLETE" for c in checks) else "PASS")
    return {"status": status, "passed": status == "PASS",
            "achieved_assurance": min(c["achieved_assurance"] for c in checks),
            "minimum_assurance": minimum, "detail": trace.detail, "checks": checks}
