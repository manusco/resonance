---
name: resonance-ops-update-resonance
description: The Maintainer. Upgrades the Resonance framework kernel without breaking the user's project context. Use when migrating to a new version of Resonance.
archetype: procedure
---

# /resonance-ops-update-resonance: upgrade the framework, preserve the context

> **Role:** the Maintainer.
> **Invoked as:** `/update-resonance` (to upgrade the Resonance OS).
> **Input:** Upstream Changes.
> **Output:** Upgraded `.forge` and `.agents` folders.
> **Definition of Done:** Resonance framework files are updated while `00_soul.md` and user memory remain intact. `/system-health` passes after the upgrade.

You are upgrading the OS. You must not overwrite user customizations. You must back up before you touch anything.

## Prerequisites (fail fast)

- [ ] Network access allowed.
- [ ] Git Status clean.

## Algorithm (Execution)

Copy this checklist and tick items as you go.

1. **Verify ownership boundary**: Confirm `.resonance/` will not be touched. It holds the user's soul, state, and memory. The upgrade only touches `.agents/` and `AGENTS.md`. → verify: `.resonance/` is not in scope.
2. **Clone latest**: Fetch the new version to a temp location outside the project root. → verify: temp directory exists and is not inside the project.
3. **Delete `.agents/`**: Remove the entire old skill library. Do not overwrite. Delete. Overwriting leaves ghost files from renamed or removed skills, which the agent will silently read and contradict new skills. → verify: `.agents/` no longer exists.
4. **Copy new `.agents/`**: Copy the compiled skill library from the temp location. → verify: `.agents/skills/` contains the new domain structure.
5. **Copy `AGENTS.md`** and the `resonance.sh` / `resonance.ps1` scripts. → verify: files exist.
6. **Verify the upgrade**: Run `/system-health`. It must report the correct skill count. Flag if score < 80. → verify: health check passes.
7. **Clean up**: Remove the temp directory.


## Recovery

- Something went wrong after deleting `.agents/` → clone the repo and copy `.agents/` back in. This is faster and cleaner than restoring a backup of an old version.
- `/system-health` fails (score < 50) → do not use the system. Re-run steps 3–5 from a fresh clone. The issue is almost always a partial copy.
- Conflict in `00_soul.md` → this should not happen because `.resonance/` is never touched. If it does happen, the user has accidentally run the wrong command. Stop and confirm scope before proceeding.


## Out of Scope

- Modifying the application code (this is strictly a framework upgrade tool).

## Cognitive Frameworks

### The Transplant
Upgrading a framework while preserving the user's project memory is like a transplant. You must preserve the Soul (`00_soul.md`) and the Memory (`01_state.md`, `02_memory.md`).

## Reference Library

- **[Completion Attestation](../core/references/completion_attestation.md)**: Required sign-off format.

{{RESOLVER:decision_brief}}

{{RESOLVER:completion}}

{{RESOLVER:voice}}

{{OVERLAY}}
