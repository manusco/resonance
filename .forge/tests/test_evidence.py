import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FORGE = ROOT / ".forge"
sys.path.insert(0, str(FORGE))

import evidence
from test_eval_schemas import load, validate


class EvidenceTests(unittest.TestCase):
    def manifest_args(self, exit_state="COMPLETE"):
        return {
            "exit_state": exit_state,
            "cases": [evidence.hash_item("case", b"case")],
            "skills": [],
            "instructions_hash": evidence.sha256_bytes(b"instructions"),
            "models": {"answerer_id": "model-a", "judge_id": "model-b"},
            "commands": [],
            "command_fingerprints": {},
            "repetitions": 1,
            "thresholds": {"pass": 1},
            "host": "test",
            "tool_profile": "none",
            "permission_profile": "read-only",
            "results": [],
            "summary": {"replay_envelope": {"prompt_hash": evidence.sha256_bytes(b"prompt")}},
        }

    def test_hashes_are_deterministic_and_content_addressed(self):
        self.assertEqual(evidence.sha256_bytes(b"same"), evidence.sha256_bytes(b"same"))
        self.assertNotEqual(evidence.sha256_bytes(b"same"), evidence.sha256_bytes(b"different"))

    def test_command_redaction_removes_common_secret_forms(self):
        command = "agent --api-key=alpha --password beta TOKEN=gamma Authorization: Bearer delta"
        redacted = evidence.redact_command(command)
        for secret in ("alpha", "beta", "gamma", "delta"):
            self.assertNotIn(secret, redacted)
        self.assertGreaterEqual(redacted.count("[REDACTED]"), 4)

    def test_repository_memory_and_generated_roots_are_refused(self):
        for candidate in (ROOT / ".resonance" / "evidence", ROOT / ".agents" / "evidence",
                          ROOT / ".forge" / "skills" / "evidence"):
            with self.assertRaises(ValueError):
                evidence.validate_evidence_root(candidate, ROOT, explicit=True)

    def test_runs_are_immutable_addressable_and_latest_is_only_a_pointer(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = evidence.EvidenceRun(root=root, repo=ROOT, runner=FORGE / "evidence.py",
                                         runner_id="test", baseline_id="base-1")
            first_path = first.write(**self.manifest_args(), result_payloads={"result.json": {"ok": True}})
            second = evidence.EvidenceRun(root=root, repo=ROOT, runner=FORGE / "evidence.py",
                                          runner_id="test", baseline_id="base-1")
            second_path = second.write(**self.manifest_args())
            self.assertNotEqual(first_path, second_path)
            self.assertTrue(first_path.exists())
            pointer = json.loads((root / "latest.json").read_text(encoding="utf-8"))
            self.assertEqual(pointer["run_id"], second.run_id)
            self.assertNotIn("repository", pointer)
            manifest = json.loads(second_path.read_text(encoding="utf-8"))
            validate(manifest, load("evidence-manifest.schema.json"))
            replay = manifest["summary"]["replay_envelope"]
            self.assertEqual(replay["baseline_id"], "base-1")
            self.assertIn("changed_path_hashes", replay)
            self.assertIn("environment", replay)
            self.assertEqual(manifest["repository"]["dirty"],
                             bool(manifest["repository"]["changed_paths"]))
            self.assertEqual(set(replay["changed_path_hashes"]),
                             set(manifest["repository"]["changed_paths"]))

    def test_failed_runs_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            run = evidence.EvidenceRun(root=Path(directory), repo=ROOT,
                                       runner=FORGE / "evidence.py", runner_id="failed")
            path = run.write(**self.manifest_args(exit_state="FAILED"))
            manifest = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["exit_state"], "FAILED")

    def test_promotion_requires_complete_provenance(self):
        with self.assertRaisesRegex(ValueError, "baseline ID"):
            evidence.require_promotion_provenance(
                evidence_root="x", baseline_id="", identities={"agent": "a"},
                revisions={"agent": "r"},
            )
        evidence.require_promotion_provenance(
            evidence_root="x", baseline_id="base", identities={"agent": "a"},
            revisions={"agent": "r"},
        )


if __name__ == "__main__":
    unittest.main()
