#!/usr/bin/env python3
"""
Resonance - Orchestration Eval (grounded outcomes for skills a single completion
cannot measure).

`run_evals.py` grades one chat completion against a rubric. That undersells the
orchestration and runtime skills (`/goal`, `/audit`, `/second-opinion`, `/ship`,
`/retro`, `/update-*`), whose value is spawning agents, running tools, or driving a
repo, not writing prose. This harness measures them by GROUNDED OUTCOME: set up a
fixture, run a real AGENT against the task, then check the world (did the test pass?
was the planted bug named?).

Cases live in `.forge/orch_evals/*.json`:
  {
    "name": "goal_fix_failing_test", "skill": "ops/goal",
    "task": "instruction given to the agent",
    "fixture": {"files": {"rel/path": "file contents", ...}},
    "assert": {"type": "command", "cmd": "node --test", "expect_exit": 0}
          |   {"type": "contains", "any": ["sql injection", "unauthenticated"]}
  }

The AGENT must be a real agent that can use tools (not a bare completion): set
`--agent-cmd "<cmd>"` or `RESONANCE_AGENT_CMD`. It is run with cwd set to the fixture
dir and the skill body plus task on stdin; it is expected to modify files there. A
`command` assertion then runs in that dir; a `contains` assertion checks the agent's
final output. Examples of an agent CLI: a headless `opencode run` or `claude -p`.
Without an agent command the harness only validates case structure.

Usage:
  python .forge/orch_eval.py --check
  RESONANCE_AGENT_CMD="opencode run" python .forge/orch_eval.py
Exit: 0 all passed / structure ok, 1 a case failed, 2 bad args.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FORGE = Path(__file__).resolve().parent
REPO = FORGE.parent
SKILLS = REPO / ".agents" / "skills"
CASES = FORGE / "orch_evals"


def skill_body(skill: str) -> str:
    p = SKILLS / skill / "SKILL.md"
    if not p.exists():
        return ""
    t = p.read_text(encoding="utf-8", errors="replace")
    end = t.find("\n---", 3)
    return t[end + 4:].strip() if t.startswith("---") and end != -1 else t


def check_case(c: dict) -> list[str]:
    problems = []
    for k in ("name", "skill", "task", "fixture", "assert"):
        if k not in c:
            problems.append(f"missing '{k}'")
    if "skill" in c and not (SKILLS / c["skill"] / "SKILL.md").exists():
        problems.append(f"skill not found: {c['skill']}")
    if isinstance(c.get("fixture"), dict) and not c["fixture"].get("files"):
        problems.append("fixture has no files")
    a = c.get("assert", {})
    if a.get("type") not in ("command", "contains"):
        problems.append("assert.type must be 'command' or 'contains'")
    return problems


def run_case(agent_cmd: list[str], c: dict, timeout: int = 900) -> dict:
    work = Path(tempfile.mkdtemp(prefix="orch_"))
    try:
        for rel, content in c["fixture"]["files"].items():
            fp = work / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content, encoding="utf-8")
        prompt = f"Apply the following skill, then do the task in this directory.\n\n<skill>\n{skill_body(c['skill'])}\n</skill>\n\nTASK: {c['task']}"
        try:
            r = subprocess.run(agent_cmd, cwd=str(work), input=prompt, capture_output=True,
                               text=True, encoding="utf-8", errors="replace", timeout=timeout)
            out = ((r.stdout or "") + "\n" + (r.stderr or "")).strip()
        except Exception as e:
            return {"name": c["name"], "passed": False, "detail": f"agent error: {e}"}

        a = c["assert"]
        if a["type"] == "command":
            cr = subprocess.run(a["cmd"], cwd=str(work), shell=True, capture_output=True,
                                text=True, encoding="utf-8", errors="replace", timeout=600)
            ok = cr.returncode == a.get("expect_exit", 0)
            return {"name": c["name"], "passed": ok,
                    "detail": f"`{a['cmd']}` exit {cr.returncode} (want {a.get('expect_exit', 0)})"}
        else:  # contains
            hay = out.lower()
            pats = [p.lower() for p in a.get("any", [])]
            hit = [p for p in pats if p in hay]
            allp = [p.lower() for p in a.get("all", [])]
            miss = [p for p in allp if p not in hay]
            ok = (not pats or bool(hit)) and not miss
            return {"name": c["name"], "passed": ok,
                    "detail": f"matched {hit or 'n/a'}" + (f", missing {miss}" if miss else "")}
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Run Resonance grounded orchestration evals.")
    ap.add_argument("--check", action="store_true", help="validate case structure only")
    ap.add_argument("--agent-cmd", default=os.environ.get("RESONANCE_AGENT_CMD", ""),
                    help="a real agent CLI (tools-capable) run in the fixture dir")
    a = ap.parse_args(argv)

    if not CASES.is_dir():
        print(f"no orch_evals dir at {CASES}"); return 2
    cases = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(CASES.glob("*.json"))]
    if not cases:
        print("no orchestration eval cases found"); return 2

    if a.check or not a.agent_cmd:
        print(f"orch-eval CHECK (structure only): {len(cases)} cases\n")
        bad = 0
        for c in cases:
            probs = check_case(c)
            mark = "ok  " if not probs else "FAIL"
            print(f"  [{mark}] {c.get('name','?'):32} {c.get('skill','?')}"
                  + ("" if not probs else "  " + "; ".join(probs)))
            bad += 1 if probs else 0
        print(f"\n{len(cases)} cases | {bad} structural problem(s)")
        if not a.agent_cmd and not a.check:
            print("(no agent command; ran structure check only. Set --agent-cmd or "
                  "RESONANCE_AGENT_CMD to a tools-capable agent for a grounded run.)")
        return 1 if bad else 0

    cmd = shlex.split(a.agent_cmd)
    print(f"orch-eval GROUNDED run via `{a.agent_cmd}`: {len(cases)} cases\n")
    failed = 0
    for c in cases:
        res = run_case(cmd, c)
        tag = "PASS" if res["passed"] else "FAIL"
        failed += 0 if res["passed"] else 1
        print(f"  {tag}  {c['name']:32} {c['skill']:22} {res['detail']}")
    print(f"\n{len(cases)} cases | {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
