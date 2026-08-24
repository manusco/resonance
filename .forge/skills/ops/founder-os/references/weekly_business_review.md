# The Weekly Business Review: inspection, not status theater

> The WBR is where a company notices reality once a week, on purpose. It reads the numbers against their targets, finds what is stuck, and produces decisions. If it produces a feeling of progress instead of a list of decisions, it was theater.

## Contents

- [1. Inspection vs Status Theater](#1-inspection-vs-status-theater)
- [2. The Standing Agenda](#2-the-standing-agenda)
- [3. Read the Ledger, Not the Narrative](#3-read-the-ledger-not-the-narrative)
- [4. What Moved, What Is Stuck](#4-what-moved-what-is-stuck)
- [5. Decisions Out, Logged as dec- Entries](#5-decisions-out-logged-as-dec-entries)
- [6. Outcome-Pending Work](#6-outcome-pending-work)
- [7. Timebox and Cadence](#7-timebox-and-cadence)
- [8. Failure Modes](#8-failure-modes)

## 1. Inspection vs Status Theater

Status theater is everyone taking turns saying what they did. It feels productive and changes nothing, because "what I did" is activity, and activity is not the point. Inspection starts from the numbers and their targets, then asks why the gap is the size it is. The difference is where the meeting starts. Theater starts with people. Inspection starts with the scorecard.

The founder's job in the WBR is not to collect updates. It is to find the two or three places where reality has diverged from the plan and force a decision at each one. Everything else in the meeting is context for that.

## 2. The Standing Agenda

Same shape every week so the meeting is scannable and short:

1. **Scorecard read.** Walk the KPI tree top to bottom. Each metric against its target and its trend. Green, flat, or off-track. Numbers only, no story yet.
2. **Off-track drilldown.** For every red or newly flat metric, one question: what changed, and what is the smallest move that could fix it. This is the meeting. Spend the time here.
3. **Stuck list.** What has not moved in two or more weeks despite being a priority. A stall is a signal, not a status.
4. **Decisions.** The calls the review produced, each assigned to one owner. These get written to the ledger before anyone leaves.
5. **Outcome check-ins.** Any `met-` or `exp-` entry whose `due:` date has arrived (surface with `py .forge/measurement_due.py`). Record the real reading, close or supersede the entry.

Highlights and wins get one line at the top, not a lap around the table. The review is weighted toward what is off, because what is off is where the decisions are.

## 3. Read the Ledger, Not the Narrative

The scorecard is the set of `met-` entries in `.resonance/ledger/metrics.md`, each carrying its own target. The review reads current value against target, not a story about the value. When the number and the story disagree, the number wins and the story is the thing to explain.

Reading the ledger has a second effect: it removes the argument about what the goal was. The target is on the entry, set at quarter start. Nobody gets to remember it differently in week seven. This is the whole reason company state lives as typed records instead of prose. A review over prose spends its time reconstructing what was meant. A review over the ledger spends its time on what to do.

## 4. What Moved, What Is Stuck

Two lists come out of the scorecard read.

**What moved** is any metric that changed materially since last week, up or down. A drop is more informative than a rise; chase it first. Name the cause if it is known, log it as a question if it is not.

**What is stuck** is any priority metric flat for two or more weeks. A stall usually means one of three things: the work aimed at it did not land, the work landed and the lever is weaker than assumed, or nobody actually owns it. The drilldown names which. A metric stuck for a month with no decision attached is the clearest sign a review has become theater.

## 5. Decisions Out, Logged as dec- Entries

A review that ends without decisions was a broadcast. Every real call the meeting produces becomes a `dec-` entry in `.resonance/ledger/decisions.md`, with one owner and, where it applies, the metric it is meant to move as an `evidences:` edge.

```
## dec-cut-paid-search: Pause paid search, shift budget to lifecycle
type: decision
created: 2026-07-15
status: active
confidence: medium
review_due: 2026-08-15
chose: pause paid search
over: hold spend and wait another month
evidences: met-cac-2026-07

CAC is above target and lifecycle has unused capacity this month.
```

When a later decision reverses or replaces this one, do not edit it. Supersede it: the new entry carries `supersedes: dec-cut-paid-search`, and the old one gets `status: superseded` and a `superseded_by:` line. The audit trail is the point. Six months on, the value is not the current decision but the chain of what you believed and when, and why you changed your mind. A decision log you overwrite is a decision log that has forgotten how you got here.

## 6. Outcome-Pending Work

Most decisions a WBR produces cannot be graded in the room. Pausing paid search proves out in next month's CAC, not today. That work ends `DONE_PENDING_OUTCOME`: the decision is made and the metric that will judge it carries a `due:` date. The review does not pretend to know the result. It sets the check-in.

Each week, the outcome-check-in step reads whatever `measurement_due.py` surfaces, records the real value on the `met-` or `exp-` entry, and closes the loop. This is how the company grades its own decisions against reality instead of against how confident it felt when it made them. A decision that looked right and aged badly is the most valuable entry in the ledger, because it retrains the next call.

## 7. Timebox and Cadence

- **Weekly, same day, same time.** Predictability is half the value. A review that slips is a review that gets skipped.
- **Sixty minutes, hard cap.** The scorecard read is fast. The drilldowns are where time goes. If a topic needs more than the review can give, it becomes a `dec-` to schedule a working session, not a takeover of the meeting.
- **Prepared, not assembled live.** The scorecard is pulled before the meeting, not built during it. The review reads a ready board; it does not wait while someone fetches numbers.
- **One driver.** The founder or the operator runs it and holds the timebox. A review with no driver drifts back into theater by week three.

## 8. Failure Modes

- **Round-robin updates.** Everyone reports activity. Start from the scorecard instead of from people.
- **No decisions.** The meeting produces a feeling, not a `dec-` entry. If nothing was decided, nothing was inspected.
- **Arguing the number.** Time lost debating what the target was. Put targets in the ledger so this never happens.
- **Grading the ungradable.** Declaring a decision a success in the room when its proof lands next month. Mark it `DONE_PENDING_OUTCOME` and set the check-in.
- **Overwriting decisions.** Editing a past `dec-` instead of superseding it, which erases the reasoning trail.
- **No timebox.** The review sprawls, so people dread it, so it decays. Cap it and defer deep work to a separate session.

## 9. Optional EOS and L10 variant

Use this variant when the company already runs EOS. Keep the same evidence-first rule and ledger outputs.

1. Segue, 5 minutes. One personal or professional win per person.
2. Scorecard, 5 minutes. Mark off-track numbers for the issues list.
3. Rocks, 5 minutes. Mark each quarterly priority on track or off track.
4. Headlines, 5 minutes. Capture material customer and employee news.
5. To-dos, 5 minutes. Check last week's commitments. Treat misses as system evidence, not guilt.
6. IDS, 60 minutes. Identify, Discuss, Solve the highest-priority issues.
7. Conclude, 5 minutes. Assign new actions, name messages to cascade, and rate the meeting.

For IDS, collect issues from off-track metrics, off-track Rocks, organizational constraints, and headlines. Force a top three. For each issue, identify the root cause before discussing solutions, then choose one action with one owner and one due date. Write each settled call as a `dec-` entry. "The team" is not an owner.

Do not let the L10 format replace the core contract. The meeting still starts from evidence, respects timeboxes, and ends with owned decisions and dated follow-up.
