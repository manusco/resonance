#!/usr/bin/env python3
"""Transactional Resonance installer and updater."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
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
FRAMEWORK_VERSION = "2.5.34"


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
    return resolved


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
    )}
    return hashlib.sha256(json.dumps(stable, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


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
    manifest = {"schema": 1, "version": "adopted", "profile": profile,
                "files": {r: digest(p) for r, p in files.items()}}
    path = target / MANIFEST
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return path


def plan(source: Path, target: Path, profile: str | None = None) -> dict:
    source, target = source.resolve(), target.resolve()
    if source == target:
        raise ValueError("source and target must differ")
    current = load_manifest(target)
    profile = resolve_profile(target, profile, current)
    incoming = source_files(source, profile=profile)
    preserved = []
    for rel in PRESERVE_IF_UNOWNED:
        destination = inside(target, target / rel)
        if rel in incoming and destination.is_file() and rel not in current["files"]:
            incoming.pop(rel)
            preserved.append(rel)
    conflicts, writes, removes = [], [], []
    for rel, src in incoming.items():
        dst = inside(target, target / rel)
        prior = current["files"].get(rel)
        if dst.exists() and (not prior or digest(dst) != prior):
            conflicts.append(rel)
        elif not dst.exists() or digest(dst) != digest(src):
            writes.append(rel)
    for rel, prior in current["files"].items():
        dst = inside(target, target / rel)
        if rel not in incoming and dst.is_file():
            if digest(dst) == prior:
                removes.append(rel)
            else:
                conflicts.append(rel)
    result = {"version": version(source), "revision": source_revision(source),
            "profile": profile, "writes": sorted(writes),
            "removes": sorted(removes), "conflicts": sorted(set(conflicts)),
            "preserved": sorted(preserved),
            "files": {rel: digest(src) for rel, src in incoming.items()}}
    result["plan_digest"] = plan_digest(result)
    return result


def apply(source: Path, target: Path, expected_version: str | None = None,
          profile: str | None = None, expected_revision: str | None = None,
          expected_plan_digest: str | None = None) -> Path:
    source, target = source.resolve(), target.resolve()
    work = plan(source, target, profile)
    if expected_version and work["version"] != expected_version.lstrip("v"):
        raise ValueError(f"source version {work['version']} does not match requested {expected_version}")
    if expected_revision and work["revision"] != expected_revision.lower():
        raise ValueError("source commit does not match the reviewed revision")
    if expected_plan_digest and work["plan_digest"] != expected_plan_digest.lower():
        raise ValueError("update plan changed after review")
    if work["conflicts"]:
        raise ValueError("user-owned or modified managed files block update: " + ", ".join(work["conflicts"]))
    required = (".forge/forge.py", ".forge/validate_skill.py", ".forge/eval_integrity.py")
    if work["profile"] == "source":
        missing = [rel for rel in required if rel not in work["files"]]
        if missing:
            raise ValueError("source is incomplete; missing required validators: " + ", ".join(missing))
    verify_write_access(target, work["writes"] + work["removes"] + [MANIFEST])
    stamp = time.strftime("%Y%m%d-%H%M%S") + f"-{time.time_ns() % 1_000_000_000:09d}"
    backup = target / ".resonance" / "backups" / f"resonance-update-{stamp}"
    backup.mkdir(parents=True, exist_ok=False)
    journal = {"schema": 1, "status": "backing-up", "version": work["version"],
               "profile": work["profile"],
               "target": str(target), "entries": []}
    journal_path = backup / "journal.json"
    journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")
    touched = work["writes"] + work["removes"] + [MANIFEST]
    for rel in touched:
        dst = inside(target, target / rel)
        existed = dst.is_file()
        if existed:
            saved = backup / "files" / rel
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, saved)
        journal["entries"].append({"path": rel, "existed": existed})
        journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")
    journal["status"] = "applying"
    journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")
    stage_root = target / ".resonance" / "tmp"
    stage_root.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="resonance-stage-", dir=stage_root))
    try:
        for rel in work["writes"]:
            staged = stage / rel
            staged.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / rel, staged)
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
        manifest = {"schema": 1, "version": work["version"], "profile": work["profile"],
                    "files": work["files"]}
        mp = target / MANIFEST
        mp.parent.mkdir(parents=True, exist_ok=True)
        tmp = mp.with_suffix(".tmp")
        tmp.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
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
        root = target / ".resonance" / "backups"
        for journal in root.glob("resonance-update-*/journal.json") if root.is_dir() else []:
            try:
                if json.loads(journal.read_text(encoding="utf-8")).get("status") not in ("complete", "rolled-back"):
                    pending.append(str(journal.parent))
            except Exception:
                pending.append(str(journal.parent))
        return {"ok": not work["conflicts"] and not pending, "pending_recovery": pending, **work}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def rollback(backup: Path) -> None:
    backup = backup.resolve()
    journal_path = backup / "journal.json"
    journal = json.loads(journal_path.read_text(encoding="utf-8"))
    target = Path(journal["target"]).resolve()
    for entry in reversed(journal.get("entries", [])):
        rel, existed = entry["path"], entry["existed"]
        dst = inside(target, target / rel)
        saved = backup / "files" / rel
        if existed and saved.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(saved, dst)
        elif not existed and dst.is_file():
            dst.unlink()
    journal["status"] = "rolled-back"
    journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")


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
    ap.add_argument("--rollback", type=Path, help="restore a backup whose journal is applying")
    args = ap.parse_args(argv)
    if args.rollback:
        rollback(args.rollback)
        print(f"rolled back: {args.rollback}")
        return 0
    if not args.source or not args.target:
        ap.error("--source and --target are required unless --rollback is used")
    if args.adopt:
        print(f"adopted ownership: {adopt(args.source, args.target, args.profile)}")
        return 0
    result = doctor(args.source, args.target, args.profile) if args.doctor else plan(args.source, args.target, args.profile)
    if args.json or args.doctor or not args.apply:
        print(json.dumps(result, indent=2))
    if args.doctor:
        return 0 if result["ok"] else 1
    if not args.apply:
        return 1 if result["conflicts"] else 0
    if not args.version or not args.revision or not args.plan_digest:
        ap.error("--apply requires --version, --revision, and --plan-digest from the reviewed preview")
    backup = apply(args.source, args.target, args.version, args.profile, args.revision, args.plan_digest)
    print(f"updated to {version(args.source)} ({args.profile or 'recorded profile'}); backup: {backup}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
