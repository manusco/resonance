---
name: resonance-ops-page-audit
description: The Experience Auditor Swarm. Audits a live page or a whole site from first principles: the job each page exists to do, whether its value promise is real and delivered fast, clarity, the path to action, craft, function, and trust. Use when auditing a website or landing page you run, doing a first-principles UX and conversion review, asking where a site can be improved, or producing a forward-looking improvement backlog. Runs the experience lenses (conversion, design, copywriter, seo, code audit) page by page, then hands implementation to /goal and shipping to /ship.
archetype: orchestration
owner: ops.page-audit
activation: manual
authority: consequential
triggers:
  - audit a page, website, or product experience
entrypoints:
  - /page-audit
negative_triggers:
  - implement or deploy the findings directly
inputs:
  - user_request
  - artifact
  - page_audit_scope
outputs:
  - user_request
  - recommendation
  - plan
  - evidence
  - conversion_scope
  - copy_scope
  - design_scope
  - seo_scope
  - test_scope
  - qa_scope
  - audit_scope
  - health_scope
side_effects:
  - may_coordinate_work
  - may_execute_checks
write_sets:
  - project:experience-backlog
failure_policy: stop
invokes:
  - resonance-ops-system-health
  - resonance-ops-audit
  - resonance-marketing-conversion
  - resonance-marketing-copywriter
  - resonance-design-designer
  - resonance-marketing-seo
  - resonance-ops-qa
---

# /resonance-ops-page-audit: audit the experience, not just the code

> **Role:** the Experience Gatekeeper. You walk up to each page fresh and make it prove why it deserves to exist.
> **Invoked as:** `/page-audit` (to run the experience swarm across a page or a site).
> **Input:** A live URL, a local site repo, or a set of properties.
> **Output:** A per-page findings sheet (add / change / rearrange / remove), a `FUTURE_IMPROVEMENTS.md` forward backlog, and for a multi-site run a cross-site master report.
> **Definition of Done:** Every in-scope page and relevant state is inventoried. Findings distinguish observed evidence from assumptions, name the owning lens, and rank changes by the page's user task and risk. The forward backlog is written and ranked.

`/audit` hunts the code for what is broken. This is its twin for the experience. You do not lead with a list of tweaks. You ask, for every page, what job it does, whether the value is real, and whether the intended user can complete the relevant task. Use above-the-fold promise and time-to-value checks where the page serves a marketing or acquisition job. The current page is evidence, not the target. Derive the answer from the job to be done, then decide: add, change, rearrange, remove, or leave.

You do not run every lens yourself. You orchestrate the skills that already own each one, and you add the frame none of them have: the page's reason to exist, the gap between promise and delivery where relevant, and the highest-priority change for the user or business. Include other necessary findings in the ranked plan.

## Prerequisites (fail fast)

- [ ] You can reach the page: a running URL, or a local build you can serve and drive in a real browser.
- [ ] You know the audience and the business goal, or you have read them from `.resonance/`. If neither, that is a `/grill` question for the owner, not a guess.

## Algorithm (The Loop)

Copy this checklist and tick items as you go. Run it per site, page by page. Do not stop on a cosmetic nudge.

1. **Ground.** Read `.resonance/` (soul, systems, state) and the site's docs. Write down what the site is, who it serves, the one business outcome that matters, and what "better" means here in numbers. Unknown from the repo means a `/grill` question, not an assumption.
2. **Inventory.** Enumerate every page and every meaningful state from `src/pages`, `app/`, the router, and the rendered output. No page gets skipped. Produce the page list before auditing.
3. **Baseline.** Run `/system-health` for the score and flags, and `/audit` for code, security, and function findings (P0-P3). This is the safety net a page-by-page pass misses.
4. **Interrogate each page.** Run the first-principles battery (see Page Interrogation Battery). For each dimension, delegate the deep lens to the skill that owns it, and add the frames only this skill carries. Produce a per-page findings sheet.
   - Purpose, user job, task path, and useful or missing information: this skill's frame.
   - Value promise vs delivery, and the gap: this skill's frame, with `/friction` for the value-proposition mechanics.
   - Copy, idiomatic and proof-backed: delegate to `/copywriter`.
   - Clarity and task hierarchy: `/design`, with `/friction` for commercial friction.
   - Commercial action and conversion: `/friction`; preserve product-workspace actions that serve distinct tasks.
   - Design and craft: `/design`.
   - Function and correctness: `/audit` and `/test`. Click it, submit it, break it.
   - Performance, SEO, accessibility, trust: `/seo` and `/audit`.
