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

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (log durable learnings to `.resonance/learnings.jsonl`).

> **Model note (Claude):** Strong native reasoning. Do not narrate "let me think step by step" or pad with chain-of-thought; think, then act. Prefer the dedicated file and search tools over shell. State assumptions briefly, then proceed.
