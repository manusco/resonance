#!/usr/bin/env python3
"""
Resonance Forge - Eval Runner and Scorecard (R1 + Track 1).

Skills ship golden cases in evals/*.json. `validate_skill.py` checks they EXIST;
this actually RUNS them and measures the lift each skill produces.

Modes:
  --check      structural gate, free, <1s. Every case has a matching skill name,
               a query, and a non-empty rubric. CI-safe. (Default with no model.)
  live         for each case, prompt a model WITH and WITHOUT the skill body, then
               have a judge grade both against the rubric. Reports with-minus-without.
  --score      live run aggregated into a per-skill scorecard (docs/EVAL_SCORECARD.md
               and .forge/eval_results.json): the measured proof that a skill helps,
               and the list of skills that do not (the /improve work-list).

The model is pluggable so this stays cross-tool and never locks a vendor:
  --model-cmd "claude -p"        (default when the claude CLI is present)
  env RESONANCE_MODEL_CMD="..."  (same)
Any CLI that reads a prompt on stdin and prints the completion works.

Selection:
  path (e.g. marketing/seo) | --all | --changed [ref]   (only skills changed vs ref)
  --limit N   cap cases per skill (cheap sampling)
  --parallel N   concurrent model calls (default 4)

Usage:
  python .forge/run_evals.py --all --check
  python .forge/run_evals.py --all --score --model-cmd "claude -p"
  python .forge/run_evals.py --changed --score --limit 1

Exit: 0 pass, 1 a case failed / structural problem / a skill showed no lift, 2 bad args.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

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


def skill_rel(sk: Path) -> str:
    return sk.parent.relative_to(SKILLS).as_posix()


def changed_skill_paths(ref: str) -> set[str]:
    """Skill dirs (domain/name) whose source or output changed vs a git ref."""
    try:
        r = subprocess.run(["git", "diff", "--name-only", ref], cwd=str(REPO),
                           capture_output=True, text=True, timeout=30)
    except Exception:
        return set()
    out: set[str] = set()
    for f in r.stdout.splitlines():
        m = re.search(r"(?:\.agents|\.forge)/skills/(.+?)/(?:SKILL\.md|skill\.tmpl\.md|references/|evals/)", f)
        if m:
            out.add(m.group(1))
    return out


def find_cases(path: str, changed_ref: str | None) -> list[tuple[Path, Path]]:
    out = []
    roots = sorted(SKILLS.glob("**/SKILL.md")) if path == "--all" else [SKILLS / path / "SKILL.md"]
    changed = changed_skill_paths(changed_ref) if changed_ref else None
    for sk in roots:
        if changed is not None and skill_rel(sk) not in changed:
            continue
        evdir = sk.parent / "evals"
        if evdir.is_dir():
            for ev in sorted(evdir.glob("*.json")):
                out.append((sk, ev))
    return out


def run_model(cmd: list[str], prompt: str) -> str:
    try:
        # force UTF-8 on stdin/stdout: skill bodies use non-ASCII (arrows, quotes)
        # that the Windows locale (cp1252) cannot encode, which would silently fail.
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=300,
                           encoding="utf-8", errors="replace")
        return (r.stdout or "").strip()
    except Exception as e:
        return f"[model error: {e}]"


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
        return ([bool(v) for v in vals] + [False] * len(rubric))[:len(rubric)]
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


def run_case(cmd: list[str], sk: Path, ev: Path, threshold: float) -> dict:
    d = json.loads(ev.read_text(encoding="utf-8"))
    rub = d["expected_behavior"]
    with_out = run_model(cmd, build_prompt(d, skill_body(sk)))
    without = run_model(cmd, build_prompt(d, None))
    sw = sum(judge(cmd, d["query"], with_out, rub))
    swo = sum(judge(cmd, d["query"], without, rub))
    n = len(rub)
    return {"skill": skill_name(sk), "path": skill_rel(sk), "eval": ev.name, "rubric_n": n,
            "with": sw, "without": swo, "with_frac": sw / n, "without_frac": swo / n,
            "pass": sw >= threshold * n and sw >= swo}


def verdict(with_avg: float, lift: float, threshold: float) -> str:
    if with_avg >= threshold and lift > 0.05:
        return "proven"
    if lift < -0.05 or with_avg < threshold - 0.2:
        return "weak"
    return "flat"


def write_scorecard(results: list[dict], threshold: float) -> tuple[str, dict]:
    by_skill: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        by_skill[r["path"]].append(r)
    rows = []
    for path, rs in sorted(by_skill.items()):
        n = len(rs)
        wavg = sum(r["with_frac"] for r in rs) / n
        woavg = sum(r["without_frac"] for r in rs) / n
        lift = wavg - woavg
        rows.append({"path": path, "skill": rs[0]["skill"], "cases": n,
                     "with": round(wavg, 3), "without": round(woavg, 3), "lift": round(lift, 3),
                     "verdict": verdict(wavg, lift, threshold)})
    rows.sort(key=lambda x: x["lift"], reverse=True)
    proven = sum(1 for r in rows if r["verdict"] == "proven")
    weak = [r["path"] for r in rows if r["verdict"] == "weak"]

    lines = ["# Resonance Eval Scorecard", "",
             "Measured lift per skill: the same task graded with and without the skill "
             "in context. `with` and `without` are the mean fraction of the rubric satisfied. "
             "`lift` is the gap the skill closes. Produced by `.forge/run_evals.py --score`.", "",
             f"- Skills measured: **{len(rows)}**  |  proven (real lift): **{proven}**  |  "
             f"weak (no lift, the /improve work-list): **{len(weak)}**", "",
             "| skill | cases | without | with | lift | verdict |", "| :-- | --: | --: | --: | --: | :-- |"]
    for r in rows:
        lines.append(f"| `{r['path']}` | {r['cases']} | {r['without']:.2f} | {r['with']:.2f} | "
                     f"{r['lift']:+.2f} | {r['verdict']} |")
    if weak:
        lines += ["", "## Work-list (skills showing no measured lift)", ""]
        lines += [f"- `{p}`" for p in weak]
    md = "\n".join(lines) + "\n"
    data = {"threshold": threshold, "skills": rows,
            "summary": {"measured": len(rows), "proven": proven, "weak": len(weak)}}
    return md, data


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Run Resonance golden evals and score skill lift.")
    ap.add_argument("path", nargs="?", default=None, help="skill path (e.g. marketing/seo); omit for all")
    ap.add_argument("--all", action="store_true", help="run every skill's evals")
    ap.add_argument("--check", action="store_true", help="structure only, no model")
    ap.add_argument("--score", action="store_true", help="live run, write the per-skill scorecard")
    ap.add_argument("--changed", nargs="?", const="HEAD~1", default=None,
                    help="only skills changed vs a git ref (default HEAD~1)")
    ap.add_argument("--limit", type=int, default=0, help="cap cases per skill (0 = all)")
    ap.add_argument("--parallel", type=int, default=4, help="concurrent model calls")
    ap.add_argument("--model-cmd", default=os.environ.get("RESONANCE_MODEL_CMD", ""),
                    help="model command reading the prompt on stdin (default: claude -p)")
    ap.add_argument("--threshold", type=float, default=0.8, help="fraction of rubric to pass")
    args = ap.parse_args(argv)

    target = "--all" if (args.all or args.changed or not args.path) else args.path
    cases = find_cases(target, args.changed)
    if args.limit:
        seen: dict[str, int] = defaultdict(int)
        capped = []
        for sk, ev in cases:
            k = skill_rel(sk)
            if seen[k] < args.limit:
                seen[k] += 1
                capped.append((sk, ev))
        cases = capped
    if not cases:
        print(f"no evals found for '{target}'" + (" (changed selection)" if args.changed else ""))
        return 2

    model_cmd = args.model_cmd or ("claude -p" if _has("claude") else "")
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
        if not args.check and not model_cmd:
            print("(no model command found; ran structure check only. Set --model-cmd or "
                  "RESONANCE_MODEL_CMD, e.g. 'claude -p', for a live scored run.)")
        return 1 if bad else 0

    cmd = shlex.split(model_cmd)
    print(f"eval LIVE run via `{model_cmd}`: {len(cases)} cases, parallel={args.parallel}\n")
    with ThreadPoolExecutor(max_workers=max(1, args.parallel)) as pool:
        results = list(pool.map(lambda ce: run_case(cmd, ce[0], ce[1], args.threshold), cases))

    if args.score:
        md, data = write_scorecard(results, args.threshold)
        (REPO / "docs").mkdir(exist_ok=True)
        (REPO / "docs" / "EVAL_SCORECARD.md").write_text(md, encoding="utf-8")
        (FORGE / "eval_results.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        s = data["summary"]
        print(f"scorecard: {s['measured']} skills measured, {s['proven']} proven, {s['weak']} weak")
        print("wrote docs/EVAL_SCORECARD.md and .forge/eval_results.json")
        return 1 if s["weak"] else 0

    failed = 0
    for r in results:
        failed += 0 if r["pass"] else 1
        tag = "PASS" if r["pass"] else "FAIL"
        print(f"  {tag}  {r['path']}/{r['eval']}  with={r['with']}/{r['rubric_n']} without={r['without']}/{r['rubric_n']}")
    print(f"\n{len(results)} cases | {failed} failed")
    return 1 if failed else 0


def _has(exe: str) -> bool:
    from shutil import which
    return which(exe) is not None


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
