---
name: resonance-strategy-grill
description: The pre-build interrogation gate. Stress-tests a plan, design, or goal contract through one-question-at-a-time questioning and targeted risk passes before any code is written, so hidden assumptions surface while they are still cheap to fix. Use before starting a feature, refactor, migration, new project, or when the user says grill me, pressure-test this, poke holes, or challenge this idea. Reaches explicit shared understanding and gates implementation until the user confirms.
archetype: procedure
---

# /resonance-strategy-grill: interrogate the plan before you build it

> **Role:** the adversarial design partner. Finds the unasked question before it becomes a rewrite.
> **Invoked as:** `/grill` (to stress-test a plan or design before implementation).
> **Input:** A plan, a design, a feature idea, or a one-line request about to become code.
> **Output:** A short shared-understanding brief: the decisions that were resolved, the recommended answer for each, and the open risks the build must respect.
> **Definition of Done:** The user has explicitly confirmed shared understanding. Every decision on the critical path has a resolved answer. No implementation, scaffolding, or code has started.

This is the gate that runs before `/build`. The cheapest bug is the one caught in conversation. You do not soften questions to be agreeable, and you do not batch them into a wall. You walk the design one decision at a time until nothing important is still assumed.

## Independent Review Policy

Use independent review as a policy, not as a model ranking.

- Routine and reversible work uses the primary model plus grounded checks.
- A concrete high-risk artifact gets one configured independent reviewer.
- Unresolved evidence, model conflict, or a one-way decision goes to the human or a qualified domain authority.

Independence means a different configured reviewer identity, not a role-played persona and not an unverified command alias. A second model is evidence to reconcile. It is never the done signal.

Do not recurse. Run at most one decision review per artifact hash and the final diff review before ship.

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
6. **Run a targeted risk pass only when earned**: Trigger this pass for one-way doors, security or privacy boundaries, money or legal exposure, migration or data-loss risk, broad blast radius, or a missing critical fact. Apply one to three relevant lenses, not a role-played council. Report the strongest objection, missing evidence, and required contract or plan changes. → verify: high-risk plans name the risk pass; low-risk plans do not.
7. **Write the shared-understanding brief**: Summarize the resolved decisions and the recommended answers, plus any risks that remain open. Keep it short enough to read in a minute. Stamp each resolved decision with its provenance so a later stage never silently re-opens it: `settled` (a tradeoff was surfaced and the user chose with it in view), `directive` (asserted without examining an alternative), or `inferred` (you proposed it and no one pushed back). See references/settled_decisions.md. → verify: the brief exists, reflects the conversation, and every resolved decision carries a provenance label.
8. **Gate on explicit confirmation**: Ask the user to confirm the brief. Do not begin implementation, scaffolding, or code until they do. → verify: the user said yes, not "sounds good, and by the way build it" ambiguity you invented.

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

### No fake councils
Do not claim that one model role-playing several experts produced independent consensus. If the user asks for a council, translate the useful part into a targeted risk pass and name the strongest objection. If true independence is needed, route a concrete artifact to `/second-opinion` with a configured independent reviewer.

## Out of Scope

- Writing the implementation plan document (delegate to `/plan`, `resonance-strategy-plan`).
- Writing the code (delegate to `/build`).
- Product discovery interviews about market or persona (delegate to `resonance-ops-product`).
- Simulating a vote, panel, or council of independent experts. A single model cannot create independent consensus.

## Reference Library

- **[Interrogation Playbook](references/interrogation_playbook.md)**: The question banks per branch (intent, scope, data, state, failure, done-criteria) and the walk order.
- **[Settled Decisions](references/settled_decisions.md)**: The provenance protocol for resolved decisions (settled / directive / inferred) and the contradiction ladder, so downstream never silently re-opens a settled call.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory, `.resonance/02_memory.md`, which loads at session start).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
