import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class LegacyManifestUpgradeTests(unittest.TestCase):
    def test_full_build_ignores_stale_project_owned_skill_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            target.mkdir()
            for relative in (".forge", ".agents", ".claude", ".cursor", ".opencode"):
                shutil.copytree(ROOT / relative, target / relative)
            for relative in ("README.md", "AGENTS.md", "CLAUDE.md"):
                shutil.copy2(ROOT / relative, target / relative)

            manifest = json.loads((ROOT / "docs/skill-manifest.json").read_text(encoding="utf-8"))
            stale = [entry for entry in manifest if entry["id"] != "resonance-strategy-blueprint"]
            (target / "docs").mkdir()
            (target / "docs/skill-manifest.json").write_text(
                json.dumps(stale, indent=2) + "\n", encoding="utf-8"
            )
            stale_bytes = (target / "docs/skill-manifest.json").read_bytes()
            private = target / ".agents/skills/company/private/SKILL.md"
            private.parent.mkdir(parents=True)
            private.write_text(
                "---\nname: company-private\ndescription: private fixture\narchetype: knowledge\n---\n",
                encoding="utf-8",
            )

            command = [sys.executable, str(target / ".forge/forge.py"), "build", "--all", "--host", "all", "--dry-run"]
            for state in ("stale", "missing"):
                with self.subTest(project_manifest=state):
                    result = subprocess.run(
                        command, cwd=target, capture_output=True, text=True,
                        encoding="utf-8", errors="replace",
                    )
                    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                    self.assertNotIn("docs/skill-manifest.json", result.stdout + result.stderr)
                if state == "stale":
                    self.assertEqual(stale_bytes, (target / "docs/skill-manifest.json").read_bytes())
                    (target / "docs/skill-manifest.json").unlink()


if __name__ == "__main__":
    unittest.main()
