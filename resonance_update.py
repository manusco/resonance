#!/usr/bin/env python3
"""Transactional Resonance installer and updater."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import uuid
import urllib.error
import urllib.request
from pathlib import Path

MANIFEST = ".resonance/framework-manifest.json"
PRESERVE_IF_UNOWNED = ("AGENTS.md", "CLAUDE.md", ".cursor/rules/resonance.mdc")
MANAGED_ROOTS = (".agents", ".forge", ".claude/skills", ".cursor/skills",
                 ".cursor/rules/resonance.mdc", ".opencode/commands", "AGENTS.md",
                 "CLAUDE.md", "resonance.ps1", "resonance.sh", "resonance_update.py")
PROFILE_ROOTS = {
    # A source checkout owns the compiler, documentation, and host bridges.
    "source": MANAGED_ROOTS,
    # A compiled consumer owns only generated skills and host adapters. The
    # validator is run from the pinned source checkout, never from the target.
    "compiled": (".agents/skills", ".claude/skills", ".cursor/skills",
                  ".cursor/rules/resonance.mdc", ".opencode/commands",
                  "resonance.ps1", "resonance.sh", "resonance_update.py"),
}
LEGACY_ROOTS = (".codex/prompts", ".opencode/command")
RELEASE_API = "https://api.github.com/repos/manusco/resonance/releases/latest"
NOTICE_SCHEMA = 1
MAX_NOTICE_BYTES = 64 * 1024
NOTICE_TTL_SECONDS = 24 * 60 * 60
FRAMEWORK_VERSION = "2.5.43"


class SourceDirtyError(ValueError):
    """Raised when the source checkout has real Git status entries."""

    def __init__(self, paths: list[str], warnings: str = ""):
        self.paths = paths
        self.warnings = warnings
        message = "source checkout must be clean; use a pinned tag or commit with no local changes"
        if paths:
            message += ": " + ", ".join(paths[:10])
            if len(paths) > 10:
                message += f", ... ({len(paths)} total)"
        if warnings:
            message += f" (git warnings: {warnings.strip()})"
        super().__init__(message)


class UpdateRollbackError(RuntimeError):
    """Raised when an update fails and its automatic rollback also fails."""

    def __init__(self, apply_error: BaseException, rollback_error: BaseException, backup: Path):
        self.apply_error = apply_error
        self.rollback_error = rollback_error
        self.backup = backup
        super().__init__(
            f"update failed ({apply_error}); rollback also failed ({rollback_error}); "
            f"recovery journal: {backup / 'journal.json'}"
        )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(root: Path, path: Path) -> Path:
    root = root.resolve()
    resolved = path.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes target: {path}") from exc
    lexical = Path(os.path.abspath(path))
    try:
        relative = lexical.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes target: {path}") from exc
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError(f"managed path traverses a symlink: {path}")
    return lexical


def verify_write_access(target: Path, paths: list[str]) -> None:
    """Probe create and delete access in each existing destination directory."""
    checked: set[Path] = set()
    for relative in paths:
        destination = inside(target, target / relative)
        parent = destination if destination.is_dir() else destination.parent
        while not parent.exists() and parent != target:
            parent = parent.parent
        parent = inside(target, parent)
        if parent in checked:
            continue
        checked.add(parent)
        try:
            with tempfile.NamedTemporaryFile(prefix=".resonance-write-probe-", dir=parent, delete=True):
                pass
        except OSError as exc:
            raise PermissionError(
                f"managed path is not writable before update: {parent}; "
                "rerun with filesystem permission that also covers rollback"
            ) from exc


def source_files(source: Path, include_legacy: bool = False,
                 profile: str = "source") -> dict[str, Path]:
    if profile not in PROFILE_ROOTS:
        raise ValueError(f"unknown installation profile: {profile}")
    source = source.resolve()
    clean = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=source,
        capture_output=True,
        text=False,
    )
    stderr = clean.stderr.decode("utf-8", errors="replace") if clean.stderr else ""
    if clean.returncode != 0:
        raise ValueError(
            "source must be a Git checkout with readable status; "
            "install from a pinned tag or commit"
            + (f" (git stderr: {stderr.strip()})" if stderr.strip() else "")
        )
    dirty = [
        entry.decode("utf-8", errors="replace")
        for entry in clean.stdout.split(b"\0")
        if entry
    ]
    if dirty:
        raise SourceDirtyError(dirty, stderr)
    result = subprocess.run(["git", "ls-files", "-z"], cwd=source, capture_output=True)
    if result.returncode != 0:
        raise ValueError("source must be a Git checkout; install from a pinned tag or commit")
    tracked = [p.decode("utf-8", "strict") for p in result.stdout.split(b"\0") if p]
    files = {}
    for rel in tracked:
        roots = PROFILE_ROOTS[profile] + (LEGACY_ROOTS if include_legacy else ())
        if any(rel == root or rel.startswith(root.rstrip("/") + "/") for root in roots):
            path = source / rel
            if path.is_file():
                files[Path(rel).as_posix()] = path
    return files


def load_manifest(target: Path) -> dict:
    p = target / MANIFEST
    if not p.is_file():
        return {"schema": 1, "files": {}}
    data = json.loads(p.read_text(encoding="utf-8"))
    if data.get("schema") != 1 or not isinstance(data.get("files"), dict):
        raise ValueError(f"invalid ownership manifest: {p}")
    profile = data.get("profile")
    if profile is not None and profile not in PROFILE_ROOTS:
        raise ValueError(f"invalid installation profile in ownership manifest: {p}")
    return data


def resolve_profile(target: Path, requested: str | None, manifest: dict) -> str:
    recorded = manifest.get("profile")
    if requested and requested not in PROFILE_ROOTS:
        raise ValueError(f"unknown installation profile: {requested}")
    if recorded and requested and recorded != requested:
        raise ValueError(f"target is recorded as {recorded}; profile migration is unsupported")
    if recorded:
        return recorded
    if requested:
        return requested
    # Existing source consumers are backwards compatible. A target that has
    # generated skills but no compiler is ambiguous, so require an explicit
    # profile instead of silently claiming the consumer as source mode.
    if (target / ".agents" / "skills").exists() and not (target / ".forge").exists():
        raise ValueError("profile is required for a legacy compiled-looking target; choose source or compiled")
    return "source"


def version(source: Path) -> str:
    return str(json.loads((source / "package.json").read_text(encoding="utf-8"))["version"])


def source_revision(source: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=source, capture_output=True, text=True, check=True
    )
    revision = result.stdout.strip().lower()
    if len(revision) != 40 or any(ch not in "0123456789abcdef" for ch in revision):
        raise ValueError("source checkout does not resolve to a full commit")
    return revision


def plan_digest(work: dict) -> str:
    stable = {key: work[key] for key in (
        "version", "revision", "profile", "writes", "removes", "conflicts", "preserved",
        "files", "observed", "reasons", "manifest_write", "baseline_revision",
    )}
    return hashlib.sha256(json.dumps(stable, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def git_output(root: Path, *args: str) -> bytes:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.decode("utf-8", errors="replace").strip() or "Git command failed")
    return result.stdout


def git_commit(root: Path, revision: str) -> str:
    resolved = git_output(root, "rev-parse", "--verify", f"{revision}^{{commit}}").decode().strip().lower()
    if len(resolved) != 40 or any(ch not in "0123456789abcdef" for ch in resolved):
        raise ValueError("source revision is not a full Git commit")
    return resolved


def release_baseline(source: Path, manifest: dict, profile: str, paths: set[str]) -> tuple[str | None, dict[str, tuple[str, bytes]], str | None]:
    """Resolve only an installed revision proven to belong to the selected source history."""
    installed_version = str(manifest.get("version", ""))
    if installed_version == "adopted" and not manifest.get("source_revision"):
        return None, {}, "adopted installation has no verified historical release"
    recorded_profile = manifest.get("profile")
    if recorded_profile != profile:
        return None, {}, "installed profile does not match the selected profile"
    try:
        current_revision = git_commit(source, "HEAD")
        recorded_revision = manifest.get("source_revision")
        if recorded_revision:
            if (not isinstance(recorded_revision, str) or len(recorded_revision) != 40
                    or any(ch not in "0123456789abcdefABCDEF" for ch in recorded_revision)):
                raise ValueError("installed source revision is invalid")
            baseline_revision = git_commit(source, recorded_revision)
        elif installed_version == "adopted":
            raise ValueError("adopted installation has no verified historical release")
        else:
            if stable_version(installed_version) is None:
                raise ValueError("installed version has no exact local release tag")
            tag = f"v{installed_version}"
            baseline_revision = git_commit(source, tag)
            package = json.loads(git_output(source, "show", f"{baseline_revision}:package.json").decode("utf-8"))
            if str(package.get("version", "")) != installed_version:
                raise ValueError("local release tag version does not match the installed manifest")
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", baseline_revision, current_revision], cwd=source,
            capture_output=True,
        )
        if ancestor.returncode:
            raise ValueError("installed release is outside the selected source history")
        package = json.loads(git_output(source, "show", f"{baseline_revision}:package.json").decode("utf-8"))
        if stable_version(installed_version) and str(package.get("version", "")) != installed_version:
            raise ValueError("installed source revision version does not match the manifest")
        allowed = PROFILE_ROOTS[profile]
        tree = git_output(source, "ls-tree", "-r", "-z", "--full-tree", baseline_revision)
        blob_refs = {}
        for record in tree.split(b"\0"):
            if not record:
                continue
            metadata, raw_path = record.split(b"\t", 1)
            mode, kind, oid = metadata.decode("ascii").split()
            relative = raw_path.decode("utf-8", errors="strict")
            if relative in paths and kind == "blob" and mode in ("100644", "100755") and any(
                relative == root or relative.startswith(root.rstrip("/") + "/") for root in allowed
            ):
                blob_refs[relative] = oid
        resolved_blobs = git_blob_batch(source, list(dict.fromkeys(blob_refs.values())))
        blobs = {path: (oid, resolved_blobs[oid]) for path, oid in blob_refs.items()}
        return baseline_revision, blobs, None
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return None, {}, str(exc)


def project_locked_paths(target: Path) -> set[str]:
    path = target / ".resonance" / "project-skills.lock.json"
    inside(target, path)
    if not path.is_file():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema_version") != 1 or not isinstance(data.get("skills"), list):
            raise ValueError("invalid project skill lock schema")
        locked = set()
        for skill in data["skills"]:
            files = skill.get("files") if isinstance(skill, dict) else None
            if not isinstance(files, dict):
                raise ValueError("invalid project skill lock entry")
            for relative in files:
                if (not isinstance(relative, str) or not relative.startswith(".agents/skills/")
                        or safe_relative(relative) != relative):
                    raise ValueError("invalid path in project skill lock")
                locked.add(relative)
        return locked
    except (OSError, json.JSONDecodeError, TypeError, AttributeError, ValueError) as exc:
        raise ValueError(f"cannot safely read project skill lock {path}: {exc}") from exc


def git_blob_batch(root: Path, oids: list[str]) -> dict[str, bytes]:
    if not oids:
        return {}
    result = subprocess.run(["git", "cat-file", "--batch"], cwd=root,
                            input="".join(f"{oid}\n" for oid in oids).encode("ascii"),
                            capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.decode("utf-8", errors="replace").strip() or "cannot read Git blobs")
    raw, blobs = result.stdout, {}
    for _ in oids:
        header, separator, raw = raw.partition(b"\n")
        if not separator:
            raise ValueError("Git blob response is truncated")
        oid, kind, size = header.decode("ascii").split()
        length = int(size)
        content = raw[:length]
        raw = raw[length:]
        if len(content) != length or not raw.startswith(b"\n") or kind != "blob":
            raise ValueError("Git blob response is invalid")
        blobs[oid] = content
        raw = raw[1:]
    if raw:
        raise ValueError("Git blob response contains trailing data")
    return blobs


def target_git_snapshot(target: Path, paths: list[str]) -> tuple[Path | None, str, str | None, dict[str, tuple[str, str, bytes]]]:
    """Return the target's HEAD and ordinary blobs for requested paths, including a repo prefix."""
    try:
        top = Path(git_output(target, "rev-parse", "--show-toplevel").decode().strip()).resolve()
        prefix = git_output(target, "rev-parse", "--show-prefix").decode().strip().strip("/")
        commit = git_commit(target, "HEAD")
        tree = git_output(target, "ls-tree", "-r", "-z", "--full-tree", commit)
        wanted, refs = set(paths), {}
        for record in tree.split(b"\0"):
            if not record:
                continue
            metadata, raw_path = record.split(b"\t", 1)
            mode, kind, oid = metadata.decode("ascii").split()
            relative = raw_path.decode("utf-8", errors="strict")
            if prefix:
                if not relative.startswith(prefix + "/"):
                    continue
                key = relative[len(prefix) + 1:]
            else:
                key = relative
            if key in wanted and kind == "blob" and mode in ("100644", "100755"):
                refs[key] = (mode, oid)
        contents = git_blob_batch(top, list(dict.fromkeys(oid for _, oid in refs.values())))
        return top, prefix, commit, {path: (mode, oid, contents[oid]) for path, (mode, oid) in refs.items()}
    except (OSError, UnicodeError, ValueError):
        return None, "", None, {}


