---
name: resonance-software-deliver-change
description: End-to-end software delivery conductor. Use when a user wants a code change taken from goal contract through plan, implementation, verification, audit, release proposal, and retained evidence without auto-shipping.
archetype: orchestration
owner: software.delivery
activation: manual
authority: consequential
triggers:
  - deliver a software change from request to reviewed release candidate
entrypoints:
  - skill:software-deliver-change
negative_triggers:
  - ship without review consent
inputs:
  - user_request
  - plan
  - implementation_plan
outputs:
  - user_request
  - artifact
  - evidence
  - decision
  - grill_scope
  - plan_scope
  - implementation_plan
  - test_scope
  - qa_scope
  - audit_scope
  - release_scope
  - ship_scope
  - review_scope
  - second_opinion_scope
side_effects:
  - may_coordinate_work
  - may_write_files
write_sets:
  - project:software-change
failure_policy: stop
invokes:
  - resonance-strategy-grill
  - resonance-strategy-plan
  - resonance-engineering-build
  - resonance-ops-qa
  - resonance-ops-audit
  - resonance-ops-second-opinion
  - resonance-ops-ship
---

# resonance-software-deliver-change: deliver a software change with evidence

> **Role:** software delivery conductor.
> **Input:** A desired software outcome, bug fix, feature, migration, or release goal.
> **Output:** A verified change, or a stopped run with evidence and next action.
> **Definition of Done:** The approved contract is satisfied. Tests and validators prove the change. The diff passes audit and second opinion where required. Release is proposed, not auto-shipped.

This is not a second goal loop and it does not call `/goal` as a subroutine. It
uses the goal contract and evidence rules as its outer boundary, then routes the
software work through plan, build, QA, audit, and ship proposal.

## Prerequisites

- [ ] The request is a software delivery outcome, not a narrow one-step command.
- [ ] Repository status is known.
- [ ] The user has approved any one-way door before it happens.

## Pipeline

1. **Contract:** draft the goal contract in the `/goal` format without starting a nested goal loop. Preserve user directives, inferred tactics, non-goals, risks, and acceptance checks. → gate: checkable acceptance criteria exist.
2. **Grill:** invoke `resonance-strategy-grill` on the contract and high-risk assumptions. → gate: unresolved human-owned decisions are answered or explicitly deferred.
3. **Plan:** invoke `resonance-strategy-plan` to create atomic slices. → gate: each slice has a verifiable DoD and no slice crosses unrelated ownership boundaries.
4. **Approve:** present contract plus plan before file edits. → gate: human approval exists for the plan and any consequential actions.
5. **Build:** invoke `resonance-engineering-build` slice by slice. → gate: new or changed checks fail before the fix where practical, then pass after.
6. **Verify:** invoke `resonance-ops-qa` and run project validators. Attach evidence receipts to the active goal state for each acceptance criterion. → gate: stale hashes are rejected and every criterion has accepted evidence.
7. **Audit:** invoke `resonance-ops-audit` and reconcile P0/P1 findings before completion. → gate: no blocking findings remain.
8. **Independent review:** invoke `resonance-ops-second-opinion` for high-risk contracts and material diffs. → gate: feedback is reconciled or explicitly rejected with reason.
9. **Release proposal:** invoke `resonance-ops-ship` only as a proposal unless the user explicitly approves shipping. → gate: no autonomous commit, merge, tag, deploy, or release.

## Recovery

- Contract is vague → return to Grill. Do not build against a guess.
- Plan cannot produce verifiable slices → return to Plan. Do not use a broad slice.
- Evidence is stale or missing → re-run the real check and attach a current receipt.
- Audit finds a blocker → fix the blocker before release proposal.
- User withholds shipping approval → stop after verified implementation and PR or commit proposal.

## Out of Scope

- Marketing, sales, finance, or leadership operating cycles.
- Autonomous merge, tag, release, deploy, or framework mutation.
- Dynamic scheduling or a general graph runtime.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory; when `.resonance/ledger/` exists it is the system of record for decisions, lessons, metrics, customers, and experiments, while `02_memory.md` keeps `[lib]` notes and pointers).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
