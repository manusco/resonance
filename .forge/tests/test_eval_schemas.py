import copy
import json
import re
import unittest
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / ".forge" / "schemas"
HEX = "a" * 64
NOW = "2026-08-23T12:00:00Z"


class SchemaFailure(ValueError):
    pass


def _resolve(schema, root):
    ref = schema.get("$ref")
    if not ref:
        return schema
    if not ref.startswith("#/"):
        raise SchemaFailure(f"unsupported reference: {ref}")
    node = root
    for part in ref[2:].split("/"):
        node = node[part]
    return node


def validate(instance, schema, root=None, path="$"):
    root = root or schema
    schema = _resolve(schema, root)
    for branch in schema.get("allOf", []):
        validate(instance, branch, root, path)
    if "if" in schema:
        try:
            validate(instance, schema["if"], root, path)
            condition_matches = True
        except SchemaFailure:
            condition_matches = False
        branch = schema.get("then") if condition_matches else schema.get("else")
        if branch is not None:
            validate(instance, branch, root, path)
    if "not" in schema:
        try:
            validate(instance, schema["not"], root, path)
        except SchemaFailure:
            pass
        else:
            raise SchemaFailure(f"{path}: matched forbidden schema")
    if "const" in schema and instance != schema["const"]:
        raise SchemaFailure(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        raise SchemaFailure(f"{path}: unsupported value {instance!r}")

    expected = schema.get("type")
    if expected:
        expected = [expected] if isinstance(expected, str) else expected
        checks = {
            "object": lambda value: isinstance(value, dict),
            "array": lambda value: isinstance(value, list),
            "string": lambda value: isinstance(value, str),
            "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
            "number": lambda value: isinstance(value, (int, float)) and not isinstance(value, bool),
            "boolean": lambda value: isinstance(value, bool),
            "null": lambda value: value is None,
        }
        if not any(checks[kind](instance) for kind in expected):
            raise SchemaFailure(f"{path}: expected {expected}")

    if isinstance(instance, dict):
        required = schema.get("required", [])
        missing = [key for key in required if key not in instance]
        if missing:
            raise SchemaFailure(f"{path}: missing {', '.join(missing)}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = set(instance) - set(properties)
            if extra:
                raise SchemaFailure(f"{path}: unknown fields {sorted(extra)}")
        for key, value in instance.items():
            if key in properties:
                validate(value, properties[key], root, f"{path}.{key}")

    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            raise SchemaFailure(f"{path}: too few items")
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in instance}) != len(instance):
            raise SchemaFailure(f"{path}: duplicate items")
        if "items" in schema:
            for index, value in enumerate(instance):
                validate(value, schema["items"], root, f"{path}[{index}]")

    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            raise SchemaFailure(f"{path}: string is too short")
        if len(instance) > schema.get("maxLength", len(instance)):
            raise SchemaFailure(f"{path}: string is too long")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], instance):
            raise SchemaFailure(f"{path}: pattern mismatch")
        if schema.get("format") == "date-time":
            try:
                datetime.fromisoformat(instance.replace("Z", "+00:00"))
            except ValueError as exc:
                raise SchemaFailure(f"{path}: invalid date-time") from exc

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            raise SchemaFailure(f"{path}: below minimum")
        if "maximum" in schema and instance > schema["maximum"]:
            raise SchemaFailure(f"{path}: above maximum")
        if "exclusiveMinimum" in schema and instance <= schema["exclusiveMinimum"]:
            raise SchemaFailure(f"{path}: below exclusive minimum")
        if "exclusiveMaximum" in schema and instance >= schema["exclusiveMaximum"]:
            raise SchemaFailure(f"{path}: above exclusive maximum")


def load(name):
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def composition_invariants(contract):
    participants = [contract["lead"], *contract["contributors"], *contract["reviewers"]]
    if len(participants) != len(set(participants)):
        raise SchemaFailure("a skill cannot hold conflicting composition roles")
    semantic = set(contract["authority_split"]["frontmatter_owns"])
    presentation = set(contract["authority_split"]["command_registry_owns"])
    if semantic & presentation:
        raise SchemaFailure("frontmatter and command registry authority overlap")


def trace_invariants(trace):
    sequences = [event["sequence"] for event in trace["events"]]
    if sequences != list(range(1, len(sequences) + 1)):
        raise SchemaFailure("trace event sequence must be contiguous")
    required = 0
    for event in trace["events"]:
        if event["mutation_mode"] in {"WRITE", "EXTERNAL", "DESTRUCTIVE"} or event["authority"] in {"APPROVE", "PUBLISH", "EXECUTE", "DELETE"}:
            required = max(required, 2)
        if event["outcome"] == "SUCCEEDED" and event["mutation_mode"] in {"WRITE", "EXTERNAL", "DESTRUCTIVE"}:
            required = 3
    if trace["assurance_level"] < required:
        raise SchemaFailure(f"trace needs assurance level {required}")