def safe_relative(relative: str) -> str:
    path = Path(relative)
    if path.is_absolute() or not relative or any(part in ("", ".", "..") for part in relative.split("/")):
        raise ValueError(f"unsafe journal path: {relative}")
    if path.as_posix() != relative:
        raise ValueError(f"unsafe journal path: {relative}")
    return relative


def managed_path(relative: str, profile: str) -> bool:
    return any(relative == root or relative.startswith(root.rstrip("/") + "/")
               for root in PROFILE_ROOTS[profile])


def notice_root() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "resonance"


def notice_state() -> dict:
    path = notice_root() / "update-notice.json"
    if not path.is_file():
        return {"schema": NOTICE_SCHEMA, "enabled": False}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"schema": NOTICE_SCHEMA, "enabled": False}
    return {"schema": NOTICE_SCHEMA, "enabled": data.get("enabled") is True}


def set_notice(enabled: bool) -> Path:
    root = notice_root()
    root.mkdir(parents=True, exist_ok=True)
    destination = root / "update-notice.json"
    temporary = destination.with_suffix(".tmp")
    temporary.write_text(json.dumps({"schema": NOTICE_SCHEMA, "enabled": enabled}) + "\n", encoding="utf-8")
    os.replace(temporary, destination)
    return destination


def load_notice_cache(now: float | None = None) -> dict | None:
    path = notice_root() / "update-cache.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        checked_at = float(data["checked_at"])
        release = {"version": str(data["version"]), "url": str(data["url"])}
        if stable_version(release["version"]) is None:
            return None
        if (now if now is not None else time.time()) - checked_at > NOTICE_TTL_SECONDS:
            return None
        return release
    except (KeyError, OSError, TypeError, ValueError):
        return None


