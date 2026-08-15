"""Tests for deterministic release metadata and changelog extraction."""
import sys
import unittest
from pathlib import Path

FORGE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FORGE_DIR))
import release_notes  # noqa: E402


class ReleaseNotesTest(unittest.TestCase):
    def test_extracts_only_requested_release(self):
        changelog = (
            "# Changelog\n\n"
            "## v2.4.88\n\nNew release.\n\n### Added\n- One.\n\n"
            "## v2.4.87\n\nOld release.\n"
        )
        notes = release_notes.extract_notes(changelog, "2.4.88")
        self.assertIn("New release.", notes)
        self.assertNotIn("Old release.", notes)

    def test_missing_release_fails(self):
        with self.assertRaisesRegex(ValueError, "no exact"):
            release_notes.extract_notes("# Changelog\n", "2.4.88")

    def test_empty_release_fails(self):
        with self.assertRaisesRegex(ValueError, "no release notes"):
            release_notes.extract_notes("## v2.4.88\n\n## v2.4.87\nOld\n", "2.4.88")

    def test_semver_is_numeric(self):
        self.assertGreater(
            release_notes.parse_version("2.4.10"),
            release_notes.parse_version("2.4.9"),
        )

    def test_decimal_or_partial_version_fails(self):
        for value in ("2.4", "2.4.08", "v2.4.88"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                release_notes.parse_version(value)


if __name__ == "__main__":
    unittest.main()
