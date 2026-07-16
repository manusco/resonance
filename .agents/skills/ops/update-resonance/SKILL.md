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

1. **Verify ownership boundary**: The upgrade replaces `.agents/` and `AGENTS.md` and never edits the user's soul, state, or lessons. Single exception: step 6 MOVES legacy lessons into the user's loaded index (content preserved, dead container removed). → verify: nothing else under `.resonance/` is in scope.
2. **Clone latest**: Fetch the new version to a temp location outside the project root. → verify: temp directory exists and is not inside the project.
3. **Delete `.agents/`**: Remove the entire old skill library. Do not overwrite. Delete. Overwriting leaves ghost files from renamed or removed skills, which the agent will silently read and contradict new skills. → verify: `.agents/` no longer exists.
4. **Copy new `.agents/`**: Copy the compiled skill library from the temp location. → verify: `.agents/skills/` contains the new domain structure.
5. **Copy `AGENTS.md`** and the `resonance.sh` / `resonance.ps1` scripts. → verify: files exist.
6. **Migrate legacy memory**: If `.resonance/learnings.jsonl` exists, append each entry as a dated one-line lesson under `## Lessons` in `.resonance/02_memory.md`, then delete the file. Lessons in a store no host loads are lessons lost; fleet repos kept writing there for months while nothing read them. → verify: `learnings.jsonl` is gone and its lessons appear in the loaded index.
7. **Verify the upgrade**: Run `/system-health`. It must report the correct skill count. Flag if score < 80. → verify: health check passes.
8. **Clean up**: Remove the temp directory.

## Recovery

- Something went wrong after deleting `.agents/` → clone the repo and copy `.agents/` back in. This is faster and cleaner than restoring a backup of an old version.
- `.agents/skills` is empty after the copy → the copy failed silently and every specialist is disabled. Re-copy from the temp clone before anything else, then verify the skill count via the wake script or `/system-health`.
- `/system-health` fails (score < 50) → do not use the system. Re-run steps 3-5 from a fresh clone. The issue is almost always a partial copy.
- Conflict in `00_soul.md` → this should not happen because `.resonance/` is never touched. If it does happen, the user has accidentally run the wrong command. Stop and confirm scope before proceeding.

## Out of Scope

- Modifying the application code (this is strictly a framework upgrade tool).

## Cognitive Frameworks

### The Transplant
Upgrading a framework while preserving the user's project memory is like a transplant. You must preserve the Soul (`00_soul.md`) and the Memory (`01_state.md`, `02_memory.md`).

## Reference Library

- **[Completion Attestation](../core/references/completion_attestation.md)**: Required sign-off format.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory, `.resonance/02_memory.md`, which loads at session start).

> **Model note (Claude):** Strong native reasoning. Do not narrate "let me think step by step" or pad with chain-of-thought; think, then act. Prefer the dedicated file and search tools over shell. State assumptions briefly, then proceed.
