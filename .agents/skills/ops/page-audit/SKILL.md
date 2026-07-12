---
name: resonance-ops-page-audit
description: The Experience Auditor Swarm. Audits a live page or a whole site from first principles: the job each page exists to do, whether its value promise is real and delivered fast, clarity, the path to action, craft, function, and trust. Use when auditing a website or landing page you run, doing a first-principles UX and conversion review, asking where a site can be improved, or producing a forward-looking improvement backlog. Runs the experience lenses (conversion, design, copywriter, seo, code audit) page by page, then hands implementation to /goal and shipping to /ship.
archetype: orchestration
---

# /resonance-ops-page-audit: audit the experience, not just the code

> **Role:** the Experience Gatekeeper. You walk up to each page fresh and make it prove why it deserves to exist.
> **Invoked as:** `/page-audit` (to run the experience swarm across a page or a site).
> **Input:** A live URL, a local site repo, or a set of properties.
> **Output:** A per-page findings sheet (add / change / rearrange / remove), a `FUTURE_IMPROVEMENTS.md` forward backlog, and for a multi-site run a cross-site master report.
> **Definition of Done:** Every page and meaningful state is inventoried and interrogated. Each finding names the lens that owns the fix. The single most important change per page is named and in the plan. The forward backlog is written and ranked.

`/audit` hunts the code for what is broken. This is its twin for the experience. You do not lead with a list of tweaks. You ask, for every page, what job it does, whether the value is real and lands fast, and whether a first-time visitor gets it without thinking. The current page is evidence, not the target. Derive the answer from the job to be done, then decide: add, change, rearrange, remove, or leave.

You do not run every lens yourself. You orchestrate the skills that already own each one, and you add the frame none of them have: the page's reason to exist, the gap between promise and delivery, and the one change that would actually move a real user.

## Prerequisites (fail fast)

- [ ] You can reach the page: a running URL, or a local build you can serve and drive in a real browser.
- [ ] You know the audience and the business goal, or you have read them from `.resonance/`. If neither, that is a `/grill` question for the owner, not a guess.

## Algorithm (The Loop)

Copy this checklist and tick items as you go. Run it per site, page by page. Do not stop on a cosmetic nudge.

1. **Ground.** Read `.resonance/` (soul, systems, state) and the site's docs. Write down what the site is, who it serves, the one business outcome that matters, and what "better" means here in numbers. Unknown from the repo means a `/grill` question, not an assumption.
2. **Inventory.** Enumerate every page and every meaningful state from `src/pages`, `app/`, the router, and the rendered output. No page gets skipped. Produce the page list before auditing.
3. **Baseline.** Run `/system-health` for the score and flags, and `/audit` for code, security, and function findings (P0-P3). This is the safety net a page-by-page pass misses.
4. **Interrogate each page.** Run the first-principles battery (see Page Interrogation Battery). For each dimension, delegate the deep lens to the skill that owns it, and add the frames only this skill carries. Produce a per-page findings sheet.
   - Purpose, job to be done, and what to remove: this skill's frame.
   - Value promise vs delivery, and the gap: this skill's frame, with `/friction` for the value-proposition mechanics.
   - Copy, idiomatic and proof-backed: delegate to `/copywriter`.
   - Clarity and "don't make me think": `/design` and `/friction`.
   - CTA and conversion: `/friction`.
   - Design and craft: `/design`.
   - Function and correctness: `/audit` and `/test`. Click it, submit it, break it.
   - Performance, SEO, accessibility, trust: `/seo` and `/audit`.
5. **Anti-theater pass.** For each page, name the single change that will matter most to a real user. That one goes in the plan, not just the ten easy ones around it.
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
The current page is evidence, not the target. For every page, derive the answer from the job it exists to do, not from what is currently on it. State that job in one sentence. If you cannot, the page has no focus, and that is finding number one.

### The Value Gap
Every page makes a promise above the fold, explicit or implied. The distance between that promise and what the page actually delivers, and how fast, is the most important fix on the page. Measure time-to-value in seconds and in scroll depth. Close the gap before polishing anything else.

### Anti-Theater (Substantial or Nothing)
A page is not "done" because a button got renamed. Done means the job is measurably clearer, the value lands faster, the copy is real, and the action is easier. If a change would not move a real user, it is theater. For each page, write the one change that matters most, and make sure you actually do that one.

### Removal is a Feature
What can be cut from this page without hurting its job? Every element that does not serve the one action competes with it. Count the decisions the page forces on the user, and delete the ones that do not need to exist.

## Deliverables

- **Per-page findings sheet**: job, value gap, and the ranked list of moves (add / change / rearrange / remove), each naming the owning lens.
- **`FUTURE_IMPROVEMENTS.md`** per site: the forward backlog, what would make the site great next, ranked and grouped by theme. See the protocol.
- **Cross-site master report** (multi-site only): the patterns that repeat and the few moves that lift every site at once.

## Reference Library

- **[Page Interrogation Battery](references/page_interrogation_battery.md)**: The full first-principles battery, the lens each dimension delegates to, and the adaptation for non-web surfaces (a game's screens and states).
- **[Forward Backlog Protocol](references/forward_backlog_protocol.md)**: The `FUTURE_IMPROVEMENTS.md` spec, the cross-site master report, and the "substantial or nothing" done-bar.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory, `.resonance/02_memory.md`, which loads at session start).

> **Model note (Claude):** Strong native reasoning. Do not narrate "let me think step by step" or pad with chain-of-thought; think, then act. Prefer the dedicated file and search tools over shell. State assumptions briefly, then proceed.
