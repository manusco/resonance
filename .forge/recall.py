#!/usr/bin/env python3
"""
Resonance - Memory Recall (R6).

Retrieve the most relevant slices of project memory by meaning, instead of
loading whole files. Sources: .resonance/*.md, .resonance/learnings.jsonl, and
active entries in .resonance/decisions.jsonl, PLUS a cross-project brain
(~/.resonance, or $RESONANCE_GLOBAL_BRAIN) so a learning earned in one repo
raises the floor in the next. The agent should recall before a task instead of
reading the entire brain. Use --local-only to skip the global brain.

Default retriever is a pure-stdlib BM25 (works offline, no dependency, no key).
It is pluggable: set RESONANCE_EMBED_CMD to a command that reads text on stdin
and prints a JSON vector, and recall will rank by cosine similarity instead.
Lexical is the default so a fresh clone works with nothing installed.

Usage:
  python .forge/recall.py "what did we decide about auth"
  python .forge/recall.py "database choice" --k 3
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RES = Path(".resonance")
TOKEN = re.compile(r"[a-z0-9_]+")


def tok(s: str) -> list[str]:
    return TOKEN.findall(s.lower())


def _scan(base: Path, prefix: str) -> list[tuple[str, str]]:
    """Return (source_label, text) chunks from one memory bank."""
    out: list[tuple[str, str]] = []
    if not base.exists():
        return out
    for md in sorted(base.glob("*.md")):
        text = md.read_text(encoding="utf-8", errors="replace")
        # split on level-2/3 headings; keep the heading with its body
        parts = re.split(r"\n(?=#{2,3}\s)", text)
        for p in parts:
            p = p.strip()
            if len(p) > 30:
                head = p.splitlines()[0].lstrip("# ").strip()[:60]
                out.append((f"{prefix}{md.name}:{head}", p))
    lj = base / "learnings.jsonl"
    if lj.exists():
        for line in lj.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line:
                try:
                    d = json.loads(line)
                    out.append((f"{prefix}learnings.jsonl", json.dumps(d, ensure_ascii=False)))
                except json.JSONDecodeError:
                    out.append((f"{prefix}learnings.jsonl", line))
    dj = base / "decisions.jsonl"
    if dj.exists():
        for line in dj.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                if d.get("status") == "active":
                    out.append((f"{prefix}decisions.jsonl:{d.get('id','')}",
                                d.get("decision", "") + " " + d.get("why", "")))
            except json.JSONDecodeError:
                pass
    return out


def global_brain() -> Path:
    return Path(os.environ.get("RESONANCE_GLOBAL_BRAIN", str(Path.home() / ".resonance")))


def chunks(include_global: bool = True) -> list[tuple[str, str]]:
    """Local project memory, plus the cross-project brain so a learning from
    another repo raises the floor here. Global brain is ~/.resonance (or
    $RESONANCE_GLOBAL_BRAIN); local entries appear first, so they rank first on ties."""
    out = _scan(RES, "")
    if include_global:
        g = global_brain()
        try:
            same = g.resolve() == RES.resolve()
        except Exception:
            same = False
        if not same:
            out += _scan(g, "global:")
    return out


def bm25(query: str, docs: list[str], k1: float = 1.5, b: float = 0.75) -> list[float]:
    toks = [tok(d) for d in docs]
    N = len(toks) or 1
    avg = sum(len(t) for t in toks) / N
    df: Counter = Counter()
    for t in toks:
        for w in set(t):
            df[w] += 1
    q = tok(query)
    scores = []
    for t in toks:
        tf = Counter(t)
        s = 0.0
        for w in q:
            if w not in tf:
                continue
            idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
            s += idf * (tf[w] * (k1 + 1)) / (tf[w] + k1 * (1 - b + b * len(t) / (avg or 1)))
        scores.append(s)
    return scores


def embed_rank(query: str, docs: list[str], cmd: str) -> list[float] | None:
    import shlex
    def vec(text: str) -> list[float] | None:
        try:
            r = subprocess.run(shlex.split(cmd), input=text, capture_output=True, text=True, timeout=60)
            m = re.search(r"\[[^\]]*\]", r.stdout)
            return json.loads(m.group(0)) if m else None
        except Exception:
            return None
    qv = vec(query)
    if not qv:
        return None
    def cos(a, bb):
        num = sum(x * y for x, y in zip(a, bb))
        da = math.sqrt(sum(x * x for x in a)); db = math.sqrt(sum(y * y for y in bb))
        return num / (da * db) if da and db else 0.0
    out = []
    for d in docs:
        dv = vec(d)
        out.append(cos(qv, dv) if dv else 0.0)
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Recall project memory by meaning.")
    ap.add_argument("query")
    ap.add_argument("--k", type=int, default=5)
    a = ap.parse_args(argv)

    if not RES.exists():
        print("no .resonance/ memory found. Run /init first.")
        return 0
    ch = chunks()
    if not ch:
        print(".resonance/ is empty. Nothing to recall yet.")
        return 0
    docs = [c[1] for c in ch]
    cmd = os.environ.get("RESONANCE_EMBED_CMD", "")
    scores = (embed_rank(a.query, docs, cmd) if cmd else None) or bm25(a.query, docs)
    ranked = sorted(zip(scores, ch), key=lambda x: -x[0])
    hits = [(s, c) for s, c in ranked if s > 0][:a.k]
    if not hits:
        print(f"nothing in memory matches '{a.query}'")
        return 0
    print(f"recall for '{a.query}' (top {len(hits)}):\n")
    for s, (label, text) in hits:
        snippet = " ".join(text.split())[:280]
        print(f"[{label}]  (score {s:.2f})")
        print(f"  {snippet}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
