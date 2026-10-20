#!/usr/bin/env python3
"""
Resonance Forge - Field Report to loop closure.

A field report (a skill that misfired in the real world, filed as a sanitized
GitHub issue via .github/ISSUE_TEMPLATE/skill-field-report.yml, or local JSON)
starts the manual correction loop. This prints two proposals:

  1. a lesson proposal that a human may turn into a ledger entry after review
  2. a STUB EVAL case for the named skill, marked needs-eval

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

Optional metadata: run_id + artifact_version, sensitivity (public-sanitized or
restricted-do-not-submit), owner_role, and the outcome + due_date pair (which
also requires an owner role). Restricted reports are refused. Metadata is
submitter-provided, not host-verified.

Usage:
  py .forge/field_report.py --file report.json
  echo '{...}' | py .forge/field_report.py --date 2026-07-18
  py .forge/field_report.py --file report.json --eval-out /path/to/review/05_field_x.json

The optional output path must remain outside active skill eval directories.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path


_TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:+-]{0,127}$")
_ROLE = re.compile(r"^[a-z][a-z0-9-]{1,63}$")
_LINE_BREAKS = "\r\n\v\f\x1c\x1d\x1e\x85\u2028\u2029"


def _slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "field-report"


def _one_line(s: str) -> str:
    return " ".join(s.split())


def lesson_block(rep: dict, date: str) -> str:
    rid = _slug(rep.get("id") or rep.get("summary", "field-report"))
    skill = rep.get("skill", "unknown-skill")
    summary = rep.get("summary", "").strip() or "a field report"
    exp = rep.get("expected") or []
    first = exp[0] if exp else "handle this case correctly"
    report_metadata = _proposal_metadata(rep)
    provenance = ""
    if report_metadata:
        provenance = "\nReport metadata (submitter-provided, unverified): " + "; ".join(
            f"{key}={_one_line(str(value))}" for key, value in report_metadata.items()
        ) + ".\n"
    return (f"## les-{rid}: {summary}\n"
            f"Proposed {date} lesson from field report on {skill}: it misfired on the scenario below. It should "
            f"{_one_line(first)}. A candidate regression eval is proposed for maintainer review."
            f"{provenance}\n")


def _proposal_metadata(rep: dict) -> dict:
    fields = {
        "run_id": "run_id",
        "artifact_version": "artifact_version",
        "sensitivity": "sensitivity",
        "owner_role": "owner_role",
        "outcome": "outcome",
        "outcome_due": "due_date",
    }
    return {label: rep[key] for label, key in fields.items() if rep.get(key)}


def eval_stub(rep: dict) -> dict:
    stub = {
        "skill": rep.get("skill", "unknown-skill"),
        "query": rep.get("scenario", "").strip() or rep.get("summary", ""),
        "expected_behavior": rep.get("expected") or ["(fill in the expected behavior)"],
        "checks": [{"kind": "regex_absent", "value": "[" + chr(0x2014) + chr(0x2013) + "]"}],
        "_source": f"field-report:{rep.get('id', '')}",
        "_status": "needs-eval",
    }
    stub.update({f"_{key}": value for key, value in _proposal_metadata(rep).items()})
    return stub


def validate_report(rep: object) -> str | None:
    """Validate optional attribution and follow-up metadata before rendering proposals."""
    if not isinstance(rep, dict):
        return "field report must be a JSON object"
    if not isinstance(rep.get("skill"), str) or not re.fullmatch(
        r"(?:resonance-[a-z0-9]+(?:-[a-z0-9]+)*|[a-z0-9-]+(?:/[a-z0-9-]+)+|/[a-z0-9-]+)",
        rep["skill"],
    ):
        return "field report needs a valid 'skill' identifier"
    if rep.get("sensitivity") not in (
        None, "public-sanitized", "restricted", "restricted-do-not-submit"
    ):
        return "sensitivity must be 'public-sanitized' or 'restricted-do-not-submit'"
    if rep.get("sensitivity") in ("restricted", "restricted-do-not-submit"):
        return "restricted reports cannot be converted; redact a derivative and mark it 'public-sanitized'"

    for key, limit in (("id", 128), ("summary", 300), ("scenario", 4000)):
        value = rep.get(key)
        if value is not None and (not isinstance(value, str) or len(value) > limit):
            return f"'{key}' must be text no longer than {limit} characters"
        if key == "summary" and value is not None and any(ch in value for ch in _LINE_BREAKS):
            return "'summary' must be a single line"
    expected = rep.get("expected", [])
    if not isinstance(expected, list) or len(expected) > 10 or any(
        not isinstance(item, str) or not item.strip() or len(item) > 1000 for item in expected
    ):
        return "'expected' must be a list of up to 10 non-empty text items (1000 characters each)"

    run_id, version = rep.get("run_id"), rep.get("artifact_version")
    if (run_id is None) != (version is None):
        return "'run_id' and 'artifact_version' must be supplied together"
    if run_id is not None and (
        not isinstance(run_id, str) or not _TOKEN.fullmatch(run_id)
    ):
        return "'run_id' must be a short opaque identifier without URLs or paths"
    if version is not None and (
        not isinstance(version, str) or not _TOKEN.fullmatch(version)
    ):
        return "'artifact_version' must be a short version or revision token"

    owner, outcome, due = (rep.get("owner_role"), rep.get("outcome"), rep.get("due_date"))
    if owner is not None and (not isinstance(owner, str) or not _ROLE.fullmatch(owner)):
        return "'owner_role' must be a lowercase role slug, not a person's name"
    if (outcome is None) != (due is None):
        return "'outcome' and 'due_date' must be supplied together"
    if outcome is not None:
        if owner is None:
            return "'owner_role' is required when a delayed outcome is supplied"
        if not isinstance(outcome, str) or not outcome.strip() or len(outcome) > 300:
            return "'outcome' must be non-empty text of at most 300 characters"
        try:
            parsed = _dt.date.fromisoformat(due)
        except (TypeError, ValueError):
            return "'due_date' must be a real date in YYYY-MM-DD format"
        if parsed.isoformat() != due:
            return "'due_date' must use YYYY-MM-DD format"
    return None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Turn a field report into a lesson + a stub eval.")
    ap.add_argument("--file", help="report JSON path (default: stdin)")
    ap.add_argument("--date", default=_dt.date.today().isoformat(), help="ISO date for the lesson")
    ap.add_argument("--eval-out", help="write a draft stub outside active skill eval directories")
    a = ap.parse_args(argv)

    raw = Path(a.file).read_text(encoding="utf-8") if a.file else sys.stdin.read()
    rep = json.loads(raw)
    error = validate_report(rep)
    if error:
        print(error, file=sys.stderr)
        return 2
    try:
        parsed_date = _dt.date.fromisoformat(a.date)
    except ValueError:
        print("--date must be a real date in YYYY-MM-DD format", file=sys.stderr)
        return 2
    if parsed_date.isoformat() != a.date:
        print("--date must use YYYY-MM-DD format", file=sys.stderr)
        return 2

    if a.eval_out:
        target = Path(a.eval_out).resolve()
        repo = Path(__file__).resolve().parents[1]
        for root in (repo / ".forge" / "skills", repo / ".agents" / "skills"):
            try:
                relative = target.relative_to(root.resolve())
            except ValueError:
                continue
            if "evals" in relative.parts:
                print("eval proposals must stay outside active skill eval directories", file=sys.stderr)
                return 2

    lesson = lesson_block(rep, a.date)
    stub = eval_stub(rep)
    stub_json = json.dumps(stub, ensure_ascii=True, indent=2) + "\n"

    print("=== lesson proposal (not a ledger entry; review before adding) ===\n")
    print(lesson)
    print("=== stub eval (review, then add to the skill's evals/) ===\n")
    print(stub_json)
    if a.eval_out:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(stub_json, encoding="utf-8")
        print(f"wrote stub eval -> {a.eval_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