def save_notice_cache(release: dict, now: float | None = None) -> Path:
    root = notice_root()
    root.mkdir(parents=True, exist_ok=True)
    destination = root / "update-cache.json"
    temporary = destination.with_suffix(".tmp")
    payload = {
        "schema": NOTICE_SCHEMA,
        "checked_at": now if now is not None else time.time(),
        "version": release["version"],
        "url": release["url"],
    }
    temporary.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")
    os.replace(temporary, destination)
    return destination


class _RejectRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        raise urllib.error.HTTPError(req.full_url, code, "redirect rejected", headers, fp)


def latest_stable_release(timeout: float = 3.0) -> dict:
    request = urllib.request.Request(
        RELEASE_API,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "resonance-update-notice"},
    )
    response = urllib.request.build_opener(_RejectRedirects()).open(request, timeout=timeout)
    length = response.headers.get("Content-Length")
    if length and int(length) > MAX_NOTICE_BYTES:
        raise ValueError("release response exceeds size limit")
    raw = response.read(MAX_NOTICE_BYTES + 1)
    if len(raw) > MAX_NOTICE_BYTES:
        raise ValueError("release response exceeds size limit")
    data = json.loads(raw.decode("utf-8"))
    tag = data.get("tag_name", "")
    if data.get("draft") or data.get("prerelease") or not stable_version(tag):
        raise ValueError("latest release is not stable")
    return {"version": tag.lstrip("v"), "url": data.get("html_url", "")}


