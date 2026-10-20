import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".forge"))
import fingerprint_scan


class FingerprintScanTests(unittest.TestCase):
    def test_github_docs_are_not_mistaken_for_repository_source_links(self):
        self.assertIsNone(fingerprint_scan.SOURCE_MARKERS.search(
            "See https://docs.git" + "hub.com/en/repositories/about"
        ))

    def test_github_repository_source_links_are_detected(self):
        for url in (
            "git" + "hub.com/private/repository",
            "https://git" + "hub.com/private/repository",
            "ssh://git" + "hub.com/private/repository",
        ):
            with self.subTest(url=url):
                self.assertIsNotNone(fingerprint_scan.SOURCE_MARKERS.search(url))

    def test_other_source_markers_still_match(self):
        for text in (
            "provenance" + ": source",
            "based on " + "https://example.com/project",
            "comm" + "it abcdef0123456789",
        ):
            with self.subTest(text=text):
                self.assertIsNotNone(fingerprint_scan.SOURCE_MARKERS.search(text))


if __name__ == "__main__":
    unittest.main()
