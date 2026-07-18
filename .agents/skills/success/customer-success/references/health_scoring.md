# Health Scoring

> A health score is a prediction about who will renew and who will leave. Build it from leading indicators tied to the customer's outcome, not from logins, and check that it actually predicts. A score you never validate is astrology with a dashboard.

## Contents

- [1. Leading vs lagging: why logins lie](#1-leading-vs-lagging-why-logins-lie)
- [2. The four dimensions of health](#2-the-four-dimensions-of-health)
- [3. Designing the score](#3-designing-the-score)
- [4. Scoring mechanics](#4-scoring-mechanics)
- [5. Validate the score against real churn](#5-validate-the-score-against-real-churn)
- [6. From color to action](#6-from-color-to-action)
- [7. Anti-patterns](#7-anti-patterns)
- [8. Metrics](#8-metrics)

## 1. Leading vs lagging: why logins lie

A lagging indicator tells you what already happened: renewed, churned, downgraded. By the time it moves, the outcome is set and you can do nothing. A leading indicator moves before the outcome and gives you time to act.

Logins are the most common health signal and one of the weakest. Presence is not value. A customer can log in every day and still be about to churn, because they never reached the outcome they bought, or the one person who used it just left. Track what the customer does that produces their result, not that they showed up.

The test for any candidate signal: if this number moves, does the probability of renewal move with it. If not, it is decoration.

## 2. The four dimensions of health

A single metric cannot carry health. Combine four dimensions, each answering a different question.

| Dimension | Question it answers | Example signals |
|-----------|---------------------|-----------------|
| **Outcome** | Are they getting the result they bought | Reached the value milestone, business KPI moving, ROI evident |
| **Adoption breadth** | How deeply is it embedded | Active seats vs licensed, key workflows in use, depth not just frequency |
| **Relationship** | How safe is the account politically | Multi-threaded, exec sponsor engaged, champion still in seat |
| **Sentiment** | What do they feel and say | NPS or CSAT, support tone, QBR engagement, escalation history |

Outcome is the heaviest. A customer reaching their desired outcome forgives a lot; one who is not will churn even while happy with your support. Relationship is the quiet one people skip: a single-threaded account tied to one champion is one resignation away from red, no matter how good the usage looks.

## 3. Designing the score

- **Weight toward the desired outcome.** The signals that predict renewal are the ones tied to why this customer bought. A marketing team bought pipeline; their health is campaigns shipped and leads sourced, not seats provisioned.
- **Segment the model.** An enterprise account and an SMB account do not share thresholds. Small accounts run hotter and colder; large accounts move slowly and hide risk behind contract length. Score them on separate scales.
- **Keep it legible.** A score a human cannot explain is a score no one will act on. If you cannot say in one sentence why an account is yellow, the model is too clever. Favor a handful of weighted signals over a black box.
- **Use both absolute and trend.** A high but falling adoption number is more dangerous than a low but climbing one. Recency of meaningful action is the strongest single predictor; weight the direction, not only the level.

## 4. Scoring mechanics

- **Three states, not ten.** Green (on track, expansion candidate), Yellow (drifting, intervene now), Red (at risk, save motion). More granularity than that invites false precision and slows the response.
- **Thresholds per segment**, calibrated to observed churn, not guessed.
- **Decay stale signals.** A milestone hit six months ago is not current health. Weight recent action higher and let old wins fade.
- **Cap the vanity terms.** Any single presence metric (logins, page views) contributes a small slice at most, so it can never turn an account green on its own.

## 5. Validate the score against real churn

This is the step most teams skip and the one that makes the score worth trusting. A health score is a hypothesis. Test it.

- Pull the accounts that churned last quarter and check what color they were 90 days before. If most were green, the model is blind and needs rebuilding.
- Pull green accounts and confirm they renew and expand at a higher rate than yellow and red. If green does not out-renew red, the colors mean nothing.
- Re-calibrate on a regular cadence. Product changes, the market shifts, and last year's predictive signal goes stale.

A score that does not separate churners from renewers is not a health score. It is a comfort blanket.

## 6. From color to action

A score exists to trigger a motion. If nothing changes when an account turns yellow, delete the score.

| Color | Meaning | Motion |
|-------|---------|--------|
| **Green** | On track, value proven | Nurture, ask for the expansion, request the reference |
| **Yellow** | Drifting, early risk | Diagnose the failing dimension, targeted intervention, re-set the success plan |
| **Red** | At risk | Root-cause diagnosis, human outreach, save play or managed exit |

Yellow is where the payoff is. Red is often too late and green needs little. Build the team's day around the yellow queue.

## 7. Anti-patterns

- **Single-signal health.** Logins as the whole score. The most common failure and the easiest to fool.
- **The unvalidated model.** A score no one has ever checked against actual churn. It feels rigorous and predicts nothing.
- **Green by default.** New accounts auto-scored green before they have done anything, hiding a stalled onboarding until the renewal misses.
- **Gaming for the deck.** Nudging colors so the board slide looks calm. The number exists to be honest, not flattering. A green forecast on a red account is a lie you tell yourself first.

## 8. Metrics

| Metric | Definition | Why it matters |
|--------|------------|----------------|
| Predictive accuracy | Share of churned accounts that were red or yellow before churn | Tells you the score works |
| Green renewal rate | Renewal rate of green accounts | Should clearly beat red |
| Yellow recovery rate | Yellow accounts moved back to green | Measures whether intervention works |
| Coverage | Share of accounts with a current, non-stale score | An uncovered account is an unmanaged one |

Read predictive accuracy first. Every other health metric assumes the score is real, and only this one proves it.