def stable_version(value: str) -> tuple[int, int, int] | None:
    value = value.lstrip("v")
    parts = value.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        return None
    return tuple(int(part) for part in parts)


def check_notice(installed: str, quiet: bool = False) -> int:
    if not notice_state()["enabled"]:
        if not quiet:
            print("update notices are disabled")
        return 0
    try:
        latest = load_notice_cache()
        if latest is None:
            latest = latest_stable_release()
            save_notice_cache(latest)
        installed_version = stable_version(installed)
        if installed_version is None:
            raise ValueError("installed version is invalid")
        if stable_version(latest["version"]) > installed_version:
            print(f"Resonance {latest['version']} is available: {latest['url']}")
    except Exception as exc:
        if not quiet:
            print(f"update notice unavailable: {exc}", file=sys.stderr)
            return 1
    return 0


def adopt(source: Path, target: Path, profile: str | None = None) -> Path:
    """Record the exact bytes of a pre-manifest installation without changing them."""
    target = target.resolve()
    if (target / MANIFEST).exists():
        raise ValueError("ownership manifest already exists")
    if profile is None and not (target / ".forge").exists():
        raise ValueError("profile is required when adopting a target without .forge; choose source or compiled")
    profile = profile or "source"
    incoming = source_files(source, include_legacy=True, profile=profile)
    for rel in PRESERVE_IF_UNOWNED:
        incoming.pop(rel, None)
    files = {rel: target / rel for rel, src in incoming.items()
             if (target / rel).is_file() and digest(target / rel) == digest(src)}
    if not files:
        raise ValueError("no recognizable Resonance files found to adopt")
    manifest = {"schema": 1, "version": version(source), "profile": profile,
                "source_revision": source_revision(source),
                "files": {r: digest(p) for r, p in files.items()}}
    path = target / MANIFEST
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return path


def plan(source: Path, target: Path, profile: str | None = None) -> dict:
    source, target = source.resolve(), target.resolve()
    if source == target:
        raise ValueError("source and target must differ")
    inside(target, target / MANIFEST)
    current = load_manifest(target)
    profile = resolve_profile(target, profile, current)
    incoming = source_files(source, profile=profile)
    preserved = []
    for rel in PRESERVE_IF_UNOWNED:
        destination = inside(target, target / rel)
        if rel in incoming and destination.is_file() and rel not in current["files"]:
            incoming.pop(rel)
            preserved.append(rel)
    baseline_revision, baseline, baseline_error = release_baseline(
        source, current, profile, set(current["files"])
    )
    locked = project_locked_paths(target)
    conflicts, writes, removes, reasons = [], [], [], {}
    observed = {}
    def inspect(rel: str, dst: Path) -> tuple[bool, str | None]:
        exists = dst.exists() or dst.is_symlink()
        if not exists:
            observed[rel] = {"exists": False}
            return False, None
        if dst.is_symlink() or not dst.is_file():
            observed[rel] = {"exists": True, "unsafe": True}
            return True, None
        data = dst.read_bytes()
        mode = stat.S_IMODE(os.stat(dst, follow_symlinks=False).st_mode)
        observed[rel] = {"exists": True, "sha256": hashlib.sha256(data).hexdigest(),
                         "mode": mode}
        return True, observed[rel]["sha256"]

    for rel, src in incoming.items():
        inside(target, target / rel)
        dst = target / rel
        prior = current["files"].get(rel)
        exists, live_hash = inspect(rel, dst)
        incoming_hash = digest(src)
        if rel in locked:
            conflicts.append(rel)
            reasons[rel] = {"code": "project_skill_locked", "message": "path is listed in the project skill lock"}
        elif exists and live_hash == incoming_hash:
            reasons[rel] = {"code": "matches_incoming", "message": "live bytes match the selected source"}
        elif exists and live_hash is not None and prior and live_hash == prior:
            writes.append(rel)
            reasons[rel] = {"code": "matches_manifest", "message": "live bytes match the recorded ownership hash"}
        elif exists and live_hash is not None and prior and rel in baseline and baseline[rel][1] == dst.read_bytes():
            writes.append(rel)
            reasons[rel] = {"code": "matches_installed_release", "message": "live bytes match the verified installed release"}
        elif not exists and prior:
            conflicts.append(rel)
            reasons[rel] = {"code": "missing_managed_path", "message": "recorded managed path is missing locally"}
        elif not exists:
            writes.append(rel)
            reasons[rel] = {"code": "new_path", "message": "path is new in the selected source"}
        else:
            conflicts.append(rel)
            reasons[rel] = {"code": "unverified_local_bytes", "message": (
                baseline_error or "live bytes match neither the selected source nor verified installed release"
            )}
    for rel, prior in current["files"].items():
        if not isinstance(rel, str) or not managed_path(rel, profile):
            conflicts.append(str(rel))
            reasons[str(rel)] = {"code": "invalid_ownership_path",
                                 "message": "ownership manifest claims a path outside the selected framework profile"}
            continue
        inside(target, target / rel)
        dst = target / rel
        if rel not in incoming:
            exists, live_hash = inspect(rel, dst)
            if rel in locked:
                conflicts.append(rel)
                reasons[rel] = {"code": "project_skill_locked", "message": "path is listed in the project skill lock"}
            elif not exists:
                continue
            elif live_hash is not None and (live_hash == prior or (
                rel in baseline and baseline[rel][1] == dst.read_bytes()
            )):
                removes.append(rel)
            else:
                conflicts.append(rel)
                reasons[rel] = {"code": "unverified_local_bytes", "message": (
                    baseline_error or "live bytes match neither the manifest nor verified installed release"
                )}
    # The ownership file is part of the reviewed plan even though it is not a framework source file.
    manifest_path = target / MANIFEST
    observed[MANIFEST] = {"exists": manifest_path.is_file(),
                          "sha256": digest(manifest_path) if manifest_path.is_file() else None}
    next_files = {rel: digest(src) for rel, src in incoming.items()}
    next_manifest = {"schema": 1, "version": version(source), "profile": profile,
                     "source_revision": source_revision(source), "files": next_files}
    try:
        old_manifest = load_manifest(target) if manifest_path.is_file() else None
    except (OSError, ValueError, json.JSONDecodeError):
        old_manifest = None
    manifest_write = old_manifest != next_manifest
    result = {"version": version(source), "revision": source_revision(source),
            "profile": profile, "writes": sorted(writes),
            "removes": sorted(removes), "conflicts": sorted(set(conflicts)),
            "preserved": sorted(preserved),
            "files": next_files, "reasons": reasons, "observed": observed,
            "manifest_write": manifest_write, "baseline_revision": baseline_revision,
            "baseline_error": baseline_error}
    result["plan_digest"] = plan_digest(result)
    return result


