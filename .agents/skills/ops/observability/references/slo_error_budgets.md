# SLOs and Error Budgets

## Contents
- The vocabulary
- Choosing a good SLI
- Setting the SLO
- The error-budget math
- Burn rate
- Error-budget policy
- Common mistakes

## The vocabulary

Three terms, in strict order:

- **SLI (Service Level Indicator)**: a measured number describing service quality, almost always a ratio of good events to valid events over a window. Example: (requests served under 300ms and with a 2xx/3xx status) / (all valid requests). An SLI is measured, not promised.
- **SLO (Service Level Objective)**: the internal target for an SLI over a window. Example: 99.9% of valid requests are good over a rolling 28 days. An SLO is a promise you make to yourself and your users.
- **SLA (Service Level Agreement)**: a contract with financial or legal consequences if an SLO is missed. Your SLO should be stricter than any SLA, so you notice trouble before a customer invokes the contract.

Rule of thumb: SLA is looser than SLO is measured by SLI. If SLA equals SLO you have no safety margin before you owe money.

## Choosing a good SLI

A good SLI moves when users are unhappy and stays flat when they are fine. Test every candidate against that.

- Prefer the ratio form: good events / valid events. It is dimensionless, aggregates cleanly, and maps directly to a percentage target.
- Measure as close to the user as you can. A request that fails at the load balancer still failed the user, even if your app never saw it. Server-side-only SLIs miss the failures that never reached the server.
- Define "good" and "valid" precisely and in advance. Is a 429 (rate-limited) good, bad, or excluded? Is a 404 on a genuinely missing resource an error or expected behavior? Are health-check pings excluded from "valid"? Write it down; ambiguity here poisons every later number.
- Pick SLIs per user journey, not per machine. "Checkout succeeds" matters; "pod #7 CPU" does not belong in an SLO.

Common SLI types:
- **Availability**: fraction of valid requests that succeeded.
- **Latency**: fraction of valid requests served faster than a threshold. Note it is a fraction over a threshold, not "the average latency." An SLO is stated as "99% under 300ms," never as "average 300ms."
- **Quality / correctness**: fraction of responses that were actually correct (for pipelines, search, ML serving).
- **Freshness**: fraction of data served within an acceptable staleness bound (for caches, replicas, feeds).

## Setting the SLO

The target comes from user expectation and cost, not from a wish for more nines.

- Ask what level of failure users actually notice and tolerate. Below that line, tightening the SLO spends real engineering money for reliability nobody perceives.
- Every extra nine is roughly a 10x jump in effort and cost. 99% to 99.9% to 99.99% is not linear. Do not buy nines you do not need.
- 100% is the wrong target, always. It forbids all deploys, all experiments, all planned maintenance, and it is unachievable anyway because your dependencies are not 100%. An SLO of 100% is a promise to fail.
- Set the window explicitly (a rolling 28 or 30 days is common). The window defines how much bad time the budget represents and how fast good behavior "forgives" past failure.

## The error-budget math

The error budget is the failure you are allowed to spend:

```
error budget = 100% - SLO
```

Over a window, convert that to a concrete allowance. For a 99.9% SLO the budget is 0.1% of valid events.

Two ways to size it:

**By time** (rough intuition, assumes uniform traffic):

```
SLO      allowed unavailability
99%      ~7 hours 18 min per 30 days
99.9%    ~43 min 12 sec per 30 days
99.95%   ~21 min 36 sec per 30 days
99.99%   ~4 min 19 sec per 30 days
```

**By events** (the honest version, since traffic is never uniform):

```
budget of bad events = (1 - SLO) * total valid events in the window
```

Worked example: 99.9% SLO, 20,000,000 valid requests in 28 days.
- Allowed bad fraction = 1 - 0.999 = 0.001.
- Budget = 0.001 * 20,000,000 = 20,000 bad requests for the whole window.
- After a spike burns 8,000 of them in one afternoon, 12,000 remain (60% budget left) with most of the window still to go.

Event-based is better than time-based whenever traffic is spiky: a five-minute outage during your nightly quiet hour costs far fewer bad events than the same five minutes at peak, and the budget should reflect that.

## Burn rate

Burn rate expresses how fast you are consuming the budget relative to the pace that would exactly exhaust it at the end of the window.

```
burn rate = (error rate over a window) / (1 - SLO)
```

- Burn rate 1 = you are spending the budget exactly on schedule; you would end the window at zero, on target.
- Burn rate 2 = you would exhaust the entire window's budget in half the window.
- Burn rate 14.4 = you would exhaust a 30-day budget in about 2 days.

Burn rate is what you alert on, because it captures both a sudden outage (very high burn over minutes) and a slow leak (mildly elevated burn over hours or days). A raw "SLO breached" alert only fires after the damage is done; burn rate warns while the budget is draining. The alerting policy for burn rate lives in the alerting reference.

## Error-budget policy

The budget is only useful if spending it changes behavior. Agree the policy before you need it, so it is a rule and not an argument mid-incident.

- **Budget remaining**: ship. Take reliability risk, run experiments, push features. Unspent budget is permission to move fast; a team that never touches its budget set the SLO too loose.
- **Budget exhausted**: freeze feature launches. Redirect effort to reliability (fix the top burners, add safeguards, pay down the debt that is spending the budget) until the SLO recovers over the window.
- Make the trade explicit and shared between the people who want features and the people who carry the pager. The error budget is the neutral arbiter that turns "is it reliable enough" from opinion into a number both sides agreed to in advance.

## Common mistakes

- Setting the SLO at 100%, or one nine short of the SLA. No margin, no room to deploy.
- Averaging latency instead of using a threshold-and-fraction ("average 300ms" instead of "99% under 300ms"). Averages hide the tail that users feel.
- Measuring the SLI only server-side and missing the failures that die at the edge before the app sees them.
- Sampling the events that feed the SLI. If the SLI is an estimate, the budget is fiction. Count SLI events fully.
- Writing an SLO with no error-budget policy. A target nobody acts on is decoration; the policy is the whole mechanism.
- One global SLO for a service with several distinct journeys. Checkout and a marketing page do not deserve the same target; set SLOs per journey.
