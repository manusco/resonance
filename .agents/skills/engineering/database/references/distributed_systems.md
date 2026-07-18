# Distributed Systems: mental models for things that fail

> **Objective**: The moment a write leaves one process and crosses a network, "it worked" stops being a yes/no. These are the durable models for reasoning about systems where the network drops, duplicates, delays, and reorders. Reach for them before you write the happy path, not after the 3am page.

The core shift: a local function call either returns or throws. A remote call has a third outcome, unknown. The request may have succeeded with a lost response, failed cleanly, or still be running. Every model below exists to make that third outcome survivable.

## Contents
- CAP and consistency models
- Idempotency and the exactly-once illusion
- The outbox pattern and sagas
- Back-pressure and queueing
- Error budgets as a decision gate
- Reversibility: one-way vs two-way doors
- FMEA: failure-mode thinking
- Quick reference

## CAP and consistency models

CAP states that during a network **partition** (P), a system must choose between **consistency** (C, every read sees the latest write) and **availability** (A, every request gets a non-error response). You do not get to skip partitions; on a real network they happen. So the honest reading is: when the network splits, do you refuse to answer (CP) or answer possibly-stale (AP)?

PACELC is the useful extension: **else** (E), when there is no partition, you still trade **latency** (L) against **consistency** (C). A globally strong store pays a round-trip to a quorum on every write even when the network is healthy. There is no free strong consistency.

Consistency is a spectrum, not a switch. From strongest to weakest:

| Model | Guarantee | Cost | Use when |
| :--- | :--- | :--- | :--- |
| Linearizable (strong) | Every read sees the most recent write, single global order | Highest latency, lowest availability under partition | Money, inventory counts, uniqueness (usernames), locks |
| Sequential | One global order, not tied to real time | High | Rarely chosen directly |
| Causal | Effects never seen before their cause | Medium | Comments after posts, reply threads, collaborative edits |
| Read-your-writes | You see your own writes immediately | Low, often client-pinned | Profile edits, "you just posted this" |
| Monotonic reads | Reads never go backward in time | Low | Feeds, dashboards |
| Eventual | Replicas converge if writes stop | Lowest latency, highest availability | View counts, presence, caches, analytics |

The decision rule: **pick the weakest model that is still correct for the invariant you must hold.** If two users can never both claim the last seat, that is a strong-consistency (CP) invariant and no amount of caching changes it. If a like count is off by three for two seconds, eventual is correct and strong consistency is wasted money and latency. Most systems are a mix: strong for the ledger, eventual for the timeline.

Trap: "eventually consistent" does not mean "consistent after a short wait." It means consistent only if writes stop, which they never do. Design reads to tolerate staleness explicitly (show a timestamp, disable the button, re-read before the irreversible step), do not assume the window is small.

## Idempotency and the exactly-once illusion

An unreliable network offers exactly three delivery guarantees:

| Guarantee | Mechanism | Failure mode |
| :--- | :--- | :--- |
| At-most-once | Send, never retry | Lost messages, silent data loss |
| At-least-once | Retry until acknowledged | Duplicate delivery |
| Exactly-once | (delivery) does not exist | It is a marketing claim |

You cannot achieve exactly-once *delivery* over a channel that can lose the acknowledgement. This is the Two Generals result: the sender can never be sure its message arrived, so it must either retry (risking duplicates) or give up (risking loss). What people mean by "exactly-once" is achievable, but it is built, not delivered:

> **at-least-once delivery + idempotent handler = exactly-once effect.**

Retry aggressively so nothing is lost, and make the handler safe to run twice so duplicates do no harm. The handler carries the guarantee, not the transport.

**Idempotency key pattern.** The caller generates a unique key per logical operation (a UUID, or a natural key like `order-4412-capture`). The server, inside one transaction:

1. Tries to insert the key into a `processed_requests` table with a unique constraint.
2. If the insert succeeds, this is the first time: do the work, store the response against the key, commit.
3. If the insert hits the unique violation, this is a replay: return the stored response, do no work.

The key insert and the effect must commit in the **same transaction**, or a crash between them reopens the double-execution window you were closing. Naturally-idempotent operations (`SET status = 'paid'`, `PUT` of a full resource) need no key. Operations that accumulate (`balance = balance + 10`, "send email", "charge card") are the dangerous ones; they need a key or a natural dedup guard.

## The outbox pattern and sagas

**The dual-write problem.** A handler often must do two things that must both happen or neither: update the database and tell the outside world (publish an event, call a webhook, charge a card). There is no transaction that spans your database and an external system. So this code is broken:

```
db.commit(order)          # (1) succeeds
payment.charge(order)     # (2) times out... did it charge? retry? unknown.
```

If (1) commits and (2) is lost, the order is paid in your DB but never charged. Flip the order and a crash after the charge but before commit charges a customer for an order you have no record of. There is no ordering of two independent commits that is safe.

