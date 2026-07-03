# Churn and Win-Back

> Classify the churn before you fight it. Voluntary churn needs a reason-aware save path. Involuntary churn needs dunning. Win-back is a separate, capped campaign. Keep the exit honest at every step.

## Contents

- [1. Classify first](#1-classify-first)
- [2. Proactive risk signals](#2-proactive-risk-signals)
- [3. The cancel and save flow](#3-the-cancel-and-save-flow)
- [4. Save offers by reason](#4-save-offers-by-reason)
- [5. Dunning: involuntary churn](#5-dunning-involuntary-churn)
- [6. Win-back: users already gone](#6-win-back-users-already-gone)
- [7. The dark-pattern line](#7-the-dark-pattern-line)
- [8. Metrics](#8-metrics)

## 1. Classify first

The intervention depends entirely on the type. Do not run a save offer at a user whose card just expired.

| Type | Cause | Where you intervene |
|------|-------|---------------------|
| **Voluntary** | User chose to leave: dissatisfied, found an alternative, no longer needs it | Cancel flow, exit reason, save offer |
| **Involuntary** | Payment failed: expired card, insufficient funds, bank decline | Dunning sequence, card-update prompt |
| **Delinquent** | User drifted off: stopped using, then stopped paying | Re-engagement, then win-back |

Reality: roughly 20 to 40% of subscription churn is involuntary. Fixing dunning recovers real revenue and requires zero persuasion, so it is usually the highest-return churn work you can do first.

## 2. Proactive risk signals

The cheapest save happens before the user reaches the cancel button. Watch leading indicators and intervene early.

| Signal | Risk | Intervention |
|--------|------|--------------|
| Login frequency falling | Medium | In-app "welcome back" + a fitting tip |
| Core-feature usage declining | High | Targeted email: re-introduce the feature tied to their goal |
| Support tickets spiking | High | Proactive outreach from a human |
| Billing or cancel page visited | Critical | Flag for immediate save-offer prep |
| Seats or teammates removed | Critical | "Downsizing?" outreach with a downgrade path |

Recency of meaningful action is the strongest single churn predictor. Falling recency is your earliest warning; act on it before the other signals appear.

## 3. The cancel and save flow

The cancel flow is a conversion funnel in reverse. Every step is a chance to save, but the exit stays reachable throughout.

```
Cancel -> Exit reason (1 question) -> Reason-aware save offer -> Confirm -> Downgrade option
```

Principles:
- **Keep cancel easy to find.** A hidden or multi-hurdle exit generates chargebacks and kills word of mouth. See section 7.
- **Offer pause before cancel.** Many users who click cancel would happily freeze for one to three months. Pausing keeps the data and the relationship.
- **Offer downgrade before losing them.** A free or cheaper tier beats an empty seat.
- **Show what leaves with them.** "You have 47 projects and 3 teammates who will also lose access." Concrete loss is the honest counterweight to leaving.
- **Ask one exit question.** The reason drives the offer. Keep it to a single, fast selection.

## 4. Save offers by reason

The exit reason determines the offer. A generic discount at everyone is lazy and it trains users to threaten cancellation for a coupon.

| Reason given | Fitted save offer |
|--------------|-------------------|
| Too expensive | Downgrade to a cheaper tier, or a time-boxed discount |
| Missing a feature | Roadmap status and timeline; a human follow-up if it is close |
| Switching to a competitor | Honest comparison + a personal onboarding session |
| Not using it enough | Usage tips + a pause option so the value has time to land |
| Just need a break | Pause the subscription: keep the data, stop the charge |
| Project or need ended | Let them go cleanly; offer to preserve the account for a later return |

Sequence the offers within a reason from least discount to most: pause, then downgrade, then discount. Reach for the discount last, because it is the most expensive and the easiest to abuse.

## 5. Dunning: involuntary churn

No human decided to leave here, so there is nothing to persuade. The job is to recover the payment and keep access up while you do.

### Before the failure
- **7 days before a card expires**: email + in-app banner, "Your card ending 4242 expires soon", one-click update.
- **3 days before**: reminder with the update link.
- **Day of**: final pre-expiry prompt.

### After a decline
- **Day 0**: "Payment failed" email with an update link. Retry automatically.
- **Day 3**: second retry + email, "We tried again, still no luck".
- **Day 7**: "Your account will be limited in 7 days."
- **Day 10**: restrict to read-only. Do not delete anything.
- **Day 14**: "We are keeping your data safe. Update your card to pick up where you left off."
- **Day 30**: hibernate the account. Data preserved, access removed.

### Smart retries
- Retry a declined card 3 to 4 times across ~14 days, not all on day one.
- Vary the day of week; some banks apply daily limits.
- For multi-item charges, retry the smallest amount first to clear a partial.
- Escalate the channel: if email is not landing, use an in-app modal or SMS.

Restrict before you delete, and keep the data safe throughout. A recovered card should restore full access instantly.

## 6. Win-back: users already gone

Separate from re-engagement (which targets a quiet but still-subscribed user, in `references/email_lifecycle.md`). Win-back targets people who already left. Respect the departure and cap the campaign.

| Timing after cancel | Approach |
|---------------------|----------|
| ~7 days | "We already shipped improvements from feedback like yours" (only if true) |
| ~30 days | "Here is what changed since you left" (a real changelog) |
| ~90 days | A come-back offer: a discount or an extended trial of a newer tier |
| ~6 months | A final note tied to a genuine, significant update |

Rules:
- Maximum four win-back emails. Then stop and suppress.
- Only claim improvements you actually made. A fabricated "we fixed it" is a trust breach that the returning user discovers immediately.
- Tie the ask to what they left over. Someone who churned on price hears a pricing change; someone who churned on a missing feature hears that the feature shipped.

## 7. The dark-pattern line

Retention beats persuasion, but never by trapping the user. These tactics buy one month and cost trust, chargebacks, refunds, and word of mouth. They are out of bounds.

- Hiding the cancel button, or burying it behind a support-ticket or phone-call requirement when signup was one click.
- Pre-checking a downgrade, a pause, or a "keep my plan" that the user did not choose.
- Confusing double-negatives on the confirm ("Uncheck to not keep your subscription").
- Adding fake steps or forced delays whose only purpose is to exhaust the user into staying.
- Making the "cancel" button quiet and the "stay" button loud past the point of a fair default.

A save offer persuades with a real alternative. A dark pattern removes the choice. Keep the exit as easy as the entrance and win the stay on merit.

## 8. Metrics

| Metric | Definition | Rough target |
|--------|------------|--------------|
| Gross churn rate | Customers lost / total customers | < 5% monthly |
| Net churn rate | Gross churn minus expansion revenue | < 0% (net negative churn) |
| Save rate | Cancel attempts saved / cancel attempts | > 15% |
| Dunning recovery rate | Failed payments recovered | > 50% |
| Involuntary share | Involuntary churn / total churn | Know it; it is often 20 to 40% |
| Win-back rate | Returned / targeted | Track, keep the send count capped |

Read save rate and dunning recovery separately. A healthy dunning recovery can mask a poor voluntary save rate, and the two need different fixes.
