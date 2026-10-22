import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


consumer = load("consumer_check_test", ROOT / ".forge/consumer_check.py")
test_runner = load("forge_test_runner", ROOT / ".forge/tests/run.py")


class ConsumerCheckTests(unittest.TestCase):
    def fixture(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        managed = root / ".agents/skills/example/SKILL.md"
        managed.parent.mkdir(parents=True)
        managed.write_text("example\n", encoding="utf-8")
        manifest = root / ".resonance/framework-manifest.json"
        manifest.parent.mkdir()
        manifest.write_text(json.dumps({
            "schema": 1,
            "profile": "compiled",
            "files": {".agents/skills/example/SKILL.md": hashlib.sha256(managed.read_bytes()).hexdigest()},
        }), encoding="utf-8")
        return root, managed, manifest

    def test_legacy_compiled_consumer_missing_runtime_fails_read_only(self):
        root, managed, manifest = self.fixture()
        before = {managed: managed.read_bytes(), manifest: manifest.read_bytes()}
        result = consumer.check(root)
        self.assertFalse(result["ok"])
        self.assertEqual("pass", result["checks"][0]["status"])
        self.assertIn("forge_runtime", result["failed"])
        self.assertEqual(before, {managed: managed.read_bytes(), manifest: manifest.read_bytes()})

    def test_project_lock_without_verifier_fails(self):
        root, _, _ = self.fixture()
        forge = root / ".forge"
        forge.mkdir()
        for name in ("forge.py", "validate_skill.py", "eval_integrity.py"):
            (forge / name).write_text("raise SystemExit(0)\n", encoding="utf-8")
        lock = root / ".resonance/project-skills.lock.json"
        lock.write_text('{"schema_version":1,"skills":[]}\n', encoding="utf-8")
        result = consumer.check(root)
        self.assertIn("project_skills", result["failed"])
        verifier_check = next(check for check in result["checks"] if check["name"] == "project_skills")
        self.assertEqual("fail", verifier_check["status"])
        self.assertIn("missing", verifier_check["reason"])

    def test_owned_hash_mismatch_fails(self):
        root, managed, _ = self.fixture()
        managed.write_text("changed\n", encoding="utf-8")
        result = consumer.check(root)
        self.assertFalse(result["ok"])
        self.assertEqual([".agents/skills/example/SKILL.md"], result["checks"][0]["mismatched"])

    def test_manifest_path_escape_is_rejected(self):
        root, _, manifest = self.fixture()
        manifest.write_text(json.dumps({"profile": "compiled", "files": {"../escape": "0" * 64}}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "escapes consumer root"):
            consumer.owned_files(root)

    def test_unknown_profile_is_rejected(self):
        root, _, manifest = self.fixture()
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["profile"] = "other"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unknown consumer profile"):
            consumer.check(root)

    def test_unknown_manifest_schema_is_rejected(self):
        root, _, manifest = self.fixture()
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["schema"] = 999
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unsupported consumer manifest schema"):
            consumer.check(root)

    def test_powershell_path_literal_escapes_apostrophes(self):
        self.assertEqual("'C:\\project\\owner''s\\resonance.ps1'", consumer.powershell_literal("C:\\project\\owner's\\resonance.ps1"))

    @unittest.skipUnless(shutil.which("pwsh") or shutil.which("powershell"), "PowerShell unavailable")
    def test_installed_powershell_parser_path(self):
        root, _, _ = self.fixture()
        (root / "resonance.ps1").write_text("Write-Host 'valid'\n", encoding="utf-8")
        result = consumer.check(root)
        powershell = next(check for check in result["checks"] if check["name"] == "powershell_syntax")
        self.assertEqual("pass", powershell["status"], powershell)

    def test_source_test_runner_refuses_installed_consumer(self):
        root, _, _ = self.fixture()
        stderr = StringIO()
        with mock.patch.object(test_runner, "ROOT", root), redirect_stderr(stderr):
            self.assertEqual(2, test_runner.main())
        self.assertIn("consumer_check.py", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
