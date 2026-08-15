#!/usr/bin/env python3
"""Generate machine-readable skill manifests from compiled skills."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(".agents/skills")
OUT = Path("docs/skill-manifest.json")


def frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    raw = text[3:end] if end != -1 else ""
    data: dict[str, object] = {}
    current = None
    for line in raw.splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            current = m.group(1)
            value = m.group(2).strip()
            data[current] = value.strip("\"'") if value else []
            continue
        m = re.match(r"^\s*-\s*(.+?)\s*$", line)
        if m and current:
            data.setdefault(current, [])
            if isinstance(data[current], list):
                data[current].append(m.group(1).strip())
    return data


def manifest(root: Path = ROOT) -> list[dict]:
    out = []
    for sk in sorted(root.glob("**/SKILL.md")):
        text = sk.read_text(encoding="utf-8", errors="replace")
        fm = frontmatter(text)
        if not fm.get("name"):
            continue
        archetype = fm.get("archetype", "knowledge")
        side_effects = []
        if archetype in ("procedure", "orchestration"):
            side_effects.append("may_write_files")
        out.append({
            "schema_version": 1,
            "id": fm["name"],
            "path": sk.relative_to(root).as_posix(),
            "archetype": archetype,
            "owner": str(fm["name"]).replace("resonance-", "").replace("-", "."),
            "activation": "manual" if archetype in ("procedure", "orchestration") else "automatic",
            "authority": "consequential" if side_effects else "advisory",
            "triggers": [fm.get("description", "")],
            "negative_triggers": [],
            "inputs": [],
            "outputs": [],
            "invokes": fm.get("invokes", []) if isinstance(fm.get("invokes"), list) else [],
            "side_effects": side_effects,
            "write_sets": [],
            "failure_policy": "stop",
        })
    return out


def main(argv: list[str]) -> int:
    data = manifest()
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if "--check" in argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print(f"DRIFT  {OUT} is out of date. Run: py .forge/kernel/manifest.py")
            return 1
        print(f"fresh  {OUT}")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote  {OUT}  ({len(data)} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
