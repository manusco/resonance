---
name: resonance-strategy-plan
description: Implementation-plan author. Turns a confirmed feature, refactor, or architecture goal into an atomic, dependency-aware, verifiable plan using earned research, product, and architecture input. Use when the intended outcome is clear but the implementation sequence is not. It produces the approved plan artifact but does not build it. Brief clarifies an unclear ask, Grill interrogates a proposed plan, and Goal drives an accepted outcome through execution.
archetype: orchestration
contract_version: 1
job_id: delivery.plan
stage: PLAN
contributes_to:
  - delivery.goal
reviews:
finalizes:
  - implementation-plan
artifact_access:
  - user-request:read
  - research-evidence:read
  - implementation-plan:create,modify,approve
  - project-design-contract:read
dispatch_conditions:
  - a clear intended outcome needs an atomic implementation plan
compatibility: active
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
  - design_scope
  - plan
  - decision
  - implementation_plan
  - product_scope
  - research_scope
  - researcher_scope
  - venture_scope
  - architect_scope
  - blueprint_scope
side_effects:
  - may_coordinate_work
write_sets:
  - project:implementation-plan
failure_policy: stop
invokes:
  - resonance-ops-product
  - resonance-strategy-researcher
  - resonance-strategy-venture
  - resonance-strategy-architect
  - resonance-strategy-blueprint
  - resonance-design-designer
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
2. **Blueprint Applicability**: Read `.resonance/04_systems.md` when it contains an approved blueprint. If the work changes a governed boundary, ownership rule, dependency direction, trust zone, data contract, runtime topology, or named exception, record the affected `SYS-*` rules in `blueprint_scope` and route the proposal through `/blueprint check` before approval. If no approved baseline exists, record that fact without inventing one. Purely local work may record `blueprint_scope: not_applicable` with one sentence of evidence. → verify: the plan either cites affected rules, records a justified skip, or names the missing baseline.
3. **Research**: Use existing codebase evidence first. Delegate to `resonance-strategy-researcher` when unresolved external or technical evidence could change the choice; use venture validation only when a business-model assumption is in scope. Do not add research handoffs for settled, local choices.
4. **Working Backwards**: State the user outcome and relevant context; use a Feature PRD, Refactor RFC, or Evolution artifact when it helps define or assess the work.
5. **Design Contract Applicability**: For changes to user-visible behavior, names, status, or interaction, consult [Project Design Contract](../../design/designer/references/project_design_contract.md) and plan against applicable approved defaults and explicit variants. During normal UI planning, if the app has no filled entry point after source lookup, or the work adds a shared pattern with no applicable approved rule, activate Designer to discover and create or resume a bounded PROPOSED baseline or addendum from the brief and available evidence before planning. A broken declaration or pointer, or an unresolved source conflict, stays unresolved; do not create a replacement or competing contract. Preserve pointers and approved content; keep unknowns explicit. Routine reuse needs no new handoff or approval. A small repair may follow observed conventions without inventing policy. Skip work with no visible effect. → verify: the plan records its applicable source/rules, any needed proposed baseline/addendum, or a concise reason this does not apply.
6. **Constraints**: Define scale, performance, security, or other usage constraints that affect this outcome.
7. **Plan Generation**: Include the phases, architecture artifacts, rationales, and verification commands needed to implement and assess the full outcome. Keep actions independently executable; split them when doing so clarifies ownership or dependencies. Add diagrams and file stubs only when they help execute the work. Verify each material behavior at its owner, not by an arbitrary percentage of actions.
8. **Approval**: When running standalone, present the completed plan for the required user approval before execution. When invoked by `/goal`, return the plan for the one combined goal-contract approval.

### Proportionality gate

Use the [Necessity Protocol](../../ops/core/references/necessity_protocol.md) when choosing plan stages, research, artifacts, and handoffs. Keep a step when it changes a decision, reduces a material risk, or supplies needed verification. Match research depth and artifacts to the unresolved choice. Preserve the complete approved outcome and required approval gates; do not add a second approval ritual or silently cut scope.

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

### Action clarity
Give each action a clear owner, verb, object, and verification. Split compound work when separate ownership or dependencies make the steps safer or easier to execute; do not split work to satisfy a timing or step-count quota.

## Reference Library

- **[Completion Attestation](../../ops/core/references/completion_attestation.md)**: Required evidence format.

{{RESOLVER:operating_standard}}

{{OVERLAY}}
