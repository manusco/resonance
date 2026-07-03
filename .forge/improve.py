#!/usr/bin/env python3
"""
Resonance - /improve helper: the self-improving loop's grounded measurement.

The eval scorecard (`run_evals.py --score`) names the skills that show no measured
lift (verdict `weak` or `flat`). /improve works that list: for each, sharpen the
skill body or its eval rubric, rebuild, then RE-MEASURE and keep the change only if
the lift actually rose. A change kept without re-measuring is just a guess, which is
the exact failure the whole framework is built to avoid.

This tool provides the two grounded pieces the loop needs:
  worklist              the skills with no measured lift, weakest first
  remeasure <path>      re-run one skill's evals and compare to the recorded lift

The model is pluggable (same contract as run_evals): --model-cmd or RESONANCE_MODEL_CMD.

  python .forge/improve.py worklist
  python .forge/improve.py remeasure engineering/build --model-cmd "claude -p"
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shlex
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FORGE = Path(__file__).resolve().parent
RESULTS = FORGE / "eval_results.json"

_spec = importlib.util.spec_from_file_location("run_evals", FORGE / "run_evals.py")
run_evals = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run_evals)


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
        print("no scorecard yet. Run `python .forge/run_evals.py --all --score` first (needs a model).")
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
          "rebuild, then `improve.py remeasure <path>` and keep the change only if lift rose.")
    return 0


def remeasure(path: str, model_cmd: str, limit: int) -> int:
    cmd = shlex.split(model_cmd) if model_cmd else (["claude", "-p"] if run_evals._has("claude") else [])
    if not cmd:
        print("no model command; set --model-cmd or RESONANCE_MODEL_CMD (e.g. 'claude -p') to re-measure live.")
        return 2
    cases = run_evals.find_cases(path, None)
    if limit:
        cases = cases[:limit]
    if not cases:
        print(f"no evals found for {path}")
        return 2
    results = [run_evals.run_case(cmd, sk, ev, 0.8) for sk, ev in cases]
    n = len(results)
    wavg = sum(r["with_frac"] for r in results) / n
    woavg = sum(r["without_frac"] for r in results) / n
    lift = wavg - woavg
    print(f"{path}: re-measured with={wavg:.2f} without={woavg:.2f} lift={lift:+.2f} over {n} case(s)")
    old = next((r for r in load_results().get("skills", []) if r["path"] == path), None)
    if old and old.get("lift") is not None:
        delta = lift - old["lift"]
        verdict = "IMPROVED" if delta > 0.02 else ("REGRESSED" if delta < -0.02 else "no change")
        print(f"  vs recorded lift {old['lift']:+.2f}: {verdict} ({delta:+.2f}). "
              f"Keep the change only if IMPROVED; otherwise revert.")
        return 0 if delta > 0.02 else 1
    print("  no prior recorded lift for this skill; treat this as the new baseline.")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Resonance /improve helper (grounded measurement).")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("worklist", help="skills with no measured lift, weakest first")
    rm = sub.add_parser("remeasure", help="re-run one skill's evals vs its recorded lift")
    rm.add_argument("path", help="skill path, e.g. engineering/build")
    rm.add_argument("--model-cmd", default=os.environ.get("RESONANCE_MODEL_CMD", ""))
    rm.add_argument("--limit", type=int, default=0, help="cap cases (cheap)")
    a = ap.parse_args(argv)
    if a.cmd == "worklist":
        return worklist()
    if a.cmd == "remeasure":
        return remeasure(a.path, a.model_cmd, a.limit)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
