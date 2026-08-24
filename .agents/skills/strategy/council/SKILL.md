---
name: resonance-strategy-council
description: Decision council for challenging a completed analysis, recommendation, or plan, and for reviewing a consequential choice at a high-risk checkpoint. Selects relevant specialist subagents, gathers blind opening positions, runs one rebuttal round and scenario tests, then reconciles evidence into an advisory decision memo. Use when the user asks for a council, expert panel, multidisciplinary challenge, blind-spot review, or high-stakes deliberation. Does not replace /brief, /grill, /plan, /audit, or /second-opinion.
archetype: orchestration
owner: strategy.council
activation: manual
authority: consequential
triggers:
  - challenge a completed analysis, recommendation, or plan through relevant specialist perspectives
  - review a consequential decision at a high-risk checkpoint
  - convene a council, expert panel, or multidisciplinary blind-spot review
entrypoints:
  - /council
negative_triggers:
  - frame a raw request or create an execution brief
  - answer a simple reversible single-domain question
  - audit code or independently validate a concrete artifact
  - implement or auto-execute the recommendation
inputs:
  - user_request
  - artifact
  - decision_scope
  - evidence
outputs:
  - user_request
  - recommendation
  - evidence
  - decision
  - council_scope
  - review_scope
  - second_opinion_scope
  - brief_scope
  - grill_scope
  - plan_scope
  - goal_scope
side_effects:
  - may_coordinate_work
  - may_write_files
write_sets:
  - project:council-report
failure_policy: stop
invokes:
  - resonance-strategy-brief
  - resonance-strategy-grill
  - resonance-strategy-plan
  - resonance-ops-goal
  - resonance-ops-second-opinion
---

# /resonance-strategy-council: expose blind spots before the decision

> **Role:** the council chair. Select the smallest relevant panel, force useful disagreement, and reconcile evidence without inventing consensus.
> **Invoked as:** `/council` (to challenge an existing analysis or review a high-risk decision).
> **Input:** A completed analysis, recommendation, plan, or explicit high-risk decision checkpoint.
> **Output:** An advisory decision memo with agreements, disagreements, scenarios, recommendation, confidence, reversal conditions, and next action.
> **Definition of Done:** The decision and success criteria are explicit; each selected mandate can change the answer; blind openings and one rebuttal round are complete; material minority objections survive reconciliation; provenance and independence limits are named; the recommendation is evidence-based and includes confidence, reversal conditions, and a human-owned next action; nothing was auto-executed.

This skill reviews a decision artifact. It does not turn a raw request into a better prompt. Use `/brief` for intent framing. Use `/grill` when the missing answer belongs to the user, `/audit` for a technical verification swarm, and `/plan` or `/goal` only after the direction is accepted.

## Prerequisites

- [ ] A completed analysis, recommendation, plan, or explicit high-risk decision exists.
- [ ] The decision, intended outcome, and success criteria can be stated without inventing user intent.
- [ ] Sensitive context is safe for the selected reviewers. External dispatch requires explicit approval.

If the request is simple, reversible, and single-domain, answer directly or route it to the relevant specialist. Do not convene a council for ceremony.

## Algorithm

1. **Bound the review.** Extract the artifact, decision, outcome, criteria, facts, constraints, assumptions, missing evidence, stakes, and reversibility. Preserve provenance. Do not replace `/brief` or silently repair the user's intent. -> verify: a bounded decision packet exists.
2. **Select the panel.** Choose three relevant specialist mandates by default, up to five only when each adds a distinct decision-changing lens. State why each belongs. Do not use a fixed cast or decorative personas. -> verify: every mandate has a distinct question to answer.
3. **Declare provenance.** State whether reviewers are same-family subagents or genuinely independent reviewers. Never call separate context passes independent consensus. -> verify: independence is described accurately.
4. **Collect blind openings.** Dispatch the same decision packet to each specialist before sharing other conclusions. Require a verdict, evidence, assumptions, strongest objection, failure case, and change conditions. -> verify: openings were formed without cross-anchoring.
5. **Run one rebuttal round.** Each specialist challenges the weakest material assumption in another position and the strongest objection to its own. Stop after one round. -> verify: disagreement was tested without recursive debate.
6. **Test scenarios.** Select only scenarios that could change the answer, including failure and reversal cases. Add security, legal, financial, operational, or reputational cases when the stakes warrant them. -> verify: scenario results affect the tradeoff analysis or are omitted.
7. **Reconcile evidence.** Report agreements, disagreements, minority objections, evidence gaps, options, tradeoffs, recommendation, confidence, and reversal conditions. Never vote or average away a high-harm dissent. -> verify: the memo preserves material dissent and traces conclusions to evidence.
8. **Route the next action.** Send user-owned ambiguity to `/grill`. When genuine model independence matters, send one concrete artifact to `/second-opinion` once, then reconcile it. Route accepted direction to `/plan` or `/goal`. Never auto-execute. -> verify: the user retains consequential and one-way decisions.

## Recovery

- Raw or ambiguous ask with no reviewable artifact -> route to `/brief`; do not manufacture a council question.
- A missing value judgment belongs to the user -> pause and route the specific choice to `/grill` with a recommendation.
- Specialist outputs repeat one another -> collapse duplicates, name the missing lens, and do not claim broad coverage.
- Same-model reviewers agree -> report agreement as multi-lens convergence, not independent evidence.
- A high-harm minority objection remains unresolved -> preserve it as a blocker or explicit decision risk regardless of vote count.
- Sensitive material would leave the approved boundary -> stop; offer local review, redaction, or a bounded summary.
- The user requests implementation -> finish the advisory memo, then hand off to the authorized execution skill.

## Guardrails

- Three specialists by default, five maximum.
- One rebuttal round. No recursive councils.
- One `/second-opinion` call per artifact hash when true independence matters.
- No majority vote, simulated consensus, or persona theater.
- No external disclosure without explicit approval.
- No implementation, publication, migration, purchase, deletion, deployment, or shipping.
- Persist a council report only when the user requests a file or a downstream workflow requires the artifact. Limit writes to the named council-report artifact.

## Reference Library

- **[Deliberation Protocol](references/deliberation_protocol.md)**: Decision packet, panel selection, blind openings, rebuttal, reconciliation, and authority boundaries.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory; when `.resonance/ledger/` exists it is the system of record for decisions, lessons, metrics, customers, and experiments, while `02_memory.md` keeps `[lib]` notes and pointers).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
