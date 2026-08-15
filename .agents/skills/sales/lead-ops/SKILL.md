---
name: resonance-sales-lead-ops
description: Audits lead lifecycle quality, resolves ownership, maps the customer experience from form fill to follow-up, and generates daily watchlists. Use when asked to audit lead handling, find missed follow-ups, resolve lead owners, map inbound CX, or build a daily lead operating view.
archetype: procedure
---

# /resonance-sales-lead-ops: no lead left behind

> **Role:** resonance-sales
> **Input:** A lead cohort (CRM filter, date range, source, or specific lead IDs) + CRM access.
> **Output:** A lead treatment audit report with severity classifications, owner resolutions, CX maps, and recommended actions.
> **Definition of Done:** Every audited lead has a treatment classification, an owner resolution with provenance, a CX timeline, and a recommended next action. No inferred owners from timeline activity alone. No auto-escalation. Free of AI slop and em dashes. Passed the validator.

## Prerequisites (fail fast)

- [ ] A lead cohort and source window are defined (which leads, from when).
- [ ] CRM access is available to read contact, company, deal, outreach, and meeting data.

## Algorithm

Copy this checklist and tick items as you go.

### Job 1: Lead Treatment Audit

1. **Define the Cohort**: Identify the leads to audit by source, date range, lifecycle stage, or ad-hoc list. Confirm the audit window (e.g., "all MQLs from the past 7 days"). → verify: cohort is bounded, not open-ended.

2. **Review Each Lead's Treatment**: For every lead in the cohort, inspect:
   - CRM owner assignment and timestamp
   - Outreach timeline (emails, calls, LinkedIn, meetings)
   - Automation touches vs. real human follow-up
   - Meeting status (booked, held, no-show, rescheduled)
   - Relevant conversation evidence (notes, chat threads)
   → verify: automated touches are distinguished from manual human outreach.

3. **Classify Treatment Quality**: Assign each lead exactly one classification:

   | Classification | Definition |
   |:---|:---|
   | **Manual** | A human rep made direct, personalized outreach |
   | **Automated** | Only automation sequences touched the lead |
   | **Mixed** | Both automation and human outreach occurred |
   | **Missing** | No outreach of any kind within the SLA window |
   | **Stale** | Outreach happened but stopped before a meeting or resolution |

   → verify: every lead has exactly one classification.

4. **Assign Severity and Diagnosis**: For leads classified as Missing, Stale, or Automated-only, assign a severity:

   | Severity | Criteria |
   |:---|:---|
   | **P0 Critical** | High-intent lead (demo request, pricing visit) with zero human outreach within SLA |
   | **P1 High** | MQL with delayed outreach (>24h for high-intent, >48h for standard) |
   | **P2 Medium** | Lead received outreach but follow-up sequence stalled before resolution |
   | **P3 Low** | Low-intent lead with adequate automation coverage |

   → verify: severity correlates with intent signal strength, not just volume.

### Job 2: Owner Resolution

5. **Resolve the Owner**: For each lead, determine the authoritative owner using this strict fallback path:
   1. Contact owner (primary)
   2. Company owner (if contact owner is missing)
   3. Deal owner (if company owner is missing)
   4. None assigned

   Enrich the owner record with: segment, team, manager, and account size where available. → verify: no owner is inferred from timeline activity alone. Every owner resolution has a stated provenance ("Contact owner: Jane Smith, assigned 2024-03-15").

### Job 3: Customer Experience Map

6. **Map the CX Timeline**: For each audited lead, reconstruct the experience in plain language:
   - Source event (form fill, demo request, hand-raiser, event registration)
   - Routing path (how the lead was assigned, time-to-assignment)
   - Outreach sequence (what happened, when, by whom)
   - Meeting outcome (booked, held, no-show, rescheduled, none)
   - Current status and next expected action
   → verify: the CX map reads as a narrative, not a data dump.

7. **Distinguish Cycles**: Do not count historical meetings from prior cycles as current-cycle success. A lead that had a meeting 6 months ago and raised their hand again is a new cycle. → verify: only current-cycle activity is used for treatment scoring.

### Job 4: Daily Watchlist

8. **Generate the Watchlist**: Produce a daily operating view containing:
   - Priority leads that need immediate attention (P0/P1)
   - Leads with meetings today or this week
   - Leads where follow-up has stalled (>48h since last touch)
   - Blockers (unassigned leads, missing contact info, ownership conflicts)
   - Recommended actions per lead (specific, not generic)
   → verify: the watchlist is actionable in under 2 minutes of reading.

## Recovery

- CRM data is incomplete for a lead → audit what is available. Flag gaps explicitly: `[MISSING: outreach history]`, `[MISSING: meeting status]`. A partial audit with honest gaps beats skipping the lead.
- Owner resolution hits "None assigned" → flag as P0 immediately. Recommend assignment based on territory, segment, or round-robin logic.
- Historical cycle data is mixed with current cycle → ask ONE clarifying question about the current cycle start date. Do not silently merge cycles.
- Tried to produce the audit 3 times with conflicting data → stop, output the conflicts explicitly, recommend a data hygiene pass, escalate.

## Cognitive Frameworks

### Speed-to-Lead
Response time is the single highest-leverage variable in lead conversion. Under 5 minutes = 21x more likely to qualify. Over 24 hours = the lead is effectively cold. Every hour of delay is measurable revenue loss.

### The Treatment Spectrum
Not all leads need the same treatment. High-intent leads (demo requests, pricing page repeat visitors) need human outreach within the SLA. Low-intent leads (content downloads, newsletter signups) can live in automation. The audit classifies so the team allocates effort correctly.

### Ownership Provenance
"Who owns this lead?" is one of the most common CRM disputes. The fallback path (contact → company → deal → none) is not arbitrary. Contact owner is the most specific signal. Company owner is the most stable. Deal owner is the most commercially relevant. The fallback path uses specificity first, then stability, then commercial relevance.

### The Approval Gate Pattern
Lead ops recommendations (owner reassignment, escalation, process changes) are recommendations, not auto-actions. The workflow:
1. Agent audits the cohort and produces findings.
2. Ops lead reviews the findings and recommended actions.
3. Ops lead approves owner changes, escalations, or process updates.
4. Changes are logged with attribution and timestamp.

## Reference Library

- **[CRM Operations](references/crm_operations_protocol.md)**: CRM architecture, automation workflows, data hygiene, and reporting dashboards.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory, `.resonance/02_memory.md`, which loads at session start).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
