#!/usr/bin/env python3
"""
Resonance - Field-inbox age check (warn-only, machine-local).

The field-return channel harvests [lib]-tagged lessons from managed repos into
a private inbox. Two things rot silently: lessons nobody routes, and a harvest
that stopped running. This check makes both loud at push time. It never blocks
(exit 0 always) and is silent on machines without ~/.resonance/machine.json
wiring (cloners never see it).

Inbox location: <privatePack>/inbox/field-lessons.jsonl (unprocessed lessons;
routed ones are removed by the maintainer). Harvest stamp:
<privatePack>/inbox/.last_harvest (ISO date, written by the harvest tool).
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

MAX_LESSON_AGE_DAYS = 30
MAX_HARVEST_AGE_DAYS = 14


def main() -> int:
    gb = Path(os.environ.get("RESONANCE_GLOBAL_BRAIN", str(Path.home() / ".resonance")))
    try:
        cfg = json.loads((gb / "machine.json").read_text(encoding="utf-8-sig"))
    except Exception:
        return 0
    pm, pack = cfg.get("publicMirror", ""), cfg.get("privatePack", "")
    if not pm or not pack:
        return 0
    try:
        if Path(pm).resolve() != Path.cwd().resolve():
            return 0
    except Exception:
        return 0
    inbox = Path(pack) / "inbox"
    today = _dt.date.today()

    jl = inbox / "field-lessons.jsonl"
    if jl.is_file():
        oldest: _dt.date | None = None
        count = 0
        for line in jl.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            count += 1
            try:
                d = _dt.date.fromisoformat(json.loads(line).get("ts", "")[:10])
                oldest = d if oldest is None or d < oldest else oldest
            except Exception:
                pass
        if oldest and (today - oldest).days > MAX_LESSON_AGE_DAYS:
            print(f"Resonance inbox: {count} unrouted field lesson(s); the oldest is from "
                  f"{oldest} (> {MAX_LESSON_AGE_DAYS} days). Route or discard them.")

    stamp = inbox / ".last_harvest"
    if stamp.is_file():
        try:
            last = _dt.date.fromisoformat(stamp.read_text(encoding="utf-8").strip()[:10])
            if (today - last).days > MAX_HARVEST_AGE_DAYS:
                print(f"Resonance inbox: last harvest ran {last} "
                      f"(> {MAX_HARVEST_AGE_DAYS} days ago). The watcher may be dead.")
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
