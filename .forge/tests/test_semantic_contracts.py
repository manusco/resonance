"""Tests for the frozen composition contract v1."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

FORGE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FORGE))

from kernel.manifest import composition_warnings, manifest, normalize_entry  # noqa: E402
import validate_skill  # noqa: E402


CANARY = "resonance-ops-goal"


def entry(**overrides):
    base = {
        "id": CANARY,
        "contract_version": 1,
        "job_id": "delivery.goal",
        "stage": "EXECUTE",
        "contributes_to": [],
        "reviews": [],
        "finalizes": ["verified-outcome"],
        "artifact_access": ["verified-outcome:create,modify"],
        "dispatch_conditions": ["an outcome needs bounded execution"],
        "compatibility": "active",
        "authority": "consequential",
        "entrypoints": ["/goal"],
    }
    base.update(overrides)
    return base


class CompositionCompatibilityTest(unittest.TestCase):
    def test_v0_noncanary_is_accepted(self):
        self.assertEqual([], composition_warnings([{"id": "resonance-x-y"}], {CANARY}))

    def test_v0_canary_warns_without_becoming_an_error(self):
        warnings = composition_warnings([{"id": CANARY}], {CANARY})
        self.assertTrue(any("v0" in item for item in warnings))

    def test_v1_contract_is_clean(self):
        self.assertEqual([], composition_warnings([entry()], {CANARY}))

    def test_unknown_version_fails_closed_in_warning_mode(self):
        warnings = composition_warnings([entry(contract_version=2)], {CANARY})
        self.assertTrue(any("unknown contract_version" in item and "fail closed" in item
                            for item in warnings))

    def test_mixed_versions_are_rejected(self):
        primary = entry(contributes_to=["delivery.legacy"])
        legacy = {"id": "resonance-software-legacy", "job_id": "delivery.legacy"}
        warnings = composition_warnings([primary, legacy], {CANARY})
        self.assertTrue(any("mix contract versions" in item and "reject" in item
                            for item in warnings))

    def test_explicit_v0_with_v1_fields_requires_migration(self):
        warnings = composition_warnings([entry(contract_version=0)], {CANARY})
        self.assertTrue(any("explicit migration required" in item for item in warnings))


class CompositionConsistencyTest(unittest.TestCase):
    def test_cross_field_conflicts_warn(self):
        broken = entry(
            contributes_to=["delivery.goal"],
            reviews=["delivery.goal"],
            artifact_access=["verified-outcome:read"],
        )
        warnings = composition_warnings([broken], {CANARY})
        joined = "\n".join(warnings)
        self.assertIn("contributes to its own job", joined)
        self.assertIn("reviews its own job", joined)
        self.assertIn("both contributes to and reviews", joined)
        self.assertIn("without a finalizing artifact right", joined)

    def test_shared_artifact_rights_do_not_claim_exclusive_path_ownership(self):
        first = entry()
        second = entry(id="resonance-ops-qa", job_id="verification.qa",
                       contributes_to=["delivery.goal"], finalizes=[],
                       artifact_access=["verified-outcome:read,review"],
                       dispatch_conditions=["verification is required"], entrypoints=[])
        warnings = composition_warnings([first, second], {CANARY, "resonance-ops-qa"})
        self.assertFalse(any("collision" in item or "exclusive" in item for item in warnings))

    def test_alias_requires_one_canonical_target(self):
        warnings = composition_warnings([entry(compatibility="alias")], {CANARY})
        self.assertTrue(any("exactly one canonical job" in item for item in warnings))


class ManifestAndValidatorTest(unittest.TestCase):
    def test_real_canary_templates_are_consistent(self):
        root = FORGE / "skills"
        paths = [
            "ops/goal", "software/deliver-change", "ops/audit", "ops/security",
            "ops/reviewer", "ops/qa", "strategy/architect", "engineering/performance",
            "engineering/backend", "engineering/frontend", "engineering/database",
            "engineering/ai-engineering", "strategy/brief", "strategy/grill", "strategy/plan",
        ]
        entries = [normalize_entry(root / path / "skill.tmpl.md", root) for path in paths]
        warnings = composition_warnings([item for item in entries if item], {
            "resonance-ops-goal", "resonance-software-deliver-change", "resonance-ops-audit",
            "resonance-ops-security", "resonance-ops-reviewer", "resonance-ops-qa",
            "resonance-strategy-architect", "resonance-engineering-performance",
            "resonance-engineering-backend", "resonance-engineering-frontend",
            "resonance-engineering-database", "resonance-engineering-ai-engineering",
            "resonance-strategy-brief", "resonance-strategy-grill", "resonance-strategy-plan",
        })
        self.assertEqual([], warnings)

    def test_deliver_change_compatibility_trigger_does_not_compete_with_goal(self):
        root = FORGE / "skills"
        goal = normalize_entry(root / "ops" / "goal" / "skill.tmpl.md", root)
        compatibility = normalize_entry(
            root / "software" / "deliver-change" / "skill.tmpl.md", root,
        )
        self.assertTrue(any("new outcome" in item for item in goal["triggers"]))
        self.assertTrue(all(
            "explicit" in item or "existing workflow" in item
            for item in compatibility["triggers"]
        ))
        self.assertTrue(any(
            "new end-to-end outcome" in item
            for item in compatibility["negative_triggers"]
        ))

    def test_manifest_emits_flat_contract_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "ops" / "goal"
            skill.mkdir(parents=True)
            skill.joinpath("SKILL.md").write_text(
                "---\nname: resonance-ops-goal\ndescription: Use when driving a goal.\n"
                "archetype: orchestration\ncontract_version: 1\njob_id: delivery.goal\n"
                "stage: EXECUTE\ncontributes_to:\nreviews:\nfinalizes:\n  - verified-outcome\n"
                "artifact_access:\n  - verified-outcome:create,modify\ndispatch_conditions:\n"
                "  - outcome work is authorized\ncompatibility: active\nowner: ops.goal\n"
                "activation: manual\nauthority: consequential\ntriggers:\n  - drive goal\n"
                "inputs:\n  - user_request\noutputs:\n  - evidence\ninvokes:\n  - resonance-ops-qa\n"
                "side_effects:\n  - may_coordinate_work\nwrite_sets:\n  - project:goal-state\n"
                "entrypoints:\n  - /goal\nfailure_policy: stop\n---\n",
                encoding="utf-8",
            )
            data = manifest(root)
            self.assertEqual(1, data[0]["contract_version"])
            self.assertEqual("delivery.goal", data[0]["job_id"])
            self.assertEqual(["verified-outcome:create,modify"], data[0]["artifact_access"])

    def test_v1_contract_errors_are_always_enforced_for_accepted_cohort(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "SKILL.md"
            skill.write_text(
                "---\nname: resonance-ops-goal\ndescription: Use when driving a goal.\n"
                "archetype: knowledge\n---\n\n# Goal\n",
                encoding="utf-8",
            )
            (root / "evals").mkdir()
            for number in range(3):
                (root / "evals" / f"{number}.json").write_text("{}", encoding="utf-8")
            normal = validate_skill.validate(skill, validate_skill.Report(str(skill)))
            canary = validate_skill.validate(skill, validate_skill.Report(str(skill)), True)
            self.assertTrue(any("composition contract" in item for item in normal.errors))
            self.assertEqual(normal.errors, canary.errors)


if __name__ == "__main__":
    unittest.main()