**The outbox pattern** removes the second system from the critical path. Instead of calling out, you write the intent into an `outbox` table *in the same transaction* as the business change:

```
BEGIN;
  UPDATE orders SET status = 'confirmed' WHERE id = 4412;
  INSERT INTO outbox (id, topic, payload, status)
    VALUES (gen_uuid(), 'payment.capture', '{"order":4412,"amount":900}', 'pending');
COMMIT;
```

One atomic commit. Either both rows land or neither does. A separate **relay** process then polls the outbox for `pending` rows, performs the external call, and marks the row `sent`. The relay retries on failure, so publishing is at-least-once, which is exactly why the consumer must be idempotent (see the idempotency key above).

### Worked example: a payment that must not double-fire

Requirement: confirming an order captures payment exactly once, even if the app crashes, the payment API times out, or the relay restarts mid-batch.

1. **Confirm** writes `orders.status = 'confirmed'` and an outbox row `payment.capture` with a deterministic idempotency key `capture-order-4412` in one transaction. If the process dies here, the transaction either committed fully or not at all.
2. **Relay** reads the pending outbox row and calls the payment provider, passing `Idempotency-Key: capture-order-4412` (every serious payment API accepts one). The provider dedups on its side: a retry with the same key returns the original charge, it does not charge twice.
3. **Ack**: on a success response the relay marks the outbox row `sent`. If the relay crashes *after* the provider charged but *before* marking `sent`, it will re-read the row and call again, but the same idempotency key makes the second call a no-op that returns the first result. The effect stays exactly-once.

The double-fire windows (crash after charge, timeout with unknown outcome, relay reprocessing a batch) all collapse because the provider key makes the capture idempotent and the outbox makes the intent durable. Neither piece alone is enough: the outbox without the key double-charges on relay retry; the key without the outbox loses the capture if the app crashes before it ever calls out.

### Sagas

When a workflow spans several services and no single database transaction can cover it, a **saga** models it as a sequence of local transactions, each with a **compensating action** that semantically undoes it. There is no rollback across services, so you move forward to a consistent state or run compensations backward to one.

Example: book trip = reserve flight, then reserve hotel, then charge card. If the hotel step fails, you do not "roll back" the flight, you run its compensation: cancel the flight reservation. Compensations are business logic (a refund, a cancellation, a release), not a database undo, and they must themselves be idempotent and retryable.

Two coordination styles:

| Style | Coordination | Good | Bad |
| :--- | :--- | :--- | :--- |
| Choreography | Each service reacts to events, no central brain | Loosely coupled, no single bottleneck | Hard to see the whole flow, cyclic event storms |
| Orchestration | One coordinator issues commands and tracks state | Flow is explicit and debuggable | The orchestrator is a component to build and keep available |

Default to orchestration once a saga has more than three steps or any branch: an explicit state machine you can query beats reconstructing the flow from scattered event logs.

## Back-pressure and queueing

**Little's Law** is the one equation to memorize:

> **L = lambda * W** : items in the system = arrival rate x average time in the system.

Rearranged, `W = L / lambda`. If 500 requests per second each sit in the system for 0.2s, you have `500 * 0.2 = 100` requests in flight on average. It holds for any stable system regardless of distribution, so it sizes thread pools, connection pools, and concurrency limits without a simulator.

**Utilization is the trap.** Queue wait does not rise linearly with load; it explodes as you approach capacity. For a simple M/M/1 queue the wait time scales with `rho / (1 - rho)`, where `rho` is utilization:

| Utilization | Relative wait in queue |
| :--- | :--- |
| 50% | 1x |
| 80% | 4x |
| 90% | 9x |
| 95% | 19x |
| 99% | 99x |

This is why a system that looks fine at 70% falls over at 90% for "no reason": you did not add much load, you crossed into the steep part of the curve. Plan capacity for the knee (60-75%), never for 100%.

**The unbounded queue is a hidden failure.** When arrival rate exceeds service rate, a bounded queue rejects, but an unbounded queue *accepts everything and grows*. Latency climbs without limit while memory fills, and the system does not fail fast, it fails slow and then dies all at once (OOM, or every request timing out on stale work). An unbounded queue does not absorb overload, it hides it and defers the crash to the worst possible moment.

**Back-pressure** is the fix: when you cannot keep up, tell the caller. Concretely:

- Bound every queue. A full bounded queue that rejects is more honest than an unbounded one that lies.
- Shed load explicitly: return `429 Too Many Requests` or `503`, ideally with `Retry-After`. A fast rejection lets the caller back off; a slow accept-then-timeout wastes work on both sides.
- Prefer dropping the newest work under overload for user-facing latency, or the oldest when freshness matters (stale queue entries are often already abandoned by the client).
- Propagate the signal upstream. Back-pressure that stops at one hop just moves the unbounded queue one layer out.

