#!/usr/bin/env python3
"""
Resonance - Multi-Model Second Opinion (R5).

Dispatch a diff to a DIFFERENT model for an independent review, so cross-model
disagreement surfaces the bug one model rationalizes away. This is the harness;
the ops/second-opinion skill reconciles the result with the primary review.

Vendor-neutral and pluggable, like the eval runner. The second model is any CLI
that reads a prompt on stdin and prints its review:
  --model-cmd "codex exec"     (or gemini, llm, ollama run <model>, ...)
  env RESONANCE_REVIEW_CMD="..."
If none is configured, it prints the review prompt so you can run it in another
model by hand and paste the findings back. Clone-and-go survives with no setup.

Usage:
  python .forge/second_opinion.py                       # reviews `git diff HEAD`
  python .forge/second_opinion.py --diff changes.patch
  python .forge/second_opinion.py --model-cmd "codex exec" --context "adds JWT refresh"
"""
from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RUBRIC = """Review this diff as an independent second reviewer on a different model \
than the author. Be strict and specific. Look for, in this order of harm:
1. Correctness bugs (wrong output, missed edge/null/empty/error case, off-by-one, race).
2. Runtime safety (crashes, unhandled failures, resource leaks).
3. Auth and data integrity (missing checks, injection, broken invariants).
4. Environment robustness (config, migrations, backward compatibility).
5. Verification quality (untested paths, weak assertions).
For each finding give: file:line, a severity P0-P3, and one sentence on why it \
harms the user. If you find nothing at a severity, say so. Do not restyle or \
suggest broad rewrites. Reply as a short ranked list, most severe first."""


def get_diff(arg: str | None) -> str:
    if arg:
        p = Path(arg)
        return p.read_text(encoding="utf-8", errors="replace") if p.exists() else arg
    try:
        r = subprocess.run(["git", "diff", "HEAD"], capture_output=True, text=True, timeout=30)
        return r.stdout
    except Exception:
        return ""


def resolve_cmd(explicit: str) -> str:
    if explicit:
        return explicit
    env = os.environ.get("RESONANCE_REVIEW_CMD", "")
    if env:
        return env
    from shutil import which
    for c in ("codex", "gemini", "llm"):
        if which(c):
            return {"codex": "codex exec", "gemini": "gemini -p", "llm": "llm"}[c]
    return ""


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Get an independent second-model review of a diff.")
    ap.add_argument("--diff", help="patch file or inline diff (default: git diff HEAD)")
    ap.add_argument("--model-cmd", default="", help="second-model command reading the prompt on stdin")
    ap.add_argument("--context", default="", help="one line on what the change does")
    a = ap.parse_args(argv)

    diff = get_diff(a.diff).strip()
    if not diff:
        print("no diff found (nothing staged/changed, or pass --diff). Nothing to review.")
        return 0
    prompt = RUBRIC + (f"\n\nContext: {a.context}" if a.context else "") + f"\n\nDIFF:\n{diff}"

    cmd = resolve_cmd(a.model_cmd)
    if not cmd:
        print("No second-model command configured. Run the review below in another "
              "model (Codex, Gemini, a local model) and paste its findings back so "
              "the skill can reconcile them.\n")
        print("Set --model-cmd or RESONANCE_REVIEW_CMD to automate it.\n")
        print("=" * 60)
        print(prompt)
        return 0

    try:
        r = subprocess.run(shlex.split(cmd), input=prompt, capture_output=True, text=True, timeout=300)
        out = (r.stdout or "").strip()
    except Exception as e:
        print(f"second-model command failed ({e}). Falling back to the manual prompt.\n")
        print(prompt)
        return 0
    print(f"=== second opinion via `{cmd}` ===\n")
    print(out or "(the second model returned nothing)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
