#!/usr/bin/env python3
"""
Resonance Forge — Skill Compiler.

One source -> many targets. Author a skill once as a template with placeholders;
compile it per tool (host) and per model (overlay) into a ready SKILL.md.

    template.skill.md  x  host  x  model   ->   <output>/SKILL.md

This is the "don't lock to one vendor" layer: the SKILL.md/AGENTS.md shape is the
cross-tool lingua franca, but you author above it and emit a tailored output per
tool and model. Pure stdlib, cross-platform.

Placeholders understood in a template body:
    {{RESOLVER:name}}   inline .forge/resolvers/<name>.md   (shared sections: voice,
                        decision_brief, completion, locks, learnings, ...)
    {{OVERLAY}}         inline the chosen model overlay (.forge/overlays/<model>.md)
    {{TOOL:logical}}    map a logical tool name to this host's real tool name
                        (e.g. {{TOOL:edit}} -> "Edit" on claude-code, "apply_patch" on codex)

Host config (.forge/hosts/<host>.json):
    { "tool_names": {"read": "...", ...}, "output_path": ".agents/skills/{name}/SKILL.md",
      "default_model": "claude", "notes": "..." }

Usage:
    python .forge/forge.py build skill-author
    python .forge/forge.py build skill-author --host claude-code --model claude
    python .forge/forge.py build --all --host all
    python .forge/forge.py build skill-author --dry-run   # exit 1 if output drifted
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

# Resource dirs copied verbatim next to the generated SKILL.md so its references,
# scripts, and evals resolve at the output location.
RESOURCE_DIRS = ("references", "scripts", "assets", "evals")

FORGE = Path(__file__).resolve().parent
REPO = FORGE.parent
SKILLS_SRC = FORGE / "skills"
RESOLVERS = FORGE / "resolvers"
OVERLAYS = FORGE / "overlays"
HOSTS = FORGE / "hosts"

RESOLVER_RE = re.compile(r"\{\{RESOLVER:([a-z0-9_-]+)\}\}")
OVERLAY_RE = re.compile(r"\{\{OVERLAY\}\}")
TOOL_RE = re.compile(r"\{\{TOOL:([a-z0-9_-]+)\}\}")


def load_host(host: str) -> dict:
    p = HOSTS / f"{host}.json"
    if not p.exists():
        raise SystemExit(f"forge: unknown host '{host}'. Available: {available_hosts()}")
    return json.loads(p.read_text(encoding="utf-8"))


def available_hosts() -> list[str]:
    return sorted(p.stem for p in HOSTS.glob("*.json"))


def available_skills() -> list[str]:
    return sorted(p.parent.relative_to(SKILLS_SRC).as_posix() for p in SKILLS_SRC.glob("**/skill.tmpl.md"))


def resolve_template(text: str, host: dict, model: str) -> str:
    """Expand all placeholders. Resolvers expand first, then their own {{TOOL}}/
    {{OVERLAY}} placeholders get a second pass so shared sections can use them."""

    def sub_resolver(m: re.Match) -> str:
        name = m.group(1)
        f = RESOLVERS / f"{name}.md"
        if not f.exists():
            raise SystemExit(f"forge: missing resolver '{name}' ({f})")
        return f.read_text(encoding="utf-8").strip()

    def sub_overlay(_m: re.Match) -> str:
        f = OVERLAYS / f"{model}.md"
        if not f.exists():
            raise SystemExit(f"forge: missing overlay '{model}' ({f})")
        return f.read_text(encoding="utf-8").strip()

    def sub_tool(m: re.Match) -> str:
        logical = m.group(1)
        names = host.get("tool_names", {})
        if logical not in names:
            raise SystemExit(f"forge: host has no tool mapping for '{logical}'")
        return names[logical]

    # two passes so resolver bodies may themselves contain {{TOOL}} / {{OVERLAY}}
    for _ in range(2):
        text = RESOLVER_RE.sub(sub_resolver, text)
    text = OVERLAY_RE.sub(sub_overlay, text)
    text = TOOL_RE.sub(sub_tool, text)
    return text


def output_path(host: dict, name: str) -> Path:
    tmpl = host.get("output_path", ".agents/skills/{name}/SKILL.md")
    return REPO / tmpl.format(name=name)


def build_one(name: str, host_name: str, model: str | None, dry_run: bool) -> int:
    src = SKILLS_SRC / name / "skill.tmpl.md"
    if not src.exists():
        raise SystemExit(f"forge: no template for '{name}' ({src}). "
                         f"Available: {available_skills()}")
    host = load_host(host_name)
    model = model or host.get("default_model", "claude")
    rendered = resolve_template(src.read_text(encoding="utf-8"), host, model).rstrip() + "\n"

    out = output_path(host, name)
    if dry_run:
        current = out.read_text(encoding="utf-8") if out.exists() else ""
        if current != rendered:
            print(f"DRIFT  {out}  (regenerate: forge build {name} --host {host_name})")
            return 1
        print(f"fresh  {out}")
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered, encoding="utf-8")
    # Copy sibling resources (references/scripts/assets/evals) so links resolve.
    # Remove stale files individually (Windows can lock directory rmdir) then copy.
    for res in RESOURCE_DIRS:
        src_res = src.parent / res
        if src_res.is_dir():
            dst_res = out.parent / res
            if dst_res.exists():
                for f in sorted(dst_res.rglob("*"), reverse=True):
                    try:
                        f.unlink() if f.is_file() else f.rmdir()
                    except OSError:
                        pass
            shutil.copytree(src_res, dst_res, dirs_exist_ok=True)
    print(f"built  {out}  [host={host_name} model={model}]")
    return 0


def load_commands() -> list[dict]:
    """Read the slash-command alias map (.forge/commands.json)."""
    p = FORGE / "commands.json"
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8")).get("commands", [])


def render_command(alias: str, spec: dict, host: dict) -> str:
    """A thin command shim that routes to the canonical skill. The heavy body lives
    once under .agents/skills; the shim only registers the /alias per tool."""
    skill = spec["skill"]
    desc = spec.get("desc", f"Run the Resonance {alias} procedure.")
    manual = spec.get("manual", False)
    canonical = f".agents/skills/{skill}/SKILL.md"
    if host.get("command_style", "skill") == "skill":
        fm = [f"name: {alias}", f"description: {desc}"]
        if manual:
            fm.append("disable-model-invocation: true")
        front = "---\n" + "\n".join(fm) + "\n---\n"
        body = (f"\n# /{alias}\n\n"
                f"Run the Resonance **{alias}** procedure.\n\n"
                f"Read `{canonical}` in full and execute it exactly, following its Definition "
                f"of Done. That skill is the procedure; this file only routes the /{alias} "
                f"command to it.\n")
        return front + body
    # prompt style (codex, opencode): a plain prompt with a description
    front = "---\n" + f"description: {desc}\n" + "---\n"
    body = (f"\nRun the Resonance {alias} procedure. Read `{canonical}` in full and execute "
            f"it, following its Definition of Done.\n")
    return front + body


def build_commands(host_name: str, dry_run: bool) -> int:
    """Generate per-tool /command shims for hosts that declare a command_path.
    Hosts without one surface commands via AGENTS.md routing instead."""
    host = load_host(host_name)
    tmpl = host.get("command_path")
    if not tmpl:
        return 0
    rc, n = 0, 0
    for spec in load_commands():
        alias = spec["alias"]
        out = REPO / tmpl.format(alias=alias)
        rendered = render_command(alias, spec, host).rstrip() + "\n"
        if dry_run:
            current = out.read_text(encoding="utf-8") if out.exists() else ""
            if current != rendered:
                print(f"DRIFT  {out}")
                rc = 1
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
        n += 1
    if not dry_run:
        root = tmpl.split("{")[0]
        print(f"commands  {host_name}: {n} shims -> {root}")
    return rc


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Resonance Forge — compile skills from templates.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="Compile one or all skill templates")
    b.add_argument("name", nargs="?", help="Skill name (omit with --all)")
    b.add_argument("--all", action="store_true", help="Build every skill template")
    b.add_argument("--host", default="claude-code", help="Host name or 'all'")
    b.add_argument("--model", default=None, help="Model overlay (default: host default)")
    b.add_argument("--dry-run", action="store_true", help="Compare only; exit 1 on drift")

    c = sub.add_parser("commands", help="Generate slash-command shims from commands.json")
    c.add_argument("--host", default="all", help="Host name or 'all'")
    c.add_argument("--dry-run", action="store_true", help="Compare only; exit 1 on drift")

    sub.add_parser("list", help="List available skills, hosts, overlays")

    args = ap.parse_args(argv)

    if args.cmd == "list":
        print("skills:  ", ", ".join(available_skills()) or "(none)")
        print("hosts:   ", ", ".join(available_hosts()) or "(none)")
        print("overlays:", ", ".join(sorted(p.stem for p in OVERLAYS.glob("*.md"))) or "(none)")
        print("commands:", ", ".join(c["alias"] for c in load_commands()) or "(none)")
        return 0

    if args.cmd == "commands":
        hosts = available_hosts() if args.host == "all" else [args.host]
        rc = 0
        for h in hosts:
            rc |= build_commands(h, args.dry_run)
        return rc

    names = available_skills() if args.all else ([args.name] if args.name else [])
    if not names:
        raise SystemExit("forge build: pass a skill name or --all")
    hosts = available_hosts() if args.host == "all" else [args.host]

    rc = 0
    for n in names:
        for h in hosts:
            rc |= build_one(n, h, args.model, args.dry_run)
    # A full build also refreshes the slash-command shims so a clone is ready to use.
    if args.all:
        for h in hosts:
            rc |= build_commands(h, args.dry_run)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
