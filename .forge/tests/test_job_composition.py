import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FORGE = ROOT / ".forge"
if str(FORGE) not in sys.path:
    sys.path.insert(0, str(FORGE))

import job_composition
from schema_check import load_schema, validate


class JobCompositionTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "docs" / "skill-manifest.json").read_text(encoding="utf-8"))

    def test_every_skill_job_compiles_to_valid_job_contract(self):
        contracts = job_composition.compile_contracts(self.manifest)
        expected = sum(1 for item in self.manifest if item.get("job_id"))
        self.assertEqual(expected, len(contracts))
        schema = load_schema("composition-contract.schema.json")
        for contract in contracts:
            with self.subTest(job_id=contract["job_id"]):
                validate(contract, schema)
                job_composition.validate_invariants(contract)

    def test_delivery_goal_derives_participants_from_skill_edges(self):
        contracts = {item["job_id"]: item for item in job_composition.compile_contracts(self.manifest)}
        goal = contracts["delivery.goal"]
        self.assertEqual("resonance-ops-goal", goal["lead"])
        self.assertIn("resonance-engineering-backend", goal["contributors"])
        self.assertIn("resonance-ops-security", goal["reviewers"])
        self.assertEqual("resonance-ops-goal", goal["finalizer"])

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


if __name__ == "__main__":
    unittest.main()