5. **Anti-theater pass.** For each page, name the highest-priority change that will matter most to a real user. Put it first in the plan alongside any other necessary findings.
6. **Synthesize.** Rank each page's findings as add, change, rearrange, or remove, most important first. For a multi-site run, extract the patterns that repeat across sites.
7. **Forward backlog.** Write `FUTURE_IMPROVEMENTS.md` per site (see Forward Backlog Protocol). For a multi-site run, write the cross-site master report.
8. **Hand off.** Implementation goes to `/goal`, deploy to `/ship`. You produce the plan and the backlog. You do not implement or ship in this skill.

## Recovery

- Audience or goal is not knowable from the repo → stop guessing, raise it as a `/grill` question for the owner.
- A page's claim cannot be verified against real product behavior → flag it as a trust risk and stop. Do not audit the conversion of a false promise.
- Every finding is cosmetic → you have not gone deep enough. Re-run the battery on the job and the value gap, not the surface.

## Out of Scope

- Implementing the changes (delegate to `/goal`).
- Deploying and verifying production (delegate to `/ship`).
- The internals of the code and security audit (delegate to `/audit`, which you call as a lens).
- Writing the long-form copy (delegate to `/copywriter`).

## Cognitive Frameworks

### First Principles
The current page is evidence, not the target. State the page's job and the user's task path from available evidence. If the job is unclear, record the uncertainty and its impact; do not declare the page unfocused without evidence.

### The Value Gap
For marketing pages, compare the promise at the decision point with what the page delivers and how quickly. For task workspaces, measure the task information, status, and action path users need. Record the evidence and choose a task-appropriate measure; do not require an above-the-fold marketing model for every surface.

### Anti-Theater (Substantial or Nothing)
A page is not "done" because a button got renamed. The audit should identify an evidence-backed priority and a way to judge it. If a change would not help a real user or the stated business goal, it is theater. Rank the priority first and include all other necessary findings in the plan; implementation belongs to the handoff owner.

### Removal is a Feature
Find what users need to notice, understand, compare, decide, and do. Derive hierarchy and action staging from task frequency, consequence, uncertainty, and recovery cost. Multiple actions may be valid on product workspaces or comparison pages. Delegate detailed visual hierarchy to `/design` and commercial action choices to `/friction`.

## Deliverables

- **Per-page findings sheet**: job, value gap, and the ranked list of moves (add / change / rearrange / remove), each naming the owning lens.
- **`FUTURE_IMPROVEMENTS.md`** per site: the forward backlog, what would make the site great next, ranked and grouped by theme. See the protocol.
- **Cross-site master report** (multi-site only): the patterns that repeat and the few moves that lift every site at once.

## Reference Library

- **[Page Interrogation Battery](references/page_interrogation_battery.md)**: The full first-principles battery, the lens each dimension delegates to, and the adaptation for non-web surfaces (a game's screens and states).
- **[Forward Backlog Protocol](references/forward_backlog_protocol.md)**: The `FUTURE_IMPROVEMENTS.md` spec, the cross-site master report, and the "substantial or nothing" done-bar.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory; when `.resonance/ledger/` exists it is the system of record for decisions, lessons, metrics, customers, and experiments, while `02_memory.md` keeps `[lib]` notes and pointers).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
