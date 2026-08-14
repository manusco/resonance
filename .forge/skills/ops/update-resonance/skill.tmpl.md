---
name: resonance-ops-update-resonance
description: The Maintainer. Upgrades the Resonance framework kernel with a preflight plan, backup, scoped replacement, rollback path, and verification. Use when migrating a project to a new version of Resonance.
archetype: procedure
---

# /resonance-ops-update-resonance: upgrade the framework, preserve the project

> **Role:** the Maintainer.
> **Invoked as:** `/update-resonance`.
> **Input:** target project, desired Resonance version or source checkout.
> **Output:** upgraded Resonance framework files, verified against the target project.
> **Definition of Done:** managed framework files are upgraded, project memory and application code are untouched, backups exist, validation passes, and the operator can see exactly what changed.

You are upgrading a public framework inside a real project. Treat the project as the source of truth. Do not force a bulk replacement over a dirty or customized workspace.

## Prerequisites (fail fast)

- [ ] Source version is known and available.
- [ ] Target project root is confirmed.
- [ ] Git status has been classified by path.
- [ ] No unresolved conflicts exist in any path the upgrade would touch.
- [ ] A backup location outside the managed replacement paths is ready.

## Ownership Boundary

### Managed by the framework

These may be upgraded when preflight says they are safe:

- `.agents/skills/`
- `.forge/`
- `.claude/skills/`
- `.cursor/skills/`
- `.codex/prompts/`
- `.opencode/command/`
- `resonance.sh`
- `resonance.ps1`
- generated bridge files when the target has no local edits to them

### Project-owned

Never overwrite these as part of a framework upgrade:

- `.resonance/00_soul.md`
- `.resonance/01_state.md`
- `.resonance/02_memory.md`
- `.resonance/ledger/`
- `.resonance/memory/`
- application code
- project docs, plans, audits, handovers, and tests
- project-specific `AGENTS*.md`, `CLAUDE*.md`, or host settings unless the diff proves they are generated framework bridges with no local edits

Legacy exception: if `.resonance/learnings.jsonl` exists and the user approves the migration, append its lessons into `.resonance/02_memory.md` and remove the legacy file only after the append is verified.

## Algorithm

Copy this checklist and tick items as you go.

0. **Read the project**: Inspect `git status --short`, existing Resonance directories, and the target's `AGENTS.md` / `CLAUDE.md` shape. -> verify: local changes are grouped as framework-managed, project-owned, or unrelated.
1. **Plan first**: Print a plan with source version, target project, managed paths to touch, project-owned paths excluded, backup path, validation commands, and rollback command. -> verify: no file has changed yet.
2. **Block unsafe states**: Stop if any touched path has an unresolved conflict, staged deletion, unknown ownership, or local customization that cannot be classified. Dirty application files outside the managed paths are context, not a blocker. -> verify: blocker names exact paths.
3. **Back up before edits**: Copy every touched existing path to `.resonance/backups/resonance-upgrade-<timestamp>/` or another user-approved backup outside replacement paths. -> verify: backup contains the old files.
4. **Stage the new framework aside**: Copy source framework files into a temporary staging directory inside `.resonance/tmp/` or system temp, never directly over live files. -> verify: staged `.agents/skills` and `.forge` counts match the source.
5. **Compare and classify**: Diff staged framework files against live managed paths. Preserve target-local files that are outside generated trees. For generated trees, replacement is allowed only after backup and staging validation. -> verify: no project-owned path appears in the write set.
6. **Apply atomically by path**: Replace generated framework directories with a prepared directory swap or remove-and-rename inside the confirmed project root. Copy scripts and generated bridges only when allowed by the ownership boundary. -> verify: each write target resolves inside the project root.
7. **Migrate legacy memory only with proof**: If approved, append legacy lessons, verify they appear in `.resonance/02_memory.md`, then remove `learnings.jsonl`. -> verify: no lesson is lost.
8. **Regenerate if the target ships `.forge`**: Run the target's Forge build when `.forge/forge.py` exists. If the project intentionally has only compiled `.agents`, do not invent `.forge`; copy compiled skills only. -> verify: generated files are consistent with source mode.
9. **Validate**: Run the strongest available checks in the target: framework validation, command shim checks, `/system-health` or `resonance.ps1`, and any project-specific smoke check that does not require unrelated dirty files to be resolved. -> verify: failures are reported with exact commands and output.
10. **Report**: Summarize changed paths, preserved project-owned paths, backup path, validation output, and rollback instructions.

## Recovery

- Preflight finds unresolved conflicts in touched paths -> stop. Do not edit.
- Preflight finds unrelated dirty application files -> proceed only if the write set excludes them and report that they were left alone.
- Backup fails -> stop before edits.
- Staging validation fails -> remove staging directory and stop.
- Apply fails midway -> restore touched paths from backup, then rerun validation.
- Validation fails after apply -> leave the backup in place, report failure, and offer rollback. Do not claim success.
- `.agents/skills` is empty after apply -> restore from backup immediately. Empty skills disable the framework.
- Project-specific `AGENTS.md` differs from framework `AGENTS.md` -> do not overwrite silently. Either preserve it and add missing bridge guidance manually, or ask for approval with a diff.

## Out of Scope

- Modifying application code.
- Resolving unrelated merge conflicts.
- Rewriting project memory or soul files.
- Deleting local customizations because the framework source lacks them.

## Cognitive Frameworks

### The Safe Upgrade Path

An upgrade is a migration, not a bulk copy. The work is plan, backup, staged copy, ownership check, atomic apply, validation, and rollback. If any part is not verifiable, stop before touching files.

### Generated vs. Owned

Generated framework trees can be replaced after backup because stale files are dangerous. Project-owned files must be merged or left alone because overwriting them loses context.

## Reference Library

- **[Completion Attestation](../core/references/completion_attestation.md)**: Required sign-off format.

{{RESOLVER:operating_standard}}

{{OVERLAY}}
