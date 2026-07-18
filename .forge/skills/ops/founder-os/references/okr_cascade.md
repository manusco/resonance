# The OKR Cascade: company to team to this week

> An objective is a direction. A key result is a number that proves you went there. If a key result cannot be checked by a `met-` reading in the ledger, it is a task wearing an outcome's clothes.

## Contents

- [1. Objective vs Key Result](#1-objective-vs-key-result)
- [2. The Three Levels](#2-the-three-levels)
- [3. Key Results Are Ledger Metrics](#3-key-results-are-ledger-metrics)
- [4. The Sandbagging Trap](#4-the-sandbagging-trap)
- [5. Outcomes, Not Tasks](#5-outcomes-not-tasks)
- [6. Cascade Discipline](#6-cascade-discipline)
- [7. The Reset Cadence](#7-the-reset-cadence)
- [8. Failure Modes](#8-failure-modes)

## 1. Objective vs Key Result

An **objective** is qualitative and directional: "Become the default onboarding tool for small B2B teams." It sets the aim and it should be a little uncomfortable to say out loud.

A **key result** is a number with a target and a date: "Activated accounts from 120 to 300 by quarter end." It is the evidence that the objective moved. Three to five key results per objective is the working range. Fewer and you are not covering the objective; more and none of them is load-bearing.

The test: read a key result to someone outside the company. If they cannot tell whether it was hit without asking you to explain, it is not a key result yet.

## 2. The Three Levels

The cascade has exactly three levels, and each level answers to the one above it.

- **Company (the quarter).** One or two objectives. This is the whole company's direction for the quarter, set by the founder. If there are five company objectives, there are zero.
- **Team or function (the quarter).** Each function names the key results it owns that roll up into the company objective. Sales owns pipeline and closed revenue. Success owns retention and expansion. Product owns activation. A function's key results must visibly sum toward the company number, or the function is optimizing something the company did not ask for.
- **This week (the operating unit).** The company runs on weeks, not quarters. Each week, every owner names the one or two moves that advance their quarterly key result. This is where OKRs meet the calendar. A quarter is won or lost in twelve or thirteen weekly increments, not in a burst at the end.

The cascade is a chain of "so that." We ship the guided-setup flow *so that* activation rises *so that* we become the default onboarding tool. If a weekly move does not connect up the chain to a company objective, cut it or question the objective.

## 3. Key Results Are Ledger Metrics

A key result is not prose in a doc. It is a `met-` entry in `.resonance/ledger/metrics.md` with a `target` and an `as_of` date, or an `exp-` entry when the result is a test of a hypothesis. The target on the entry is the key result's target. The reading is the current value.

```
## met-activated-accounts-q3: Activated accounts, Q3 target
type: metric
created: 2026-07-01
status: active
value: 120
unit: accounts
target: 300
as_of: 2026-07-01
source: product analytics, weekly pull
due: 2026-09-30
```

Because the target lives in the ledger, the weekly business review reads the gap instead of re-litigating what the goal was. When a key result's proof lands in the future, the work that chases it ends `DONE_PENDING_OUTCOME`, and the `due:` date is when `py .forge/measurement_due.py` will surface it for a real reading. Nobody has to remember to check; the ledger remembers.

## 4. The Sandbagging Trap

The failure that quietly kills an OKR system: setting a target you have already hit, or one you are certain to hit. A key result you are confident of is not a key result. It is a status report written in advance.

Sandbagging happens because a missed number feels like failure, so people set numbers they cannot miss. The fix is to separate the goal from the grade. A healthy stretch key result lands somewhere around 70 percent in a good quarter. Hitting 100 percent on every key result is not excellence; it is evidence the targets were too low and the company left growth on the table.

Refuse to set a key result at or below a level the company has already reached. "500 signups this quarter" when last quarter did 520 is not a goal, it is a floor with a bow on it. Push the number until the owner is genuinely unsure they will hit it, then write that number down.

## 5. Outcomes, Not Tasks

"Ship the referral feature" is a task. "Lift the share of signups that come from referrals from 4 percent to 15 percent" is a key result. The task can be done in full and change nothing. The outcome is the point.

The flip test: if you can mark a key result "done" by completing an activity rather than by moving a number, it is a task in disguise. Rewrite it as the number the activity is supposed to move. If you cannot name that number, you do not yet know why you are doing the work, and that is the finding.

Ship dates and launches still belong on the roadmap; they are just not key results. The roadmap holds the bets. The OKR holds the outcome the bets are supposed to produce.

## 6. Cascade Discipline

- **Sum-check every level.** A function's key results must add up to more than the company target, or the company target has no path. If sales owns 400K in new revenue and the three named plays sum to 250K, the plan is already short by 150K in week one.
- **One owner per key result.** Shared ownership is no ownership. Two names on a number means each waits for the other.
- **No orphan work.** Any weekly move that does not trace to a key result is either a hidden priority you should promote to the OKR, or drag you should cut.
- **Keep the count brutal.** One or two company objectives. Three to five key results each. The discipline is in what you refuse to add.

## 7. The Reset Cadence

OKRs reset on a fixed quarterly rhythm, not when someone remembers. The reset is a real session: grade last quarter's key results from their final `met-` readings, write one line of why each landed where it did, then set the next quarter's cascade. The grading is not a performance review; it calibrates how well the company sets targets. A team that keeps hitting 100 percent is sandbagging; a team stuck near 30 percent is either dreaming or blocked, and the review names which.

Mid-quarter, the cascade is stable. Chasing a new objective in week six because a competitor shipped something is how a company ends the quarter having moved nothing. Log the new idea as a `dec-` candidate for next quarter and hold the line.

## 8. Failure Modes

- **Too many objectives.** Five company objectives means no priority. Cut to one or two.
- **Activity key results.** "Run 10 experiments" instead of "lift conversion to 6 percent." Grade the outcome, not the effort.
- **Sandbagged targets.** Numbers set to be hit. If you are sure, it is too low.
- **Set and forget.** OKRs written at quarter start and never read again. The weekly review is what keeps them alive.
- **No ledger tie.** Key results kept in a slide instead of as `met-` entries, so the number of record drifts and every review argues about what it even is.
- **Cascade that does not sum.** Function targets that do not add up to the company target. The gap is the plan's hole; find it in week one, not week twelve.
