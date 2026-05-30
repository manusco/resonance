# B2B Sales Pipeline Protocol

> **Goal**: Engineer a B2B sales pipeline from first principles — qualification, pipeline mechanics, deal strategy, and objection handling. Dense reference for agents building or auditing sales systems.

## 1. The Revenue Equation

Everything in B2B sales reduces to one equation:

```
Revenue = Opportunities × Win Rate × Average Deal Size × (1 / Sales Cycle Length)
```

Improving any variable improves revenue. The highest-leverage variable depends on your stage:
- **Early-stage** (< $1M ARR): Focus on Opportunities (volume) and Win Rate (qualification).
- **Growth** ($1-10M ARR): Focus on Average Deal Size (move upmarket) and Sales Cycle (process efficiency).
- **Scale** ($10M+): Focus on Win Rate (deal strategy) and all variables simultaneously.

---

## 2. Lead Lifecycle — The Handoff Chain

Every handoff is a potential leak. Define stages, owners, and SLAs with zero ambiguity.

| Stage | Entry Criteria | Owner | SLA | Exit |
|-------|---------------|-------|-----|------|
| **Subscriber** | Opted into content | Marketing | — | Engagement threshold met |
| **Lead** | Identified + basic info | Marketing | — | Fit criteria met |
| **MQL** | Fit + engagement score | Marketing | — | Sales accepts/rejects in 48h |
| **SQL** | Sales qualifies via call | Sales (SDR) | Contact in ≤4h | Opportunity created or recycled |
| **Opportunity** | BANT/MEDDIC confirmed | Sales (AE) | — | Closed-won or closed-lost |
| **Customer** | Contract signed | CS | Onboard in ≤7 days | Retained or churned |

### MQL Definition (The Gate That Matters Most)
An MQL requires **both** fit AND engagement. Neither alone qualifies.

**Fit** (who they are): ICP match on company size, industry, role, tech stack, geography.
**Engagement** (what they did): Pricing page visit, demo request, multiple sessions, content download pattern.

A Fortune 500 CTO who never visits your site isn't an MQL. A college student who downloads every ebook isn't an MQL.

### Speed-to-Lead (The Silent Revenue Killer)

| Response Time | Qualification Likelihood |
|--------------|------------------------|
| < 5 minutes | **21x** more likely to qualify |
| 5-30 minutes | 4x more likely |
| > 30 minutes | 10x drop in conversion |
| > 24 hours | Lead is effectively cold |

**Rule**: If you can't contact MQLs in under 5 minutes, fix routing before fixing anything else.

---

## 3. Lead Scoring — Quantifying Intent

### Two-Axis Model (Fit × Engagement)

```
                    HIGH FIT
                       │
        IDEAL MQL      │      NURTURE
    (High fit,         │   (High fit,
     high engagement)  │    low engagement)
                       │
───────────────────────┼───────────────────
                       │
        MONITOR        │      DISCARD
    (Low fit,          │   (Low fit,
     high engagement)  │    low engagement)
                       │
                    LOW FIT
```

### Scoring Signals

**Fit Scoring (Explicit)**:
| Signal | Points | Rationale |
|--------|--------|-----------|
| Company size matches ICP | +20 | Core qualification |
| Decision-maker title | +15 | Authority to buy |
| Target industry | +10 | Relevant use case |
| Compatible tech stack | +5 | Integration fit |

**Engagement Scoring (Implicit)**:
| Signal | Points | Rationale |
|--------|--------|-----------|
| Demo/trial request | +25 | Active evaluation |
| Pricing page (2+ visits) | +15 | Buying intent |
| Case study download | +10 | ROI evaluation |
| 3+ sessions in 7 days | +10 | Sustained interest |
| Email click (nurture) | +5 | Engaged |

**Negative Scoring**:
| Signal | Points | Why |
|--------|--------|-----|
| Competitor domain | -50 | Intelligence gathering |
| Personal email for B2B | -20 | Non-buyer signal |
| Unsubscribe | -30 | Exit signal |
| Title: student/intern | -15 | No authority |

**MQL Threshold**: 50-80 points on 100-point scale. Calibrate quarterly against closed-won data.

---

## 4. Qualification Frameworks — When to Use Which

This is the most important decision in your sales process. The wrong framework for your deal complexity wastes time or loses deals.

### BANT (Budget, Authority, Need, Timeline)

| Factor | Key Question |
|--------|-------------|
| Budget | "Is there budget allocated?" |
| Authority | "Who makes the final decision?" |
| Need | "What problem are you solving?" |
| Timeline | "When do you need this?" |

**Use when**: ACV < $10K, transactional sales, short cycle (< 30 days), single decision-maker.
**Weakness**: Assumes buyer knows their budget and timeline upfront. Fails on complex deals.

