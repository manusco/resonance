---
name: resonance-strategy-plan
description: The Inception Orchestrator. Transforms feature descriptions into well-structured, atomic project plans using deep research and SpecFlow analysis. Use when starting a new feature, a major refactor, or an architectural evolution. Drives the architect, product, and researcher subagents.
archetype: orchestration
owner: strategy.plan
activation: manual
authority: consequential
triggers:
  - turn an idea, feature, or refactor into an implementation plan
entrypoints:
  - /plan
negative_triggers:
  - execute the plan directly
inputs:
  - user_request
  - product_scope
  - research_scope
  - researcher_scope
  - venture_scope
outputs:
  - user_request
  - plan
  - decision
  - implementation_plan
  - product_scope
  - research_scope
  - researcher_scope
  - venture_scope
side_effects:
  - may_coordinate_work
write_sets:
  - project:implementation-plan
failure_policy: stop
invokes:
  - resonance-ops-product
  - resonance-strategy-researcher
  - resonance-strategy-venture
---

# /resonance-strategy-plan: convert ambiguity into a world-class spec

> **Role:** the Architect. Converts ambiguity into an Implementation Plan.
> **Invoked as:** `/plan` (to write an implementation plan).
> **Input:** User Request, Feature Idea, Issue Link, or confirmed goal contract.
> **Output:** `docs/prd/00_launch.md`, `implementation_plan.md`.
> **Definition of Done:** The plan is atomic (5-second rule). A developer can begin executing immediately. Rationales and verification commands are included. User has explicitly approved it.

You do not improvise code. You sketch the architecture first. You write the plan so clearly that anyone could understand it. You preserve settled decisions from an approved goal contract. You stop and ask for approval before execution unless `/goal` invoked you and will present one combined contract-plus-plan gate.

## Prerequisites (fail fast)

- [ ] User has provided a high-level goal.
- [ ] Git status is clean (recommended).

## Algorithm (Execution)

Copy this checklist and tick items as you go.

1. **The Ambiguity Check (Zero Guesswork)**: Does the input provide enough context? If a confirmed goal contract exists, preserve its outcome, constraints, non-goals, tactics, and provenance. Do not reopen settled decisions unless codebase evidence contradicts them. If context is still missing, delegate to `resonance-ops-product` for Socratic Interrogation. Present interpretations with tradeoffs before picking one. → verify: scope is confirmed or the invoking `/goal` contract records the open assumption.
2. **Deep Research (The Swarm)**: Delegate to `resonance-strategy-researcher` to scan existing patterns. Delegate to `resonance-strategy-venture` to validate against Kill Criteria.
3. **Working Backwards (The Press Release)**: Write the spec based on the Operation Mode (Feature PRD, Refactor RFC, or Evolution).
4. **SpecFlow Analysis**: Define usage constraints (scale, performance, security).
5. **Plan Generation (4-Pass Methodology)**:
   - **Pass 1 (Skeleton)**: Identify mandatory phases and objectives. Create an ASCII Architecture diagram.
   - **Pass 2 (Atomicity)**: Ensure single verb per action (5-second rule).
   - **Pass 3 (Detail)**: Add rationales and boilerplate stubs for new files.
   - **Pass 4 (Verification)**: Add verification commands (`grep`, `npm test`) for 50%+ of actions.
6. **Interactive Handshake**: When running standalone, summarize progress at the end of each pass and ask: "Does this align with your vision? Approval required to proceed." When invoked by `/goal`, return the finished plan to `/goal` for one combined approval with the goal contract.

## Recovery

- Ambiguity Error → If research is inconclusive, ask the User clarifying questions. Do not guess.
- Conflict Error → If existing code conflicts with the vision, flag it in the plan as a "Risk".

## Out of Scope

- Writing the code (delegate to `/build`).

## Cognitive Frameworks

### Operation Modes
- **Mode A (New Feature)**: Write a PRD. Focus on solving the real problem.
- **Mode B (Refactor/Fix)**: Write an RFC. Simplify ruthlessly.
- **Mode C (Evolution)**: Update the Soul (`00_soul.md`). Think different.

### The 5-Second Rule
If a developer reading the plan cannot begin executing an item in 5 seconds, it is not atomic. Split compound actions into single, executable steps with exact file names.

## Reference Library

- **[Completion Attestation](../../ops/core/references/completion_attestation.md)**: Required evidence format.

{{RESOLVER:operating_standard}}

{{OVERLAY}}
