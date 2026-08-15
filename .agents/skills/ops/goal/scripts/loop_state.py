#!/usr/bin/env python3
"""
Resonance - Goal Loop State (the bound enforcer for /goal).

The /goal skill runs a bounded autonomous loop. This makes the bound real: the
caps live in code, not in prose the model can rationalize past. After each slice
is built and verified, the loop calls `check` and obeys the returned directive.
State lives at .resonance/goal_state.json. Pure stdlib.

Directives:
  CONTINUE      keep going to the next slice
  STOP_SLICE    this slice failed max_slice_attempts times: re-plan it or escalate
  STOP_STUCK    no slice advanced in the last stuck_window iterations, OR the same
                failure signature repeated: stop, escalate
  STOP_CAP      hit the total iteration cap: stop, report progress

Pass --sig with a short fingerprint of the failing observation (for example the
tool name plus the error class) so a loop on one identical error is caught early,
not only after the whole stuck window. This is the duplicate-call detector the
reliable-loop literature calls for: the same action failing the same way N times
is a loop, not progress.

Usage:
  python loop_state.py start "Add CSV export" --dod "export button downloads valid CSV; test green" --contract goal_contract.json --plan-hash abc123
  python loop_state.py check slice-2 advanced           # or: progress | failed
  python loop_state.py check slice-2 failed --sig "test:AssertionError"
  python loop_state.py resume                            # after a crash or handover
  python loop_state.py status
  python loop_state.py done                              # clear state when the goal is verified
"""
from __future__ import annotations

import argparse
import json
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path

def _find_forge() -> Path:
    for p in Path(__file__).resolve().parents:
        candidate = p / ".forge"
        if candidate.is_dir():
            return candidate
        if p.name == ".forge":
            return p
    raise RuntimeError("cannot locate .forge directory for Resonance kernel")


FORGE = _find_forge()
if str(FORGE) not in sys.path:
    sys.path.insert(0, str(FORGE))

from kernel.contracts import ContractError, hash_data  # noqa: E402
from kernel.evidence import (  # noqa: E402
    accept_evidence,
    append_attempt,
    atomic_write_json,
    create_receipt,
    file_lock,
    read_receipt,
    transition_goal,
)
from kernel.runner import run_execution  # noqa: E402

STATE = Path(".resonance") / "goal_state.json"
CAPS = {"max_slice_attempts": 3, "max_iters": 40, "stuck_window": 4}

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}


def _save(s: dict) -> None:
    atomic_write_json(STATE, s)


def _load_contract(raw: str | None) -> tuple[dict | None, str | None]:
    if not raw:
        return None, None
    p = Path(raw)
    text = p.read_text(encoding="utf-8") if p.exists() else raw
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return None, f"contract is not valid JSON: {e}"
    if not isinstance(data, dict):
        return None, "contract must be a JSON object"
    required = ("outcome", "acceptance_checks")
    missing = [k for k in required if k not in data]
    if missing:
        return None, f"contract missing required field(s): {', '.join(missing)}"
    if not isinstance(data.get("acceptance_checks"), list) or not data["acceptance_checks"]:
        return None, "contract acceptance_checks must be a non-empty list"
    return data, None


def cmd_start(a) -> int:
    contract, err = _load_contract(a.contract)
    if err:
        print(f"cannot start goal loop: {err}")
        return 2
    plan_hash = a.plan_hash or ""
    if contract and not plan_hash:
        print("cannot start goal loop: approved contract requires --plan-hash")
        return 2
    if contract and not plan_hash.startswith("sha256:"):
        print("cannot start goal loop: --plan-hash must be a sha256:<64 hex> hash")
        return 2
    with file_lock(STATE):
        run_id = "run-" + hashlib.sha256(f"{a.goal}\n{_now()}".encode("utf-8")).hexdigest()[:16]
        criterion_ids = [f"criterion-{i + 1}" for i, _ in enumerate(contract.get("acceptance_checks", []) if contract else [])]
        _save({"schema_version": 1, "goal": a.goal, "dod": a.dod or "", "status": "active",
               "goal_revision": 1, "run_id": run_id, "criterion_ids": criterion_ids,
               "started": _now(), "updated_at": _now(),
               "caps": CAPS, "contract": contract, "contract_hash": hash_data(contract) if contract else "",
               "plan_hash": plan_hash, "iterations": [], "attempts": [], "executions": [], "evidence": [],
               "completed_history": []})
    print(f"goal loop started. DoD: {a.dod or '(none given: define a checkable one before building)'}")
    print(f"caps: {CAPS['max_slice_attempts']} attempts/slice, {CAPS['max_iters']} total, "
          f"stuck after {CAPS['stuck_window']} with no advance.")
    return 0


