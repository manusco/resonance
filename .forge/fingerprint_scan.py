#!/usr/bin/env python3
"""
Resonance Forge - Fingerprint Scan.

Scans changed public files for source markers and, when a private corpus is
configured through RESONANCE_PRIVATE_CORPUS, distinctive phrase overlap.

Usage:
    python .forge/fingerprint_scan.py
    RESONANCE_PRIVATE_CORPUS=/path/to/private/corpus python .forge/fingerprint_scan.py

Exit: 0 clean, 1 findings, 2 bad args.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
WORD_RE = re.compile(r"[a-z0-9][a-z0-9'-]*", re.I)
SOURCE_MARKERS = re.compile(
    r"(packaged source note|source note|provenance:|attribution:|"
    r"inspired by\s+https?://|adapted from\s+https?://|ported from\s+https?://|"
    r"forked from\s+https?://|based on\s+https?://|"
    r"github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+|commit\s+[0-9a-f]{7,40})",
    re.I,
)
ALLOWED_MARKERS = (
    "github.com/manusco/resonance",
)
SCANNER_IMPLEMENTATIONS = {
    ".forge/fingerprint_scan.py",
    ".forge/validate_library.py",
}
TEXT_EXT = {
    ".md", ".txt", ".json", ".py", ".js", ".ts", ".tsx", ".jsx", ".yml", ".yaml",
    ".toml", ".sh", ".ps1", ".mjs", ".cjs", ".html", ".css"
}
SKIP_PARTS = {".git", "node_modules", ".venv", "dist", "build", "__pycache__"}
PRIVATE_AUDIT_DIRS = {"marketing-agent-integration-audit"}


def changed_files(ref: str) -> list[Path]:
    names: set[str] = set()
    cmds = [
        ["git", "diff", "--name-only", ref],
        ["git", "diff", "--name-only", "--cached"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode == 0:
            names.update(x.strip() for x in r.stdout.splitlines() if x.strip())
    out = []
    for name in sorted(names):
        p = REPO / name
        if p.is_file() and is_text_path(p):
            out.append(p)
    return out


def is_text_path(path: Path) -> bool:
    if any(part in SKIP_PARTS for part in path.parts):
        return False
    return path.suffix.lower() in TEXT_EXT


def read_text(path: Path) -> str:
    try:
        if path.stat().st_size > 2_000_000:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def old_lines(path: Path, ref: str) -> set[str]:
    rp = rel(path)
    r = subprocess.run(["git", "show", f"{ref}:{rp}"], cwd=str(REPO),
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if r.returncode != 0:
        return set()
    return set(r.stdout.splitlines())


def new_text(path: Path, ref: str) -> str:
    previous = old_lines(path, ref)
    return "\n".join(line for line in read_text(path).splitlines() if line not in previous)


def words(text: str) -> list[str]:
    return [m.group(0).lower() for m in WORD_RE.finditer(text)]


def phrases(text: str, n: int) -> set[str]:
    ws = words(text)
    return {" ".join(ws[i:i + n]) for i in range(0, max(0, len(ws) - n + 1))}


def corpus_overlap(root: Path, targets: set[str], n: int, max_files: int) -> str | None:
    if shutil.which("rg") and targets:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tf:
            tf.write("\n".join(sorted(targets)))
            tf.write("\n")
            pattern_file = tf.name
        try:
            r = subprocess.run(
                [
                    "rg", "-I", "-F", "-f", pattern_file,
                    "--glob", "!**/node_modules/**",
                    "--glob", "!**/.git/**",
                    "--glob", "!**/marketing-agent-integration-audit/**",
                    str(root),
                ],
                cwd=str(REPO), capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=120,
            )
            if r.returncode == 0:
                return (r.stdout.splitlines() or ["match found"])[0]
            if r.returncode == 1:
                return None
        finally:
            try:
                Path(pattern_file).unlink()
            except OSError:
                pass

    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if d not in SKIP_PARTS and d not in PRIVATE_AUDIT_DIRS
        ]
        for fname in filenames:
            if count >= max_files:
                return None
            p = Path(dirpath) / fname
            if not is_text_path(p):
                continue
            txt = read_text(p)
            if not txt:
                continue
            ws = words(txt)
            for i in range(0, max(0, len(ws) - n + 1)):
                ph = " ".join(ws[i:i + n])
                if ph in targets:
                    return ph
            count += 1
    return None


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO).as_posix()
    except ValueError:
        return path.as_posix()


def is_scanner_definition(path: Path, line: str) -> bool:
    if rel(path) not in SCANNER_IMPLEMENTATIONS:
        return False
    return "SOURCE_MARKERS" in line or "PROVENANCE" in line or "r\"" in line or "r'" in line


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Scan changed files for source fingerprints.")
    ap.add_argument("--ref", default="HEAD", help="Git ref to compare against")
    ap.add_argument("--min-words", type=int, default=10, help="minimum phrase length")
    ap.add_argument("--max-corpus-files", type=int, default=50000,
                    help="maximum private corpus text files to index")
    args = ap.parse_args(argv)

    files = changed_files(args.ref)
    findings: list[str] = []

    for p in files:
        text = read_text(p)
        previous = old_lines(p, args.ref)
        for ln_no, line in enumerate(text.splitlines(), 1):
            if line in previous:
                continue
            if (SOURCE_MARKERS.search(line)
                    and not any(a in line.lower() for a in ALLOWED_MARKERS)
                    and not is_scanner_definition(p, line)):
                findings.append(f"source marker: {rel(p)}:{ln_no}")

    corpus_env = os.environ.get("RESONANCE_PRIVATE_CORPUS", "").strip()
    if corpus_env:
        corpus = Path(corpus_env)
        if not corpus.is_dir():
            print(f"fingerprint: private corpus not found: {corpus}")
            return 2
        changed_phrases: set[str] = set()
        phrase_owner: dict[str, str] = {}
        for p in files:
            for ph in phrases(new_text(p, args.ref), args.min_words):
                changed_phrases.add(ph)
                phrase_owner.setdefault(ph, rel(p))
        hit = corpus_overlap(corpus, changed_phrases, args.min_words, args.max_corpus_files)
        if hit:
            findings.append(f"private phrase overlap: {phrase_owner.get(hit, '(changed file)')} "
                            f"-> '{hit[:120]}'")

    print(f"fingerprint scan: {len(files)} changed text file(s)")
    for f in findings:
        print(f"  ERROR  {f}")
    print(f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
