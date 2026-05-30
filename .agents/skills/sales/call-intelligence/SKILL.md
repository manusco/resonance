---
name: resonance-sales-call-intelligence
description: Analyzes sales call transcripts to extract deep persona insights, objection handling metrics, vocabulary libraries, and feature requests. Use when asked to audit discovery calls, extract insights from meeting recordings, or compile prospect feedback.
archetype: procedure
---

# /resonance-sales-call-intelligence: analyze sales transcripts

> **Role:** resonance-frontend
> **Input:** Sales call transcripts (pasted text, CSV, or MCP connections).
> **Output:** A structured Persona Intelligence Report and Interactive React Dashboard.
> **Definition of Done:** The output dashboard parses speaker turns, extracts goals, pains, triggers, objections, and product feature gaps with direct verbatims, and provides a messaging vocabulary library. Free of AI slop and em dashes. Passed the validator.

## Prerequisites (fail fast)

- [ ] Transcripts or call recordings are available for analysis.
- [ ] You have identified if speaker attribution (rep vs. prospect) is present or needs auto-inference.

## Algorithm

Copy this checklist and tick items as you go.

1. **Profile Prospects**: Extract job titles, seniority levels, and target department groupings (e.g., C-Suite, VP, Manager). → verify: dataset confidence level is declared at top.
2. **Ingest and Clean**: Ingest raw text or CSV entries, map speakers, and separate conversation blocks. → verify: transcript source type is declared.
3. **Extract 10 Dimensions**: Extract goals, pains (functional/emotional/social), triggers, objections, product gaps, competitor comments, buying processes, vocabulary words, buying signals, and red flags. → verify: all quotes are extracted exactly as spoken.
4. **Objection & Feature Analysis**: Tabulate objection types and rank product feature gaps by frequency. → verify: objection handling is rated as Effective, Neutral, or Missed.
5. **Interactive Dashboard**: Construct an interactive React-based dashboard displaying tabs for Overview, Personas, Objections, Feature Gaps, and Vocabulary. → verify: contains a bar chart representing objection frequency.

## Recovery

- Transcript dataset size is extremely small (1-2 calls) → label confidence as LOW and append a standard directional hypothesis warning.
- Speaker attribution is missing or mixed → run speaker role auto-inference logic (detecting who explains pricing/product vs. who highlights constraints) before continuing.
- Tried to build a dashboard 3 times but React components hit rendering errors → stop, output the structured long-form markdown report instead, and escalate.

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
