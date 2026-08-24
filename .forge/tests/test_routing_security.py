import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("routing_eval_security", ROOT / ".forge" / "routing_eval.py")
ROUTING = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(ROUTING)
INTEGRITY_SPEC = importlib.util.spec_from_file_location(
    "eval_integrity_security", ROOT / ".forge" / "eval_integrity.py")
INTEGRITY = importlib.util.module_from_spec(INTEGRITY_SPEC)
assert INTEGRITY_SPEC.loader
INTEGRITY_SPEC.loader.exec_module(INTEGRITY)


def routing_case(case_id="a" * 32, query="Please audit authorization."):
    return {
        "schema_version": 1, "id": case_id, "query": query,
        "expected_primary": "resonance-ops-security", "allowed_contributors": [],
        "forbidden_skills": ["resonance-ops-reviewer"], "harm_tier": "HIGH",
        "cluster": "security-review", "rationale": "Security owns authorization conclusions.",
        "expected_activation_mode": "AUTO", "ambiguity_behavior": "ROUTE",
        "deterministic_checks": [],
    }


def make_dataset(root: Path, role="protected_validation", diagnostic="CASE_LEVEL", case=None,
                 reuse_count=0, max_reuse=None, state="ACTIVE"):
    max_reuse = 1 if role == "sealed_promotion" and max_reuse is None else (max_reuse or 3)
    (root / "cases").mkdir(parents=True)
    case_path = root / "cases" / ("b" * 32 + ".json")
    case_path.write_text(json.dumps(case or routing_case()), encoding="utf-8")
    hashes = {"cases/" + case_path.name: ROUTING.sha256_file(case_path)}
    (root / "dataset.json").write_text(json.dumps({
        "schema_version": 1, "dataset_id": "c" * 32, "role": role,
        "owner": "eval-custodian", "created_at": "2026-08-24T00:00:00Z",
        "permitted_use": "routing validation only", "rotation_rule": "rotate on contamination or limit",
        "max_reuse_count": max_reuse, "diagnostic_policy": diagnostic,
    }), encoding="utf-8")
    (root / "custody-state.json").write_text(json.dumps({
        "schema_version": 1, "dataset_id": "c" * 32, "reuse_count": reuse_count,
        "contamination_events": [], "retirement_state": state,
    }), encoding="utf-8")
    (root / "hash-manifest.json").write_text(json.dumps({
        "schema_version": 1, "algorithm": "sha256", "files": hashes,
    }), encoding="utf-8")


