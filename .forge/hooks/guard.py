#!/usr/bin/env python3
"""
Resonance - Deterministic Guard (the hooks layer).

Layer 3 enforcement of the rules that should never depend on the model
remembering them. Runs as a git pre-commit hook (universal, cross-tool) or a
Claude Code hook. Opt in with `py .forge/hooks/install.py`.

Blocks a commit when a staged text file:
  - contains an em or en dash (the house rule bans them everywhere),
  - edits .resonance/00_soul.md (the Soul is immutable law; override with
    RESONANCE_ALLOW_SOUL=1 when the change is deliberate),
  - contains an obvious secret (API key, private key, token).

Pure stdlib. Exit 1 blocks the commit; exit 0 lets it through.

Usage:
  py .forge/hooks/guard.py --staged        # check staged files (pre-commit)
  py .forge/hooks/guard.py path/to/file.md # check specific files
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DASH = re.compile(r"[—–]")  # em, en
TEXT_EXT = {".md", ".txt", ".json", ".py", ".ts", ".tsx", ".js", ".jsx", ".sh",
            ".ps1", ".yml", ".yaml", ".html", ".css", ".mjs", ".cjs", ".go", ".rs"}
SECRETS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}"), "OpenAI-style key"),
    (re.compile(r"\bghp_[A-Za-z0-9]{36}\b"), "GitHub token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"(?i)\b(api[_-]?key|secret|token)\b\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]"), "hardcoded secret"),
]


def staged_files() -> list[str]:
    try:
        r = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                           capture_output=True, text=True, timeout=20)
        return [f for f in r.stdout.splitlines() if f.strip()]
    except Exception:
        return []


def check(path: str, problems: list[str]) -> None:
    p = Path(path)
    if not p.is_file():
        return
    norm = path.replace("\\", "/")
    if norm.endswith(".resonance/00_soul.md") and os.environ.get("RESONANCE_ALLOW_SOUL") != "1":
        problems.append(f"{norm}: edits the Soul (.resonance/00_soul.md). "
                        f"Set RESONANCE_ALLOW_SOUL=1 if this is deliberate.")
        return
    if p.suffix.lower() not in TEXT_EXT:
        return
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return
    for i, line in enumerate(text.splitlines(), 1):
        if "banned vocabulary" in line.lower():
            continue
        if DASH.search(line):
            problems.append(f"{norm}:{i}: em/en dash (use a hyphen, comma, or period).")
        for rx, label in SECRETS:
            if rx.search(line):
                problems.append(f"{norm}:{i}: possible {label}. Do not commit secrets.")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Resonance deterministic commit guard.")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--staged", action="store_true", help="check staged files")
    a = ap.parse_args(argv)

    files = a.files or (staged_files() if a.staged else [])
    if not files:
        return 0
    problems: list[str] = []
    for f in files:
        check(f, problems)
    if problems:
        print("Resonance guard blocked the commit:\n")
        for p in problems:
            print(f"  x {p}")
        print(f"\n{len(problems)} violation(s). Fix them, or bypass once with `git commit --no-verify`.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
