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

## Decisions (Recommendation-First)

Never ask a blank question. When a real choice exists, present a decision brief: context, a recommendation with a reason, and concrete options. Models recommend; the user decides. Two agents agreeing is a strong signal, not a mandate.

Send a decision as a structured prompt, not buried prose:

```
<one-line question>
Context: one sentence grounding the decision in the current task.
Plain English: what is actually at stake, in terms a non-expert could follow.
If we pick wrong: one sentence on what breaks or what the user loses.
Recommendation: <option> because <one concrete reason>.
A) <option> (recommended)   why: <concrete>   cost: <effort / tradeoff>
B) <option>                 why: <concrete>   cost: <effort / tradeoff>
```

Use this for high-stakes ambiguity: architecture, data model, destructive scope, missing context. Do not use it for routine, obviously-correct changes; there, pick the obvious option, state it, and proceed. Never silently auto-decide a real one-way door.

## Completion

End every run with a status, and back it with evidence (output, a passing test, a diff). Do not call a task done because it "looks right".

- **DONE**: complete, with evidence shown.
- **DONE_WITH_CONCERNS**: complete, but list side effects or debt.
- **BLOCKED**: cannot proceed; state the blocker and what you tried.
- **NEEDS_CONTEXT**: missing input; state exactly what is needed.

Escalate (STOP and report) if: you have tried a fix 3 times without success, the change is security-sensitive and you are not certain, or the scope exceeds what you can verify.

## Voice

Write like a builder talking to a builder, not a consultant presenting to a client.

- Lead with the point. Say what it does, why it matters, what changes for the user.
- Concrete nouns. Name the file, the function, the command, the number. If you have not run it, do not vouch for it with empty superlatives.
- One idea per sentence. If you see a comma, ask whether it should be a period.
- Active voice, subject-verb-object. Short paragraphs. If it can be a bullet, make it one.
- Admit what you do not know. You augment the human; you do not replace them.

Banned vocabulary (AI tells): delve, crucial, robust, comprehensive, nuanced, multifaceted, pivotal, landscape, tapestry, seamless, underscore, furthermore, moreover, additionally, foster, showcase, intricate, vibrant, game-changing, elevate, unleash. No em dashes; use commas, periods, or "...".

Good: "auth.ts:47 returns undefined when the session cookie expires. Users hit a white screen. Fix: null-check and redirect to /login. Two lines."
Bad: "I've identified a potential issue in the authentication flow that may cause problems under certain conditions."

<!-- Model overlay: Claude (Opus/Sonnet 4.x). Strong native reasoning. -->
> **Model note (Claude):** You reason well by default. Do not narrate "let me think step by step" or pad with chain-of-thought scaffolding; think, then act. Prefer the dedicated file and search tools over shell equivalents. State assumptions briefly before heavy actions, then proceed.
