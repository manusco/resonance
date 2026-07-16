#!/usr/bin/env python3
"""
Resonance - /improve helper: the self-improving loop's grounded measurement.

The eval scorecard (`run_evals.py --score`) names the skills with no measured
lift. /improve works that list: sharpen the skill body or its rubric, rebuild,
then RE-MEASURE and keep the change only on a calibrated verdict. A change kept
without an honest measurement is a guess wearing a number.

Subcommands:
  worklist              skills with no measured lift, weakest first
  calibrate             the A/A noise floor: remeasure unchanged skills against
                        themselves, pool the deltas, store floors in the baseline
  remeasure <path>      paired A/B: the skill body at --baseline-ref (default
                        HEAD) versus the working tree, same cases, same judge,
                        same session, k reps per arm

The decision rule (pooled, calibrated; replaces the old fixed constant):
  KEEP only if mean delta >= max(0.10, skill_floor)
       AND no case regressed by more than case_floor
  where skill_floor = mean + 2*std of the pooled A/A skill-level |deltas|
        case_floor  = mean + 2*std of the pooled A/A case-level |deltas|
  Floors are POOLED across the calibration set and shared by all skills
  (per-skill floors from tiny samples are a lottery; explicitly out of scope).

Hard honesty rules:
  - UNCALIBRATED runs print numbers but never a keep verdict. Run calibrate once.
  - The judge is never the answerer (RESONANCE_MODEL_CMD vs RESONANCE_JUDGE_CMD).
  - A changed evals directory (rubric edit) resets the baseline: remeasure
    reports NEW BASELINE and refuses a verdict. "Never weaken a rubric to pass
    it" is a mechanism here, not prose.

  python .forge/improve.py worklist
  python .forge/improve.py calibrate
  python .forge/improve.py remeasure engineering/build --baseline-ref HEAD
"""
from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import math
import os
import shlex
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FORGE = Path(__file__).resolve().parent
REPO = FORGE.parent
RESULTS = FORGE / "eval_results.json"
HARD_MIN = 0.10  # the floor never drops below this, calibrated or not

_spec = importlib.util.spec_from_file_location("run_evals", FORGE / "run_evals.py")
run_evals = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run_evals)

CALIBRATION_SKILLS = ["strategy/grill", "marketing/copywriter", "engineering/backend"]


def load_results() -> dict:
    if RESULTS.exists():
        try:
            return json.loads(RESULTS.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"skills": [], "summary": {}}


def worklist() -> int:
    data = load_results()
    rows = [r for r in data.get("skills", []) if r.get("verdict") in ("weak", "flat")]
    rows.sort(key=lambda r: r.get("lift", 0))
    if not data.get("skills"):
        print("no scorecard yet. Run `python .forge/run_evals.py --all --score` first "
              "(results are machine-local; see docs/EVALS.md).")
        return 2
    if not rows:
        print("no weak or flat skills: every measured skill shows real lift. Nothing to improve.")
        return 0
    print(f"improvement work-list ({len(rows)} skills with no measured lift), weakest first:\n")
    for r in rows:
        print(f"  {r['verdict']:5}  lift={r.get('lift', 0):+.2f}  {r['path']}  "
              f"(with={r.get('with')}, without={r.get('without')})")
    print("\nFor each, decide whether the BODY is weak (the skill does not add enough) or the "
          "RUBRIC is coarse (the eval cannot see the skill's value), fix it in .forge SOURCE, "
          "rebuild, then `improve.py remeasure <path>` and keep the change only on a KEEP verdict.")
    return 0


def _cmds(model_cmd: str, judge_cmd: str) -> tuple[list[str], list[str]] | None:
    m = (model_cmd or os.environ.get("RESONANCE_MODEL_CMD", "")).strip()
    j = (judge_cmd or os.environ.get("RESONANCE_JUDGE_CMD", "")).strip()
    if not m:
        print("no answerer model; set RESONANCE_MODEL_CMD (e.g. the model_cli adapter).")
        return None
    if not j:
        print("no judge model; set RESONANCE_JUDGE_CMD to a DIFFERENT model than the answerer.")
        return None
    if m == j:
        print("refusing: judge command equals the answerer. Self-grading flatters.")
        return None
    return shlex.split(m), shlex.split(j)


def _strip_frontmatter(text: str) -> str:
    end = text.find("\n---", 3)
    return text[end + 4:].strip() if text.startswith("---") and end != -1 else text


