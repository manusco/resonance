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
    r"|Zero-Trust Agent Architecture|Created by the [A-Z])",
    re.I,
)
TIME_BOUND = re.compile(r"\b(20\d\d Edition|as of 20\d\d|in 20\d\d\b|\(20\d\d\))")
DASH = re.compile(r"[\u2014\u2013]")  # em, en

# \u2500\u2500 State ledger (.resonance/ledger/), schema resonance-ledger/N \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
LEDGER_VERSION_MAX = 1
LEDGER_FILE_PREFIX = {"decisions": "dec", "lessons": "les", "metrics": "met",
                      "customers": "cus", "experiments": "exp"}
LEDGER_TYPE = {"dec": "decision", "les": "lesson", "met": "metric",
               "cus": "customer", "exp": "experiment"}
LEDGER_STATUS = {"active", "superseded", "closed"}
LEDGER_REQUIRED = {
    "decision": ("type", "created", "status"),
    "lesson": ("type", "created", "status"),
    "metric": ("type", "created", "status", "value", "unit", "as_of", "source"),
    "customer": ("type", "created", "status"),
    "experiment": ("type", "created", "status", "hypothesis"),
}
LEDGER_EDGE_FIELDS = ("supersedes", "evidences", "caused", "superseded_by")
LEDGER_ID_RE = re.compile(r"^(dec|les|met|cus|exp)-[a-z0-9][a-z0-9-]*$")
LEDGER_ENTRY_RE = re.compile(r"^##\s+((dec|les|met|cus|exp)-[a-z0-9-]+):\s*(.+?)\s*$")
LEDGER_SCHEMA_RE = re.compile(r"^schema:\s*resonance-ledger/(\d+)\s*$")
LEDGER_FIELD_RE = re.compile(r"^([a-z_]+):\s*(.*)$")


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


def _split_edges(raw: str) -> list[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


def _parse_ledger_file(path: Path):
    """Return (version_or_None, has_marker, entries). Each entry is a dict:
    {id, prefix, fields: {key: value}, line}. Prose headings are ignored; only
    headings whose id starts with a known type prefix are parsed as entries."""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    version, has_marker = None, False
    for ln in lines[:6]:
        m = LEDGER_SCHEMA_RE.match(ln.strip())
        if m:
            has_marker = True
            version = int(m.group(1))
            break
    entries, i = [], 0
    while i < len(lines):
        m = LEDGER_ENTRY_RE.match(lines[i])
        if not m:
            i += 1
            continue
        eid, prefix = m.group(1), m.group(2)
        fields, j = {}, i + 1
        while j < len(lines) and lines[j].strip() != "":
            fm = LEDGER_FIELD_RE.match(lines[j])
            if fm:
                fields[fm.group(1)] = fm.group(2).strip()
            j += 1
        entries.append({"id": eid, "prefix": prefix, "fields": fields, "line": i + 1})
        i = j
    return version, has_marker, entries


def _is_iso_date(s: str) -> bool:
    try:
        _dt.date.fromisoformat(s)
        return True
    except ValueError:
        return False


def _ledger_checks(errors: list[str], warnings: list[str]) -> None:
    """Validate the typed state ledger if one exists. Absence of .resonance/ledger/
    is the grace rule: a legacy untyped brain skips every check, silently. Mirrors
    the conditional pattern of _flagship_memory_checks. Deterministic checks only."""
    ldir = Path(".resonance/ledger")
    if not ldir.is_dir():
        return
    all_entries: dict[str, dict] = {}      # id -> entry (+ _file, _type)
    referenced: list[tuple[str, str, str]] = []  # (src_id, field, target_id)
    for fname, prefix in sorted(LEDGER_FILE_PREFIX.items()):
        fpath = ldir / f"{fname}.md"
        if not fpath.is_file():
            errors.append(f"ledger: missing file .resonance/ledger/{fname}.md")
            continue
        version, has_marker, entries = _parse_ledger_file(fpath)
        if not has_marker:
            errors.append(f"ledger: {fname}.md missing 'schema: resonance-ledger/N' marker")
        elif version > LEDGER_VERSION_MAX:
            errors.append(f"ledger: {fname}.md schema version {version} is newer than this "
                          f"framework knows ({LEDGER_VERSION_MAX}); upgrade the framework")
        etype = LEDGER_TYPE[prefix]
        for e in entries:
            loc = f"ledger/{fname}.md:{e['line']}"
            eid, fields = e["id"], e["fields"]
            if not LEDGER_ID_RE.match(eid):
                errors.append(f"ledger: bad id '{eid}' ({loc})")
            if e["prefix"] != prefix:
                errors.append(f"ledger: '{eid}' is a {LEDGER_TYPE[e['prefix']]} entry in "
                              f"{fname}.md (belongs in {e['prefix']} file) ({loc})")
            if eid in all_entries:
                errors.append(f"ledger: duplicate id '{eid}' ({loc})")
            for req in LEDGER_REQUIRED[etype]:
                if req not in fields:
                    errors.append(f"ledger: '{eid}' missing required field '{req}' ({loc})")
            if fields.get("type") and fields["type"] != etype:
                errors.append(f"ledger: '{eid}' type '{fields['type']}' should be '{etype}' ({loc})")
            st = fields.get("status")
            if st and st not in LEDGER_STATUS:
                errors.append(f"ledger: '{eid}' status '{st}' not in {sorted(LEDGER_STATUS)} ({loc})")
            for datef in ("created", "as_of", "due"):
                if fields.get(datef) and not _is_iso_date(fields[datef]):
                    errors.append(f"ledger: '{eid}' {datef} '{fields[datef]}' is not an ISO date ({loc})")
            if etype == "experiment" and st == "closed" and "result" not in fields:
                errors.append(f"ledger: closed experiment '{eid}' missing 'result' ({loc})")
            for ef in LEDGER_EDGE_FIELDS:
                if ef in fields:
                    for tgt in _split_edges(fields[ef]):
                        referenced.append((eid, ef, tgt))
            e["_file"], e["_type"], e["_loc"] = fname, etype, loc
            all_entries[eid] = e
    # cross-entry: no dangling edge refs
    for src, field, tgt in referenced:
        if tgt not in all_entries:
            errors.append(f"ledger: '{src}' {field} points at missing id '{tgt}'")
    # supersede reciprocity
    for eid, e in all_entries.items():
        sup = e["fields"].get("supersedes")
        if not sup:
            continue
        for old_id in _split_edges(sup):
            old = all_entries.get(old_id)
            if not old:
                continue  # dangling already reported
            if old["fields"].get("status") != "superseded":
                errors.append(f"ledger: '{eid}' supersedes '{old_id}' but it is not "
                              f"status:superseded ({old['_loc']})")
            if old["fields"].get("superseded_by") != eid:
                errors.append(f"ledger: '{old_id}' missing 'superseded_by: {eid}' back-ref "
                              f"({old['_loc']})")


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
