#!/usr/bin/env python3
"""Typed ledger parser, validator, and status-aware recall helpers."""
from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

ENTRY_RE = re.compile(r"^##\s+((dec|les|met|cus|exp)-[a-z0-9-]+):\s*(.+?)\s*$")
FIELD_RE = re.compile(r"^([a-z_]+):\s*(.*)$")
SCHEMA_RE = re.compile(r"^schema:\s*resonance-ledger/(\d+)\s*$")
VERSION_MAX = 2
FILE_PREFIX = {
    "decisions": "dec",
    "lessons": "les",
    "metrics": "met",
    "customers": "cus",
    "experiments": "exp",
}
TYPE_BY_PREFIX = {
    "dec": "decision",
    "les": "lesson",
    "met": "metric",
    "cus": "customer",
    "exp": "experiment",
}
STATUS = {"active", "superseded", "closed"}
REQUIRED_V1 = {
    "decision": ("type", "created", "status"),
    "lesson": ("type", "created", "status"),
    "metric": ("type", "created", "status", "value", "unit", "as_of", "source"),
    "customer": ("type", "created", "status"),
    "experiment": ("type", "created", "status", "hypothesis"),
}
REQUIRED_V2 = {
    "decision": ("type", "created", "status", "confidence", "review_due"),
    "lesson": ("type", "created", "status", "confidence", "review_due"),
    "metric": ("type", "created", "status", "value", "unit", "as_of", "source"),
    "customer": ("type", "created", "status", "confidence", "review_due"),
    "experiment": ("type", "created", "status", "hypothesis"),
}
EDGE_FIELDS = ("supersedes", "evidences", "caused", "superseded_by")
ID_RE = re.compile(r"^(dec|les|met|cus|exp)-[a-z0-9][a-z0-9-]*$")
KNOWN_FIELDS = {
    "type", "created", "status", "confidence", "review_due", "value", "unit", "as_of",
    "source", "hypothesis", "result", "supersedes", "evidences", "caused",
    "superseded_by", "due", "hardened", "chose", "over", "target", "segment",
    "mrr", "since",
}


def parse_ledger(root: Path = Path(".resonance/ledger"), *, strict_files: bool = True) -> list[dict]:
    entries: list[dict] = []
    if not root.is_dir():
        return entries
    files = [root / f"{name}.md" for name in FILE_PREFIX] if strict_files else sorted(root.glob("*.md"))
    for path in files:
        if not path.is_file():
            continue
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
            duplicate_fields: list[str] = []
            while j < len(lines):
                if ENTRY_RE.match(lines[j]):
                    break
                if in_fields and not lines[j].strip():
                    in_fields = False
                    j += 1
                    continue
                fm = FIELD_RE.match(lines[j]) if in_fields else None
                if fm:
                    if fm.group(1) in fields:
                        duplicate_fields.append(fm.group(1))
                    fields[fm.group(1)] = fm.group(2).strip()
                elif lines[j].strip():
                    body.append(lines[j].strip())
                j += 1
            entries.append({
                "id": m.group(1),
                "prefix": m.group(2),
                "title": m.group(3),
                "status": fields.get("status", "active"),
                "confidence": fields.get("confidence", ""),
                "review_due": fields.get("review_due", ""),
                "fields": fields,
                "duplicate_fields": duplicate_fields,
                "body": "\n".join(body),
                "text": "\n".join([f"{k}: {v}" for k, v in sorted(fields.items())] + body),
                "source": path.name,
                "line": i + 1,
            })
            i = j
    return entries


def load_entries(root: Path = Path(".resonance/ledger"), *, include_historical: bool = False) -> list[dict]:
    errors, _warnings = validate_ledger(root)
    if errors:
        return []
    entries = parse_ledger(root)
    if include_historical:
        return sorted(entries, key=entry_rank)
    superseded_by = {
        target.strip()
        for entry in entries
        for target in entry.get("fields", {}).get("supersedes", "").split(",")
        if target.strip()
    }
    current = [
        e for e in entries
        if e.get("status") != "superseded" and e["id"] not in superseded_by
    ]
    return sorted(current, key=entry_rank)


def entry_rank(entry: dict) -> tuple[int, int, str]:
    status_score = {"active": 0, "closed": 1, "superseded": 2}.get(entry.get("status", ""), 3)
    confidence_score = {"high": 0, "medium": 1, "low": 2, "": 3}.get(entry.get("confidence", ""), 3)
    review_due = entry.get("review_due") or "9999-12-31"
    return (status_score, confidence_score, review_due)


def active_entries(root: Path = Path(".resonance/ledger")) -> list[dict]:
    return load_entries(root, include_historical=False)


