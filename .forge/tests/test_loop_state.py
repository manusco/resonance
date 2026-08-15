"""Tests for the /goal bound enforcer (loop_state.py, stdlib only).

The whole point of loop_state.py is that the caps live in code, not prose. These
tests prove the four stops actually fire: total cap, per-slice attempts, the
duplicate-failure signature detector, and the whole-window stuck check, plus that
a run resumes from persisted state. This is the grounded proof that /goal cannot
run away.
"""
import io
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from contextlib import redirect_stdout
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "ops" / "goal" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import loop_state  # noqa: E402

GOOD_PLAN = "sha256:" + ("a" * 64)
GOOD_HASH = "sha256:" + ("b" * 64)


class LoopBoundTest(unittest.TestCase):
    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)
        # small, explicit caps so the tests are fast and legible
        loop_state.CAPS = {"max_slice_attempts": 3, "max_iters": 5, "stuck_window": 4}

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def _run(self, *argv) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            loop_state.main(list(argv))
        return buf.getvalue()

    def _contract(self):
        contract = {
            "outcome": "faster search",
            "acceptance_checks": ["benchmark improves", "docs updated"]
        }
        Path("goal_contract.json").write_text(json.dumps(contract), encoding="utf-8")
        self._run("start", "speed search", "--dod", "benchmark improves",
                  "--contract", "goal_contract.json", "--plan-hash", GOOD_PLAN)
        return contract

    def _execution(self, criterion="criterion-1"):
        return {
            "schema_version": 1,
            "execution_id": f"exe-{criterion}",
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
            "after_manifest_hash": GOOD_HASH,
            "artifact_hashes": [],
            "runner": "resonance-kernel-runner/1"
        }

    def _record_execution(self, criterion="criterion-1"):
        state_path = Path(".resonance/goal_state.json")
        state = json.loads(state_path.read_text(encoding="utf-8"))
        receipt = self._execution(criterion)
        state.setdefault("executions", []).append(receipt)
        state_path.write_text(json.dumps(state), encoding="utf-8")
        return receipt

    def _evidence(self, criterion="criterion-1", *, contract_hash=None, plan_hash=GOOD_PLAN):
        state = json.loads(Path(".resonance/goal_state.json").read_text(encoding="utf-8"))
        execution = self._record_execution(criterion)
        return {
            "schema_version": 1,
            "evidence_id": f"evd-{criterion}",
            "run_id": state["run_id"],
            "goal_revision": 1,
            "source_revision": "abc123",
            "contract_hash": contract_hash or state["contract_hash"],
            "plan_hash": plan_hash,
            "slice_id": "slice-1",
            "criterion_id": criterion,
            "execution_receipts": [execution],
            "fixture_manifest_hash": "sha256:fixture",
            "verifier": "unit-test",
            "result": "accepted",
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

    def test_continue_on_progress(self):
        self._run("start", "g", "--dod", "d")
        self.assertIn("CONTINUE", self._run("check", "slice-1", "advanced"))

    def test_stop_slice_after_attempts(self):
        self._run("start", "g", "--dod", "d")
        self._run("check", "slice-1", "failed")
        self._run("check", "slice-1", "failed")
        self.assertIn("STOP_SLICE", self._run("check", "slice-1", "failed"))

    def test_stop_stuck_on_repeated_signature(self):
        self._run("start", "g", "--dod", "d")
        # different slices (no slice cap) but the same failure signature
        self._run("check", "s1", "failed", "--sig", "test:AssertionError")
        self._run("check", "s2", "failed", "--sig", "test:AssertionError")
        out = self._run("check", "s3", "failed", "--sig", "test:AssertionError")
        self.assertIn("STOP_STUCK", out)
        self.assertIn("signature", out)

    def test_stop_cap_on_total_iters(self):
        self._run("start", "g", "--dod", "d")
        self.assertIn("CONTINUE", self._run("check", "a", "advanced"))
        self.assertIn("CONTINUE", self._run("check", "b", "advanced"))
        self.assertIn("CONTINUE", self._run("check", "c", "advanced"))
        self.assertIn("CONTINUE", self._run("check", "d", "advanced"))
        self.assertIn("STOP_CAP", self._run("check", "e", "advanced"))

    def test_resume_reads_persisted_state(self):
        self._run("start", "ship the ledger", "--dod", "validators green")
        self._run("check", "slice-1", "advanced")
        out = self._run("resume")
        self.assertIn("ship the ledger", out)
        self.assertIn("slice-1", out)

    def test_start_persists_contract_and_plan_hash(self):
        contract = {
            "outcome": "faster search",
            "acceptance_checks": ["benchmark improves"]
        }
        Path("goal_contract.json").write_text(json.dumps(contract), encoding="utf-8")
        self._run("start", "speed search", "--dod", "benchmark improves",
                  "--contract", "goal_contract.json", "--plan-hash", GOOD_PLAN)
        out = self._run("status")
        self.assertIn("faster search", out)
        self.assertIn(GOOD_PLAN, out)

    def test_contract_requires_plan_hash(self):
        contract = {"outcome": "faster search", "acceptance_checks": ["benchmark improves"]}
        Path("goal_contract.json").write_text(json.dumps(contract), encoding="utf-8")
        out = self._run("start", "speed search", "--contract", "goal_contract.json")
        self.assertIn("requires --plan-hash", out)
        self.assertIn("no active goal", self._run("status"))

    def test_contract_rejects_non_hash_plan_hash(self):
        contract = {"outcome": "faster search", "acceptance_checks": ["benchmark improves"]}
        Path("goal_contract.json").write_text(json.dumps(contract), encoding="utf-8")
        out = self._run("start", "speed search", "--contract", "goal_contract.json", "--plan-hash", "abc123")
        self.assertIn("sha256", out)
        self.assertIn("no active goal", self._run("status"))

    def test_stale_evidence_is_rejected(self):
        self._contract()
        evidence = self._evidence(contract_hash="sha256:" + ("c" * 64))
        Path("evidence.json").write_text(json.dumps(evidence), encoding="utf-8")
        out = self._run("evidence", "evidence.json")
        self.assertIn("evidence rejected", out)
        self.assertIn("contract hash mismatch", out)

    def test_cannot_achieve_without_all_evidence(self):
        self._contract()
        evidence = self._evidence("criterion-1")
        Path("evidence.json").write_text(json.dumps(evidence), encoding="utf-8")
        self.assertIn("evidence accepted", self._run("evidence", "evidence.json"))
        out = self._run("achieve")
        self.assertIn("cannot achieve goal", out)
        self.assertIn("criterion-2", out)

    def test_achieve_and_done_retain_history(self):
        self._contract()
        for criterion in ("criterion-1", "criterion-2"):
            Path(f"{criterion}.json").write_text(json.dumps(self._evidence(criterion)), encoding="utf-8")
            self.assertIn("evidence accepted", self._run("evidence", f"{criterion}.json"))
        self.assertIn("goal achieved", self._run("achieve"))
        self.assertIn("completed history retained", self._run("done"))
        history = json.loads(Path(".resonance/goal_history.json").read_text(encoding="utf-8"))
        self.assertEqual(len(history["completed"]), 1)
        self.assertFalse(Path(".resonance/goal_state.json").exists())
        self.assertTrue(Path(".resonance/evidence/evd-criterion-1.json").exists())

    def test_done_refuses_active_goal(self):
        self._contract()
        out = self._run("done")
        self.assertIn("cannot clear", out)
        self.assertTrue(Path(".resonance/goal_state.json").exists())

    def test_invalid_contract_blocks_start(self):
        out = self._run("start", "speed search", "--contract", "{}")
        self.assertIn("cannot start", out)
        self.assertIn("missing required", out)
        self.assertIn("no active goal", self._run("status"))

    def test_resume_with_no_goal(self):
        self.assertIn("no active goal", self._run("resume"))


if __name__ == "__main__":
    unittest.main()