def body_at_ref(path: str, ref: str) -> str:
    r = subprocess.run(["git", "show", f"{ref}:.agents/skills/{path}/SKILL.md"],
                       cwd=str(REPO), capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        return ""
    return _strip_frontmatter(r.stdout)


def _judged_frac(cmd, jcmd, case: dict, body: str, reps: int) -> list[float]:
    """k generations of one arm (a given body), each judged; per-rep fractions."""
    rub = case["expected_behavior"]
    checks = case.get("checks") or []
    n = len(rub) + len(checks)
    out = []
    for _ in range(max(1, reps)):
        o = run_evals.run_model(cmd, run_evals.build_prompt(case, body))
        s = sum(run_evals.judge(jcmd, case["query"], o, rub)) + run_evals.det_checks(o, checks)
        out.append(s / n)
    return out


def _paired(path: str, cmd, jcmd, old_body: str, new_body: str, reps: int) -> dict | None:
    """Paired comparison per case: mean(new) - mean(old). The without-arm cancels
    in the pairing, so it is not run (half the cost, none of the drift)."""
    cases = run_evals.find_cases(path, None)
    if not cases:
        print(f"no evals found for {path}")
        return None
    per_case = []
    for sk, ev in cases:
        d = json.loads(ev.read_text(encoding="utf-8"))
        old_f = _judged_frac(cmd, jcmd, d, old_body, reps)
        new_f = _judged_frac(cmd, jcmd, d, new_body, reps)
        per_case.append({"eval": ev.name,
                         "old": sum(old_f) / len(old_f),
                         "new": sum(new_f) / len(new_f)})
    delta = sum(c["new"] - c["old"] for c in per_case) / len(per_case)
    return {"path": path, "cases": per_case, "delta": delta}


def _floors(base: dict) -> dict | None:
    cal = base.get("calibration")
    if not cal or "skill_floor" not in cal:
        return None
    return cal


def _mean_std(vals: list[float]) -> tuple[float, float]:
    m = sum(vals) / len(vals)
    var = sum((v - m) ** 2 for v in vals) / len(vals)
    return m, math.sqrt(var)


def calibrate(model_cmd: str, judge_cmd: str, runs: int, reps: int) -> int:
    cmds = _cmds(model_cmd, judge_cmd)
    if not cmds:
        return 2
    cmd, jcmd = cmds
    out_dir = run_evals.private_eval_dir()
    if not out_dir:
        print("no private results directory configured (machine.json); calibration has "
              "nowhere durable to live. Configure it first.")
        return 2
    skills = [s for s in CALIBRATION_SKILLS if run_evals.find_cases(s, None)]
    if len(skills) < 2:
        print("calibration skills not found; adjust CALIBRATION_SKILLS.")
        return 2
    print(f"A/A calibration: {runs} runs across {skills}, reps={reps}, judge=`{' '.join(jcmd)}`")
    skill_deltas: list[float] = []
    case_deltas: list[float] = []
    for i in range(runs):
        path = skills[i % len(skills)]
        body = run_evals.skill_body(run_evals.SKILLS / path / "SKILL.md")
        r = _paired(path, cmd, jcmd, body, body, reps)  # A/A: same body twice
        if not r:
            continue
        skill_deltas.append(abs(r["delta"]))
        case_deltas.extend(abs(c["new"] - c["old"]) for c in r["cases"])
        print(f"  run {i + 1}/{runs} [{path}] |delta|={abs(r['delta']):.3f}")
    if len(skill_deltas) < 3:
        print("too few successful runs; calibration aborted.")
        return 1
    sm, ss = _mean_std(skill_deltas)
    cm, cs = _mean_std(case_deltas)
    cal = {"skill_floor": round(sm + 2 * ss, 3), "case_floor": round(cm + 2 * cs, 3),
           "n_runs": len(skill_deltas), "n_case_samples": len(case_deltas),
           "reps": reps, "judge": " ".join(jcmd), "model": " ".join(cmd),
           "date": _dt.date.today().isoformat(),
           "note": "floors POOLED across the calibration set, shared by all skills; "
                   "assumes roughly homogeneous noise across skills"}
    base = run_evals.load_baseline(out_dir)
    base["calibration"] = cal
    run_evals.save_baseline(out_dir, base)
    effective = max(HARD_MIN, cal["skill_floor"])
    print(f"\ncalibrated: skill_floor={cal['skill_floor']:.3f}, case_floor={cal['case_floor']:.3f} "
          f"(pooled, n={cal['n_runs']}/{cal['n_case_samples']})")
    print(f"effective keep threshold: delta >= {effective:.3f} "
          f"(the minimum detectable effect of this gate)")
    if cal["skill_floor"] > 0.25:
        print("floor exceeds 0.25: raise reps to 5 before trusting keep verdicts.")
    return 0


def remeasure(path: str, model_cmd: str, judge_cmd: str, baseline_ref: str, reps: int) -> int:
    cmds = _cmds(model_cmd, judge_cmd)
    if not cmds:
        return 2
    cmd, jcmd = cmds
    out_dir = run_evals.private_eval_dir()
    base = run_evals.load_baseline(out_dir) if out_dir else {}
    cal = _floors(base)

    # rubric-change gate: a changed evals dir resets the baseline, no verdict
    cur_hash = run_evals.evals_dir_hash(path)
    entry = base.get("skills", {}).get(path)
    if entry and entry.get("evals_hash") and entry["evals_hash"] != cur_hash:
        print(f"NEW BASELINE: the evals for {path} changed since the recorded baseline "
              f"(rubric edits never count as lift). No keep verdict. "
              f"Re-run `run_evals.py {path} --score` to re-baseline, then remeasure.")
        if out_dir:
            entry["evals_hash"] = cur_hash
            entry["lift"] = None
            entry["note"] = "rubric changed; re-baseline required"
            entry["date"] = _dt.date.today().isoformat()
            run_evals.save_baseline(out_dir, base)
        return 3

    old_body = body_at_ref(path, baseline_ref)
    if not old_body:
        print(f"cannot read the skill body at {baseline_ref}:.agents/skills/{path}/SKILL.md")
        return 2
    new_body = run_evals.skill_body(run_evals.SKILLS / path / "SKILL.md")
    if old_body.strip() == new_body.strip():
        print(f"{path}: the body at {baseline_ref} and the working tree are identical; "
              f"nothing to compare (for noise floors, use `calibrate`).")
        return 2

    r = _paired(path, cmd, jcmd, old_body, new_body, reps)
    if not r:
        return 2
    print(f"{path}: paired delta {r['delta']:+.3f} over {len(r['cases'])} case(s), reps={reps}")
    for c in r["cases"]:
        print(f"  {c['eval']}: old={c['old']:.2f} new={c['new']:.2f} ({c['new'] - c['old']:+.2f})")

    if not cal:
        print("\nUNCALIBRATED: numbers only, no keep verdict. Run `improve.py calibrate` once, "
              "then remeasure again.")
        return 2
    skill_floor = max(HARD_MIN, cal["skill_floor"])
    case_floor = cal["case_floor"]
    regressed = [c for c in r["cases"] if (c["new"] - c["old"]) < -case_floor]
    if r["delta"] >= skill_floor and not regressed:
        print(f"\nKEEP: delta {r['delta']:+.3f} >= {skill_floor:.3f} and no case regressed "
              f"beyond the case floor ({case_floor:.3f}). The monthly scored run refreshes "
              f"the absolute baseline.")
        return 0
    why = []
    if r["delta"] < skill_floor:
        why.append(f"delta {r['delta']:+.3f} < floor {skill_floor:.3f}")
    if regressed:
        why.append(f"{len(regressed)} case(s) regressed beyond {case_floor:.3f}: "
                   + ", ".join(c["eval"] for c in regressed))
    print(f"\nREVERT: {'; '.join(why)}. Do not keep the change.")
    return 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Resonance /improve helper (grounded measurement).")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("worklist", help="skills with no measured lift, weakest first")
    ca = sub.add_parser("calibrate", help="A/A pooled noise floors (writes to the private baseline)")
    ca.add_argument("--model-cmd", default="")
    ca.add_argument("--judge-cmd", default="")
    ca.add_argument("--runs", type=int, default=10)
    ca.add_argument("--reps", type=int, default=3)
    rm = sub.add_parser("remeasure", help="paired A/B vs --baseline-ref; calibrated keep/revert")
    rm.add_argument("path", help="skill path, e.g. engineering/build")
    rm.add_argument("--model-cmd", default="")
    rm.add_argument("--judge-cmd", default="")
    rm.add_argument("--baseline-ref", default="HEAD")
    rm.add_argument("--reps", type=int, default=3)
    a = ap.parse_args(argv)
    if a.cmd == "worklist":
        return worklist()
    if a.cmd == "calibrate":
        return calibrate(a.model_cmd, a.judge_cmd, a.runs, a.reps)
    if a.cmd == "remeasure":
        return remeasure(a.path, a.model_cmd, a.judge_cmd, a.baseline_ref, a.reps)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
