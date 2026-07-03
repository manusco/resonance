#!/usr/bin/env python3
"""
Install the Resonance git hooks (opt-in).

Copies the deterministic guards into .git/hooks so they run automatically:
  - pre-commit: blocks dashes, Soul edits, and secrets, and runs the library
    validator when skills change,
  - pre-push:   the ship-gate. Blocks pushing a release tag or main when the
    validators, the eval check, or doc-drift are not green.
Existing hooks are backed up, not clobbered. Uninstall by deleting the files in
.git/hooks.

  py .forge/hooks/install.py            # install the git hooks
  py .forge/hooks/install.py --claude   # also enable the Claude Code edit-time guard
"""
from __future__ import annotations

import json
import shutil
import stat
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HOOKS = ["pre-commit", "pre-push"]
HOOK_CMD = "py .forge/hooks/guard.py --hook"


def install_git_hooks() -> int:
    src_dir = Path(".forge/hooks")
    hooks_dir = Path(".git/hooks")
    if not hooks_dir.exists():
        print("no .git/hooks (not a git repo, or run from the repo root)")
        return 1
    for name in HOOKS:
        src = src_dir / name
        if not src.exists():
            print(f"cannot find {src} (run from the repo root)")
            return 1
        dst = hooks_dir / name
        if dst.exists():
            shutil.copy(dst, hooks_dir / f"{name}.backup")
            print(f"existing {name} backed up to .git/hooks/{name}.backup")
        shutil.copy(src, dst)
        dst.chmod(dst.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        print(f"installed .git/hooks/{name}")
    print("Resonance git guards enabled (pre-commit + pre-push ship-gate).")
    print("Disable: delete the files in .git/hooks. Bypass once: --no-verify.")
    return 0


def enable_claude_hook() -> int:
    snippet = Path(".claude/hooks/settings.snippet.json")
    if not snippet.exists():
        print("cannot find .claude/hooks/settings.snippet.json")
        return 1
    post_hooks = json.loads(snippet.read_text(encoding="utf-8"))["hooks"]["PostToolUse"]
    settings_path = Path(".claude/settings.local.json")
    data: dict = {}
    if settings_path.exists():
        try:
            data = json.loads(settings_path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    post = data.setdefault("hooks", {}).setdefault("PostToolUse", [])
    already = any(
        any(h.get("command") == HOOK_CMD for h in entry.get("hooks", []))
        for entry in post if isinstance(entry, dict)
    )
    if already:
        print("Claude Code guard hook already enabled in .claude/settings.local.json")
        return 0
    post.extend(post_hooks)
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Claude Code guard hook enabled in .claude/settings.local.json (runs after Write/Edit).")
    return 0


def main(argv: list[str]) -> int:
    rc = install_git_hooks()
    if rc != 0:
        return rc
    if "--claude" in argv:
        return enable_claude_hook()
    print("Tip: `py .forge/hooks/install.py --claude` also adds the Claude Code edit-time guard.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
