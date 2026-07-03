#!/usr/bin/env python3
"""
Install the Resonance git hooks (opt-in).

Copies .forge/hooks/pre-commit into .git/hooks/pre-commit and makes it
executable, so the deterministic guard (no dashes, no Soul edits, no secrets,
library validation on skill changes) runs before every commit. Preserves any
other hooks you already have. Uninstall by deleting .git/hooks/pre-commit.

  py .forge/hooks/install.py
"""
from __future__ import annotations

import os
import shutil
import stat
import sys
from pathlib import Path


def main() -> int:
    src = Path(".forge/hooks/pre-commit")
    hooks_dir = Path(".git/hooks")
    if not src.exists():
        print("cannot find .forge/hooks/pre-commit (run from the repo root)")
        return 1
    if not hooks_dir.exists():
        print("no .git/hooks (not a git repo, or run from the repo root)")
        return 1
    dst = hooks_dir / "pre-commit"
    if dst.exists():
        shutil.copy(dst, hooks_dir / "pre-commit.backup")
        print("existing pre-commit backed up to .git/hooks/pre-commit.backup")
    shutil.copy(src, dst)
    dst.chmod(dst.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    print("Resonance git guard enabled. It runs on every commit.")
    print("Disable: delete .git/hooks/pre-commit. Bypass once: git commit --no-verify.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
