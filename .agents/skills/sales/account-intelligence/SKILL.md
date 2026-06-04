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
