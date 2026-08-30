import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("resonance_releases", ROOT / ".forge" / "releases.py")
releases = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = releases
spec.loader.exec_module(releases)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.target = self.root / "project"
        self.target.mkdir()
        self.cache = self.root / "cache" / "releases.json"
        patch = mock.patch.dict(os.environ, {}, clear=True)
        patch.start()
        self.addCleanup(patch.stop)

    def manifest(self, version="2.5.2", schema=1):
        path = self.target / ".resonance" / "framework-manifest.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps({"schema": schema, "version": version, "files": {}}))

    def release(self, version="2.6.0"):
        return {"version": version, "tag": "v" + version,
                "url": "https://github.com/" + "test/releases/tag/v" + version}

    def check(self, now=100000, **kwargs):
        return releases.check_update(self.target, cache_path=self.cache, now=now, **kwargs)

    def test_stable_versions_use_numeric_order(self):
        self.assertEqual(releases.parse_version("v2.10.3"), (2, 10, 3))
        self.assertGreater(releases.parse_version("2.10.0"), releases.parse_version("2.9.9"))

    def test_rejects_nonstable_and_invalid_versions(self):
        for value in ("", "2.6", "2.6.0-rc.1", "2.6.0+build", "02.6.0", "2.06.0",
                      "2.6.00", " v2.6.0", "2.6.0\n", "latest", "../../2.6.0"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                releases.parse_version(value)

    def test_installed_version_uses_manifest_not_application(self):
        (self.target / "package.json").write_text('{"version":"99.0.0"}')
        self.assertIsNone(releases.installed_version(self.target))
        self.manifest()
        self.assertEqual(releases.installed_version(self.target), "2.5.2")

    def test_invalid_manifests_are_unknown(self):
        for version, schema in (("adopted", 1), ("2.5.2", 2), (None, 1), ("2.5.2-rc.1", 1)):
            with self.subTest(version=version, schema=schema):
                self.manifest(version, schema)
                self.assertIsNone(releases.installed_version(self.target))
        (self.target / ".resonance" / "framework-manifest.json").write_text("broken json")
        self.assertIsNone(releases.installed_version(self.target))

    def test_unknown_installation_does_not_query_github(self):
        with mock.patch.object(releases, "fetch_release") as fetch:
            result = self.check()
        fetch.assert_not_called()
        self.assertEqual(result["status"], "unknown")
        self.assertFalse(result["notify"])

    def test_optout_skips_network_and_cache(self):
        self.manifest()
        with mock.patch.dict(os.environ, {"RESONANCE_NO_UPDATE_CHECK": "1"}), \
                mock.patch.object(releases, "fetch_release") as fetch:
            result = self.check(force=True)
        fetch.assert_not_called()
        self.assertEqual(result["status"], "disabled")
        self.assertFalse(result["notify"])
        self.assertFalse(self.cache.exists())

    def test_new_version_notifies_once_and_cache_expires_daily(self):
        self.manifest()
        with mock.patch.object(releases, "fetch_release", return_value=self.release()) as fetch:
            first = self.check()
            repeat = self.check(now=100001)
            refreshed = self.check(now=186401)
        self.assertEqual(fetch.call_count, 2)
        self.assertEqual(first["status"], "available")
        self.assertEqual(first["installed"], "2.5.2")
        self.assertEqual(first["latest"], "2.6.0")
        self.assertTrue(first["notify"])
        self.assertFalse(repeat["notify"])
        self.assertFalse(refreshed["notify"])
        self.assertTrue(self.cache.exists())

    def test_each_new_version_can_notify(self):
        self.manifest()
        with mock.patch.object(releases, "fetch_release", side_effect=[self.release(), self.release("2.7.0")]):
            self.assertTrue(self.check()["notify"])
            self.assertTrue(self.check(now=186401)["notify"])

    def test_force_bypasses_fresh_cache(self):
        self.manifest()
        with mock.patch.object(releases, "fetch_release", return_value=self.release()) as fetch:
            self.check()
            self.check(now=100001, force=True)
        self.assertEqual(fetch.call_count, 2)

    def test_current_and_newer_installations_stay_quiet(self):
        for installed, latest in (("2.6.0", "2.6.0"), ("2.10.0", "2.9.0")):
            with self.subTest(installed=installed):
                self.manifest(installed)
                with mock.patch.object(releases, "fetch_release", return_value=self.release(latest)):
                    result = self.check(force=True)
                self.assertEqual(result["status"], "current")
                self.assertFalse(result["notify"])

    def test_network_failures_are_quiet_and_cached(self):
        self.manifest()
        with mock.patch.object(releases, "fetch_release", side_effect=OSError("offline")) as fetch:
            first = self.check()
            repeat = self.check(now=100001)
        fetch.assert_called_once()
        self.assertEqual(first["status"], "unavailable")
        self.assertEqual(repeat["status"], "unavailable")
        self.assertFalse(first["notify"])
        self.assertFalse(repeat["notify"])

    def test_corrupt_cache_is_a_miss(self):
        self.manifest()
        self.cache.parent.mkdir()
        for contents in ("not json", "[]", '{"schema":999}'):
            with self.subTest(contents=contents):
                self.cache.write_text(contents)
                with mock.patch.object(releases, "fetch_release", return_value=self.release()) as fetch:
                    result = self.check()
                fetch.assert_called_once()
                self.assertEqual(result["status"], "available")

    def test_unwritable_cache_does_not_block_check(self):
        self.manifest()
        self.cache.parent.write_text("parent is a file")
        with mock.patch.object(releases, "fetch_release", return_value=self.release()):
            result = self.check()
        self.assertEqual(result["status"], "available")

    def github_response(self, data, endpoint=None):
        response = io.BytesIO(data)
        response.geturl = lambda: endpoint or releases.API + "/latest"
        return response

    def github_payload(self, endpoint=None, **overrides):
        payload = {"tag_name": "v2.6.0", "draft": False, "prerelease": False}
        payload.update(overrides)
        return self.github_response(json.dumps(payload).encode(), endpoint)

    def test_fetch_requires_bounded_timeout_and_normalizes_version(self):
        with mock.patch("urllib.request.urlopen", return_value=self.github_payload()) as fetch:
            result = releases.fetch_release()
        self.assertEqual(fetch.call_args.kwargs["timeout"], 3)
        self.assertEqual(result["version"], "2.6.0")
        self.assertEqual(result["tag"], "v2.6.0")
        self.assertTrue(result["url"].startswith("https://github.com/"))

    def test_fetch_rejects_draft_prerelease_and_malformed_metadata(self):
        for overrides in ({"draft": True}, {"prerelease": True}, {"draft": "false"},
                          {"draft": None}, {"tag_name": "v2.6.0-rc.1"}, {"tag_name": "v02.6.0"}):
            with self.subTest(overrides=overrides), \
                    mock.patch("urllib.request.urlopen", return_value=self.github_payload(**overrides)), \
                    self.assertRaises(ValueError):
                releases.fetch_release()

    def test_fetch_rejects_wrong_exact_version(self):
        response = self.github_payload(endpoint=releases.API + "/tags/v2.5.2")
        with mock.patch("urllib.request.urlopen", return_value=response), \
                self.assertRaises(ValueError):
            releases.fetch_release("2.5.2")

    def test_fetch_rejects_oversized_response(self):
        with mock.patch("urllib.request.urlopen", return_value=self.github_response(b" " * 65537)), \
                self.assertRaises(ValueError):
            releases.fetch_release()

    def test_fetch_rejects_redirect(self):
        response = self.github_payload(endpoint="https://attacker.example/releases/latest")
        with mock.patch("urllib.request.urlopen", return_value=response), self.assertRaisesRegex(ValueError, "redirect"):
            releases.fetch_release()

    def test_fetch_rejects_nonobject_json(self):
        for raw in (b"null", b"[]", b"false"):
            with self.subTest(raw=raw), \
                    mock.patch("urllib.request.urlopen", return_value=self.github_response(raw)), \
                    self.assertRaises(ValueError):
                releases.fetch_release()

    def test_quiet_cli_offline_is_silent_and_successful(self):
        self.manifest()
        with mock.patch.object(releases, "cache_file", return_value=self.cache), \
                mock.patch.object(releases, "fetch_release", side_effect=OSError("offline")), \
                mock.patch("sys.stdout", new_callable=io.StringIO) as out, \
                mock.patch("sys.stderr", new_callable=io.StringIO) as err:
            result = releases.main(["check", "--target", str(self.target), "--quiet"])
        self.assertEqual(result, 0)
        self.assertEqual(out.getvalue(), "")
        self.assertEqual(err.getvalue(), "")

    def test_explicit_force_reports_network_failure(self):
        self.manifest()
        with mock.patch.object(releases, "cache_file", return_value=self.cache), \
                mock.patch.object(releases, "fetch_release", side_effect=OSError("offline")) as fetch, \
                mock.patch("sys.stdout", new_callable=io.StringIO) as out:
            result = releases.main(["check", "--target", str(self.target), "--force"])
        fetch.assert_called_once()
        self.assertEqual(result, 1)
        self.assertEqual(json.loads(out.getvalue())["status"], "unavailable")

    def test_cache_location_uses_platform_directory_and_project_key(self):
        home = self.root / "home"
        cases = (("darwin", {}, home / "Library/Caches"),
                 ("linux", {"XDG_CACHE_HOME": str(self.root / "xdg")}, self.root / "xdg"),
                 ("win32", {"LOCALAPPDATA": str(self.root / "local")}, self.root / "local"))
        for platform, environment, expected in cases:
            with self.subTest(platform=platform), mock.patch.object(releases.sys, "platform", platform), \
                    mock.patch.dict(os.environ, environment, clear=True), \
                    mock.patch.object(Path, "home", return_value=home):
                location = releases.cache_file(self.target)
                other = releases.cache_file(self.root / "other-project")
            self.assertTrue(location.is_relative_to(expected))
            self.assertFalse(location.is_relative_to(self.target))
            self.assertNotEqual(location, other)

    def test_cache_rejects_relative_and_project_local_environment_paths(self):
        for cache_root in ("relative-cache", str(self.target / "cache")):
            with self.subTest(cache_root=cache_root), mock.patch.object(releases.sys, "platform", "linux"), \
                    mock.patch.dict(os.environ, {"XDG_CACHE_HOME": cache_root}):
                location = releases.cache_file(self.target)
            self.assertTrue(location.is_absolute())
            self.assertFalse(location.is_relative_to(self.target))


if __name__ == "__main__":
    unittest.main()
