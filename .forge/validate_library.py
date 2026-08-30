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
import datetime as _dt
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

LINK_MD = re.compile(r"\]\(([^)]+\.md)[^)]*\)")
NAME_RE = re.compile(r"(?m)^name:\s*(.+?)\s*$")
DESC_SKILL = re.compile(r'"skill"\s*:\s*"([^"]+)"')
PROVENANCE = re.compile(
    r"(ui-ux-pro-max|\bancoleman\b|Outstanding Skills Standard|Universal 1% Standard"
    r"|Zero-Trust Agent Architecture|Created by the [A-Z]"
    r"|Packaged Source Note|Source Note|provenance:|attribution:"
    r"|inspired by\s+https?://|adapted from\s+https?://|ported from\s+https?://"
    r"|forked from\s+https?://|based on\s+https?://)",
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


def frontmatter_invokes(text: str) -> list[str]:
    """Extract the `invokes:` YAML list from a skill's frontmatter (the declared
    edges of the skill-dependency graph). Returns [] if absent."""
    if not text.startswith("---"):
        return []
    end = text.find("\n---", 3)
    fm = text[3:end] if end != -1 else ""
    out, in_list = [], False
    for line in fm.splitlines():
        if re.match(r"^invokes:\s*$", line):
            in_list = True
            continue
        if in_list:
            m = re.match(r"^\s*-\s*(.+?)\s*$", line)
            if m:
                out.append(m.group(1).strip())
                continue
            if line.strip():  # a new key ends the list
                break
    return out


def rel(p: Path, root: Path) -> str:
    try:
        return p.relative_to(root.parent).as_posix()
    except ValueError:
        return p.as_posix()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Validate the whole Resonance skill library.")
    ap.add_argument("--root", default=".agents/skills", help="Skills root to scan")
    ap.add_argument("--strict", action="store_true", help="Warnings count as failure")
    ap.add_argument("--composition-canary", action="store_true",
                    help="deprecated compatibility flag; v1 contract enforcement is always active")
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

    _evals_sync_check(errors)
    _flagship_memory_checks(errors, warnings)
    _ledger_checks(errors, warnings)
    _command_target_checks(errors)
    _skill_graph_checks(root, errors)
    _skill_manifest_checks(root, errors)
    from kernel.manifest import composition_warnings, manifest
    from validate_skill import COMPOSITION_CANARY_IDS
    errors.extend(
        warning.replace("composition canary:", "composition contract:", 1)
        for warning in composition_warnings(manifest(root), COMPOSITION_CANARY_IDS)
    )

    print(f"Resonance library scan: {len(skills)} skills under {root}\n")
    for e in errors:
        print(f"  ERROR  {e}")
    for w in warnings:
        print(f"  warn   {w}")
    print(f"\n{len(errors)} error(s) | {len(warnings)} warning(s)")
    return 1 if (errors or (args.strict and warnings)) else 0


def _evals_sync_check(errors: list[str]) -> None:
    """The runner reads COMPILED evals (.agents); the improvement baseline hashes
    SOURCE evals (.forge/skills). A hand-edit to a compiled case would change what
    gets measured without tripping the rubric-change gate, so the two trees must
    stay identical (newline-normalized; git may translate line endings)."""
    src_root = Path(".forge/skills")
    out_root = Path(".agents/skills")
    if not src_root.is_dir() or not out_root.is_dir():
        return
    for src in sorted(src_root.glob("**/evals/*.json")):
        rel = src.relative_to(src_root)
        out = out_root / rel
        if not out.is_file():
            errors.append(f"eval not compiled: {rel.as_posix()} (run forge.py build)")
            continue
        a = src.read_bytes().replace(b"\r\n", b"\n")
        b = out.read_bytes().replace(b"\r\n", b"\n")
        if a != b:
            errors.append(f"eval diverged from source: {rel.as_posix()} (run forge.py build)")


def _flagship_memory_checks(errors: list[str], warnings: list[str]) -> None:
    """Instance-memory checks, active only on a machine where
    ~/.resonance/machine.json wires this repo to a private memory overlay.
    Everywhere else this is silent, so cloners never see it. Two checks:
    the overlay must be reachable (a loop that dies silently stays dead),
    and lessons older than 30 days must carry a hardening pointer
    ('=> hardened: <id>') or an explicit '[soft]' marker."""
    gb = Path(os.environ.get("RESONANCE_GLOBAL_BRAIN", str(Path.home() / ".resonance")))
    try:
        cfg = json.loads((gb / "machine.json").read_text(encoding="utf-8-sig"))
    except Exception:
        return
    pm, fm = cfg.get("publicMirror", ""), cfg.get("flagshipMemory", "")
    if not pm or not fm:
        return
    try:
        if Path(pm).resolve() != Path.cwd().resolve():
            return
    except Exception:
        return
    idx = Path(fm) / "02_memory.local.md"
    if not idx.is_file():
        warnings.append(f"flagship memory unreachable: {idx} (machine.json flagshipMemory)")
        return
    lesson_rx = re.compile(r"^- (\d{4}-\d{2}-\d{2}) \*\*")
    today = _dt.date.today()
    section = ""
    for ln_no, line in enumerate(idx.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if line.startswith("## "):
            section = line[3:].strip().lower()
            continue
        if section != "lessons":
            continue
        m = lesson_rx.match(line.strip())
        if not m or "=> hardened:" in line or "[soft]" in line:
            continue
        try:
            d = _dt.date.fromisoformat(m.group(1))
        except ValueError:
            continue
        if (today - d).days > 30:
            warnings.append(f"unhardened lesson older than 30 days: {idx.name}:{ln_no} "
                            f"(add '=> hardened: <id>' or '[soft]')")


def _ledger_checks(errors: list[str], warnings: list[str]) -> None:
    """Validate the typed state ledger if one exists. Absence of .resonance/ledger/
    is the grace rule: a legacy untyped brain skips every check, silently. Mirrors
    the conditional pattern of _flagship_memory_checks. Deterministic checks only."""
    try:
        from kernel.ledger import validate_ledger
    except Exception as exc:
        errors.append(f"ledger: cannot import kernel validator: {exc}")
        return
    l_errors, l_warnings = validate_ledger(Path(".resonance/ledger"))
    errors.extend(l_errors)
    warnings.extend(l_warnings)


def _command_target_checks(errors: list[str]) -> None:
    """Every slash command must resolve to a real skill file. doc_drift checks
    counts and map/manifest agreement but not target existence, so a command that
    points at a skill nobody built (a dangling /command) slips through. This closes
    that gap: the shim routes to .agents/skills/<skill>/SKILL.md, so it must exist."""
    cj = Path(".forge/commands.json")
    out_root = Path(".agents/skills")
    if not cj.is_file() or not out_root.is_dir():
        return
    try:
        cmds = json.loads(cj.read_text(encoding="utf-8")).get("commands", [])
    except Exception:
        return
    for c in cmds:
        skill = c.get("skill", "")
        if skill and not (out_root / skill / "SKILL.md").is_file():
            errors.append(f"command '/{c.get('alias')}' targets missing skill "
                          f"'{skill}' (.agents/skills/{skill}/SKILL.md does not exist)")


def _skill_graph_checks(root: Path, errors: list[str]) -> None:
    """Validate the declared skill-dependency graph: every `invokes:` edge must
    point at a skill that exists. A dangling edge means an orchestrator names a
    delegate that was renamed or never built."""
    skills = sorted(root.glob("**/SKILL.md"))
    names: set[str] = set()
    edges: list[tuple[str, Path, list[str]]] = []
    for sk in skills:
        text = sk.read_text(encoding="utf-8", errors="replace")
        nm = frontmatter_name(text)
        if nm:
            names.add(nm)
        inv = frontmatter_invokes(text)
        if inv:
            edges.append((nm or rel(sk, root), sk, inv))
    for nm, sk, inv in edges:
        for tgt in inv:
            if tgt not in names:
                errors.append(f"skill graph: '{nm}' invokes '{tgt}', which is not a known "
                              f"skill ({rel(sk, root)})")


def _skill_manifest_checks(root: Path, errors: list[str]) -> None:
    """The machine-readable skill manifest is the compile-time ownership contract
    for tools that should not parse Markdown ad hoc. Keep it present and fresh."""
    try:
        import kernel.manifest as km
    except Exception as exc:
        errors.append(f"skill manifest: cannot import generator: {exc}")
        return
    out = Path("docs/skill-manifest.json")
    if not out.is_file():
        errors.append("skill manifest: docs/skill-manifest.json is missing")
        return
    expected = json.dumps(km.manifest(root), indent=2, ensure_ascii=False) + "\n"
    current = out.read_text(encoding="utf-8", errors="replace")
    if current != expected:
        errors.append("skill manifest: docs/skill-manifest.json is stale "
                      "(run py .forge/kernel/manifest.py)")
    errors.extend(km.validate(km.manifest(root)))

    try:
        import job_composition
        expected_jobs = json.dumps(job_composition.compile_contracts(km.manifest(root)), indent=2) + "\n"
    except Exception as exc:
        errors.append(f"job composition: cannot compile contracts: {exc}")
        return
    job_out = Path("docs/job-compositions.json")
    if not job_out.is_file():
        errors.append("job composition: docs/job-compositions.json is missing")
    elif job_out.read_text(encoding="utf-8", errors="replace") != expected_jobs:
        errors.append("job composition: docs/job-compositions.json is stale "
                      "(run py .forge/job_composition.py)")


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
