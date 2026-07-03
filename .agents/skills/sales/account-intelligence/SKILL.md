---
name: resonance-sales-account-intelligence
description: Identifies which accounts deserve attention now, why, and what action to take next. Covers signal detection, account scoring, brief generation, and customer-facing deck construction. Use when asked to prioritize accounts, build account briefs, prepare customer decks, or audit account expansion potential.
archetype: procedure
---

# /resonance-sales-account-intelligence: know your accounts before you call

> **Role:** resonance-sales
> **Input:** An account list, CRM data, usage signals, or a meeting brief request.
> **Output:** A ranked account list with why-now evidence and recommended actions, OR a structured account brief/deck.
> **Definition of Done:** Every recommended account has a named signal, a recency date, and a concrete next step. No accounts recommended solely because they are large. No fabricated ownership, intent, or titles. Free of AI slop and em dashes. Passed the validator.

## Prerequisites (fail fast)

- [ ] An account pool is defined (named accounts, segment, territory, or CRM filter).
- [ ] At least one data source is accessible (CRM records, usage data, public signals, or account notes).

## Algorithm

Copy this checklist and tick items as you go.

### Job 1: Account Prioritization (Trigger Radar)

1. **Define the Pool**: Separate the account pool into three motions:
   - **New-logo**: Accounts with no existing relationship.
   - **Recovery**: Churned or dormant accounts with re-engagement potential.
   - **Expansion**: Active accounts with usage or seat growth signals.
   → verify: every account is classified into exactly one motion.

2. **Gather Evidence**: Pull company-approved evidence first (CRM, usage data, account notes, meeting history). Add public triggers (funding rounds, leadership changes, job postings, tech stack signals) only when internal data is insufficient. → verify: internal evidence is primary, public evidence is supplementary.

3. **Score by Actionability**: Rank accounts on four dimensions:
   - **Actionability**: Can the rep take a concrete next step today?
   - **Recency**: How recent is the signal? Use absolute dates, never "recently."
   - **Fit**: Does the account match the ICP on firmographic and behavioral criteria?
   - **Next-step clarity**: Is the recommended action specific enough for a rep to execute?
   → verify: each scored account has values on all four dimensions.

4. **Output a Ranked List**: Return a short ranked list (10-15 accounts max), not a market summary. Label weak or stale evidence rather than forcing a recommendation. → verify: every entry has a signal, date, and next step.

### Job 2: Account Brief Generation

5. **Resolve the Account**: Pull only the approved fields needed:
   - Account plan and renewal context
   - Usage summary (active users, top workflows, feature adoption)
   - Contact map (champion, economic buyer, technical evaluator)
   - Recent meeting context and open opportunities
   → verify: fields are sourced, not invented.

6. **Build the Narrative**: Structure the brief as:
   - What the customer is doing today
   - What value they are already getting (with evidence)
   - What risks, gaps, or opportunities are visible
   - Which use cases fit their stack, role, or goal
   - What next step should come out of the conversation
   → verify: the narrative leads with customer outcomes, not product features.

7. **Choose the Brief Shape**: Match the format to the meeting type:

   | Meeting Type | Focus | Key Slides/Sections |
   |:---|:---|:---|
   | Discovery / first meeting | Credibility + relevant opportunities | Context, automation opportunity, use cases, proof, next steps |
   | QBR / business review | Value delivered + optimization | Health overview, usage trends, feature adoption, opportunities |
   | Renewal | Trajectory + measurable outcomes | Year in review, usage trends, plan fit, expansion, next steps |
   | Expansion / executive | Current value + new team potential | Current impact, builders, what works, new use cases, proof |
   | Onboarding kickoff | Expectations + success criteria | Goals, timeline, team, first milestones |

   → verify: format matches the stated meeting type.

8. **Content Guardrails**:
   - Lead with the customer outcome, not the data source.
   - Use concrete numbers only when the source supports them.
   - Clean up technical names before putting them in customer-facing materials.
   - Flag any claims, roadmap mentions, or customer references that need approval.
   → verify: no raw internal IDs, SQL, private notes, or unapproved proof in customer-facing output.

## Recovery

- Account data is sparse → produce the brief from available context. Flag gaps explicitly: `[MISSING: usage data]`, `[MISSING: champion contact]`. A partial brief with honest gaps beats a fabricated one.
- No clear trigger signal for an account → label it "no current signal" and deprioritize. Do not fabricate urgency.
- Contact map is single-threaded → flag as a risk. Recommend multi-threading actions: "Offer a technical deep-dive for the evaluator" or "Request an executive briefing."
- Tried to build an account brief 3 times without enough data → stop, output what you have, list the specific data sources needed, escalate.

## Cognitive Frameworks

### The Why-Now Test
Every account recommendation must answer: "Why this account, why this week?" If the answer is "they're big" or "they haven't heard from us in a while," that's not a signal. Signals are events, behaviors, or timing that make action relevant now.

### Multi-Threading as Deal Insurance
Deals with a single contact close at ~5%. Deals with 3+ contacts close at 25%+. Every account brief should identify at minimum: the champion (internal advocate), the economic buyer (signs the check), and the technical evaluator (validates the solution). If any are missing, flag it as a gap.

### The Adoption Gap
Compare what the account is using against what they could be using given their company scale, industry, and tech stack. The gap between current usage and potential usage is the expansion hypothesis. Frame it as "signals suggest" and "the data indicates," never as surveillance.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (log durable learnings to `.resonance/learnings.jsonl`).

> **Model note (Claude):** Strong native reasoning. Do not narrate "let me think step by step" or pad with chain-of-thought; think, then act. Prefer the dedicated file and search tools over shell. State assumptions briefly, then proceed.
