# Activation and Onboarding

> Get the user to their first real win before their motivation runs out. Activation is an action they take, not a tour you give them.

## Contents

- [1. The activation model](#1-the-activation-model)
- [2. Finding the aha moment](#2-finding-the-aha-moment)
- [3. Time-to-value: cut the gap](#3-time-to-value-cut-the-gap)
- [4. First-run patterns](#4-first-run-patterns)
- [5. Empty states and the setup moment](#5-empty-states-and-the-setup-moment)
- [6. Long time-to-value products](#6-long-time-to-value-products)
- [7. Retention loops and habit formation](#7-retention-loops-and-habit-formation)
- [8. Metrics](#8-metrics)
- [9. Failure modes](#9-failure-modes)

## 1. The activation model

```
Signup -> First value -> Habit -> Retention
          |                        |
     time-to-value            activation rate
      (compress)               (measure by cohort)
```

Core rule: a user who does not feel value in the first session rarely comes back. Activation is not "finished the tour" or "completed the profile". It is the moment the product did the thing they came for. Design the first-run backward from that moment.

## 2. Finding the aha moment

The aha moment is the earliest action that predicts long-term retention. It is specific and measurable.

| Product type | Typical aha moment | How you measure it |
|--------------|--------------------|--------------------|
| SaaS tool | Completed the first core action | Created first [object] |
| Collaboration | Brought in a second person | Team size > 1 |
| Analytics | Saw a real insight on real data | Dashboard populated |
| Marketplace | Finished the first transaction | First buy or sell |
| Content | Consumed one high-value piece | Completion event |

How to find yours: cohort analysis. Take users who retained past day 30 and users who churned. Look at week one. Which action shows up in the retained group and not the churned group? That correlation, held across cohorts, is your candidate. Validate it does not just track generally engaged users by checking whether pushing more users through that action lifts retention.

## 3. Time-to-value: cut the gap

Time-to-value (TTV) is the elapsed time from signup to the aha moment. It is the single number onboarding exists to shrink.

Order of operations, cheapest first:
1. **Remove steps.** Every field at signup is a dropout. Ask only what the first-run needs to personalize. Defer the rest.
2. **Pre-fill and default.** Sensible defaults beat empty inputs. Detect what you can (timezone, plan, sample workspace).
3. **Do the work for them.** Import, connect, or generate a starter so the product is not empty on arrival.
4. **Then, and only then, encourage.** Progress bars and nudges help a short path. They cannot rescue a long one.

Cutting a step beats adding a tooltip that explains the step.

## 4. First-run patterns

Pick by product shape. Do not stack all four.

### Setup wizard (3 to 5 steps)
Collect only essential config. Show progress ("Step 2 of 4") to pull completion via the goal-gradient effect. Allow skip but track it, since skippers activate slower. End on a win, never on a settings screen.

### Interactive walkthrough
Guide the user through their first real action, not a video. Use their data, not a demo. Name the value at each step ("You just published your first page").

### Template or quick-start
Offer pre-built templates so the canvas is never blank. "Start from this template" beats "Create from scratch". This kills the blank-canvas paralysis.

### Setup checklist
Show 5 to 7 setup actions in-app. Pre-check anything already done, because the Zeigarnik effect makes an unfinished list pull for completion. Celebrate the last check.

## 5. Empty states and the setup moment

Empty states are the highest-leverage screens you have, because every new user sees them. Treat them as onboarding, not as a fallback.

- Never ship a bare "No data yet".
- Show what the screen will look like full, using sample or ghost data.
- One clear CTA: "Create your first [thing]".
- State the payoff: "This is where your [outcome] will appear".

The setup moment (connect a source, invite a team, import data) is where TTV is won or lost. Make the highest-value connection the default path, not an advanced option.

## 6. Long time-to-value products

Some products cannot deliver the full aha in one session. A tax tool proves itself at filing. A hiring tool proves itself at the first hire. An analytics tool needs weeks of data before the trend is real. Forcing a fake five-minute win here is dishonest and it churns users when reality arrives.

Design for a long TTV instead of pretending it is short:

- **Define a leading milestone.** Pick an early, reachable proxy that correlates with the eventual value (connected the payroll feed, imported last quarter, invited the finance lead). Activate on the proxy, not the far-off payoff.
- **Set the expectation out loud.** Tell the user when value arrives ("Your first full report is ready after 14 days of data") so the wait is a plan, not a disappointment.
- **Show accruing progress.** A filling dashboard, a "3 of 10 data points collected" counter, a preview built from partial data. Visible movement holds a user across a gap.
- **Bridge the gap with the sequence.** This is where lifecycle email carries weight: keep the setup warm, deliver interim value (a benchmark, a tip, a partial insight), and land the "it's ready" trigger the moment the real value exists. See `references/email_lifecycle.md`.
- **Instrument the wait.** Watch drop-off between the leading milestone and the true aha, and shorten whatever step stalls people there.

## 7. Retention loops and habit formation

First-use success is not retention. Retention is a loop the user re-enters on their own.

The loop: **Trigger, Action, Variable Reward, Investment.**
1. **Trigger.** External at first (an email, a notification), internal over time (a felt need the product now owns). Durable habits run on internal triggers.
2. **Action.** The simplest behavior that delivers the reward. Reduce friction here relentlessly.
3. **Variable reward.** New, not fully predictable value: a fresh insight, progress, recognition. Predictable rewards stop pulling.
4. **Investment.** The user puts something in (data, config, a teammate) that makes the next loop better and raises switching cost.

Map your loop, then fix the weakest link rather than adding a fifth reminder to a broken action step.

## 8. Metrics

| Metric | What it measures | Rough target |
|--------|------------------|--------------|
| Time-to-first-value | Speed to aha | As low as the product allows |
| Activation rate | % of signups reaching the aha | > 40% early cohorts |
| Setup completion | % finishing onboarding | > 60% |
| Day-1 retention | % returning next day | > 40% |
| Day-7 retention | % active after a week | > 25% |
| Core-feature adoption | % using the core action in week one | > 50% |

Read every one of these by cohort. A blended average will look stable while a new cohort quietly churns.

## 9. Failure modes

1. **Feature tour instead of value tour.** Showing every feature is not showing value. Drive to the one action that delivers the first win.
2. **Asking too much at signup.** Role, company size, photo: each field is a dropout. Collect what personalizes the first-run, defer the rest.
3. **Sample data that never becomes their data.** A demo that does not transition into the user's own workspace teaches nothing about their value.
4. **No path for the stuck user.** If someone pauses more than 30 seconds, offer help: a tooltip, a chat, a guided route.
5. **One path for everyone.** Segment by role or use case at signup and branch the first-run.
6. **Faking a short TTV on a long-TTV product.** A hollow instant win sets an expectation the product breaks later. Use a leading milestone instead (section 6).
