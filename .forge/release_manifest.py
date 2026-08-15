#!/usr/bin/env python3
"""Create a deterministic release manifest with committed-file checksums."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path


def run(args: list[str]) -> str:
    return subprocess.check_output(args, text=True, encoding="utf-8", errors="replace").strip()


def committed_files(commit: str) -> dict[str, bytes]:
    archive = subprocess.check_output(["git", "archive", "--format=tar", commit])
    files: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tf:
        for member in tf.getmembers():
            if not member.isfile():
                continue
            stream = tf.extractfile(member)
            if stream is None:
                continue
            files[member.name] = stream.read()
    return dict(sorted(files.items()))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Write release manifest JSON and SHA256SUMS.")
    ap.add_argument("--output", default="dist/release-manifest.json")
    ap.add_argument("--checksums", default="dist/SHA256SUMS")
    args = ap.parse_args(argv)

    out = Path(args.output)
    sums = Path(args.checksums)
    out.parent.mkdir(parents=True, exist_ok=True)
    sums.parent.mkdir(parents=True, exist_ok=True)

    commit = run(["git", "rev-parse", "HEAD"])
    commit_time = run(["git", "show", "-s", "--format=%cI", commit])
    committed = committed_files(commit)
    files = []
    checksum_lines = []
    for rel, blob in committed.items():
        digest = hashlib.sha256(blob).hexdigest()
        files.append({"path": rel, "sha256": digest, "bytes": len(blob)})
        checksum_lines.append(f"{digest}  {rel}")

    package = json.loads(committed["package.json"].decode("utf-8"))
    manifest = {
        "schema_version": 1,
        "version": package["version"],
        "commit": commit,
        "created_at": commit_time,
        "source": "git-commit-tree",
        "tracked_file_count": len(files),
        "tree_hash": hashlib.sha256(
            "\n".join(f"{f['path']}\0{f['sha256']}" for f in files).encode("utf-8")
        ).hexdigest(),
        "files": files,
    }
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    sums.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    print(f"wrote {out} and {sums} ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
