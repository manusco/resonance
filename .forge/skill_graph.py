#!/usr/bin/env python3
"""
Resonance Forge - Skill Dependency Graph renderer.

Reads the `invokes:` frontmatter of every skill (the declared edges of the
skill-dependency graph) and renders docs/SKILL_GRAPH.md: a Mermaid diagram plus
an edge table. validate_library.py checks that every edge resolves to a real
skill; this draws the map. Pure stdlib.

Usage:
  python .forge/skill_graph.py            # write docs/SKILL_GRAPH.md
  python .forge/skill_graph.py --check    # exit 1 if the file is out of date
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SKILLS = Path(".agents/skills")
OUT = Path("docs/SKILL_GRAPH.md")
NAME_RE = re.compile(r"(?m)^name:\s*(.+?)\s*$")


def _fm(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def _name(text: str) -> str:
    m = NAME_RE.search(_fm(text))
    return m.group(1).strip().strip('"').strip("'") if m else ""


def _invokes(text: str) -> list[str]:
    out, in_list = [], False
    for line in _fm(text).splitlines():
        if re.match(r"^invokes:\s*$", line):
            in_list = True
            continue
        if in_list:
            m = re.match(r"^\s*-\s*(.+?)\s*$", line)
            if m:
                out.append(m.group(1).strip())
                continue
            if line.strip():
                break
    return out


def collect(root: Path = SKILLS) -> list[tuple[str, list[str]]]:
    edges = []
    for sk in sorted(root.glob("**/SKILL.md")):
        text = sk.read_text(encoding="utf-8", errors="replace")
        name, inv = _name(text), _invokes(text)
        if name and inv:
            edges.append((name, inv))  # declared order preserved
    return sorted(edges, key=lambda e: e[0])


def render(root: Path = SKILLS) -> str:
    edges = collect(root)
    out = [
        "# Skill Dependency Graph",
        "",
        "> Generated from the `invokes:` frontmatter of each skill by "
        "`.forge/skill_graph.py`. Do not edit by hand; run the script. "
        "`validate_library.py` checks that every edge below resolves to a real skill, "
        "so a renamed or missing delegate fails the build.",
        "",
        "## Orchestration edges",
        "",
        "```mermaid",
        "graph LR",
    ]
    for name, inv in edges:
        for tgt in inv:
            out.append(f"  {name} --> {tgt}")
    out += ["```", "", "## Edges", "", "| Orchestrator | Invokes |", "| --- | --- |"]
    for name, inv in edges:
        out.append(f"| {name} | {', '.join(inv)} |")
    return "\n".join(out) + "\n"


def main(argv: list[str]) -> int:
    rendered = render()
    if "--check" in argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != rendered:
            print(f"DRIFT  {OUT} is out of date. Run: py .forge/skill_graph.py")
            return 1
        print(f"fresh  {OUT}")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(rendered, encoding="utf-8")
    print(f"wrote  {OUT}  ({len(collect())} orchestrators)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
