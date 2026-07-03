# Attribution Models Protocol

> "Attribution is a model, not a measurement. Every model has a bias baked in. Name it out loud."

## Contents

- [1. The Core Truth](#1-the-core-truth)
- [2. The Single-Touch Models](#2-the-single-touch-models)
- [3. The Multi-Touch Models](#3-the-multi-touch-models)
- [4. Where Each Model Lies](#4-where-each-model-lies)
- [5. MTA vs MMM](#5-mta-vs-mmm)
- [6. Incrementality: The Only Real Test](#6-incrementality-the-only-real-test)
- [7. Choosing and Triangulating](#7-choosing-and-triangulating)
- [8. Common Failures](#8-common-failures)

## 1. The Core Truth

A customer touches many channels before converting: an ad, a search, a newsletter, a friend, a return visit. Attribution decides how to split the credit for the conversion across those touches. There is no objectively correct split, because you cannot observe the counterfactual for a single person. Every model is an assumption about how credit should flow. The job is to pick the assumption whose distortion you can live with for the decision in front of you, and to never mistake the model's output for ground truth.

## 2. The Single-Touch Models

Assign 100% of the credit to one touch.

| Model | Gives all credit to | Systematic bias |
| :--- | :--- | :--- |
| **First-touch** | The first interaction | Overcredits discovery and top-of-funnel; ignores everything that closed the deal |
| **Last-touch** | The last interaction before conversion | Overcredits closing channels (brand search, direct); makes upper-funnel look worthless |
| **Last non-direct** | The last touch that was not "direct" | Slightly less wrong than last-touch; still starves the top of the funnel |

Single-touch is simple and it is the default in most ad platforms, which is exactly why it is dangerous. Last-click is the single most common cause of a bad budget decision: it credits the channel that was there at the end (often branded search or retargeting, which the customer would have converted through anyway) and shows near-zero return for the awareness channels that created the demand in the first place. Cut those on a last-click read and conversions fall a quarter later with no obvious culprit.

## 3. The Multi-Touch Models

Split credit across several touches.

| Model | Split rule | Best for |
| :--- | :--- | :--- |
| **Linear** | Equal credit to every touch | A baseline that refuses to privilege any stage; rarely matches reality but is honest about its ignorance |
| **Position-based (U-shaped)** | 40% first, 40% last, 20% spread across the middle | Journeys where discovery and closing both clearly matter and the middle is nurture |
| **Time-decay** | More credit to touches nearer the conversion | Long consideration cycles where recent touches plausibly did more work |
| **Data-driven (DDA)** | Credit assigned by an algorithm from observed conversion paths | High-volume accounts with enough path data; the split is empirical, not hand-picked |

Data-driven attribution sounds like the answer to "which model is right", but it is still a model. It needs a large volume of both converting and non-converting paths to be stable, it is often a black box you cannot fully audit, and it still depends entirely on the touches being tracked. It cannot credit a channel it never saw.

## 4. Where Each Model Lies

- **First-touch** makes your best awareness channel look like your only channel and your closers look free. Believe it, and you overspend on the top and underinvest in conversion.
- **Last-touch** does the reverse and is the more common trap because platforms report it by default. It makes branded search and retargeting look like heroes when they were mostly harvesting demand other channels created.
- **Linear** refuses to distinguish a decisive touch from an incidental one; a throwaway impression gets the same credit as the demo that sold the deal.
- **Position-based** hard-codes a belief (first and last matter most) that may not hold for your funnel.
- **Time-decay** assumes recency equals influence, which punishes the early touch that actually created the intent.
- **Data-driven** launders its assumptions into an algorithm, so the bias is harder to see, not absent. It also breaks silently when tracking coverage drops.

Every one of these shares a deeper limitation: they can only distribute credit among **tracked, converting** paths. They are blind to the untracked, blind to the counterfactual, and structurally unable to tell you whether a channel was **incremental** (did it cause conversions that would not have happened otherwise) or merely **present** (it was on the path, but the customer would have converted anyway).

## 5. MTA vs MMM

Two whole families sit above the individual models.

### Multi-Touch Attribution (MTA)
Bottom-up. Stitches individual user journeys from tracked touches and assigns credit per path using one of the models above.
- **Strength**: user-level, granular, can attribute down to a keyword or creative.
- **Fatal weakness**: depends on deterministic cross-device, cross-channel user tracking, which privacy changes are steadily dismantling: cookie deprecation, ad-blockers, walled gardens that do not share user-level data, consent gating, and platforms that report only their own conversions. As coverage falls, MTA does not fail loudly; it quietly under-reports whatever it cannot see and over-credits whatever it can.

### Marketing-Mix Modeling (MMM)
Top-down. Regresses aggregate outcomes (sales, signups) against aggregate inputs (spend per channel, seasonality, price, promotions) over time. No user-level data required.
- **Strength**: survives cookie loss and privacy changes because it never needed individual tracking; captures offline and hard-to-track channels (TV, out-of-home, PR); can estimate diminishing returns and saturation per channel.
- **Weakness**: coarse (channel-level, not user-level); needs a long history and real spend variation to fit; slow to react; correlational unless combined with experiments; easily confounded by anything that moves with spend (you always advertise more at Christmas, so does everyone).

### The reconciliation
MTA answers "which touch, for this user?" MMM answers "how much did this channel contribute, in aggregate?" They will disagree. Mature measurement runs both and calibrates them against incrementality experiments (section 6) rather than trusting either alone.

## 6. Incrementality: The Only Real Test

Attribution redistributes credit for conversions that happened. Incrementality asks the only question that matters for spend: **would this conversion have happened anyway?**

The clean way to answer it is an experiment, not a model:
- **Geo holdout / ghost ads / PSA test**: withhold a channel from a randomized group (a set of regions, or a matched audience) and compare conversions to the exposed group. The difference is the incremental effect. Everything else is inference.
- A channel can score huge in last-touch and near-zero in incrementality (retargeting people who would have bought regardless is the classic case). When attribution and incrementality disagree, incrementality is closer to the truth, because it has a control group and attribution does not.

If a budget decision is large enough to matter, back it with a holdout, not a report.

## 7. Choosing and Triangulating

- **Match the model to the decision.** Optimizing a single closing campaign: last-touch is tolerable. Deciding whether upper-funnel earns its budget: last-touch is disqualifying; use MMM or an incrementality test.
- **Never let one single-touch model drive a reallocation alone.** Require a second lens before cutting a channel: a different model, an MMM read, a holdout, or zero-party data.
- **Triangulate with zero-party data.** A "How did you hear about us?" field on signup captures the touch the customer consciously credits, which no tracking model sees. It is biased (people misremember, over-credit brand) but it catches untracked and offline sources the pixel misses. Cross-reference it with the software attribution.
- **State the model on every report.** A conversion figure without its attribution model attached is unreadable. "Revenue by channel (last non-direct, 30-day window)" is a claim you can evaluate. "Revenue by channel" is not.

## 8. Common Failures

- **Last-click drives a budget cut.** The most common and most expensive error: killing awareness spend because last-click shows it converting nothing, then watching pipeline dry up a quarter later. Fix: never reallocate on a single-touch model; require a holdout or MMM.
- **Treating data-driven as truth.** Assuming the algorithm removed the bias. It moved it somewhere you cannot see and it still cannot credit untracked touches. Fix: validate DDA against incrementality.
- **Ignoring tracking decay.** Reading MTA as if coverage were complete while consent rates and cookie loss quietly erode it. Fix: monitor match/coverage rates; lean on MMM and experiments as coverage falls.
- **Confusing present with incremental.** Rewarding channels that were on the path but caused nothing. Fix: run holdouts on the channels that look best in attribution, especially retargeting and brand search.
- **No model stated.** Shipping conversion numbers with no attribution model or window attached. Fix: label every attributed metric with its model and window.
