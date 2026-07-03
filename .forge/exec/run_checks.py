#!/usr/bin/env python3
"""
Resonance execution surface - run the project's real checks (the grounded verifier).

/test and /goal must ground on EXECUTED results, not described ones. Google DeepMind
showed a model cannot reliably self-correct without an external signal; SWE-bench
agents got good by iterating against real test output. This detects the project's
toolchain and runs its actual test, build, or lint command, capturing pass or fail
and the output as structured JSON. When no runnable check exists, it says so (a gap
to surface, never a silent pass). Pure stdlib, cross-platform.

Usage:
  python .forge/exec/run_checks.py [dir] [--only test|build|lint|typecheck] [--all] [--json]
Exit: 0 every run check passed, 1 a check failed, 3 no runnable check was found.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

KINDS = ("test", "build", "lint", "typecheck")


def _pm(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    if (root / "bun.lockb").exists() or (root / "bun.lock").exists():
        return "bun"
    return "npm"


def _node_cmd(pm: str, kind: str) -> str:
    # test has a bare form on npm/yarn/pnpm; everything else goes through `run`.
    if kind == "test" and pm in ("npm", "yarn", "pnpm"):
        return f"{pm} test"
    return f"{pm} run {kind}"


def detect(root: Path) -> list[dict]:
    """Return the runnable checks for this project, in a stable order per ecosystem."""
    checks: list[dict] = []
    pkg = root / "package.json"
    if pkg.exists():
        try:
            scripts = json.loads(pkg.read_text(encoding="utf-8", errors="replace")).get("scripts", {}) or {}
        except Exception:
            scripts = {}
        pm = _pm(root)
        for kind in KINDS:
            val = (scripts.get(kind) or "").strip()
            if val and "no test specified" not in val.lower():
                checks.append({"kind": kind, "cmd": _node_cmd(pm, kind), "eco": f"node/{pm}"})
    if (root / "go.mod").exists():
        checks += [{"kind": "test", "cmd": "go test ./...", "eco": "go"},
                   {"kind": "build", "cmd": "go build ./...", "eco": "go"},
                   {"kind": "lint", "cmd": "go vet ./...", "eco": "go"}]
    if (root / "Cargo.toml").exists():
        checks += [{"kind": "test", "cmd": "cargo test", "eco": "rust"},
                   {"kind": "build", "cmd": "cargo build", "eco": "rust"},
                   {"kind": "lint", "cmd": "cargo clippy", "eco": "rust"}]
    if (root / "pyproject.toml").exists() or (root / "setup.py").exists() or (root / "requirements.txt").exists():
        checks += [{"kind": "test", "cmd": "python -m pytest -q", "eco": "python"},
                   {"kind": "lint", "cmd": "ruff check .", "eco": "python"},
                   {"kind": "typecheck", "cmd": "mypy .", "eco": "python"}]
    mk = root / "Makefile"
    if mk.exists():
        targets = mk.read_text(encoding="utf-8", errors="replace")
        for kind in ("test", "build", "lint"):
            if any(line.startswith(f"{kind}:") for line in targets.splitlines()):
                # a Makefile target encodes the author's intent; prefer it.
                checks.insert(0, {"kind": kind, "cmd": f"make {kind}", "eco": "make"})
    # de-dupe by kind, first detection wins (Makefile inserted at front on purpose)
    seen, uniq = set(), []
    for c in checks:
        if c["kind"] not in seen:
            seen.add(c["kind"])
            uniq.append(c)
    return uniq


def run_one(check: dict, root: Path) -> dict:
    try:
        r = subprocess.run(check["cmd"], cwd=str(root), shell=True, capture_output=True,
                           text=True, timeout=1200, encoding="utf-8", errors="replace")
        out = ((r.stdout or "") + (r.stderr or "")).strip()
        tail = "\n".join(out.splitlines()[-40:])
        return {**check, "exit_code": r.returncode, "passed": r.returncode == 0, "output_tail": tail}
    except subprocess.TimeoutExpired:
        return {**check, "exit_code": None, "passed": False, "output_tail": "timed out after 1200s"}
    except Exception as e:
        return {**check, "exit_code": None, "passed": False, "output_tail": f"could not run: {e}"}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Run the project's real checks (grounded verifier).")
    ap.add_argument("dir", nargs="?", default=".", help="project dir (default: cwd)")
    ap.add_argument("--only", choices=KINDS, help="run only this kind")
    ap.add_argument("--all", action="store_true", help="run test, build, lint, and typecheck (default: test)")
    ap.add_argument("--json", action="store_true", help="emit JSON only")
    a = ap.parse_args(argv)

    root = Path(a.dir).resolve()
    checks = detect(root)
    if a.only:
        checks = [c for c in checks if c["kind"] == a.only]
    elif not a.all:
        checks = [c for c in checks if c["kind"] == "test"]

    if not checks:
        msg = f"no runnable {'check' if not a.only else a.only} found in {root.name} (this is a gap to surface, not a pass)"
        print(json.dumps({"root": str(root), "checks": [], "gap": msg}) if a.json else msg)
        return 3

    results = [run_one(c, root) for c in checks]
    ok = all(r["passed"] for r in results)
    if a.json:
        print(json.dumps({"root": str(root), "passed": ok, "checks": results}, indent=2))
    else:
        print(f"grounded checks in {root.name}:\n")
        for r in results:
            mark = "PASS" if r["passed"] else "FAIL"
            print(f"  [{mark}] {r['kind']:9} {r['eco']:11} `{r['cmd']}` (exit {r['exit_code']})")
            if not r["passed"]:
                for line in r["output_tail"].splitlines()[-8:]:
                    print(f"         {line}")
        print(f"\n{'all checks passed' if ok else 'a check failed'}: verified by execution, not by inspection.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
