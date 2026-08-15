import importlib.util
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

    def test_skill_reference_cannot_escape(self):
        with self.assertRaises(ValueError):
            evals.skill_md_for_rel("../../../outside")

    def test_equivalent_commands_are_same_identity(self):
        self.assertTrue(evals.same_command("same-model --flag", "same-model    --flag"))


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
