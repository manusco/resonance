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

## Default: latest stable release

An update notice is information, not authorization. If the user has not requested an upgrade, continue their task without updating. Never run apply because a session-start notice appeared.

When the user invokes `/update-resonance` without a source or version, use the latest stable **published GitHub Release**, never `main`. If `.forge/releases.py` is available and the target has an ownership manifest:

1. Run `python3 .forge/releases.py update --target <project>` (`py` on Windows). For a named release, add `--version <version>`.
2. Show the resolved version, commit, write/remove/conflict plan, project-owned exclusions, backup policy, validation, and rollback path. The helper clones the fixed official repository into temporary storage outside the target and runs that release's transactional updater in preview mode.
3. Stop on conflicts. Otherwise ask for approval of this exact preview. Invocation alone authorizes preview, not apply.
4. After approval, run the emitted command with the exact `--version`, `--revision`, and `--apply`. If the tag now points to another commit, stop and request a new preview and approval. Never remove the revision pin or fall back to an unpinned source.
5. Verify the completed journal, ownership manifest version, private skill lock, and validation output; report the backup and rollback instructions. The helper does not replace the safety checks below.

The automatic checker caches successes and failures for 24 hours outside the project, emits one notice per installed/latest version pair, and stays silent on unavailable GitHub or unknown installations. Use `python3 .forge/releases.py check --force` for an explicit diagnostic check. Never escalate network permissions for a background notice.

Legacy installations without the helper or manifest use Source Resolution and explicit adoption below. Framework source checkouts must be updated through their Git workflow, never by installing the framework over itself.

## Prerequisites (fail fast)

- [ ] Source version is resolved with the Source Resolution order below.
- [ ] Target project root is confirmed.
- [ ] Git status has been classified by path.
- [ ] No unresolved conflicts exist in any path the upgrade would touch.
- [ ] A backup location outside the managed replacement paths is ready.

## Source Resolution

A target project does not need to record the Resonance upstream URL. Most upgraded projects will only have `.agents/` and local memory. Resolve the source in this order:

1. **Explicit source from the user**: local path, Git URL, branch, tag, or commit.
2. **Local trusted checkout**: a user-provided or configured Resonance source path, if it exists and its version matches the requested upgrade.
3. **Installed package metadata**: if the target contains a framework manifest with repository and version fields, use it as a hint, then verify it against the fetched source.
4. **Official public source**: with no requested version, resolve `tag_name` from `gh api repos/manusco/resonance/releases/latest`. Validate a stable `vMAJOR.MINOR.PATCH` tag and fetch it with `git clone --depth 1 --branch <tag> https://github.com/manusco/resonance.git <temp-source>` outside the target project. Record its exact commit for approval. Do not use the application remote or silently fall back to `main` when release lookup fails. Explicit branch/commit requests retain their named source.
5. **Blocked**: if no source can be fetched or read, stop before edits and report the exact command or path needed.

Verification:

- The resolved source must contain `.agents/skills/`, `.forge/` when shipping source mode, `AGENTS.md`, `resonance.sh`, `resonance.ps1`, and `package.json`.
- The source version must match the requested version, unless the user explicitly asked for a branch or commit.
- The temp clone or staging directory must not be inside the target project.
- Never infer the source URL from the target application remote. The app's `origin` is the product repo, not the framework source.
## Ownership Boundary

### Managed by the framework

These may be upgraded when preflight says they are safe:

- `.agents/skills/`
- `.forge/`
- `.claude/skills/`
- `.cursor/skills/`
- `.opencode/commands/`
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
- private or company skills under `.agents/skills/` that are absent from the framework ownership manifest
- `.resonance/project-skills.lock.json`, the committed content lock for those project skills
- project-specific `AGENTS*.md`, `CLAUDE*.md`, or host settings unless the diff proves they are generated framework bridges with no local edits

Legacy exception: if `.resonance/learnings.jsonl` exists and the user approves the migration, append its lessons into `.resonance/02_memory.md` and remove the legacy file only after the append is verified.

## Algorithm

Copy this checklist and tick items as you go.

0. **Read the project**: Inspect `git status --short`, existing Resonance directories, and the target's `AGENTS.md` / `CLAUDE.md` shape. -> verify: local changes are grouped as framework-managed, project-owned, or unrelated.
1. **Resolve source**: Use the Source Resolution order. Fetch or verify the source outside the target project. -> verify: source path, version, and fetch method are named.
2. **Plan first**: Run the new checkout's `.forge/update.py --source <source> --target <target> --version <version>`. For a pre-manifest installation, first check out its installed release and pass that old checkout as `--source` to the new updater with `--adopt`; adoption accepts only byte-identical released files. Then use the new checkout as the source for the dry run. Print the plan, backup policy, validation commands, and rollback path. -> verify: adoption changes only the ownership manifest; the dry run changes nothing.
3. **Block unsafe states**: Stop if any touched path has an unresolved conflict, staged deletion, unknown ownership, or local customization that cannot be classified. Dirty application files outside the managed paths are context, not a blocker. -> verify: blocker names exact paths.
4. **Back up before edits**: Copy every touched existing path to `.resonance/backups/resonance-upgrade-<timestamp>/` or another user-approved backup outside replacement paths. -> verify: backup contains the old files.
5. **Stage the new framework aside**: Copy source framework files into a temporary staging directory inside `.resonance/tmp/` or system temp, never directly over live files. -> verify: staged `.agents/skills` and `.forge` counts match the source.
6. **Compare and classify**: Diff staged framework files against live managed paths. Preserve target-local files that are outside generated trees. For generated trees, replacement is allowed only after backup and staging validation. -> verify: no project-owned path appears in the write set.
7. **Apply transactionally**: Run the same updater command with `--apply`. It stages files outside the target, verifies ownership hashes, applies by path, writes the new manifest, and restores touched paths on failure. -> verify: each write target resolves inside the project root and the journal says `complete`.
8. **Migrate legacy memory only with proof**: If approved, append legacy lessons, verify they appear in `.resonance/02_memory.md`, then remove `learnings.jsonl`. -> verify: no lesson is lost.
9. **Regenerate if the target ships `.forge`**: Run the target's Forge build when `.forge/forge.py` exists. If the project intentionally has only compiled `.agents`, do not invent `.forge`; copy compiled skills only. -> verify: generated files are consistent with source mode.
10. **Validate**: Run the strongest available checks in the target: framework validation, command shim checks, `/system-health` or `resonance.ps1`, and any project-specific smoke check that does not require unrelated dirty files to be resolved. -> verify: failures are reported with exact commands and output.
11. **Verify project skills**: When `.resonance/project-skills.lock.json` exists, run `python3 .forge/project_skills.py --check`. Never regenerate the project-owned lock as an implicit part of a framework upgrade. -> verify: every committed private skill still matches its pre-upgrade content lock.
12. **Report**: Summarize changed paths, preserved project-owned paths, backup path, validation output, and rollback instructions.

## Recovery

- Source cannot be resolved or fetched -> stop before edits. Name the missing source path, network access, or clone command.
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

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory; when `.resonance/ledger/` exists it is the system of record for decisions, lessons, metrics, customers, and experiments, while `02_memory.md` keeps `[lib]` notes and pointers).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
