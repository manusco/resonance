---
name: resonance-ops-incident
description: The Incident Commander. Drives a live production incident from detection to a blameless postmortem: triage, declare severity, assign command, mitigate before root-cause, communicate on a cadence, verify recovery. Use when production is down, an active incident or outage is in progress, a SEV1 is declared, you just got paged, latency or error rates are spiking, or a deploy broke prod. Manual-only: it has real side effects (rollbacks, feature-flag flips, status-page updates, stakeholder messages), so a human must invoke it.
archetype: procedure
---

# /resonance-ops-incident: stop the bleeding first, learn second

> **Role:** the Incident Commander (IC).
> **Invoked as:** `/incident` (to run a live production incident).
> **Input:** A live signal that production is degraded or down: a page, an alert, an error/latency spike, or a user report you have confirmed.
> **Output:** A mitigated and verified system, a captured incident timeline, and a drafted blameless postmortem with owned action items.
> **Definition of Done:** The incident is mitigated and recovery is verified against a real signal (not a hunch). A single IC owned the response. The timeline is captured from detection to resolution. A blameless postmortem is drafted: 5-whys on contributing factors, action items each with a named owner, no person blamed. Stakeholders were told it is resolved.

**Iron Law: Mitigate before you diagnose.** While users are down, your job is to stop the bleeding, not to find the elegant root cause. Roll back or flip the feature flag first. The investigation happens after the graph is green. A beautiful RCA delivered an hour late is a failure.

This procedure has real side effects. Do not auto-fire it. A human declares the incident and stays in the loop for every irreversible action (rollback, flag flip, external status update).

## Prerequisites (fail fast)

- [ ] The signal is real and confirmed, not a single flaky alert. If you cannot confirm impact (a graph, a reproduced error, a second corroborating report), your first act is to confirm it, then continue.
- [ ] You know which surface is affected and roughly how many users. If not, triage (step 1) establishes it before you declare severity.
- [ ] You can reach the levers to mitigate: deploy/rollback access, feature-flag console, or the owner who has them. If you cannot, escalating to someone who can is step 3.

## Algorithm

Copy this checklist and tick items as you go. Do not skip a step to save time while users are down; skipping mitigation to hunt the root cause is the classic failure this skill exists to prevent.

1. **Detect and triage.** Confirm the signal is real and scope the blast radius: what is broken, since when, how many users, is it getting worse. Pull the graph or reproduce the error before you act. -> verify: impact is confirmed with evidence and written down (surface, start time, affected users, trend).
2. **Declare severity.** Map the impact to SEV1-SEV4 using clear criteria (see severity_matrix.md). When it is between two levels, round up: over-declaring costs a little attention, under-declaring costs the outage. -> verify: a severity is stated out loud and the criterion that set it is named.
3. **Assign an Incident Commander.** One named person owns the response and coordinates; everyone else executes. If nobody has claimed it, you are the IC now, say so explicitly. The IC does not fix and coordinate at the same time on a SEV1: delegate the hands-on work and keep the overview. -> verify: exactly one IC is named and acknowledged.
4. **Stabilize and mitigate.** Restore service by the fastest reversible path: roll back the last deploy, flip the feature flag off, fail over, or shed load. Do the root-cause investigation later. Prefer the action you can undo. -> verify: the mitigation is applied and the primary signal (error rate, latency, availability) is measurably recovering, not just "should be fixed".
5. **Communicate on a cadence.** Post a first update fast (we are aware, impact, IC name, next update time) and then keep to the promised interval until resolved (see comms_protocol.md). Separate the internal channel from the external status page; never leak internal speculation to customers. -> verify: at least one update is out and the next update time is committed.
6. **Resolve and verify recovery.** Declare resolved only when the signal is healthy on real traffic and has held for a sane window, not on the first green data point. Confirm the specific thing users reported is actually working. -> verify: the health signal is stable over the hold window and the original symptom is gone.
7. **Write a blameless postmortem.** Draft it while memory is fresh (see blameless_postmortem.md): a factual timeline, contributing factors traced via 5-whys, and action items each with a named owner and a due date. Attack the system and the gaps in it, never the person who typed the command. -> verify: the postmortem has a timeline, 5-whys on the causes, and at least one action item with a real owner, and contains no blame.

## Recovery

- Cannot confirm the signal is real -> do not declare a SEV and do not roll anything back. Confirm impact first (graph, reproduction, second report). A rollback fired at a phantom is its own incident.
- Mitigation did not move the signal -> it was the wrong lever. Revert your change if it was reversible, re-scope the blast radius, and try the next reversible mitigation. Do not stack three speculative changes at once; you will not know which one helped or hurt.
- Severity is genuinely ambiguous -> declare the higher level and downgrade later once impact is clearer. Downgrading is cheap; a silent SEV1 is not.
- The IC is overloaded or unreachable -> hand off command explicitly to a named person and announce the handoff in the channel. Command is never implicit and never shared.
- Root cause is still unknown after mitigation -> that is fine. The system is stable; move the investigation to the debugger (`/debug`) and the postmortem, off the live incident clock.
- Tried a mitigation 3 times without recovery -> stop, escalate to the next tier or the service owner, and widen who is on the call. Do not keep guessing alone while users are down.

## Out of Scope

- Deep root-cause analysis of the underlying defect. Once the system is stable, hand the investigation to `/debug` (resonance-engineering-debugger).
- Shipping the permanent fix and the release. That is `/ship` (resonance-ops-ship), tracked as a postmortem action item, not done live under pressure.
- Non-production degradations with no user impact. Those are bugs, not incidents.

## Cognitive Frameworks

### Mitigate, then diagnose
The live incident has one goal: end user pain. Reach for the reversible lever (rollback, flag off, failover) before the clever fix. Curiosity about the root cause is a postmortem activity, not an outage activity.

### One throat to choke
A crowd with no commander thrashes. Exactly one IC holds the picture, decides, and delegates. On a SEV1 the IC coordinates and does not also have their head down in the code, that is a separate operator.

### Round up under uncertainty
When severity or the right mitigation is unclear, pick the safer-for-users option: the higher severity, the more reversible action. You can always downgrade or undo. You cannot un-lose the minutes an under-call cost.

### Blameless by design
People do not cause incidents, systems that allow a single mistake to reach production do. The postmortem asks "what let this happen and what makes it impossible next time", never "who did it". Blame buys silence, and silence buys the next outage.

## Reference Library

- **[Severity Matrix](references/severity_matrix.md)**: SEV1-SEV4 criteria and the response expectations each one triggers.
- **[Comms Protocol](references/comms_protocol.md)**: Update cadence, audiences, and the internal-versus-external split.
- **[Blameless Postmortem](references/blameless_postmortem.md)**: Timeline, 5-whys, owned action items, and the no-blame rule.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory; when `.resonance/ledger/` exists it is the system of record for decisions, lessons, metrics, customers, and experiments, while `02_memory.md` keeps `[lib]` notes and pointers).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
