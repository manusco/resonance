# The Agent Delegation Map: which skill owns which function

> A company is a set of functions, and Resonance already has a specialist for most of them. The founder's job is not to do each function. It is to own the outcome, hand the function to the right skill, and hold the authority line. This map says who owns what so work routes without a meeting.

## Contents

- [1. The Principle: Own the Outcome, Delegate the Function](#1-the-principle-own-the-outcome-delegate-the-function)
- [2. The Map](#2-the-map)
- [3. Reading the Map in a Weekly Review](#3-reading-the-map-in-a-weekly-review)
- [4. One Owner Per Function](#4-one-owner-per-function)
- [5. What the Founder Never Delegates](#5-what-the-founder-never-delegates)
- [6. When No Skill Owns It](#6-when-no-skill-owns-it)
- [7. Failure Modes](#7-failure-modes)

## 1. The Principle: Own the Outcome, Delegate the Function

Delegation is not "make it someone else's problem." It is: name the outcome, name the owner, set the authority the owner has to act unasked, then inspect the result on the cadence. The founder still owns the number. The skill owns the work that moves it.

A function without a named owner defaults to the founder, which means it defaults to whatever the founder happened to notice this week. The map exists so nothing important lives in that gap.

## 2. The Map

Each business function routes to the Resonance skill that carries its expertise. The KPI-tree node in the last column is the metric the founder inspects to know the function is working.

| Function | Owning skill(s) | Founder inspects |
| :--- | :--- | :--- |
| New revenue, pipeline | `resonance-sales-revops`, `resonance-sales-pipeline` | Pipeline coverage, stage velocity, closed new MRR |
| Outbound, lead generation | `resonance-sales-outbound-sequence`, `resonance-sales-lead-ops`, `resonance-sales-account-intelligence` | Qualified meetings booked, reply rate |
| Retention, expansion | `resonance-success-customer-success` | Gross retention, net expansion, churn by cohort |
| Product direction, roadmap | `resonance-ops-product` | Activation rate, feature adoption, roadmap-to-outcome |
| Growth loops, funnel | `resonance-strategy-growth`, `resonance-marketing-conversion` | Signup conversion, loop coefficient |
| Lifecycle, retention marketing | `resonance-marketing-lifecycle` | Activation nudges, reactivation rate |
| Paid acquisition | `resonance-marketing-paid-acquisition` | CAC, paid payback, channel mix |
| SEO and organic | `resonance-marketing-seo` | Qualified organic traffic, ranked pages |
| Finance, runway, the raise | `resonance-strategy-finance` | Runway in months, burn, unit economics |
| Hiring | `resonance-people-hiring` | Open roles filled, scorecard pass rate |
| Legal, contracts, terms | `resonance-ops-legal` | Contract turnaround, open legal risks |
| Incidents, reliability | `resonance-ops-incident`, `resonance-ops-observability` | Time to mitigate, incident count |
| Engineering delivery | `resonance-engineering-build`, `resonance-ops-qa` | Slice throughput, checks green |

The map is not exhaustive and it does not need to be. It covers the functions a founder-run company actually spends attention on. When a real function is missing a row, add it in a decision, do not improvise around it.

## 3. Reading the Map in a Weekly Review

The map and the KPI tree are the same object seen from two sides. The tree says which metric matters; the map says which skill owns moving it. In the weekly review, a red node points at exactly one owning skill, and the drilldown becomes: what is that skill's plan to move this number, and does it have the authority to run the plan without waiting on me.

This is what keeps the review from turning into the founder personally solving every function. A red retention node is a `resonance-success-customer-success` question, not a founder-does-it-tonight question. The founder decides, the skill executes.

## 4. One Owner Per Function

Every function has exactly one owning skill of record, even when several skills touch it. Outbound involves account intelligence, sequences, and lead ops, but `resonance-sales-outbound-sequence` owns the outcome number; the others feed it. Shared ownership of an outcome means each owner assumes the other has it, and the number sits still.

When two skills genuinely overlap, name the owner of the metric and make the others contributors. The owner is the one the weekly review asks when the number is off.

## 5. What the Founder Never Delegates

Some functions can be informed by a skill but the decision stays with the founder, always:

- **Money movement.** Wires, refunds above the standing limit, payouts. A skill can prepare and recommend; the founder authorizes. See the authority-budgets reference.
- **External commitments in the company's name.** Investor updates, press, signed contracts, public commitments. A skill drafts; the founder sends.
- **Hiring and firing decisions.** `resonance-people-hiring` runs the process and recommends; the yes or no is the founder's.
- **Company direction.** The OKR cascade, the north-star, a pivot. Skills execute the strategy; they do not set it.

These are the founder's job by definition. A delegation map that hands them off is not delegation, it is abdication.

## 6. When No Skill Owns It

Some functions have no Resonance specialist. Office space, a specific vendor negotiation, a founder's own network relationship. For these, the map's job is to make the gap explicit: this function is founder-owned, no skill, and here is the cadence I will inspect it on. An un-owned function is fine as long as it is named. An un-owned function nobody noticed is how a company gets surprised.

Do not stretch a skill to cover a function it does not fit just to fill a row. A forced owner is worse than a named gap, because the review will trust it and the trust is misplaced.

## 7. Failure Modes

- **Founder as the owner of everything.** Every function defaults up because none was assigned. The company runs at the speed of one person's attention.
- **Shared outcome ownership.** Two skills on one number, so neither moves it.
- **Delegating the undelegatable.** Handing money movement or investor comms to a skill to act unasked. These need human authorization every time.
- **Forced ownership.** Assigning a function to a skill that does not fit, so the review trusts a plan that was never real.
- **Silent gaps.** A function with no owner and no one aware of it, discovered only when it fails.
