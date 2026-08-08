#!/usr/bin/env python3
"""
Resonance - Doc Drift Checker (auto-doc-drift for /ship).

The docs drift from reality quietly: a version bumped in package.json but not the
README badge, a command added but the AGENTS map or the README count left stale.
This checks the things a release must keep in sync, deterministically, so /ship
can gate on it. Pure stdlib.

Checks:
  - the version string matches across package.json, the plugin and marketplace
    manifests, the README badge, and the installer scripts,
  - AGENTS.md's command map matches .forge/commands.json (same aliases -> skills),
  - the README's skill and command counts are not below reality,
  - the CHANGELOG has an entry for the current version.

Usage: python .forge/doc_drift.py
Exit: 0 in sync, 1 drift found.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(".")


def read(p: str) -> str:
    fp = ROOT / p
    return fp.read_text(encoding="utf-8", errors="replace") if fp.exists() else ""


def main() -> int:
    problems: list[str] = []

    # 1. version consistency (package.json is canonical)
    try:
        version = json.loads(read("package.json"))["version"]
    except Exception:
        print("cannot read version from package.json")
        return 1
    checks = {
        ".claude-plugin/plugin.json": rf'"version":\s*"{re.escape(version)}"',
        "README.md": rf"Resonance-v{re.escape(version)}-",
        "resonance.sh": re.escape(version),
        "resonance.ps1": re.escape(version),
    }
    for f, pat in checks.items():
        if not re.search(pat, read(f)):
            problems.append(f"version drift: {f} does not show {version}")
    mk = read(".claude-plugin/marketplace.json")
    if mk and mk.count(f'"{version}"') < mk.count('"version"'):
        problems.append(f"version drift: .claude-plugin/marketplace.json not all {version}")

    # 2. AGENTS command map vs commands.json
    try:
        cj = {c["alias"]: c["skill"] for c in json.loads(read(".forge/commands.json"))["commands"]}
    except Exception:
        cj = {}
    amap = dict(re.findall(r"\*\*/([a-z-]+)\*\*\s*->\s*`([^`]+)`", read("AGENTS.md")))
    for a in set(cj) - set(amap):
        problems.append(f"command map: /{a} in commands.json but not AGENTS.md")
    for a in set(amap) - set(cj):
        problems.append(f"command map: /{a} in AGENTS.md but not commands.json")
    for a in set(cj) & set(amap):
        if cj[a] != amap[a]:
            problems.append(f"command map: /{a} points to {cj[a]} vs AGENTS {amap[a]}")

    # 3. README counts not below reality
    n_skills = len(list((ROOT / ".agents/skills").glob("**/SKILL.md")))
    n_cmds = len(cj)
    readme = read("README.md")
    for m in re.findall(r"Skills-(\d+)\+?", readme):
        if int(m) > n_skills:
            problems.append(f"README claims {m} skills but there are {n_skills}")
    for m in re.findall(r"Commands-(\d+)", readme):
        if int(m) != n_cmds:
            problems.append(f"README badge says {m} commands but there are {n_cmds}")

    # 3b. README body prose, not only the badges (where drift keeps hiding)
    for m in re.findall(r"(\d+)\s+slash commands", readme):
        if int(m) != n_cmds:
            problems.append(f"README body says {m} slash commands but there are {n_cmds}")
    n_domains = sum(1 for d in (ROOT / ".agents/skills").glob("*") if d.is_dir())
    for m in re.findall(r"across (\d+) domains", readme):
        if int(m) != n_domains:
            problems.append(f"README says 'across {m} domains' but there are {n_domains}")
    for a in cj:
        if not re.search(rf"/{re.escape(a)}(?![\w-])", readme):
            problems.append(f"command /{a} in commands.json but not in the README catalog")

    # 4. CHANGELOG has this version
    if f"## v{version}" not in read("CHANGELOG.md"):
        problems.append(f"CHANGELOG.md has no entry for v{version}")

    if problems:
        print(f"doc drift ({version}):\n")
        for p in problems:
            print(f"  x {p}")
        print(f"\n{len(problems)} issue(s). Sync the docs before shipping.")
        return 1
    print(f"docs in sync at v{version}: {n_skills} skills, {n_cmds} commands, manifests and map agree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