class RoutingSecurityTests(unittest.TestCase):
    def test_repository_path_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside the repository"):
            ROUTING.load_protected_dataset(ROOT / ".forge" / "routing_evals", "protected_validation")

    def test_integrity_scan_rejects_committed_protected_dataset_metadata(self):
        with tempfile.TemporaryDirectory() as raw:
            fake_repo = Path(raw)
            metadata = fake_repo / "dataset.json"
            metadata.write_text(json.dumps({"role": "sealed_promotion"}), encoding="utf-8")
            with mock.patch.object(INTEGRITY, "REPO", fake_repo):
                problems = INTEGRITY.repository_protected_dataset_problems()
            self.assertEqual(["protected routing dataset must live outside repository: dataset.json"], problems)

    def test_integrity_scan_rejects_private_live_eval_artifacts(self):
        with tempfile.TemporaryDirectory() as raw:
            fake_repo = Path(raw)
            (fake_repo / "contract.json").write_text(json.dumps({
                "approval": {"state": "APPROVED"}, "datasets": {}, "canary": {},
            }), encoding="utf-8")
            (fake_repo / "trace.jsonl").write_text(
                '{"type":"tool_use","part":{"tool":"read"}}\n', encoding="utf-8",
            )
            (fake_repo / "canary-cost-ledger.json").write_text("{}", encoding="utf-8")
            with mock.patch.object(INTEGRITY, "REPO", fake_repo):
                problems = INTEGRITY.repository_private_eval_artifact_problems()
            self.assertEqual(3, len(problems))
            self.assertTrue(any("approved evaluation contract" in problem for problem in problems))
            self.assertTrue(any("raw host trace" in problem for problem in problems))
            self.assertTrue(any("private evaluation artifact" in problem for problem in problems))

    def test_case_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            make_dataset(root)
            escaped = root / "cases" / ("b" * 32 + ".json")
            with mock.patch.object(Path, "resolve", autospec=True, side_effect=lambda path, strict=False: (
                    ROOT / ".forge" / "routing_eval.py" if path == escaped else Path.absolute(path))):
                with self.assertRaisesRegex(ValueError, "escapes dataset root"):
                    ROUTING.protected_files(root)

    def test_role_confusion_and_sealed_diagnostics_are_rejected(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            make_dataset(root)
            with self.assertRaisesRegex(ValueError, "role mismatch"):
                ROUTING.load_protected_dataset(root, "sealed_promotion")
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            make_dataset(root, role="sealed_promotion", diagnostic="CASE_LEVEL")
            with self.assertRaisesRegex(ValueError, "SUMMARY_ONLY"):
                ROUTING.load_protected_dataset(root, "sealed_promotion")

    def test_hash_verification_detects_mutation_and_retires_dataset(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            make_dataset(root)
            dataset = ROUTING.load_protected_dataset(root, "protected_validation")
            (root / "cases" / ("b" * 32 + ".json")).write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "changed during execution"):
                ROUTING.assert_protected_unchanged(dataset)
            state = json.loads((root / "custody-state.json").read_text(encoding="utf-8"))
            self.assertEqual("CONTAMINATED", state["retirement_state"])
            self.assertEqual(1, len(state["contamination_events"]))

    def test_access_reuse_rotation_and_hash_events_are_logged(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            make_dataset(root, max_reuse=1)
            dataset = ROUTING.load_protected_dataset(root, "protected_validation")
            ROUTING.begin_protected_access(dataset, "provider/model-revision")
            ROUTING.assert_protected_unchanged(dataset)
            state = json.loads((root / "custody-state.json").read_text(encoding="utf-8"))
            self.assertEqual(1, state["reuse_count"])
            self.assertEqual("RETIRED", state["retirement_state"])
            events = [json.loads(line) for line in (root / "access-log.jsonl").read_text().splitlines()]
            self.assertEqual(["ACCESS", "HASH_VERIFIED"], [event["event"] for event in events])

    def test_oracle_fields_and_copied_rationale_are_rejected(self):
        item = routing_case()
        self.assertTrue(ROUTING.oracle_leakage(item, "expected_primary is secret"))
        output = {"reason": item["rationale"], "primary_skill": item["expected_primary"]}
        self.assertTrue(ROUTING.oracle_leakage(item, "safe request", output))

    def test_prompt_is_oracle_isolated_for_paraphrase_and_multilingual_query(self):
        item = routing_case(query="Pruefe bitte die Berechtigungen dieser API.")
        prompt = ROUTING.router_prompt(item["query"], ROUTING.load_catalog())
        self.assertEqual([], ROUTING.oracle_leakage(item, prompt))
        self.assertNotIn(item["rationale"], prompt)
        self.assertNotIn(item["id"], prompt)

    def test_sealed_summary_never_contains_case_level_or_oracle_values(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            make_dataset(root, role="sealed_promotion", diagnostic="SUMMARY_ONLY")
            dataset = ROUTING.load_protected_dataset(root, "sealed_promotion")
            report = ROUTING.score([dataset["cases"][0]], [{
                "primary_skill": "resonance-ops-security", "contributors": [], "mode": "AUTO",
                "abstain": False, "confidence": .9, "reason": "authorization review", "clarification": None,
            }])
            report["execution"] = {
                "adapter": "opencode-json-v1", "cost_usd": 0.125, "host_events": 3,
            }
            rendered = json.dumps(ROUTING.protected_summary(report, dataset))
            self.assertNotIn("diagnostics", rendered)
            self.assertNotIn(dataset["cases"][0]["id"], rendered)
            self.assertNotIn(dataset["cases"][0]["expected_primary"], rendered)
            self.assertNotIn("input_hashes", rendered)
            self.assertIn('"violation_categories": {}', rendered)
            self.assertIn('"cost_usd": 0.125', rendered)

    def test_invalid_ask_oracle_is_rejected_before_protected_access(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            invalid = routing_case()
            invalid.update({"expected_primary": None, "expected_activation_mode": "ASK",
                            "ambiguity_behavior": "ASK_MATERIAL_QUESTION",
                            "ask_materiality": {"route_changes_primary": False,
                                                 "possible_primary_skills": ["resonance-ops-security"]}})
            make_dataset(root, role="sealed_promotion", diagnostic="SUMMARY_ONLY", case=invalid)
            self.assertEqual(1, ROUTING.main(["--check", "--promotion-holdout-dir", str(root)]))
            state = json.loads((root / "custody-state.json").read_text(encoding="utf-8"))
            self.assertEqual(0, state["reuse_count"])

    def test_valid_sealed_preflight_does_not_consume_the_dataset(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            make_dataset(root, role="sealed_promotion", diagnostic="SUMMARY_ONLY")
            self.assertEqual(0, ROUTING.main(["--check", "--promotion-holdout-dir", str(root)]))
            state = json.loads((root / "custody-state.json").read_text(encoding="utf-8"))
            self.assertEqual(0, state["reuse_count"])
            self.assertEqual("ACTIVE", state["retirement_state"])

    def test_sealed_dataset_must_be_single_use(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            make_dataset(root, role="sealed_promotion", diagnostic="SUMMARY_ONLY")
            metadata_path = root / "dataset.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata["max_reuse_count"] = 2
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "single-use"):
                ROUTING.load_protected_dataset(root, "sealed_promotion")

    def test_concurrent_custody_overwrite_contaminates_the_dataset(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            make_dataset(root, role="sealed_promotion", diagnostic="SUMMARY_ONLY")
            dataset = ROUTING.load_protected_dataset(root, "sealed_promotion")
            ROUTING.begin_protected_access(dataset, "test/model")
            state_path = root / "custody-state.json"
            overwritten = json.loads(state_path.read_text(encoding="utf-8"))
            overwritten.update({"reuse_count": 0, "retirement_state": "ACTIVE"})
            state_path.write_text(json.dumps(overwritten), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "changed concurrently"):
                ROUTING.assert_protected_unchanged(dataset)
            repaired = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(1, repaired["reuse_count"])
            self.assertEqual("CONTAMINATED", repaired["retirement_state"])
            self.assertTrue(repaired["contamination_events"])

    def test_immutable_control_mutation_is_detected(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            make_dataset(root)
            dataset = ROUTING.load_protected_dataset(root, "protected_validation")
            metadata_path = root / "dataset.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata["owner"] = "unexpected-writer"
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "control metadata changed"):
                ROUTING.assert_protected_unchanged(dataset)

    def test_sealed_failure_sidecar_requires_retirement_and_is_external(self):
        with tempfile.TemporaryDirectory() as raw, tempfile.TemporaryDirectory() as outside:
            root = Path(raw)
            make_dataset(root, role="sealed_promotion", diagnostic="SUMMARY_ONLY")
            dataset = ROUTING.load_protected_dataset(root, "sealed_promotion")
            dataset["state"]["retirement_state"] = "RETIRED"
            target = Path(outside) / "failed.json"
            ROUTING.write_failed_sidecar(target, dataset, [{"raw_output": "private"}])
            self.assertEqual("private", json.loads(target.read_text())["failures"][0]["raw_output"])
            with self.assertRaisesRegex(ValueError, "outside the repository"):
                ROUTING.write_failed_sidecar(ROOT / ".forge" / "failed.json", dataset, [])

    def test_passing_sealed_run_does_not_write_sidecar(self):
        with tempfile.TemporaryDirectory() as raw, tempfile.TemporaryDirectory() as outside:
            root = Path(raw)
            make_dataset(root, role="sealed_promotion", diagnostic="SUMMARY_ONLY")
            target = Path(outside) / "should-not-exist.json"
            output = {"primary_skill": "resonance-ops-security", "contributors": [],
                      "mode": "AUTO", "abstain": False, "confidence": .9,
                      "reason": "authorization review", "clarification": None}
            with mock.patch.object(ROUTING, "_run_router_with_raw",
                                   return_value=(output, {"cost_usd": 0.0, "events": 0}, "raw")):
                self.assertEqual(0, ROUTING.main([
                    "--promotion-holdout-dir", str(root), "--model-cmd", "router",
                    "--model-id", "test/model", "--failed-run-sidecar", str(target),
                ]))
            self.assertFalse(target.exists())

    def test_failed_sealed_run_writes_private_reproduction_sidecar(self):
        with tempfile.TemporaryDirectory() as raw, tempfile.TemporaryDirectory() as outside:
            root = Path(raw)
            make_dataset(root, role="sealed_promotion", diagnostic="SUMMARY_ONLY")
            target = Path(outside) / "failed.json"
            output = {"primary_skill": "resonance-ops-reviewer", "contributors": [],
                      "mode": "AUTO", "abstain": False, "confidence": .9,
                      "reason": "general review", "clarification": None}
            stream = io.StringIO()
            with mock.patch.object(ROUTING, "_run_router_with_raw",
                                   return_value=(output, {"cost_usd": 0.0, "events": 0},
                                                 "PRIVATE_RAW_OUTPUT")), redirect_stdout(stream):
                self.assertEqual(1, ROUTING.main([
                    "--promotion-holdout-dir", str(root), "--model-cmd", "router",
                    "--model-id", "test/model", "--failed-run-sidecar", str(target),
                ]))
            payload = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual("PRIVATE_RAW_OUTPUT", payload["failures"][0]["raw_output"])
            self.assertIn("high_harm_primary_misroute", payload["report"]["violation_categories"])
            self.assertNotIn("PRIVATE_RAW_OUTPUT", stream.getvalue())

    def test_protected_opacity_rejects_semantic_identifiers(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            make_dataset(root)
            case_path = root / "cases" / ("b" * 32 + ".json")
            item = json.loads(case_path.read_text())
            item["id"] = "security-review"
            self.assertTrue(ROUTING.validate_protected_opacity(root, [item]))

    def test_protected_results_cannot_be_written_into_repository(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            make_dataset(root)
            with self.assertRaises(SystemExit):
                ROUTING.main(["--check", "--validation-holdout-dir", str(root),
                              "--results", str(ROOT / "private-result.json")])

    def test_public_memorization_does_not_supply_protected_paraphrase_oracle(self):
        public = routing_case(query="Run the security audit.")
        protected = routing_case(query="Pruefe, wer auf den Endpunkt zugreifen darf.")
        prompt = ROUTING.router_prompt(protected["query"], ROUTING.load_catalog())
        self.assertNotIn(public["query"], prompt)
        self.assertNotIn(protected["expected_primary"], prompt.split("USER REQUEST:", 1)[1])


if __name__ == "__main__":
    unittest.main()
