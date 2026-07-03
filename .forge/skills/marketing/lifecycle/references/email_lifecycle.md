# Email Lifecycle

> Right message, right trigger, right person. Default to triggered off behavior. Reserve batch for genuine one-to-many news.

## Contents

- [1. Triggered vs batch](#1-triggered-vs-batch)
- [2. The sequence families](#2-the-sequence-families)
- [3. Welcome and onboarding sequence](#3-welcome-and-onboarding-sequence)
- [4. Nurture sequence](#4-nurture-sequence)
- [5. Milestone and behavioral triggers](#5-milestone-and-behavioral-triggers)
- [6. Re-engagement sequence](#6-re-engagement-sequence)
- [7. Segmentation and RFM](#7-segmentation-and-rfm)
- [8. Cadence and frequency](#8-cadence-and-frequency)
- [9. Deliverability and suppression](#9-deliverability-and-suppression)
- [10. Failure modes](#10-failure-modes)

## 1. Triggered vs batch

| | Triggered | Batch |
|--|-----------|-------|
| Fires on | A behavior or state change (signed up, hit a milestone, went quiet) | A schedule, to a segment |
| Relevance | High, mapped to what the user just did | Low, same message to everyone |
| Use for | Onboarding, milestones, dunning, re-engagement, most lifecycle | A launch, an outage, a real news item |
| Risk | Low; small, relevant volume | High; blasts hit unengaged users and hurt the sending domain |

Default is triggered. Choose batch only when the message is genuinely one-to-many and time-bound. A "feature of the month" newsletter is defensible; a "day 3, everyone gets email 3" blast that ignores whether the user already did the thing is not. Triggered sequences own the timing off the user's clock, not the calendar's.

Note on lifecycle vs the words: this reference designs the sequence, the trigger, and the timing. The word-level copy, subject-line craft, and humanizing the draft belong to `resonance-marketing-copywriter`. Hand over a brief and the moment; let the copywriter write the send.

## 2. The sequence families

Four jobs, four families:
- **Welcome / onboarding**: support in-app activation. Get the user to the aha.
- **Nurture**: build value and trust for users not yet ready to convert or expand.
- **Milestone / behavioral**: react to what the user does (or stops doing) in the product.
- **Re-engagement**: pull a quiet user back before they are gone.

Win-back (for users who already left) lives in `references/churn_and_winback.md`; dunning (for failed payments) lives there too.

## 3. Welcome and onboarding sequence

Email supports in-app onboarding. It does not replace it. Every send should push toward the aha moment, defined in `references/activation_onboarding.md`.

| Trigger | Purpose | Content |
|---------|---------|---------|
| On signup | Welcome + first step | "Here is the one thing to do first" |
| First value not reached in 24h | Nudge to aha | Remove the specific blocker, one CTA |
| First value reached | Reinforce + next step | "You did X. Here is what unlocks next" |
| Day 3, key feature unused | Feature-in-context | Show the feature tied to their goal, not a tour |
| Day 5 | Proof | A short, real customer outcome |
| Day 7 | Check-in | "Stuck? Here is the fastest way to get help" |

Branch on behavior. A user who hit the aha on day 1 should not get the "still stuck?" nudge on day 2. Suppress a step the moment its goal is met.

## 4. Nurture sequence

For subscribers or trials not yet activated or converted. Goal: earn trust and stay useful until intent appears.

- Lead with usefulness, not asks. Teach, benchmark, or solve a small problem each send.
- Space it out. Nurture is a slow cadence (weekly or slower), not a daily drip.
- Watch for intent signals (pricing-page visit, repeat logins, a high-value action) and hand the user to a conversion or sales path when they fire.
- Exit the nurture when the user activates or converts. Do not keep nurturing an active customer.

## 5. Milestone and behavioral triggers

The highest-converting lifecycle email is a reaction to real behavior.

| Signal | Trigger email |
|--------|---------------|
| Reached a usage milestone | Celebrate + suggest the next capability |
| Hit a plan limit | Contextual upgrade prompt |
| Adopted feature A, never used complementary feature B | "People who use A also use B" |
| Invited a teammate | Onboard the inviter as a power user |
| Usage climbing | Expansion or advanced-tips path |
| Usage dropping | Early re-engagement before they go fully quiet |

Fire these off product events, not a schedule. The relevance comes from the timing matching the action.

## 6. Re-engagement sequence

Trigger: inactivity that is unusual for this product. Calibrate the window to your natural cadence. A daily tool goes quiet at 7 to 14 days; a monthly tool might be 45.

| Timing | Message | Tone |
|--------|---------|------|
| First (early inactivity) | "Here is what you were building" | Helpful, specific, not needy |
| Second | "What's new since you were last here" | Value-forward, tied to their use case |
| Third | "Anything we can help with?" | Human, personal, offers a real hand |
| Final | "Still useful to you?" | Honest; sets up the win-back or a clean exit |

Rule: after four unanswered touches, stop and move the user to suppressed or to a win-back track. Chasing a silent user damages deliverability and the relationship.

## 7. Segmentation and RFM

Segment by lifecycle stage first (new, activated, habitual, at-risk, churned), then by value.

RFM scores each user on three axes:
- **Recency**: how recently they took a meaningful action. The strongest churn predictor.
- **Frequency**: how often they engage.
- **Monetary**: revenue or plan value.

Score each axis (for example 1 to 5) and combine to get treatment tiers:

| Segment | RFM shape | Treatment |
|---------|-----------|-----------|
| Champions | High R, high F, high M | Expansion, referral asks, early access |
| Loyal | High F, mid M | Upsell, keep the habit warm |
| At-risk | Low R, formerly high F | Re-engagement now, before they churn |
| New | High R, low F | Onboarding and activation sequence |
| Hibernating | Low R, low F, low M | One re-engagement attempt, then suppress |

RFM turns a flat list into a set of populations that each need a different message. It stops you sending a champion the beginner nudge and an at-risk user the upsell.

## 8. Cadence and frequency

- Match cadence to the family: onboarding is dense (daily-ish for a week), nurture is slow (weekly or less), re-engagement is a short, spaced burst.
- Cap total sends per user across all sequences. Overlapping triggers can stack into a flood; enforce a global frequency cap.
- Respect quiet hours and timezone. Send when the user is likely awake and working, not at 3am local.
- Prune decaying flows. A triggered flow that stops converting should be paused, not left running forever.

## 9. Deliverability and suppression

Sending reputation is a shared asset. Protect it.

- **Suppress the unengaged.** Repeatedly ignoring your email is a signal; keep mailing and the inbox providers notice. Move long-unengaged addresses to a suppression list with an audit trail.
- **Preflight a broadcast.** Before any large batch, check segment overlap (so a user is not in three sends at once) and last-sent recency (so you are not re-hitting people you just mailed).
- **Warm up volume.** Ramp new sending domains and IPs; do not go from zero to a full list.
- **Honor unsubscribe instantly and keep the record.** Every suppression is tracked.

Involuntary suppression (a hard bounce) and voluntary suppression (an unsubscribe) are both permanent for that address. Do not resurrect them.

## 10. Failure modes

1. **Spraying batch where triggered is correct.** The default mistake. If the message reacts to a user's behavior, it must be triggered off that behavior, not sent to a whole segment on a fixed day.
2. **No suppression on a step already satisfied.** Emailing "finish setup" to a user who finished setup reads as a broken system and erodes trust.
3. **Sequences that never exit.** A user who converted should leave the nurture. A user who activated should leave onboarding. Define exit conditions on every flow.
4. **Ignoring frequency across flows.** Each sequence looks reasonable alone; together they bury the user. Cap globally.
5. **Mailing the dead.** Sending to long-unengaged addresses to hit a number tanks deliverability for everyone, including engaged users.
6. **Treating RFM tiers the same.** A champion and a hibernating user on the same send wastes both.
