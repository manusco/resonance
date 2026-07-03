# Experimentation Ops Protocol

> "Decide the sample size and the stopping rule before you look at the data. Everything after is theater."

## Contents

- [1. The Pre-Registration Discipline](#1-the-pre-registration-discipline)
- [2. Sample Size and Minimum Detectable Effect](#2-sample-size-and-minimum-detectable-effect)
- [3. Significance, Power, and What p Means](#3-significance-power-and-what-p-means)
- [4. The Peeking Problem](#4-the-peeking-problem)
- [5. Sequential Testing and Stopping Rules](#5-sequential-testing-and-stopping-rules)
- [6. Holdouts](#6-holdouts)
- [7. Common Traps](#7-common-traps)
- [8. The Test Readout](#8-the-test-readout)

## 1. The Pre-Registration Discipline

Before the test runs, write down and freeze five things:

1. **Hypothesis**: "If we [change X], then [primary metric Y] will improve because [reason Z]."
2. **Primary metric**: exactly one. Every additional "primary" metric multiplies your false-positive rate.
3. **Minimum detectable effect (MDE)**: the smallest lift worth shipping for. This is a business decision, not a statistical one.
4. **Sample size and horizon**: computed from the MDE (section 2). This fixes when the test ends.
5. **Stopping rule**: fixed-horizon (look once, at the end) or a named sequential method (section 5). Decide now, not when the numbers get exciting.

Writing these down is what separates an experiment from a fishing trip. If they are not fixed in advance, the analysis has too many free parameters and any result can be justified after the fact.

## 2. Sample Size and Minimum Detectable Effect

You cannot pick a sample size without first picking the smallest effect you care about. Smaller effects need dramatically more traffic.

The four inputs to a sample-size calculation:
- **Baseline conversion rate** (the metric's current value before the change).
- **Minimum detectable effect (MDE)**: the smallest relative lift you want to be able to detect (e.g. a 5% relative improvement). Halving the MDE roughly quadruples the required sample.
- **Significance level (alpha)**: usually 0.05. The false-positive rate you accept.
- **Statistical power (1 - beta)**: usually 0.80. The chance of detecting a real effect of MDE size.

Compute the number with a calculator (Evan Miller's, or your platform's), never by eye. Then sanity-check it against your traffic: sample size divided by weekly visitors gives the run time. If that run time is months, the test as scoped is not viable, and you must either accept a larger MDE, pick a higher-traffic surface, or use a more sensitive metric.

### Run at least one full cycle
Even when the math clears early, run a test for at least one full business cycle (usually a week, often two) so that weekday/weekend and day-of-week effects average out. A test that ran Tuesday to Thursday is measuring Tuesday-to-Thursday users, not your audience.

## 3. Significance, Power, and What p Means

- **p-value**: the probability of seeing an effect this large (or larger) if the variant did nothing. p < 0.05 means "unlikely under the null", not "95% chance the variant is better" and not "95% chance we are right". This misreading drives most bad calls.
- **Significant is not the same as meaningful.** With enough traffic, a 0.1% lift becomes statistically significant and is still not worth the engineering to ship it. Compare the effect to the MDE, not just to zero.
- **Not significant is not the same as no effect.** A flat result on an underpowered test tells you almost nothing. It may mean no effect, or it may mean you lacked the sample to see one. Report the confidence interval, which shows the range of effects still consistent with the data.
- **Power is the other half.** An underpowered test is a coin flip dressed as evidence. If you cannot reach the sample size for a reasonable MDE, do not run a formal test and pretend it settled anything; call it directional.

## 4. The Peeking Problem

This is the most common way marketers ship false wins. If you watch a running test and stop it the instant it crosses p < 0.05, your real false-positive rate is not 5%. It is far higher, because a test in progress crosses the significance line by chance many times before settling. Each look is another opportunity to catch a random high and call it a victory.

The rule for a fixed-horizon test is blunt: **do not act on interim results.** Compute the sample size, run to it, look once. Monitoring for operational breakage (did the variant crash the page, is there a sample-ratio mismatch) is fine and necessary. Reading the win/loss verdict early and acting on it is not.

If the business genuinely cannot wait for the full horizon, you do not fix that by peeking at a fixed-horizon test. You switch to a method built for continuous monitoring (section 5).

## 5. Sequential Testing and Stopping Rules

Sequential methods are designed so you can look repeatedly without inflating the false-positive rate, because the significance threshold is adjusted to pay for every look.

- **Group-sequential / alpha-spending (O'Brien-Fleming, Pocock)**: pre-plan a fixed number of interim analyses and spend your alpha budget across them. Early looks require a much stronger result to stop; the bar loosens as the test matures. Lets you stop early for a clear win or clear futility without cheating.
- **Always-valid inference (sequential likelihood-ratio tests, mSPRT, "always-valid p-values" and confidence sequences)**: the approach several modern experimentation platforms use. Valid to look at any time, as often as you like, because the statistics are constructed to hold under continuous monitoring. The cost is somewhat lower sensitivity than a perfectly-run fixed-horizon test of the same length.

The trade is real: sequential testing buys you honest early stopping in exchange for needing a larger sample to detect the same effect if the test runs full length. Choose it when the value of stopping early (or the inability to commit to a horizon) outweighs that cost. What you may not do is use fixed-horizon statistics and then peek, which is the worst of both worlds: no early-stopping guarantee and an inflated error rate.

## 6. Holdouts

A holdout is a slice of the audience deliberately excluded from a treatment (or from all experiments) so you can measure true, durable, cumulative impact.

- **Feature / campaign holdout**: keep a small percentage from ever receiving a launched change, for weeks or months, to measure long-run effect after the novelty fades. An in-test win can decay to nothing once the newness wears off; the holdout catches that.
- **Global / marketing holdout**: withhold all marketing from a randomized group to estimate the incremental lift of marketing as a whole. This is the aggregate cousin of the incrementality tests in `attribution_models.md`.
- **Cost**: a holdout is deliberately forgone value on that slice. Keep it as small as statistical power allows, and be explicit that you are trading a little short-term revenue for a trustworthy causal read.

## 7. Common Traps

- **Peeking / early stopping.** Stopping the moment it looks significant. The single biggest source of false wins. Fix: fixed sample size and one look, or a sequential method.
- **Novelty and primacy effects.** Regular users react to a change simply because it is new (or resist because it is unfamiliar). The effect fades. Fix: run longer, segment new vs returning users, and confirm with a holdout.
- **Sample-ratio mismatch (SRM).** The split arrived at, say, 55/45 instead of the intended 50/50. This signals a broken randomizer or biased assignment and invalidates the test. Fix: check the ratio with a chi-square test before trusting any result; if SRM is present, do not read the outcome.
- **Multiple comparisons.** Testing many metrics or many variants and celebrating whichever crossed 0.05. With twenty metrics, one will look significant by chance. Fix: pre-declare one primary metric; correct (Bonferroni or similar) when you must test several.
- **Winner's curse.** The observed lift of a variant selected because it won is biased upward; the true effect is usually smaller than the point estimate. Fix: expect regression to the mean, and lean on the lower bound of the confidence interval for the business case.
- **Underpowered tests.** Not enough traffic to detect the MDE, so a null result is meaningless and any positive result is fragile. Fix: compute power up front; if you cannot reach it, call the result directional, not conclusive.
- **Changing the test mid-flight.** Editing the variant, the traffic split, or the audience after launch resets the experiment. Fix: freeze the setup; a change means a new test.
- **Simpson's paradox.** An aggregate result reverses inside every segment (or vice versa) because of a lurking variable. Fix: check whether the headline effect holds within key segments before shipping.

## 8. The Test Readout

Report every completed test with:
- The pre-registered hypothesis and primary metric.
- The observed effect **with its confidence interval**, not just a point estimate and a p-value.
- The sample size reached and whether it hit the planned target.
- Any guardrail metrics and whether they moved.
- The decision: ship, kill, or iterate, and the reason.

A "failed" test that was run honestly is a real result: you learned the change does not move the metric, and that is worth knowing. A test that was peeked at, underpowered, or SRM-broken is not a result at all, however exciting the number looked.
