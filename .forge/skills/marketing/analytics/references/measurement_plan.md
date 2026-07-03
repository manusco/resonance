# Measurement Plan Protocol

> "If no decision changes when the number moves, do not track the number."

## Contents

- [1. The Top-Down Method](#1-the-top-down-method)
- [2. The Measurement Plan Table](#2-the-measurement-plan-table)
- [3. Event Taxonomy and Naming](#3-event-taxonomy-and-naming)
- [4. The Tracking Plan](#4-the-tracking-plan)
- [5. The Funnel](#5-the-funnel)
- [6. The North-Star Metric](#6-the-north-star-metric)
- [7. Guardrail Metrics](#7-guardrail-metrics)
- [8. Common Failures](#8-common-failures)

## 1. The Top-Down Method

Work in this order. Never reverse it.

1. **Decision.** What action will this data change? "Should we keep funding the webinar channel?" is a decision. "Understand our users" is not.
2. **Metric.** What single number would settle that decision? Pick one primary metric per question. If two numbers disagree, you have not defined the decision tightly enough.
3. **Event.** What is the minimum set of events and properties that computes that metric? Instrument only those.

The failure mode is bottom-up: teams log every click "to be safe", ship 400 events, and six months later nobody knows which are trustworthy, which are double-counted, or which query answers the actual question. Every event you add is a maintenance liability and a chance to be wrong. Add events on demand from a metric, not on spec.

### The one-sentence test
For every event in your plan, finish this sentence: "We track `event_x` because it lets us compute `metric_y`, which tells us whether to `decision_z`." If you cannot finish it, delete the event.

## 2. The Measurement Plan Table

The plan is a table, written before any instrumentation. One row per business question.

| Question (decision) | Primary metric | Definition (numerator / denominator / window) | Events + properties | Owner |
| :--- | :--- | :--- | :--- | :--- |
| Is paid search worth its spend? | Cost per activated user | Activated users from paid search / paid-search spend, 28-day window | `signup_completed`, `activation_reached` with `source` property | Growth |
| Is onboarding working? | Activation rate | Users reaching aha within 7 days / users who signed up, by cohort | `activation_reached`, cohorted on `signup_completed` | Product |
| Is the newsletter driving revenue? | Revenue per subscriber | Attributed revenue / active subscribers, 30-day | `subscribe_confirmed`, `purchase_completed` with attribution | Marketing |

The "Definition" column is where honest analytics lives or dies. A metric name is not a definition. "Conversion rate" needs a numerator, a denominator, and a time window, or two people will compute two different numbers and both will be "right".

## 3. Event Taxonomy and Naming

Events are a controlled schema, not a free-text log. Decide the convention once, enforce it forever.

### Naming convention
- **Format**: `object_action`, for example `checkout_started`, `plan_upgraded`, `video_played`. Some teams prefer `Object Action` title case; pick one and never mix.
- **Tense**: past tense. The event fires after the thing happened. `signup_completed`, not `complete_signup`.
- **Case**: `snake_case` everywhere, consistently. Casing drift (`SignUp` vs `sign_up`) silently forks your data into two events.
- **Granularity**: name the object and the action, not the UI. `cta_clicked` with a `location` property beats forty differently named button events. When the button moves, the property changes, the event survives, and history stays intact.

### Properties, not new events
Variation lives in properties, not in the event name. One `purchase_completed` event with `plan`, `amount`, `currency`, `coupon` properties, not `purchase_pro`, `purchase_annual`, `purchase_with_coupon`. This keeps the event count small and queries composable.

### Controlled property vocabulary
Fix the allowed values for high-value properties. `source` should be a closed set (`paid_search`, `organic`, `referral`, `email`, `direct`), not free text where `Paid Search`, `paidsearch`, and `ppc` all mean the same thing and none of them join.

### Identity
Decide how anonymous and known users stitch together before launch. An `anonymous_id` on first touch, aliased to a stable `user_id` at signup, is the usual pattern. Getting this wrong fractures every funnel that crosses the login boundary.

## 4. The Tracking Plan

The tracking plan is the single source of truth for what is instrumented. It is a living document (a sheet or a schema file in the repo), and code is expected to match it, not the reverse.

Each event entry carries:
- **Event name** (from the convention above).
- **Trigger**: the exact user or system action that fires it, stated so an engineer and an analyst read it the same way.
- **Properties**: name, type, allowed values, required or optional.
- **Which metric it feeds** (the back-reference to section 2).

### Governance rules
- **Version it.** Changes to the tracking plan are reviewed like schema migrations, because that is what they are.
- **No orphan events.** An event that feeds no metric does not ship.
- **No silent renames.** Renaming an event breaks every historical query on it. Add the new event, run both in parallel, migrate reports, then retire the old one.
- **Reconcile the money metrics.** Any metric tied to revenue is reconciled against the billing system or CRM on a schedule. If analytics and billing disagree on revenue, billing wins and analytics gets fixed.

## 5. The Funnel

A funnel is the ordered sequence of steps from stranger to realized value. Define the steps as events, measure the drop-off between each, and name the single worst step before proposing any fix.

- Measure the funnel by **cohort**, not as a blended all-time average. A blended funnel hides whether last month's cohort converts worse than last year's.
- The bottleneck is the step with the steepest drop relative to its benchmark, not simply the lowest absolute number. A 60% drop at a step that normally drops 20% matters more than a 90% drop at a step that always drops 90%.
- Do not optimize a downstream step while an upstream step leaks. Fixing checkout is wasted if activation is broken.

## 6. The North-Star Metric

The north-star is the one metric that best proxies the value customers actually receive, and that the business grows by growing.

- It measures **delivered value**, not vanity. "Weekly active teams that sent a message", not "total signups". "Nights booked", not "app downloads".
- It leads revenue rather than being revenue. Revenue is the lagging result; the north-star is the behavior that produces it, so you can act on it early.
- It is **one** metric. A north-star committee of six numbers is a dashboard, not a north-star. Supporting metrics sit under it; they do not share the crown.

### Anti-patterns
- Registered users (counts people who signed up once and vanished).
- Pageviews or sessions alone (traffic is not value).
- Cumulative totals (only ever go up, so they hide decline).

## 7. Guardrail Metrics

Every optimization target needs guardrails: metrics you agree not to harm while chasing the primary one. You can juice activation by spamming, or lift conversion by hiding the price; guardrails catch the win that is actually a loss.

Typical guardrails: unsubscribe rate, refund rate, latency or load time, support ticket volume, long-term retention. Set a threshold; if the experiment wins the primary metric but breaches a guardrail, it does not ship.

## 8. Common Failures

- **Instrumenting bottom-up.** Logging everything and hunting for insight later. Fix: derive events from metrics from decisions.
- **Metric without a definition.** Reporting "conversion" with no numerator, denominator, or window. Fix: the definition column is mandatory.
- **Casing and vocabulary drift.** `SignUp` and `sign_up` as two events; `ppc` and `paid_search` as two sources. Fix: a controlled schema and a linted tracking plan.
- **Silent breakage.** An app release stops firing an event; the funnel quietly craters and nobody notices for weeks. Fix: monitor event volume and alert on anomalies.
- **Reporting a change the week a tracking change shipped.** Attributing a metric jump to a campaign when the real cause was a measurement change. Fix: annotate the timeline with instrumentation changes.