def apply(source: Path, target: Path, expected_version: str | None = None,
          profile: str | None = None, expected_revision: str | None = None,
          expected_plan_digest: str | None = None) -> Path | None:
    source, target = source.resolve(), target.resolve()
    work = plan(source, target, profile)
    if expected_version and work["version"] != expected_version.lstrip("v"):
        raise ValueError(f"source version {work['version']} does not match requested {expected_version}")
    if expected_revision and work["revision"] != expected_revision.lower():
        raise ValueError("source commit does not match the reviewed revision")
    if expected_plan_digest and work["plan_digest"] != expected_plan_digest.lower():
        raise ValueError("update plan changed after review")
    if work["conflicts"]:
        details = "; ".join(
            f"{path}: {work['reasons'].get(path, {}).get('message', 'unverified local bytes')}"
            for path in work["conflicts"][:10]
        )
        if len(work["conflicts"]) > 10:
            details += f"; {len(work['conflicts']) - 10} more paths, use --json for the complete list"
        raise ValueError("user-owned or modified managed files block update: " + details)
    required = (".forge/forge.py", ".forge/validate_skill.py", ".forge/eval_integrity.py")
    if work["profile"] == "source":
        missing = [rel for rel in required if rel not in work["files"]]
        if missing:
            raise ValueError("source is incomplete; missing required validators: " + ", ".join(missing))
    if not work["writes"] and not work["removes"] and not work["manifest_write"]:
        return None
    touched = list(dict.fromkeys(work["writes"] + work["removes"] + ([MANIFEST] if work["manifest_write"] else [])))
    verify_write_access(target, touched)
    stamp = uuid.uuid4().hex
    backup = target / ".resonance" / "updates" / stamp
    journal_path = backup / "journal.json"
    next_manifest = {"schema": 1, "version": work["version"], "profile": work["profile"],
                     "source_revision": work["revision"], "files": work["files"]}
    stage_root = inside(target, target / ".resonance" / "tmp")
    inside(target, backup)
    inside(target, journal_path)
    stage_root.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="resonance-stage-", dir=stage_root))
    try:
        for rel in work["writes"]:
            if digest(source / rel) != work["files"][rel]:
                raise ValueError(f"source changed after preview: {rel}")
            staged = stage / rel
            staged.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / rel, staged)
            if digest(staged) != work["files"][rel]:
                raise ValueError(f"staged source failed hash verification: {rel}")

        # Recheck every observed live preimage immediately before building the recovery receipt.
        for rel, observed in work["observed"].items():
            if rel not in touched:
                continue
            dst = inside(target, target / rel)
            exists = dst.exists()
            if exists != observed["exists"]:
                raise ValueError(f"target changed after preview: {rel}")
            if exists and (not dst.is_file() or digest(dst) != observed.get("sha256")):
                raise ValueError(f"target changed after preview: {rel}")

        git_root, git_prefix, git_commit_hash, git_blobs = target_git_snapshot(target, touched)
        entries = []
        for rel in touched:
            dst = inside(target, target / rel)
            existed = dst.is_file()
            entry = {"path": rel, "existed": existed}
            if existed:
                data = dst.read_bytes()
                mode = stat.S_IMODE(os.stat(dst, follow_symlinks=False).st_mode)
                entry.update({"sha256": hashlib.sha256(data).hexdigest(), "mode": mode})
                blob = git_blobs.get(rel)
                expected_exec = bool(blob and blob[0] == "100755")
                if blob and blob[2] == data and bool(mode & 0o111) == expected_exec:
                    entry.update({"source": "git", "blob_oid": blob[1]})
                else:
                    entry["source"] = "file"
            else:
                entry["source"] = "missing"
            entries.append(entry)

        git_ref = None
        if git_commit_hash and any(entry.get("source") == "git" for entry in entries):
            git_ref = f"refs/resonance/updates/{stamp}"
            repository = git_root
            result = subprocess.run(["git", "update-ref", git_ref, git_commit_hash], cwd=repository,
                                    capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(f"cannot pin recovery commit before update: {result.stderr.strip()}")

        backup.mkdir(parents=True, exist_ok=False)
        journal = {"schema": 2, "status": "backing-up", "transaction_id": stamp,
                   "version": work["version"], "profile": work["profile"], "target": str(target),
                   "git_root": str(git_root) if git_ref else None, "git_prefix": git_prefix,
                   "git_commit": git_commit_hash if git_ref else None, "git_ref": git_ref,
                   "entries": entries}
        journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")
        for entry in entries:
            if entry.get("source") == "file":
                rel = entry["path"]
                saved = backup / "files" / rel
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target / rel, saved)
                if digest(saved) != entry["sha256"]:
                    raise RuntimeError(f"recovery preimage failed hash verification: {rel}")
        journal["status"] = "applying"
        journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")
    except BaseException:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    try:
        for rel in work["writes"]:
            dst = inside(target, target / rel)
            dst.parent.mkdir(parents=True, exist_ok=True)
            os.replace(stage / rel, dst)
        for rel in work["removes"]:
            inside(target, target / rel).unlink(missing_ok=True)
        if work["profile"] == "source":
            checks = [target / ".forge" / "forge.py", target / ".forge" / "validate_skill.py",
                      target / ".forge" / "eval_integrity.py"]
            commands = [
                [sys.executable, str(checks[0]), "build", "--all", "--host", "all", "--dry-run", "--consumer"],
                [sys.executable, str(checks[1]), "--all", "--strict", str(target / ".agents" / "skills")],
                [sys.executable, str(checks[2])],
            ]
        else:
            # Compiled targets do not contain .forge. Validate their generated
            # files with the pinned source checkout instead.
            checks = [source / ".forge" / "forge.py", source / ".forge" / "validate_skill.py",
                      source / ".forge" / "eval_integrity.py"]
            commands = [
                [sys.executable, str(checks[0]), "build", "--all", "--host", "all", "--dry-run"],
                [sys.executable, str(checks[1]), "--all", "--strict", str(target / ".agents" / "skills")],
                [sys.executable, str(checks[2])],
            ]
        for tool, command in zip(checks, commands):
            if not tool.is_file():
                raise RuntimeError(f"post-update validator missing: {tool}")
            result = subprocess.run(command, cwd=target, capture_output=True, text=True,
                                    encoding="utf-8", errors="replace", timeout=180)
            if result.returncode != 0:
                raise RuntimeError(f"post-update validation failed: {' '.join(command)}\n"
                                   f"{result.stdout}\n{result.stderr}")
        if work["manifest_write"]:
            mp = target / MANIFEST
            mp.parent.mkdir(parents=True, exist_ok=True)
            tmp = mp.with_suffix(".tmp")
            tmp.write_text(json.dumps(next_manifest, indent=2) + "\n", encoding="utf-8")
            os.replace(tmp, mp)
        project_lock = target / ".resonance" / "project-skills.lock.json"
        if project_lock.is_file():
            project_check = (target if work["profile"] == "source" else source) / ".forge" / "project_skills.py"
            if not project_check.is_file():
                raise RuntimeError("project skill lock exists but its verifier is missing")
            result = subprocess.run(
                [sys.executable, str(project_check), "--check", "--root", str(target)], cwd=target,
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
            )
            if result.returncode != 0:
                raise RuntimeError(
                    "post-update project skill verification failed:\n"
                    f"{result.stdout}\n{result.stderr}"
                )
        journal["status"] = "complete"
        journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")
        return backup
    except BaseException as apply_error:
        try:
            rollback(backup)
        except BaseException as rollback_error:
            raise UpdateRollbackError(apply_error, rollback_error, backup) from rollback_error
        raise
    finally:
        shutil.rmtree(stage, ignore_errors=True)


