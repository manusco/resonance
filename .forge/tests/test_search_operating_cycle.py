import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".forge" / "skills" / "marketing" / "run-search-operating-cycle" / "scripts" / "validate_search_run.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_search_run", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SearchOperatingCycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()

    def validate(self, document):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "document.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            return self.validator.main([str(SCRIPT), str(path)])

    def contract(self):
        return {
            "document_type": "search_run_contract",
            "property_registry": [
                {"property_id": "public-site", "property_uri": "sc-domain:example.org", "owner_role": "SEO owner"}
            ],
            "cadence": "monthly",
            "timezone": "Europe/Berlin",
            "credential_reference": "secret-manager:gsc-readonly",
            "artifact_destination": {"kind": "private", "path": "/private/work/search-runs"},
            "comparison_window": {
                "current_start": "2026-07-01",
                "current_end": "2026-07-31",
                "prior_start": "2026-06-01",
                "prior_end": "2026-06-30",
            },
            "previous_run": None,
        }

    def test_private_contract_passes(self):
        self.assertEqual(0, self.validate(self.contract()))

    def test_repository_destination_requires_approval(self):
        contract = self.contract()
        contract["artifact_destination"] = {"kind": "repository", "path": "docs/search-report.md"}
        self.assertEqual(1, self.validate(contract))

    def test_individual_information_is_rejected(self):
        contract = self.contract()
        contract["property_registry"][0]["email"] = "person@example.org"
        self.assertEqual(1, self.validate(contract))

    def test_individual_information_is_rejected_anywhere_in_report(self):
        report = {
            "document_type": "search_run_report",
            "scoped_property_ids": ["public-site"],
            "property_outcomes": [{"property_id": "public-site", "state": "clean", "evidence_state": "complete"}],
            "findings": [],
            "contact_email": "person@example.org",
        }
        self.assertEqual(1, self.validate(report))

    def test_cannibalization_finding_requires_joint_dimensions(self):
        report = {
            "document_type": "search_run_report",
            "scoped_property_ids": ["public-site"],
            "property_outcomes": [{"property_id": "public-site", "state": "finding", "evidence_state": "complete"}],
            "findings": [{
                "property_id": "public-site",
                "kind": "cannibalization",
                "category": "Product Correctness",
                "severity": "P2",
                "state": "finding",
                "dimensions": ["query"],
                "evidence_reference": "private:run/evidence.json",
                "harm": "Two pages may split relevance signals.",
                "recommended_action": "Inspect joint query-page rows.",
                "owner_role": "SEO owner",
                "verification_method": "Repeat the joint query-page export.",
            }],
        }
        self.assertEqual(1, self.validate(report))

    def test_canonical_report_passes(self):
        report = {
            "document_type": "search_run_report",
            "scoped_property_ids": ["public-site"],
            "property_outcomes": [{"property_id": "public-site", "state": "clean", "evidence_state": "complete"}],
            "findings": [],
        }
        self.assertEqual(0, self.validate(report))

    def test_report_must_cover_each_scoped_property_exactly_once(self):
        report = {
            "document_type": "search_run_report",
            "scoped_property_ids": ["public-site", "docs-site"],
            "property_outcomes": [{"property_id": "public-site", "state": "clean", "evidence_state": "complete"}],
            "findings": [],
        }
        self.assertEqual(1, self.validate(report))

    def test_skill_has_six_evals_and_no_scheduler_implementation(self):
        skill_root = SCRIPT.parents[1]
        self.assertGreaterEqual(len(list((skill_root / "evals").glob("*.json"))), 6)
        template = (skill_root / "skill.tmpl.md").read_text(encoding="utf-8")
        self.assertIn("failure_policy: stop", template)
        self.assertIn("resonance-marketing-seo", template)
        self.assertNotIn("schedule.create", template)


if __name__ == "__main__":
    unittest.main()
