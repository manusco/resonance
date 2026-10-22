import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("eval_integrity_tested", ROOT / ".forge" / "eval_integrity.py")
integrity = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = integrity
spec.loader.exec_module(integrity)


class EvalIntegrityTests(unittest.TestCase):
    def test_snapshot_covers_evals_and_tests(self):
        files = integrity.snapshot()
        self.assertTrue(any("/evals/" in p for p in files))
        self.assertTrue(any(p.endswith("test_eval_integrity.py") for p in files))

    def test_snapshot_detects_deleted_or_changed_oracle(self):
        current = integrity.snapshot()
        path = next(iter(current))
        altered = dict(current)
        altered[path] = "0" * 64
        self.assertTrue(any(path in problem for problem in integrity.verify(altered)))

    def _isolated_repository(self, root: Path, *, files: list[str], optional: bool = False) -> tuple[Path, Path]:
        forge = root / ".forge"
        eval_dir = forge / "skills/ops/example/evals"
        eval_dir.mkdir(parents=True)
        (root / "fixtures").mkdir(exist_ok=True)
        case_path = eval_dir / "01.json"
        case_path.write_text(json.dumps({
            "skill": "resonance-ops-example",
            "query": "Use the attached evidence.",
            "files": files,
            "fixture_optional": optional,
            "expected_behavior": ["Ground the answer in the supplied file."],
        }), encoding="utf-8")
        return forge, case_path

    def test_snapshot_detects_referenced_fixture_mutation_and_deletion(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td).resolve()
            fixture = root / "fixtures/reference.md"
            fixture.parent.mkdir()
            fixture.write_text("approved source v1", encoding="utf-8")
            forge, _ = self._isolated_repository(
                root, files=["fixtures/reference.md", "fixtures/reference.md"]
            )
            with mock.patch.object(integrity, "REPO", root), mock.patch.object(integrity, "FORGE", forge):
                original = integrity.snapshot()
                self.assertEqual(1, sum(path == "fixtures/reference.md" for path in original))
                fixture.write_text("approved source v2", encoding="utf-8")
                changed = integrity.verify(original)
                self.assertTrue(any("changed oracle file: fixtures/reference.md" in p for p in changed))
                fixture.unlink()
                deleted = integrity.verify(original)
                self.assertTrue(any("missing required eval fixture fixtures/reference.md" in p for p in deleted))

    def test_snapshot_rejects_traversal_without_reading_outside_repository(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as outside:
            root = Path(td).resolve()
            outside_fixture = Path(outside) / "outside.txt"
            outside_fixture.write_text("must not be read", encoding="utf-8")
            forge, _ = self._isolated_repository(root, files=[f"../{outside_fixture.name}"])
            with mock.patch.object(integrity, "REPO", root), mock.patch.object(integrity, "FORGE", forge):
                problems = integrity.verify({})
            self.assertTrue(any("eval file escapes repository" in problem for problem in problems))

    def test_snapshot_rejects_symlinked_fixture_escape(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as outside:
            root = Path(td).resolve()
            outside_fixture = Path(outside) / "secret.md"
            outside_fixture.write_text("external content", encoding="utf-8")
            link = root / "fixtures/external.md"
            link.parent.mkdir()
            try:
                link.symlink_to(outside_fixture)
            except OSError:
                self.skipTest("symlinks are unavailable")
            forge, _ = self._isolated_repository(root, files=["fixtures/external.md"])
            with mock.patch.object(integrity, "REPO", root), mock.patch.object(integrity, "FORGE", forge):
                problems = integrity.verify({})
            self.assertTrue(any("eval file escapes repository" in problem for problem in problems))

    def test_missing_optional_fixture_is_not_added_to_oracle(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td).resolve()
            forge, _ = self._isolated_repository(root, files=["fixtures/future.md"], optional=True)
            with mock.patch.object(integrity, "REPO", root), mock.patch.object(integrity, "FORGE", forge):
                files = integrity.snapshot()
            self.assertFalse(any(path == "fixtures/future.md" for path in files))

    def test_framework_fixture_namespace_is_narrow(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td).resolve()
            framework_fixture = root / ".forge/fixtures/example.md"
            framework_fixture.parent.mkdir(parents=True)
            framework_fixture.write_text("public source evidence", encoding="utf-8")
            self.assertEqual(framework_fixture, integrity.contained_fixture(".forge/fixtures/example.md", root))
            with self.assertRaisesRegex(ValueError, "outside approved fixture roots"):
                integrity.contained_fixture(".forge/private/example.md", root)

    def test_framework_fixture_rejects_symlink_to_repository_sibling(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td).resolve()
            forge, _ = self._isolated_repository(root, files=[".forge/fixtures/alias.md"])
            fixture_root = forge / "fixtures"
            fixture_root.mkdir()
            private = forge / "private-config.md"
            private.write_text("repository-private", encoding="utf-8")
            alias = fixture_root / "alias.md"
            try:
                alias.symlink_to(private)
            except OSError:
                self.skipTest("symlinks are unavailable")
            with mock.patch.object(integrity, "REPO", root), mock.patch.object(integrity, "FORGE", forge):
                problems = integrity.verify({})
            self.assertTrue(any("escapes framework fixture namespace" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