def cmd_check(a) -> int:
    s = _load()
    if not s:
        print("no active goal. Run `start` first.")
        return 2
    if a.result not in ("advanced", "progress", "failed"):
        print("result must be advanced | progress | failed")
        return 2
    sig = getattr(a, "sig", None)
    entry = {"n": len(s.get("iterations", [])) + 1, "slice": a.slice,
             "result": a.result, "sig": sig, "ts": _now()}
    with file_lock(STATE):
        s = append_attempt(_load(), entry)
        caps = s.get("caps", CAPS)
        its = s["iterations"]
        _save(s)

    # total cap
    if len(its) >= caps["max_iters"]:
        print(f"STOP_CAP  hit {caps['max_iters']} iterations. Stop and report progress.")
        return 0
    # slice failure cap
    slice_attempts = [i for i in its if i["slice"] == a.slice]
    if a.result != "advanced" and len(slice_attempts) >= caps["max_slice_attempts"]:
        print(f"STOP_SLICE  '{a.slice}' has {len(slice_attempts)} attempts without advancing. "
              f"Re-plan this slice or escalate. Do not keep retrying.")
        return 0
    # duplicate-failure detector: the same failing signature repeating is a loop on
    # one error, caught earlier than the whole-window stuck check.
    if a.result != "advanced" and sig:
        same_sig = [i for i in its if i.get("sig") == sig and i["result"] != "advanced"]
        if len(same_sig) >= caps["max_slice_attempts"]:
            print(f"STOP_STUCK  the same failure signature repeated {len(same_sig)} times "
                  f"('{sig}'). You are looping on one error, not making progress. "
                  f"Change the approach or escalate; do not retry it again.")
            return 0
    # stuck detector
    window = its[-caps["stuck_window"]:]
    if len(window) >= caps["stuck_window"] and all(i["result"] != "advanced" for i in window):
        print(f"STOP_STUCK  no slice advanced in the last {caps['stuck_window']} iterations. "
              f"Stop, widen scope or escalate.")
        return 0
    print("CONTINUE  proceed to the next slice.")
    return 0


def cmd_status(a) -> int:
    s = _load()
    if not s:
        print("no active goal.")
        return 0
    its = s["iterations"]
    adv = sum(1 for i in its if i["result"] == "advanced")
    print(f"goal: {s['goal']}")
    print(f"status: {s.get('status', 'active')}")
    print(f"DoD: {s['dod']}")
    if s.get("contract"):
        print(f"contract outcome: {s['contract'].get('outcome', '(none)')}")
    if s.get("plan_hash"):
        print(f"plan hash: {s['plan_hash']}")
    if s.get("run_id"):
        print(f"run id: {s['run_id']}")
    ev_count = len(s.get("evidence", []))
    if ev_count:
        print(f"accepted evidence receipts: {ev_count}")
    print(f"iterations: {len(its)}  advanced: {adv}  last: {its[-1] if its else '(none)'}")
    return 0


def cmd_exec(a) -> int:
    if not _load():
        print("no active goal. Run `start` first.")
        return 2
    command = a.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        print("exec requires a command after --")
        return 2
    with file_lock(STATE):
        s = _load()
        receipt = run_execution(a.action_id, command, Path.cwd())
        path = Path(".resonance") / "executions" / f"{receipt['execution_id']}.json"
        create_receipt(path, receipt)
        s.setdefault("executions", [])
        s["executions"] = list(s["executions"]) + [receipt]
        s.setdefault("execution_receipts", [])
        s["execution_receipts"] = list(s["execution_receipts"]) + [path.as_posix()]
        _save(s)
    print(f"execution recorded: {receipt['execution_id']} exit={receipt['exit_code']}")
    return 0