def split_edges(raw: str) -> list[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


def is_iso_date(value: str) -> bool:
    try:
        _dt.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def file_schema(path: Path) -> tuple[int | None, bool]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for line in lines[:6]:
        m = SCHEMA_RE.match(line.strip())
        if m:
            return int(m.group(1)), True
    return None, False


def validate_ledger(root: Path = Path(".resonance/ledger")) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not root.is_dir():
        return errors, warnings

    allowed = {f"{name}.md" for name in FILE_PREFIX}
    for rogue in sorted(root.glob("*.md")):
        if rogue.name not in allowed:
            errors.append(f"ledger: unexpected file .resonance/ledger/{rogue.name}")

    all_entries: dict[str, dict] = {}
    referenced: list[tuple[str, str, str]] = []
    for fname, prefix in sorted(FILE_PREFIX.items()):
        path = root / f"{fname}.md"
        if not path.is_file():
            errors.append(f"ledger: missing file .resonance/ledger/{fname}.md")
            continue
        version, has_marker = file_schema(path)
        if not has_marker:
            errors.append(f"ledger: {fname}.md missing 'schema: resonance-ledger/N' marker")
        elif version and version > VERSION_MAX:
            errors.append(
                f"ledger: {fname}.md schema version {version} is newer than this "
                f"framework knows ({VERSION_MAX}); upgrade the framework"
            )
        schema_version = version or 1
        etype = TYPE_BY_PREFIX[prefix]
        for entry in [e for e in parse_ledger(root) if e["source"] == f"{fname}.md"]:
            loc = f"ledger/{fname}.md:{entry['line']}"
            eid = entry["id"]
            fields = entry["fields"]
            if not entry["title"].strip():
                errors.append(f"ledger: '{eid}' title must not be empty ({loc})")
            if schema_version >= 2 and not entry.get("body", "").strip():
                errors.append(f"ledger: '{eid}' body must not be empty ({loc})")
            for dup in entry.get("duplicate_fields", []):
                errors.append(f"ledger: '{eid}' duplicate field '{dup}' ({loc})")
            for key, value in fields.items():
                if schema_version >= 2 and key not in KNOWN_FIELDS:
                    errors.append(f"ledger: '{eid}' unknown field '{key}' ({loc})")
                if not value.strip():
                    errors.append(f"ledger: '{eid}' field '{key}' must not be empty ({loc})")
            if not ID_RE.match(eid):
                errors.append(f"ledger: bad id '{eid}' ({loc})")
            if entry["prefix"] != prefix:
                errors.append(
                    f"ledger: '{eid}' is a {TYPE_BY_PREFIX[entry['prefix']]} entry in "
                    f"{fname}.md (belongs in {entry['prefix']} file) ({loc})"
                )
            if eid in all_entries:
                errors.append(f"ledger: duplicate id '{eid}' ({loc})")
            required = REQUIRED_V2[etype] if schema_version >= 2 else REQUIRED_V1[etype]
            for req in required:
                if req not in fields:
                    errors.append(f"ledger: '{eid}' missing required field '{req}' ({loc})")
            if fields.get("type") and fields["type"] != etype:
                errors.append(f"ledger: '{eid}' type '{fields['type']}' should be '{etype}' ({loc})")
            status = fields.get("status")
            if status and status not in STATUS:
                errors.append(f"ledger: '{eid}' status '{status}' not in {sorted(STATUS)} ({loc})")
            for datef in ("created", "as_of", "due", "review_due"):
                if fields.get(datef) and not is_iso_date(fields[datef]):
                    errors.append(f"ledger: '{eid}' {datef} '{fields[datef]}' is not an ISO date ({loc})")
            if "confidence" in fields and fields["confidence"] not in {"low", "medium", "high"}:
                errors.append(
                    f"ledger: '{eid}' confidence '{fields['confidence']}' is not low, medium, or high ({loc})"
                )
            if etype == "experiment" and status == "closed" and "result" not in fields:
                errors.append(f"ledger: closed experiment '{eid}' missing 'result' ({loc})")
            for edge in EDGE_FIELDS:
                if edge in fields:
                    for target in split_edges(fields[edge]):
                        referenced.append((eid, edge, target))
            entry["_loc"] = loc
            all_entries[eid] = entry

    for src, field, target in referenced:
        if target not in all_entries:
            errors.append(f"ledger: '{src}' {field} points at missing id '{target}'")
    for eid, entry in all_entries.items():
        supersedes = entry["fields"].get("supersedes")
        if not supersedes:
            continue
        for old_id in split_edges(supersedes):
            old = all_entries.get(old_id)
            if not old:
                continue
            if old["fields"].get("status") != "superseded":
                errors.append(
                    f"ledger: '{eid}' supersedes '{old_id}' but it is not "
                    f"status:superseded ({old['_loc']})"
                )
            if old["fields"].get("superseded_by") != eid:
                errors.append(
                    f"ledger: '{old_id}' missing 'superseded_by: {eid}' back-ref "
                    f"({old['_loc']})"
                )
    return errors, warnings
