#!/usr/bin/env python3
"""Fail-closed promotion verdicts from immutable evidence manifests."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parent.parent
PRECEDENCE = [
    "EVIDENCE_INTEGRITY", "SAFETY_AUTHORITY", "COMPATIBILITY",
    "TRACE_ASSURANCE", "STRUCTURAL_INTEGRITY", "ROUTING_HARM",
    "DECLARED_METRICS", "TASK_QUALITY", "COST_LATENCY",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def git_state(repo: Path) -> tuple[str, bool, list[str]]:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=30)
    status = subprocess.run(["git", "status", "--porcelain=v1"], cwd=repo,
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=30)
    if head.returncode or status.returncode:
        raise ValueError("cannot verify current repository identity")
    changed = sorted(line[3:].replace("\\", "/") for line in status.stdout.splitlines() if line)
    return head.stdout.strip().lower(), bool(changed), changed


def verdict(candidate_id: str, manifests: list[Path], *, repo: Path = REPO,
            max_age_hours: int = 168, allow_dirty: bool = False,
            required_kinds: set[str] | None = None) -> dict[str, Any]:
    required = required_kinds or {"structural", "routing_public", "routing_protected", "orchestration"}
    reasons: dict[str, list[str]] = {gate: [] for gate in PRECEDENCE}
    loaded: list[tuple[Path, dict[str, Any]]] = []
    now = datetime.now(timezone.utc)
    for path in manifests:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("schema_version") != 1:
                raise ValueError("unsupported evidence schema")
            if data.get("exit_state") != "COMPLETE":
                reasons["EVIDENCE_INTEGRITY"].append(f"{path.name}: run is {data.get('exit_state', 'missing')}")
            age = (now - utc(data["ended_at"])).total_seconds() / 3600
            if age < 0 or age > max_age_hours:
                reasons["EVIDENCE_INTEGRITY"].append(f"{path.name}: evidence age {age:.1f}h exceeds {max_age_hours}h")
            loaded.append((path, data))
        except Exception as exc:
            reasons["EVIDENCE_INTEGRITY"].append(f"{path}: {exc}")

    if not loaded:
        reasons["EVIDENCE_INTEGRITY"].append("no readable evidence manifests")
    current_sha, current_dirty, current_paths = git_state(repo)
    kinds: set[str] = set()
    for path, data in loaded:
        repository = data.get("repository", {})
        if repository.get("git_sha") != current_sha:
            reasons["EVIDENCE_INTEGRITY"].append(f"{path.name}: git SHA does not match current tree")
        if not allow_dirty and (current_dirty or repository.get("dirty")):
            reasons["EVIDENCE_INTEGRITY"].append("dirty tree is not allowed for promotion")
        if allow_dirty and sorted(repository.get("changed_paths", [])) != current_paths:
            reasons["EVIDENCE_INTEGRITY"].append(f"{path.name}: changed paths do not match current tree")
        summary = data.get("summary", {})
        kind = summary.get("evidence_kind")
        if isinstance(kind, str):
            kinds.add(kind)
        for gate in PRECEDENCE[1:]:
            state = summary.get("gates", {}).get(gate)
            if state in {"FAIL", "REJECT"}:
                reasons[gate].append(f"{path.name}: {gate} failed")
            elif state in {"INCOMPLETE", "INCONCLUSIVE"}:
                reasons[gate].append(f"{path.name}: {gate} is {state.lower()}")

    missing = sorted(required - kinds)
    if missing:
        reasons["EVIDENCE_INTEGRITY"].append("missing evidence kinds: " + ", ".join(missing))

    failed_gate = next((gate for gate in PRECEDENCE if reasons[gate]), None)
    flat = [reason for gate in PRECEDENCE for reason in reasons[gate]]
    if failed_gate is None:
        outcome = "PROMOTE"
    elif any("failed" in reason or "REJECT" in reason for reason in reasons[failed_gate]):
        outcome = "REJECT"
    else:
        outcome = "INCOMPLETE"
    aggregate_hash = hashlib.sha256("".join(sorted(digest(p) for p, _ in loaded)).encode()).hexdigest()
    return {
        "schema_version": 1,
        "candidate_id": candidate_id,
        "evidence_manifest_hash": aggregate_hash,
        "evaluated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "outcome": outcome,
        "precedence": PRECEDENCE,
        "failed_gate": failed_gate,
        "reasons": flat or ["all required promotion gates passed"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--manifest", action="append", default=[])
    parser.add_argument("--max-age-hours", type=int, default=168)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    result = verdict(args.candidate_id, [Path(p).resolve() for p in args.manifest],
                     max_age_hours=args.max_age_hours, allow_dirty=args.allow_dirty)
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8", newline="\n")
    else:
        print(payload, end="")
    return {"PROMOTE": 0, "REJECT": 1, "INCOMPLETE": 2, "INCONCLUSIVE": 2}[result["outcome"]]


if __name__ == "__main__":
    raise SystemExit(main())
