---
name: resonance-strategy-blueprint
description: Creates, revises, and checks a project-owned architecture blueprint that defines durable principles, system boundaries, ownership, safe evolution, and controlled exceptions. Use when establishing an architecture constitution, auditing a brownfield system against first principles, planning evolutionary migration, or checking a plan, change, PR, or release for architectural drift.
archetype: orchestration
contract_version: 1
job_id: architecture.blueprint
stage: APPROVE
contributes_to:
reviews:
  - delivery.plan
finalizes:
  - architecture-blueprint
  - architecture-conformance-report
artifact_access:
  - project-evidence:read
  - architecture-blueprint:create,modify,review,approve
  - architecture-decision:create,modify,review
  - architecture-exception:create,modify,review,approve
  - implementation-plan:read,review
  - implementation-artifact:read,review
  - architecture-conformance-report:create,modify,approve
dispatch_conditions:
  - a project needs a durable architecture constitution or an existing blueprint needs revision
  - a plan, change, PR, or release needs an architecture conformance decision
compatibility: active
owner: strategy.blueprint
activation: manual
authority: consequential
triggers:
  - create or revise an architecture blueprint
  - audit a brownfield system from first principles without requiring a rewrite
  - check a plan, change, PR, or release for architectural drift
entrypoints:
  - /blueprint
negative_triggers:
  - answer an isolated architecture question without creating or checking a durable blueprint
  - perform a general multi-domain code audit
  - implement, deploy, or merge changes
inputs:
  - user_request
  - project_evidence
  - blueprint_mode
  - system_context
  - implementation_artifact
outputs:
  - user_request
  - recommendation
  - evidence
  - system_context
  - implementation_artifact
  - architecture_blueprint
  - architecture_conformance_report
  - architecture_scope
  - architect_scope
  - product_scope
  - security_scope
  - observability_scope
  - qa_scope
  - plan_scope
  - review_scope
  - reviewer_scope
side_effects:
  - may_coordinate_work
  - may_write_architecture_artifacts
write_sets:
  - project:architecture-artifacts
failure_policy: stop
invokes:
  - resonance-strategy-architect
  - resonance-ops-product
  - resonance-ops-security
  - resonance-ops-observability
  - resonance-ops-qa
  - resonance-strategy-plan
  - resonance-ops-reviewer
---

# /resonance-strategy-blueprint: set direction and catch drift

> **Role:** architecture constitution owner and conformance gate.
> **Invoked as:** `/blueprint create`, `/blueprint revise`, or `/blueprint check`.
> **Input:** Project evidence plus either the intended system outcomes or an approved blueprint and a concrete artifact to check.
> **Output:** A project-owned architecture blueprint or an architecture conformance report with evidence, findings, exceptions, and a verdict.
> **Definition of Done:** Current reality, approved target, and next safe transition are distinct; every material rule and boundary has an owner; decisions and exceptions are traceable; the result cites evidence; a human approves a new baseline or principle change; and no application change, deployment, or merge is performed.

The blueprint governs architectural direction. It is not a description of every
file, a style guide, or a reason to rewrite working software. Read
[Blueprint Protocol](references/blueprint_protocol.md) for creation and revision.
Read [Conformance Protocol](references/conformance_protocol.md) for checks.

## Prerequisites

- [ ] Name the mode: `create`, `revise`, or `check`.
- [ ] Preserve the user's outcome, constraints, and exclusions.
- [ ] In `create` or `revise`, inspect repository and operational evidence. Do not derive intended architecture from code alone.
- [ ] In `check`, obtain the approved blueprint and the concrete plan, diff, PR, or release candidate. If either is missing, stop and name it.

## Pipeline

1. **Frame the contract.** State the system purpose, quality attributes, scope, evidence sources, assumptions, and unresolved decisions. Separate facts from proposals. -> gate: the audit scope and approval owner are explicit.
2. **Map reality.** Invoke `resonance-strategy-architect` to trace context, containers, trust zones, dependencies, data ownership, decisions, state transitions, side effects, and failure paths. Invoke product, security, observability, or QA only when their domain can change the result. -> gate: the observed current state cites evidence and does not claim intent.
3. **Choose the mode.** Run the matching path:
   - `create`: derive principles and a target from system purpose and required qualities, then define safe transition seams.
   - `revise`: classify the new evidence as clarification, exception, decision, or principle change. Preserve stable principles unless the evidence invalidates them.
   - `check`: trace the artifact against each applicable rule and contract. Do not rewrite the baseline to make the artifact pass.
4. **Control evolution.** Keep current state, target state, and transition state separate. For every gap, select keep, constrain, migrate, replace, or remove. Prefer the smallest reversible slice that reduces risk while preserving behavior. -> gate: no total rewrite is proposed without evidence that incremental paths cannot meet the required qualities.
5. **Record decisions and exceptions.** Write an architecture decision for a durable choice. Record a controlled exception for a temporary violation. Never hide debt in prose or label it temporary without an exit condition. -> gate: each exception has scope, rationale, owner, risk, compensating controls, review trigger, evidence, and removal condition.
6. **Verify.** Invoke `resonance-ops-qa` for testability and failure paths, `resonance-ops-security` for trust or authorization boundaries, and `resonance-ops-observability` for runtime proof when applicable. -> gate: every claimed invariant has a verification method or is labeled unverified.
7. **Decide.** For a blueprint, return `PROPOSED` until a human approves it, then `APPROVED`. For a check, return `CONFORMING`, `CONFORMING_WITH_EXCEPTIONS`, or `NON_CONFORMING`, with blocking findings first and the smallest safe next action. -> gate: accepted debt never appears as clean conformance.
8. **Route.** Send approved migration work to `resonance-strategy-plan` and concrete code review to `resonance-ops-reviewer`. Do not implement, deploy, merge, or change production state.

## Guardrails

- One authoritative owner for each business rule, canonical write, state transition, and side effect.
- Interfaces request named operations. They do not coordinate business transactions or write canonical state across an owning boundary.
- Provider acceptance, queueing, delivery, settlement, and business completion are separate facts unless the domain contract proves otherwise.
- Failure behavior, idempotency, retries, reconciliation, audit evidence, and recovery are part of the design.
- Dependencies cross boundaries only through explicit contracts.
- Architecture debt is visible, owned, bounded, and removable.
- The blueprint changes through evidence and explicit decisions, not implementation convenience.
- Project architecture belongs in project artifacts. Never copy it into this reusable skill.

## Recovery

- Evidence is incomplete -> publish an evidence-gap list and keep affected sections `UNVERIFIED`; do not invent the system.
- Current behavior conflicts with stated intent -> show both and ask the approval owner which is authoritative.
- A principle change is requested only to pass a check -> return `NON_CONFORMING` and route the proposed principle change as a separate decision.
- A legacy dependency must remain -> place it in the transition map and controlled exception register with compensating controls and a removal condition.
- The artifact is too broad to trace safely -> split the check by boundary or user-visible flow, then reconcile the verdicts.
- A specialist cannot run -> name the missing evidence and lower confidence. Do not fabricate its findings.

## Reference Library

- **[Blueprint Protocol](references/blueprint_protocol.md):** Artifact structure, first-principles derivation, brownfield mapping, evolution rules, and exception schema.
- **[Conformance Protocol](references/conformance_protocol.md):** Change tracing, finding severity, verdicts, and planning, review, and release gates.

{{RESOLVER:operating_standard}}

{{OVERLAY}}
