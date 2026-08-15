---
name: resonance-sales-run-revenue-motion
description: Sales revenue-motion conductor. Use when a user wants prospecting, account intelligence, outbound sequence, call preparation, CRM hygiene, pipeline review, forecast, and customer-success handoff governed as one revenue motion.
archetype: orchestration
owner: sales.revenue-motion
activation: manual
authority: consequential
triggers:
  - run or prepare a governed sales motion
entrypoints:
  - skill:sales-run-revenue-motion
negative_triggers:
  - send outreach or mutate CRM without approval
inputs:
  - user_request
  - plan
  - revenue_motion_scope
outputs:
  - user_request
  - plan
  - artifact
  - evidence
  - decision
  - account_scope
  - account_intelligence_scope
  - lead_ops_scope
  - outbound_scope
  - outbound_sequence_scope
  - call_scope
  - call_intelligence_scope
  - pipeline_scope
  - revops_scope
  - customer_success_scope
  - legal_scope
side_effects:
  - may_coordinate_work
  - may_write_files
write_sets:
  - project:revenue-motion
failure_policy: stop
invokes:
  - resonance-sales-account-intelligence
  - resonance-sales-lead-ops
  - resonance-sales-outbound-sequence
  - resonance-sales-call-intelligence
  - resonance-sales-pipeline
  - resonance-sales-revops
  - resonance-success-customer-success
  - resonance-ops-legal
---

# resonance-sales-run-revenue-motion: govern the path from target account to handoff

> **Role:** revenue-motion conductor.
> **Input:** target accounts, ICP, territory, quota goal, campaign request, or pipeline problem.
> **Output:** account plan, outreach sequence, call plan, CRM mutation proposal, forecast, and handoff notes.
> **Definition of Done:** The motion names the buyer, jurisdiction, contact basis, buyer action, CRM source of truth, forecast method, next step, and handoff owner. No outreach or CRM mutation occurs without approval.

## Pipeline

1. **Scope:** define ICP, segment, territory, jurisdiction, CRM source, goal, and send authority. -> gate: no unknown recipient basis.
2. **Account intelligence:** invoke `resonance-sales-account-intelligence` and `resonance-sales-lead-ops`. -> gate: target list has provenance and confidence.
3. **Compliance:** invoke `resonance-ops-legal` when outreach rules, privacy, recording, or regulated claims are relevant. -> gate: no risky send path is treated as safe by default.
4. **Sequence and call:** invoke outbound-sequence and call-intelligence for message and conversation assets. -> gate: claims, objections, and buyer action are explicit.
5. **Pipeline and RevOps:** invoke pipeline and revops for stages, hygiene, forecast, and owner actions. -> gate: forecast uses observed conversion or is labeled unweighted or assumption-based.
6. **Handoff:** invoke customer-success when the motion touches expansion, renewal, onboarding, or post-sale risk.
7. **Approval:** present exact sends, CRM mutations, and follow-up actions for human consent.

## Recovery

- Contact provenance is missing -> stop or downgrade to research-only.
- CRM mutation is ambiguous -> draft the change, do not execute it.
- Forecast probabilities are unobserved -> label them assumptions or use an unweighted view.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory; when `.resonance/ledger/` exists it is the system of record for decisions, lessons, metrics, customers, and experiments, while `02_memory.md` keeps `[lib]` notes and pointers).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
