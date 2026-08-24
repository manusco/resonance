import importlib.util
import json
import subprocess
import sys
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("routing_eval", ROOT / ".forge" / "routing_eval.py")
ROUTING = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(ROUTING)


def result(primary, contributors=None, mode="AUTO", abstain=False, clarification=None):
    return {
        "primary_skill": primary, "contributors": contributors or [], "mode": mode,
        "abstain": abstain, "confidence": 0.9, "reason": "The request matches this owner.",
        "clarification": clarification,
    }


def case(case_id, primary, tier="STANDARD", cluster="test", mode="AUTO",
         forbidden=None, allowed=None, ambiguity="ROUTE"):
    value = {
        "schema_version": 1, "id": case_id, "query": "route this", "expected_primary": primary,
        "allowed_contributors": allowed or [], "forbidden_skills": forbidden or [],
        "harm_tier": tier, "cluster": cluster, "rationale": "owner boundary",
        "expected_activation_mode": mode, "ambiguity_behavior": ambiguity,
        "deterministic_checks": [],
    }
    if ambiguity == "ASK_MATERIAL_QUESTION":
        value["ask_materiality"] = {
            "route_changes_primary": True,
            "possible_primary_skills": ["resonance-strategy-brief", "resonance-strategy-council"],
        }
    return value


class RoutingEvalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = ROUTING.load_catalog()
        cls.skill_ids = {item["id"] for item in cls.catalog}

    def test_public_fixtures_are_valid_and_cover_required_classes(self):
        cases = ROUTING.load_cases()
        errors = [problem for item in cases for problem in ROUTING.validate_case(item, self.skill_ids)]
        self.assertEqual([], errors)
        tiers = {item["harm_tier"] for item in cases}
        self.assertEqual({"STANDARD", "HIGH", "CRITICAL"}, tiers)
        self.assertTrue(any(item["expected_primary"] is None for item in cases))
        self.assertTrue(any(item["ambiguity_behavior"] == "ASK_MATERIAL_QUESTION" for item in cases))
        self.assertEqual([], ROUTING.validate_case_set(cases))

    def test_mode_policy_rejects_ask_without_material_ambiguity(self):
        item = case("bad-ask", None, mode="ASK", ambiguity="ROUTE")
        self.assertIn("ASK mode requires material ambiguity", ROUTING.validate_case(item, self.skill_ids))

    def test_mode_policy_rejects_manual_for_ordinary_specialist(self):
        item = case("bad-manual", "resonance-engineering-performance", mode="MANUAL")
        self.assertIn(
            "MANUAL mode is reserved for explicit or consequential entrypoints",
            ROUTING.validate_case(item, self.skill_ids),
        )

    def test_duplicate_query_cannot_disagree_on_route_or_mode(self):
        first = case("first", "resonance-strategy-researcher", mode="AUTO")
        second = case("second", "resonance-strategy-researcher", mode="MANUAL")
        self.assertTrue(ROUTING.validate_case_set([first, second]))

    def test_prompt_contains_catalog_but_not_oracle(self):
        item = ROUTING.load_cases()[0]
        prompt = ROUTING.router_prompt(item["query"], self.catalog)
        self.assertIn("CATALOG", prompt)
        self.assertIn(item["query"], prompt)
        self.assertNotIn(item["rationale"], prompt)
        self.assertNotIn("expected_primary", prompt)
        self.assertIn("host_activation", prompt)
        self.assertIn("Routing never grants permission for side effects", prompt)
        self.assertIn("Default contributors to an empty list", prompt)
        self.assertIn("Do not add a skill because it is related", prompt)
        self.assertIn("Decide the route first, then apply this mode rule exactly", prompt)
        self.assertIn("Never use MANUAL for any other primary", prompt)
        self.assertNotIn('"activation":', prompt)

    def test_result_requires_exact_shape_and_valid_catalog_ids(self):
        valid = result("resonance-strategy-brief", mode="MANUAL")
        self.assertEqual([], ROUTING.validate_result(valid, self.skill_ids))
        invalid = dict(valid, unexpected=True)
        self.assertTrue(ROUTING.validate_result(invalid, self.skill_ids))
        invalid = dict(valid, primary_skill="not-a-skill")
        self.assertTrue(ROUTING.validate_result(invalid, self.skill_ids))

    def test_ask_requires_abstention_and_question(self):
        invalid = result(None, mode="ASK")
        self.assertTrue(ROUTING.validate_result(invalid, self.skill_ids))
        valid = result(None, mode="ASK", abstain=True, clarification="Which environment?")
        self.assertEqual([], ROUTING.validate_result(valid, self.skill_ids))

    def test_exact_primary_contributor_and_abstention_metrics(self):
        cases = [
            case("a", "resonance-strategy-brief", allowed=["resonance-ops-product"]),
            case("b", None, mode="ASK", ambiguity="ASK_MATERIAL_QUESTION"),
        ]
        outputs = [
            result("resonance-strategy-brief", ["resonance-ops-product"]),
            result(None, mode="ASK", abstain=True, clarification="What is the target?"),
        ]
        report = ROUTING.score(cases, outputs)
        self.assertTrue(report["passed"])
        self.assertEqual(1.0, report["metrics"]["exact_primary_accuracy"])
        self.assertEqual(1.0, report["metrics"]["contributor_precision"])
        self.assertEqual(1.0, report["metrics"]["contributor_recall"])
        self.assertEqual(1.0, report["metrics"]["abstention_quality"])

    def test_one_critical_forbidden_selection_fails(self):
        cases = [case("critical", "resonance-ops-ship", "CRITICAL", "shipping",
                      mode="MANUAL", forbidden=["resonance-engineering-build"])]
        outputs = [result("resonance-ops-ship", ["resonance-engineering-build"], mode="MANUAL")]
        report = ROUTING.score(cases, outputs)
        self.assertFalse(report["passed"])
        self.assertTrue(any("critical forbidden" in item for item in report["violations"]))

    def test_one_missed_critical_manual_gate_fails(self):
        cases = [case("critical", "resonance-ops-ship", "CRITICAL", "shipping", mode="MANUAL")]
        outputs = [result("resonance-ops-ship", mode="AUTO")]
        report = ROUTING.score(cases, outputs)
        self.assertFalse(report["passed"])
        self.assertTrue(any("routing mode mismatch" in item for item in report["violations"]))

    def test_standard_mode_mismatch_fails(self):
        cases = [case("standard", "resonance-engineering-performance", mode="AUTO")]
        outputs = [result("resonance-engineering-performance", mode="MANUAL")]
        report = ROUTING.score(cases, outputs)
        self.assertFalse(report["passed"])
        self.assertTrue(any("routing mode mismatch" in item for item in report["violations"]))

    def test_high_harm_only_cohort_does_not_invent_standard_macro_failure(self):
        cases = [case("high", "resonance-ops-goal", "HIGH", "goal")]
        report = ROUTING.score(cases, [result("resonance-ops-goal")], {"goal"})
        self.assertTrue(report["passed"])
        self.assertIsNone(report["metrics"]["standard_macro_accuracy"])
        self.assertIsNone(report["metrics"]["standard_exact_primary_wilson_95"])
        self.assertEqual(0, report["metrics"]["standard_clear_case_count"])

    def test_high_harm_misroute_in_changed_cluster_fails(self):
        cases = [case("high", "resonance-ops-security", "HIGH", "security")]
        outputs = [result("resonance-ops-reviewer")]
        report = ROUTING.score(cases, outputs, {"security"})
        self.assertFalse(report["passed"])
        self.assertTrue(any("high-harm primary" in item for item in report["violations"]))

    def test_standard_macro_accuracy_below_threshold_fails(self):
        cases = [case("a", "resonance-strategy-brief"), case("b", "resonance-strategy-council")]
        outputs = [result("resonance-strategy-brief"), result("resonance-strategy-brief")]
        report = ROUTING.score(cases, outputs)
        self.assertFalse(report["passed"])
        self.assertTrue(any("macro accuracy" in item for item in report["violations"]))

    def test_confusion_matrices_are_per_skill_and_cluster(self):
        cases = [case("a", "resonance-strategy-council", cluster="framing")]
        outputs = [result("resonance-strategy-brief")]
        report = ROUTING.score(cases, outputs)
        self.assertEqual(1, report["confusion"]["per_cluster"]["framing"][
            "resonance-strategy-council -> resonance-strategy-brief"])
        self.assertEqual(1, report["confusion"]["per_expected_skill"][
            "resonance-strategy-council"]["resonance-strategy-brief"])

    def test_wilson_interval_is_bounded(self):
        low, high = ROUTING.wilson(19, 20)
        self.assertGreaterEqual(low, 0)
        self.assertLessEqual(high, 1)
        self.assertLess(low, high)

    def test_opencode_adapter_extracts_final_json_and_cost(self):
        expected = result("resonance-ops-security")
        raw = "\n".join([
            json.dumps({"type": "step_start", "part": {}}),
            json.dumps({"type": "text", "part": {"text": json.dumps(expected)}}),
            json.dumps({"type": "step_finish", "part": {"cost": 0.0125}}),
        ])
        parsed, usage = ROUTING.parse_router_output(raw, "opencode-json-v1")
        self.assertEqual(expected, parsed)
        self.assertEqual({"cost_usd": 0.0125, "events": 3}, usage)

    def test_plain_adapter_remains_backward_compatible(self):
        expected = result("resonance-strategy-brief")
        parsed, usage = ROUTING.parse_router_output(json.dumps(expected))
        self.assertEqual(expected, parsed)
        self.assertEqual({"cost_usd": 0.0, "events": 0}, usage)

    def test_transport_timeout_retries_within_the_declared_limit(self):
        expected = result("resonance-ops-security")
        with mock.patch.object(
            ROUTING, "_run_router_with_raw",
            side_effect=[subprocess.TimeoutExpired(["router"], 1),
                         (expected, {"cost_usd": 0.01, "events": 3}, "raw")],
        ) as runner:
            output, usage, raw, attempts = ROUTING.run_router_with_retries(
                "router", "prompt", 1, "plain-json", 1)
        self.assertEqual(expected, output)
        self.assertEqual("raw", raw)
        self.assertEqual(1, len(attempts))
        self.assertEqual("TimeoutExpired", attempts[0]["error_type"])
        self.assertEqual(2, runner.call_count)


if __name__ == "__main__":
    unittest.main()
