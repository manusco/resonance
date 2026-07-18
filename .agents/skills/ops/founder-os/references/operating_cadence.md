# The Operating Cadence: run the company on rhythm

> A business runs on rhythm, not on prompts. If work only happens when the founder remembers to ask, the company moves at the speed of one person's memory. The cadence is a written spec of what fires when, plus one worked example of scheduling it on the host. Resonance is not a daemon. It states the rhythm and hands the timer to the machine you already run on.

## Contents

- [1. Cadence Over Chat](#1-cadence-over-chat)
- [2. The Per-Function Cadence Spec](#2-the-per-function-cadence-spec)
- [3. Follow-Up Timers and the Ledger](#3-follow-up-timers-and-the-ledger)
- [4. Resonance Is Pull, Not a Daemon](#4-resonance-is-pull-not-a-daemon)
- [5. Scheduling It: One Worked Example](#5-scheduling-it-one-worked-example)
- [6. The Session-Start Pull](#6-the-session-start-pull)
- [7. Failure Modes](#7-failure-modes)

## 1. Cadence Over Chat

Chat is pull: nothing happens until the founder types. That is correct for open-ended work and wrong for the recurring spine of a company. A pipeline review that only happens when someone thinks of it is a pipeline review that happens late. The recurring work of a business is known in advance, so it should be scheduled in advance, and the founder's attention should go to the exceptions the cadence surfaces, not to remembering the cadence exists.

The rule: anything that should happen on a clock goes on the clock. What is left for chat is judgment, decisions, and the surprises the rhythm turns up.

## 2. The Per-Function Cadence Spec

Each function on the delegation map has a natural frequency. Write it down as a spec: what fires, how often, and what it produces. This spec is the company's heartbeat on paper.

| Cadence | What fires | Produces |
| :--- | :--- | :--- |
| Daily | Approval-queue clear (morning and end of day); incident and reliability check | Cleared Tier 1 queue; open incidents triaged |
| Weekly | Business review; pipeline review; scorecard pull | `dec-` entries; updated `met-` readings; stuck list |
| Biweekly | Outbound and lifecycle review; content and SEO check | Reply-rate readings; next-batch decisions |
| Monthly | Financial close; runway and burn read; investor update draft | Runway in months; a drafted update for founder to send |
| Quarterly | OKR grade and reset; KPI-tree review; authority-budget review | Next cascade; retuned tree; superseded budgets |

The frequencies are a starting point, not law. A company raising soon runs the runway read weekly. A company with no sales motion drops the pipeline review. Set each function's frequency to how fast its numbers actually move, then hold the rhythm.

## 3. Follow-Up Timers and the Ledger

Not all cadence is periodic. Much of it is a timer set by an event: a proposal sent needs a follow-up in four days, a trial started needs an activation nudge on day three, a decision made needs its outcome checked next month. These are not calendar events; they are due dates attached to records.

Resonance already has the mechanism. A `met-` or `exp-` entry carries a `due:` date, and work whose proof lands later ends `DONE_PENDING_OUTCOME` rather than DONE. The follow-up timer is just a `due:` field. When the date arrives, the entry surfaces itself. There is no separate reminder system to maintain, because the ledger is the reminder system.

```
## exp-proposal-acme-followup: Acme proposal, follow-up due
type: experiment
created: 2026-07-14
status: active
hypothesis: a value-recap follow-up on day four revives a stalled proposal
due: 2026-07-18
```

## 4. Resonance Is Pull, Not a Daemon

This is the line that keeps the design honest. Resonance does not run a background process. Nothing in the framework fires on a clock by itself. `py .forge/measurement_due.py` is a pull: it scans the ledger for entries whose `due:` date has arrived and prints them when something invokes it. It is silent when nothing is due and it does nothing until called.

The rhythm therefore needs a caller, and the caller is the host you already run: the operating system's own scheduler, or your CI, invoking the host CLI on a schedule. The cadence spec above is the what and the when. The host scheduler is the timer. Resonance is the work that runs when the timer fires. Keeping these separate is deliberate: a framework that spawns its own daemons is a framework you have to trust with uptime, and this one asks for none of that.

## 5. Scheduling It: One Worked Example

Take one row, the weekly business review, and put it on a real timer. Two forms, pick the one that matches your host.

Windows Task Scheduler, via `schtasks`, every Monday at 09:00, invoking the host CLI on the project:

```
schtasks /Create /TN "Resonance Weekly Business Review" /SC WEEKLY /D MON /ST 09:00 /TR "cmd /c cd /d D:\Dev\YourProject && claude -p \"/founder-os run the weekly business review\" >> logs\wbr.log 2>&1"
```

A cron line on a Unix host, same intent, Mondays at 09:00:

```
0 9 * * 1 cd /srv/yourproject && claude -p "/founder-os run the weekly business review" >> logs/wbr.log 2>&1
```

Read what this is and is not. It is one line of the host's own scheduler calling the host's own CLI, which runs the founder-os skill against the project. The schedule lives in the operating system, the review lives in Resonance, and the two meet only when the timer fires. Add one such entry per cadence row you want automated, or run the row by hand. Both are valid. The spec is the same either way; the scheduler is an option, not a dependency.

Swap `claude` for whichever host CLI you run. The pattern is host-agnostic: a scheduled invocation of the CLI with a founder-os command. Nothing here is a Resonance process. It is your machine, on your schedule, calling a skill.

## 6. The Session-Start Pull

Between scheduled runs, the ledger still surfaces what is due the moment any session opens. `measurement_due.py` at session start prints the `met-` and `exp-` entries whose `due:` date has passed, so even a founder who never sets up the scheduler sees the follow-ups and outcome check-ins that have come due. The scheduler makes the cadence automatic. The session-start pull makes it inescapable. A founder who opens the project at all cannot miss what the rhythm turned up.

## 7. Failure Modes

- **Cadence in the founder's head.** The rhythm exists only as intention, so it slips the first busy week. Write the spec.
- **Expecting a daemon.** Assuming Resonance fires the cadence itself. It does not. Wire the host scheduler or run the rows by hand.
- **Reminders outside the ledger.** A separate tool for follow-ups, which drifts from the company state. Use `due:` on `met-` and `exp-` entries.
- **Frequency mismatch.** Reviewing a fast metric monthly or a slow one daily. Set each function's cadence to how fast its numbers move.
- **All schedule, no exceptions.** Running the cadence but never acting on what it surfaces. The rhythm exists to route attention to the exceptions, not to generate reports nobody reads.
