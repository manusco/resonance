# Quota and Capacity Planning

> A revenue target is a physics problem before it is a motivation problem. Reps times productivity times ramp sets a ceiling, and no amount of pushing beats a ceiling. Model the ceiling, reconcile it with the board's number, and if they do not meet, name the gap and pick a lever.

## Contents

- [1. Coverage: The Inverse of Win Rate](#1-coverage-the-inverse-of-win-rate)
- [2. Capacity from the Target](#2-capacity-from-the-target)
- [3. Ramp: The Rep Who Does Not Exist Yet](#3-ramp-the-rep-who-does-not-exist-yet)
- [4. Quota Setting: Attainable and Economic](#4-quota-setting-attainable-and-economic)
- [5. Territory Design: Balance on Potential](#5-territory-design-balance-on-potential)
- [6. Reconciling Top-Down and Bottom-Up](#6-reconciling-top-down-and-bottom-up)
- [7. A Worked Example](#7-a-worked-example)

## 1. Coverage: The Inverse of Win Rate

Pipeline coverage is open in-period qualified pipeline divided by the quota you must close.

```
Coverage ratio = Open qualified pipeline (closing in period) / Quota for the period
Required coverage = 1 / win rate on qualified pipeline
```

The 3x heuristic is simply `1 / 0.33`. It assumes you close a third of your qualified pipeline. That is a starting guess, not a law:

| Win rate on qualified pipeline | Required coverage |
| :--- | :--- |
| 50% | 2x |
| 33% | 3x |
| 25% | 4x |
| 20% | 5x |
| 15% | 6.7x |

Two disciplines keep coverage honest:

- **Count only qualified, in-period pipeline.** All-time pipeline stuffed with dead deals and dates in three quarters inflates coverage and hides the real gap. Coverage on junk is not coverage.
- **Use your own win rate.** Borrowing a benchmark win rate to justify 3x is how teams run at half the coverage they believe. Measure the rate at which your qualified pipeline actually converts, and set coverage from that.

## 2. Capacity from the Target

Build the headcount from the number, top down:

```
1. Net-new target                 T
2. Over-assignment factor         F   (total assigned quota = T x F, so the team lands T even below 100% attainment; F is usually 1.15 to 1.25)
3. Rep annual quota               Q
4. Fully-ramped reps needed       N = (T x F) / Q
```

The over-assignment factor exists because not every rep hits quota. If you assign exactly T across the team and the average rep lands 85 percent, you miss by 15 percent before you start. Assigning `T x F` builds the shortfall in. Equivalently, expected team attainment is `1 / F`.

Then translate the number into a sourcing target:

```
Pipeline needed  = Total assigned quota / win rate
Opps needed      = Pipeline needed / ACV
```

Opps needed is the target you hand to the SDR team and marketing. This is how a revenue number becomes a demand-generation quota upstream, instead of a hope that pipeline appears.

## 3. Ramp: The Rep Who Does Not Exist Yet

A new hire does not carry full quota on day one. Ramp time is roughly onboarding plus one sales cycle: the time to learn the product and to work a deal from first meeting to close. It runs 3 to 9 months for most B2B motions.

Consequences you cannot skip:

- **Hire ahead of need.** To have N productive reps in Q3, the reps must be hired ramp-months earlier. A plan that hires in the quarter it needs the output is short by the whole ramp.
- **Count ramping reps at partial productivity.** A rep in month 2 of a 6-month ramp is not zero and not full; model them at a fraction. Summed across a growing team, the ramp drag is large enough to sink a plan that ignores it.
- **Budget for attrition.** Reps leave. Plan headcount with a 10 to 20 percent annual attrition buffer, or the capacity you modeled quietly erodes.

The trap is a capacity plan that assumes every seat is filled by a fully-ramped rep on January 1. That rep does not exist yet. Model the ones you will actually have.

## 4. Quota Setting: Attainable and Economic

A quota must clear two tests at once:

- **Attainable:** roughly 60 to 70 percent of reps should hit it. If everyone hits, the quota is too low and you are leaving production on the table. If 10 percent hit, it is a fantasy, reps stop believing it, and the good ones leave.
- **Economic:** quota should sit at a healthy multiple of on-target earnings, commonly 4x to 6x OTE. The multiple is what pays for the fully-loaded rep plus support, overhead, and profit. A rep on 200K OTE carrying an 800K quota is a 4x that only works at very high margin; the same rep at 1M is a 5x with more room.

The two tests can conflict: the economically required quota may be higher than reps can attain. When they do, that is not a number to average, it is a signal that productivity, pricing, or the motion has to change. Do not paper over it by setting a quota nobody hits.

## 5. Territory Design: Balance on Potential

A territory is a rep's addressable market. Design it on opportunity potential, not account count.

- **Balance on potential, not headcount of accounts.** Fifty enterprise logos and five hundred SMB accounts can hold equal revenue potential. Splitting on account count hands one rep a goldmine and another a desert, and both cost you: one is capacity-constrained and leaving deals unworked, the other is starving and about to quit.
- **Minimize disruption.** Reps build relationships and account knowledge. Reshuffling territories every year burns that context. Change when the imbalance justifies the disruption, not annually by reflex.
- **Keep patches whole.** Split by segment, geography, or named-account list so ownership is unambiguous. Overlapping territories create the "who owns this" dispute that `resonance-sales-lead-ops` then has to untangle.

Bad territories show up as a wide spread in attainment that has nothing to do with rep skill: your best rep missing in a thin patch, a weak rep hitting in a rich one. Check attainment against territory potential before you conclude anything about the reps.

## 6. Reconciling Top-Down and Bottom-Up

Two numbers must meet:

- **Top-down:** the board's target T.
- **Bottom-up:** what current capacity can produce, `ramped reps x quota x expected attainment`.

When bottom-up is below top-down, you have a gap, and there are exactly three honest levers:

1. **Hire.** Add capacity, remembering ramp, so the reps are productive when the number is due.
2. **Raise productivity.** Improve win rate, ACV, or cycle time (the velocity levers) so each rep produces more.
3. **Reset the target.** If hiring and productivity cannot close the gap in time, the target is not real, and saying so now is cheaper than discovering it in Q4.

Presenting the gap and the lever choice is a Recommendation-First decision: name the gap, show the three options with their cost and risk, recommend one, and let the operator decide. Silently accepting an impossible target is the failure mode.

## 7. A Worked Example

```
Net-new target        T   = 6,000,000
Over-assignment       F   = 1.2         -> assigned quota = 7,200,000
Rep quota             Q   = 1,000,000   (OTE 200,000 -> 5x, economic)
Reps needed           N   = 7,200,000 / 1,000,000 = 7.2 -> round to 8 AEs
Win rate                  = 20%          -> required coverage = 1 / 0.20 = 5x
Pipeline needed           = 7,200,000 x 5 = 36,000,000 qualified pipeline for the year
ACV                       = 50,000       -> opps needed = 36,000,000 / 50,000 = 720 qualified opps/year (~60/month)
Ramp                  R   = 4 months     -> hire the 8 AEs by Q3-minus-ramp, plus a ~15% attrition buffer
```

Read what the example forces into the open: this plan needs 8 ramped AEs, 5x coverage (not 3x, because the win rate is 20 percent), 36M of qualified pipeline, and 60 qualified opps a month from the top of the funnel. If the SDR and marketing engine cannot source 60 opps a month, the 6M target is already a miss, and you know it in January instead of December.
