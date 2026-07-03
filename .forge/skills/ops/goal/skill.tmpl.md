---
name: resonance-ops-goal
description: The autonomous goal loop. Takes a goal and drives it to a verified finish by framing it, decomposing it into slices, then building and verifying each against grounded checks (real tests, validators, audit), bounded and never auto-shipping. Use when the user gives an outcome to reach rather than a single step, says take this to done, run with it, or make this happen end to end. Manual-only (drives builds, tests, and real side effects).
archetype: orchestration
---

# /resonance-ops-goal: carry a goal to a verified finish

> **Role:** the conductor. Turns an outcome into a bounded, grounded, autonomous loop over the existing skills.
> **Invoked as:** `/goal "<outcome>"` (to drive a goal to done).
> **Input:** A goal or outcome, not a single step.
> **Output:** The goal reached and verified by real checks, or a clear stop with the progress made and what blocked it.
> **Definition of Done:** The goal's checkable Definition of Done is met and proven by grounded verification (tests green, validators clean, audit APPROVE). Every slice's DoD is met. Nothing was shipped without explicit approval. Decisions and learnings were recorded.

You do not improvise your way to a goal and you do not grind forever. You frame it, break it into slices, and loop: build a slice, verify it against reality, decide, repeat, until the goal is proven done or the loop hits a real bound and stops. The line between this and a runaway agent is three things: the done-signal is always an executed check and never your own opinion, the loop is bounded by code, and one-way doors and the finish are gated by the human.

## Prerequisites (fail fast)

- [ ] The input is a goal (an outcome), not a single instruction. If it is one step, just do the step.
- [ ] Git status is clean or the user accepts working on top of current changes.
- [ ] A second-model command is configured if the final gate should be automatic (optional; degrades to manual).

## Algorithm

Copy this checklist and tick items as you go.

1. **Frame (one human gate, up front).** Run `/grill` on the goal to turn it into a plan with an explicit, checkable Definition of Done. Present the plan and the DoD. Get approval before any code. This single approval is what keeps the loop honest. → verify: the user approved a plan with a DoD that a machine can check.
2. **Start the bound.** `py .forge/skills/ops/goal/scripts/loop_state.py start "<goal>" --dod "<checkable DoD>"`. → verify: state initialized.
3. **Decompose.** `/plan` produces atomic slices, each with its own DoD. → verify: an ordered slice list exists.
4. **Loop over slices, autonomously and bounded.** For each slice:
   - **Recall** relevant memory and settled decisions (`py .forge/recall.py`, `py .forge/decisions.py list`) so you do not re-solve or re-litigate.
   - **Build** the slice (`/build`).
   - **Verify with grounded signals only** (`/test` live execution runs the real tests; run the validators; `/audit` the diff). The done-signal is executed, never "this should work". See done_conditions.
   - **Check the bound:** `loop_state.py check <slice> advanced|progress|failed`. Obey the directive: CONTINUE, or STOP_SLICE / STOP_STUCK / STOP_CAP (then re-plan the slice once, or stop and escalate). Never override a STOP.
   - **Record** any real decision (`py .forge/decisions.py add`).
   Run multiple slices without pausing. Pause only at the checkpoints below. → verify: each slice ends verified or the loop stopped on a bound.
5. **Final gate.** When the goal DoD verifies, run `/second-opinion` on the whole change. → verify: a second-model review was reconciled.
6. **Propose ship, never auto-ship.** Present the result and the evidence and ask for approval to `/ship`. Clear the loop (`loop_state.py done`). → verify: shipped only after explicit approval.

## Checkpoints (the more-autonomous cadence)

Proceed on your own within and across slices. Stop and check in only when it matters:
- **Always** before a one-way door: any deploy, destructive change, schema migration, or architectural decision. These need explicit human confirmation, no exceptions.
- **When the bound says stop** (STOP_SLICE / STOP_STUCK / STOP_CAP): stop, report progress and what blocked it, and hand back or re-plan.
- **At the finish:** present the verified result for the ship approval.
See checkpoint_protocol for how to present a checkpoint.

## Recovery

- Ambiguous or shifting goal → return to `/grill`; do not build against a guess.
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
