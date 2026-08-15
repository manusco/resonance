#!/usr/bin/env python3
"""Typed ledger parser and status-aware recall helpers."""
from __future__ import annotations

import re
from pathlib import Path

ENTRY_RE = re.compile(r"^##\s+((dec|les|met|cus|exp)-[a-z0-9-]+):\s*(.+?)\s*$")
FIELD_RE = re.compile(r"^([a-z_]+):\s*(.*)$")


def parse_ledger(root: Path = Path(".resonance/ledger")) -> list[dict]:
    entries: list[dict] = []
    if not root.is_dir():
        return entries
    for path in sorted(root.glob("*.md")):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        i = 0
        while i < len(lines):
            m = ENTRY_RE.match(lines[i])
            if not m:
                i += 1
                continue
            fields = {}
            body = []
            j = i + 1
            in_fields = True
            while j < len(lines):
                if ENTRY_RE.match(lines[j]):
                    break
                if in_fields and not lines[j].strip():
                    in_fields = False
                    j += 1
                    continue
                fm = FIELD_RE.match(lines[j]) if in_fields else None
                if fm:
                    fields[fm.group(1)] = fm.group(2).strip()
                elif lines[j].strip():
                    body.append(lines[j].strip())
                j += 1
            entries.append({
                "id": m.group(1),
                "title": m.group(3),
                "status": fields.get("status", "active"),
                "confidence": fields.get("confidence", ""),
                "review_due": fields.get("review_due", ""),
                "fields": fields,
                "text": "\n".join([f"{k}: {v}" for k, v in sorted(fields.items())] + body),
                "source": path.name,
            })
            i = j
    return entries


def active_entries(root: Path = Path(".resonance/ledger")) -> list[dict]:
    return [e for e in parse_ledger(root) if e.get("status") != "superseded"]
