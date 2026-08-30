import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("promotion_eval", ROOT / ".forge" / "promotion_eval.py")
promotion_eval = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(promotion_eval)
HEX = "a" * 64


def manifest(path: Path, kind: str, *, state: str = "COMPLETE", gates=None,
             candidate_id: str = "candidate"):
    required = promotion_eval.REQUIRED_GATES_BY_KIND[kind]
    gate_map = {gate: "PASS" for gate in required}
    gate_map.update(gates or {})
    value = {
        "schema_version": 1, "run_id": f"run-{kind}",
        "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "ended_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "repository": {"git_sha": "a" * 40, "dirty": False, "changed_paths": []},
        "runner": {"id": kind, "hash": HEX},
        "cases": [{"id": f"{kind}-case", "hash": HEX}],
        "skills": [{"id": "strategy/brief", "hash": HEX}],
        "instructions": HEX,
        "models": {"answerer_id": "answerer", "judge_id": "judge"},
        "commands": [{"id": "runner", "hash": HEX}],
        "execution": {
            "repetitions": 1, "thresholds": {}, "host": "test",
            "tool_profile": "test", "permission_profile": "sandbox",
            "cost": {"currency": "USD", "amount": 0}, "latency_ms": 1,
        },
        "results": [{"id": f"{kind}-result", "hash": HEX}],
        "summary": {"candidate_id": candidate_id, "evidence_kind": kind, "gates": gate_map},
        "exit_state": state,
    }
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


class PromotionEvaluatorTests(unittest.TestCase):
    def run_verdict(self, paths, **kwargs):
        with patch.object(promotion_eval, "git_state", return_value=("a" * 40, False, [])):
            return promotion_eval.verdict("candidate", paths, repo=ROOT, **kwargs)

    def test_missing_evidence_is_incomplete(self):
        result = self.run_verdict([])
        self.assertEqual("INCOMPLETE", result["outcome"])
        self.assertEqual("EVIDENCE_INTEGRITY", result["failed_gate"])

    def test_all_required_kinds_promote(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = [manifest(root / f"{kind}.json", kind) for kind in
                     ("structural", "routing_public", "routing_protected", "orchestration")]
            self.assertEqual("PROMOTE", self.run_verdict(paths)["outcome"])

    def test_schema_invalid_manifest_is_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = manifest(Path(tmp) / "structural.json", "structural")
            value = json.loads(path.read_text(encoding="utf-8"))
            del value["runner"]
            path.write_text(json.dumps(value), encoding="utf-8")
            result = self.run_verdict([path], required_kinds={"structural"})
            self.assertEqual("INCOMPLETE", result["outcome"])
            self.assertTrue(any("schema" in reason and "runner" in reason for reason in result["reasons"]))

    def test_missing_required_gate_is_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = manifest(Path(tmp) / "structural.json", "structural")
            value = json.loads(path.read_text(encoding="utf-8"))
            del value["summary"]["gates"]["STRUCTURAL_INTEGRITY"]
            path.write_text(json.dumps(value), encoding="utf-8")
            result = self.run_verdict([path], required_kinds={"structural"})
            self.assertEqual("INCOMPLETE", result["outcome"])
            self.assertTrue(any("missing required gates" in reason for reason in result["reasons"]))

    def test_candidate_mismatch_is_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = manifest(Path(tmp) / "structural.json", "structural", candidate_id="other")
            result = self.run_verdict([path], required_kinds={"structural"})
            self.assertEqual("INCOMPLETE", result["outcome"])
            self.assertTrue(any("candidate_id" in reason for reason in result["reasons"]))

    def test_duplicate_evidence_kind_is_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = manifest(root / "one.json", "structural")
            second = manifest(root / "two.json", "structural")
            result = self.run_verdict([first, second], required_kinds={"structural"})
            self.assertEqual("INCOMPLETE", result["outcome"])
            self.assertTrue(any("duplicate evidence kind" in reason for reason in result["reasons"]))

    def test_high_priority_failure_rejects_before_quality(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = [manifest(root / f"{kind}.json", kind) for kind in
                     ("structural", "routing_public", "routing_protected")]
            paths.append(manifest(root / "orchestration.json", "orchestration",
                                  gates={"SAFETY_AUTHORITY": "FAIL", "TASK_QUALITY": "FAIL"}))
            result = self.run_verdict(paths)
            self.assertEqual("REJECT", result["outcome"])
            self.assertEqual("SAFETY_AUTHORITY", result["failed_gate"])

    def test_incomplete_run_cannot_promote(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = manifest(Path(tmp) / "structural.json", "structural", state="INCOMPLETE")
            self.assertEqual("INCOMPLETE", self.run_verdict([path], required_kinds={"structural"})["outcome"])

    def test_dirty_path_mismatch_is_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = manifest(Path(tmp) / "structural.json", "structural")
            with patch.object(promotion_eval, "git_state", return_value=("a" * 40, True, ["x.py"])):
                result = promotion_eval.verdict("candidate", [path], repo=ROOT,
                                                allow_dirty=True, required_kinds={"structural"})
            self.assertEqual("INCOMPLETE", result["outcome"])


if __name__ == "__main__":
    unittest.main()
