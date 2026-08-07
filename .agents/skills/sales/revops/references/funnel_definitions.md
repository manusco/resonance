# Funnel and Exit-Criteria Definitions

> One written set of stages, shared by marketing and sales. A stage advances on a buyer action, never a seller activity. This document is the single source of truth; if two teams disagree about what an MQL is, the funnel leaks at the seam and nobody owns the leak.

## Contents

- [1. Why One Definition Beats Two Good Ones](#1-why-one-definition-beats-two-good-ones)
- [2. The Buyer-Action Rule](#2-the-buyer-action-rule)
- [3. The Canonical Stages](#3-the-canonical-stages)
- [4. The Marketing-to-Sales Seam: MQL and SAL](#4-the-marketing-to-sales-seam-mql-and-sal)
- [5. Exit Criteria as Verifiable Truth](#5-exit-criteria-as-verifiable-truth)
- [6. Probability Is Earned, Not Assigned](#6-probability-is-earned-not-assigned)
- [7. Common Definition Failures](#7-common-definition-failures)

## 1. Why One Definition Beats Two Good Ones

Every funnel dispute traces back to two teams using the same word for different things. Marketing counts an MQL when a lead crosses a score. Sales counts it when someone picks up the phone. Both are defensible, and that is the problem: the hand-off has no shared line, so leads fall through it and each side has data proving the other dropped them.

The fix is not a better definition. It is one definition, written down, agreed by both teams, and enforced in the system. The value here is not cleverness, it is that everyone points at the same line. This document exists so the line is written once.

## 2. The Buyer-Action Rule

A deal advances a stage when the buyer does something that proves progression, not when the rep does something that looks like progress.

- Seller activity (does NOT advance a stage): sent a proposal, gave a demo, left a voicemail, logged a call, added a contact.
- Buyer action (advances a stage): booked the meeting, confirmed budget exists, introduced the economic buyer, returned redlines, gave a verbal, signed.

The reason is forecasting. Seller activity is under the rep's control and tells you nothing about whether the deal will close. Buyer action is the buyer spending their own time and political capital, which is the only real signal. A pipeline advanced on seller activity is a pipeline of wishes.

## 3. The Canonical Stages

Adapt the names to your CRM, but keep the meaning and the exit criteria.

| Stage | Owner | Enters when | Exit criteria (buyer truth, verifiable) |
| :--- | :--- | :--- | :--- |
| Inquiry / Lead | Marketing | Contact captured | Matches ICP and shows a real engagement signal |
| MQL | Marketing | Score crosses threshold | Fits ICP and shows intent; passed to sales for acceptance |
| SAL (Sales Accepted Lead) | SDR / AE | A rep accepts the MQL | Rep confirms fit and intent in a live conversation; discovery meeting booked and held |
| Stage 1: Discovery | AE | Qualified opportunity created | Confirmed pain tied to a metric, budget exists, decision process can be named |
| Stage 2: Validation | AE | Solution fit under way | Economic buyer engaged, solution mapped to their metric, technical validation passed, champion confirmed |
| Stage 3: Proposal / Negotiation | AE | Proposal delivered | Verbal agreement, terms and paper process agreed, mutual action plan to signature with a date |
| Commit / Contracting | AE | In signature | Signature or PO in hand |
| Closed Won | AE | Deal booked | Contract executed |
| Closed Lost | AE | Deal dead | Loss reason logged, competitive loss separated from no-decision |

The iron rule sits under every row: the exit criterion is a thing the buyer did, and it is verifiable by someone other than the rep.

## 4. The Marketing-to-Sales Seam: MQL and SAL

The single most expensive undefined line in B2B is the one between marketing and sales. Define it explicitly:

- **MQL (Marketing Qualified Lead):** marketing's assertion that a lead fits the ICP and shows enough intent to warrant a rep's time. Defined by an agreed fit-plus-intent score, not by marketing's hope.
- **SAL (Sales Accepted Lead):** sales agreeing to work the MQL. This is the accountability handshake. When a rep accepts, an SLA clock starts (speed-to-lead; delegate the audit of that clock to `resonance-sales-lead-ops`).
- **SQL / Qualified Opportunity:** the rep has confirmed fit and intent in a conversation and created an opportunity. This is where the pipeline begins.

The hand-off must have a rejection path. If a rep rejects an MQL, the reason routes back to marketing so scoring improves. An MQL with no acceptance and no rejection is the crack leads fall through.

## 5. Exit Criteria as Verifiable Truth

Write each exit criterion so a manager who was not on the call can check it. "Rep feels good about it" fails the test. "Buyer confirmed a Q3 budget line and named the two other approvers" passes.

For the qualified stages, the exit criteria are the MEDDIC or SPICED elements made concrete:

- **Pain with a metric:** not "they have problems" but "they lose N hours a week, worth roughly X."
- **Economic buyer engaged:** you have spoken to the person who controls the budget, not only the champion.
- **Decision process known:** you can name the steps from here to signature and the dates.
- **Paper process known:** you know who signs, whether legal and security review, and how long each takes.
- **Compelling event:** a dated reason the buyer must act by a certain time, not a date the rep picked to fill the field.
- **Decision criteria known:** you can name what the buyer will score solutions against and who set those criteria, not "the demo went well."
- **Champion tested:** the champion has done something that cost them, an intro to the economic buyer or a push for you in a meeting you were not in. A friendly contact who only shares information is a coach, not a champion.
- **Competition known:** the buyer has named who else is in the evaluation and what would tip it. "No competition" from a rep who never asked is a gap, not an edge.

If a criterion cannot be answered with a fact, the deal has not earned the stage, no matter how good the call felt.

## 6. Probability Is Earned, Not Assigned

Stage probabilities (Stage 1 = 20 percent, Stage 3 = 60 percent, and so on) are useful for weighted pipeline only if the stage definitions are enforced. If reps advance deals on seller activity, the probabilities are attached to fiction and the weighted pipeline lies with a decimal point. Derive the probabilities from your own historical stage-to-close conversion, not from a template, and recheck them each quarter. A probability is a measured conversion rate, not a number of good vibes.

## 7. Common Definition Failures

| Failure | Symptom | Fix |
| :--- | :--- | :--- |
| Two teams, two MQL definitions | Marketing and sales argue over lead quality with conflicting numbers | One written fit-plus-intent definition, both teams sign off |
| Stages advance on seller activity | Big pipeline, low win rate, forecast misses | Rewrite every exit criterion as a buyer action |
| No rejection path at the seam | MQLs vanish, scoring never improves | Route rejection reasons back to marketing |
| Template probabilities | Weighted pipeline never matches reality | Derive probabilities from your own stage-to-close data |
| "Compelling event" is a filled field | Close dates slip every quarter | Require a buyer-driven event, not a rep-picked date |
