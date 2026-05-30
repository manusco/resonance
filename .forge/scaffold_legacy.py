#!/usr/bin/env python3
"""
Resonance Forge — Legacy Scaffolder.

Mechanical port of an existing .agents/skills/<name>/ (or .agents/workflows/<f>.md)
into .forge/skills/<name>/ so the rebuild can focus on the template body, not on
file plumbing. Idempotent. Never overwrites a template you have already written.

Behavior:
  - .agents/skills/<name>/references/  -> .forge/skills/<name>/references/   (copy)
  - .agents/skills/<name>/scripts/     -> .forge/skills/<name>/scripts/      (copy)
  - .agents/skills/<name>/data/        -> .forge/skills/<name>/data/         (copy)
  - .forge/skills/<name>/evals/        -> ensure exists (you write the cases)
  - .forge/skills/<name>/skill.tmpl.md -> seed a stub IF missing (you fill it in)

Usage:
    py .forge/scaffold_legacy.py resonance-backend
    py .forge/scaffold_legacy.py --workflow build       # port .agents/workflows/build.md
    py .forge/scaffold_legacy.py --all-skills
    py .forge/scaffold_legacy.py --all-workflows
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LEGACY_SKILLS = REPO / ".agents" / "skills"
LEGACY_WORKFLOWS = REPO / ".agents" / "workflows"
FORGE_SKILLS = REPO / ".forge" / "skills"
RESOURCE_DIRS = ("references", "scripts", "assets", "data")

STUB_KNOWLEDGE = '''---
name: {name}
description: TODO third-person what + when. Use when <trigger>, <trigger>.
archetype: knowledge
---

# {title}

> **Expertise:** TODO one line
> **Apply when:** TODO

## How this expert thinks

TODO

## Frameworks

TODO

## Boundaries

- Out of scope: TODO.
- Do NOT: TODO.

## Reference library

TODO list references one level deep:
- [<ref>](references/<file>.md): when to open it

{{{{RESOLVER:voice}}}}

{{{{OVERLAY}}}}
'''

STUB_PROCEDURE = '''---
name: {name}
description: TODO third-person what + when. Use when <trigger>, <trigger>.
archetype: procedure
---

# /{name}: TODO one-line job

> **Role:** TODO
> **Input:** TODO
> **Output:** TODO
> **Definition of Done:** TODO

## Prerequisites (fail fast)

- [ ] TODO

## Algorithm

1. **TODO**: action. → verify: check.

## Recovery

- TODO failure mode → TODO step.

{{{{RESOLVER:decision_brief}}}}

{{{{RESOLVER:completion}}}}

{{{{RESOLVER:voice}}}}

{{{{OVERLAY}}}}
'''


def port_skill(name: str, archetype: str = "knowledge") -> None:
    src = LEGACY_SKILLS / name
    if not src.is_dir():
        print(f"skip   {name}: no legacy dir at {src}")
        return
    dst = FORGE_SKILLS / name
    dst.mkdir(parents=True, exist_ok=True)
    for res in RESOURCE_DIRS:
        s = src / res
        if s.is_dir():
            d = dst / res
            if d.exists():
                shutil.rmtree(d)
            shutil.copytree(s, d, dirs_exist_ok=True)
            print(f"  port {res}/  ({sum(1 for _ in s.rglob('*') if _.is_file())} files)")
    (dst / "evals").mkdir(exist_ok=True)
    tmpl = dst / "skill.tmpl.md"
    if not tmpl.exists():
        title = " ".join(p.capitalize() for p in name.replace("resonance-", "").split("-"))
        stub = STUB_KNOWLEDGE if archetype == "knowledge" else STUB_PROCEDURE
        tmpl.write_text(stub.format(name=name, title=title), encoding="utf-8")
        print(f"  seed skill.tmpl.md (stub)")
    print(f"ok     {name}")


def port_workflow(slug: str) -> None:
    """Workflow = procedure skill. Its name stays bare ('/build' = 'build')."""
    src = LEGACY_WORKFLOWS / f"{slug}.md"
    if not src.exists():
        print(f"skip   /{slug}: no legacy file at {src}")
        return
    dst = FORGE_SKILLS / slug
    dst.mkdir(parents=True, exist_ok=True)
    (dst / "evals").mkdir(exist_ok=True)
    # Save the legacy source so the rebuild can mine it.
    legacy_copy = dst / "_legacy_workflow.md"
    legacy_copy.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    tmpl = dst / "skill.tmpl.md"
    if not tmpl.exists():
        title = " ".join(p.capitalize() for p in slug.split("-"))
        tmpl.write_text(STUB_PROCEDURE.format(name=slug, title=title), encoding="utf-8")
        print(f"  seed skill.tmpl.md (procedure stub)")
    print(f"ok     /{slug}  (legacy saved at _legacy_workflow.md)")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Port legacy skills/workflows into the Forge.")
    ap.add_argument("name", nargs="?", help="skill name (e.g. resonance-backend)")
    ap.add_argument("--workflow", action="store_true", help="port .agents/workflows/<name>.md")
    ap.add_argument("--all-skills", action="store_true")
    ap.add_argument("--all-workflows", action="store_true")
    ap.add_argument("--archetype", default="knowledge",
                    choices=["knowledge", "procedure", "orchestration"])
    args = ap.parse_args(argv)

    if args.all_skills:
        for p in sorted(LEGACY_SKILLS.iterdir()):
            if p.is_dir():
                port_skill(p.name, args.archetype)
        return 0
    if args.all_workflows:
        for p in sorted(LEGACY_WORKFLOWS.glob("*.md")):
            port_workflow(p.stem)
        return 0
    if not args.name:
        ap.error("name required (or use --all-skills / --all-workflows)")
    if args.workflow:
        port_workflow(args.name)
    else:
        port_skill(args.name, args.archetype)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
