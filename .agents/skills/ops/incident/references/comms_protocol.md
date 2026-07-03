# Comms Protocol

> During an incident, silence reads as chaos. A steady, boring update on a promised cadence is worth more than a perfect diagnosis nobody hears. Say what you know, say what you are doing, say when you will speak next.

## Contents
- The two channels
- Cadence by severity
- Anatomy of an update
- Internal versus external
- Stakeholders and audiences
- The resolution message
- What not to say

## The two channels

Run every incident on two separate tracks and never let them bleed together.

- **Internal channel** (the incident channel or call): the responders' working space. Raw, fast, technical. Hypotheses, dead ends, who is doing what. It is fine to be wrong here.
- **External channel** (status page, customer notice): the public face. Calm, factual, no speculation. Only states confirmed impact and confirmed progress. A customer must never read your internal guessing.

The IC or a named comms lead owns what crosses from internal to external. Nothing goes public by accident.

## Cadence by severity

Commit to an interval and keep it, even when the update is "no change yet".

- **SEV1:** every 15 to 30 minutes, internal and external.
- **SEV2:** every 30 to 60 minutes.
- **SEV3:** once or twice a day, internal only unless a customer is waiting.
- **SEV4:** no incident cadence; normal ticket updates.

The rule that matters most: always state the time of the next update, and hit it. A missed promised update erodes trust faster than the outage itself.

## Anatomy of an update

Every update, internal or external, answers four things in plain language:

1. **What is happening.** The impact in user terms ("checkout is failing for some customers"), not internal jargon.
2. **What we are doing.** The current action ("rolling back the latest deploy"), without over-promising a fix time you do not have.
3. **Who owns it.** The IC name, so people know where to direct questions.
4. **When we will update next.** A concrete time. This is the part people actually wait for.

Keep it short. Three or four sentences. An update nobody can parse in ten seconds is not an update.

## Internal versus external

| Aspect | Internal | External |
| :-- | :-- | :-- |
| Tone | Fast, technical, candid | Calm, plain, reassuring |
| Content | Hypotheses, actions, dead ends | Confirmed impact and progress only |
| Speculation | Allowed and useful | Never |
| Root cause | Discussed freely | Only after it is confirmed and safe to share |
| Timing | Real time | On the committed cadence |

## Stakeholders and audiences

Different people need different altitudes:

- **Responders** need the raw internal feed.
- **Support and success** need to know what to tell customers and what the workaround is, before customers call them.
- **Leadership** needs severity, business impact, and time-to-mitigation, not a stack trace.
- **Customers** need to know you are aware, that you are on it, and roughly when to check back.

Tailor the message to the audience. The same wall of technical detail does not serve all four.

## The resolution message

When you declare resolved, close the loop everywhere you opened it:

- State that service is restored and since when.
- Name the mitigation in one line ("we rolled back the change that caused it").
- Set the expectation that a postmortem will follow, so the story is not left hanging.
- Thank the responders internally. Keep the external note gracious and short.

Do not declare resolved externally until the signal has actually held. Retracting a premature all-clear is worse than staying quiet a few more minutes.

## What not to say

- No blame, no names, no "the vendor screwed up", in any external message.
- No promised fix time you cannot back with evidence.
- No internal speculation on the status page.
- No going dark. If there is nothing new, the update is "no change, next update at HH:MM".
