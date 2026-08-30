#!/usr/bin/env python3
"""Compile skill-level composition declarations into job contracts."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from kernel.manifest import artifact_rights
from schema_check import load_schema, validate


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "docs" / "skill-manifest.json"
OUTPUT = ROOT / "docs" / "job-compositions.json"


def validate_invariants(contract: dict[str, Any]) -> None:
    participants = [contract["lead"], *contract["contributors"], *contract["reviewers"]]
    if len(participants) != len(set(participants)):
        raise ValueError(f"{contract['job_id']}: a skill has conflicting composition roles")
    actors = {row["actor"] for row in contract["artifact_access"]}
    missing_access = sorted(set(participants) - actors)
    if missing_access:
        raise ValueError(
            f"{contract['job_id']}: participants have no artifact access: "
            + ", ".join(missing_access)
        )
    if contract["finalizer"] != contract["lead"]:
        raise ValueError(f"{contract['job_id']}: only the declared lead may finalize v1 jobs")
    semantic = set(contract["authority_split"]["frontmatter_owns"])
    presentation = set(contract["authority_split"]["command_registry_owns"])
    if semantic & presentation:
        raise ValueError(f"{contract['job_id']}: semantic and presentation authority overlap")


def _access_rows(entry: dict[str, Any]) -> list[dict[str, Any]]:
    parsed, issues = artifact_rights(entry.get("artifact_access", []))
    if issues:
        raise ValueError(f"{entry['id']}: {'; '.join(issues)}")
    return [
        {"artifact": artifact, "actor": entry["id"], "rights": sorted(right.upper() for right in rights)}
        for artifact, rights in sorted(parsed.items())
    ]


def compile_contracts(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    owners: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in manifest:
        if entry.get("job_id"):
            owners[str(entry["job_id"])].append(entry)
    duplicate = sorted(job for job, entries in owners.items() if len(entries) != 1)
    if duplicate:
        raise ValueError("multiple lead skills declare job(s): " + ", ".join(duplicate))

    by_id = {entry["id"]: entry for entry in manifest}
    contracts: list[dict[str, Any]] = []
    authority_split = {
        "frontmatter_owns": [
            "skill_identity", "owner", "activation", "authority", "side_effects",
            "entrypoints", "inputs", "outputs", "invocation_relationships", "failure_policy",
        ],
        "command_registry_owns": [
            "command_name", "aliases", "target_skill_id", "host_exposure", "help_text", "host_rendering",
        ],
        "conflict_behavior": "FAIL",
    }
    compatibility = {
        "supported_versions": [1], "unknown_version": "FAIL_CLOSED", "mixed_version": "REJECT",
        "upgrade": "EXPLICIT_MIGRATION_REQUIRED", "downgrade": "NOT_SUPPORTED",
    }
    for job_id, entries in sorted(owners.items()):
        lead = entries[0]
        contributors = sorted(
            item["id"] for item in manifest if job_id in item.get("contributes_to", [])
        )
        reviewers = sorted(item["id"] for item in manifest if job_id in item.get("reviews", []))
        participants = [lead["id"], *contributors, *reviewers]
        access = []
        for participant in participants:
            access.extend(_access_rows(by_id[participant]))
        contract = {
            "schema_version": 1,
            "contract_version": 1,
            "job_id": job_id,
            "stage": lead["stage"],
            "lead": lead["id"],
            "contributors": contributors,
            "reviewers": reviewers,
            "finalizer": lead["id"],
            "artifact_access": access,
            "dispatch_conditions": lead.get("dispatch_conditions", []),
            "compatibility": compatibility,
            "authority_split": authority_split,
        }
        validate(contract, load_schema("composition-contract.schema.json"))
        validate_invariants(contract)
        contracts.append(contract)
    return contracts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload = json.dumps(compile_contracts(manifest), indent=2) + "\n"
    output = args.output.resolve()
    if args.check:
        if not output.is_file() or output.read_text(encoding="utf-8") != payload:
            print(f"job composition output is stale: {output}")
            return 1
        print(f"job composition output is current: {output}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(payload, encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
