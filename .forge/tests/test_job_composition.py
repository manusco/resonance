import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FORGE = ROOT / ".forge"
if str(FORGE) not in sys.path:
    sys.path.insert(0, str(FORGE))

import job_composition
from kernel.manifest import normalize_entry
from kernel.manifest import graph_errors
from schema_check import load_schema, validate


class JobCompositionTests(unittest.TestCase):
    def setUp(self):
        source = FORGE / "skills"
        self.manifest = [
            normalize_entry(path, source)
            for path in sorted(source.glob("**/skill.tmpl.md"))
        ]
        self.manifest = [entry for entry in self.manifest if entry]

    def test_every_skill_job_compiles_to_valid_job_contract(self):
        contracts = job_composition.compile_contracts(self.manifest)
        expected = sum(1 for item in self.manifest if item.get("job_id"))
        self.assertEqual(expected, len(contracts))
        schema = load_schema("composition-contract.schema.json")
        for contract in contracts:
            with self.subTest(job_id=contract["job_id"]):
                validate(contract, schema)
                job_composition.validate_invariants(contract)

    def test_nonlead_job_participants_declare_versioned_profiles(self):
        for item in self.manifest:
            if not item.get("job_id") and (item.get("contributes_to") or item.get("reviews")):
                with self.subTest(skill=item["id"]):
                    self.assertEqual(1, item.get("contract_version"))
                    self.assertEqual("participant", item.get("contract_role"))
                    self.assertTrue(item.get("artifact_access"))
                    self.assertTrue(item.get("dispatch_conditions"))

    def test_delivery_goal_derives_participants_from_skill_edges(self):
        contracts = {item["job_id"]: item for item in job_composition.compile_contracts(self.manifest)}
        goal = contracts["delivery.goal"]
        self.assertEqual("resonance-ops-goal", goal["lead"])
        self.assertIn("resonance-engineering-backend", goal["contributors"])
        self.assertIn("resonance-ops-security", goal["reviewers"])
        self.assertEqual("resonance-ops-goal", goal["finalizer"])

    def test_plan_governance_handoff_is_non_recursive_and_keeps_both_artifacts(self):
        contracts = {item["job_id"]: item for item in job_composition.compile_contracts(self.manifest)}
        plan = contracts["delivery.plan"]
        blueprint = contracts["architecture.blueprint"]
        plan_skill = next(item for item in self.manifest if item["id"] == plan["lead"])
        blueprint_skill = next(item for item in self.manifest if item["id"] == blueprint["lead"])

        self.assertIn("resonance-strategy-blueprint", plan_skill["invokes"])
        self.assertNotIn("resonance-strategy-plan", blueprint_skill["invokes"])
        self.assertIn("implementation-plan", plan_skill["finalizes"])
        self.assertIn("architecture-conformance-report", blueprint_skill["finalizes"])
        self.assertIn("implementation_plan", plan_skill["outputs"])
        self.assertIn("blueprint_scope", plan_skill["outputs"])
        self.assertFalse([issue for issue in graph_errors(self.manifest) if "cycle" in issue.lower()])

    def test_duplicate_job_owner_fails_closed(self):
        duplicate = list(self.manifest)
        owner = next(item for item in self.manifest if item.get("job_id") == "delivery.goal")
        duplicate.append({**owner, "id": "duplicate-goal-owner"})
        with self.assertRaisesRegex(ValueError, "multiple lead skills"):
            job_composition.compile_contracts(duplicate)

    def test_participant_without_artifact_access_fails_closed(self):
        mutated = [dict(item) for item in self.manifest]
        reviewer = next(item for item in mutated if "delivery.goal" in item.get("reviews", []))
        reviewer["artifact_access"] = []
        with self.assertRaisesRegex(ValueError, "participants have no artifact access"):
            job_composition.compile_contracts(mutated)

    def test_blueprint_cannot_approve_human_governed_artifacts(self):
        blueprint = next(
            item for item in self.manifest if item.get("job_id") == "architecture.blueprint"
        )
        rights = {
            row.split(":", 1)[0]: set(row.split(":", 1)[1].split(","))
            for row in blueprint["artifact_access"]
        }
        self.assertNotIn("approve", rights["architecture-blueprint"])
        self.assertNotIn("approve", rights["architecture-exception"])
        self.assertIn("approve", rights["architecture-conformance-report"])

    def test_participants_may_be_nested_but_must_be_invocable_from_the_lead(self):
        contracts = {item["job_id"]: item for item in job_composition.compile_contracts(self.manifest)}
        goal = contracts["delivery.goal"]
        self.assertIn("resonance-engineering-backend", goal["contributors"])

        mutated = json.loads(json.dumps(self.manifest))
        lead = next(item for item in mutated if item["id"] == "resonance-engineering-build")
        lead["invokes"].remove("resonance-engineering-backend")
        with self.assertRaisesRegex(ValueError, "not reachable through invokes"):
            job_composition.compile_contracts(mutated)

    def test_conditional_invokes_do_not_have_to_be_contract_participants(self):
        manifest = [
            {"id": "resonance-test-lead", "job_id": "test.job", "stage": "PLAN",
             "invokes": ["resonance-test-worker", "resonance-optional-reviewer"],
             "dispatch_conditions": ["dispatch reviewer only when risk requires"],
             "artifact_access": ["job-result:create,modify"], "finalizes": ["job-result"]},
            {"id": "resonance-test-worker", "contributes_to": ["test.job"],
             "artifact_access": ["worker-output:create"]},
            {"id": "resonance-optional-reviewer", "artifact_access": ["review-note:create"]},
        ]
        contract = job_composition.compile_contracts(manifest)[0]
        self.assertEqual(["resonance-test-worker"], contract["contributors"])

    def test_unreachable_extra_participant_fails_closed(self):
        mutated = json.loads(json.dumps(self.manifest))
        outsider = next(item for item in mutated if item["id"] == "resonance-engineering-game-dev")
        outsider.setdefault("contributes_to", []).append("marketing.campaign")
        outsider["artifact_access"] = ["game-output:create"]
        with self.assertRaisesRegex(ValueError, "not reachable through invokes"):
            job_composition.compile_contracts(mutated)

    def test_finalizer_must_have_a_right_to_finish_each_declared_artifact(self):
        manifest = [{"id": "resonance-test-lead", "job_id": "test.job", "stage": "PLAN",
                     "invokes": [], "dispatch_conditions": ["always"],
                     "artifact_access": ["other-artifact:read"], "finalizes": ["job-result"]}]
        with self.assertRaisesRegex(ValueError, "cannot finalize 'job-result'"):
            job_composition.compile_contracts(manifest)

    def test_duplicate_artifact_rights_compile_to_one_minimal_row(self):
        manifest = [{"id": "resonance-test-lead", "job_id": "test.job", "stage": "PLAN",
                     "invokes": [], "dispatch_conditions": ["always"],
                     "artifact_access": ["job-result:create", "job-result:create,modify"],
                     "finalizes": ["job-result"]}]
        contract = job_composition.compile_contracts(manifest)[0]
        self.assertEqual([{"artifact": "job-result", "actor": "resonance-test-lead",
                           "rights": ["CREATE", "MODIFY"]}], contract["artifact_access"])


if __name__ == "__main__":
    unittest.main()
