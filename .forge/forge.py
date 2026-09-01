#!/usr/bin/env python3
"""
Resonance Forge - Skill Compiler.

One source -> many targets. Author a skill once as a template with placeholders;
compile it per tool (host) and per model (overlay) into a ready SKILL.md.

    template.skill.md  x  host  x  model   ->   <output>/SKILL.md

This is the "don't lock to one vendor" layer: the SKILL.md/AGENTS.md shape is the
cross-tool lingua franca, but you author above it and emit a tailored output per
tool and model. Pure stdlib, cross-platform.

Placeholders understood in a template body:
    {{RESOLVER:name}}   inline .forge/resolvers/<name>.md   (shared sections: voice,
                        decision_brief, completion, locks, learnings, ...)
    {{OVERLAY}}         inline the portable execution profile
    {{TOOL:logical}}    map a logical tool name to this host's real tool name
                        (e.g. {{TOOL:edit}} -> "Edit" on claude-code, "apply_patch" on codex)

Host config (.forge/hosts/<host>.json):
    { "tool_names": {"read": "...", ...}, "output_path": ".agents/skills/{name}/SKILL.md",
      "default_model": "claude", "notes": "..." }

Usage:
    python .forge/forge.py build skill-author
    python .forge/forge.py build ops/skill-author/resonance-skill-author
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
if str(FORGE) not in sys.path:
    sys.path.insert(0, str(FORGE))
SKILLS_SRC = FORGE / "skills"
RESOLVERS = FORGE / "resolvers"
OVERLAYS = FORGE / "overlays"
HOSTS = FORGE / "hosts"
CANONICAL_HOST = {
    "host": "portable", "default_model": "portable",
    "output_path": ".agents/skills/{name}/SKILL.md",
    "tool_names": {"read": "read", "write": "write", "edit": "edit", "bash": "shell",
                   "grep": "search", "glob": "search", "ask": "ask the user",
                   "subagent": "delegate"},
}

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
    host = CANONICAL_HOST
    model = model or "portable"
    if model != "portable":
        raise SystemExit("forge: canonical skills only accept --model portable; model-specific behavior belongs in runtime profiles")
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
        dst_res = out.parent / res
        if dst_res.exists():
            for f in sorted(dst_res.rglob("*"), reverse=True):
                try:
                    f.unlink() if f.is_file() else f.rmdir()
                except OSError:
                    pass
            try:
                dst_res.rmdir()
            except OSError:
                pass
        if src_res.is_dir():
            shutil.copytree(src_res, dst_res, dirs_exist_ok=True)
    print(f"built  {out}  [profile={model}]")
    return 0


def load_commands() -> list[dict]:
    """Read the slash-command alias map (.forge/commands.json)."""
    p = FORGE / "commands.json"
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8")).get("commands", [])


def load_command_registry() -> dict:
    """Read command presentation data without interpreting skill semantics."""
    p = FORGE / "commands.json"
    if not p.exists():
        raise SystemExit(f"forge: missing command registry ({p})")
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data.get("commands"), list) or not isinstance(data.get("catalog"), dict):
        raise SystemExit("forge: commands.json requires 'commands' and 'catalog' objects")
    return data


DOC_SECTIONS = {
    "README.md": (
        "SKILL_COUNT_BADGE",
        "COMMAND_COUNT_BADGE",
        "SKILL_COUNT_SUMMARY",
        "COMMAND_COUNT_SUMMARY",
        "COMMAND_CATALOG",
        "SKILL_DOMAIN_COUNT",
    ),
    "AGENTS.md": ("COMMAND_CATALOG", "AUTOMATIC_SKILLS"),
}


def section_marker(name: str, edge: str) -> str:
    return f"<!-- RESONANCE-GENERATED:{name}:{edge} -->"


def replace_generated_section(text: str, name: str, rendered: str, path: Path) -> str:
    """Replace one bounded section, refusing ambiguous or damaged boundaries."""
    start = section_marker(name, "START")
    end = section_marker(name, "END")
    if text.count(start) != 1 or text.count(end) != 1:
        raise SystemExit(
            f"forge: {path} requires exactly one {start} and one {end} marker"
        )
    start_at = text.index(start)
    end_at = text.index(end)
    if start_at >= end_at:
        raise SystemExit(f"forge: {path} has reversed markers for {name}")
    body_start = start_at + len(start)
    replacement = "\n" + rendered.rstrip() + "\n"
    return text[:body_start] + replacement + text[end_at:]


def validate_catalog(registry: dict) -> tuple[list[dict], list[dict], list[str]]:
    commands = registry["commands"]
    families = registry["catalog"].get("families")
    help_items = registry["catalog"].get("help")
    if not isinstance(families, list) or not isinstance(help_items, list):
        raise SystemExit("forge: command catalog requires 'families' and 'help' lists")
    aliases = [c.get("alias") for c in commands]
    if any(not isinstance(a, str) or not a for a in aliases) or len(aliases) != len(set(aliases)):
        raise SystemExit("forge: command aliases must be non-empty and unique")
    catalog_aliases = [a for family in families for a in family.get("aliases", [])]
    if len(catalog_aliases) != len(set(catalog_aliases)):
        raise SystemExit("forge: every command may appear in only one catalog family")
    missing = sorted(set(aliases) - set(catalog_aliases))
    unknown = sorted(set(catalog_aliases) - set(aliases))
    if missing or unknown:
        raise SystemExit(f"forge: command catalog mismatch; missing={missing}, unknown={unknown}")
    if any(not isinstance(item, str) or not item.strip() for item in help_items):
        raise SystemExit("forge: command catalog help entries must be non-empty strings")
    manifest = framework_skill_manifest()
    by_path = {Path(item["path"]).parent.as_posix(): item for item in manifest}
    for command in commands:
        alias, skill = command.get("alias"), command.get("skill")
        if not isinstance(skill, str) or skill not in by_path:
            raise SystemExit(f"forge: /{alias} targets unknown canonical skill {skill!r}")
        if "manual" in command and not isinstance(command["manual"], bool):
            raise SystemExit(f"forge: /{alias} manual must be boolean")
        declared = by_path[skill].get("entrypoints", [])
        if declared and f"/{alias}" not in declared:
            raise SystemExit(
                f"forge: /{alias} conflicts with {skill} declared entrypoints {declared}"
            )
    return commands, families, help_items


def framework_skill_manifest() -> list[dict]:
    """Build runtime metadata only from framework-owned skill templates."""
    from kernel.manifest import normalize_entry

    entries = []
    for template in sorted(SKILLS_SRC.glob("**/skill.tmpl.md")):
        entry = normalize_entry(template, SKILLS_SRC)
        if entry:
            entries.append(entry)
    return entries


def render_readme_catalog(commands: list[dict], families: list[dict], help_items: list[str]) -> str:
    by_alias = {c["alias"]: c for c in commands}
    lines = [f"The registry contains **{len(commands)} commands**.", ""]
    for family in families:
        lines.append(f"**{family['name']}**")
        entries = [f"`/{alias}`: {by_alias[alias]['desc']}" for alias in family["aliases"]]
        lines.append(" · ".join(entries))
        lines.append("")
    lines.append("**Which command should I use?**")
    lines.extend(f"- {item}" for item in help_items)
    lines.extend(["", "If the route is still unclear, start with `/brief`."])
    return "\n".join(lines)


def render_agents_catalog(commands: list[dict], families: list[dict], help_items: list[str]) -> str:
    by_alias = {c["alias"]: c for c in commands}
    lines = []
    for family in families:
        lines.append(f"### {family['name']}")
        for alias in family["aliases"]:
            spec = by_alias[alias]
            lines.append(f"- **/{alias}** -> `{spec['skill']}` - {spec['desc']}")
        lines.append("")
    lines.append("### Choosing between nearby commands")
    lines.extend(f"- {item}" for item in help_items)
    lines.extend(["", "If the route is still unclear, start with `/brief`."])
    return "\n".join(lines)


def build_command_docs(dry_run: bool) -> int:
    """Generate bounded command documentation while preserving all other bytes."""
    commands, families, help_items = validate_catalog(load_command_registry())
    manifest = framework_skill_manifest()
    skill_count = len(manifest)
    domains = sorted({Path(item["path"]).parts[0] for item in manifest})
    automatic = sorted(
        Path(item["path"]).parent.as_posix()
        for item in manifest
        if item.get("activation") == "automatic"
    )
    rendered = {
        "README.md": {
            "SKILL_COUNT_BADGE": (
                f'    <img src="https://img.shields.io/badge/Skills-{skill_count}-00f2ea?style=for-the-badge" '
                f'alt="{skill_count} skills" />'
            ),
            "COMMAND_COUNT_BADGE": (
                f'    <img src="https://img.shields.io/badge/Commands-{len(commands)}-7025eb?style=for-the-badge" '
                f'alt="{len(commands)} commands" />'
            ),
            "COMMAND_COUNT_SUMMARY": (
                f"- **{len(commands)} slash commands** like `/brief`, `/plan`, `/grill`, `/council`, "
                "`/build`, `/debug`, `/design`, `/test`, `/improve`, and `/ship`. Type the command, "
                "or describe the job and let the specialist auto-fire."
            ),
            "COMMAND_CATALOG": render_readme_catalog(commands, families, help_items),
            "SKILL_COUNT_SUMMARY": (
                f"- **{skill_count} domain-tested skills** across {', '.join(domains[:-1])}, and {domains[-1]}. "
                "Each skill is a structured procedure with prerequisites, a step-by-step algorithm, a Recovery path, "
                "and a Definition of Done, backed by a deep reference library. Not a prompt. A protocol."
            ),
            "SKILL_DOMAIN_COUNT": (
                f"{skill_count} skills across {len(domains)} domains, each a self-contained protocol backed by reference docs."
            ),
        },
        "AGENTS.md": {
            "COMMAND_CATALOG": render_agents_catalog(commands, families, help_items),
            "AUTOMATIC_SKILLS": (
                "Knowledge skills apply themselves when relevant: "
                + ", ".join(f"`{path}`" for path in automatic)
                + "."
            ),
        },
    }
    rc = 0
    for relative, names in DOC_SECTIONS.items():
        path = REPO / relative
        # Decode bytes directly so Python does not normalize line endings. The
        # replacement is bounded; every byte outside the markers stays intact.
        current = path.read_bytes().decode("utf-8")
        updated = current
        for name in names:
            updated = replace_generated_section(updated, name, rendered[relative][name], path)
        if dry_run:
            if current != updated:
                print(f"DRIFT  {path}")
                rc = 1
        else:
            path.write_bytes(updated.encode("utf-8"))
            print(f"catalog   {relative}: {len(commands)} commands")
    return rc


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
        return "<!-- Generated by Resonance Forge. -->\n" + front + body
    # prompt style (codex, opencode): a plain prompt with a description
    front = "---\n" + f"description: {desc}\n" + "---\n"
    body = (f"\nRun the Resonance {alias} procedure. Read `{canonical}` in full and execute "
            f"it, following its Definition of Done.\n")
    return "<!-- Generated by Resonance Forge. -->\n" + front + body


def generated_command(text: str) -> bool:
    return text.startswith("<!-- Generated by Resonance Forge. -->")


def build_commands(host_name: str, dry_run: bool) -> int:
    """Generate per-tool /command shims for hosts that declare a command_path.
    Hosts without one surface commands via AGENTS.md routing instead."""
    host = load_host(host_name)
    tmpl = host.get("command_path")
    if not tmpl:
        return 0
    rc, n = 0, 0
    expected: set[Path] = set()
    for spec in load_commands():
        alias = spec["alias"]
        out = REPO / tmpl.format(alias=alias)
        expected.add(out)
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
    root_path = REPO / tmpl.split("{")[0]
    if root_path.is_dir() and not dry_run:
        for old in root_path.rglob("*.md"):
            body = old.read_text(encoding="utf-8", errors="replace")
            if old not in expected and generated_command(body):
                old.unlink()
    if not dry_run:
        root = tmpl.split("{")[0]
        print(f"commands  {host_name}: {n} shims -> {root}")
        try:
            if Path.cwd().resolve() != REPO.resolve():
                print(f"note: shims land relative to the parent of .forge/ ({REPO}), "
                      f"not the current directory. Install .forge/ at the project root.")
        except Exception:
            pass
    return rc


def render_bridge(host: dict) -> str | None:
    """The per-host context bridge: the file this host DOES load at session start,
    pointing at the operating standard (AGENTS.md) and the project memory (.resonance/).
    This is the carrier. Without it, a host that only auto-loads its own memory file
    never sees AGENTS.md or the accumulated lessons. Hosts that read AGENTS.md natively
    declare context_bridge: null and rely on AGENTS.md's own memory pointer."""
    cb = host.get("context_bridge")
    if not cb:
        return None
    imports = cb.get("imports", ["AGENTS.md"])
    style = cb.get("style", "at-import")
    if style == "at-import":
        # Claude Code: an @path line transcludes the file into always-loaded context.
        head = ("# Resonance\n\nThis project runs on the Resonance operating standard. It and "
                "the project memory load at the start of every session through the imports "
                "below. Do not edit this file by hand; the Forge regenerates it.\n\n")
        return head + "\n".join(f"@{p}" for p in imports) + "\n"
    if style == "mdc-always":
        # Cursor: an always-applied rule. .mdc cannot transclude, so it instructs the read.
        refs = ", ".join(f"`{p}`" for p in imports)
        front = ("---\ndescription: Resonance operating standard and project memory\n"
                 "alwaysApply: true\n---\n")
        body = ("\nFollow the Resonance operating standard in `AGENTS.md` in full. At the start "
                "of every session, read the project memory before acting: " + refs + ". They "
                "carry the project's state and its accumulated lessons; load any linked leaf "
                "file relevant to the task, and never solve the same problem twice. Do not edit "
                "this file by hand; the Forge regenerates it.\n")
        return front + body
    raise SystemExit(f"forge: unknown context_bridge style '{style}'")