def doctor(source: Path, target: Path, profile: str | None = None) -> dict:
    try:
        work = plan(source, target, profile)
        pending = []
        roots = (target / ".resonance" / "backups", target / ".resonance" / "updates")
        journals = [journal for root in roots if root.is_dir() for journal in root.glob("*/journal.json")]
        for journal in journals:
            try:
                if json.loads(journal.read_text(encoding="utf-8")).get("status") not in ("complete", "rolled-back"):
                    pending.append(str(journal.parent))
            except Exception:
                pending.append(str(journal.parent))
        return {"ok": not work["conflicts"] and not pending, "pending_recovery": pending, **work}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def rollback(backup: Path) -> None:
    if backup.is_symlink():
        raise ValueError("recovery journal path cannot be a symlink")
    backup = backup.resolve()
    journal_path = backup / "journal.json"
    inside(backup, journal_path)
    journal = json.loads(journal_path.read_text(encoding="utf-8"))
    target = Path(journal["target"]).resolve()
    if journal.get("schema") == 2:
        if backup.parent != target / ".resonance" / "updates" or journal.get("transaction_id") != backup.name:
            raise ValueError("recovery journal is outside its recorded target")
    elif backup.parent != target / ".resonance" / "backups":
        raise ValueError("legacy backup journal is outside its recorded target")
    entries = journal.get("entries", [])
    if not isinstance(entries, list):
        raise ValueError("recovery journal entries are invalid")
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("recovery journal entry is invalid")
        rel = safe_relative(entry.get("path", ""))
        if rel in seen:
            raise ValueError(f"duplicate recovery path: {rel}")
        seen.add(rel)
        inside(target, target / rel)
        if not isinstance(entry.get("existed"), bool):
            raise ValueError(f"invalid recovery entry for {rel}")

    git_paths = [entry["path"] for entry in entries
                 if entry.get("existed") is True and entry.get("source") == "git"]
    git_blobs = {}
    if git_paths:
        git_root = Path(journal.get("git_root", "")).resolve()
        git_ref, git_commit_hash = journal.get("git_ref"), journal.get("git_commit")
        transaction_id = journal.get("transaction_id")
        if (not isinstance(transaction_id, str) or not isinstance(git_ref, str)
                or git_ref != f"refs/resonance/updates/{transaction_id}"
                or not isinstance(git_commit_hash, str) or len(git_commit_hash) != 40
                or any(ch not in "0123456789abcdef" for ch in git_commit_hash.lower())):
            raise ValueError("invalid pinned Git recovery metadata")
        pinned = git_output(target, "rev-parse", "--verify", f"{git_ref}^{{commit}}").decode().strip().lower()
        actual_root = Path(git_output(target, "rev-parse", "--show-toplevel").decode().strip()).resolve()
        actual_prefix = git_output(target, "rev-parse", "--show-prefix").decode().strip().strip("/")
        if pinned != git_commit_hash.lower() or actual_root != git_root or actual_prefix != journal.get("git_prefix", ""):
            raise ValueError("pinned recovery repository or commit changed")
        wanted = set(git_paths)
        prefix = journal.get("git_prefix", "").strip("/")
        tree = git_output(git_root, "ls-tree", "-r", "-z", "--full-tree", git_commit_hash)
        refs = {}
        for record in tree.split(b"\0"):
            if not record:
                continue
            metadata, raw_path = record.split(b"\t", 1)
            tree_mode, kind, oid = metadata.decode("ascii").split()
            git_path = raw_path.decode("utf-8", errors="strict")
            if prefix:
                if not git_path.startswith(prefix + "/"):
                    continue
                rel = git_path[len(prefix) + 1:]
            else:
                rel = git_path
            if rel in wanted:
                refs[rel] = (tree_mode, kind, oid)
        oids = []
        for entry in entries:
            rel = entry["path"]
            if rel not in wanted:
                continue
            ref = refs.get(rel)
            if (ref is None or ref[0] not in ("100644", "100755") or ref[1] != "blob"
                    or ref[2] != entry.get("blob_oid")):
                raise ValueError(f"recovery blob does not match pinned path: {rel}")
            oids.append(ref[2])
        contents = git_blob_batch(git_root, list(dict.fromkeys(oids)))
        git_blobs = {rel: (refs[rel][0], refs[rel][2], contents[refs[rel][2]]) for rel in wanted}

    restores = []
    for entry in entries:
        rel, existed = entry["path"], entry["existed"]
        dst = inside(target, target / rel)
        if not existed:
            restores.append((rel, dst, False, None, None))
            continue
        source_kind = entry.get("source", "file")
        if source_kind == "git":
            git_mode, _, data = git_blobs[rel]
            if hashlib.sha256(data).hexdigest() != entry.get("sha256"):
                raise ValueError(f"recovery blob hash mismatch: {rel}")
            mode = entry.get("mode")
            if type(mode) is not int or mode < 0 or mode > 0o7777:
                raise ValueError(f"invalid saved mode for {rel}")
            if bool(mode & 0o111) != (git_mode == "100755"):
                raise ValueError(f"recovery executable mode mismatch: {rel}")
        elif source_kind == "file":
            saved = inside(backup, backup / "files" / rel)
            if not saved.is_file():
                if journal.get("status") == "backing-up" and journal.get("schema") == 1:
                    continue
                raise ValueError(f"recovery preimage is missing: {saved}")
            data = saved.read_bytes()
            if entry.get("sha256") and hashlib.sha256(data).hexdigest() != entry["sha256"]:
                raise ValueError(f"recovery preimage hash mismatch: {rel}")
            mode = entry.get("mode", stat.S_IMODE(os.stat(saved, follow_symlinks=False).st_mode))
            if type(mode) is not int or mode < 0 or mode > 0o7777:
                raise ValueError(f"invalid saved mode for {rel}")
        else:
            raise ValueError(f"unknown recovery source for {rel}")
        restores.append((rel, dst, True, data, mode))

    for rel, dst, existed, data, mode in reversed(restores):
        if not existed:
            if dst.is_file():
                dst.unlink()
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary_name = tempfile.mkstemp(prefix=".resonance-restore-", dir=dst.parent)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
            os.chmod(temporary, mode)
            os.replace(temporary, dst)
        finally:
            temporary.unlink(missing_ok=True)
    journal["status"] = "rolled-back"
    journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")


