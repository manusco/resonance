---
name: resonance-ops-goal
description: The autonomous goal loop. Takes a goal and drives it to a verified finish by first confirming a goal contract, then decomposing it into slices, building, and verifying against grounded checks (real tests, validators, audit), bounded and never auto-shipping. Use when the user gives an outcome to reach rather than a single step, mixes goals with requested tactics, says take this to done, run with it, or make this happen end to end. Manual-only (drives builds, tests, and real side effects).
archetype: orchestration
invokes:
  - resonance-strategy-grill
  - resonance-strategy-plan
  - resonance-engineering-build
  - resonance-ops-qa
  - resonance-ops-audit
  - resonance-ops-second-opinion
  - resonance-ops-ship
---

# /resonance-ops-goal: carry a goal to a verified finish

> **Role:** the conductor. Turns an outcome into a bounded, grounded, autonomous loop over the existing skills.
> **Invoked as:** `/goal "<outcome>"` (to drive a goal to done).
> **Input:** A goal or outcome, not a single step.
> **Output:** The goal reached and verified by real checks, or a clear stop with the progress made and what blocked it.
> **Definition of Done:** The approved goal contract is satisfied. The goal's checkable acceptance checks are met and proven by grounded verification (tests green, validators clean, audit APPROVE). Every slice's DoD is met. Nothing was shipped without explicit approval. Decisions and learnings were recorded.

You do not execute the surface wording of a messy request. Users often mix the outcome, a guessed tactic, constraints, and fears in one sentence. First write the goal contract. It separates what must be true from what was merely proposed. Then break the contract into slices and loop: build a slice, verify it against reality, decide, repeat, until the goal is proven done or the loop hits a real bound and stops. The line between this and a runaway agent is three things: the done-signal is always an executed check and never your own opinion, the loop is bounded by code, and one-way doors and the finish are gated by the human.

{{RESOLVER:independent_review_policy}}

## Prerequisites (fail fast)

- [ ] The input is a goal (an outcome), not a single instruction. If it is one step, just do the step.
- [ ] Git status is clean or the user accepts working on top of current changes.
- [ ] A second-model command is configured if the final gate should be automatic (optional; otherwise the gate produces a manual prompt and stays incomplete until answered).

## Algorithm

Copy this checklist and tick items as you go.

1. **Draft the goal contract.** Separate the request into: outcome; user directives and requested tactics, with provenance (`settled`, `directive`, or `inferred`); hard constraints; unresolved assumptions or contradictions; non-goals; material risks; acceptance checks; and any deferred metric with a due date. Do not fill empty boxes with invented certainty. Do not generate a downstream execution prompt. → verify: contract fields with content are explicit and requested tactics are not treated as approved implementation.
2. **Resolve only user-owned unknowns.** Run `/grill` on the contract. Grill resolves decisions the repo cannot answer and runs a targeted risk pass only when the triggers are present. → verify: the contract is updated with resolved decisions and remaining risks.
3. **Decompose without reopening settled decisions.** `/plan` consumes the confirmed contract and produces atomic slices, each with its own DoD. When `/plan` is invoked by `/goal`, suppress pass-by-pass approval and return the plan for one combined gate. → verify: an ordered slice list exists and preserves contract provenance.
4. **Approve once before code.** Present the goal contract plus the plan and acceptance checks. Get approval before any code. This single approval is what keeps the loop honest. → verify: the user approved a contract and plan with checks that a machine can run.
5. **Start the bound.** `py .forge/skills/ops/goal/scripts/loop_state.py start "<goal>" --dod "<checkable DoD>" --contract goal_contract.json --plan-hash "<hash>"`. → verify: state initialized with the approved contract and plan hash. Missing plan hash blocks the loop.
6. **Loop over slices, autonomously and bounded.** For each slice:
   - **Recall** relevant memory and settled decisions (the loaded `02_memory.md` index carries both; `py .forge/recall.py "<topic>"` for deeper slices) so you do not re-solve or re-litigate.
   - **Build** the slice (`/build`).
   - **Verify with grounded signals only**: `/test` runs the real tests (`.forge/exec/run_checks.py`) and a real browser (`.forge/exec/browser_check.mjs`); run the validators; `/audit` the diff. The done-signal is executed, never "this should work". See done_conditions.
   - **Check the bound:** `loop_state.py check <slice> advanced|progress|failed`. Obey the directive: CONTINUE, or STOP_SLICE / STOP_STUCK / STOP_CAP (then re-plan the slice once, or stop and escalate). Never override a STOP.
   - **Attach evidence:** when a criterion is proven, write an `EvidenceReceipt` and run `loop_state.py evidence <receipt>`. Stale contract or plan hashes are rejected. Overrides require an approval receipt.
   - **Record** any real decision as a one-line entry under `## Decisions` in `.resonance/02_memory.md`.
   Run multiple slices without pausing. Pause only at the checkpoints below. → verify: each slice ends verified or the loop stopped on a bound.
