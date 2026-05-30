# CRM Operations Protocol

> **Goal**: Design, automate, and maintain the CRM as the revenue system of record. Covers architecture, automation workflows, data hygiene, reporting, and tool selection.

## 1. Architecture — The Revenue Stack

The CRM is not a contact database. It's the nervous system connecting marketing, sales, and CS into a unified revenue engine.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CRM (Source of Truth)                        │
│                                                                     │
│  Contacts → Lifecycle Stages → Opportunities → Revenue → Retention  │
└────────┬──────────────┬──────────────┬──────────────┬───────────────┘
         │              │              │              │
    ┌────▼────┐   ┌─────▼─────┐  ┌────▼────┐   ┌────▼────┐
    │Marketing│   │  Product   │  │ Billing │   │   CS    │
    │Automation│  │ Analytics  │  │ System  │   │Platform │
    └─────────┘   └───────────┘  └─────────┘   └─────────┘
     Lead Gen      Usage Signals   Revenue       Health Scores
     Nurture       PLG Triggers    Renewals      NPS/CSAT
     Scoring       Feature Adopt.  Expansion     Churn Signals
```

**Iron Rule**: One system of record. If data lives in two places, it will conflict. Every integration syncs TO the CRM, not FROM it.

---

## 2. CRM Selection

### Decision Framework

| Factor | Weight | What to Evaluate |
|--------|--------|-----------------|
| Integration depth | 30% | Native connections to your marketing, product, and billing tools |
| Workflow automation | 25% | Lifecycle stage automation, routing, alerts without code |
| Reporting | 20% | Pipeline, attribution, and forecast dashboards natively |
| Scalability | 15% | Contact volume, custom objects, API limits at 2-3x current scale |
| Total cost | 10% | Seats + integrations + implementation + migration |

### Platform Recommendations

| GTM Motion | Best Fit | Why | When to Outgrow |
|------------|----------|-----|-----------------|
| Founder-led (0-10 deals/mo) | **Attio, Folk, Notion CRM** | Low overhead, fast setup | When you need automation + scoring |
| PLG + sales-assisted | **HubSpot** | Strong product analytics integration, free tier, good automation | Rarely — scales well to enterprise |
| SMB sales-led | **HubSpot, Pipedrive** | Workflow automation, affordable, fast to implement | Pipedrive: when you need marketing automation. HubSpot: rarely. |
| Mid-market | **HubSpot Professional, Salesforce Essentials** | Multi-team support, reporting depth | When you need CPQ or advanced approvals |
| Enterprise | **Salesforce** | Deep customization, CPQ, approval chains, ecosystem | You don't outgrow Salesforce — you outgrow your implementation |

### Migration Principles
1. **Clean before you move** — Dedupe and purge before migration, not after.
2. **Map fields first** — Document every field mapping before touching data.
3. **Run parallel** — Operate both systems for 2-4 weeks. Validate data integrity.
4. **Automation last** — Migrate data first, rebuild automations in the new system second.

---

## 3. Data Architecture

### Contact Data Model

| Field Category | Required Fields | Why |
|---------------|----------------|-----|
| **Identity** | Email, Full Name, Company | Basic identification |
| **Firmographic** | Company Size, Industry, Revenue, Location | Fit scoring |
| **Role** | Job Title, Department, Seniority | Authority mapping |
| **Lifecycle** | Stage, Score, Source, Owner | Pipeline management |
| **Activity** | Last Activity Date, Session Count, Key Pages | Engagement signals |
| **Deal** | ACV, Stage, Close Date, Products | Revenue tracking |

### Custom Properties (Keep Minimal)
Every custom property adds complexity. Before creating one, ask:
1. "Will we report on this?" → If no, don't create it.
2. "Will we automate on this?" → If no, don't create it.
3. "Will we segment on this?" → If no, don't create it.

If none of those are yes, it's noise.

### Object Relationships

```
Company (1) ──── (Many) Contacts
Company (1) ──── (Many) Deals/Opportunities
Contact (Many) ── (Many) Deals (via Roles: Decision Maker, Champion, Influencer, Blocker)
Deal (1) ──────── (Many) Activities (calls, emails, meetings, notes)
Deal (1) ──────── (Many) Line Items / Products
```

---

## 4. Automation Workflows

### Lifecycle Stage Automations

| Trigger | Action | Purpose |
|---------|--------|---------|
| Score hits MQL threshold | Set stage = MQL, assign owner via routing rules, send alert | Speed-to-lead |
| Rep marks "Accepted" | Set stage = SQL, create Opportunity record, start SLA timer | Pipeline entry |
| Opportunity closed-won | Set stage = Customer, trigger CS handoff sequence, create onboarding tasks | Smooth transition |
| Opportunity closed-lost | Log loss reason, return contact to nurture sequence with 90-day cooldown | Win-back pipeline |
| No activity in 14 days (SQL) | Alert rep: "Lead going cold" | Prevent staleness |

### Marketing-to-Sales Automations

| Trigger | Action | Priority |
|---------|--------|----------|
| MQL created | Instant Slack + email alert with full lead context and engagement history | Critical |
| High-intent page visit (pricing, demo, competitor comparison) | Real-time alert to assigned rep | High |
| Meeting booked via scheduling tool | Notify AE, auto-enrich CRM record, create pre-meeting task | High |
| Dormant lead returns (>30 days inactive, then active session) | Alert: "Your lead [Name] is back on the site" | Medium |
| Lead watches demo video >75% | Add to SDR outreach queue | Medium |

### Deal Management Automations

| Trigger | Action |
|---------|--------|
| Deal in stage > 2x average days | Alert rep + manager: "Stale deal — update or close" |
| Deal stage advanced | Update forecast, create follow-up task for next milestone |
| Close date pushed | Require reason field, notify manager, log push count |
| Contract sent | Create "Follow up in 3 days if no response" task |
| Deal value changes >20% | Alert manager for review |

### Customer Success Automations

| Trigger | Action |
|---------|--------|
| Closed-won | Create onboarding task sequence, schedule kickoff call |
| 30 days post-close | Trigger check-in email + NPS survey |
| Usage drops >40% month-over-month | Alert CS: "At-risk account" |
| Renewal 90 days out | Create renewal opportunity, alert CS owner |
| NPS score ≤ 6 | Escalate to CS manager immediately |

---

## 5. Data Hygiene — The Unsexy Revenue Lever

Bad data costs enterprises $12.9M/year (Gartner). For startups, it silently kills pipeline.

### Deduplication

| Strategy | Implementation |
|----------|---------------|
| **Match keys** | Email (primary) + Company Domain + Phone (secondary) |
| **Merge priority** | CRM record wins. Most recent activity wins for field values. |
| **Frequency** | Weekly automated scan. Monthly manual review of edge cases. |
| **Prevention** | Block duplicate creation at form submission (email match check). |

### Required Fields Enforcement
- Block stage advancement if required fields are empty.
- Use progressive profiling — collect different fields at each interaction.
- Auto-fill where possible (enrichment APIs on lead creation).

### Enrichment Strategy

| Tool | Strength | Best For | Cost Tier |
|------|----------|----------|-----------|
| Clearbit/Breeze | Real-time enrichment, strong for tech | PLG + inbound | $$ |
| Apollo | Contact data + outbound sequences | Prospecting | $ |
| ZoomInfo | Largest B2B database, intent signals | Enterprise teams | $$$ |
| Clay | Waterfall enrichment (tries multiple sources) | Max coverage | $$ |
| LinkedIn Sales Nav | Direct access to decision-makers | Relationship selling | $$ |

**Enrichment rule**: Enrich on creation (immediate fit scoring) and re-enrich quarterly (data decays ~30%/year).

### Quarterly Data Audit Checklist
- [ ] Merge all duplicates (automated + manual edge cases)
- [ ] Validate email deliverability on contacts inactive >6 months
- [ ] Archive contacts with zero activity in 12+ months
- [ ] Audit lifecycle stage distribution — identify bottleneck stages
- [ ] Verify enrichment accuracy on 50-contact sample
- [ ] Check for contacts missing required fields at their stage
- [ ] Review and clean custom property usage (delete unused properties)
- [ ] Validate source attribution accuracy

---

## 6. Reporting Dashboards

### Three Audiences, Three Dashboards

**Marketing Dashboard** — "Are we generating qualified pipeline?"

| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| Lead volume by source | Count by UTM/channel | Channel allocation |
| MQL rate | MQLs / Total leads | Scoring quality |
| Cost per MQL | Marketing spend / MQLs | Efficiency |
| MQL-to-SQL conversion | SQLs / MQLs (target: 30-50%) | Handoff quality |
| Source-to-revenue attribution | Revenue by first-touch source | True channel ROI |

**Sales Dashboard** — "Are we converting pipeline to revenue?"

| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| Pipeline value | Sum of open opportunity amounts | Health check |
| Stage conversion rates | Deals advanced / deals entered | Where deals die |
| Win rate | Closed-won / total closed (target: 20-30%) | Deal quality |
| Average deal size | Revenue / closed-won count | Expansion signal |
| Pipeline velocity | (Deals × Size × Win Rate) / Cycle Days | Revenue per day |
| Forecast accuracy | Forecast / Actual (trailing 3 months, target: >80%) | Process maturity |

**Executive Dashboard** — "Is the business healthy?"

| Metric | Formula | Target |
|--------|---------|--------|
| CAC | Total S&M spend / new customers | — |
| LTV:CAC | Customer lifetime value / CAC | 3:1 to 5:1 |
| Revenue vs. target | Actual / Plan | >90% |
| Pipeline coverage | Pipeline / Quota | 3-4x |
| Net revenue retention | (Starting MRR + expansion - churn) / Starting MRR | >110% |
| Payback period | CAC / (ARPU × Gross Margin) | <12 months |

### Attribution Models

| Model | How It Works | Best For |
|-------|-------------|----------|
| **First-touch** | 100% credit to first interaction | Understanding top-of-funnel channels |
| **Last-touch** | 100% credit to final interaction before conversion | Understanding closing channels |
| **Linear** | Equal credit to all touchpoints | Simple multi-touch |
| **U-shaped** | 40% first, 40% last, 20% middle | Balancing acquisition + conversion |
| **W-shaped** | 30% first, 30% lead creation, 30% opportunity creation, 10% rest | B2B with long cycles |

**Rule**: No single model is correct. Run first-touch AND last-touch minimum. Compare to understand the full picture.

---

## 7. Deal Desk — Governance for Non-Standard Deals

### When to Engage Deal Desk
- ACV > $25K (or your threshold for non-standard)
- Discount > 20% of list price
- Non-standard payment terms (net-90, quarterly, milestone-based)
- Multi-year contracts with custom pricing
- Custom legal terms, SLAs, or data processing agreements

### Approval Tiers

| Deal Complexity | Approval Required | Turnaround SLA |
|----------------|-------------------|---------------|
| Standard pricing | Auto-approved | Instant |
| ≤ 20% discount | Sales manager | 24 hours |
| 20-40% discount | VP Sales | 48 hours |
| 40%+ or custom terms | Deal desk + Finance | 72 hours |
| Multi-year / enterprise | Finance + Legal | 5 business days |

### Discount Governance
- Track every discount as a percentage and dollar amount.
- Report average discount by rep, segment, and competitor.
- If >50% of deals require discounts, your list price is wrong.
- If everyone asks for the same exception, make it standard.

---

## 8. RevOps Maturity Model

| Level | Stage | Characteristics | Focus |
|-------|-------|----------------|-------|
| **0** | Chaos | Spreadsheets, no CRM, founder memory | Get a CRM. Any CRM. |
| **1** | Foundation | CRM adopted, basic pipeline tracking | Stage definitions, required fields |
| **2** | Process | Lead scoring, routing, SLAs defined | Handoff SLAs, speed-to-lead |
| **3** | Automation | Workflows run without manual intervention | Lifecycle automation, alerts |
| **4** | Intelligence | Dashboards drive decisions, attribution works | Forecast accuracy, attribution |
| **5** | Optimization | Continuous testing, predictive analytics | Pipeline prediction, churn models |

**Assessment**: Identify your current level. Invest in reaching the next level — skipping levels creates fragile systems.

---

## 9. Common Failures

| Failure | Symptom | Root Cause | Fix |
|---------|---------|-----------|-----|
| Leads go cold | High MQL volume, low SQL conversion | Slow routing, no SLA | Speed-to-lead automation |
| Pipeline is inflated | Big pipeline, low win rate | Unqualified deals entering | Tighter qualification gates |
| Forecast is unreliable | Commits don't close | No verifiable next steps | Require stage evidence |
| Reps don't use CRM | Data is stale, incomplete | Too many fields, no value to rep | Simplify. Show reps how CRM helps THEM. |
| Attribution is broken | Can't prove marketing ROI | Inconsistent UTM, no source tracking | UTM governance + mandatory source field |
| Churn is invisible | Revenue drops without warning | No usage tracking in CRM | Integrate product analytics → CRM |
