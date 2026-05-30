---
name: resonance-ops-update-roadmap
description: The Synchronizer. Realigns the project map (state.md) with the territory (git history). Use when the roadmap is out of sync, after a long session of unlogged work, or when onboarding onto a stale project.
archetype: procedure
---

# /resonance-ops-update-roadmap: map must match territory

> **Role:** the Synchronizer and GPS.
> **Invoked as:** `/update-roadmap` (to sync state.md with git log).
> **Input:** `git log` and `.resonance/01_state.md`.
> **Output:** Updated `.resonance/01_state.md`.
> **Definition of Done:** `01_state.md` accurately reflects the last 10 git commits. Completed tasks are marked done. The immediate next step is recalculated.

The Plan says we are at Step 1. The Code says we are at Step 5. Drift is failure. You must make the Map match the Territory.

## Prerequisites (fail fast)

- [ ] `.resonance/01_state.md` exists.
- [ ] Git history exists.

## Algorithm (Execution)

Copy this checklist and tick items as you go.

1. **Read Territory**: Run `git log -n 10 --oneline` to identify what *actually* happened.
2. **Read Map**: Read `.resonance/01_state.md` to identify what we *thought* happened.
3. **Reconcile**:
   - Mark Done: If Git says the feature is merged, mark it `[x]` in the state.
   - Context Update: Add any new constraints found in the commit messages.
   - Next Step: Re-calculate the immediate next step.
4. **Governance**: Save the updated `01_state.md`.

## Recovery

- Conflict → If Map and Territory diverge wildly, favor the Territory (Git). Update the Map to reflect Reality. Never revert code just to match an old plan.

## Out of Scope

- Planning new features (delegate to `/plan`).

## Cognitive Frameworks

### The Reality Check
Most plans fail because the map becomes outdated. Code is the only objective truth. When in doubt, read the code.

## Reference Library

- **[Karpathy Rules](../core/references/karpathy_rules.md)**: Universal coding standards (Simplicity, Surgical).

{{RESOLVER:decision_brief}}

{{RESOLVER:completion}}

{{RESOLVER:voice}}

{{OVERLAY}}
