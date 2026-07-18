# Authority Budgets and the Approval Queue

> An agent that can act unasked is a force multiplier until the day it wires the wrong refund. The fix is not to forbid action; it is to set an explicit budget for what an agent may spend, send, or commit on its own, and to route everything past the line into a batched queue the founder clears. Founder attention is the scarce input. Design for its economics.

## Contents

- [1. Why Budgets, Not Rules](#1-why-budgets-not-rules)
- [2. The Four Authority Dimensions](#2-the-four-authority-dimensions)
- [3. The Escalation Tiers](#3-the-escalation-tiers)
- [4. The Hard Stops](#4-the-hard-stops)
- [5. The Approval Queue, Not the Chat](#5-the-approval-queue-not-the-chat)
- [6. Setting a Function's Budget](#6-setting-a-functions-budget)
- [7. Budgets Are dec- Entries](#7-budgets-are-dec-entries)
- [8. Failure Modes](#8-failure-modes)

## 1. Why Budgets, Not Rules

A rule ("never send email") is too blunt: it either blocks useful work or gets waived so often it means nothing. A budget is a number: an agent may spend up to X, send to known contacts, commit up to Y of exposure, and anything past the line queues for a human. Budgets scale with trust and shrink with blast radius. They let an agent run at full speed inside a fence instead of stopping at every step to ask.

The line moves with reversibility. A cheap, reversible action gets a wide budget. An expensive or one-way action gets none: it always queues. The question is never "is this agent smart enough," it is "if this is wrong, how bad, and can we undo it."

## 2. The Four Authority Dimensions

Every action an agent might take unasked falls on one of four dimensions. Set a budget on each, per function.

- **Spend.** Money out. A per-action cap and a rolling weekly cap. "Up to 100 EUR per action, 500 EUR per week, on approved vendors only."
- **Send.** Outbound communication in the company's name. Scoped by audience and reversibility. "May send to existing customers from templates; may not send to investors, press, or new cold contacts."
- **Commit.** Promises that bind the company. Contracts, SLAs, public statements, refunds and credits. Nearly always a hard stop, because a commitment is expensive to unwind and the damage is to trust.
- **Change.** Standing configuration. Mail rules, integrations, access grants, production settings. A change persists and compounds, so it queues even when any single change looks small.

A function's authority is the four numbers together. Sales outbound might have send-to-known-contacts and zero spend. Paid acquisition might have a real spend budget and zero commit. The map (see the delegation reference) says who owns the function; the budget says how far they run alone.

## 3. The Escalation Tiers

Three tiers, sized to one founder's attention, not to a management chain.

- **Tier 0, act and log.** Inside budget on all four dimensions and reversible. The agent acts, writes what it did, and moves on. No approval. This tier is most of the work, and keeping it wide is what makes the fleet worth having.
- **Tier 1, queue and batch.** Over a budget line but reversible or bounded in damage. The agent prepares the action fully, then parks it in the approval queue. The founder clears the queue in scheduled batches, not in the moment.
- **Tier 2, stop and ask now.** A one-way door or real blast radius: money movement above the standing limit, anything in the company's public name, a production or security change, a legal commitment. The agent stops and raises it directly, with the recommendation and the cost of being wrong. Nothing at this tier ever proceeds on the agent's own say-so.

The tiers are a function of reversibility and blast radius, not of how confident the agent is. A confident agent about to wire a refund is exactly the case the tiers exist to catch.

## 4. The Hard Stops

Some actions are Tier 2 regardless of amount, because the harm is to trust or is legally binding and neither undoes cleanly:

- **Money movement out of the company.** Wires, refunds, payouts, credits above the standing per-action limit.
- **Investor and board communication.** Updates, forecasts, any number sent to people who fund the company.
- **Press, public posts, and anything in the company's public voice.**
- **Signed agreements and legal commitments.**
- **Production and security changes.** Access grants, secrets, infrastructure, data deletion.
- **Anything that touches a customer's money or personal data irreversibly.**

These do not get a budget. A skill may draft the investor update and compute the refund; it may not send the update or move the money. The split is always the same: preparation is delegated, authorization is the founder's.

## 5. The Approval Queue, Not the Chat

The wrong model is the agent interrupting the founder in chat every time it hits a line. That reintroduces exactly the attention drain delegation was supposed to remove, and it trains the founder to rubber-stamp because each item arrives alone and out of context.

The right model is a batched queue. Tier 1 actions accumulate as prepared items, each with what it is, why, the cost, and the recommendation. The founder clears the queue on a fixed cadence: a morning pass, an end-of-day pass. Batching is what protects the scarce resource. Ten decisions reviewed together in five minutes beat ten interruptions across a day, and the founder decides with the context of the whole queue instead of one item at a time. A Tier 2 stop still raises immediately; the queue is for everything short of a one-way door.

## 6. Setting a Function's Budget

For each function on the delegation map, write the four numbers before handing it off:

1. **Spend cap** per action and per week, and the approved-vendor list if any.
2. **Send scope**, the audiences and templates allowed, and the audiences that are hard stops.
3. **Commit authority**, almost always none; name the rare exceptions explicitly.
4. **Change authority**, which standing settings may move without approval, which queue.

Start tight. A new function gets a small budget, and the budget widens as the ledger shows the function acting well inside it. Trust is earned in the audit trail, not granted at setup. A budget set too wide on day one is discovered the expensive way.

## 7. Budgets Are dec- Entries

An authority budget is a settled decision, so it lives in the ledger as a `dec-` entry, not as a habit in someone's head. It is greppable, it is versioned, and it is superseded when it changes rather than quietly widened.

```
## dec-authority-sales-outbound: Authority budget for sales outbound
type: decision
created: 2026-07-10
status: active
chose: send-to-known-contacts, zero spend, zero commit
over: full send authority including cold and press
```

When a function graduates to a wider budget, supersede the entry; the old one stays as the record of what the limit was and when it moved. This matters after an incident: "what was this agent allowed to do at the time" has an exact, timestamped answer instead of an argument. A budget you widen by editing is a budget with no memory of why it grew.

## 8. Failure Modes

- **No budget, so everything asks.** Every action interrupts the founder. The fleet adds attention cost instead of removing it.
- **No budget, so everything acts.** An agent wires a refund or emails an investor unasked. The one incident that ends the trust.
- **Confidence as authority.** Letting a sure-sounding agent cross a hard stop. The tiers key on blast radius, not tone.
- **Chat instead of queue.** Approvals arriving one at a time in the moment, training the founder to rubber-stamp.
- **Budgets in someone's head.** Limits that are habits, not `dec-` entries, so they drift and cannot be audited.
- **Wide on day one.** A generous starting budget instead of an earned one, discovered when it is exercised wrong.
