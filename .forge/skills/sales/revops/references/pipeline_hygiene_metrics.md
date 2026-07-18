# Pipeline Hygiene and Funnel Metrics

> A forecast is only as honest as the stage data under it. Wrong close dates, stale stages, and phantom pipeline are not a reporting annoyance, they are a decision poison: you staff, forecast, and spend against a lie. Stage hygiene is the cheapest revenue lever there is.

## Contents

- [1. Stage Conversion: Where Deals Die](#1-stage-conversion-where-deals-die)
- [2. Sales Cycle: Measure the Median](#2-sales-cycle-measure-the-median)
- [3. Pipeline Velocity: Revenue Per Day](#3-pipeline-velocity-revenue-per-day)
- [4. Leakage: The No-Decision Loss](#4-leakage-the-no-decision-loss)
- [5. Aging and Stalled Deals](#5-aging-and-stalled-deals)
- [6. The Cost of Bad Data](#6-the-cost-of-bad-data)
- [7. The Hygiene Routine](#7-the-hygiene-routine)

## 1. Stage Conversion: Where Deals Die

Stage conversion is the share of deals that advance from one stage to the next.

```
Stage conversion rate = Deals that advanced from stage N / Deals that entered stage N
```

Cohort it by the period a deal entered the stage, so you compare like with like. The conversion curve tells you where deals die, and the cause differs by location:

- A cliff early (SAL to Stage 1) is a qualification problem: you are accepting leads that were never real opportunities.
- A cliff late (Stage 3 to close) is a closing or pricing problem: real deals stall at the end.

Do not average the funnel into one win rate and stop there. The single number hides the stage that is actually leaking.

## 2. Sales Cycle: Measure the Median

Sales cycle is the time from opportunity created (or SQL) to closed won.

```
Sales cycle = median days from opportunity created to closed won
```

Use the median, not the mean. A handful of monster deals that took a year will drag the mean and make you plan around a cycle no typical deal has. The median is the deal in the middle, which is the one you actually forecast against.

## 3. Pipeline Velocity: Revenue Per Day

Velocity is the master metric of a funnel because it combines the four things you can change into one number: revenue per day.

```
Pipeline velocity = (Number of qualified opps x Win rate x Average deal size) / Sales cycle length in days
```

The four levers, and the trap:

- **More qualified opps:** raises velocity, if quality holds.
- **Higher win rate:** better qualification and closing.
- **Bigger deals (ACV):** move upmarket or expand the offer.
- **Shorter cycle:** remove friction in the process.

The trap is pushing one lever and quietly breaking another. Stuffing the top with unqualified opps raises the opp count and drops the win rate, and velocity can fall while the pipeline "grows." Read the four levers together, never one alone.

## 4. Leakage: The No-Decision Loss

Not every lost deal is lost to a competitor. Many die of no decision: the buyer does nothing. Track it separately.

```
Closed lost = competitive loss + no-decision loss
```

A high no-decision rate is a qualification problem wearing a closing costume. The deals were never real: no compelling event, no economic buyer, no budget. The fix is upstream, at the exit criteria for the qualified stages (see funnel_definitions.md), not in closing tactics. Reps cannot close a deal the buyer was never going to make. Measuring no-decision separately is what tells you the problem is qualification, not talent.

## 5. Aging and Stalled Deals

A deal that sits in a stage far past that stage's normal age is a stalled deal, and a stalled deal in the forecast is a lie waiting to be found.

```
Flag as stalled when: days in stage > about 1.5x to 2x the stage's median age
```

Alert on it, inspect it, and force a decision: advance it with real evidence, push it with a reason, or close it lost. What you cannot do is leave it sitting open inflating your pipeline. Stalled deals are the raw material of phantom pipeline.

## 6. The Cost of Bad Data

Bad funnel data does not stay in the report. It flows into every decision downstream:

- **Wrong close dates** wreck the forecast, because the forecast is built by close date.
- **Stale stages** overstate progress, so weighted pipeline lies.
- **Phantom pipeline** (dead deals still marked open) inflates coverage, so you think you are covered when you are not, and you under-source.
- **Missing fields** hide the exit-criteria evidence, so nobody can inspect a commit.

The chain is the point: you staff capacity, set coverage, and commit a forecast on top of this data. Poison at the bottom is poison all the way up. This is why stage hygiene is not busywork for reps, it is the foundation the entire revenue plan stands on, and it is nearly free compared to the cost of a missed quarter you did not see coming.

## 7. The Hygiene Routine

Make hygiene a system, not a nag:

- **Required fields to advance.** Block a stage change until the exit-criteria fields are filled. The system enforces the definition so a manager does not have to.
- **Close-date discipline.** A pushed close date requires a reason and increments a push counter. Reps who push the same deal four times are telling you something.
- **Aging alerts.** Auto-flag deals past the stalled threshold to the rep and manager.
- **The weekly scrub.** A standing pass to close phantom deals, fix dates, and clear stale stages before the forecast call reads from the data.
- **One definition of every metric.** Win rate, cycle, velocity, and each stage mean one thing across marketing and sales. Two definitions of win rate is two teams arguing about which lie is correct.

Hygiene is unglamorous and it is the cheapest revenue you will ever find. A clean funnel forecasts itself; a dirty one cannot be forecast at any price.
