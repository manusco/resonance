#!/usr/bin/env python3
"""
Resonance Forge - Field Report to loop closure.

A field report (a skill that misfired in the real world, filed as a GitHub issue
via .github/ISSUE_TEMPLATE/skill-field-report.yml, or a local JSON) is where the
outer loop starts. This turns one into the two artifacts that close it:

  1. a ledger LESSON entry (a les- record) for .resonance/ledger/lessons.md
  2. a STUB EVAL case for the named skill, so the regression can never recur and
     the eval suite compounds (the Ratchet, made mechanical)

The maintainer reviews and commits. Nothing is auto-appended to a tracked file.
Pure stdlib.

Report JSON shape:
  {
    "skill": "resonance-ops-qa",
    "id": "qa-missed-empty-input",
    "summary": "qa skipped the zero-item path",
    "scenario": "the exact prompt/input where the skill misfired",
    "expected": ["what the skill should have done", "..."]
  }

Usage:
  py .forge/field_report.py --file report.json
  echo '{...}' | py .forge/field_report.py --date 2026-07-18
  py .forge/field_report.py --file report.json --eval-out .forge/skills/ops/qa/evals/05_field_x.json
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

def _slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "field-report"


def lesson_block(rep: dict, date: str) -> str:
    rid = _slug(rep.get("id") or rep.get("summary", "field-report"))
    skill = rep.get("skill", "unknown-skill")
    summary = rep.get("summary", "").strip() or "a field report"
    exp = rep.get("expected") or []
    first = exp[0] if exp else "handle this case correctly"
    return (f"## les-{rid}: {summary}\n"
            f"type: lesson\ncreated: {date}\nstatus: active\n\n"
            f"Field report on {skill}: it misfired on the scenario below. It should "
            f"{first}. Hardened by the stub eval case filed with this report.\n")


def eval_stub(rep: dict) -> dict:
    return {
        "skill": rep.get("skill", "unknown-skill"),
        "query": rep.get("scenario", "").strip() or rep.get("summary", ""),
        "expected_behavior": rep.get("expected") or ["(fill in the expected behavior)"],
        "checks": [{"kind": "regex_absent", "value": "[" + chr(0x2014) + chr(0x2013) + "]"}],
        "_source": f"field-report:{rep.get('id', '')}",
        "_status": "needs-eval",
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Turn a field report into a lesson + a stub eval.")
    ap.add_argument("--file", help="report JSON path (default: stdin)")
    ap.add_argument("--date", default=_dt.date.today().isoformat(), help="ISO date for the lesson")
    ap.add_argument("--eval-out", help="write the stub eval JSON to this path")
    a = ap.parse_args(argv)

    raw = Path(a.file).read_text(encoding="utf-8") if a.file else sys.stdin.read()
    rep = json.loads(raw)
    if not rep.get("skill"):
        print("field report needs a 'skill' field", file=sys.stderr)
        return 2

    lesson = lesson_block(rep, a.date)
    stub = eval_stub(rep)
    stub_json = json.dumps(stub, ensure_ascii=True, indent=2) + "\n"

    print("=== ledger lesson (add to .resonance/ledger/lessons.md) ===\n")
    print(lesson)
    print("=== stub eval (review, then add to the skill's evals/) ===\n")
    print(stub_json)
    if a.eval_out:
        Path(a.eval_out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.eval_out).write_text(stub_json, encoding="utf-8")
        print(f"wrote stub eval -> {a.eval_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
