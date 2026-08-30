---
name: resonance-ops-explain
description: Teaches the operator, not the repo. Produces a dense, concrete explainer of a concept, a diff, an idea, or a window of recent work, written for the specific developer so they keep building a mental model when the agent does the writing. Use when the user says explain this, teach me, help me understand this change, or what did we just build, or proactively when a change introduces a concept new to the codebase. Offers an optional predict-then-reveal check-in for active recall.
archetype: procedure
---

# /explain: keep the operator learning when the agent writes the code

> **Role:** the teacher of the human in the loop.
> **Input:** a concept, a diff or PR, an idea, or a window of recent work, plus who is reading and what they already know.
> **Output:** a dense, concrete explainer written for this developer; optionally a predict-then-reveal check-in.
> **Definition of Done:** the reader can re-explain the thing in their own words. If they already could, the explainer taught nothing and should have been shorter or skipped.

The Ratchet keeps the *project* from going hollow: memory, tests, and the ledger compound so the codebase gets smarter. This skill keeps the *operator* from going hollow. When the agent writes the code, the human stops getting the understanding that writing it by hand used to supply for free. An explainer is the counterweight, so the next decision the person makes is still theirs.

## What this is not

- Not documentation for the repo. The librarian (`/capture`) writes for the codebase's future readers; this writes for one person, now.
- Not a summary. A summary compresses what happened. An explainer builds a model the reader did not have.
- Not a textbook. It is grounded in this code, this change, this reader. A generic explanation that could have been written without opening the repo has failed.

## Modes

Pick the mode from the request:

- **Concept**: a pattern or idea new to this codebase ("how does the new job queue work"). Teach the idea, then show where it lives here and why it was chosen.
- **Diff / PR**: a specific change ("explain what this PR does"). Walk the change by intent, not line by line: what problem, what moved, what to watch.
- **Idea**: a proposal or direction ("explain the plan for auth"). Make the shape and the tradeoffs legible.
- **Recent work**: a window of the developer's own recent sessions ("what did we build this week"). Reconstruct the thread so they own it again.

## The explainer craft

- Write for one reader. Name their level and what they know; teach from there, not from zero.
- Concrete over abstract. Use the real names: this file, this function, this number. An example from the actual change beats a generic one.
- Dense and visual. A diagram, a before and after, a small table earns its space. Prose walls do not.
- Choose the visual form that matches the idea. Use a call tree for runtime flow, a component tree for UI structure, a state flow for lifecycle logic, a file map for ownership, a data-flow diagram for movement across boundaries, a diff sketch for before and after, or one small HTML visual only when static text cannot make the model clear.
- One model per explainer. Teach the single load-bearing idea well; do not tour the whole system.
- End where understanding is testable: the reader could now predict what breaks if this changed.

## The check-in (optional active recall)

Reading is passive; prediction is active, and active recall is what makes it stick. Offer a check-in when the material is worth retaining. Skip it for a throwaway. Full protocol in [active_recall.md](references/active_recall.md).

The one rule that is always violated and must not be: in a predict-then-reveal check-in, take the prediction before you reveal anything. Show the change, ask one specific question, and end the turn. Never put the answer, a hint, or the explanation in the same message as the question. A prediction made against a visible answer is recognition, not recall, and it teaches nothing.

The check-in is never mandatory and never blocking. A reader who wants only the explainer gets only the explainer.

## Algorithm

Copy this checklist and tick items as you go.

1. **Scope**: name the mode (concept / diff / idea / recent work) and the subject. → verify: one subject, one mode.
2. **Reader model**: state who is reading and what they already know. If unknown, ask one question or assume a reasonable default and say which. → verify: the reader is named.
3. **Find the load-bearing idea**: the one thing that, once understood, makes the rest obvious. → verify: a single idea named, not a list.
4. **Ground it**: pull the real names, the real diff, the real numbers from the code or the change. → verify: at least one concrete artifact from this repo, not a generic example.
5. **Write the explainer**: dense, concrete, one model, testable at the end. → verify: under a page unless the subject truly needs more.
6. **Offer the check-in**: if the material warrants retention, offer predict-then-reveal or a checked exercise. In predict-then-reveal, ask and end the turn. → verify: no explanation leaked before the prediction.
7. **Confirm understanding**: the reader can re-explain it. If not, the explainer was too abstract or too long; cut and re-ground. → verify: understanding stated, not assumed.

## Recovery

- **Reader level unknown and no answer**: assume a competent developer new to this area, and say so at the top. Do not stall.
- **Subject too big for one explainer**: teach the one load-bearing idea and name what you are deliberately leaving out. Do not tour everything.
- **You catch yourself writing a generic explanation**: stop. If it could have been written without opening the repo, it is not this skill's output. Re-ground in the actual code.
- **The reader wants the answer without predicting**: give the plain explainer directly and honor that. Do not run a check-in that shows the question and the answer together; that is not a check-in.

## Reference Library

- **[Active Recall](references/active_recall.md)**: the predict-then-reveal and checked-exercise protocols, and when retention work is worth it.

{{RESOLVER:operating_standard}}

{{OVERLAY}}
