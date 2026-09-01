#!/usr/bin/env python3
"""Validate a search operating-cycle contract or report with stdlib only."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path


CATEGORIES = {
    "Product Correctness",
    "Runtime Safety",
    "Authorization Integrity",
    "Data Integrity",
    "Environment Robustness",
    "Verification Quality",
    "Maintainability",
}
SEVERITIES = {"P0", "P1", "P2", "P3"}
STATES = {"clean", "candidate", "finding", "rejected", "fixed", "skipped", "incomplete"}
EVIDENCE_STATES = {"complete", "partial", "stale", "missing", "unavailable"}
INDIVIDUAL_FIELD_MARKERS = {"email", "person", "phone", "contact", "owner_name", "individual"}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def individual_field_paths(value: object, path: str = "root") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower()
            if normalized in INDIVIDUAL_FIELD_MARKERS or normalized.endswith("_email"):
                found.append(f"{path}.{key}")
            found.extend(individual_field_paths(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(individual_field_paths(child, f"{path}[{index}]"))
    return found


def validate_dates(window: object, errors: list[str]) -> None:
    require(isinstance(window, dict), "comparison_window must be an object", errors)
    if not isinstance(window, dict):
        return
    values: dict[str, date] = {}
    for field in ("current_start", "current_end", "prior_start", "prior_end"):
        raw = window.get(field)
        try:
            values[field] = date.fromisoformat(raw)
        except (TypeError, ValueError):
            errors.append(f"comparison_window.{field} must be an ISO date")
    if len(values) == 4:
        require(values["current_start"] <= values["current_end"], "current window is reversed", errors)
        require(values["prior_start"] <= values["prior_end"], "prior window is reversed", errors)


def validate_contract(data: dict[str, object], errors: list[str]) -> None:
    registry = data.get("property_registry")
    require(isinstance(registry, list) and bool(registry), "property_registry must be a non-empty list", errors)
    if isinstance(registry, list):
        for index, item in enumerate(registry):
            require(isinstance(item, dict), f"property_registry[{index}] must be an object", errors)
            if not isinstance(item, dict):
                continue
            require(bool(item.get("property_id")), f"property_registry[{index}].property_id is required", errors)
            require(bool(item.get("property_uri")), f"property_registry[{index}].property_uri is required", errors)
            require(bool(item.get("owner_role")), f"property_registry[{index}].owner_role is required", errors)
            require("owner_name" not in item and "email" not in item, f"property_registry[{index}] must use a role, not individual information", errors)
    for field in ("cadence", "timezone", "credential_reference"):
        require(isinstance(data.get(field), str) and bool(data.get(field)), f"{field} is required", errors)
    credential = data.get("credential_reference")
    if isinstance(credential, str):
        require("token=" not in credential.lower() and "password=" not in credential.lower(), "credential_reference must not contain a credential value", errors)
    destination = data.get("artifact_destination")
    require(isinstance(destination, dict), "artifact_destination must be an object", errors)
    if isinstance(destination, dict):
        kind = destination.get("kind")
        require(kind in {"private", "repository"}, "artifact_destination.kind must be private or repository", errors)
        require(bool(destination.get("path")), "artifact_destination.path is required", errors)
        if kind == "repository":
            require(data.get("repository_write_approved") is True, "repository destination requires repository_write_approved: true", errors)
    require("previous_run" in data, "previous_run is required and may be null", errors)
    validate_dates(data.get("comparison_window"), errors)


def validate_report(data: dict[str, object], errors: list[str]) -> None:
    findings = data.get("findings")
    coverage = data.get("property_outcomes")
    scoped = data.get("scoped_property_ids")
    require(isinstance(findings, list), "findings must be a list", errors)
    require(isinstance(scoped, list) and bool(scoped), "scoped_property_ids must be a non-empty list", errors)
    require(isinstance(coverage, list) and bool(coverage), "property_outcomes must be a non-empty list", errors)
    outcome_ids: list[str] = []
    if isinstance(coverage, list):
        for index, outcome in enumerate(coverage):
            require(isinstance(outcome, dict), f"property_outcomes[{index}] must be an object", errors)
            if isinstance(outcome, dict):
                property_id = outcome.get("property_id")
                require(isinstance(property_id, str) and bool(property_id), f"property_outcomes[{index}].property_id is required", errors)
                if isinstance(property_id, str) and property_id:
                    outcome_ids.append(property_id)
                require(outcome.get("state") in STATES, f"property_outcomes[{index}].state is not canonical", errors)
                require(outcome.get("evidence_state") in EVIDENCE_STATES, f"property_outcomes[{index}].evidence_state is not canonical", errors)
    if isinstance(scoped, list) and all(isinstance(item, str) and item for item in scoped):
        require(len(scoped) == len(set(scoped)), "scoped_property_ids must be unique", errors)
        require(len(outcome_ids) == len(set(outcome_ids)), "property_outcomes property_id values must be unique", errors)
        require(set(outcome_ids) == set(scoped), "property_outcomes must cover every scoped_property_id exactly once", errors)
    if not isinstance(findings, list):
        return
    for index, finding in enumerate(findings):
        require(isinstance(finding, dict), f"findings[{index}] must be an object", errors)
        if not isinstance(finding, dict):
            continue
        require(finding.get("category") in CATEGORIES, f"findings[{index}].category is not canonical", errors)
        require(finding.get("severity") in SEVERITIES, f"findings[{index}].severity must be P0-P3", errors)
        require(finding.get("state") in STATES, f"findings[{index}].state is not canonical", errors)
        for field in ("property_id", "evidence_reference", "harm", "recommended_action", "owner_role", "verification_method"):
            require(bool(finding.get(field)), f"findings[{index}].{field} is required", errors)
        if finding.get("kind") == "cannibalization" and finding.get("state") == "finding":
            dimensions = finding.get("dimensions")
            require(isinstance(dimensions, list) and {"query", "page"}.issubset(dimensions), f"findings[{index}] cannibalization requires joint query-page dimensions", errors)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_search_run.py <contract-or-report.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read {path}: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("ERROR: root must be a JSON object", file=sys.stderr)
        return 1
    errors: list[str] = []
    for individual_path in individual_field_paths(data):
        errors.append(f"individual information field is not allowed: {individual_path}")
    document_type = data.get("document_type")
    if document_type == "search_run_contract":
        validate_contract(data, errors)
    elif document_type == "search_run_report":
        validate_report(data, errors)
    else:
        errors.append("document_type must be search_run_contract or search_run_report")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {document_type} is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
