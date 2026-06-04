---
name: resonance-sales-outbound-sequence
description: Builds source-backed outbound sequences from CRM data, trigger signals, and campaign context. Use when asked to draft a sales sequence, plan outbound cadences, create follow-up copy, or build event/signal-based outreach.
archetype: procedure
---

# /resonance-sales-outbound-sequence: draft sequences that sell, not spam

> **Role:** resonance-sales
> **Input:** Target description (persona, trigger event, campaign context) + CRM/account data + sender's value proposition.
> **Output:** A structured, source-backed outbound sequence with operator notes.
> **Definition of Done:** The sequence contains 3-5 steps with subject lines, body copy, CTAs, personalization markers, operator notes, and assumption flags. Every claim traces to a source. No fabricated proof. No auto-send. Free of AI slop and em dashes. Passed the validator.

## Prerequisites (fail fast)

- [ ] A target persona is identified (role, seniority, industry, company size).
- [ ] At least one trigger signal or campaign context is provided (event, behavior, timing, pain hypothesis).
- [ ] The sender's value proposition is clear enough to connect to a specific outcome.

## Algorithm

Copy this checklist and tick items as you go.

1. **Context Gathering**: Pull the best available context from CRM records, account notes, campaign docs, meeting notes, and any approved data sources. Separate facts from assumptions. → verify: sources are listed, assumptions are flagged.

2. **Decompose the Motion**: Identify the five elements that make a sequence specific:
   - **Audience**: Who exactly receives this? Role, seniority, segment.
   - **Signal**: What triggered this outreach? Event, behavior, timing, pain.
   - **Offer**: What is the specific value proposition for this audience?
   - **Sender**: Who sends it? Rep, founder, SDR? Tone follows sender.
   - **Channel mix**: Email, LinkedIn, call, video? Sequence the channels.
   → verify: all five elements are documented before drafting.

3. **Separate Reusable from Specific**: Identify which elements can be templated across the campaign and which must change per account or per persona. Mark personalization points with `[PERSONALIZE: field]` markers. → verify: at least 3 personalization markers exist per step.

4. **Draft the Sequence**: Write 3-5 concise steps with:
   - Subject line (under 8 words, no clickbait)
   - Body copy (under 120 words per step, plainspoken language)
   - One clear CTA per step (binary choice or specific ask)
   - Operator notes: what the rep should check, customize, or verify before sending
   → verify: each step has a subject, body, CTA, and operator note.

5. **Flag Assumptions and Claims**: Label every claim, statistic, customer reference, or operational detail that needs verification. Use `[VERIFY: claim]` markers. Never invent proof, executive involvement, custom audits, or usage data. → verify: no unverified claims survive without a flag.

6. **Tone and Signal Hygiene**: Review the full sequence for surveillance language. Behavioral signals (page visits, product usage, intent data) are useful but must not sound invasive. Use framing like "based on your team's activity" not "we noticed you visited our pricing page 4 times." → verify: read the sequence from the prospect's perspective.

## Recovery

- Trigger signal is vague or missing → ask ONE targeted question: "What event, behavior, or timing makes this audience worth contacting now?" Do not proceed on zero-signal outreach.
- No CRM data available → draft the sequence from campaign context alone. Flag every personalization marker as `[NEEDS CRM DATA]`. Produce a usable skeleton, not a blocker.
- Rep wants to port copy from another campaign → separate the reusable elements (structure, CTA pattern, channel mix) from the specific elements (claims, proof, persona details). Never blindly copy subject lines or proof points across audiences.
- Tried to draft a speakable sequence 3 times without a natural flow → stop, reduce to 3 steps maximum, simplify vocabulary, escalate.

## Cognitive Frameworks

### The Signal-to-Noise Ratio
Every outbound step competes with 100+ messages per day. The only sequences that convert are those where the prospect thinks "this person actually understands my situation." Generic outreach is noise. Source-backed outreach is signal.

### The Personalization Ladder
Level 1: Name + company (worthless, everyone does this).
Level 2: Industry + role (slightly better, still generic).
Level 3: Trigger + pain hypothesis (this is the minimum bar).
Level 4: Account-specific context + quantified gap (this is where deals start).

### The Approval Gate Pattern
No outbound sequence should auto-send. The workflow:
1. Agent drafts the sequence with source-backed context.
2. Rep reviews, customizes personalization markers, verifies claims.
3. Rep approves each step before it enters the send queue.
4. CRM/sequencer logs the send with attribution.

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

<!-- Model overlay: Claude (Opus/Sonnet 4.x). Strong native reasoning. -->
> **Model note (Claude):** You reason well by default. Do not narrate "let me think step by step" or pad with chain-of-thought scaffolding; think, then act. Prefer the dedicated file and search tools over shell equivalents. State assumptions briefly before heavy actions, then proceed.
