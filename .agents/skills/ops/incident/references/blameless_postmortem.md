# Blameless Postmortem

> The outage already happened. The only thing left worth extracting is the learning that stops the next one. You get that learning only if people tell the truth, and people tell the truth only when they will not be punished for it. Blame buys silence, and silence buys the next outage.

## Contents
- The no-blame rule
- When to write it
- Structure
- Building the timeline
- 5-whys on contributing factors
- Action items that survive
- Anti-patterns

## The no-blame rule

The postmortem attacks the system, never the person. "A human ran the wrong migration" is not a root cause; it is a symptom. The real questions are: why did the system let a single command take down production, why was there no guard, no review gate, no staged rollout, no fast rollback. A person made a normal mistake inside a system that turned it into an outage. Fix the system.

Concretely:
- Name roles and actions, not individuals as culprits ("the deploy was pushed", not "Sam broke it").
- Assume everyone acted reasonably with the information they had at the time. Judge decisions by what was knowable then, not by what you know now (no hindsight bias).
- If a person feels safe enough to say "I did X and it caused this", that is a gift. Treat it as the most valuable input in the room, never as an admission of guilt.

A blameful postmortem is worse than none: it teaches everyone to hide the next mistake.

## When to write it

Draft it while the memory is fresh, right after recovery, not weeks later when the timeline has gone fuzzy. Required for every SEV1 and SEV2. Optional but encouraged for a SEV3 that revealed something surprising.

## Structure

A workable postmortem has these sections:

1. **Summary.** Two or three sentences: what broke, impact, duration, how it was mitigated.
2. **Impact.** Users affected, features down, duration, and any money, data, or trust cost.
3. **Timeline.** Timestamped sequence from first signal to resolution (see below).
4. **Contributing factors.** The chain of conditions that made it possible, via 5-whys.
5. **What went well.** Detection, mitigation, teamwork that worked. Keep the good muscle memory.
6. **What went badly / where we got lucky.** Honest gaps, and the near-misses that only luck covered.
7. **Action items.** Concrete changes, each with an owner and a due date.

## Building the timeline

Facts with timestamps, in order, no interpretation:

- When the problem actually started (often before anyone noticed).
- When it was detected, and by what: an alert, or a customer.
- Key decisions and actions: severity declared, IC assigned, mitigation applied.
- When the signal recovered, and when resolved was declared.

The gap between "started" and "detected" is often the most useful number in the whole document. If customers noticed before your monitoring did, that gap is an action item.

## 5-whys on contributing factors

Ask "why" past the first satisfying answer until you reach something structural you can actually change.

Worked example:
- The checkout API returned errors. **Why?** A deploy shipped a config that pointed at a dead cache host.
- **Why did that config ship?** The staging config was copied to production by hand.
- **Why was it copied by hand?** There is no automated config promotion, it is a manual step.
- **Why did nothing catch the bad host?** There is no health check on the cache connection at boot.
- **Why did it take 20 minutes to notice?** The alert watches error rate, and the errors were being swallowed and retried silently.

Root causes found: manual config promotion, no boot-time health check, swallowed errors that hid the signal. Three action items, none of which is "be more careful".

Most incidents have more than one contributing factor. Trace each thread; do not stop at the first one that feels like enough.

## Action items that survive

An action item is real only if it has an owner and a date. "We should improve monitoring" is a wish, not an action.

- **Owned.** One named person is accountable, even if others do the work.
- **Specific.** "Add a boot-time health check on the cache connection", not "make deploys safer".
- **Dated.** A due date, tracked in the normal backlog like any other work.
- **Prioritized by recurrence risk.** The change that makes this whole class of failure impossible outranks the one that patches this single instance.

Close the loop: action items that are filed and forgotten mean the next identical outage was preventable and you chose not to.

## Anti-patterns

- Naming a person as the root cause. The system that allowed it is the root cause.
- Stopping 5-whys at the first human error. Keep going to the structural gap.
- Action items with no owner or no date. They will not happen.
- Writing it weeks late from memory. The details, and the honesty, are gone by then.
- A wall of blame that makes people defensive. You will get a clean-looking document and zero real learning.
