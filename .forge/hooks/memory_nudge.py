#!/usr/bin/env python3
"""
Resonance - Session memory hooks (SessionStart canary + Stop nudge).

Machine-local enforcement of the Ratchet for a repo whose own memory lives
outside the working tree (a private overlay loaded via CLAUDE.local.md).
Silent everywhere else: without ~/.resonance/machine.json naming this repo as
publicMirror and a flagshipMemory path, both modes exit quietly, so cloners
never see any of this. Wire it in .claude/settings.local.json (never committed):

  SessionStart -> py .forge/hooks/memory_nudge.py --session-start
  Stop         -> py .forge/hooks/memory_nudge.py --stop

--session-start: records git HEAD as the session anchor, and alarms into
context when the private memory path is configured but unreachable, or the
git guards are not installed. A loop that can die silently will; this one
screams at the next session start instead.

--stop: when the session made >= 2 commits and the private memory index was
not touched, blocks the stop once with a nudge to record a lesson (or state
that nothing durable was learned). Honors stop_hook_active; once per session.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

TMP = Path(".resonance") / "tmp"


def machine() -> dict:
    gb = Path(os.environ.get("RESONANCE_GLOBAL_BRAIN", str(Path.home() / ".resonance")))
    try:
        return json.loads((gb / "machine.json").read_text(encoding="utf-8-sig"))
    except Exception:
        return {}


def is_flagship(cfg: dict) -> bool:
    pm = cfg.get("publicMirror", "")
    if not pm:
        return False
    try:
        return Path(pm).resolve() == Path.cwd().resolve()
    except Exception:
        return False


def memory_index(cfg: dict) -> Path | None:
    fm = cfg.get("flagshipMemory", "")
    return Path(fm) / "02_memory.local.md" if fm else None


def head_sha() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"],
                           capture_output=True, text=True, timeout=15)
        return r.stdout.strip()
    except Exception:
        return ""


def payload() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def session_start() -> int:
    data = payload()
    sid = str(data.get("session_id", "unknown"))[:64]
    cfg = machine()
    TMP.mkdir(parents=True, exist_ok=True)
    cutoff = time.time() - 7 * 86400
    for pattern in ("session_*", "nudged_*"):
        for f in TMP.glob(pattern):
            try:
                if f.stat().st_mtime < cutoff:
                    f.unlink()
            except Exception:
                pass
    sha = head_sha()
    if sha:
        (TMP / f"session_{sid}.anchor").write_text(sha, encoding="utf-8")
    if not is_flagship(cfg):
        return 0
    alarms: list[str] = []
    idx = memory_index(cfg)
    if idx is not None and not idx.is_file():
        alarms.append(
            f"FLAGSHIP MEMORY UNREACHABLE: machine.json points flagshipMemory at "
            f"'{cfg.get('flagshipMemory')}' but {idx.name} is not there. The private "
            f"memory is NOT loading this session. Fix the path or run the bootstrap script.")
    for hook in ("pre-commit", "pre-push"):
        installed = Path(".git/hooks") / hook
        source = Path(".forge/hooks") / hook
        if not installed.is_file():
            alarms.append(
                f"GIT GUARDS NOT INSTALLED: .git/hooks/{hook} is missing. "
                f"Run `npm run hooks:install` (dash guard, version guard, ship-gate).")
        elif source.is_file():
            a = installed.read_bytes().replace(b"\r\n", b"\n")
            b = source.read_bytes().replace(b"\r\n", b"\n")
            if a != b:
                alarms.append(
                    f"GIT GUARD STALE: .git/hooks/{hook} differs from .forge/hooks/{hook}. "
                    f"Re-run `npm run hooks:install` so the installed guard matches the source.")
    if alarms:
        print("Resonance canary:")
        for a in alarms:
            print(f"  ! {a}")
    return 0


def stop() -> int:
    data = payload()
    if data.get("stop_hook_active"):
        return 0
    sid = str(data.get("session_id", "unknown"))[:64]
    cfg = machine()
    if not is_flagship(cfg):
        return 0
    idx = memory_index(cfg)
    if idx is None or not idx.is_file():
        return 0  # unreachable memory already alarmed at session start
    anchor = TMP / f"session_{sid}.anchor"
    marker = TMP / f"nudged_{sid}"
    if not anchor.is_file() or marker.exists():
        return 0
    old = anchor.read_text(encoding="utf-8").strip()
    try:
        r = subprocess.run(["git", "rev-list", "--count", f"{old}..HEAD"],
                           capture_output=True, text=True, timeout=15)
        commits = int(r.stdout.strip() or "0")
    except Exception:
        return 0
    if commits < 2:
        return 0
    if idx.stat().st_mtime > anchor.stat().st_mtime:
        return 0  # memory touched this session; the Ratchet turned
    marker.write_text("1", encoding="utf-8")
    print(json.dumps({
        "decision": "block",
        "reason": (f"{commits} commits this session and zero lessons recorded. Add one line to "
                   f"the private memory index ({idx}) or state explicitly that nothing durable "
                   f"was learned, then stop again. Nudges once per session.")
    }))
    return 0


def main(argv: list[str]) -> int:
    if "--session-start" in argv:
        return session_start()
    if "--stop" in argv:
        return stop()
    print("usage: memory_nudge.py --session-start | --stop")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
