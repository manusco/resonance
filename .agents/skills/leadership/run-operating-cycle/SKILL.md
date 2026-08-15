---
name: resonance-leadership-run-operating-cycle
description: Leadership operating-cycle conductor. Use when a founder, manager, or executive needs goals, decisions, delegation, hiring, feedback, conflict, cadence, or operating review turned into a clear management cycle.
archetype: orchestration
owner: leadership.operating-cycle
activation: manual
authority: consequential
triggers:
  - run a leadership or management operating cycle
entrypoints:
  - skill:leadership-run-operating-cycle
negative_triggers:
  - make people decisions without context or consent
inputs:
  - user_request
  - plan
  - leadership_scope
outputs:
  - user_request
  - plan
  - artifact
  - evidence
  - decision
  - founder_os_scope
  - hiring_scope
  - productivity_scope
  - retro_scope
  - legal_scope
side_effects:
  - may_coordinate_work
  - may_write_files
write_sets:
  - project:leadership-cycle
failure_policy: stop
invokes:
  - resonance-ops-founder-os
  - resonance-people-hiring
  - resonance-ops-productivity
  - resonance-ops-retro
  - resonance-ops-legal
---

# resonance-leadership-run-operating-cycle: make management explicit

> **Role:** leadership operating conductor.
> **Input:** leadership goal, team issue, hiring need, delegation problem, operating review, or decision cadence.
> **Output:** decision brief, operating cadence, delegation map, feedback plan, hiring loop, or review agenda with owners.
> **Definition of Done:** The cycle names the business outcome, people affected, decision owner, communication plan, follow-up date, and any legal or HR risk. It recommends; the human decides.

## Pipeline

1. **Frame:** define the leadership outcome, constraints, affected people, decision rights, confidentiality, and deadline. -> gate: no hidden stakeholder.
2. **Operating system:** invoke founder-os or productivity for cadence, delegation, priorities, and owner clarity.
3. **People systems:** invoke hiring for role, scorecard, interview loop, or compensation-adjacent hiring decisions.
4. **Review:** invoke retro for lessons, operating debt, and what must change next cycle.
5. **Legal or HR boundary:** invoke legal when employment law, termination, discrimination, compensation, equity, or formal discipline may be involved.
6. **Decision and follow-up:** produce the recommendation, owner, communication plan, and review date. Record durable decisions in the ledger when available.

## Recovery

- The request affects employment status, compensation, or formal discipline -> escalate before action.
- Stakeholders are unknown -> ask before drafting a decision.
- The plan is only vibes -> convert it to owners, dates, and observable outcomes.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory; when `.resonance/ledger/` exists it is the system of record for decisions, lessons, metrics, customers, and experiments, while `02_memory.md` keeps `[lib]` notes and pointers).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
