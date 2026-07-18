#!/usr/bin/env python3
"""
Resonance Forge - Due-Outcome pull.

DONE_PENDING_OUTCOME work records a metric or experiment in the ledger with a
`due:` date, the day its real result should be checked in. This scans for the
entries that have come due and surfaces them. It is PULL, not push: nothing fires
on a clock. A session (or a SessionStart hook) runs it, and it is silent when
nothing is due, so it never nags. Pure stdlib.

Usage:
  py .forge/measurement_due.py             # what outcomes are due today
  py .forge/measurement_due.py --date 2026-08-01
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

LEDGER = Path(".resonance/ledger")
ENTRY_RE = re.compile(r"^##\s+((met|exp)-[a-z0-9-]+):\s*(.+?)\s*$")
FIELD_RE = re.compile(r"^([a-z_]+):\s*(.*)$")


def _parse(path: Path) -> list[tuple[str, str, dict]]:
    out: list[tuple[str, str, dict]] = []
    if not path.is_file():
        return out
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    i = 0
    while i < len(lines):
        m = ENTRY_RE.match(lines[i])
        if not m:
            i += 1
            continue
        eid, title = m.group(1), m.group(3)
        fields, j = {}, i + 1
        while j < len(lines) and lines[j].strip() != "":
            fm = FIELD_RE.match(lines[j])
            if fm:
                fields[fm.group(1)] = fm.group(2).strip()
            j += 1
        out.append((eid, title, fields))
        i = j
    return out


def due_entries(today: _dt.date) -> list[tuple[str, str, str]]:
    due: list[tuple[str, str, str]] = []
    for name in ("metrics", "experiments"):
        for eid, title, f in _parse(LEDGER / f"{name}.md"):
            d = f.get("due")
            if f.get("status") == "active" and d:
                try:
                    if _dt.date.fromisoformat(d) <= today:
                        due.append((eid, title, d))
                except ValueError:
                    print(f"warning: {eid} has a malformed due date '{d}'", file=sys.stderr)
    return due


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Surface ledger outcomes that are due to check in.")
    ap.add_argument("--date", default=_dt.date.today().isoformat())
    a = ap.parse_args(argv)
    if not LEDGER.is_dir():
        return 0
    try:
        today = _dt.date.fromisoformat(a.date)
    except ValueError:
        print("date must be ISO (YYYY-MM-DD)", file=sys.stderr)
        return 2
    due = due_entries(today)
    if not due:
        return 0  # silent: nothing due, so no nag
    print("Outcomes due to check in (DONE_PENDING_OUTCOME):")
    for eid, title, d in due:
        print(f"  {eid}  {title}  (due {d})")
    print("Verify the real result, then update the ledger entry (set the value or result "
          "and status: closed). This is how the outer loop closes.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
