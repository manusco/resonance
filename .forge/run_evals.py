#!/usr/bin/env python3
"""
Resonance Forge - Eval Runner (R1).

Skills ship golden cases in evals/*.json. `validate_skill.py` checks they EXIST;
this actually RUNS them. Two modes:

  --check (default when no model is configured): structural gate, free, <1s.
     Verifies every case has a matching skill name, a query, and a non-empty
     `expected_behavior` rubric, and that the skill compiles. CI-safe.

  live run (when a model command is available): for each case, prompt a model
     WITH and WITHOUT the skill body, then have a judge model grade each output
     against the rubric. Reports the gap the skill closes (with-minus-without).

The model is pluggable so this stays cross-tool and never hard-locks a vendor:
  --model-cmd "claude -p"        (default; reads the prompt on stdin)
  env RESONANCE_MODEL_CMD="..."  (same)
Any CLI that reads a prompt on stdin and prints the completion works.

Usage:
  python .forge/run_evals.py --all --check
  python .forge/run_evals.py marketing/copywriter
  python .forge/run_evals.py marketing/copywriter --model-cmd "claude -p"

Exit codes: 0 all pass, 1 a case failed or a structural problem, 2 bad args.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

FORGE = Path(__file__).resolve().parent
REPO = FORGE.parent
SKILLS = REPO / ".agents" / "skills"
NAME_RE = re.compile(r"(?m)^name:\s*(.+?)\s*$")


def skill_name(skill_md: Path) -> str:
    m = NAME_RE.search(skill_md.read_text(encoding="utf-8", errors="replace")[:2000])
    return m.group(1).strip().strip('"').strip("'") if m else ""


def skill_body(skill_md: Path) -> str:
    t = skill_md.read_text(encoding="utf-8", errors="replace")
    end = t.find("\n---", 3)
    return t[end + 4:].strip() if t.startswith("---") and end != -1 else t


def find_cases(path: str) -> list[tuple[Path, Path]]:
    """Return (skill_md, eval_json) pairs for one skill path or --all."""
    out = []
    roots = sorted(SKILLS.glob("**/SKILL.md")) if path == "--all" else [SKILLS / path / "SKILL.md"]
    for sk in roots:
        evdir = sk.parent / "evals"
        if evdir.is_dir():
            for ev in sorted(evdir.glob("*.json")):
                out.append((sk, ev))
    return out


def run_model(cmd: list[str], prompt: str) -> str:
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=300)
    return (r.stdout or "").strip()


def build_prompt(case: dict, body: str | None) -> str:
    parts = []
    if body:
        parts.append("Apply the following skill to the task.\n\n<skill>\n" + body + "\n</skill>\n")
    for f in case.get("files", []) or []:
        fp = REPO / f
        if fp.exists():
            parts.append(f"<file path=\"{f}\">\n{fp.read_text(encoding='utf-8', errors='replace')}\n</file>")
    parts.append("Task: " + case["query"])
    return "\n\n".join(parts)


def judge(cmd: list[str], query: str, output: str, rubric: list[str]) -> list[bool]:
    items = "\n".join(f"{i+1}. {r}" for i, r in enumerate(rubric))
    p = (f"You are grading an AI output against a rubric. Be strict and literal.\n\n"
         f"TASK:\n{query}\n\nOUTPUT:\n{output}\n\nRUBRIC (each item pass or fail):\n{items}\n\n"
         f"Reply with ONLY a JSON array of booleans, one per rubric item, e.g. [true,false,true].")
    raw = run_model(cmd, p)
    m = re.search(r"\[[^\]]*\]", raw)
    try:
        vals = json.loads(m.group(0)) if m else []
        return [bool(v) for v in vals][:len(rubric)] + [False] * (len(rubric) - len(vals))
    except Exception:
        return [False] * len(rubric)


def check_case(sk: Path, ev: Path) -> list[str]:
    problems = []
    try:
        d = json.loads(ev.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"invalid JSON: {e}"]
    if d.get("skill") != skill_name(sk):
        problems.append(f"skill field '{d.get('skill')}' != frontmatter name '{skill_name(sk)}'")
    if not d.get("query", "").strip():
        problems.append("empty query")
    rub = d.get("expected_behavior")
    if not isinstance(rub, list) or not rub:
        problems.append("expected_behavior is missing or empty")
    return problems


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Run Resonance golden evals.")
    ap.add_argument("path", nargs="?", default=None, help="skill path (e.g. marketing/seo); omit for all")
    ap.add_argument("--all", action="store_true", help="run every skill's evals")
    ap.add_argument("--check", action="store_true", help="structure only, no model")
    ap.add_argument("--model-cmd", default=os.environ.get("RESONANCE_MODEL_CMD", ""),
                    help="model command reading the prompt on stdin (default: claude -p)")
    ap.add_argument("--threshold", type=float, default=0.8, help="fraction of rubric to pass")
    args = ap.parse_args(argv)

    target = "--all" if (args.all or not args.path) else args.path
    cases = find_cases(target)
    if not cases:
        print(f"no evals found for '{target}'")
        return 2

    # decide mode
    model_cmd = args.model_cmd
    if not args.check and not model_cmd:
        model_cmd = "claude -p" if _has("claude") else ""
    live = bool(model_cmd) and not args.check

    if not live:
        print(f"eval CHECK (structure only): {len(cases)} cases\n")
        bad = 0
        for sk, ev in cases:
            probs = check_case(sk, ev)
            if probs:
                bad += 1
                print(f"  FAIL  {ev.relative_to(REPO).as_posix()}")
                for p in probs:
                    print(f"        {p}")
        print(f"\n{len(cases)} cases | {bad} structural problem(s)")
        if args.check is False and not model_cmd:
            print("(no model command found; ran structure check only. "
                  "Set --model-cmd or RESONANCE_MODEL_CMD, e.g. 'claude -p', for a live run.)")
        return 1 if bad else 0

    cmd = shlex.split(model_cmd)
    print(f"eval LIVE run via `{model_cmd}`: {len(cases)} cases\n")
    failed = 0
    for sk, ev in cases:
        d = json.loads(ev.read_text(encoding="utf-8"))
        rub = d["expected_behavior"]
        with_out = run_model(cmd, build_prompt(d, skill_body(sk)))
        without = run_model(cmd, build_prompt(d, None))
        gw = judge(cmd, d["query"], with_out, rub)
        gwo = judge(cmd, d["query"], without, rub)
        sw, swo = sum(gw), sum(gwo)
        ok = sw >= args.threshold * len(rub) and sw >= swo
        failed += 0 if ok else 1
        tag = "PASS" if ok else "FAIL"
        print(f"  {tag}  {ev.relative_to(REPO).as_posix()}  with={sw}/{len(rub)} without={swo}/{len(rub)}")
    print(f"\n{len(cases)} cases | {failed} failed")
    return 1 if failed else 0


def _has(exe: str) -> bool:
    from shutil import which
    return which(exe) is not None


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
