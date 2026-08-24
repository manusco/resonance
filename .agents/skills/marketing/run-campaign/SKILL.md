---
name: resonance-marketing-run-campaign
description: Marketing campaign conductor. Use when a defined outreach, nurture, newsletter, social, creative, video, or paid campaign must move from intent through specialist assets, approval, launch proposal, and outcome measurement. It may dispatch an unresolved hypothesis to GTM Thinker and an unresolved portfolio choice to Growth. It owns neither strategic decision and never auto-publishes.
archetype: orchestration
owner: marketing.campaign
activation: manual
authority: consequential
triggers:
  - plan and prepare a marketing campaign
entrypoints:
  - skill:marketing-run-campaign
negative_triggers:
  - publish or spend without approval
inputs:
  - user_request
  - plan
  - campaign_scope
  - gtm_hypothesis_decision_packet
  - growth_strategy_brief
outputs:
  - user_request
  - plan
  - artifact
  - evidence
  - decision
  - grill_scope
  - copy_scope
  - content_distribution_scope
  - lifecycle_scope
  - paid_acquisition_scope
  - analytics_scope
  - creative_scope
  - legal_scope
  - gtm_hypothesis_scope
  - growth_strategy_scope
  - gtm_thinker_scope
  - growth_scope
side_effects:
  - may_coordinate_work
  - may_write_files
write_sets:
  - project:marketing-campaign
failure_policy: stop
invokes:
  - resonance-strategy-gtm-thinker
  - resonance-strategy-growth
  - resonance-strategy-grill
  - resonance-marketing-copywriter
  - resonance-marketing-content-distribution
  - resonance-marketing-lifecycle
  - resonance-marketing-paid-acquisition
  - resonance-marketing-analytics
  - resonance-design-studio
  - resonance-ops-legal
---

# resonance-marketing-run-campaign: prepare campaigns that can survive contact

> **Role:** campaign conductor.
> **Input:** a campaign goal, audience, offer, channel, or content calendar request.
> **Output:** an approved campaign brief, channel assets, compliance checks, tracking plan, and launch proposal.
> **Definition of Done:** The campaign has one business goal, one audience, approved claims, channel-specific assets, compliance review where needed, tracking instrumentation, and a dated outcome check. Nothing is published or spent without approval.

This skill does not replace the channel specialists. It owns the campaign spine: brief, claim discipline, asset dependency order, approval, tracking, and outcome closure.

## Pipeline

1. **Strategic intake:** If the user presents one uncommitted campaign or positioning bet, dispatch `resonance-strategy-gtm-thinker`. If the user asks which growth problem or channel deserves investment, dispatch `resonance-strategy-growth`. If both decisions already exist, preserve them and invoke neither. Mentioning GTM or growth alone does not earn a dispatch. -> gate: the campaign may proceed, and the unresolved strategic owner is explicit.
2. **Brief:** define audience, offer, promise, channels, budget, constraints, and the metric that decides success. -> gate: one primary outcome and guardrails exist.
3. **Grill:** invoke `resonance-strategy-grill` on weak assumptions, audience proof, claims, and risk. -> gate: open owner questions are answered or deferred.
4. **Claims and compliance:** invoke `resonance-ops-legal` when outreach, privacy, consent, regulated claims, or contests are involved. -> gate: no high-risk claim ships without review.
5. **Message:** invoke `resonance-marketing-copywriter` for the core argument, subject lines, hooks, CTAs, and anti-slop pass. -> gate: every claim has proof or is softened.
6. **Channel plan:** invoke lifecycle, content-distribution, paid-acquisition, or analytics as needed. -> gate: channel-specific requirements are named.
7. **Creative:** invoke `resonance-design-studio` for thumbnails, social graphics, images, or video briefs. -> gate: asset specs include format, safe zones, rights, and accessibility.
8. **Measurement:** invoke `resonance-marketing-analytics` for UTMs, events, dashboard, sample window, and guardrails. -> gate: outcome check is recorded as `DONE_PENDING_OUTCOME` when proof lands later.
9. **Launch proposal:** present assets, risks, approvals still needed, and the exact publish or spend action for human consent.

## Out of Scope

- Deciding the cross-funnel growth constraint or channel portfolio.
- Approving an unvalidated GTM hypothesis.
- Replacing channel specialists.
- Publishing or spending without human approval.

## Recovery

- Audience or offer is vague -> return to Grill.
- Claim lacks proof -> rewrite or remove it.
- Compliance basis is unknown -> stop and ask for counsel or owner input.
- Tracking cannot be verified -> do not call the campaign ready.
- GTM Thinker rejects the hypothesis -> stop before asset production and return the evidence.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory; when `.resonance/ledger/` exists it is the system of record for decisions, lessons, metrics, customers, and experiments, while `02_memory.md` keeps `[lib]` notes and pointers).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
