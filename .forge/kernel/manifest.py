#!/usr/bin/env python3
"""Generate machine-readable skill manifests from compiled skills."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(".agents/skills")
OUT = Path("docs/skill-manifest.json")
VALID_ARCHETYPES = {"knowledge", "procedure", "orchestration"}
VALID_ACTIVATION = {"automatic", "manual"}
VALID_AUTHORITY = {"advisory", "consequential", "human"}
VALID_FAILURE_POLICY = {"stop", "degrade", "escalate"}
VALID_CONTRACT_VERSIONS = {1}
VALID_CONTRACT_STAGES = {"FRAME", "PLAN", "EXECUTE", "VERIFY", "APPROVE", "PUBLISH"}
VALID_COMPATIBILITY = {"active", "provisional", "deprecated", "alias", "retired"}
VALID_ARTIFACT_RIGHTS = {
    "read", "create", "append_evidence", "modify", "review", "approve", "publish", "execute",
}
COMPATIBLE_CHANNELS = {"user_request", "plan", "evidence", "decision", "artifact", "recommendation"}
UNSAFE_WRITE_SETS = {".", "./", "*", "**", "AGENTS.md", ".agents", ".forge", ".resonance"}
CHANNEL_ALIASES = {
    "copywriter_scope": "copy_scope",
    "studio_scope": "creative_scope",
    "founder_os_scope": "founder_os_scope",
    "skill_author_resonance_skill_author_scope": "skill_author_scope",
}
LIST_FIELDS = {
    "triggers",
    "negative_triggers",
    "inputs",
    "outputs",
    "invokes",
    "side_effects",
    "write_sets",
    "entrypoints",
}

COMPOSITION_FIELDS = {
    "contract_version", "job_id", "stage", "contributes_to", "reviews", "finalizes",
    "artifact_access", "dispatch_conditions", "compatibility",
}


def frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    raw = text[3:end] if end != -1 else ""
    data: dict[str, object] = {}
    current = None
    for line in raw.splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            current = m.group(1)
            value = m.group(2).strip()
            data[current] = value.strip("\"'") if value else []
            continue
        m = re.match(r"^\s*-\s*(.+?)\s*$", line)
        if m and current:
            data.setdefault(current, [])
            if isinstance(data[current], list):
                data[current].append(m.group(1).strip())
    return data


def skill_id_to_path(skill_id: str) -> str:
    prefix = "resonance-"
    raw = skill_id[len(prefix):] if skill_id.startswith(prefix) else skill_id
    parts = raw.split("-")
    if len(parts) < 2:
        return raw
    domains = {
        "design",
        "engineering",
        "finance",
        "leadership",
        "marketing",
        "ops",
        "people",
        "research",
        "sales",
        "software",
        "strategy",
        "success",
    }
    if parts[0] in domains:
        return parts[0] + "/" + "-".join(parts[1:])
    return raw.replace("-", "/")


def list_field(fm: dict, key: str) -> list[str]:
    value = fm.get(key, [])
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def inferred_outputs(archetype: str) -> list[str]:
    if archetype == "orchestration":
        return ["plan", "evidence", "decision"]
    if archetype == "procedure":
        return ["artifact", "recommendation"]
    return ["guidance"]


def inferred_side_effects(archetype: str) -> list[str]:
    if archetype == "orchestration":
        return ["may_coordinate_work", "may_write_files"]
    if archetype == "procedure":
        return ["may_write_files"]
    return []


def default_failure_policy(archetype: str) -> str:
    return "stop" if archetype in {"orchestration", "procedure"} else "degrade"


def normalize_entry(sk: Path, root: Path) -> dict | None:
    text = sk.read_text(encoding="utf-8", errors="replace")
    fm = frontmatter(text)
    if not fm.get("name"):
        return None
    archetype = str(fm.get("archetype", "knowledge"))
    orchestration = archetype == "orchestration"
    inputs = list_field(fm, "inputs") if orchestration else list_field(fm, "inputs") or ["user_request"]
    side_effects = (
        list_field(fm, "side_effects")
        if orchestration else list_field(fm, "side_effects") or inferred_side_effects(archetype)
    )
    authority = str(
        fm.get("authority", "" if orchestration else "consequential" if side_effects else "advisory")
    )
    contract_version = str(fm.get("contract_version", "")).strip()
    entry = {
        "schema_version": 1,
        "id": str(fm["name"]),
        "path": sk.relative_to(root).as_posix(),
        "archetype": archetype,
        "owner": str(
            fm.get("owner", "" if orchestration else skill_id_to_path(str(fm["name"])).replace("/", "."))
        ),
        "activation": str(fm.get(
            "activation",
            "" if orchestration else "manual" if archetype == "procedure" else "automatic",
        )),
        "authority": authority,
        "triggers": list_field(fm, "triggers") if orchestration else list_field(fm, "triggers") or [str(fm.get("description", ""))],
        "negative_triggers": list_field(fm, "negative_triggers"),
        "inputs": inputs,
        "outputs": list_field(fm, "outputs") if orchestration else list_field(fm, "outputs") or inferred_outputs(archetype),
        "invokes": list_field(fm, "invokes"),
        "side_effects": side_effects,
        "write_sets": list_field(fm, "write_sets"),
        "entrypoints": list_field(fm, "entrypoints"),
        "failure_policy": str(fm.get("failure_policy", "" if orchestration else default_failure_policy(archetype))),
    }
    if any(field in fm for field in COMPOSITION_FIELDS):
        entry.update({
            "contract_version": int(contract_version) if contract_version.isdigit() else contract_version,
            "job_id": str(fm.get("job_id", "")),
            "stage": str(fm.get("stage", "")),
            "contributes_to": list_field(fm, "contributes_to"),
            "reviews": list_field(fm, "reviews"),
            "finalizes": list_field(fm, "finalizes"),
            "artifact_access": list_field(fm, "artifact_access"),
            "dispatch_conditions": list_field(fm, "dispatch_conditions"),
            "compatibility": str(fm.get("compatibility", "")),
        })
    return entry


def artifact_rights(items: list[str]) -> tuple[dict[str, set[str]], list[str]]:
    """Parse flat `<artifact>:<right>[,<right>]` declarations."""
    parsed: dict[str, set[str]] = {}
    issues: list[str] = []
    for item in items:
        artifact, sep, raw_rights = item.partition(":")
        rights = {right.strip().lower() for right in raw_rights.split(",") if right.strip()}
        if not sep or not artifact.strip() or not rights:
            issues.append(f"invalid artifact_access '{item}' (expected artifact:right[,right])")
            continue
        invalid = rights - VALID_ARTIFACT_RIGHTS
        if invalid:
            issues.append(f"invalid artifact right(s) {sorted(invalid)} in '{item}'")
        parsed.setdefault(artifact.strip(), set()).update(rights)
    return parsed, issues


def composition_warnings(data: list[dict], canary_ids: set[str]) -> list[str]:
    """Return warning-only v1 canary findings. This never changes strict validation."""
    warnings: list[str] = []
    by_job = {entry.get("job_id"): entry for entry in data if entry.get("job_id")}
    job_counts: dict[str, int] = defaultdict(int)
    for entry in data:
        if entry.get("job_id"):
            job_counts[str(entry["job_id"])] += 1

    for entry in data:
        sid = entry["id"]
        present = COMPOSITION_FIELDS & set(entry)
        version = entry.get("contract_version", 0)
        if sid in canary_ids and not present:
            warnings.append(f"composition canary: '{sid}' is v0 and has no contract")
            continue
        if not present:
            continue
        if version == 0:
            warnings.append(f"composition canary: '{sid}' mixes v0 with v1 fields; explicit migration required")
            continue
        if version not in VALID_CONTRACT_VERSIONS:
            warnings.append(f"composition canary: '{sid}' has unknown contract_version '{version}'; fail closed")
            continue
        missing = [field for field in COMPOSITION_FIELDS if field not in entry]
        if missing:
            warnings.append(f"composition canary: '{sid}' v1 contract is missing {sorted(missing)}")
            continue
        if not entry.get("job_id"):
            warnings.append(f"composition canary: '{sid}' has an empty job_id")
        elif job_counts[str(entry["job_id"])] > 1:
            warnings.append(f"composition canary: job_id '{entry['job_id']}' is declared more than once")
        if entry.get("stage") not in VALID_CONTRACT_STAGES:
            warnings.append(f"composition canary: '{sid}' has invalid stage '{entry.get('stage')}'")
        if entry.get("compatibility") not in VALID_COMPATIBILITY:
            warnings.append(f"composition canary: '{sid}' has invalid compatibility '{entry.get('compatibility')}'")

        access, access_issues = artifact_rights(entry.get("artifact_access", []))
        warnings.extend(f"composition canary: '{sid}' {issue}" for issue in access_issues)
        if not access:
            warnings.append(f"composition canary: '{sid}' has no valid artifact_access")
        own_job = entry.get("job_id")
        if own_job in entry.get("contributes_to", []):
            warnings.append(f"composition canary: '{sid}' contributes to its own job")
        if own_job in entry.get("reviews", []):
            warnings.append(f"composition canary: '{sid}' reviews its own job")
        if set(entry.get("contributes_to", [])) & set(entry.get("reviews", [])):
            warnings.append(f"composition canary: '{sid}' both contributes to and reviews the same job")
        for target in entry.get("contributes_to", []) + entry.get("reviews", []):
            peer = by_job.get(target)
            if peer is None:
                warnings.append(f"composition canary: '{sid}' references unknown job '{target}'")
            elif peer.get("contract_version", 0) != version:
                warnings.append(f"composition canary: '{sid}' and job '{target}' mix contract versions; reject")
        finalizes = set(entry.get("finalizes", []))
        for artifact in finalizes:
            if not ({"approve", "publish", "create", "modify"} & access.get(artifact, set())):
                warnings.append(f"composition canary: '{sid}' finalizes '{artifact}' without a finalizing artifact right")
        if entry.get("reviews") and not any("review" in rights for rights in access.values()):
            warnings.append(f"composition canary: '{sid}' reviews jobs without artifact review access")
        privileged = {right for rights in access.values() for right in rights} & {"approve", "publish", "execute"}
        if entry.get("authority") == "advisory" and privileged:
            warnings.append(f"composition canary: advisory '{sid}' declares privileged rights {sorted(privileged)}")
        if entry.get("compatibility") == "alias" and len(entry.get("contributes_to", [])) != 1:
            warnings.append(f"composition canary: alias '{sid}' must contribute to exactly one canonical job")
        if entry.get("compatibility") == "retired" and (entry.get("entrypoints") or entry.get("finalizes")):
            warnings.append(f"composition canary: retired '{sid}' retains an entrypoint or finalizer")
        if not entry.get("dispatch_conditions"):
            warnings.append(f"composition canary: '{sid}' has no dispatch_conditions")
    return sorted(set(warnings))


def manifest(root: Path = ROOT) -> list[dict]:
    out = []
    for sk in sorted(root.glob("**/SKILL.md")):
        entry = normalize_entry(sk, root)
        if entry:
            out.append(entry)
    return out


def validate(data: list[dict], roots: list[str] | None = None) -> list[str]:
    errors: list[str] = []
    by_id = {entry["id"]: entry for entry in data}
    if len(by_id) != len(data):
        seen: set[str] = set()
        for entry in data:
            sid = entry["id"]
            if sid in seen:
                errors.append(f"skill manifest: duplicate id '{sid}'")
            seen.add(sid)
    owners: dict[str, list[str]] = defaultdict(list)
    for entry in data:
        sid = entry["id"]
        owners[entry.get("owner", "")].append(sid)
        if entry.get("schema_version") != 1:
            errors.append(f"skill manifest: '{sid}' schema_version must be 1")
        if entry.get("archetype") not in VALID_ARCHETYPES:
            errors.append(f"skill manifest: '{sid}' has invalid archetype '{entry.get('archetype')}'")
        if entry.get("activation") not in VALID_ACTIVATION:
            errors.append(f"skill manifest: '{sid}' has invalid activation '{entry.get('activation')}'")
        if entry.get("authority") not in VALID_AUTHORITY:
            errors.append(f"skill manifest: '{sid}' has invalid authority '{entry.get('authority')}'")
        if entry.get("failure_policy") not in VALID_FAILURE_POLICY:
            errors.append(
                f"skill manifest: '{sid}' has invalid failure_policy '{entry.get('failure_policy')}'"
            )
        for key in LIST_FIELDS:
            if not isinstance(entry.get(key), list):
                errors.append(f"skill manifest: '{sid}' field '{key}' must be a list")
        for required in ("inputs", "outputs"):
            if not entry.get(required):
                errors.append(f"skill manifest: '{sid}' field '{required}' must not be empty")
        if entry.get("archetype") == "orchestration":
            if not entry.get("owner"):
                errors.append(f"skill manifest: orchestration '{sid}' must declare owner")
            if not entry.get("invokes"):
                errors.append(f"skill manifest: orchestration '{sid}' must declare invokes")
            if entry.get("failure_policy") == "degrade":
                errors.append(f"skill manifest: orchestration '{sid}' cannot default to degrade")
            if not entry.get("write_sets"):
                errors.append(f"skill manifest: orchestration '{sid}' must declare write_sets")
            for write_set in entry.get("write_sets", []):
                if write_set in UNSAFE_WRITE_SETS:
                    errors.append(f"skill manifest: orchestration '{sid}' has unsafe write_set '{write_set}'")
            if not entry.get("entrypoints"):
                errors.append(f"skill manifest: orchestration '{sid}' must declare entrypoints")
    for owner, skills in owners.items():
        if not owner:
            errors.append("skill manifest: empty owner")
        if len(skills) > 1:
            errors.append(f"skill manifest: owner '{owner}' assigned to multiple skills: {skills}")
    for entry in data:
        for target in entry.get("invokes", []):
            if target not in by_id:
                errors.append(f"skill manifest: '{entry['id']}' invokes unknown skill '{target}'")
                continue
            caller = entry
            callee = by_id[target]
            parts = target.replace("resonance-", "").split("-")
            target_channel = "_".join(parts[1:]) + "_scope" if len(parts) > 1 else ""
            domain_channel = parts[0] + "_scope" if parts else ""
            alias_channel = CHANNEL_ALIASES.get(target_channel, "")
            shared = set(caller.get("outputs", [])) & set(callee.get("inputs", []))
            if (
                not (shared - {"user_request"})
                and target_channel not in caller.get("outputs", [])
                and domain_channel not in caller.get("outputs", [])
                and alias_channel not in caller.get("outputs", [])
            ):
                errors.append(f"skill manifest: '{entry['id']}' cannot satisfy inputs for '{target}'")
            if caller.get("authority") == "advisory" and callee.get("authority") in {"consequential", "human"}:
                errors.append(f"skill manifest: '{entry['id']}' escalates authority through '{target}'")
    for left in data:
        for right in data:
            if left["id"] >= right["id"]:
                continue
            shared_writes = set(left.get("write_sets", [])) & set(right.get("write_sets", []))
            if shared_writes:
                errors.append(
                    f"skill manifest: write_set collision {sorted(shared_writes)} between "
                    f"'{left['id']}' and '{right['id']}'"
                )
    graph_roots = roots or [entry["id"] for entry in data if entry.get("entrypoints")]
    errors.extend(graph_errors(data, graph_roots))
    return errors


def graph_errors(data: list[dict], roots: list[str] | None = None) -> list[str]:
    by_id = {entry["id"]: entry for entry in data}
    errors: list[str] = []
    graph = {entry["id"]: [t for t in entry.get("invokes", []) if t in by_id] for entry in data}
    temporary: set[str] = set()
    permanent: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> None:
        if node in permanent:
            return
        if node in temporary:
            cycle = stack[stack.index(node):] + [node]
            errors.append(f"skill graph: cycle detected: {' -> '.join(cycle)}")
            return
        temporary.add(node)
        stack.append(node)
        for nxt in graph.get(node, []):
            visit(nxt)
        stack.pop()
        temporary.remove(node)
        permanent.add(node)

    for node in graph:
        visit(node)

    inbound: dict[str, int] = defaultdict(int)
    for targets in graph.values():
        for target in targets:
            inbound[target] += 1
    start = roots or [entry["id"] for entry in data if entry.get("archetype") == "orchestration"]
    reached: set[str] = set()
    q = deque(start)
    while q:
        node = q.popleft()
        if node in reached:
            continue
        reached.add(node)
        q.extend(graph.get(node, []))
    for entry in data:
        if entry.get("archetype") == "procedure" and inbound[entry["id"]] == 0:
            # Standalone procedures can be invoked directly through commands.
            continue
        if entry.get("archetype") == "knowledge":
            continue
        if entry["id"] not in reached:
            errors.append(f"skill graph: '{entry['id']}' is not reachable from an orchestrator")
    return errors


def main(argv: list[str]) -> int:
    data = manifest()
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if "--check" in argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print(f"DRIFT  {OUT} is out of date. Run: py .forge/kernel/manifest.py")
            return 1
        print(f"fresh  {OUT}")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote  {OUT}  ({len(data)} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
