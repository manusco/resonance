---
name: resonance-ops-ship
description: The Logistics Officer. Safely transports code to the user using the ShipIt protocol. Use when preparing a release, tagging a version, generating a changelog, or deploying to production.
archetype: procedure
---

# /resonance-ops-ship: safe transport of code to user

> **Role:** the Logistics Officer.
> **Invoked as:** `/ship` (to deploy the project).
> **Input:** Merged `main` branch.
> **Output:** Deployed artifact + Tagged Release.
> **Definition of Done:** Artifact is verified before tagging. Semantic versioning is correctly applied. Changelog is updated. Commits are logical (not one massive WIP). Release is tagged and pushed. Docs are in sync (doc_drift.py clean: version, command map, and counts agree). Production is verified healthy after deploy (a post-deploy smoke test passes and the error rate is normal), and a rollback path was known before the deploy started.

Shipping is irreversible. You must verify the artifact *before* you tag it. You are the last line of defense.

## Prerequisites (fail fast)

- [ ] Branch is `main`.
- [ ] Local tree is clean.
- [ ] CI is Green.

## Algorithm (Execution)

Copy this checklist and tick items as you go.

1. **Pre-Flight Check**: Detect the project's toolchain first (see Toolchain Detection); do not assume npm.
   - **Safety**: Run the project's test command.
   - **Build**: Run the project's build command.
   - **Perf**: Check bundle sizes (ensure no massive chunks).
   - **SEO**: Delegate to `resonance-marketing-seo` to verify Meta Tags, Sitemap, and Robots.txt.
2. **Versioning**: Determine Semantic Version (Major = Breaking, Minor = Feat, Patch = Fix). Update `package.json`.
3. **Changelog & Docs Sync**: Use `git log --oneline [last_tag]..HEAD` and update `CHANGELOG.md` with human-readable notes. Then run `py .forge/doc_drift.py` to confirm the version, command map, and skill and command counts match across `README.md`, `AGENTS.md`, and the manifests. Fix any drift before committing.
4. **Logical Commits & Push**: Instead of one massive "WIP" commit, bisect the code into logical commits (`chore: setup`, `feat: models`, `feat: UI`, `docs: version bump`).
5. **Tag & Release**: `git tag vX.Y.Z`, then `git push origin main --tags`. Confirm the rollback path first (a previous release, a feature flag, or a canary you can abort) so you can undo before you deploy.
6. **Deploy, canary first where supported**: Roll out to a small slice before everyone. Watch the health window before promoting to full traffic. If there is no canary path, deploy and go straight to verification with a tighter watch.
7. **Verify the deploy (do not skip)**: After deploy, prove production is healthy. Run a post-deploy smoke test against prod: the health endpoint, one critical user path, the error rate, and the key metrics versus baseline. The deploy is done when production is confirmed healthy, not because the pipeline went green.
8. **Rollback on failure**: If verification fails, execute the rollback plan immediately (abort the canary or roll back to the previous release). Restore production first, then investigate. See Canary and Rollback.

## Recovery

- Build fail → abort immediately. Do not tag.
- Deploy or post-deploy verification fails → execute the rollback plan (abort the canary or roll back to the previous release) and restore production before anything else. Revert the tag (`git tag -d vX.Y.Z`) only after prod is healthy again.
- No rollback path exists → do not deploy. Establish one first: a previous release to fall back to, a feature flag, or a canary you can abort.

## Out of Scope

- Writing new features (delegate to `/build`).
- Root cause analysis of a failed build (delegate to `/debug`).

## Cognitive Frameworks

### The Checkpoint
Shipping is irreversible. The artifact must be verified before it receives a version tag.

### Logical Commits
Do not dump 50 files into a single commit. Organize them chronologically by layer: infrastructure first, then backend models, then UI, then documentation.

### Canary and Rollback
Deploy to a small slice first and watch it before full rollout, so a bad release hits a few users, not all of them. Always know how to undo before you deploy. Green CI means the code built; a verified deploy means production actually works. Only the second one is done.

## Reference Library

- **[Completion Attestation](../core/references/completion_attestation.md)**: Required sign-off format.
- **[Git Mastery](../core/references/git_mastery.md)**: Tagging, branching, and release protocols.
- **[Toolchain Detection](../core/references/toolchain_detection.md)**: Detect and run the project's commands, not npm by reflex.
- **[Canary and Rollback](references/canary_and_rollback.md)**: Progressive rollout, post-deploy verification, and rollback triggers.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory; when `.resonance/ledger/` exists it is the system of record for decisions, lessons, metrics, customers, and experiments, while `02_memory.md` keeps `[lib]` notes and pointers).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