def cmd_evidence(a) -> int:
    s = _load()
    if not s:
        print("no active goal. Run `start` first.")
        return 2
    try:
        evidence = read_receipt(a.evidence)
        approval = read_receipt(a.approval) if a.approval else None
        with file_lock(STATE):
            new_state = accept_evidence(_load(), evidence, approval)
            path = Path(".resonance") / "evidence" / f"{evidence['evidence_id']}.json"
            create_receipt(path, evidence)
            try:
                _save(new_state)
            except Exception:
                try:
                    path.unlink()
                finally:
                    raise
    except (ContractError, OSError, json.JSONDecodeError) as e:
        print(f"evidence rejected: {e}")
        return 2
    print(f"evidence accepted: {evidence.get('evidence_id')}")
    return 0


def cmd_achieve(a) -> int:
    s = _load()
    if not s:
        print("no active goal. Run `start` first.")
        return 2
    try:
        with file_lock(STATE):
            _save(transition_goal(_load(), "achieved"))
    except (ContractError, ValueError) as e:
        print(f"cannot achieve goal: {e}")
        return 2
    print("goal achieved with accepted evidence.")
    return 0


def cmd_cancel(a) -> int:
    s = _load()
    if not s:
        print("no active goal. Run `start` first.")
        return 2
    try:
        with file_lock(STATE):
            _save(transition_goal(_load(), "cancelled"))
    except ValueError as e:
        print(f"cannot cancel goal: {e}")
        return 2
    print("goal cancelled.")
    return 0


def cmd_resume(a) -> int:
    """After a crash, a /handover, or a new session, read the persisted state and
    say where to pick up. The loop state is the checkpoint; this reads it back so a
    run resumes at the last unverified slice instead of restarting."""
    s = _load()
    if not s:
        print("no active goal to resume. Run `start` to begin one.")
        return 0
    its = s["iterations"]
    advanced = sorted({i["slice"] for i in its if i["result"] == "advanced"})
    last = its[-1] if its else None
    print(f"RESUME  goal: {s['goal']}")
    print(f"DoD: {s['dod'] or '(none set: define a checkable one before building)'}")
    if s.get("contract"):
        print(f"contract outcome: {s['contract'].get('outcome', '(none)')}")
    if s.get("plan_hash"):
        print(f"plan hash: {s['plan_hash']}")
    print(f"iterations so far: {len(its)} (cap {s.get('caps', CAPS)['max_iters']})")
    print(f"slices advanced: {', '.join(advanced) if advanced else '(none yet)'}")
    if last:
        tail = f" [{last.get('sig')}]" if last.get("sig") else ""
        print(f"last check: slice '{last['slice']}' -> {last['result']}{tail}")
    print("Continue from the first slice not yet advanced. Recall memory first, then run "
          "the loop from there. Do not restart slices already verified.")
    return 0


def cmd_done(a) -> int:
    s = _load()
    if s and s.get("status") != "achieved":
        print("cannot clear goal loop until status is achieved. Use cancel to stop an abandoned goal.")
        return 2
    if s:
        history = Path(".resonance") / "goal_history.json"
        raw = json.loads(history.read_text(encoding="utf-8")) if history.exists() else {"schema_version": 1, "completed": []}
        completed = raw.get("completed", []) if isinstance(raw, dict) else raw
        completed.append(s)
        atomic_write_json(history, {"schema_version": 1, "completed": completed})
    if STATE.exists():
        STATE.unlink()
    print("goal loop cleared after achievement; completed history retained.")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Bound enforcer for the /goal loop.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("start"); p.add_argument("goal"); p.add_argument("--dod")
    p.add_argument("--contract", help="approved goal contract JSON object or path")
    p.add_argument("--plan-hash", default="", help="hash of the approved plan artifact")
    p = sub.add_parser("check"); p.add_argument("slice"); p.add_argument("result")
    p.add_argument("--sig", default=None, help="short fingerprint of the failing observation")
    p = sub.add_parser("exec"); p.add_argument("action_id"); p.add_argument("command", nargs=argparse.REMAINDER)
    p = sub.add_parser("evidence"); p.add_argument("evidence")
    p.add_argument("--approval", default="", help="approval receipt JSON or path for overrides")
    sub.add_parser("achieve"); sub.add_parser("cancel")
    sub.add_parser("resume"); sub.add_parser("status"); sub.add_parser("done")
    a = ap.parse_args(argv)
    return {"start": cmd_start, "check": cmd_check, "status": cmd_status,
            "exec": cmd_exec, "evidence": cmd_evidence, "achieve": cmd_achieve, "cancel": cmd_cancel,
            "resume": cmd_resume, "done": cmd_done}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
