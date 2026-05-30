#!/usr/bin/env python3
"""
Resonance Forge — Skill Validator (Tier 1, deterministic, free, <1s).

Static structural checks for any SKILL.md against the Resonance skill spec.
Pure stdlib. Cross-platform (Windows/macOS/Linux). No external deps.

Usage:
    python .forge/validate_skill.py .agents/skills/resonance-skill-author/SKILL.md
    python .forge/validate_skill.py --all .agents/skills
    python .forge/validate_skill.py --all .agents/skills --strict   # warnings fail too

Exit codes:
    0  no errors (warnings allowed unless --strict)
    1  one or more errors (or warnings under --strict)
    2  bad invocation
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ── Spec constants ───────────────────────────────────────────────────────────
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
MAX_DESC = 1024
BODY_SOFT_LINES = 500          # warn beyond this
REF_TOC_LINES = 100            # reference files longer than this need a TOC
ARCHETYPES = {"knowledge", "procedure", "orchestration"}
PORTABILITY_RESERVED = ("anthropic", "claude")  # warn: hurts cross-tool naming

# Procedure/orchestration skills must carry the Resonance operating contract.
CONTRACT_SECTIONS = ("Input", "Output", "Definition of Done", "Recovery")

# AI-slop / ceremony the voice resolver bans. Kept in sync with resolvers/voice.md.
BANNED_WORDS = (
    "delve", "crucial", "robust", "comprehensive", "nuanced", "multifaceted",
    "pivotal", "landscape", "tapestry", "seamless", "seamlessly", "underscore",
    "furthermore", "moreover", "additionally", "foster", "showcase", "intricate",
    "vibrant", "game-changing", "elevate", "unleash", "leverage the power",
)

TRIGGER_CUES = ("use when", "use this", "triggers", "trigger", "when the user",
                "when asked", "for ", "use for")


@dataclass
class Report:
    path: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return not self.errors


# ── Minimal frontmatter parser (no pyyaml dependency) ────────────────────────
def split_frontmatter(text: str) -> tuple[dict, str, int]:
    """Return (frontmatter_dict, body, body_start_line). Tolerant of block
    scalars (`key: |`) and simple `- item` lists. Values are str or list[str]."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text, 0
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text, 0

    fm: dict = {}
    key = None
    mode = None  # None | "list" | "block"
    block_buf: list[str] = []
    for raw in lines[1:end]:
        if mode == "block":
            if raw.startswith("  ") or raw.strip() == "":
                block_buf.append(raw[2:] if raw.startswith("  ") else raw)
                continue
            fm[key] = "\n".join(block_buf).strip()
            mode, block_buf = None, []
        stripped = raw.strip()
        if not stripped:
            continue
        if mode == "list" and stripped.startswith("- "):
            fm.setdefault(key, []).append(stripped[2:].strip())
            continue
        mode = None
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in ("|", ">", "|-", ">-"):
            mode, block_buf = "block", []
        elif val == "":
            mode = "list"          # may become a list on following lines
            fm[key] = ""           # default empty if no list items follow
        else:
            fm[key] = val.strip().strip('"').strip("'")
    if mode == "block":
        fm[key] = "\n".join(block_buf).strip()
    return fm, "\n".join(lines[end + 1:]), end + 1


# ── Checks ───────────────────────────────────────────────────────────────────
def check_frontmatter(fm: dict, r: Report) -> str:
    name = fm.get("name", "")
    if not name:
        r.err("frontmatter: missing required `name`")
    elif not NAME_RE.match(name if isinstance(name, str) else ""):
        r.err(f"frontmatter: `name` must match ^[a-z0-9-]{{1,64}}$ (got '{name}')")
    if isinstance(name, str):
        for bad in PORTABILITY_RESERVED:
            if bad in name:
                r.warn(f"frontmatter: `name` contains '{bad}' — fine for Claude, "
                       f"but hurts portability/namespacing across tools")

    desc = fm.get("description", "")
    if not desc:
        r.err("frontmatter: missing required `description` (this is what makes the "
              "skill trigger — never ship without it)")
    else:
        if len(desc) > MAX_DESC:
            r.err(f"frontmatter: `description` is {len(desc)} chars; max {MAX_DESC}")
        low = desc.lower()
        if desc.lstrip().lower().startswith(("i ", "i'", "you can", "you will", "we ")):
            r.warn("description: write in third person ('Creates…', not 'I can…' / "
                   "'You can…') — first/second person degrades discovery")
        if not any(cue in low for cue in TRIGGER_CUES):
            r.warn("description: add an explicit trigger ('Use when…', 'Triggers:…') so "
                   "the model knows WHEN to fire the skill, not just what it does")

    archetype = fm.get("archetype", "")
    if not archetype:
        r.warn("frontmatter: missing `archetype` (knowledge | procedure | orchestration)"
               " — Resonance skills declare their kind")
    elif archetype not in ARCHETYPES:
        r.err(f"frontmatter: `archetype` must be one of {sorted(ARCHETYPES)} "
              f"(got '{archetype}')")
    return archetype if archetype in ARCHETYPES else ""


