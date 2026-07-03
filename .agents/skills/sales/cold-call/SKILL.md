---
name: resonance-sales-cold-call
description: Generates a structured B2B cold call script using a disarming, permission-based 6-part framework. Use when asked to write a cold call script, how to open a call, how to handle phone objections, or to plan a cold calling sales outbound campaign.
archetype: procedure
---

# /resonance-sales-cold-call: structure B2B cold call execution

> **Role:** resonance-sales
> **Input:** Target description (seniority, role, company size, trigger event) + Sender's company offer.
> **Output:** A structured, speakable 6-part cold call script.
> **Definition of Done:** A speakable cold call script is generated containing Opener, Permission Framing, 3 Pain Hypotheses, Discovery, Mini Proof, and Meeting Ask. No AI slop or em dashes present. Passed the validator.

## Prerequisites (fail fast)

- [ ] Target persona's seniority and industry is identified (price-seniority mapped).
- [ ] Product value proposition is climb-ladder mapped to an outcome (not just features).

## Algorithm

Copy this checklist and tick items as you go.

1. **Opener**: Draft a disarming, honest opener that states your name, company, and a pattern interrupt without asking "is this a good time?" or saying "how are you today?". → verify: hook is under 15 words.
2. **Permission Framing**: Draft a permission request that gives the prospect explicit control and a clear exit to reduce immediate defensiveness. → verify: exit condition is stated clearly.
3. **3 Pain Hypotheses**: Formulate three specific pain hypotheses (functional, organizational, strategic) that lets the prospect self-diagnose their bottlenecks. → verify: each hypothesis is under 15 words.
4. **Discovery Questions**: Design a single consequence-focused question that gets the prospect talking about the daily impact of their selected pain. → verify: only 1 main question is posed.
5. **Mini Proof**: Formulate a brief, credible proof point ("companies like...") that establishes authority without generic or fabricated metrics. → verify: is under 3 sentences.
6. **Meeting Ask**: Create a direct meeting ask offering a binary choice of two specific days and times for a brief 15-minute call. → verify: meeting length is capped at 15-20 minutes.

## Recovery

- Prospect hangs up immediately → log as unreachable, do not re-dial same day.
- Prospect asks to "send an email" → redirect to value check: "happy to, but to keep it relevant, which of those three issues I mentioned is closest to what you're dealing with?"
- Tried to customize the script 3 times without a speakable flow → stop, run the 15-second read-aloud test, simplify vocabulary, escalate.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (log durable learnings to `.resonance/learnings.jsonl`).

> **Model note (Claude):** Strong native reasoning. Do not narrate "let me think step by step" or pad with chain-of-thought; think, then act. Prefer the dedicated file and search tools over shell. State assumptions briefly, then proceed.
