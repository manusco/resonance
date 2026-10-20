import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


evals = load("run_evals_security", ROOT / ".forge" / "run_evals.py")
orch = load("orch_eval_security", ROOT / ".forge" / "orch_eval.py")
model_cli = load("model_cli_security", ROOT / ".forge" / "exec" / "model_cli.py")


class EvalSecurityTests(unittest.TestCase):
    def test_rejects_absolute_parent_and_sensitive_paths(self):
        for path in (str(ROOT / "README.md"), "../README.md", ".env", ".git/config"):
            with self.subTest(path=path), self.assertRaises((ValueError, OSError)):
                evals.contained_fixture(path)

    def test_rejects_symlink_escape_when_supported(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as td, tempfile.TemporaryDirectory() as outside:
            link = Path(td) / "escape.txt"
            target = Path(outside) / "secret.txt"
            target.write_text("secret", encoding="utf-8")
            try:
                link.symlink_to(target)
            except OSError:
                self.skipTest("symlinks are unavailable")
            with self.assertRaises(ValueError):
                evals.contained_fixture(link.relative_to(ROOT).as_posix())

    @mock.patch("subprocess.run")
    def test_model_nonzero_exit_is_failure_and_preserves_streams(self, run):
        run.return_value = subprocess.CompletedProcess([], 7, "plausible answer", "crash detail")
        with self.assertRaises(evals.ModelFailure) as caught:
            evals.run_model(["model"], "prompt")
        self.assertEqual(caught.exception.stdout, "plausible answer")
        self.assertEqual(caught.exception.stderr, "crash detail")

    @mock.patch.object(evals, "run_model", return_value='["false"]')
    def test_judge_rejects_non_boolean_json(self, _run):
        self.assertEqual(evals.judge(["judge"], "q", "o", ["r"]), [False])

    def test_holdout_must_be_outside_repository(self):
        with self.assertRaises(ValueError):
            evals.holdout_cases(str(ROOT / ".forge"))

    def test_score_refuses_missing_inputs_before_model_calls(self):
        with mock.patch.object(evals, "run_model") as run_model:
            self.assertEqual(evals.main(["--score"]), 2)
        run_model.assert_not_called()

    def test_score_does_not_use_automatic_answerer_default(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            holdout = root / "holdout"
            holdout.mkdir()
            case = {"skill_path": "ops/goal", "skill": evals.skill_name(
                evals.skill_md_for_rel("ops/goal")), "query": "test query",
                "expected_behavior": ["states a bounded next step"]}
            (holdout / "case.json").write_text(json.dumps(case), encoding="utf-8")
            argv = ["--score", "--holdout-dir", str(holdout), "--evidence-root", str(root / "evidence"),
                    "--baseline-id", "base-1", "--judge-cmd", "judge", "--model-id", "answerer-v1",
                    "--judge-id", "judge-v1"]
            output = io.StringIO()
            with mock.patch.object(evals, "_has", return_value=True), \
                 mock.patch.object(evals, "run_model") as run_model, \
                 contextlib.redirect_stdout(output):
                self.assertEqual(evals.main(argv), 2)
            run_model.assert_not_called()
            self.assertIn("--score requires --model-cmd", output.getvalue())

    def test_scored_operator_arguments_accept_separate_external_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            holdout = root / "holdout"
            holdout.mkdir()
            case = {"skill_path": "ops/goal", "skill": evals.skill_name(
                evals.skill_md_for_rel("ops/goal")), "query": "test query",
                "expected_behavior": ["states a bounded next step"]}
            (holdout / "case.json").write_text(json.dumps(case), encoding="utf-8")
            self.assertIsNone(evals.score_configuration_error(
                check=False, holdout_dir=str(holdout), evidence_root=str(root / "evidence"),
                model_cmd="answerer --model a", judge_cmd="judge --model b",
                model_id="vendor/answerer-v1", judge_id="vendor/judge-v1", baseline_id="base-1"))
            self.assertEqual(len(evals.holdout_cases(str(holdout))), 1)

    def test_documented_score_arguments_reach_pre_model_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            holdout = root / "holdout"
            holdout.mkdir()
            case = {"skill_path": "ops/goal", "skill": evals.skill_name(
                evals.skill_md_for_rel("ops/goal")), "query": "test query",
                "expected_behavior": ["states a bounded next step"]}
            (holdout / "case.json").write_text(json.dumps(case), encoding="utf-8")
            args = ["--score", "--holdout-dir", str(holdout), "--evidence-root", str(root / "evidence"),
                    "--model-cmd", "answerer --model a", "--model-id", "vendor/answerer-v1",
                    "--judge-cmd", "judge --model b", "--judge-id", "vendor/judge-v1",
                    "--baseline-id", "baseline-1", "--reps", "3"]
            with mock.patch.object(evals.eval_integrity, "verify", return_value=["stop before model call"]), \
                 mock.patch.object(evals, "run_model") as run_model:
                self.assertEqual(evals.main(args), 1)
            run_model.assert_not_called()

    def test_scored_operator_rejects_same_commands_and_model_ids(self):
        base = {"check": False, "holdout_dir": "/private/holdout",
                "evidence_root": "/private/evidence", "model_cmd": "model", "judge_cmd": "judge",
                "model_id": "provider/a", "judge_id": "provider/b", "baseline_id": "base-1"}
        self.assertIn("commands", evals.score_configuration_error(**{**base, "judge_cmd": "model"}))
        self.assertIn("model-id", evals.score_configuration_error(**{**base, "judge_id": "provider/a"}))
        self.assertIn("baseline-id", evals.score_configuration_error(**{**base, "baseline_id": " "}))

    def test_skill_reference_cannot_escape(self):
        with self.assertRaises(ValueError):
            evals.skill_md_for_rel("../../../outside")
        for path in ("C:\\outside", 3):
            with self.subTest(path=path), self.assertRaises(ValueError):
                evals.skill_md_for_rel(path)

    def test_equivalent_commands_are_same_identity(self):
        self.assertTrue(evals.same_command("same-model --flag", "same-model    --flag"))

    def test_orchestration_fixture_paths_reject_absolute_and_traversal(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory) / "work"
            work.mkdir()
            for path in (str(Path(directory) / "outside.txt"), "../outside.txt", "C:\\outside.txt"):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    orch.contained_fixture_path(work, path)

    def test_orchestration_fixture_paths_reject_symlink_escape(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            work = Path(directory) / "work"
            work.mkdir()
            target = Path(outside) / "sentinel.txt"
            target.write_text("unchanged", encoding="utf-8")
            link = work / "escape"
            try:
                link.symlink_to(Path(outside), target_is_directory=True)
            except OSError:
                self.skipTest("symlinks are unavailable")
            with self.assertRaises(ValueError):
                orch.contained_fixture_path(work, "escape/sentinel.txt")
            self.assertEqual(target.read_text(encoding="utf-8"), "unchanged")

    def test_orchestration_case_rejects_escape_before_agent_or_file_write(self):
        with tempfile.TemporaryDirectory() as directory:
            outside = Path(directory) / "sentinel.txt"
            case = {"name": "escape", "skill": "ops/goal", "task": "no-op",
                    "fixture": {"files": {str(outside): "modified"}},
                    "assert": {"type": "contains", "any": ["done"]}}
            with mock.patch.object(orch.subprocess, "run") as run:
                with self.assertRaisesRegex(ValueError, "invalid orchestration case"):
                    orch.run_case(["agent"], case)
            run.assert_not_called()
            self.assertFalse(outside.exists())

    def test_orchestration_staging_paths_reject_escape(self):
        with self.assertRaises(ValueError):
            orch.case_skill_paths({"skill": "ops/goal", "trace_assert": {
                "allowed_skills": ["../../outside"]}})

    def test_orchestration_fixture_layout_rejects_path_conflicts(self):
        for paths in ({"src/a": "file", "src/a/child": "child"},
                      {"src/a": "one", "src/./a": "two"}):
            with self.subTest(paths=paths), self.assertRaisesRegex(ValueError, "overlap"):
                orch.validate_fixture_layout(paths)

    def test_orchestration_staging_rejects_nested_symlinks_before_copy(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory) / "skills"
            source = root / "ops" / "goal"
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text("---\nname: goal\n---\n", encoding="utf-8")
            secret = Path(outside) / "secret.md"
            secret.write_text("outside", encoding="utf-8")
            try:
                (source / "reference.md").symlink_to(secret)
            except OSError:
                self.skipTest("symlinks are unavailable")
            work = Path(directory) / "fixture"
            work.mkdir()
            case = {"skill": "ops/goal", "trace_assert": {}}
            with mock.patch.object(orch, "SKILLS", root), self.assertRaisesRegex(ValueError, "symlink"):
                orch.stage_framework(work, case)
            self.assertFalse((work / ".agents").exists())
            self.assertEqual(secret.read_text(encoding="utf-8"), "outside")

    def test_malformed_orchestration_trace_fields_return_problems(self):
        case = {"name": "bad", "skill": "ops/goal", "task": "task",
                "fixture": {"files": {"src/a.txt": 3}},
                "assert": [], "trace_assert": {"allowed_skills": "ops/security",
                                                "ordered_subsequence": [None, {}, {"nonsense": "x"}]}}
        problems = orch.check_case(case)
        self.assertTrue(any("contents must be strings" in problem for problem in problems))
        self.assertTrue(any("assert must be an object" in problem for problem in problems))
        self.assertTrue(any("ordered_subsequence items" in problem for problem in problems))
        self.assertTrue(any("constrain at least one trace field" in problem for problem in problems))
        self.assertTrue(any("unknown fields" in problem for problem in problems))


class ProviderBindingTests(unittest.TestCase):
    def test_foreign_key_cannot_fall_back_to_openai(self):
        env = {"ANTHROPIC_API_KEY": "foreign", "MODEL_NAME": "gpt-test"}
        with mock.patch.dict(os.environ, env, clear=True), self.assertRaises(ValueError):
            model_cli.provider_config()

    def test_openai_profile_binds_key_and_endpoint(self):
        env = {"MODEL_PROVIDER": "openai", "OPENAI_API_KEY": "key", "MODEL_NAME": "gpt-test"}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(model_cli.provider_config(), ("key", "https://api.openai.com/v1", "gpt-test"))

    def test_provider_key_cannot_use_custom_endpoint(self):
        env = {"MODEL_PROVIDER": "openai", "OPENAI_API_KEY": "key", "MODEL_NAME": "gpt-test",
               "MODEL_BASE_URL": "https://example.test/v1"}
        with mock.patch.dict(os.environ, env, clear=True), self.assertRaises(ValueError):
            model_cli.provider_config()


if __name__ == "__main__":
    unittest.main()