### MEDDIC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion)

| Factor | Key Question |
|--------|-------------|
| Metrics | "What measurable outcome defines success?" |
| Economic Buyer | "Who signs the check?" |
| Decision Criteria | "How will you evaluate solutions?" |
| Decision Process | "Walk me through your buying process and timeline." |
| Identify Pain | "What happens if you don't solve this?" |
| Champion | "Who internally is advocating for this?" |

**Use when**: ACV $10K-$100K+, multiple stakeholders, 30-90 day cycle. The enterprise default.
**Why it wins**: Forces you to identify the Champion and Economic Buyer — the two people who actually decide.

### MEDDPICC (MEDDIC + Paper Process + Competition)

Adds:
- **Paper Process**: "What's your procurement/legal process? How long does contract review take?"
- **Competition**: "Who else are you evaluating? What would make you choose them?"

**Use when**: ACV > $100K, enterprise procurement, legal review required, competitive deals.
**Why it wins**: Deals die in legal/procurement. Knowing the paper process early prevents Q4 surprises.

### SPICED (Situation, Pain, Impact, Critical Event, Decision)

| Factor | Key Question |
|--------|-------------|
| Situation | "Describe your current setup." |
| Pain | "What's broken or frustrating?" |
| Impact | "What does this cost you in time/money/risk?" |
| Critical Event | "Is there a deadline or event forcing a decision?" |
| Decision | "How will you decide, and who's involved?" |

**Use when**: Consultative sales, solution-selling, when you need to deeply understand the problem before proposing. Good for early-stage companies where the sales motion is still forming.

### Framework Selection Matrix

| Your Context | Use This | Why |
|-------------|----------|-----|
| Low ACV, fast cycle, one buyer | BANT | Speed. Don't over-qualify. |
| Mid-market, 2-5 stakeholders | MEDDIC | Identifies champion + EB |
| Enterprise, procurement, legal | MEDDPICC | Paper process prevents surprises |
| Consultative, early-stage company | SPICED | Deep problem understanding |
| Founder-led sales | BANT + pain focus | Keep it simple, qualify fast |

---

## 5. Sales Methodologies — How to Sell

Qualification tells you IF a deal is real. Methodology tells you HOW to win it.

### Challenger Sale
**Core idea**: Teach the buyer something they didn't know. Reframe their problem.
- **When**: Complex products where the buyer doesn't fully understand the problem.
- **How**: Lead with insight, not product. "Most companies in your space lose 20% of pipeline to [problem]. Here's why."
- **Risk**: Requires deep domain expertise. Falls flat if the insight isn't genuinely novel.

### SPIN Selling (Situation, Problem, Implication, Need-Payoff)
**Core idea**: Ask questions in a specific sequence to lead the buyer to their own conclusion.
- **When**: The buyer needs to "discover" the pain themselves (especially when they think things are fine).
- **How**: Don't pitch — ask. "What happens when [problem] occurs?" → "How does that affect [business metric]?" → "If you could [outcome], what would that be worth?"
- **Risk**: Slow. Doesn't work when the buyer already knows what they want.

### Gap Selling
**Core idea**: Quantify the gap between current state and desired state. The gap IS the value.
- **When**: ROI-driven sales where you need to justify the investment.
- **How**: Map current state (pain, cost, inefficiency) → future state (outcomes, savings, gains) → The gap = your price justification.
- **Risk**: Requires the buyer to share detailed operational data.

### Command of the Message
**Core idea**: Control the conversation through value-based messaging.
- **When**: Competitive deals where differentiation is critical.
- **How**: Every conversation ties back to: "We do [capability] which means [benefit] so you can [outcome]."

### Methodology Selection

| Situation | Methodology |
|-----------|------------|
| Buyer doesn't know they have a problem | SPIN Selling |
| Buyer knows the problem, doesn't know the solution | Challenger Sale |
| Buyer is comparing solutions | Command of the Message |
| Buyer needs ROI justification | Gap Selling |
| Quick transactional deal | None needed — just qualify and close |

---

## 6. Pipeline Stages & Deal Mechanics

### Stage Definitions

| Stage | Entry Gate | Required Data | Probability |
|-------|-----------|---------------|-------------|
| **Discovery** | First meeting held | Pain, current solution, stakeholders | 10% |
| **Evaluation** | Confirmed fit, demo done | Requirements, timeline, budget range | 25% |
| **Proposal** | Proposal requested | Pricing, terms, decision criteria | 50% |
| **Negotiation** | Proposal reviewed, terms discussed | Redlines, approval chain, close date | 75% |
| **Verbal Commit** | Verbal yes, contract in review | Signed budget approval | 90% |
| **Closed Won** | Signature received | — | 100% |
| **Closed Lost** | Deal dead | Loss reason, competitor | 0% |