## Error budgets as a decision gate

An **SLO** (service level objective) sets the target, say 99.9% of requests succeed over 30 days. The inverse is the **error budget**: 0.1%, roughly 43 minutes of full outage per month, or the equivalent trickle of errors. The budget reframes reliability from an argument ("is this stable enough to ship?") into a number both sides can read.

The gate works like this:

| Budget state | Signal | Action |
| :--- | :--- | :--- |
| Budget healthy | Failures well under target | Ship features, take reasonable risk, this is the point of having a budget |
| Budget burning fast | Error rate would exhaust it before the window ends | Investigate now, this is an early warning |
| Budget exhausted | SLO missed | Freeze feature launches, spend all effort on reliability until the budget recovers |

The budget turns "should we slow down?" into a policy instead of a debate. It also stops the opposite failure: a service comfortably inside its budget does not need more nines, and burning engineering effort to gold-plate reliability nobody asked for is its own waste. Spend the budget deliberately; an unspent budget is unshipped features.

## Reversibility: one-way vs two-way doors

Before deciding how much caution a change deserves, classify the door.

- **Two-way door**: cheap to reverse. Walk through, and if it is wrong, walk back. A feature flag, a config value, a new endpoint behind a flag, a reversible deploy. Decide fast, keep ceremony low, optimize for learning speed. Treating a two-way door as one-way is its own cost: it burns time and reviews on a decision you could simply undo.
- **One-way door**: hard or impossible to reverse. Dropping a column, deleting data, changing a public API contract others depend on, sending an email or push to a million users, moving money, publishing a breaking schema change. Slow down, require review, add guardrails (dry-run, backup, staged rollout, a kill switch), and prefer a reversible approximation first (soft-delete before hard-delete, deprecate before remove, additive schema change before destructive one).

The frame is a caution dial, not a speed limit. Match the review weight to the reversibility: a staff reviewer should not gate a flag flip, and nobody should hard-delete a production table on a hunch. Most "risky" changes have a two-way-door version if you look; reach for it, and reserve the heavy process for the doors that truly do not open twice.

## FMEA: failure-mode thinking

Failure Mode and Effects Analysis is the discipline of enumerating how a thing breaks *before* it breaks, in writing. Instead of building the happy path and reacting to incidents, you list the failure modes up front and decide which ones earn a mitigation.

For each component or step, fill a row:

| Failure mode | Cause | Effect | Detection | Mitigation |
| :--- | :--- | :--- | :--- | :--- |
| Payment API times out | Provider slow, network drop | Unknown charge state | Timeout metric, reconciliation job | Idempotency key + retry, outbox |
| Relay double-processes batch | Crash after charge, before ack | Risk of double charge | Duplicate charge alert | Idempotency key makes replay a no-op |
| Outbox grows unbounded | Relay down, publish failing | Latency and memory climb, events stale | Outbox depth metric, age alert | Alert on depth, bound ret/alert, page on backlog |
| DB primary fails over | Hardware, maintenance | Writes error for seconds | Health check, error rate | Retry with backoff, app tolerates brief write errors |

Rank rows by a rough **RPN** (Risk Priority Number) = Severity x Occurrence x Detection-difficulty, then fix from the top. The scores do not need to be precise; the value is the forced enumeration. The three questions that catch the most:

1. **What if this call never returns?** (timeout, hung connection) Every remote call needs a timeout and a plan for the unknown outcome.
2. **What if this runs twice?** (retry, duplicate delivery, double-click) If the answer is "corruption," you need idempotency.
3. **What if the dependency is down?** (degrade, queue, reject) Decide the behavior deliberately; the default (hang, then cascade) is the worst one.

Write the failure modes down where the next builder reads them. An enumerated failure mode with a decided mitigation is cheap; the same failure discovered in production is an incident.

## Quick reference

| Situation | Model | The move |
| :--- | :--- | :--- |
| "Can these two reads disagree?" | CAP / consistency | Pick the weakest model still correct for the invariant |
| "It might get called twice" | Idempotency | at-least-once + idempotent handler, key the mutation |
| "DB write plus external call" | Outbox | Write intent in the same transaction, relay publishes, consumer dedups |
| "Multi-service workflow" | Saga | Local transactions + compensations, orchestrate past 3 steps |
| "Slows down under load" | Little's Law / queueing | Bound queues, shed load, plan for the 60-75% knee |
| "Should we keep shipping?" | Error budget | Budget healthy ship, budget burnt freeze and fix |
| "How careful about this change?" | One-way / two-way door | Match caution to reversibility, prefer the reversible version |
| "How could this break?" | FMEA | Enumerate modes first, mitigate the top by RPN |