7. **Final gate.** When the goal DoD verifies, run `/second-opinion --mode diff` on the whole change. For a high-risk approved contract or plan, run `/second-opinion --mode decision` once on that artifact before the loop starts. → verify: independent review was run and reconciled, or the manual prompt was answered and reconciled.
8. **Propose ship, never auto-ship.** Run `loop_state.py achieve`; it fails unless every acceptance criterion has accepted evidence. Present the result and evidence and ask for approval to `/ship`. Clear the loop (`loop_state.py done`) only after achievement. → verify: shipped only after explicit approval and completed history is retained.

## Checkpoints (the more-autonomous cadence)

Proceed on your own within and across slices. Stop and check in only when it matters:
- **Always** before a one-way door: any deploy, destructive change, schema migration, or architectural decision. These need explicit human confirmation, no exceptions.
- **When the bound says stop** (STOP_SLICE / STOP_STUCK / STOP_CAP): stop, report progress and what blocked it, and hand back or re-plan.
- **At the finish:** present the verified result for the ship approval.
See checkpoint_protocol for how to present a checkpoint.

## Recovery

- Ambiguous or shifting goal → return to `/grill`; do not build against a guess.
- Requested tactic conflicts with the outcome or codebase evidence → keep the outcome, mark the tactic as proposed, and ask for approval before treating it as a constraint.
- A slice fails its bound → re-plan that one slice once (`/plan` on the slice). If it fails again, stop and escalate with the real output.
- A verification cannot be run (no test, no way to execute) → that is a gap, not a pass. Build the check first (a test, a script), or stop and say the DoD is unverifiable as written.
- Regression (a slice broke a prior green check) → revert the slice, re-scope, do not stack fixes on a broken base.

## Out of Scope

- Doing the domain work directly. This skill orchestrates `/grill`, `/plan`, `/build`, `/test`, `/audit`, `/second-opinion`, and `/ship`; it does not replace them.
- Shipping. `/ship` stays a separate, human-approved step.

## The guardrails (non-negotiable)

- **Grounded only.** The done-condition is an executed check (tests green, validator clean, audit APPROVE, page renders), never the model's own claim. This is the one rule that separates this from a runaway loop.
- **Bounded by code.** `loop_state.py` enforces the caps. A STOP is a stop.
- **Human owns one-way doors and the finish.** User Sovereignty holds: recommend and drive, but do not walk through a one-way door or ship without approval.

## Reference Library

- **[Loop Protocol](references/loop_protocol.md)**: The bounded reason-act-observe cycle and re-planning.
- **[Done Conditions](references/done_conditions.md)**: What counts as grounded verification, and what does not.
- **[Checkpoint Protocol](references/checkpoint_protocol.md)**: When to pause and how to present a checkpoint.

{{RESOLVER:operating_standard}}

{{OVERLAY}}