def summary(work: dict) -> str:
    if "error" in work:
        return f"Plan: blocked\nReason: {work['error']}"
    if work["conflicts"] or work.get("pending_recovery") or work.get("ok") is False:
        state = "blocked"
    elif not work["writes"] and not work["removes"] and not work["manifest_write"]:
        state = "already current"
    elif not work["writes"] and not work["removes"]:
        state = "manifest-only update"
    else:
        state = "content update"
    lines = [
        f"Plan: {state}",
        f"Version: {work['version']} ({work['profile']})",
        f"Source revision: {work['revision']}",
        f"Plan digest: {work['plan_digest']}",
        f"Writes: {len(work['writes'])}; removals: {len(work['removes'])}; ownership manifest: {'change' if work['manifest_write'] else 'unchanged'}",
    ]
    if work["conflicts"]:
        lines.append(f"Blocked paths ({len(work['conflicts'])}):")
        for rel in work["conflicts"][:10]:
            reason = work["reasons"].get(rel, {}).get("message", "unverified local bytes")
            lines.append(f"  {rel}: {reason}")
        if len(work["conflicts"]) > 10:
            lines.append(f"  ... {len(work['conflicts']) - 10} more; use --json for the full list")
        if any(work["reasons"].get(path, {}).get("code") == "missing_managed_path" for path in work["conflicts"]):
            lines.append("Next step: restore the named path from the installed release, then preview again.")
        elif any(work["reasons"].get(path, {}).get("code") == "project_skill_locked" for path in work["conflicts"]):
            lines.append("Next step: review framework ownership and the project skill lock for the named path.")
        else:
            lines.append("Next step: review each local file, or select the verified installed release source, then preview again.")
    if work.get("pending_recovery"):
        lines.append(f"Pending recovery journals ({len(work['pending_recovery'])}):")
        lines.extend(f"  {path}" for path in work["pending_recovery"][:10])
        if len(work["pending_recovery"]) > 10:
            lines.append(f"  ... {len(work['pending_recovery']) - 10} more")
        lines.append("Next step: inspect and resolve each journal before applying another update.")
    elif state == "already current":
        lines.append("No files or recovery data will change.")
    elif work["baseline_error"]:
        lines.append(f"Historical ownership baseline unavailable: {work['baseline_error']}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if argv and argv[0] == "notice":
        notice = argparse.ArgumentParser(description="Manage optional Resonance update notices")
        notice.add_argument("action", choices=("enable", "disable", "status", "check"))
        notice.add_argument("--quiet", action="store_true")
        notice_args = notice.parse_args(argv[1:])
        if notice_args.action in ("enable", "disable"):
            enabled = notice_args.action == "enable"
            path = set_notice(enabled)
            print(f"update notices {'enabled' if enabled else 'disabled'}: {path}")
            return 0
        if notice_args.action == "status":
            print("enabled" if notice_state()["enabled"] else "disabled")
            return 0
        return check_notice(FRAMEWORK_VERSION, notice_args.quiet)
    ap = argparse.ArgumentParser(description="Preview or apply a transactional Resonance update")
    ap.add_argument("--source", type=Path)
    ap.add_argument("--target", type=Path)
    ap.add_argument("--version")
    ap.add_argument("--revision", help="full source commit printed by the reviewed preview")
    ap.add_argument("--plan-digest", help="digest printed by the reviewed preview")
    ap.add_argument("--profile", choices=sorted(PROFILE_ROOTS),
                    help="installation ownership profile; compiled targets omit .forge")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--doctor", action="store_true")
    ap.add_argument("--adopt", action="store_true",
                    help="record a pre-manifest installation without changing framework files")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--summary", action="store_true", help="show a compact human-readable plan")
    ap.add_argument("--rollback", type=Path, help="restore a recovery transaction or legacy backup directory")
    args = ap.parse_args(argv)
    if args.rollback:
        try:
            rollback(args.rollback)
            print(f"rolled back: {args.rollback}")
            return 0
        except (OSError, RuntimeError, ValueError, KeyError) as exc:
            print(f"rollback blocked: {exc}", file=sys.stderr)
            return 1
    if not args.source or not args.target:
        ap.error("--source and --target are required unless --rollback is used")
    if args.adopt:
        try:
            print(f"adopted ownership: {adopt(args.source, args.target, args.profile)}")
            return 0
        except (OSError, RuntimeError, ValueError, KeyError) as exc:
            print(f"adoption blocked: {exc}", file=sys.stderr)
            return 1
    try:
        result = doctor(args.source, args.target, args.profile) if args.doctor else plan(args.source, args.target, args.profile)
        if args.summary and not args.json:
            print(summary(result))
        elif (args.json and not args.apply) or args.doctor or not args.apply:
            print(json.dumps(result, indent=2))
    except (OSError, RuntimeError, ValueError, KeyError) as exc:
        print(f"update blocked: {exc}", file=sys.stderr)
        return 1
    if args.doctor:
        return 0 if result["ok"] else 1
    if not args.apply:
        return 1 if result["conflicts"] else 0
    if not args.version or not args.revision or not args.plan_digest:
        ap.error("--apply requires --version, --revision, and --plan-digest from the reviewed preview")
    try:
        transaction = apply(args.source, args.target, args.version, args.profile, args.revision, args.plan_digest)
    except (OSError, RuntimeError, ValueError, KeyError) as exc:
        print(f"update blocked: {exc}", file=sys.stderr)
        return 1
    if transaction is None:
        if args.json:
            print(json.dumps({**result, "status": "already_current", "recovery_journal": None}, indent=2))
        else:
            print("already current; no files or recovery data changed.")
    else:
        if args.json:
            print(json.dumps({**result, "status": "updated", "recovery_journal": str(transaction / "journal.json")}, indent=2))
        else:
            print(f"updated to {version(args.source)} ({args.profile or 'recorded profile'}); recovery journal: {transaction / 'journal.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
