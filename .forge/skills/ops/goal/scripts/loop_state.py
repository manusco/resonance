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
  STOP_STUCK    no slice advanced in the last stuck_window iterations: stop, escalate
  STOP_CAP      hit the total iteration cap: stop, report progress

Usage:
  python loop_state.py start "Add CSV export" --dod "export button downloads valid CSV; test green"
  python loop_state.py check slice-2 advanced     # or: progress | failed
  python loop_state.py status
  python loop_state.py done                        # clear state when the goal is verified
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

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
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(s, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cmd_start(a) -> int:
    _save({"goal": a.goal, "dod": a.dod or "", "started": _now(),
           "caps": CAPS, "iterations": []})
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
    s["iterations"].append({"n": len(s["iterations"]) + 1, "slice": a.slice,
                            "result": a.result, "ts": _now()})
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
    print(f"DoD: {s['dod']}")
    print(f"iterations: {len(its)}  advanced: {adv}  last: {its[-1] if its else '(none)'}")
    return 0


def cmd_done(a) -> int:
    if STATE.exists():
        STATE.unlink()
    print("goal loop cleared.")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Bound enforcer for the /goal loop.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("start"); p.add_argument("goal"); p.add_argument("--dod")
    p = sub.add_parser("check"); p.add_argument("slice"); p.add_argument("result")
    sub.add_parser("status"); sub.add_parser("done")
    a = ap.parse_args(argv)
    return {"start": cmd_start, "check": cmd_check, "status": cmd_status, "done": cmd_done}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
