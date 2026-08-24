import json
import sys
import tempfile
import time
import unittest
from unittest import mock
from pathlib import Path


FORGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FORGE))
import trace_adapters  # noqa: E402
import orch_eval  # noqa: E402


NOW = "2026-08-24T10:00:00Z"


def event(sequence, *, actor="ops/audit", kind="INVOKE", target="ops/security",
          authority="READ", artifact="report.md", mutation="NONE",
          approval="NOT_REQUIRED", outcome="SUCCEEDED"):
    return {
        "run_id": "case-1", "sequence": sequence, "timestamp": NOW,
        "actor": actor, "event": kind, "target": target, "authority": authority,
        "artifact": artifact, "mutation_mode": mutation,
        "approval_state": approval, "outcome": outcome,
    }


def loaded(*events, level=1):
    return trace_adapters.TraceLoad("COMPLETE", list(events), level, "test trace")


class InvocationTraceTests(unittest.TestCase):
    def test_case_timeout_stops_a_direct_host_process(self):
        case = {
            "name": "timeout", "skill": "ops/example", "task": "wait",
            "fixture": {"files": {"input.txt": "x"}},
            "assert": {"type": "contains", "any": ["done"]},
        }
        started = time.monotonic()
        with mock.patch.object(orch_eval, "stage_framework"):
            result = orch_eval.run_case(
                [sys.executable, "-c", "import time; time.sleep(5)"], case, timeout=1,
            )
        self.assertFalse(result["passed"])
        self.assertIn("timed out", result["detail"])
        self.assertLess(time.monotonic() - started, 3)

    def test_timeout_retains_and_evaluates_partial_opencode_trace(self):
        host_event = json.dumps({
            "type": "tool_use", "timestamp": 1787554194685,
            "part": {"tool": "skill", "state": {"status": "completed", "input": {
                "name": "ops/security"
            }}}
        })
        case = {
            "name": "partial", "skill": "ops/example", "task": "wait",
            "fixture": {"files": {"input.txt": "x"}},
            "assert": {"type": "contains", "any": ["done"]},
            "trace_assert": {
                "minimum_assurance": 1,
                "ordered_subsequence": [{"event": "INVOKE", "target": "ops/security"}],
                "allowed_skills": ["ops/security"], "forbidden_skills": [],
            },
        }
        script = f"import time; print({host_event!r}, flush=True); time.sleep(5)"
        with tempfile.TemporaryDirectory() as trace_td, \
             mock.patch.object(orch_eval, "stage_framework"):
            trace_root = Path(trace_td)
            result = orch_eval.run_case(
                [sys.executable, "-c", script], case, timeout=1,
                trace_root=trace_root, trace_adapter="opencode-json-v1",
            )
            self.assertTrue((trace_root / "partial.jsonl").is_file())
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["trace"]["status"], "PASS")

    def test_stage_framework_exposes_only_case_runtime_skills(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source_skills = root / "source-skills"
            skill = source_skills / "ops" / "example"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("example", encoding="utf-8")
            (skill / "evals").mkdir()
            (skill / "evals" / "case.json").write_text("{}", encoding="utf-8")
            unused = source_skills / "ops" / "unused"
            unused.mkdir(parents=True)
            (unused / "SKILL.md").write_text("unused", encoding="utf-8")
            source_repo = root / "source-repo"
            source_repo.mkdir()
            (source_repo / "AGENTS.md").write_text("rules", encoding="utf-8")
            fixture = root / "fixture"
            fixture.mkdir()
            with mock.patch.object(orch_eval, "SKILLS", source_skills), \
                 mock.patch.object(orch_eval, "REPO", source_repo):
                orch_eval.stage_framework(fixture, {
                    "skill": "ops/example",
                    "trace_assert": {"allowed_skills": [], "forbidden_skills": []},
                })
            self.assertEqual(
                (fixture / ".agents" / "skills" / "ops" / "example" / "SKILL.md").read_text(),
                "example",
            )
            self.assertFalse((fixture / ".agents" / "skills" / "ops" / "example" / "evals").exists())
            self.assertFalse((fixture / ".agents" / "skills" / "ops" / "unused").exists())
            self.assertEqual((fixture / "AGENTS.md").read_text(), "rules")

    def test_trace_run_requires_matching_user_approved_operating_contract(self):
        contract = {
            "schema_version": 1, "contract_version": 1,
            "approval": {"state": "APPROVED", "approver": "USER"},
            "canary": {"host": "codex", "adapter": "external-jsonl-v1"},
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "contract.json"
            path.write_text(json.dumps(contract), encoding="utf-8")
            loaded_contract = trace_adapters.require_operating_contract(
                path, "external-jsonl-v1", "codex")
            self.assertEqual(loaded_contract["canary"]["host"], "codex")
            with self.assertRaisesRegex(ValueError, "host"):
                trace_adapters.require_operating_contract(path, "external-jsonl-v1", "other")

    def test_read_only_invocation_passes_at_level_one(self):
        result = trace_adapters.evaluate_trace({
            "minimum_assurance": 1,
            "ordered_subsequence": [{"event": "INVOKE", "target": "ops/security"}],
            "allowed_skills": ["ops/security"], "max_fan_out": 1,
        }, loaded(event(1)), set())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["achieved_assurance"], 1)

    def test_missing_or_wrong_order_event_fails(self):
        result = trace_adapters.evaluate_trace({"ordered_subsequence": [
            {"event": "REVIEW"}, {"event": "INVOKE"}
        ]}, loaded(event(1), event(2, kind="REVIEW")), set())
        self.assertEqual(result["status"], "FAIL")

    def test_forbidden_invocation_and_fan_out_fail(self):
        result = trace_adapters.evaluate_trace({
            "forbidden_skills": ["ops/ship"], "max_fan_out": 1,
        }, loaded(event(1), event(2, target="ops/ship")), set())
        self.assertEqual(result["status"], "FAIL")

    def test_level_one_cannot_prove_approval_boundary(self):
        result = trace_adapters.evaluate_trace({
            "approval_before_side_effect": True,
        }, loaded(
            event(1, kind="APPROVE", target="user", authority="APPROVE",
                  approval="APPROVED"),
            event(2, kind="EXECUTE", authority="EXECUTE", mutation="EXTERNAL"),
        ), set())
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["checks"][0]["minimum_assurance"], 2)

    def test_side_effect_before_approval_fails(self):
        result = trace_adapters.evaluate_trace({
            "approval_before_side_effect": True,
        }, loaded(
            event(1, kind="EXECUTE", authority="EXECUTE", mutation="EXTERNAL"),
            event(2, kind="APPROVE", target="user", authority="APPROVE",
                  approval="APPROVED"),
        ), set())
        self.assertEqual(result["status"], "FAIL")

    def test_artifact_owner_and_world_state_correlation_reach_level_three(self):
        write = event(1, actor="engineering/backend", kind="EXECUTE",
                      target="engineering/backend", authority="MODIFY",
                      artifact="src/app.py", mutation="WRITE")
        result = trace_adapters.evaluate_trace({
            "artifact_access": [{"artifact": "src/app.py", "owner": "engineering/backend",
                                 "allowed_mutations": ["MODIFY"]}],
            "correlate_world_state": True,
        }, loaded(write), {"src/app.py"})
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["achieved_assurance"], 3)

    def test_unexpected_write_and_fabricated_trace_fail(self):
        write = event(1, actor="engineering/backend", kind="EXECUTE",
                      authority="MODIFY", artifact="src/claimed.py", mutation="WRITE")
        result = trace_adapters.evaluate_trace({
            "correlate_world_state": True,
        }, loaded(write), {"src/actual.py"})
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("src/actual.py", result["checks"][0]["detail"])
        self.assertIn("src/claimed.py", result["checks"][0]["detail"])

    def test_unavailable_trace_is_incomplete(self):
        result = trace_adapters.evaluate_trace({}, trace_adapters.TraceLoad(
            "INCOMPLETE", [], 0, "unsupported"), set())
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertFalse(result["passed"])

    def test_agent_writable_trace_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            fixture = Path(td)
            trace = fixture / "trace.jsonl"
            trace.write_text(json.dumps(event(1)) + "\n", encoding="utf-8")
            result = trace_adapters.load_external_jsonl(trace, fixture, "case-1")
        self.assertEqual(result.status, "INCOMPLETE")
        self.assertIn("agent-writable", result.detail)

    def test_external_jsonl_requires_matching_run_and_contiguous_sequence(self):
        with tempfile.TemporaryDirectory() as fixture_td, tempfile.TemporaryDirectory() as trace_td:
            fixture = Path(fixture_td)
            trace = Path(trace_td) / "case.jsonl"
            trace.write_text(json.dumps(event(2)) + "\n", encoding="utf-8")
            result = trace_adapters.load_external_jsonl(trace, fixture, "case-1")
        self.assertEqual(result.status, "INCOMPLETE")
        self.assertIn("contiguous", result.detail)

    def test_opencode_read_event_is_level_two_and_relative(self):
        with tempfile.TemporaryDirectory() as td:
            fixture = Path(td)
            raw = json.dumps({
                "type": "tool_use", "timestamp": 1787554194685,
                "part": {"tool": "read", "state": {"status": "completed", "input": {
                    "filePath": str(fixture / "README.md")
                }}}
            })
            result = trace_adapters.load_opencode_jsonl(raw, fixture, "case-1")
        self.assertEqual(result.status, "COMPLETE")
        self.assertEqual(result.assurance_level, 2)
        self.assertEqual(result.events[0]["artifact"], "README.md")
        self.assertEqual(result.events[0]["authority"], "READ")

    def test_opencode_write_event_can_correlate_to_world_state(self):
        with tempfile.TemporaryDirectory() as td:
            fixture = Path(td)
            raw = json.dumps({
                "type": "tool_use", "timestamp": 1787554194685,
                "part": {"tool": "write", "state": {"status": "completed", "input": {
                    "filePath": str(fixture / "result.md")
                }}}
            })
            loaded_trace = trace_adapters.load_opencode_jsonl(raw, fixture, "case-1")
            result = trace_adapters.evaluate_trace({"correlate_world_state": True},
                                                   loaded_trace, {"result.md"})
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["achieved_assurance"], 3)

    def test_opencode_skill_tool_becomes_invocation(self):
        raw = json.dumps({
            "type": "tool_use", "timestamp": 1787554194685,
            "part": {"tool": "skill", "state": {"status": "completed", "input": {
                "name": "ops/security"
            }}}
        })
        with tempfile.TemporaryDirectory() as td:
            result = trace_adapters.load_opencode_jsonl(raw, Path(td), "case-1")
        self.assertEqual(result.events[0]["event"], "INVOKE")
        self.assertEqual(result.events[0]["target"], "ops/security")

    def test_opencode_frontmatter_skill_name_maps_to_library_path(self):
        raw = json.dumps({
            "type": "tool_use", "timestamp": 1787554194685,
            "part": {"tool": "skill", "state": {"status": "completed", "input": {
                "name": "resonance-ops-security"
            }}}
        })
        with tempfile.TemporaryDirectory() as td:
            fixture = Path(td)
            skill = fixture / ".agents" / "skills" / "ops" / "security"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: resonance-ops-security\n---\n", encoding="utf-8",
            )
            result = trace_adapters.load_opencode_jsonl(raw, fixture, "case-1")
        self.assertEqual(result.events[0]["target"], "ops/security")

    def test_opencode_malformed_json_is_incomplete(self):
        with tempfile.TemporaryDirectory() as td:
            result = trace_adapters.load_opencode_jsonl("not-json", Path(td), "case-1")
        self.assertEqual(result.status, "INCOMPLETE")


if __name__ == "__main__":
    unittest.main()
