# Churn Diagnosis and Saves

> Diagnose before you save. The intervention depends entirely on the root cause, and a discount fired at the wrong cause wastes margin and trains customers to threaten cancellation for a coupon. Some churn should not be fought at all.

## Contents

- [1. Diagnose before you save](#1-diagnose-before-you-save)
- [2. Voluntary, involuntary, and passive churn](#2-voluntary-involuntary-and-passive-churn)
- [3. Root-cause classes](#3-root-cause-classes)
- [4. Save plays by cause](#4-save-plays-by-cause)
- [5. The honest let-go](#5-the-honest-let-go)
- [6. Pause and downgrade before discount, and the dark-pattern line](#6-pause-and-downgrade-before-discount-and-the-dark-pattern-line)
- [7. The exit interview and win-back handoff](#7-the-exit-interview-and-win-back-handoff)
- [8. Metrics](#8-metrics)

## 1. Diagnose before you save

The reflex to offer a discount the moment a customer signals leaving is the most expensive habit in retention. It treats every churn as a price problem when most are not, it burns margin, and it teaches the market that a cancel threat unlocks a coupon.

Diagnose first. Find the root cause, then choose the intervention that fits it. A save with no diagnosis behind it is a guess that costs money.

## 2. Voluntary, involuntary, and passive churn

Three types, three tools. Classify before intervening.

| Type | Cause | Intervention |
|------|-------|--------------|
| **Voluntary** | Customer chose to leave: no value, wrong fit, competitor, budget | Root-cause diagnosis, then a fitted save |
| **Involuntary** | Payment failed: expired card, decline | Dunning and a card update, nothing to persuade |
| **Passive** | No decision at all: the renewal lapsed because no one drove it | Fix your own motion; this is an operational miss, not a customer choice |

Involuntary churn is smaller in B2B (annual contracts, invoicing) than in consumer, but real for card-billed SMB, and the mechanics live in `resonance-marketing-lifecycle`. Passive churn is the one to be ashamed of: the customer did not leave, you failed to renew them.

## 3. Root-cause classes

For voluntary churn, name the actual driver. Each has a different answer.

| Root cause | Signature | Real fix |
|------------|-----------|----------|
| **No value reached** | Never activated, low adoption, no outcome | Re-onboard to first value, if there is time |
| **Wrong fit** | Bought for a job the product does not do | Let go honestly; a forced save churns again and refunds |
| **Champion left** | Usage fine, sponsor gone, replacement indifferent | Re-sell value to the successor, fast |
| **Budget cut** | Value acknowledged, money gone | Downgrade or pause, keep the relationship for later |
| **Competitor** | Switching to an alternative | Honest comparison, close the real gap if you can |
| **Price** | Value seen as below cost | Re-frame value, or right-size the plan; discount last |

The signature tells you the cause; the cause tells you the fix. "Too expensive" often means "I did not get enough value to justify the price," which is a value problem wearing a price label. Test that before you discount.

## 4. Save plays by cause

Match the play to the diagnosis, and sequence the cost from low to high.

- **No value reached:** an intensive re-onboarding sprint to the first-value milestone that was missed. If the renewal is too close to reach it, be honest about the timeline.
- **Champion left:** an immediate value re-introduction to the successor, treating them as a new buyer who inherited a tool they did not choose.
- **Budget cut:** pause or downgrade to hold the relationship through the cut, with a clean path back when budget returns.
- **Competitor:** an honest side-by-side and a serious look at the gap they are leaving for. If the competitor genuinely fits better, say so.
- **Price:** re-frame against the outcome delivered, then right-size the plan. Reach for a discount only when the value is real and the fit is right, and make it time-boxed.

## 5. The honest let-go

Not every account should be saved, and pretending otherwise costs you twice.

- **Wrong fit** churns again no matter what you offer, and often refunds or disputes on the way out. Let it go cleanly and keep the goodwill.
- A forced save on a bad-fit account inflates the save rate this quarter and the churn rate next quarter, and it generates the worst reviews you will get.
- A clean exit with the door left open, and the data preserved, beats a coerced stay. Some of those customers come back when their need changes, and none of them badmouth you.

Retention is a quality number, not just a quantity one. Saving the wrong accounts is negative work.

## 6. Pause and downgrade before discount, and the dark-pattern line

- Sequence the offers from least costly to most: pause, then downgrade, then a time-boxed discount. The discount is the most expensive tool and the easiest to abuse, so it comes last.
- Keep the exit as easy as the entrance. Hiding the cancel button, requiring a phone call to leave what took one click to buy, pre-checking a plan the customer did not choose, or burying a confirm in double negatives: all out of bounds. They buy one cycle and cost trust, chargebacks, and word of mouth.
- A save offer persuades with a real alternative. A dark pattern removes the choice. The line is that simple.

## 7. The exit interview and win-back handoff

When an account does leave, extract the lesson and close the loop.

- **Ask why, once, cleanly.** A single honest exit question yields more than a long survey no one finishes. Record the reason in a structured field, not a free-text note that dies.
- **Aggregate the reasons.** Churn reasons are the highest-signal voice-of-customer data you have, because the customer paid to be wrong. Weight them by revenue and frequency and hand product a ranked list.
- **Hand off to win-back.** A departed customer is out of your scope and into the capped win-back campaign in `resonance-marketing-lifecycle`. Tag the churn reason so the win-back speaks to what they actually left over.

## 8. Metrics

| Metric | Definition | Target shape |
|--------|------------|--------------|
| Gross revenue retention | Retained revenue before expansion, over a cohort | The core leak metric; drive it up |
| Save rate | Cancel or non-renewal risks saved / total | Read it with fit quality, not as a raw count |
| Churn-reason distribution | Share of churn by root cause | Tells you which fix returns the most |
| Passive churn share | Non-renewals with no active decision | Should trend to zero; it is entirely on you |

Watch save rate and reason distribution together. A high save rate built on discounting bad-fit accounts is a number that reverses next quarter. Saving the right accounts for the right reason is the only save worth counting.
