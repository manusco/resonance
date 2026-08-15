#!/usr/bin/env python3
"""
Resonance - Multi-Model Second Opinion.

Dispatch a diff or concrete decision artifact to a DIFFERENT configured reviewer,
so cross-model disagreement surfaces the bug or assumption one model rationalizes
away. This is the harness; the ops/second-opinion skill reconciles the result.

Vendor-neutral and pluggable, like the eval runner. The second model is any CLI
that reads a prompt on stdin and prints its review:
  --model-cmd "codex exec"     (or gemini, llm, ollama run <model>, ...)
  env RESONANCE_REVIEW_CMD="..."
If none is configured, it prints the review prompt so you can run it in another
model by hand and paste the findings back. That is an incomplete gate, not a pass.

Usage:
  python .forge/second_opinion.py --mode diff
  python .forge/second_opinion.py --mode decision --artifact docs/adr/auth.md
  python .forge/second_opinion.py --model-cmd "codex exec" --reviewer-id "codex-sol"
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
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

DECISION_RUBRIC = """Review this decision artifact as an independent second reviewer \
on a different model than the author. Be strict and practical. Do not invent file \
lines or P0-P3 severities. Look for:
1. Unproven assumptions.
2. Conflicting constraints.
3. Hidden tradeoffs or lock-in.
4. Missing reversal or rollback conditions.
5. Evidence that should change the recommendation.
6. The strongest objection.
Reply as a short decision critique with: assumptions, evidence gaps, tradeoffs, \
reversal conditions, strongest objection, and required changes."""

SECRET_RE = re.compile(
    r"(-----BEGIN [A-Z ]*PRIVATE KEY-----|"
    r"(?i:api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,})"
)
DEFAULT_MAX_CHARS = 120_000


def get_diff(arg: str | None) -> str:
    if arg:
        p = Path(arg)
        return p.read_text(encoding="utf-8", errors="replace") if p.exists() else arg
    try:
        r = subprocess.run(["git", "diff", "HEAD"], capture_output=True, text=True, timeout=30)
        return r.stdout
    except Exception:
        return ""


def get_artifact(arg: str | None) -> str:
    if not arg:
        return ""
    p = Path(arg)
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else arg


def resolve_cmd(explicit: str) -> str:
    if explicit:
        return explicit
    env = os.environ.get("RESONANCE_REVIEW_CMD", "")
    if env:
        return env
    return ""


def artifact_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


def validate_dispatch(text: str, max_chars: int) -> tuple[bool, str]:
    if not text.strip():
        return False, "empty artifact"
    if len(text) > max_chars:
        return False, f"artifact too large ({len(text)} chars > {max_chars})"
    if SECRET_RE.search(text):
        return False, "possible secret detected; redact before dispatch"
    return True, ""


def identities_independent(author_id: str, reviewer_id: str) -> tuple[bool, str]:
    if not reviewer_id:
        return False, "reviewer identity unknown"
    if author_id and reviewer_id == author_id:
        return False, "reviewer identity matches author identity"
    return True, ""


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Get an independent second-model review of a diff.")
    ap.add_argument("--mode", choices=("diff", "decision"), default="diff",
                    help="review type: diff (default) or decision")
    ap.add_argument("--diff", help="patch file or inline diff (default: git diff HEAD)")
    ap.add_argument("--artifact", help="decision artifact file or inline text")
    ap.add_argument("--model-cmd", default="", help="second-model command reading the prompt on stdin")
    ap.add_argument("--reviewer-id", default=os.environ.get("RESONANCE_REVIEWER_ID", ""),
                    help="configured reviewer identity")
    ap.add_argument("--author-id", default=os.environ.get("RESONANCE_AUTHOR_ID", ""),
                    help="author or primary reviewer identity")
    ap.add_argument("--max-chars", type=int, default=int(os.environ.get(
                    "RESONANCE_REVIEW_MAX_CHARS", str(DEFAULT_MAX_CHARS))),
                    help="maximum artifact size allowed for dispatch")
    ap.add_argument("--context", default="", help="one line on what the change does")
    a = ap.parse_args(argv)

    body = get_diff(a.diff).strip() if a.mode == "diff" else get_artifact(a.artifact).strip()
    ok, reason = validate_dispatch(body, a.max_chars)
    if not ok:
        print(f"INCOMPLETE  {reason}.")
        return 2
    h = artifact_hash(body)
    rubric = RUBRIC if a.mode == "diff" else DECISION_RUBRIC
    label = "DIFF" if a.mode == "diff" else "DECISION ARTIFACT"
    prompt = (rubric
              + (f"\n\nContext: {a.context}" if a.context else "")
              + f"\n\nMode: {a.mode}\nArtifact hash: {h}\n\n{label}:\n{body}")

    cmd = resolve_cmd(a.model_cmd)
    if not cmd:
        print("INCOMPLETE  no second-model command configured. Run the review below in "
              "another model and paste its findings back so the skill can reconcile them.\n")
        print("Set --model-cmd or RESONANCE_REVIEW_CMD to automate it.\n")
        print(f"Mode: {a.mode}")
        print(f"Artifact hash: {h}")
        print("=" * 60)
        print(prompt)
        return 3

    independent, why = identities_independent(a.author_id, a.reviewer_id)
    if not independent:
        print(f"INCOMPLETE  {why}. Set --reviewer-id/RESONANCE_REVIEWER_ID "
              f"and make it differ from --author-id/RESONANCE_AUTHOR_ID.")
        return 3

    try:
        r = subprocess.run(cmd, shell=True, input=prompt, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=300)
        out = (r.stdout or "").strip()
    except Exception as e:
        print(f"FAILED  second-model command failed ({e}). Manual prompt follows.\n")
        print(prompt)
        return 1
    if r.returncode != 0:
        print(f"FAILED  second-model command exited {r.returncode}.")
        if r.stderr:
            print(r.stderr.strip())
        return 1
    if not out:
        print("FAILED  the second model returned empty output.")
        return 1
    print(f"=== second opinion mode={a.mode} reviewer={a.reviewer_id} hash={h} via `{cmd}` ===\n")
    print(out or "(the second model returned nothing)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
