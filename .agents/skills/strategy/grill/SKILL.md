---
name: resonance-strategy-grill
description: The pre-build interrogation gate. Stress-tests a plan or design through relentless, one-question-at-a-time questioning before any code is written, so hidden assumptions surface while they are still cheap to fix. Use before starting a feature, refactor, or new project, when a plan feels underspecified, or when the user says grill me, pressure-test this, poke holes, or challenge this idea. Reaches explicit shared understanding and gates implementation until the user confirms.
archetype: procedure
---

# /resonance-strategy-grill: interrogate the plan before you build it

> **Role:** the adversarial design partner. Finds the unasked question before it becomes a rewrite.
> **Invoked as:** `/grill` (to stress-test a plan or design before implementation).
> **Input:** A plan, a design, a feature idea, or a one-line request about to become code.
> **Output:** A short shared-understanding brief: the decisions that were resolved, the recommended answer for each, and the open risks the build must respect.
> **Definition of Done:** The user has explicitly confirmed shared understanding. Every decision on the critical path has a resolved answer. No implementation, scaffolding, or code has started.

This is the gate that runs before `/build`. The cheapest bug is the one caught in conversation. You do not soften questions to be agreeable, and you do not batch them into a wall. You walk the design one decision at a time until nothing important is still assumed.

## Prerequisites (fail fast)

- [ ] There is a plan, design, or request to interrogate. If the request is a single vague line, that is not a blocker, it is the reason to run this.
- [ ] The user has not already said "just build it, no questions". If they have, honor it and exit.

## Algorithm

Copy this checklist and tick items as you go.

1. **Map the decision tree**: Before asking anything, list the decisions this plan depends on and their order. A choice of data model constrains the API, which constrains the UI. Resolve upstream decisions first. → verify: you have an ordered list of decisions, not a flat pile.
2. **Answer from the codebase first**: For each decision, ask whether the answer is discoverable by reading the code, the schema, or the existing patterns. If it is, go find it. Only spend a question on what only the user knows. → verify: you did not ask the user something the repo already answered.
3. **Ask one question at a time**: Send a single question, carrying your recommended answer and one concrete reason. Wait for the reply before the next. A list of ten questions is bewildering and gets skimmed. → verify: exactly one open question per turn.
4. **Follow the dependency, not a script**: Let each answer open or close the next branch. When an answer changes an upstream assumption, walk back up before going down. → verify: later questions reflect earlier answers.
5. **Push on the soft spots**: For each resolved area, run the failure lens: what happens at zero items and at ten thousand, on the mobile case, when the network drops, when two users race, when the input is hostile. Surface the ones that matter. → verify: edge cases and failure modes were named, not skipped.
6. **Write the shared-understanding brief**: Summarize the resolved decisions and the recommended answers, plus any risks that remain open. Keep it short enough to read in a minute. → verify: the brief exists and reflects the conversation.
7. **Gate on explicit confirmation**: Ask the user to confirm the brief. Do not begin implementation, scaffolding, or code until they do. → verify: the user said yes, not "sounds good, and by the way build it" ambiguity you invented.

## Recovery

- The user answers "I don't know" to a real decision → offer your recommendation and the tradeoff, mark it as your call, and note it in the brief as an assumption to revisit. Do not stall.
- You have asked more than roughly eight questions and clarity is not converging → stop, write the brief with what is resolved, name what is still open, and hand the decision back.
- The user tries to jump straight to building mid-grill → restate the one or two unresolved decisions that would cause a rewrite, then let them choose to proceed anyway. The gate warns; it does not trap.

## Cognitive Frameworks

### The "too simple to design" trap
The failure mode is skipping this on a task that "obviously" needs no design. Simple tasks are where unexamined assumptions hide best, because nobody looks. Run the gate at proportional depth: three questions for a small change, not thirty. Depth scales; the gate does not turn off.

### Recommend, never interrogate blankly
Every question carries your recommended answer and a reason. "Should sessions expire?" is lazy. "I would expire sessions at 30 days to bound the token table, unless you need longer-lived logins, do you?" moves the work forward. The user reacts to a proposal faster than they author one from nothing.

### The gate is the product
The output is not a document, it is a confirmed shared understanding. If the user learned nothing and you learned nothing, the grill was theater. A good session changes at least one decision.

## Out of Scope

- Writing the implementation plan document (delegate to `/plan`, `resonance-strategy-plan`).
- Writing the code (delegate to `/build`).
- Product discovery interviews about market or persona (delegate to `resonance-ops-product`).

## Reference Library

- **[Interrogation Playbook](references/interrogation_playbook.md)**: The question banks per branch (intent, scope, data, state, failure, done-criteria) and the walk order.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory, `.resonance/02_memory.md`, which loads at session start).

> **Model note (Claude):** Strong native reasoning. Do not narrate "let me think step by step" or pad with chain-of-thought; think, then act. Prefer the dedicated file and search tools over shell. State assumptions briefly, then proceed.
