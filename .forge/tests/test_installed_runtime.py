"""Exercise the files a clean installation actually receives."""
from __future__ import annotations

import importlib.util
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("installed_runtime_update", ROOT / ".forge" / "update.py")
update = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = update
spec.loader.exec_module(update)


class InstalledRuntimeTests(unittest.TestCase):
    def run_cli(self, target: Path, relative: str, *args: str, env: dict | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(target / relative), *args], cwd=target, capture_output=True,
            text=True, encoding="utf-8", errors="replace", env=env, check=False,
        )

    def git(self, root: Path, *args: str) -> None:
        subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)

    def source_snapshot(self, root: Path) -> Path:
        source = root / "source"
        source.mkdir()
        for relative in (*update.MANAGED_ROOTS, "package.json"):
            origin = ROOT / relative
            destination = source / relative
            if origin.is_dir():
                shutil.copytree(
                    origin, destination,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
                )
            elif origin.is_file():
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(origin, destination)
        self.git(source, "init")
        self.git(source, "config", "user.email", "runtime-test@example.test")
        self.git(source, "config", "user.name", "Installed Runtime Test")
        self.git(source, "add", "--", *update.MANAGED_ROOTS, "package.json")
        self.git(source, "commit", "-m", "temporary installed runtime source")
        return source

    def seed_consumer_memory(self, target: Path) -> None:
        memory = target / ".resonance"
        (memory / "ledger").mkdir(parents=True)
        (memory / "02_memory.md").write_text(
            "# Project Memory\n\n## Decisions\nThe runtime install preserves the seeded memory recall beacon.\n",
            encoding="utf-8",
        )
        (memory / "ledger" / "metrics.md").write_text(
            "# Metrics\nschema: resonance-ledger/1\n\n"
            "## met-runtime-beacon: Installed runtime due check\n"
            "type: metric\ncreated: 2026-10-01\nstatus: active\nvalue: pending\n"
            "unit: check\nas_of: 2026-10-01\nsource: integration fixture\ndue: 2026-10-10\n\n"
            "The installed measurement due command must surface this beacon.\n",
            encoding="utf-8",
        )
        for name in ("decisions", "lessons", "customers", "experiments"):
            (memory / "ledger" / f"{name}.md").write_text(
                f"# {name.title()}\nschema: resonance-ledger/1\n\n", encoding="utf-8",
            )

    def test_complete_install_ships_a_closed_runtime(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = self.source_snapshot(root)
            installed = root / "installed"
            installed.mkdir()

            update.apply(source, installed)
            manifest = json.loads((installed / update.MANIFEST).read_text(encoding="utf-8"))
            self.assertEqual("source", manifest["profile"])
            self.assertTrue((installed / ".forge" / "recall.py").is_file())
            self.assertTrue((installed / ".forge" / "kernel" / "ledger.py").is_file())

            self.seed_consumer_memory(installed)
            env = dict(os.environ, RESONANCE_EMBED_CMD="")

            recall = self.run_cli(installed, ".forge/recall.py", "runtime install preserves seeded memory", env=env)
            self.assertEqual(0, recall.returncode, recall.stderr)
            self.assertIn("seeded memory recall beacon", recall.stdout)

            due = self.run_cli(installed, ".forge/measurement_due.py", "--date", "2026-10-22", env=env)
            self.assertEqual(0, due.returncode, due.stderr)
            self.assertIn("met-runtime-beacon", due.stdout)

            goal = self.run_cli(
                installed, ".forge/skills/ops/goal/scripts/loop_state.py", "status", env=env,
            )
            self.assertEqual(0, goal.returncode, goal.stderr)
            self.assertIn("no active goal", goal.stdout)

            check_fixture = root / "qa-fixture"
            (check_fixture / "tests").mkdir(parents=True)
            (check_fixture / "Makefile").write_text(
                f"test:\n\t{shlex.quote(sys.executable)} -m unittest discover -s tests\n",
                encoding="utf-8",
            )
            (check_fixture / "tests" / "test_fixture.py").write_text(
                "import os\nimport unittest\n\nclass FixtureTest(unittest.TestCase):\n"
                "    def test_runtime_check(self):\n"
                "        self.assertNotEqual(os.environ.get('FAIL_FIXTURE'), '1')\n",
                encoding="utf-8",
            )
            checks = self.run_cli(installed, ".forge/exec/run_checks.py", str(check_fixture), "--json", env=env)
            self.assertEqual(0, checks.returncode, checks.stderr)
            check_result = json.loads(checks.stdout)
            self.assertTrue(check_result["passed"], checks.stdout)
            self.assertEqual("make", check_result["checks"][0]["eco"])
            self.assertTrue(check_result["checks"][0]["passed"], checks.stdout)

            failed_env = dict(env, FAIL_FIXTURE="1")
            failed_checks = self.run_cli(
                installed, ".forge/exec/run_checks.py", str(check_fixture), "--json", env=failed_env,
            )
            self.assertEqual(1, failed_checks.returncode, failed_checks.stdout + failed_checks.stderr)
            self.assertFalse(json.loads(failed_checks.stdout)["passed"])

            consumer = self.run_cli(installed, ".forge/consumer_check.py", "--root", str(installed), env=env)
            self.assertEqual(0, consumer.returncode, consumer.stderr + consumer.stdout)
            consumer_result = json.loads(consumer.stdout)
            self.assertTrue(consumer_result["ok"], consumer.stdout)
            self.assertNotIn("forge_runtime", consumer_result["failed"])


if __name__ == "__main__":
    unittest.main()
