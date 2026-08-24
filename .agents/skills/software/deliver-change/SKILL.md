---
name: resonance-software-deliver-change
description: Compatibility entrypoint for end-to-end software delivery. Use when the user explicitly invokes the software delivery skill or an existing workflow targets its skill ID. Confirms software scope, separates unrelated work, then delegates once to resonance-ops-goal, which owns the goal contract, bounded execution, evidence, review, and ship proposal. Do not select this instead of /goal for a new outcome request.
archetype: orchestration
contract_version: 1
job_id: delivery.compatibility-intake
stage: FRAME
contributes_to:
  - delivery.goal
reviews:
finalizes:
  - goal-handoff
artifact_access:
  - software-request:read
  - goal-handoff:create,modify
dispatch_conditions:
  - the user explicitly invokes the software delivery compatibility entrypoint
  - an existing workflow targets resonance-software-deliver-change
compatibility: alias
owner: software.delivery
activation: manual
authority: consequential
triggers:
  - the user explicitly invokes the software delivery compatibility entrypoint
  - an existing workflow targets resonance-software-deliver-change
entrypoints:
  - skill:software-deliver-change
negative_triggers:
  - a new end-to-end outcome request without explicit compatibility invocation
  - ship without review consent
inputs:
  - user_request
outputs:
  - user_request
  - software_scope
  - goal_scope
side_effects:
  - may_coordinate_work
write_sets:
  - project:software-delivery-handoff
failure_policy: stop
invokes:
  - resonance-ops-goal
---

# resonance-software-deliver-change: preserve the software delivery entrypoint

> **Role:** compatibility intake for software delivery.
> **Input:** A desired software outcome, bug fix, feature, migration, or release goal.
> **Output:** A bounded software request handed to `/goal`, or a stopped intake with the scope conflict named.
> **Definition of Done:** Software scope is explicit, unrelated work is separated, and the unchanged request plus constraints are delegated exactly once to `resonance-ops-goal`. This skill does not start or reproduce a goal loop.

This skill preserves an existing software-facing entrypoint. It is not a second
goal loop. `resonance-ops-goal` owns the contract, approval gate, loop state,
planning, building, verification, evidence, audit, independent review, and ship
proposal. This skill performs software intake and delegates once. It never runs
the downstream delivery pipeline itself.

## Prerequisites

- [ ] The skill was invoked explicitly or an existing workflow targeted its skill ID.
- [ ] The request contains a software delivery outcome, not only a narrow one-step command.

## Compatibility flow

1. **Confirm the entrypoint.** If the user did not explicitly invoke this skill and no existing workflow targeted it, route a new end-to-end outcome directly to `/goal`. -> verify: this compatibility layer does not compete with Goal during ordinary routing.
2. **Bound software scope.** Preserve the user's request, directives, constraints, and provenance. Identify the software outcome. -> verify: no requirement is rewritten or invented.
3. **Separate unrelated work.** Split marketing, sales, finance, leadership, or other independent outcomes and route them to their owners. Do not absorb them into software delivery. -> verify: the Goal handoff contains one coherent software outcome.
4. **Delegate once.** Invoke `resonance-ops-goal` with the unchanged software request and its confirmed constraints. -> verify: exactly one Goal invocation occurs and no downstream delivery specialist is invoked directly by this skill.
5. **Return Goal's result.** Preserve Goal's evidence, stop condition, approvals, and ship proposal without adding a second completion claim. -> verify: no nested state, duplicate approval, duplicate audit, or duplicate ship proposal exists.

## Recovery

- Software outcome is unclear -> stop and ask the material scope question. Do not invent it.
- Request mixes independent domains -> split them before delegation.
- Goal cannot be invoked -> return `BLOCKED` with the missing route. Do not recreate its pipeline locally.
- Goal stops or remains incomplete -> preserve that status and evidence exactly.

## Out of Scope

- Marketing, sales, finance, or leadership operating cycles.
- Owning goal state, plans, builds, tests, audits, reviews, or releases.
- Autonomous merge, tag, release, deploy, or framework mutation.
- Dynamic scheduling or a general graph runtime.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory; when `.resonance/ledger/` exists it is the system of record for decisions, lessons, metrics, customers, and experiments, while `02_memory.md` keeps `[lib]` notes and pointers).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
