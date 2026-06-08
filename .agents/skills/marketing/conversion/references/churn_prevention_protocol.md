# Churn Prevention Protocol

> **Goal**: Prevent voluntary and involuntary churn through systematic intervention at every exit point.

## Contents

- [1. Churn Classification](#1-churn-classification)
- [2. Cancel Flow Design](#2-cancel-flow-design)
- [3. Dunning Sequences (Involuntary Churn)](#3-dunning-sequences-involuntary-churn)
- [4. Re-Engagement Sequences (Ghost Users)](#4-re-engagement-sequences-ghost-users)
- [5. Proactive Churn Signals](#5-proactive-churn-signals)
- [6. Win-Back Campaigns](#6-win-back-campaigns)
- [7. Metrics](#7-metrics)

## 1. Churn Classification

| Type | Cause | Intervention Point |
|------|-------|--------------------|
| **Voluntary** | User decides to leave (dissatisfied, found alternative, no longer needs) | Cancel flow, exit survey, save offer |
| **Involuntary** | Payment failure (expired card, insufficient funds) | Dunning sequence, card update prompts |
| **Delinquent** | User ghosts — stops using, stops paying | Re-engagement sequence |

**Reality**: ~20-40% of SaaS churn is involuntary. Fixing dunning alone can recover significant revenue.

## 2. Cancel Flow Design

The cancel flow is a conversion funnel in reverse. Every step is an opportunity to save.

### Flow Architecture
```
Cancel button → Exit survey → Dynamic save offer → Confirmation → Downgrade option
```

### Exit Survey (Mandatory, 1 Question)
Present 4-6 reasons — the selection determines the save offer.

| Reason | Dynamic Save Offer |
|--------|-------------------|
| "Too expensive" | Discount (20-30% for 3 months) or downgrade to cheaper tier |
| "Missing features" | Roadmap preview + timeline for requested feature |
| "Switching to competitor" | Comparison data + personal onboarding session |
| "Not using it enough" | Usage tips + pause option (freeze account 1-3 months) |
| "Just need a break" | Pause subscription (keep data, no charge) |
| "Other" | Human follow-up (CS outreach within 24 hours) |

### Rules
- **Never make cancellation hard to find**. Dark patterns destroy trust and generate chargebacks.
- **Offer pause before cancel**. Many users who "cancel" would happily pause.
- **Downgrade before cancel**. Free tier > lost customer.
- **Show what they'll lose**. "You have 47 projects and 3 team members. They'll lose access too."

## 3. Dunning Sequences (Involuntary Churn)

### Pre-Failure Prevention
- **7 days before expiry**: Email + in-app banner: "Your card ending in 4242 expires soon."
- **3 days before**: Reminder with one-click update link.
- **Day of**: Final warning.

### Post-Failure Recovery (Card Declined)
- **Day 0**: "Payment failed" email with update link. Retry payment automatically.
- **Day 3**: Second attempt + email. "We tried again — still failing."
- **Day 7**: Warning: "Your account will be restricted in 7 days."
- **Day 10**: Restrict features (read-only mode, not deletion).
- **Day 14**: Final email: "We'll keep your data safe. Update your card to continue."
- **Day 30**: Account hibernated (data preserved, access removed).

### Retry Strategy
- Retry declined cards 3-4 times over 14 days.
- Retry on different days of the week (some banks have daily limits).
- Retry at different amounts (if multi-item, try the smallest charge first).

## 4. Re-Engagement Sequences (Ghost Users)

**Trigger**: 14-30 days of inactivity (calibrate to your product's natural usage cadence).

| Timing | Message | Tone |
|--------|---------|------|
| Day 14 | "We noticed you haven't been around" | Helpful, not desperate |
| Day 21 | "Here's what's new since you left" | Value-focused (new features) |
| Day 28 | "Is there anything we can help with?" | Human, personal outreach |
| Day 35 | "We'd love your feedback" | Exit survey if no response |

**Rule**: If no response after 4 touches, stop. Don't spam inactive users.

## 5. Proactive Churn Signals

Monitor these leading indicators — intervene before they cancel.

| Signal | Risk Level | Intervention |
|--------|-----------|-------------|
| Login frequency dropping | Medium | In-app "Welcome back" + feature tip |
| Core feature usage declining | High | Personalized email: "Try [feature]" |
| Support ticket spike | High | Proactive CS outreach |
| Billing page visits | Critical | Immediate CS flag + save offer prep |
| Team members removed | Critical | "Downsizing?" outreach with downgrade options |

## 6. Win-Back Campaigns

For users who already cancelled:

| Timing | Approach |
|--------|---------|
| 7 days post-cancel | "We've already made improvements based on feedback like yours" |
| 30 days | "Here's what's changed since you left" (feature changelog) |
| 90 days | "Come back" offer (discount or extended trial of new tier) |
| 6 months | Final attempt with major product update |

**Rule**: Maximum 4 win-back emails. Respect the departure.

## 7. Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| Gross churn rate | % of customers lost / total customers | < 5% monthly |
| Net churn rate | Gross churn minus expansion revenue | < 0% (net negative churn) |
| Save rate | % of cancel attempts that were saved | > 15% |
| Dunning recovery rate | % of failed payments recovered | > 50% |
| Time to churn | Average days from first sign of risk to cancel | Track and extend |