def operating_invariants(contract):
    if contract["sampling"]["minimum_repetitions"] > contract["sampling"]["maximum_repetitions"]:
        raise SchemaFailure("minimum repetitions exceed maximum repetitions")
    paths = [dataset["path"] for dataset in contract["datasets"].values()]
    if len(paths) != len(set(paths)):
        raise SchemaFailure("dataset custody paths must be separate")


def sample_dataset(name):
    return {
        "owner": f"{name}-custodian", "path": f"D:/private/{name}", "created_at": NOW,
        "access_log": f"D:/private/{name}/access.jsonl", "hash_manifest": f"D:/private/{name}/hashes.json",
        "permitted_use": name, "reuse_count": 0, "contamination_events": [],
        "rotation_rule": "rotate after exposure", "retirement_state": "ACTIVE",
    }


def samples():
    evidence = {
        "schema_version": 1, "run_id": "run-1", "started_at": NOW, "ended_at": NOW,
        "repository": {"git_sha": HEX, "dirty": False, "changed_paths": []},
        "runner": {"id": "routing-eval", "hash": HEX}, "cases": [{"id": "case-1", "hash": HEX}],
        "skills": [{"id": "strategy/brief", "hash": HEX}], "instructions": HEX,
        "models": {"answerer_id": "answerer-1", "judge_id": "judge-1"},
        "commands": [{"id": "answerer", "hash": HEX}],
        "execution": {"repetitions": 3, "thresholds": {"accuracy": 0.95}, "host": "canary", "tool_profile": "read-only", "permission_profile": "sandbox", "cost": {"currency": "USD", "amount": 1.5}, "latency_ms": 500},
        "results": [{"id": "result-1", "hash": HEX}], "summary": {"passed": 1}, "exit_state": "COMPLETE",
    }
    routing = {
        "schema_version": 1, "id": "route.brief.1", "query": "Clarify this request", "expected_primary": "strategy/brief",
        "allowed_contributors": [], "forbidden_skills": ["strategy/council"], "harm_tier": "STANDARD", "cluster": "framing",
        "rationale": "Intent recovery precedes execution", "expected_activation_mode": "MANUAL", "ambiguity_behavior": "ROUTE",
        "deterministic_checks": [{"kind": "primary_is", "value": "strategy/brief"}],
    }
    trace = {
        "schema_version": 1, "run_id": "run-1", "assurance_level": 1,
        "events": [{"run_id": "run-1", "sequence": 1, "timestamp": NOW, "actor": "strategy/brief", "event": "INVOKE", "target": "strategy/researcher", "authority": "READ", "artifact": "evidence", "mutation_mode": "NONE", "approval_state": "NOT_REQUIRED", "outcome": "SUCCEEDED"}],
    }
    promotion = {
        "schema_version": 1, "candidate_id": "strategy/brief@1", "evidence_manifest_hash": HEX, "evaluated_at": NOW,
        "outcome": "PROMOTE", "precedence": ["EVIDENCE_INTEGRITY", "SAFETY_AUTHORITY", "COMPATIBILITY", "TRACE_ASSURANCE", "STRUCTURAL_INTEGRITY", "ROUTING_HARM", "DECLARED_METRICS", "TASK_QUALITY", "COST_LATENCY"],
        "failed_gate": None, "reasons": ["all required gates passed"],
    }
    composition = {
        "schema_version": 1, "contract_version": 1, "job_id": "framework.audit", "stage": "VERIFY", "lead": "ops/audit",
        "contributors": ["ops/security"], "reviewers": ["ops/reviewer"], "finalizer": "ops/audit",
        "artifact_access": [{"artifact": "audit-report", "actor": "ops/audit", "rights": ["CREATE", "MODIFY"]}],
        "dispatch_conditions": ["security review when trust boundary changes"],
        "compatibility": {"supported_versions": [1], "unknown_version": "FAIL_CLOSED", "mixed_version": "REJECT", "upgrade": "EXPLICIT_MIGRATION_REQUIRED", "downgrade": "NOT_SUPPORTED"},
        "authority_split": {
            "frontmatter_owns": ["skill_identity", "owner", "activation", "authority", "side_effects", "entrypoints", "inputs", "outputs", "invocation_relationships", "failure_policy"],
            "command_registry_owns": ["command_name", "aliases", "target_skill_id", "host_exposure", "help_text", "host_rendering"],
            "conflict_behavior": "FAIL",
        },
    }
    operating = {
        "schema_version": 1, "contract_id": "canary-1", "contract_version": 1,
        "approval": {"state": "APPROVED", "approver": "USER", "approved_at": NOW, "artifact_hash": HEX},
        "canary": {"host": "codex", "adapter": "codex-trace-v1", "minimum_trace_assurance": 2},
        "answerer_policy": {"model_policy": "fixed candidate", "separate_from_judge": True},
        "judge_policy": {"model_policy": "qualified independent judge", "blinded_randomized_labels": True, "response_order_reversal": True, "human_gold_calibration_set": "D:/private/gold", "agreement_threshold": 0.8, "tie_policy": "ABSTAIN", "disqualification_rule": "agreement below threshold"},
        "datasets": {name: sample_dataset(name) for name in ("public", "protected_validation", "sealed_promotion", "reserve")},
        "confidence": {"method": "Wilson interval", "level": 0.95, "abstention_target": 0.05},
        "sampling": {"rule": "SEQUENTIAL", "minimum_repetitions": 3, "maximum_repetitions": 20},
        "budgets": {"currency": "USD", "spend_ceiling": 20, "wall_clock_seconds": 3600},
        "execution": {"concurrency": 2, "retry_limit": 2, "secret_handling": "environment injection with redaction"},
        "evidence_age_days": 30,
        "failure_handling": {"outage": "INCOMPLETE", "missing_evidence": "INCOMPLETE", "budget_exhausted": "INCONCLUSIVE", "precision_unresolved": "INCONCLUSIVE"},
    }
    return {
        "evidence-manifest.schema.json": evidence,
        "routing-case.schema.json": routing,
        "invocation-trace.schema.json": trace,
        "promotion-verdict.schema.json": promotion,
        "composition-contract.schema.json": composition,
        "eval-operating-contract.schema.json": operating,
    }


