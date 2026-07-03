#!/usr/bin/env python3
"""
Resonance - Decision Log (R6).

An append-only, event-sourced record of settled decisions, so the agent never
re-litigates a call it already made (Zero Divergence). Superseded decisions are
marked, not deleted, so there is an audit trail. Stored as one JSON object per
line at .resonance/decisions.jsonl. Pure stdlib, cross-platform.

Usage:
  python .forge/decisions.py add "Use Postgres over SQLite" --why "need concurrent writes" --files db/schema.sql
  python .forge/decisions.py list                 # active decisions (resurface at session start)
  python .forge/decisions.py list --all           # include superseded/redacted
  python .forge/decisions.py search "auth"        # lexical search
  python .forge/decisions.py supersede d3 "Move to RS256 for external APIs" --why "HS256 shared-secret risk"
  python .forge/decisions.py redact d5            # mark a decision redacted (e.g. contained a secret)

Skills that read memory should `list` at session start and `search` before
re-opening a settled question.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

STORE = Path(".resonance") / "decisions.jsonl"


def _load() -> list[dict]:
    if not STORE.exists():
        return []
    out = []
    for line in STORE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def _append(rec: dict) -> None:
    STORE.parent.mkdir(parents=True, exist_ok=True)
    with STORE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _next_id(recs: list[dict]) -> str:
    n = 0
    for r in recs:
        m = re.match(r"d(\d+)$", r.get("id", ""))
        if m:
            n = max(n, int(m.group(1)))
    return f"d{n + 1}"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _print(rec: dict) -> None:
    tag = {"active": "", "superseded": " [superseded]", "redacted": " [redacted]"}.get(rec["status"], "")
    print(f"  {rec['id']}{tag}  {rec['decision']}")
    if rec.get("why"):
        print(f"       why: {rec['why']}")
    if rec.get("files"):
        print(f"       files: {', '.join(rec['files'])}")


def cmd_add(a) -> int:
    recs = _load()
    rec = {"id": _next_id(recs), "ts": _now(), "decision": a.decision,
           "why": a.why or "", "files": _split(a.files), "status": "active"}
    _append(rec)
    print(f"recorded {rec['id']}: {rec['decision']}")
    return 0


def cmd_list(a) -> int:
    recs = _load()
    shown = [r for r in recs if a.all or r["status"] == "active"]
    if not shown:
        print("no decisions recorded" + ("" if a.all else " (use --all to see superseded)"))
        return 0
    print(f"{'all' if a.all else 'active'} decisions ({len(shown)}):")
    for r in shown:
        _print(r)
    return 0


def cmd_search(a) -> int:
    terms = [t for t in re.split(r"\W+", a.query.lower()) if t]
    scored = []
    for r in _load():
        if r["status"] == "redacted":
            continue
        blob = (r["decision"] + " " + r.get("why", "") + " " + " ".join(r.get("files", []))).lower()
        score = sum(blob.count(t) for t in terms)
        if score:
            scored.append((score, r))
    scored.sort(key=lambda x: -x[0])
    if not scored:
        print(f"no decisions match '{a.query}'")
        return 0
    print(f"decisions matching '{a.query}':")
    for _, r in scored[:a.k]:
        _print(r)
    return 0


def cmd_supersede(a) -> int:
    recs = _load()
    target = next((r for r in recs if r["id"] == a.id), None)
    if not target:
        print(f"no decision '{a.id}'")
        return 1
    target["status"] = "superseded"
    STORE.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in recs) + "\n", encoding="utf-8")
    new = {"id": _next_id(recs), "ts": _now(), "decision": a.decision, "why": a.why or "",
           "files": _split(a.files), "status": "active", "supersedes": a.id}
    _append(new)
    print(f"{a.id} superseded by {new['id']}: {new['decision']}")
    return 0


def cmd_redact(a) -> int:
    recs = _load()
    hit = False
    for r in recs:
        if r["id"] == a.id:
            r["status"], r["decision"], r["why"], r["files"] = "redacted", "[redacted]", "", []
            hit = True
    if not hit:
        print(f"no decision '{a.id}'")
        return 1
    STORE.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in recs) + "\n", encoding="utf-8")
    print(f"{a.id} redacted")
    return 0


def _split(v: str | None) -> list[str]:
    return [x.strip() for x in v.split(",")] if v else []


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Resonance decision log.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add"); p.add_argument("decision"); p.add_argument("--why"); p.add_argument("--files")
    p = sub.add_parser("list"); p.add_argument("--all", action="store_true")
    p = sub.add_parser("search"); p.add_argument("query"); p.add_argument("--k", type=int, default=8)
    p = sub.add_parser("supersede"); p.add_argument("id"); p.add_argument("decision"); p.add_argument("--why"); p.add_argument("--files")
    p = sub.add_parser("redact"); p.add_argument("id")
    a = ap.parse_args(argv)
    return {"add": cmd_add, "list": cmd_list, "search": cmd_search,
            "supersede": cmd_supersede, "redact": cmd_redact}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
