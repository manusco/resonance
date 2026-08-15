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

import sys
from pathlib import Path

FORGE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(FORGE_DIR))
from kernel import manifest as skill_manifest  # noqa: E402

SKILLS = Path(".agents/skills")
OUT = Path("docs/SKILL_GRAPH.md")


def collect(root: Path = SKILLS) -> list[tuple[str, list[str]]]:
    return sorted(
        (entry["id"], entry["invokes"])
        for entry in skill_manifest.manifest(root)
        if entry.get("invokes")
    )


def render(root: Path = SKILLS) -> str:
    data = skill_manifest.manifest(root)
    edges = collect(root)
    by_id = {entry["id"]: entry for entry in data}
    out = [
        "# Skill Dependency Graph",
        "",
        "> Generated from `docs/skill-manifest.json` by `.forge/skill_graph.py`. "
        "Do not edit by hand; run the script. `validate_library.py` checks edge "
        "existence, ownership fields, cycles, reachability, and contract shape.",
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
    out += [
        "",
        "## Ownership Contracts",
        "",
        "| Skill | Archetype | Authority | Failure | Side effects |",
        "| --- | --- | --- | --- | --- |",
    ]
    for entry in sorted(data, key=lambda item: item["id"]):
        effects = ", ".join(entry["side_effects"]) if entry["side_effects"] else "none"
        out.append(
            f"| {entry['id']} | {entry['archetype']} | {entry['authority']} | "
            f"{entry['failure_policy']} | {effects} |"
        )
    invalid = skill_manifest.validate(data)
    out += [
        "",
        "## Validation",
        "",
        "This graph is valid." if not invalid else "This graph is invalid:",
    ]
    for issue in invalid:
        out.append(f"- {issue}")
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
