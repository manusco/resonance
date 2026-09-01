import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import resonance_update as update


class _Headers(dict):
    def get(self, key, default=None):
        return super().get(key, default)


class _Response(io.BytesIO):
    def __init__(self, payload):
        raw = json.dumps(payload).encode("utf-8")
        super().__init__(raw)
        self.headers = _Headers({"Content-Length": str(len(raw))})


class ReleaseUpdateTests(unittest.TestCase):
    def test_stable_version_rejects_prerelease_and_partial_versions(self):
        self.assertEqual((2, 5, 3), update.stable_version("v2.5.3"))
        self.assertEqual("2.5.32", update.FRAMEWORK_VERSION)
        self.assertIsNone(update.stable_version("2.5"))
        self.assertIsNone(update.stable_version("2.5.3-rc.1"))

    def test_disabled_notice_does_not_depend_on_host_package_json(self):
        with mock.patch.object(update, "notice_state", return_value={"schema": 1, "enabled": False}):
            self.assertEqual(0, update.main(["notice", "check", "--quiet"]))

    def test_notice_is_disabled_by_default_and_kept_outside_project(self):
        with tempfile.TemporaryDirectory() as td, mock.patch.dict(
            os.environ, {"XDG_CONFIG_HOME": td}, clear=False
        ):
            self.assertFalse(update.notice_state()["enabled"])
            path = update.set_notice(True)
            self.assertTrue(update.notice_state()["enabled"])
            self.assertEqual(Path(td) / "resonance" / "update-notice.json", path)

    def test_latest_release_rejects_draft_and_prerelease(self):
        for field in ("draft", "prerelease"):
            payload = {"tag_name": "v9.9.9", "draft": False, "prerelease": False}
            payload[field] = True
            opener = mock.Mock()
            opener.open.return_value = _Response(payload)
            with self.subTest(field=field), mock.patch("urllib.request.build_opener", return_value=opener):
                with self.assertRaisesRegex(ValueError, "not stable"):
                    update.latest_stable_release()

    def test_latest_release_caps_response_size(self):
        response = _Response({"tag_name": "v9.9.9", "draft": False, "prerelease": False})
        response.headers["Content-Length"] = str(update.MAX_NOTICE_BYTES + 1)
        opener = mock.Mock()
        opener.open.return_value = response
        with mock.patch("urllib.request.build_opener", return_value=opener):
            with self.assertRaisesRegex(ValueError, "size limit"):
                update.latest_stable_release()

    def test_notice_cache_is_global_minimal_and_expires(self):
        with tempfile.TemporaryDirectory() as td, mock.patch.dict(
            os.environ, {"XDG_CONFIG_HOME": td}, clear=False
        ):
            release = {"version": "2.5.3", "url": "https://github.com/manusco/resonance/releases/tag/v2.5.3"}
            path = update.save_notice_cache(release, now=100.0)
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual({"schema", "checked_at", "version", "url"}, set(payload))
            self.assertEqual(release, update.load_notice_cache(now=101.0))
            self.assertIsNone(update.load_notice_cache(now=100.0 + update.NOTICE_TTL_SECONDS + 1))

    def test_launcher_checks_are_quiet_nonblocking_and_never_apply(self):
        shell = (ROOT / "resonance.sh").read_text(encoding="utf-8")
        powershell = (ROOT / "resonance.ps1").read_text(encoding="utf-8")
        for launcher in (shell, powershell):
            self.assertIn("notice check --quiet", launcher)
            notice_line = next(line for line in launcher.splitlines() if "notice check --quiet" in line)
            self.assertNotIn("--apply", notice_line)


if __name__ == "__main__":
    unittest.main()
