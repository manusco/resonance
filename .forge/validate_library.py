#!/usr/bin/env python3
"""
Resonance Forge - Library Validator (Tier 1.5, cross-skill, deterministic, free).

`validate_skill.py` checks one skill in isolation. This checks the WHOLE library
for the defects that only show up across files: orphan references, duplicated or
diverged reference files, eval `skill` fields that do not match the skill name,
two-level-deep reference links, attribution/provenance leaks, em/en dashes (in
references, skill bodies, and eval fixtures), and time-bound claims. Pure stdlib.

Usage:
    python .forge/validate_library.py                      # scans .agents/skills
    python .forge/validate_library.py --root .agents/skills
    python .forge/validate_library.py --strict            # warnings fail too

Exit codes: 0 clean (warnings allowed unless --strict), 1 issues found, 2 bad args.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

LINK_MD = re.compile(r"\]\(([^)]+\.md)[^)]*\)")
NAME_RE = re.compile(r"(?m)^name:\s*(.+?)\s*$")
DESC_SKILL = re.compile(r'"skill"\s*:\s*"([^"]+)"')
PROVENANCE = re.compile(
    r"(ui-ux-pro-max|\bancoleman\b|Outstanding Skills Standard|Universal 1% Standard"
    r"|Zero-Trust Agent Architecture|Created by the [A-Z])",
    re.I,
)
TIME_BOUND = re.compile(r"\b(20\d\d Edition|as of 20\d\d|in 20\d\d\b|\(20\d\d\))")
DASH = re.compile(r"[\u2014\u2013]")  # em, en


def frontmatter_name(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    fm = text[3:end] if end != -1 else ""
    m = NAME_RE.search(fm)
    return m.group(1).strip().strip('"').strip("'") if m else ""


def rel(p: Path, root: Path) -> str:
    try:
        return p.relative_to(root.parent).as_posix()
    except ValueError:
        return p.as_posix()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Validate the whole Resonance skill library.")
    ap.add_argument("--root", default=".agents/skills", help="Skills root to scan")
    ap.add_argument("--strict", action="store_true", help="Warnings count as failure")
    args = ap.parse_args(argv)

    root = Path(args.root)
    if not root.exists():
        print(f"library: root not found: {root}")
        return 2

    skills = sorted(root.glob("**/SKILL.md"))
    errors: list[str] = []
    warnings: list[str] = []

    ref_by_name: dict[str, list[Path]] = defaultdict(list)

    for sk in skills:
        sdir = sk.parent
        body = sk.read_text(encoding="utf-8", errors="replace")
        name = frontmatter_name(body)
        linked = {m.group(1).split("/")[-1] for m in LINK_MD.finditer(body)}

        refdir = sdir / "references"
        if refdir.is_dir():
            for rf in sorted(refdir.glob("*.md")):
                ref_by_name[rf.name].append(rf)
                # orphan: reference not linked from its SKILL.md
                if rf.name not in linked:
                    warnings.append(f"orphan reference (not linked): {rel(rf, root)}")
                rtext = rf.read_text(encoding="utf-8", errors="replace")
                # two-level-deep: a reference that links to another .md
                nested = [n for n in LINK_MD.findall(rtext)
                          if not n.startswith(("http://", "https://"))]
                if nested:
                    errors.append(f"two-level reference link: {rel(rf, root)} -> {nested[0]}")
                # provenance / dashes / time-bound inside references
                _scan(rtext, rf, root, errors, warnings)

        # eval skill-name integrity + the house dash rule (evals are text too)
        evdir = sdir / "evals"
        if evdir.is_dir() and name:
            for ev in sorted(evdir.glob("*.json")):
                evtext = ev.read_text(encoding="utf-8", errors="replace")
                m = DESC_SKILL.search(evtext)
                if m and m.group(1) != name:
                    errors.append(
                        f"eval skill mismatch: {rel(ev, root)} says '{m.group(1)}', "
                        f"skill is '{name}'")
                for ln_no, line in enumerate(evtext.splitlines(), 1):
                    if DASH.search(line):
                        errors.append(f"em/en dash: {rel(ev, root)}:{ln_no}")

        _scan(body, sk, root, errors, warnings)

    # duplicate reference basenames across skills
    for rname, paths in sorted(ref_by_name.items()):
        if len(paths) > 1:
            hashes = {hashlib.md5(p.read_bytes()).hexdigest() for p in paths}
            where = ", ".join(rel(p, root) for p in paths)
            if len(hashes) > 1:
                # identical copies are acceptable (skills stay self-contained for
                # portability); only DIVERGED copies are a real bug.
                errors.append(f"duplicate reference (DIVERGED) '{rname}': {where}")

    # near-duplicate basenames (fuzzy): same stem after removing _protocol / separators
    def canon(n: str) -> str:
        return re.sub(r"[-_]", "", n.replace("_protocol", "").replace(".md", "").lower())
    canon_map: dict[str, set[str]] = defaultdict(set)
    for rname in ref_by_name:
        canon_map[canon(rname)].add(rname)
    for c, names in sorted(canon_map.items()):
        if len(names) > 1:
            warnings.append(f"near-duplicate reference names: {sorted(names)}")

    print(f"Resonance library scan: {len(skills)} skills under {root}\n")
    for e in errors:
        print(f"  ERROR  {e}")
    for w in warnings:
        print(f"  warn   {w}")
    print(f"\n{len(errors)} error(s) | {len(warnings)} warning(s)")
    return 1 if (errors or (args.strict and warnings)) else 0


def _scan(text: str, path: Path, root: Path, errors: list[str], warnings: list[str]) -> None:
    for ln_no, line in enumerate(text.splitlines(), 1):
        if "banned vocabulary" in line.lower():
            continue
        if DASH.search(line):
            errors.append(f"em/en dash: {rel(path, root)}:{ln_no}")
        if PROVENANCE.search(line):
            errors.append(f"provenance/attribution leak: {rel(path, root)}:{ln_no}")
        if TIME_BOUND.search(line):
            warnings.append(f"time-bound claim: {rel(path, root)}:{ln_no}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