### Multi-Threading (The #1 Deal Strategy)
Deals with a single contact close at **5%**. Deals with 3+ contacts close at **25%+**.

**Rule**: Never have a single-threaded deal past Discovery.

**How to multi-thread**:
1. Ask your Champion: "Who else should be involved in evaluating this?"
2. Offer a "technical deep-dive" for the technical buyer.
3. Offer an "executive briefing" for the economic buyer.
4. Create content/resources specifically for each persona.

### Mutual Action Plans (MAPs)
For deals > $25K, create a shared document with the buyer:

| Date | Milestone | Owner | Status |
|------|-----------|-------|--------|
| Week 1 | Discovery call | Both | ✅ |
| Week 2 | Demo + technical review | Seller | |
| Week 3 | Proposal delivery | Seller | |
| Week 4 | Legal review begins | Buyer | |
| Week 5 | Contract signed | Both | |

**Why**: Creates shared accountability. Surfaces timeline risks early. Signals professionalism.

---

## 7. Objection Handling — The Framework

### The 4-Step Response Pattern
1. **Acknowledge** — "I hear you. That's a fair concern."
2. **Diagnose** — "Help me understand — is it [specific fear]?"
3. **Reframe** — Address the real concern with evidence.
4. **Advance** — "If we can solve that, what would the next step be?"

### B2B Objection Playbook

| Objection | Underlying Fear | Reframe |
|-----------|----------------|---------|
| "Too expensive" | Can't justify spend | Cost of inaction: "What does the problem cost you per month?" |
| "Not the right time" | Not a priority | "What would make it urgent?" Find the critical event. |
| "We use [Competitor]" | Switching cost | Don't attack competitor. Focus on the specific pain they can't solve. |
| "Need boss approval" | Risk aversion | "What does your boss need to see? I'll help you build the case." |
| "Works fine as-is" | Change resistance | "What does 'fine' cost you?" Quantify the gap. |
| "Can it do X?" | Technical risk | "Let me show you." Offer proof-of-concept or trial. |
| "We're too small/big" | Fit doubt | Customer story: "Company [similar size] had the same concern. Here's what happened." |
| "Let me think about it" | Unclear next step | "Of course. What specifically would you want to think through?" Surface the real blocker. |

### The "No Decision" Problem
40-60% of qualified pipelines end in "no decision" — the buyer does nothing. This is the biggest competitor, not another vendor.

**Counter-strategies**:
- Quantify the cost of delay: "Every month you wait costs $X."
- Find the critical event: "What deadline or milestone makes this urgent?"
- Reduce switching cost: "We'll handle the migration. Here's a 30-day implementation plan."
- Create urgency ethically: Time-limited onboarding support, implementation slots, price lock.

---

## 8. Forecasting

### Commit Categories

| Category | Definition | Accuracy Target |
|----------|-----------|-----------------|
| **Commit** | Will close this period. Verbal agreement. | 90%+ |
| **Best Case** | Can close if things go well. Active deal. | 50-70% |
| **Pipeline** | Qualified but early. Could slip. | 10-30% |
| **Upside** | Possible but not yet qualified. | < 10% |

### Pipeline Coverage Rule
**Target**: 3-4x pipeline coverage vs. quota.
- At 2x coverage: You need a very high win rate. Risky.
- At 3x coverage: Healthy. Room for losses.
- At 5x+: Pipeline may be bloated with unqualified deals. Audit.

### Forecast Accuracy
Track forecast vs. actual monthly. If accuracy is consistently below 80%, the problem is usually:
1. Stage definitions are unclear (reps mis-stage deals).
2. No verifiable next steps (deals are stalled but marked active).
3. Single-threaded deals (champion leaves, deal dies).

---

## 9. Post-Close — The Revenue Doesn't Stop

### Handoff to Customer Success
- Structured handoff document: what was sold, why they bought, key stakeholders, success criteria.
- Joint kickoff call: sales + CS + customer within 48 hours of close.
- 30-60-90 day success plan shared with the customer.

### Expansion Revenue
- **Net Revenue Retention > 100%** = expansion outpaces churn. This is the goal.
- Track expansion signals: seat growth, feature adoption, new departments, high NPS.
- Expansion is 5-25x cheaper than new customer acquisition.

### Win/Loss Analysis
Every deal closed-lost gets a post-mortem:
1. **Why did we lose?** (Price, competition, timing, no decision, feature gap)
2. **When did we lose?** (Which stage did the deal stall or die?)
3. **What would we do differently?** (Document for the playbook.)

Review win/loss themes quarterly. Update sales collateral accordingly.