def check_body(body: str, archetype: str, r: Report) -> None:
    n_lines = len(body.splitlines())
    if n_lines > BODY_SOFT_LINES:
        r.warn(f"body: {n_lines} lines (> {BODY_SOFT_LINES}). Move detail into "
               f"references/ and keep SKILL.md a navigable overview")

    # Scan for slop, but ignore the voice resolver's own enumeration of banned
    # words (otherwise every compiled skill self-trips on its injected voice note).
    scan = "\n".join(ln for ln in body.splitlines()
                     if "banned vocabulary" not in ln.lower()).lower()
    hits = sorted({w for w in BANNED_WORDS if re.search(rf"\b{re.escape(w)}\b", scan)})
    if hits:
        r.warn(f"voice: banned/slop terms in body: {', '.join(hits)}")

    if "—" in body:  # em dash
        r.warn("voice: em dashes present — Resonance voice uses commas/periods")

    if archetype in ("procedure", "orchestration"):
        missing = [s for s in CONTRACT_SECTIONS
                   if not re.search(rf"(?im)^\s*[#*>\-\s]*{re.escape(s)}\b", body)]
        if missing:
            r.err(f"contract: {archetype} skill missing required section(s): "
                  f"{', '.join(missing)}. Procedure skills declare their "
                  f"Input / Output / Definition of Done / Recovery")


def check_references(skill_dir: Path, body: str, r: Report) -> None:
    # backslash paths anywhere
    for m in re.finditer(r"\]\(([^)]+)\)", body):
        target = m.group(1)
        if "\\" in target:
            r.warn(f"paths: use forward slashes in links (got '{target}')")

    # markdown links to local .md files referenced from SKILL.md
    refs = [m.group(1).split("#")[0] for m in re.finditer(r"\]\(([^)]+\.md)\)", body)]
    for ref in refs:
        if ref.startswith(("http://", "https://")):
            continue
        target = (skill_dir / ref).resolve()
        if not target.exists():
            r.warn(f"references: linked file not found: {ref}")
            continue
        rtext = target.read_text(encoding="utf-8", errors="replace")
        if len(rtext.splitlines()) > REF_TOC_LINES:
            if not re.search(r"(?im)^#+\s*(contents|table of contents)\b", rtext):
                r.warn(f"references: {ref} is > {REF_TOC_LINES} lines without a "
                       f"'## Contents' TOC (partial reads will miss scope)")
        # one-level-deep rule: referenced file should not itself fan out to more .md
        nested = re.findall(r"\]\(([^)]+\.md)\)", rtext)
        nested = [n for n in nested if not n.startswith(("http://", "https://"))]
        if nested:
            r.warn(f"references: {ref} links onward to {len(nested)} more file(s). "
                   f"Keep references one level deep from SKILL.md")


def check_evals(skill_dir: Path, r: Report) -> None:
    eval_dir = skill_dir / "evals"
    cases = list(eval_dir.glob("*.json")) if eval_dir.exists() else []
    if len(cases) < 3:
        r.warn(f"evals: found {len(cases)} case(s) in evals/. Ship >= 3 golden cases "
               f"(query + expected_behavior) before declaring a skill done")


def validate(path: Path, r: Report) -> Report:
    if not path.exists():
        r.err("file does not exist")
        return r
    text = path.read_text(encoding="utf-8", errors="replace")
    fm, body, _ = split_frontmatter(text)
    if not fm:
        r.err("no YAML frontmatter found (file must open with a '---' block)")
        return r
    archetype = check_frontmatter(fm, r)
    check_body(body, archetype, r)
    check_references(path.parent, body, r)
    check_evals(path.parent, r)
    return r


# ── CLI ──────────────────────────────────────────────────────────────────────
def iter_skills(root: Path):
    yield from sorted(root.glob("**/SKILL.md"))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Validate SKILL.md files against the Resonance spec.")
    ap.add_argument("path", help="Path to a SKILL.md, or a root dir with --all")
    ap.add_argument("--all", action="store_true", help="Treat path as a root; validate every SKILL.md under it")
    ap.add_argument("--strict", action="store_true", help="Warnings count as failures")
    args = ap.parse_args(argv)

    root = Path(args.path)
    targets = list(iter_skills(root)) if args.all else [root]
    if not targets:
        print(f"No SKILL.md found under {root}")
        return 2

    reports = [validate(t, Report(str(t))) for t in targets]
    n_err = n_warn = 0
    for rep in reports:
        if not rep.errors and not rep.warnings:
            print(f"PASS  {rep.path}")
            continue
        status = "FAIL" if rep.errors else "WARN"
        print(f"{status}  {rep.path}")
        for e in rep.errors:
            print(f"    ERROR  {e}")
            n_err += 1
        for w in rep.warnings:
            print(f"    warn   {w}")
            n_warn += 1

    print(f"\n{len(targets)} skill(s) | {n_err} error(s) | {n_warn} warning(s)")
    failed = n_err > 0 or (args.strict and n_warn > 0)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
