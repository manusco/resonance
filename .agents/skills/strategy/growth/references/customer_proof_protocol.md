# Customer Proof Protocol

> **Goal**: Source, rank, and deploy approved customer proof for campaigns, decks, emails, and sales conversations. Covers proof discovery, relevance ranking, story drafting, and approval chain management.

## 1. What Counts as Customer Proof

Customer proof is any evidence from real customers that supports your claims. It comes in tiers of credibility:

| Tier | Type | Credibility | Usage |
|:---|:---|:---|:---|
| **1 — Hard proof** | Named case study with metrics, published with customer approval | Highest | Landing pages, sales decks, keynotes |
| **2 — Attributed proof** | Named quote with permission, no full case study | High | Email sequences, blog posts, social proof sections |
| **3 — Anonymous proof** | "A Fortune 500 fintech company" with metrics, no name | Medium | Conference talks, sales conversations, competitive battles |
| **4 — Aggregate proof** | "87% of our customers report..." | Medium | Product marketing, website hero copy |
| **5 — Indirect proof** | Customer logos on website (permission granted) | Low | Trust signals, landing pages |

**Rule**: Higher tiers always beat lower tiers. Never use Tier 3+ when Tier 1-2 is available for the same claim.

---

## 2. Proof Sourcing — Where to Find It

### Internal Sources (Search First)

| Source | What It Contains | Access Pattern |
|:---|:---|:---|
| Customer content library | Approved stories, quotes, metrics, logos | Search by industry, use case, segment |
| CRM account notes | Deal context, success metrics, champion quotes | Search by account, segment, ACV |
| CS/AM meeting notes | Informal proof, satisfaction signals, expansion stories | Search by account, recency |
| NPS/CSAT responses | Verbatim quotes with scores | Search by score threshold, recency |
| Support tickets (resolved) | Before/after transformation stories | Search by resolution type, satisfaction |

### External Sources (Secondary)

| Source | What It Contains | Caveat |
|:---|:---|:---|
| G2/Capterra reviews | Public customer opinions with company names | Verify the review is from a real customer, not a prospect |
| LinkedIn posts | Customer mentions, organic advocacy | Must get permission before using in sales/marketing materials |
| Conference recordings | Customer talks, panels, presentations | Check recording rights and customer permission |

**Rule**: Internal approved sources always take priority. External sources require verification and permission before deployment.

---

## 3. Relevance Ranking

When multiple proof assets match, rank by:

| Dimension | Weight | How to Score |
|:---|:---|:---|
| **Audience fit** | 30% | Same industry, company size, role, or use case as the target |
| **Recency** | 25% | Proof from the last 12 months scores highest. Over 24 months: deprioritize. |
| **Specificity** | 20% | Concrete metrics beat vague praise. "$2M saved" beats "great product." |
| **Approval status** | 15% | Fully approved for external use scores highest. Pending approval: flag, don't use. |
| **Credibility tier** | 10% | Higher tier (see Section 1) scores higher. |

**Output**: Return the top 3-5 matches ranked by composite score. Include for each:
- What the proof says (headline + key metric or quote)
- Why it matches (which audience/use case/segment it fits)
- Approval status (approved / pending / needs re-approval)
- Restrictions (channel limits, expiration dates, geography limits)
- Source reference (where the proof lives)

---

## 4. Story Drafting

### Two Formats

**Narrative Story** (for blog posts, campaign assets, long-form content):
1. The person and their role
2. The business problem (specific, not generic)
3. What they tried before (the "old way")
4. The workflow or solution they built
5. The product's role in the workflow (honest, not inflated)
6. Outcomes with evidence (metrics, quotes, timeline)
7. What's next

**Metric-Forward Story Page** (for landing pages, product marketing, sales enablement):
1. Headline metric (the single most impressive number)
2. Company context (1-2 sentences)
3. Challenge (2-3 sentences)
4. Solution (2-3 sentences, specific workflows)
5. Results (3-5 metrics with before/after)
6. Pull quote from the champion

### Drafting Rules

- Use the customer's actual words when quoting. Tighten for clarity but preserve meaning.
- Separate verified claims from claims that need verification. Use `[VERIFY: claim]` markers.
- Never invent quotes, metrics, timelines, tools, or approval status.
- Label uncertain details explicitly: `[UNVERIFIED]`, `[NEEDS CUSTOMER APPROVAL]`.
- Include a review checklist at the end of every draft:
  - [ ] Quotes verified with original source
  - [ ] Metrics cross-checked against data source
  - [ ] Customer approval obtained for external use
  - [ ] Brand/legal review completed
  - [ ] Publication channel and date confirmed

---

## 5. Approval Chain

Customer proof involves multiple stakeholders. No shortcutting the chain.

| Approver | What They Check | When to Engage |
|:---|:---|:---|
| **Customer champion** | Accuracy of claims, comfort with attribution | Before any external use |
| **Customer legal/comms** | Brand usage, metric disclosure, NDA compliance | For named case studies and metric claims |
| **Internal brand** | Tone, visual guidelines, messaging consistency | Before publication |
| **Internal legal** | Competitive claims, regulatory compliance, testimonial rules | For claims about competitors or regulated industries |
| **Sales enablement** | Relevance to current pipeline, freshness, talk track accuracy | Before adding to sales decks or sequences |

### Approval Status Tracking

Every proof asset should have a status:

| Status | Meaning |
|:---|:---|
| **Approved** | Cleared for external use on specified channels |
| **Pending** | Submitted for review, not yet cleared |
| **Expired** | Approval window has closed, needs re-approval |
| **Restricted** | Approved for specific channels/uses only |
| **Declined** | Customer or legal denied permission |

**Rule**: Never use proof with a status other than "Approved" in external-facing materials. Pending proof can be used in internal sales conversations with a disclosure: "This story is pending final approval."

---

## 6. Common Failures

| Failure | Symptom | Fix |
|:---|:---|:---|
| Stale proof | Metrics from 3 years ago, customer has since churned | Set expiration dates on all proof assets. Re-verify quarterly. |
| Fabricated proof | "Companies like yours see 10x improvement" with no source | Require a source reference for every metric. No source = no claim. |
| Unapproved names | Customer logo on website without permission | Audit logo wall quarterly. Remove expired approvals. |
| One-size-fits-all | Same case study used for every prospect regardless of fit | Rank by relevance (Section 3). Irrelevant proof is worse than no proof. |
| Quote distortion | Customer said "it's pretty good" → published as "revolutionary" | Keep the original verbatim. Tighten for clarity, never inflate. |