class EvalSchemaTests(unittest.TestCase):
    def test_every_valid_contract_passes(self):
        for name, instance in samples().items():
            with self.subTest(name=name):
                validate(instance, load(name))
        composition_invariants(samples()["composition-contract.schema.json"])
        trace_invariants(samples()["invocation-trace.schema.json"])
        operating_invariants(samples()["eval-operating-contract.schema.json"])

    def test_missing_required_field_fails(self):
        instance = samples()["evidence-manifest.schema.json"]
        del instance["runner"]
        with self.assertRaisesRegex(SchemaFailure, "missing runner"):
            validate(instance, load("evidence-manifest.schema.json"))

    def test_routing_schema_requires_materiality_only_for_ask(self):
        schema = load("routing-case.schema.json")
        ask = dict(samples()["routing-case.schema.json"])
        ask.update({"expected_primary": None, "expected_activation_mode": "ASK",
                    "ambiguity_behavior": "ASK_MATERIAL_QUESTION"})
        with self.assertRaisesRegex(SchemaFailure, "ask_materiality"):
            validate(ask, schema)
        ask["ask_materiality"] = {
            "route_changes_primary": True,
            "possible_primary_skills": ["strategy/brief", "strategy/council"],
        }
        validate(ask, schema)
        route = dict(samples()["routing-case.schema.json"])
        route["ask_materiality"] = ask["ask_materiality"]
        with self.assertRaisesRegex(SchemaFailure, "forbidden schema"):
            validate(route, schema)

    def test_unknown_versions_fail_closed(self):
        for name, instance in samples().items():
            changed = copy.deepcopy(instance)
            changed["schema_version"] = 2
            with self.subTest(name=name), self.assertRaises(SchemaFailure):
                validate(changed, load(name))
        composition = samples()["composition-contract.schema.json"]
        composition["contract_version"] = 2
        with self.assertRaises(SchemaFailure):
            validate(composition, load("composition-contract.schema.json"))

    def test_mixed_composition_versions_are_rejected(self):
        first = samples()["composition-contract.schema.json"]
        second = copy.deepcopy(first)
        second["contract_version"] = 2
        versions = {item["contract_version"] for item in (first, second)}
        self.assertGreater(len(versions), 1)
        self.assertEqual(first["compatibility"]["mixed_version"], "REJECT")
        with self.assertRaises(SchemaFailure):
            validate(second, load("composition-contract.schema.json"))

    def test_authority_conflict_fails(self):
        instance = samples()["composition-contract.schema.json"]
        instance["authority_split"]["command_registry_owns"][-1] = "owner"
        with self.assertRaises(SchemaFailure):
            validate(instance, load("composition-contract.schema.json"))

    def test_conflicting_composition_roles_fail(self):
        instance = samples()["composition-contract.schema.json"]
        instance["reviewers"] = [instance["lead"]]
        with self.assertRaisesRegex(SchemaFailure, "conflicting composition roles"):
            composition_invariants(instance)

    def test_missing_budget_fails(self):
        instance = samples()["eval-operating-contract.schema.json"]
        del instance["budgets"]["spend_ceiling"]
        with self.assertRaisesRegex(SchemaFailure, "missing spend_ceiling"):
            validate(instance, load("eval-operating-contract.schema.json"))

    def test_invalid_sampling_range_fails(self):
        instance = samples()["eval-operating-contract.schema.json"]
        instance["sampling"] = {"rule": "SEQUENTIAL", "minimum_repetitions": 10, "maximum_repetitions": 3}
        validate(instance, load("eval-operating-contract.schema.json"))
        with self.assertRaisesRegex(SchemaFailure, "minimum repetitions"):
            operating_invariants(instance)

    def test_mutating_success_requires_world_state_assurance(self):
        instance = samples()["invocation-trace.schema.json"]
        event = instance["events"][0]
        event["authority"] = "MODIFY"
        event["mutation_mode"] = "WRITE"
        with self.assertRaisesRegex(SchemaFailure, "assurance level 3"):
            trace_invariants(instance)


if __name__ == "__main__":
    unittest.main()
