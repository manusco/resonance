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

- [ ] Source version is resolved with the Source Resolution order below.
- [ ] Target project root is confirmed.
- [ ] Git status has been classified by path.
- [ ] No unresolved conflicts exist in any path the upgrade would touch.
- [ ] A backup location outside the managed replacement paths is ready.
- [ ] The installation profile is known: `source` or `compiled`. A legacy target with generated skills but no profile is blocked until the owner chooses.

## Source Resolution

A target project does not need to record the Resonance upstream URL. Most upgraded projects will only have `.agents/` and local memory. Resolve the source in this order:

1. **Explicit source from the user**: local path, Git URL, branch, tag, or commit.
2. **Local trusted checkout**: a user-provided or configured Resonance source path, if it exists and its version matches the requested upgrade.
3. **Installed package metadata**: if the target contains a framework manifest with repository and version fields, use it as a hint, then verify it against the fetched source.
4. **Official public source**: fetch `https://github.com/manusco/resonance.git` with `gh repo clone manusco/resonance` or `git clone https://github.com/manusco/resonance.git` into a temp directory outside the target project.
5. **Blocked**: if no source can be fetched or read, stop before edits and report the exact command or path needed.

Verification:

- The resolved source must contain `.agents/skills/`, `.forge/` for source-mode validation, `resonance.sh`, `resonance.ps1`, and `package.json`.
- The source version must match the requested version, unless the user explicitly asked for a branch or commit.
- The temp clone or staging directory must not be inside the target project.
- Never infer the source URL from the target application remote. The app's `origin` is the product repo, not the framework source.
## Ownership Boundary

### Managed by the framework

These may be upgraded when preflight says they are safe:

- `.agents/skills/`
- `.forge/` in source mode only
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

Project-owned documentation is never runtime authority for framework validation. Forge derives command targets and runtime skill metadata from framework-owned skill templates. Project docs such as a root `README.md` may be absent, and generated files such as `docs/skill-manifest.json` may be stale or absent, without blocking an upgrade. Validation skips missing project-doc targets and never creates them.

Legacy exception: if `.resonance/learnings.jsonl` exists and the user approves the migration, append its lessons into `.resonance/02_memory.md` and remove the legacy file only after the append is verified.

### Optional update notice

The release notice is explicit opt-in with `python3 resonance_update.py notice enable`. Its setting lives in the operating system's user configuration directory, outside project repositories. It checks stable releases with tight timeout and size bounds, stores no project path, project data, credentials, or release prose, and failure never blocks a launcher. A notice only reports availability. It never applies an update. Apply remains a separate reviewed transaction bound to the exact version, full source commit, installation profile, and plan digest.

## Algorithm

Copy this checklist and tick items as you go.

0. **Read the project**: Inspect `git status --short`, existing Resonance directories, and the target's `AGENTS.md` / `CLAUDE.md` shape. -> verify: local changes are grouped as framework-managed, project-owned, or unrelated.
1. **Resolve source**: Use the Source Resolution order. Fetch or verify the source outside the target project. -> verify: source path, version, and fetch method are named.
2. **Choose the profile and plan first**: Run the pinned checkout's `resonance_update.py --source <source> --target <target> --profile <source|compiled> --version <version>`. For a pre-manifest installation, first check out its installed release and pass that old checkout as `--source` with `--adopt` and an explicit profile; adoption accepts only byte-identical released files. Then use the new checkout as the source for the dry run. Print the profile, full source revision, plan digest, backup policy, validation commands, and rollback path. -> verify: adoption changes only the ownership manifest; the dry run changes nothing.
3. **Block unsafe states**: Stop if any touched path has an unresolved conflict, staged deletion, unknown ownership, or local customization that cannot be classified. Probe reversible file creation and deletion in each existing managed destination directory before creating a backup. Dirty application files outside the managed paths are context, not a blocker. -> verify: blocker names exact paths and denied destination directories stop before backup.
4. **Back up before edits**: Copy every touched existing path to `.resonance/backups/resonance-upgrade-<timestamp>/` or another user-approved backup outside replacement paths. -> verify: backup contains the old files.
5. **Stage the new framework aside**: Copy source framework files into a temporary staging directory inside `.resonance/tmp/` or system temp, never directly over live files. -> verify: staged paths match the selected profile; compiled staging contains no `.forge`.
6. **Compare and classify**: Diff staged framework files against live managed paths. Preserve target-local files that are outside generated trees. For generated trees, replacement is allowed only after backup and staging validation. -> verify: no project-owned path appears in the write set.
7. **Apply transactionally**: Run the same profile-aware updater command with `--apply --revision <reviewed-full-commit> --plan-digest <reviewed-plan-digest>`. It refuses a changed source or plan, stages files outside the target, verifies ownership hashes, applies by path, writes the profile to the manifest, and restores touched paths on failure. -> verify: each write target resolves inside the project root and the journal says `complete`.
8. **Migrate legacy memory only with proof**: If approved, append legacy lessons, verify they appear in `.resonance/02_memory.md`, then remove `learnings.jsonl`. -> verify: no lesson is lost.
9. **Validate by profile**: Run the target's Forge build only in source mode. In compiled mode, run the pinned source validators against the target's generated skills and never invent `.forge`. -> verify: source dry run, skill validation, adapter checks, and integrity checks pass.
10. **Validate**: Run the strongest available checks in the target: framework validation, command shim checks, `/system-health` or `resonance.ps1`, and any project-specific smoke check that does not require unrelated dirty files to be resolved. -> verify: failures are reported with exact commands and output.
11. **Verify project skills**: When `.resonance/project-skills.lock.json` exists, use the verifier that belongs to the active installation profile. For a source installation, run `python3 <target>/.forge/project_skills.py --check --root <target>`. For a compiled installation, run `python3 <pinned-source>/.forge/project_skills.py --check --root <target>`. Never regenerate the project-owned lock as an implicit part of a framework upgrade. -> verify: every committed private skill still matches its pre-upgrade content lock.
12. **Report**: Summarize changed paths, preserved project-owned paths, backup path, validation output, and rollback instructions.

## Recovery

- Source cannot be resolved or fetched -> stop before edits. Name the missing source path, network access, or clone command.
- Preflight finds unresolved conflicts in touched paths -> stop. Do not edit.
- Preflight finds unrelated dirty application files -> proceed only if the write set excludes them and report that they were left alone.
- Backup fails -> stop before edits.
- Staging validation fails -> remove staging directory and stop.
- Apply fails midway -> restore touched paths from backup, then rerun validation. If rollback also fails, preserve both errors and the exact recovery journal path.
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
