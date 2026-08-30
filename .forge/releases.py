#!/usr/bin/env python3
"""Discover official releases and preview/apply a pinned transactional upgrade."""
from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import time
import urllib.request

REPOSITORY = "https://github.com/manusco/resonance.git"
API = "https://api.github.com/repos/manusco/resonance/releases"
RELEASE_URL = "https://github.com/manusco/resonance/releases/tag/"
MANIFEST = ".resonance/framework-manifest.json"
CACHE_TTL = 86400  # One request per project per day, including failed requests.
HTTP_TIMEOUT = 3  # Best-effort discovery must not hold up ordinary work.
MAX_RESPONSE = 65536  # Release prose is not needed; cap untrusted response bytes.


def parse_version(value: str) -> tuple[int, int, int]:
    if not isinstance(value, str) or not re.fullmatch(
            r"v?(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", value):
        raise ValueError("expected a stable MAJOR.MINOR.PATCH version")
    return tuple(int(part) for part in value.lstrip("v").split("."))


def installed_version(target: Path) -> str | None:
    try:
        manifest = target / MANIFEST
        if manifest.exists():
            data = json.loads(manifest.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or data.get("schema") != 1:
                return None
        else:
            # Only this framework source checkout may use package.json. Never
            # mistake an application's package version for its installed framework.
            if target.resolve() != Path(__file__).resolve().parents[1] or not (target / ".git").exists():
                return None
            data = json.loads((target / "package.json").read_text(encoding="utf-8"))
            if (data.get("name") != "@manusco/resonance"
                    or data.get("repository", {}).get("url") != "git+" + REPOSITORY):
                return None
        value = data.get("version")
        parse_version(value)
        return value.lstrip("v")
    except (OSError, ValueError, TypeError, AttributeError):
        return None


def fetch_release(requested: str = "latest") -> dict:
    if requested == "latest":
        endpoint = API + "/latest"
    else:
        parse_version(requested)
        endpoint = API + "/tags/v" + requested.lstrip("v")
    request = urllib.request.Request(endpoint, headers={
        "Accept": "application/vnd.github+json", "User-Agent": "resonance-update-check",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as response:
        # Redirects must not substitute a different API or insecure transport.
        if response.geturl() != endpoint:
            raise ValueError("unexpected release API redirect")
        raw = response.read(MAX_RESPONSE + 1)
    if len(raw) > MAX_RESPONSE:
        raise ValueError("release response is too large")
    data = json.loads(raw)
    if (not isinstance(data, dict) or data.get("draft") is not False
            or data.get("prerelease") is not False):
        raise ValueError("expected a published stable release")
    tag = data.get("tag_name")
    parse_version(tag)
    if not tag.startswith("v"):
        raise ValueError("official release tags must start with v")
    value = tag[1:]
    if requested != "latest" and value != requested.lstrip("v"):
        raise ValueError("release version does not match requested version")
    # Ignore release prose, download URLs, and target_commitish. They are neither
    # instructions nor a trusted source location or immutable revision.
    return {"version": value, "tag": tag, "url": RELEASE_URL + tag}


def cache_file(target: Path) -> Path:
    if sys.platform == "win32":
        root = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData/Local")))
    elif sys.platform == "darwin":
        root = Path.home() / "Library/Caches"
    else:
        root = Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache")))
    key = hashlib.sha256(str(target.resolve()).encode()).hexdigest()
    for candidate in (root, Path.home() / ".cache"):
        path = candidate / "resonance" / (key + ".json")
        if candidate.is_absolute() and not path.resolve().is_relative_to(target.resolve()):
            return path
    raise ValueError("no user cache location outside the target project")


def read_cache(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("schema") != 1:
            return {}
        stamp = data.get("checked_at")
        if not isinstance(stamp, (int, float)) or isinstance(stamp, bool):
            return {}
        if data.get("latest") is not None:
            parse_version(data["latest"])
        return data
    except (OSError, ValueError, TypeError):
        return {}


def write_cache(path: Path, data: dict) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix="release-", delete=False) as stream:
            staged = Path(stream.name)
            json.dump(data, stream)
        try:
            os.replace(staged, path)
        finally:
            staged.unlink(missing_ok=True)
    except OSError:
        pass  # An unwritable cache must not prevent project work or explicit checks.


def check_update(target: Path, *, cache_path: Path | None = None,
                 now: float | None = None, force: bool = False) -> dict:
    installed = installed_version(target)
    result = {"status": "unknown", "installed": installed, "latest": None, "notify": False}
    if os.environ.get("RESONANCE_NO_UPDATE_CHECK") == "1":
        return {**result, "status": "disabled"}
    if installed is None:
        return result
    path = cache_path if cache_path is not None else cache_file(target)
    stamp = time.time() if now is None else now
    cached = read_cache(path)
    age = stamp - cached.get("checked_at", stamp - CACHE_TTL)
    if force or not cached or not 0 <= age < CACHE_TTL:
        try:
            latest = fetch_release()["version"]
            parse_version(latest)
        except (OSError, ValueError, TypeError, KeyError, http.client.HTTPException):
            latest = None
        cached = {"schema": 1, "checked_at": stamp, "latest": latest,
                  "notified": cached.get("notified")}
        write_cache(path, cached)
    latest = cached.get("latest")
    if latest is None:
        return {**result, "status": "unavailable"}
    available = parse_version(latest) > parse_version(installed)
    pair = installed + ":" + latest
    notify = available and (force or cached.get("notified") != pair)
    if notify:
        cached["notified"] = pair
        write_cache(path, cached)
    return {"status": "available" if available else "current", "installed": installed,
            "latest": latest, "notify": notify}


def format_command(args: list[str], *, windows: bool = False) -> str:
    if windows:
        return "& " + " ".join("'" + arg.replace("'", "''") + "'" for arg in args)
    return shlex.join(args)


def run_update(target: Path, requested: str = "latest", *, apply: bool = False,
               revision: str | None = None) -> int:
    target = target.resolve()
    if apply and (requested == "latest" or not revision):
        raise ValueError("apply requires the exact --version and --revision from a preview")
    if requested != "latest":
        parse_version(requested)
    if revision is not None and not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("revision must be the full Git commit from the preview")
    try:
        current = json.loads((target / MANIFEST).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError("no installed ownership manifest; use the documented adoption flow first. "
                         "Framework source checkouts must be updated with Git, not self-installed") from exc
    if (not isinstance(current, dict) or current.get("schema") != 1
            or not isinstance(current.get("files"), dict)):
        raise ValueError("invalid installed ownership manifest; review before updating")
    installed = installed_version(target)
    if installed is None and current.get("version") != "adopted":
        raise ValueError("unknown installed version; review the ownership manifest first")
    release = fetch_release(requested)
    if requested == "latest" and installed and parse_version(installed) >= parse_version(release["version"]):
        print(f"Resonance {installed} is current (latest stable: {release['version']}).")
        return 0
    with tempfile.TemporaryDirectory(prefix="resonance-release-") as temp:
        source = Path(temp) / "source"
        if source.resolve().is_relative_to(target):
            raise ValueError("temporary source must be outside the target; change TMPDIR/TEMP")
        subprocess.run(["git", "-c", "core.hooksPath=" + os.devnull,
                        "-c", "advice.detachedHead=false", "clone", "--quiet",
                        "--depth", "1", "--branch", release["tag"], "--", REPOSITORY, str(source)],
                       check=True, timeout=120)
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=source, capture_output=True,
                                text=True, check=True, timeout=10).stdout.strip()
        if not re.fullmatch(r"[0-9a-f]{40}", commit) or (revision and commit != revision):
            raise ValueError("release commit changed since preview; review a new preview before applying")
        required = (".forge/update.py", "AGENTS.md", "resonance.sh", "resonance.ps1", "package.json")
        if (any(not (source / name).is_file() or (source / name).is_symlink() for name in required)
                or not list((source / ".agents/skills").glob("**/SKILL.md"))):
            raise ValueError("incomplete release source: missing required framework files")
        package = json.loads((source / "package.json").read_text(encoding="utf-8"))
        if package.get("name") != "@manusco/resonance" or package.get("version") != release["version"]:
            raise ValueError("source package version does not match the requested release")
        print(f"Resonance {installed or 'adopted'} -> {release['version']} ({commit})", flush=True)
        command = [sys.executable, str(source / ".forge/update.py"), "--source", str(source),
                   "--target", str(target), "--version", release["version"]]
        if apply:
            command.append("--apply")
        result = subprocess.run(command, check=False)
        if result.returncode == 0 and not apply:
            args = [sys.executable, str(Path(__file__).resolve()), "update", "--target", str(target),
                    "--version", release["version"], "--revision", commit, "--apply"]
            print("After reviewing the plan, approve and run:")
            print(format_command(args, windows=os.name == "nt"))
        return result.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check", help="check for a newer stable GitHub release")
    check.add_argument("--target", type=Path, default=Path.cwd())
    check.add_argument("--quiet", action="store_true", help="only emit a new update notice")
    check.add_argument("--force", action="store_true", help="bypass the daily cache")
    update = commands.add_parser("update", help="preview the latest or a named stable release")
    update.add_argument("--target", type=Path, default=Path.cwd())
    update.add_argument("--version", default="latest")
    update.add_argument("--revision", help="exact commit printed by the approved preview")
    update.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "update":
            return run_update(args.target, args.version, apply=args.apply, revision=args.revision)
        result = check_update(args.target, force=args.force)
        if result["status"] == "available" and (not args.quiet or result["notify"]):
            print(f"Resonance {result['latest']} is available. You have {result['installed']}. "
                  "Run /update-resonance to preview the upgrade.")
            print(RELEASE_URL + "v" + result["latest"])
        elif not args.quiet:
            print(json.dumps(result, indent=2))
        return 0 if args.quiet or result["status"] in {"available", "current", "disabled"} else 1
    except (OSError, ValueError, http.client.HTTPException, subprocess.SubprocessError) as exc:
        if args.command == "check" and args.quiet:
            return 0
        print(f"Resonance update failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
