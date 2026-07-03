# Severity Matrix

> Severity is a promise about response, not a description of your feelings. It sets who wakes up, how fast, and how loud you communicate. When impact sits between two levels, declare the higher one and downgrade later.

## Contents
- How to pick a severity
- SEV1: critical
- SEV2: major
- SEV3: minor
- SEV4: low
- The round-up rule
- Downgrading and upgrading

## How to pick a severity

Ask three questions in order:

1. How much of the product is unusable, and for how many users?
2. Is money, data, or safety at risk right now?
3. Is it getting worse on its own, or is it stable?

The worst answer sets the floor. A small user count with active data loss is still a SEV1. A large user count with a cosmetic glitch is a SEV3.

## SEV1: critical

**Impact.** Core product is down or unusable for most users. Active data loss or corruption. A security breach in progress. Payments or checkout fully broken. Safety risk to people.

**Response.**
- Page immediately, at any hour.
- Assign an Incident Commander before anything else.
- Update every 15 to 30 minutes, no exceptions.
- External status page goes to a major-outage state.
- Mitigate by the fastest reversible path now; the root cause waits.
- Executive and support leadership are notified, not asked.

## SEV2: major

**Impact.** A key feature is broken or badly degraded for many users, but a workaround exists or the core still functions. Significant latency. A subset of customers fully blocked. Elevated error rate that is not yet total.

**Response.**
- Page during business hours; on-call decides on out-of-hours paging.
- Name an IC.
- Update every 30 to 60 minutes.
- Status page shows degraded performance.
- Mitigate quickly, but a short controlled investigation before acting is acceptable if the system is stable.

## SEV3: minor

**Impact.** A non-critical feature is broken or a small user segment is affected. Cosmetic or low-severity bugs with a clear workaround. No money, data, or safety exposure.

**Response.**
- No page. Handle in working hours.
- An owner is enough; a full IC ceremony is overkill.
- Update stakeholders once or twice a day until closed.
- Usually no external status-page entry unless a customer asks.
- Often better routed straight to the normal bug and `/debug` flow.

## SEV4: low

**Impact.** Trivial. Minor visual defect, a typo in a rarely seen state, a slow non-critical background job. Effectively no user pain.

**Response.**
- Log it as a normal ticket. This is not really an incident.
- No paging, no IC, no status page.
- Fix it in the ordinary backlog.

## The round-up rule

If you are honestly unsure whether something is a SEV1 or a SEV2, call it a SEV1. Over-declaring wastes a little attention for a few minutes. Under-declaring means the right people find out too late, from customers instead of from you. The cost is not symmetric, so bias upward.

## Downgrading and upgrading

Severity is not fixed for the life of the incident.

- **Downgrade** once impact is provably smaller than first feared: fewer users, workaround confirmed, signal recovering. Announce the downgrade in the channel with the reason.
- **Upgrade** the moment impact grows: more surfaces failing, data loss discovered, mitigation not holding. Upgrading is not an admission of error, it is the process working.
- Every change in severity is stated explicitly and logged in the timeline with a timestamp.
