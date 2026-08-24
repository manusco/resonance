---
name: resonance-strategy-gtm-thinker
description: GTM hypothesis challenger. Use when a concrete B2B positioning, audience, offer, channel, or campaign concept has not earned commitment. Deconstructs the bet, tests assumptions, compares alternatives, and defines evidence and kill criteria. Growth owns company-wide bottleneck and channel portfolio choices. Run Campaign owns approved campaign preparation.
archetype: procedure
---

# /resonance-strategy-gtm-thinker: stress-test and expand GTM concepts

> **Role:** GTM hypothesis challenger.
> **Input:** A GTM idea description, campaign angle, or positioning hypothesis.
> **Output:** A GTM hypothesis decision packet.
> **Definition of Done:** The core hypothesis is explicit; assumptions are ranked by validation risk; the strongest counterargument is stated; deepen, adjacent, and contrarian alternatives are compared; the minimum evidence test and kill criteria exist; the recommendation is `proceed`, `revise`, or `reject`; and the next owner and handoff artifact are named.

## Prerequisites (fail fast)

- [ ] A GTM concept, target audience, or campaign goal is provided.
- [ ] You have identified if the concept is an outbound, inbound, product-led, or positioning move.

## Algorithm

Copy this checklist and tick items as you go.

1. **Deconstruct the Hypothesis**: Formulate the core bet in a clean "if we do X, then Y will happen, because Z" structure, and audit all underlying assumptions. → verify: assumptions are categorized by validation risk.
2. **Challenge Assumptions**: Act as a devil's advocate. State the strongest, most damaging counterargument against the idea and outline major organizational blind spots. → verify: counterargument is stated in under 3 sentences.
3. **PVP Expansion**: Expand the idea in 3 directions: (1) Deepen the core (10x version), (2) Adjacent plays, and (3) A contrarian or anti-conventional version that breaks category norms. → verify: all 3 expansions are documented.
4. **Validation Design**: Define the smallest real-world test that can generate a decision-grade signal. A bounded evidence sequence may span up to four weeks. Do not create channel assets, campaign calendars, publishing schedules, budgets, or launch approvals. → verify: the sequence tests the riskiest assumption without absorbing campaign execution.
5. **Metrics & Kill Criteria**: Define leading indicators, lagging indicators, and a hard, quantifiable kill threshold. → verify: a specific kill threshold is explicitly defined.
6. **Decide and Hand Off**: Recommend `proceed`, `revise`, or `reject`. Send one accepted campaign hypothesis to `resonance-marketing-run-campaign`; send competing bets or unresolved investment priority to `resonance-strategy-growth`; return a rejected hypothesis with evidence and no execution plan. → verify: one next owner and a named handoff artifact exist.

## Out of Scope

- Cross-funnel bottleneck diagnosis and channel portfolio choice → `resonance-strategy-growth`.
- Campaign coordination, specialist assets, approvals, tracking implementation, publishing, and spend proposals → `resonance-marketing-run-campaign`.
- Copy, media buying, organic distribution, lifecycle design, creative production, and measurement validity stay with their owner skills.

## Recovery

- GTM idea is too vague to calculate assumptions → ask the user ONE targeted question about the target audience or ultimate goal before proceeding. Do not proceed silently on wild assumptions.
- Core GTM hypothesis lacks an execution mechanism → halt analysis, reconstruct the "how" of the execution loop, and present it back to the user for validation.
- No viable evidence test exists after 3 attempts → stop and recommend `revise` or `reject`. Do not assume ownership of execution by shrinking the request into a micro-campaign.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory; when `.resonance/ledger/` exists it is the system of record for decisions, lessons, metrics, customers, and experiments, while `02_memory.md` keeps `[lib]` notes and pointers).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
