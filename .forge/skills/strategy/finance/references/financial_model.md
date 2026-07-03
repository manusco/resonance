# Driver-Based Financial Model

> A model is a set of assumptions made explicit. Build the top line from drivers, not from a number you typed in.

## Contents

- [1. The Rule: Everything Traces to a Driver](#1-the-rule-everything-traces-to-a-driver)
- [2. Building Revenue From Drivers](#2-building-revenue-from-drivers)
- [3. The Cost Structure](#3-the-cost-structure)
- [4. Gross Margin and Contribution](#4-gross-margin-and-contribution)
- [5. Burn and Runway](#5-burn-and-runway)
- [6. The Three Statements, Simplified](#6-the-three-statements-simplified)
- [7. Scenarios, Not Point Forecasts](#7-scenarios-not-point-forecasts)
- [8. Pressure-Testing the Model](#8-pressure-testing-the-model)
- [9. Common Modeling Errors](#9-common-modeling-errors)

## 1. The Rule: Everything Traces to a Driver

A driver is an input you can change and defend. Customers, price, conversion rate, average order value, headcount, salary. The model computes outputs from drivers. If a cell contains a number that is neither a driver nor a formula referencing drivers, delete it and rebuild it.

The test: point at any number in the model and ask "what makes this move?". If the answer is a named input with a stated assumption, the cell is sound. If the answer is "I estimated it", it is a wish.

Separate the three layers visually:
- **Assumptions** (drivers you set): one clearly marked area, every input in one place.
- **Calculations** (formulas): reference the assumptions, never hardcode.
- **Outputs** (the statements): the revenue, burn, and runway that fall out.

Change one assumption, and every dependent number updates. That is the whole point.

## 2. Building Revenue From Drivers

Never type a revenue number. Compose it. Two dominant patterns:

**Bottom-up (build from your own funnel).** You control the inputs, so this is the honest one.

```
Leads per month
  x  Lead-to-customer conversion rate
  =  New customers per month
  x  Average revenue per customer
  =  New revenue per month
```

For recurring revenue, the model is a stock that accumulates and leaks:

```
Starting MRR
  + New MRR (new customers x ARPA)
  + Expansion MRR (upgrades, seat growth)
  - Churned MRR (cancellations x ARPA)
  - Contraction MRR (downgrades)
  =  Ending MRR
```

ARPA is average revenue per account. MRR is monthly recurring revenue; ARR is MRR times 12. Net new MRR is the sum of the four movements above, and it is the single most important line in a subscription model: if it is negative, the business is shrinking even while it signs new logos.

**Top-down (market share of a sized market).** Weaker, because a percentage of a big number is easy to assert and hard to defend. Use it only as a sanity ceiling on the bottom-up build, never as the primary forecast. "We will capture 1% of a huge market" is the oldest unfunded story in the room.

## 3. The Cost Structure

Split costs by behavior, because behavior is what determines whether growth helps or hurts.

| Type | Definition | Examples | Scales with |
| :--- | :--- | :--- | :--- |
| **COGS** | Cost to deliver the product to a paying customer | Hosting per user, payment fees, support, delivery | Revenue / usage |
| **Variable** | Rises with volume but is not delivery | Sales commission, per-unit shipping | Volume |
| **Fixed** | Committed regardless of volume | Salaries, rent, software licenses, insurance | Time |

For most software companies, salaries dominate. Payroll is usually 60 to 80 percent of total burn, so headcount plan and hiring timing are the biggest levers in the whole model. Model each hire by start month and fully loaded cost (salary plus taxes, benefits, and overhead, often 1.2 to 1.4 times base). Do not model a lump "team cost"; model people, because you hire and pause people, not lumps.

## 4. Gross Margin and Contribution

Two margins, two different questions.

**Gross margin** answers "how much of each revenue dollar survives the cost of delivering it".

```
Gross profit = Revenue - COGS
Gross margin % = Gross profit / Revenue
```

Software typically runs 70 to 90 percent gross margin. A service business runs far lower because human delivery time is COGS. A marketplace's margin depends on take rate. Gross margin sets the ceiling on everything: a 20 percent gross margin business cannot spend like an 80 percent one, no matter the growth rate.

**Contribution margin** answers "does one more customer add or subtract cash, after the cost to serve and the variable cost to acquire and keep them". It is the unit-level version and it decides whether scaling is safe. A negative contribution margin means every new customer widens the loss. Full treatment of contribution margin at the unit level lives in the unit economics reference; here it is enough to know the model must surface it.

## 5. Burn and Runway

The two numbers that decide whether the company is alive next year.

**Gross burn** is total cash out per month. **Net burn** is cash out minus cash in.

```
Net monthly burn = Cash spent - Cash collected   (per month)
Runway (months) = Cash in bank / Net monthly burn
```

Runway is a date. Cash in bank divided by net burn gives the number of months, and the calendar tells you when the money runs out. Write that date down. Every plan is measured against it.

Watch for the difference between revenue and cash. Revenue is booked when earned; cash arrives when the customer pays. If you invoice net-60, you recognize revenue two months before the cash lands, and burn is about cash. Annual prepaid contracts do the opposite: cash arrives up front, revenue recognizes over 12 months. Model the cash timing, not just the revenue timing, because you pay salaries in cash.

Three burn disciplines:
- Plan to raise or reach profitability with **6 or more months of runway remaining**. Raising with two months left destroys your negotiating position.
- Watch **burn multiple** = net burn divided by net new ARR. Below 1 is efficient; above 2 means you are buying growth expensively; above 3 is a warning.
- Know your **default alive vs. default dead** status: at current growth and burn, do you reach profitability before the cash runs out on the existing balance? If dead, the plan must change now, not at the next board meeting.

## 6. The Three Statements, Simplified

You do not need audited statements to run a company, but you need the logic of all three.

- **Profit and loss (P&L)**: revenue minus costs over a period. Tells you if the business model works. Can show a profit while the bank account empties (if customers pay late).
- **Cash flow**: actual money in and out. Tells you if you survive. This is the one that kills companies. A profitable P&L with negative cash flow still goes bankrupt.
- **Balance sheet**: what you own and owe at a point in time. Cash, receivables, debt, equity. For an early company, the line that matters is cash.

The trap: profit is an opinion (it depends on when you recognize revenue and costs), cash is a fact. Manage to cash.

## 7. Scenarios, Not Point Forecasts

A single forecast is precisely wrong. Build three cases off the same driver structure by flexing the key assumptions (usually conversion, ARPA, churn, and hire timing):

- **Base**: your honest expectation. What you actually believe.
- **Downside**: growth is slower, churn is higher, the raise slips a quarter. Does the company survive? This case sets how much cash you truly need.
- **Upside**: things work. Where do you need capacity, and what breaks first?

The downside case is the important one. It answers the only question that matters when cash is tight: how bad can it get before we die, and what is the trigger to act.

## 8. Pressure-Testing the Model

Before anyone trusts a model, attack it:

- **Trace the top line.** Pick the revenue number 12 months out. Decompose it to drivers. If it requires a conversion rate or growth rate you have never hit and cannot justify, the model is fiction.
- **Sanity-check the hockey stick.** A curve that bends sharply upward must have a mechanism. New channel, new product, seasonality. If the line goes up because the spreadsheet grows a percentage every month with no cause, that is a wish.
- **Check the implied efficiency.** Back out CAC, payback, and burn multiple from the model. If it implies world-class efficiency you have not demonstrated, fix the assumptions.
- **Reconcile to actuals.** If you have real months, the model's recent past must match what happened. A model that cannot reproduce last quarter cannot predict next year.
- **Find the load-bearing assumption.** Usually one or two drivers move the outcome more than all the others. Name them, because those are what you must get right and what an investor will probe.

## 9. Common Modeling Errors

- **Hardcoded revenue.** A typed-in top line with no drivers. The cardinal sin.
- **Straight-line everything.** Real businesses have seasonality, ramp time on new hires, and lag between spend and result. A model with no ramps overstates near-term results.
- **Forgetting churn.** Adding new customers every month while assuming none leave. Every recurring model must leak.
- **Cash equals revenue.** Ignoring payment timing. You can be profitable on paper and insolvent in the bank.
- **Fully loaded costs ignored.** Modeling salary but not the 20 to 40 percent on top for taxes, benefits, and overhead.
- **One scenario.** No downside case, so no answer to "what if it goes wrong".
- **Vanity top line.** Modeling cumulative signups or gross bookings instead of active revenue and net burn.