def build_bridges(host_name: str, dry_run: bool) -> int:
    """Emit the per-host context bridge (e.g. CLAUDE.md for Claude Code). No-op for
    AGENTS.md-native hosts, whose context_bridge is null."""
    host = load_host(host_name)
    if not host.get("context_bridge"):
        return 0
    out = REPO / host["context_bridge"]["path"]
    rendered = (render_bridge(host) or "").rstrip() + "\n"
    if dry_run:
        current = out.read_text(encoding="utf-8") if out.exists() else ""
        if current != rendered:
            print(f"DRIFT  {out}  (regenerate: forge build --all --host {host_name})")
            return 1
        return 0
    # Never clobber a hand-authored file that happens to sit at this path (e.g. a user's
    # own CLAUDE.md). Only overwrite a file the Forge itself wrote (it carries the marker).
    if out.exists():
        current = out.read_text(encoding="utf-8")
        if current.strip() and "the Forge regenerates it" not in current:
            imports = ", ".join(host["context_bridge"].get("imports", []))
            print(f"skip      {host_name}: {host['context_bridge']['path']} is hand-authored; "
                  f"add these imports to it yourself: {imports}")
            return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered, encoding="utf-8")
    print(f"bridge    {host_name}: {host['context_bridge']['path']}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Resonance Forge - compile skills from templates.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="Compile one or all skill templates")
    b.add_argument("name", nargs="?", help="Skill name (omit with --all)")
    b.add_argument("--all", action="store_true", help="Build every skill template")
    b.add_argument("--host", default="claude-code", help="Host name or 'all'")
    b.add_argument("--model", default=None, help="Model overlay (default: host default)")
    b.add_argument("--dry-run", action="store_true", help="Compare only; exit 1 on drift")

    c = sub.add_parser("commands", help="Generate per-host command shims and context bridges")
    c.add_argument("--host", default="all", help="Host name or 'all'")
    c.add_argument("--dry-run", action="store_true", help="Compare only; exit 1 on drift")

    sub.add_parser("list", help="List available skills, hosts, overlays")
    d = sub.add_parser("doctor", help="Report compiler ownership and adapter support")
    d.add_argument("--json", action="store_true")

    args = ap.parse_args(argv)

    if args.cmd == "list":
        print("skills:  ", ", ".join(available_skills()) or "(none)")
        print("hosts:   ", ", ".join(available_hosts()) or "(none)")
        print("overlays:", ", ".join(sorted(p.stem for p in OVERLAYS.glob("*.md"))) or "(none)")
        print("commands:", ", ".join(c["alias"] for c in load_commands()) or "(none)")
        return 0

    if args.cmd == "doctor":
        hosts = {h: load_host(h) for h in available_hosts()}
        paths: dict[str, list[str]] = {}
        for name, cfg in hosts.items():
            if cfg.get("command_path"):
                paths.setdefault(cfg["command_path"], []).append(name)
        report = {"ok": all(len(v) == 1 for v in paths.values()),
                  "canonical_skill_path": CANONICAL_HOST["output_path"],
                  "canonical_profile": CANONICAL_HOST["default_model"],
                  "adapters": {h: {"invocation": c.get("invocation"),
                                    "command_path": c.get("command_path"),
                                    "context_bridge": c.get("context_bridge")} for h, c in hosts.items()},
                  "path_owners": paths}
        print(json.dumps(report, indent=2) if args.json else report)
        return 0 if report["ok"] else 1

    if args.cmd == "commands":
        hosts = available_hosts() if args.host == "all" else [args.host]
        rc = build_command_docs(args.dry_run)
        for h in hosts:
            rc |= build_commands(h, args.dry_run)
            rc |= build_bridges(h, args.dry_run)
        return rc

    names = available_skills() if args.all else ([args.name] if args.name else [])
    if not names:
        raise SystemExit("forge build: pass a skill name or --all")
    rc = 0
    for n in names:
        rc |= build_one(n, "portable", args.model, args.dry_run)
    # A full build also refreshes the slash-command shims and the per-host context
    # bridge (the carrier) so a clone is ready to use on every tool.
    if args.all:
        hosts = available_hosts() if args.host == "all" else [args.host]
        rc |= build_command_docs(args.dry_run)
        for h in hosts:
            rc |= build_commands(h, args.dry_run)
            rc |= build_bridges(h, args.dry_run)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
