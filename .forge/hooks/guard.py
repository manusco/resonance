#!/usr/bin/env python3
"""
Resonance - Deterministic Guard (the hooks layer).

Layer 3 enforcement of the rules that should never depend on the model
remembering them. Runs as a git pre-commit hook (universal, cross-tool) or a
Claude Code hook. Opt in with `py .forge/hooks/install.py`.

Always blocks a commit when a staged text file:
  - contains an em or en dash (the house rule bans them everywhere),
  - edits .resonance/00_soul.md (the Soul is immutable law; override with
    RESONANCE_ALLOW_SOUL=1 when the change is deliberate),
  - contains an obvious secret (API key, private key, token).

Optionally (copy mode) also flags banned slop vocabulary in prose. This is off
by default because "robust" or "leverage" are legitimate in technical docs; it
is meant for generated copy. Turn it on per file with `--copy`, or for the whole
pre-commit with RESONANCE_STRICT_VOCAB=1. Framework internals (.forge, docs, and
the files that teach the rules) are exempt so the scan never fights itself.

Pure stdlib. Exit 1 blocks the commit; exit 0 lets it through. In --hook mode
(Claude Code PostToolUse) a violation exits 2 so the feedback reaches the model.

Usage:
  py .forge/hooks/guard.py --staged            # check staged files (pre-commit)
  py .forge/hooks/guard.py path/to/file.md     # check specific files
  py .forge/hooks/guard.py --copy copy.md       # also scan for slop vocabulary
  py .forge/hooks/guard.py --hook               # Claude Code hook (reads stdin)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DASH = re.compile(r"[\u2014\u2013]")  # em, en
TEXT_EXT = {".md", ".txt", ".json", ".py", ".ts", ".tsx", ".js", ".jsx", ".sh",
            ".ps1", ".yml", ".yaml", ".html", ".css", ".mjs", ".cjs", ".go", ".rs"}
SECRETS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}"), "OpenAI-style key"),
    (re.compile(r"\bghp_[A-Za-z0-9]{36}\b"), "GitHub token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"(?i)\b(api[_-]?key|secret|token)\b\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]"), "hardcoded secret"),
]

# Slop vocabulary (copy mode only). High-signal words and phrases that mark
# machine-written prose. Sourced from the copywriter taboo list.
VOCAB_WORDS = [
    "delve", "seamless", "seamlessly", "leverage", "leveraging", "elevate",
    "empower", "empowering", "unlock", "unlocks", "synergy", "synergies",
    "tapestry", "robust", "nahtlos", "ganzheitlich", "synergie",
]
VOCAB_PHRASES = [
    "in today's fast-paced", "in the ever-evolving", "it is important to note",
    "in conclusion", "at the end of the day", "when it comes to",
    "es ist wichtig zu beachten", "in der heutigen schnelllebigen",
]
VOCAB_WORD_RX = re.compile(r"(?i)\b(" + "|".join(VOCAB_WORDS) + r")\b")
VOCAB_PHRASE_RX = re.compile(r"(?i)(" + "|".join(re.escape(p) for p in VOCAB_PHRASES) + r")")
# Files that legitimately contain the banned words (they teach or document them),
# plus framework internals. Matched as lowercase path substrings.
VOCAB_EXEMPT = ("taboo_phrases", "humanizer", "anti_slop", "anti-slop",
                "german_anti_slop", "/.forge/", "/docs/", "readme.md",
                "changelog.md", "contributing.md", "agents.md")


def staged_files() -> list[str]:
    try:
        r = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                           capture_output=True, text=True, timeout=20)
        return [f for f in r.stdout.splitlines() if f.strip()]
    except Exception:
        return []


def _vocab_exempt(norm: str) -> bool:
    low = norm.lower()
    return any(s in low for s in VOCAB_EXEMPT)


def check(path: str, problems: list[str], vocab: bool = False) -> None:
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
    scan_vocab = vocab and p.suffix.lower() == ".md" and not _vocab_exempt(norm)
    for i, line in enumerate(text.splitlines(), 1):
        if "banned vocabulary" in line.lower():
            continue
        if DASH.search(line):
            problems.append(f"{norm}:{i}: em/en dash (use a hyphen, comma, or period).")
        for rx, label in SECRETS:
            if rx.search(line):
                problems.append(f"{norm}:{i}: possible {label}. Do not commit secrets.")
        if scan_vocab:
            mw = VOCAB_WORD_RX.search(line)
            if mw:
                problems.append(f"{norm}:{i}: slop word '{mw.group(1)}' (rewrite in plain language).")
            mp = VOCAB_PHRASE_RX.search(line)
            if mp:
                problems.append(f"{norm}:{i}: slop phrase '{mp.group(1)}' (cut it).")


def hook_mode() -> int:
    """Claude Code PostToolUse hook: read the tool payload from stdin, check the
    edited file, exit 2 with feedback on a violation so the model self-corrects."""
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    fp = (payload.get("tool_input") or {}).get("file_path")
    if not fp:
        return 0
    vocab = os.environ.get("RESONANCE_STRICT_VOCAB") == "1"
    problems: list[str] = []
    check(fp, problems, vocab=vocab)
    if problems:
        print("Resonance guard flagged this edit:", file=sys.stderr)
        for p in problems:
            print(f"  x {p}", file=sys.stderr)
        return 2
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Resonance deterministic commit guard.")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--staged", action="store_true", help="check staged files")
    ap.add_argument("--copy", action="store_true", help="also scan for slop vocabulary")
    ap.add_argument("--hook", action="store_true", help="Claude Code hook mode (reads stdin)")
    a = ap.parse_args(argv)

    if a.hook:
        return hook_mode()

    files = a.files or (staged_files() if a.staged else [])
    if not files:
        return 0
    vocab = a.copy or os.environ.get("RESONANCE_STRICT_VOCAB") == "1"
    problems: list[str] = []
    for f in files:
        check(f, problems, vocab=vocab)
    if problems:
        print("Resonance guard blocked the commit:\n")
        for p in problems:
            print(f"  x {p}")
        print(f"\n{len(problems)} violation(s). Fix them, or bypass once with `git commit --no-verify`.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
