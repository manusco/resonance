import importlib.util
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("forge_catalog", ROOT / ".forge" / "forge.py")
forge = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = forge
spec.loader.exec_module(forge)


class CommandCatalogTests(unittest.TestCase):
    def test_registry_catalog_covers_each_command_once(self):
        commands, families, help_items = forge.validate_catalog(forge.load_command_registry())
        self.assertEqual(len(commands), sum(len(f["aliases"]) for f in families))
        self.assertTrue(help_items)

    def test_registry_rejects_unknown_skill_target(self):
        registry = copy.deepcopy(forge.load_command_registry())
        registry["commands"][0]["skill"] = "ops/not-real"
        with self.assertRaises(SystemExit):
            forge.validate_catalog(registry)

    def test_registry_rejects_entrypoint_conflict(self):
        registry = copy.deepcopy(forge.load_command_registry())
        command = next(item for item in registry["commands"] if item["alias"] == "goal")
        command["alias"] = "goal-conflict"
        registry["catalog"]["families"][0]["aliases"] = ["goal-conflict"]
        with self.assertRaises(SystemExit):
            forge.validate_catalog(registry)

    def test_manual_is_host_shim_metadata_not_routing_authority(self):
        registry = forge.load_command_registry()
        comment = registry["_comment"]
        self.assertIn("host shim", comment)
        self.assertIn("does not block natural-language routing", comment)

    def test_replace_preserves_every_byte_outside_markers(self):
        start = forge.section_marker("TEST", "START")
        end = forge.section_marker("TEST", "END")
        original = f"prefix\r\n{start}\r\nold\r\n{end}\r\nsuffix\r\n"
        updated = forge.replace_generated_section(original, "TEST", "new", Path("doc.md"))
        self.assertTrue(updated.startswith(f"prefix\r\n{start}"))
        self.assertTrue(updated.endswith(f"{end}\r\nsuffix\r\n"))
        self.assertIn("\nnew\n", updated)

    def test_replacement_does_not_normalize_surrounding_line_endings(self):
        start = forge.section_marker("TEST", "START")
        end = forge.section_marker("TEST", "END")
        prefix = b"prefix\r\n" + start.encode()
        suffix = end.encode() + b"\r\nsuffix\r\n"
        original = (prefix + b"\r\nold\r\n" + suffix).decode("utf-8")
        updated = forge.replace_generated_section(original, "TEST", "new", Path("doc.md"))
        encoded = updated.encode("utf-8")
        self.assertTrue(encoded.startswith(prefix))
        self.assertTrue(encoded.endswith(suffix))

    def test_missing_duplicate_and_reversed_markers_fail_closed(self):
        start = forge.section_marker("TEST", "START")
        end = forge.section_marker("TEST", "END")
        cases = ("plain", f"{start}\nbody", f"{start}\n{start}\n{end}", f"{end}\n{start}")
        for text in cases:
            with self.subTest(text=text), self.assertRaises(SystemExit):
                forge.replace_generated_section(text, "TEST", "new", Path("doc.md"))

    def test_command_docs_are_fresh_and_idempotent(self):
        self.assertEqual(forge.build_command_docs(True), 0)
        before = {name: (ROOT / name).read_bytes() for name in forge.DOC_SECTIONS}
        self.assertEqual(forge.build_command_docs(False), 0)
        after = {name: (ROOT / name).read_bytes() for name in forge.DOC_SECTIONS}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
