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
import sys
from pathlib import Path

FORGE = Path(__file__).resolve().parent
if str(FORGE) not in sys.path:
    sys.path.insert(0, str(FORGE))
from kernel.ledger import active_entries  # noqa: E402

LEDGER = Path(".resonance/ledger")


def due_entries(today: _dt.date) -> list[tuple[str, str, str]]:
    due: list[tuple[str, str, str]] = []
    for entry in active_entries(LEDGER):
        if not entry["id"].startswith(("met-", "exp-")):
            continue
        f = entry["fields"]
        d = f.get("due")
        if f.get("status") == "active" and d:
            try:
                if _dt.date.fromisoformat(d) <= today:
                    due.append((entry["id"], entry["title"], d))
            except ValueError:
                print(f"warning: {entry['id']} has a malformed due date '{d}'", file=sys.stderr)
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
