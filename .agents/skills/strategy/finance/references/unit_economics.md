# Unit Economics

> Does one more customer add cash or subtract it? Answer that before you spend a dollar to acquire the next one.

## Contents

- [1. Why Unit Economics Decide Whether Scale Helps](#1-why-unit-economics-decide-whether-scale-helps)
- [2. Contribution Margin: The Foundation](#2-contribution-margin-the-foundation)
- [3. CAC: What It Really Costs to Acquire a Customer](#3-cac-what-it-really-costs-to-acquire-a-customer)
- [4. LTV: The Value of a Customer Over Time](#4-ltv-the-value-of-a-customer-over-time)
- [5. Payback Period: The Number That Governs Cash](#5-payback-period-the-number-that-governs-cash)
- [6. The LTV:CAC Trap](#6-the-ltvcac-trap)
- [7. Cohorts, Not Blended Averages](#7-cohorts-not-blended-averages)
- [8. Diagnosing Broken Unit Economics](#8-diagnosing-broken-unit-economics)
- [9. Benchmarks as Sanity Checks](#9-benchmarks-as-sanity-checks)

## 1. Why Unit Economics Decide Whether Scale Helps

A business with sound unit economics gets healthier as it grows. A business with broken unit economics gets sicker as it grows, because every new customer deepens the loss. Growth is an amplifier, not a fix. Scaling a negative contribution margin burns cash faster, it does not earn your way out.

So the sequence is fixed: prove the unit works, then pour fuel on it. Never the reverse. Unit economics are the check you run before acquisition spend, not the report you write after.

## 2. Contribution Margin: The Foundation

Contribution margin is the cash a single customer contributes after the variable costs of serving and keeping them. It is the atom everything else is built from.

```
Contribution margin (per customer, per period)
  = Revenue per customer
  - COGS per customer            (hosting, support, payment fees, delivery)
  - Variable cost to serve       (anything that scales with the customer)
```

If contribution margin is negative, stop. You are losing money on every unit, and acquiring more units accelerates the loss. No CAC or LTV analysis matters until this is positive, because LTV is built on contribution margin, not revenue. A common and expensive error is computing LTV on revenue, which pretends delivery is free.

## 3. CAC: What It Really Costs to Acquire a Customer

Customer acquisition cost is the fully loaded cost to win one new customer.

```
CAC = (Total sales + marketing spend in a period)
      / (New customers acquired in that same period)
```

Include everything that goes into acquisition, not just ad spend:
- Ad and channel spend
- Salaries of the sales and marketing team (fully loaded)
- Tools, agencies, content production, events
- Sales commissions

Two disciplines separate a real CAC from a flattering one:

- **Blended vs. paid CAC.** Blended CAC divides total spend by all new customers, including the ones who arrived organically for free. That number flatters you and will not hold as you scale, because organic does not scale linearly with spend. Track paid CAC (spend divided by customers that spend actually acquired) as the number that governs how far you can push a channel.
- **Match the cohort window.** Spend in a month often produces customers over the following months, especially in longer sales cycles. Dividing this month's spend by this month's signups misattributes both. Align the spend period to the period the customers actually landed.

## 4. LTV: The Value of a Customer Over Time

Lifetime value is the total contribution margin a customer delivers across their entire relationship, before you spent anything to acquire them.

For a recurring-revenue business:

```
LTV = (ARPA x Gross margin %) / Churn rate
```

Where:
- **ARPA** = average revenue per account per period (usually monthly)
- **Gross margin %** = so LTV is built on margin, not revenue
- **Churn rate** = the fraction of customers lost per period

The churn rate is doing enormous work in that formula, and it sits in the denominator. Small changes swing LTV violently. At 5 percent monthly churn, average customer life is 1 / 0.05 = 20 months. At 3 percent, it is 33 months, a 65 percent jump in LTV from a two-point churn improvement. This is why LTV must always be reported with the churn assumption behind it. An LTV quoted without its churn rate is a number with no spine.

Two guardrails:
- **Do not project LTV past a horizon you can defend.** A five-year LTV on a two-year-old company assumes retention you have never observed. Cap the projection at a lifetime you have evidence for, or discount distant cash to present value.
- **Use gross margin, always.** Revenue LTV overstates value by the entire cost of delivery.

## 5. Payback Period: The Number That Governs Cash

CAC payback is how many months of contribution margin it takes to earn back the cost of acquiring the customer.

```
CAC payback (months) = CAC / (ARPA x Gross margin %)
```

This is the cash-flow number, and it is the one founders most often ignore in favor of the prettier LTV:CAC ratio. Here is why it dominates: you pay CAC in cash today, up front. You earn it back slowly, month by month. The longer the payback, the more cash you must have in the bank to fund the gap while you wait, and the more a fast-growing company starves itself of cash precisely because growth is working.

- **Under 12 months** is healthy for most subscription businesses.
- **12 to 18 months** is workable if churn is low and you have the capital to fund the gap.
- **Over 18 to 24 months** is a cash-flow problem, even with a great LTV:CAC ratio. You can be "profitable per customer" and still run out of money waiting to collect.

Faster payback means each recovered dollar can immediately fund the next acquisition. Payback period, not LTV:CAC, is what determines how fast you can grow on your own cash.

## 6. The LTV:CAC Trap

LTV:CAC is the famous ratio, and the target is roughly:

```
LTV:CAC >= 3:1
```

Below 3:1 usually means you spend too much to acquire relative to what a customer is worth. Far above 3:1 (say 8:1) can mean you are underinvesting in growth and leaving the market to competitors. But the ratio lies when reported alone, in three ways:

1. **It hides payback.** A 4:1 ratio with a 24-month payback is a slow-motion cash crisis. The ratio says "healthy"; the bank account says "we run out of money in month 9". Always report payback beside the ratio.
2. **It rests entirely on the churn assumption.** LTV is a function of churn, and churn is the hardest number to know early. Flatter the churn assumption and the ratio inflates automatically. A 3:1 built on aspirational churn is a fiction with a decimal point.
3. **It uses revenue instead of margin.** A revenue-based LTV:CAC of 3:1 on a 40 percent gross-margin business is really 1.2:1 in cash. The ratio looks fine and the unit loses money.

The rule: never present LTV:CAC as a standalone number. Present the triplet: **LTV:CAC, CAC payback in months, and the churn rate behind LTV.** Any one of the three without the other two is a way to fool yourself and, worse, to fool yourself into scaling.

## 7. Cohorts, Not Blended Averages

Blended averages hide everything that matters. If half your customers churn in month two and half stay for years, the blended average tells a comforting middle story that describes no actual customer and hides the leak.

Measure by cohort: group customers by the month they first paid, then track each group's retention and revenue over time. Cohorts reveal:
- **Whether retention is improving.** Are newer cohorts sticking better than older ones? That is product-market fit strengthening. The reverse is a warning the blended number will not show for months.
- **Where the drop-off is.** A cliff in month one is an onboarding problem; a slow bleed is a value problem. Different fix, different team.
- **True LTV.** Actual cohort retention curves beat a formula that assumes constant churn, because real churn is high early and flattens later.

The signature of product-market fit is a retention curve that flattens to a plateau, not one that decays to zero. A high day-one number that vanishes by day 90 is churn wearing makeup.

## 8. Diagnosing Broken Unit Economics

When the unit does not work, isolate the failing term rather than flailing at all of them:

- **CAC too high?** The channel is saturated or mistargeted, or the funnel converts poorly. Fix targeting and conversion before adding spend. Sometimes the answer is a cheaper channel, not a better ad.
- **LTV too low?** Either churn is high or ARPA is low. High churn is a retention and product problem (delegate the loop and retention design to growth). Low ARPA is a pricing and packaging problem (delegate to venture's pricing work). Diagnose which before prescribing.
- **Payback too long?** Even with a fine ratio, a long payback is a cash problem. Options: raise prices, collect annually up front (pulls cash forward), or shift to cheaper acquisition channels.
- **Contribution margin negative?** The most urgent case. The cost to serve exceeds revenue. Fix pricing or cost of delivery immediately, and stop acquiring until it is positive. Every new customer is making it worse.

The discipline: name the single failing metric, trace it to its cause, and prescribe the fix for that cause. Do not recommend "improve unit economics" as if it were one lever.

## 9. Benchmarks as Sanity Checks

Benchmarks are for smell-testing your own numbers, not targets to game. They vary by model and stage, so treat them as rough ranges.

| Metric | Rough healthy range | Notes |
| :--- | :--- | :--- |
| LTV:CAC | 3:1 and up | Report with payback and churn, never alone |
| CAC payback | Under 12 months | 12 to 18 workable with low churn and capital |
| Gross margin (software) | 70 to 90% | Services and hardware run much lower |
| Monthly churn (SMB) | 3 to 5% | Enterprise far lower, consumer often higher |
| Monthly churn (enterprise) | Under 1 to 2% | Annual contracts change the picture |
| Net revenue retention | 100% and up | Above 100% means expansion outruns churn |

Net revenue retention (NRR) is the underrated one: it measures revenue from existing customers over time including expansion, upgrades, and churn. Above 100 percent means your existing base grows on its own even with zero new customers, which is the strongest signal in the whole set. It means the bucket fills faster than it leaks.
