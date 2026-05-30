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
> **Definition of Done:** Artifact is verified before tagging. Semantic versioning is correctly applied. Changelog is updated. Commits are logical (not one massive WIP). Release is tagged and pushed.

Shipping is irreversible. You must verify the artifact *before* you tag it. You are the last line of defense.

## Prerequisites (fail fast)

- [ ] Branch is `main`.
- [ ] Local tree is clean.
- [ ] CI is Green.

## Algorithm (Execution)

Copy this checklist and tick items as you go.

1. **Pre-Flight Check**: 
   - **Safety**: Run `npm test`.
   - **Build**: Run `npm run build`.
   - **Perf**: Check bundle sizes (ensure no massive chunks).
   - **SEO**: Delegate to `resonance-marketing-seo` to verify Meta Tags, Sitemap, and Robots.txt.
2. **Versioning**: Determine Semantic Version (Major = Breaking, Minor = Feat, Patch = Fix). Update `package.json`.
3. **Changelog**: Use `git log --oneline [last_tag]..HEAD` and update `CHANGELOG.md` with human-readable notes.
4. **Logical Commits & Push**: Instead of one massive "WIP" commit, bisect the code into logical commits (`chore: setup`, `feat: models`, `feat: UI`, `docs: version bump`).
5. **Tag & Release**: `git tag vX.Y.Z`, then `git push origin main --tags`. Trigger Deploy.

## Recovery

- Build Fail → Abort immediately. Do not tag.
- Deploy Fail → Revert tag: `git tag -d vX.Y.Z`.

## Out of Scope

- Writing new features (delegate to `/build`).
- Root cause analysis of a failed build (delegate to `/debug`).

## Cognitive Frameworks

### The Checkpoint
Shipping is irreversible. The artifact must be verified before it receives a version tag.

### Logical Commits
Do not dump 50 files into a single commit. Organize them chronologically by layer: infrastructure first, then backend models, then UI, then documentation.

## Reference Library

- **[Completion Attestation](../core/references/completion_attestation.md)**: Required sign-off format.
- **[Git Mastery](../core/references/git_mastery.md)**: Tagging, branching, and release protocols.

{{RESOLVER:decision_brief}}

{{RESOLVER:completion}}

{{RESOLVER:voice}}

{{OVERLAY}}
