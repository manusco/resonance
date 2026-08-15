"""Tests for the small Resonance evidence kernel."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

FORGE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FORGE))

from kernel.contracts import ContractError, hash_data, validate_goal_contract  # noqa: E402
from kernel.evidence import accept_evidence, transition_goal  # noqa: E402
from kernel.ledger import active_entries  # noqa: E402
from kernel.manifest import manifest  # noqa: E402
from kernel.runner import manifest_hash  # noqa: E402

GOOD_HASH = "sha256:" + ("b" * 64)


class KernelTest(unittest.TestCase):
    def _exec(self):
        return {
            "schema_version": 1,
            "execution_id": "exe-1",
            "action_id": "act-test",
            "provider_profile": "local-shell",
            "command_or_tool": "unit-test",
            "normalized_arguments": [],
            "working_directory": ".",
            "started_at": "2026-08-15T00:00:00Z",
            "finished_at": "2026-08-15T00:00:01Z",
            "exit_code": 0,
            "stdout_hash": GOOD_HASH,
            "stderr_hash": GOOD_HASH,
            "before_manifest_hash": GOOD_HASH,
            "after_manifest_hash": manifest_hash(Path.cwd()),
            "artifact_hashes": [],
            "runner": "resonance-kernel-runner/1"
        }

    def test_goal_contract_requires_real_acceptance(self):
        with self.assertRaises(ContractError):
            validate_goal_contract({"outcome": "ship"})
        with self.assertRaises(ContractError):
            validate_goal_contract({"outcome": "ship", "acceptance_checks": []})

    def test_stale_plan_hash_rejected(self):
        contract = {"outcome": "ship", "acceptance_checks": ["tests pass"]}
        state = {
            "schema_version": 1,
            "status": "active",
            "goal_revision": 1,
            "run_id": "run-test",
            "criterion_ids": ["criterion-1"],
            "contract": contract,
            "contract_hash": hash_data(contract),
            "plan_hash": GOOD_HASH,
            "executions": [self._exec()],
            "evidence": [],
        }
        evidence = {
            "schema_version": 1,
            "evidence_id": "evd-1",
            "run_id": "run-test",
            "goal_revision": 1,
            "contract_hash": hash_data(contract),
            "plan_hash": "sha256:" + ("c" * 64),
            "slice_id": "slice-1",
            "criterion_id": "criterion-1",
            "verifier": "unit-test",
            "result": "accepted",
            "created_at": "2026-08-15T00:00:00Z",
            "execution_receipts": [self._exec()],
        }
        with self.assertRaises(ContractError):
            accept_evidence(state, evidence, None)

    def test_achieved_requires_evidence_for_each_criterion(self):
        contract = {"outcome": "ship", "acceptance_checks": ["tests pass", "docs updated"]}
        state = {
            "status": "active",
            "goal_revision": 1,
            "contract": contract,
            "criterion_ids": ["criterion-1", "criterion-2"],
            "evidence": [{"criterion_id": "criterion-1", "result": "accepted"}],
        }
        with self.assertRaises(ContractError):
            transition_goal(state, "achieved")

    def test_contractless_achievement_fails_cleanly(self):
        with self.assertRaises(ContractError):
            transition_goal({"status": "active", "evidence": []}, "achieved")

    def test_duplicate_evidence_id_rejected(self):
        contract = {"outcome": "ship", "acceptance_checks": ["tests pass"]}
        state = {
            "status": "active",
            "goal_revision": 1,
            "run_id": "run-test",
            "criterion_ids": ["criterion-1"],
            "contract": contract,
            "contract_hash": hash_data(contract),
            "plan_hash": GOOD_HASH,
            "executions": [{"execution_id": "exe-1"}],
            "evidence": [{"evidence_id": "evd-1", "criterion_id": "criterion-1", "result": "accepted"}],
        }
        evidence = {
            "schema_version": 1,
            "evidence_id": "evd-1",
            "run_id": "run-test",
            "goal_revision": 1,
            "contract_hash": hash_data(contract),
            "plan_hash": "sha256:good",
            "slice_id": "slice-1",
            "criterion_id": "criterion-1",
            "verifier": "unit-test",
            "result": "accepted",
            "created_at": "2026-08-15T00:00:00Z",
            "execution_receipts": [self._exec()],
        }
        with self.assertRaises(ContractError):
            accept_evidence(state, evidence, None)

    def test_later_rejection_blocks_achievement(self):
        contract = {"outcome": "ship", "acceptance_checks": ["tests pass"]}
        state = {
            "status": "active",
            "goal_revision": 1,
            "criterion_ids": ["criterion-1"],
            "contract": contract,
            "evidence": [
                {"evidence_id": "evd-1", "criterion_id": "criterion-1", "result": "accepted"},
                {"evidence_id": "evd-2", "criterion_id": "criterion-1", "result": "rejected"},
            ],
        }
        with self.assertRaises(ContractError):
            transition_goal(state, "achieved")

    def test_evidence_must_match_recorded_execution_bytes(self):
        contract = {"outcome": "ship", "acceptance_checks": ["tests pass"]}
        receipt = self._exec()
        state = {
            "status": "active",
            "goal_revision": 1,
            "run_id": "run-test",
            "criterion_ids": ["criterion-1"],
            "contract": contract,
            "contract_hash": hash_data(contract),
            "plan_hash": GOOD_HASH,
            "executions": [receipt],
            "evidence": [],
        }
        forged = dict(receipt)
        forged["stdout_hash"] = "sha256:" + ("c" * 64)
        evidence = {
            "schema_version": 1,
            "evidence_id": "evd-1",
            "run_id": "run-test",
            "goal_revision": 1,
            "contract_hash": hash_data(contract),
            "plan_hash": GOOD_HASH,
            "slice_id": "slice-1",
            "criterion_id": "criterion-1",
            "verifier": "unit-test",
            "result": "accepted",
            "created_at": "2026-08-15T00:00:00Z",
            "execution_receipts": [forged],
        }
        with self.assertRaises(ContractError):
            accept_evidence(state, evidence, None)

    def test_terminal_goal_rejects_new_evidence(self):
        contract = {"outcome": "ship", "acceptance_checks": ["tests pass"]}
        receipt = self._exec()
        state = {
            "status": "achieved",
            "goal_revision": 1,
            "run_id": "run-test",
            "criterion_ids": ["criterion-1"],
            "contract": contract,
            "contract_hash": hash_data(contract),
            "plan_hash": GOOD_HASH,
            "executions": [receipt],
            "evidence": [],
        }
        evidence = {
            "schema_version": 1,
            "evidence_id": "evd-1",
            "run_id": "run-test",
            "goal_revision": 1,
            "contract_hash": hash_data(contract),
            "plan_hash": GOOD_HASH,
            "slice_id": "slice-1",
            "criterion_id": "criterion-1",
            "verifier": "unit-test",
            "result": "accepted",
            "created_at": "2026-08-15T00:00:00Z",
            "execution_receipts": [receipt],
        }
        with self.assertRaises(ContractError):
            accept_evidence(state, evidence, None)

    def test_superseded_ledger_entries_are_not_active(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "decisions.md").write_text(
                "# Decisions\nschema: resonance-ledger/1\n\n"
                "## dec-old: old call\n"
                "type: decision\ncreated: 2026-08-01\nstatus: superseded\n\n"
                "Use the old thing.\n\n"
                "## dec-new: new call\n"
                "type: decision\ncreated: 2026-08-02\nstatus: active\n\n"
                "Use the new thing.\n",
                encoding="utf-8",
            )
            ids = [e["id"] for e in active_entries(root)]
            self.assertEqual(ids, ["dec-new"])

    def test_manifest_contains_contract_fields(self):
        with tempfile.TemporaryDirectory() as d:
            cwd = os.getcwd()
            try:
                os.chdir(d)
                sk = Path(".agents/skills/ops/goal")
                sk.mkdir(parents=True)
                sk.joinpath("SKILL.md").write_text(
                    "---\n"
                    "name: resonance-ops-goal\n"
                    "description: drive goals\n"
                    "archetype: orchestration\n"
                    "invokes:\n"
                    "  - resonance-ops-qa\n"
                    "---\n",
                    encoding="utf-8",
                )
                data = manifest(Path(".agents/skills"))
                self.assertEqual(data[0]["schema_version"], 1)
                self.assertEqual(data[0]["authority"], "consequential")
                self.assertEqual(data[0]["invokes"], ["resonance-ops-qa"])
            finally:
                os.chdir(cwd)


if __name__ == "__main__":
    unittest.main()
