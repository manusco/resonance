# Growth & Retention Mental Models

This reference outlines the core operating models for maximizing LTV (Lifetime Value), preventing churn, and accurately attributing revenue. These models strip away tool-specific bias (e.g., Klaviyo vs. Customer.io) and focus purely on the underlying mechanics.

## 1. Churn Prevention & Dunning
Churn is the silent killer of compounding growth. Do not focus on acquisition if your bucket is leaking.

### Active Churn (Cancellations)
Active churn happens when a user explicitly decides to stop paying.
**The "Save Offer" Protocol**:
Never let a user cancel with a single click without friction. Implement a progressive save flow:
1. **Understand**: Ask why they are leaving (Price, Missing Feature, Project Over).
2. **Pause**: Offer to pause their account for 1-3 months instead of canceling.
3. **Downgrade**: Offer a cheaper, limited tier.
4. **Discount**: Offer a 20-30% discount for the next 3 months to buy time to re-engage them.

### Passive Churn (Payment Failures)
Passive churn happens when a credit card expires or a charge fails. It is entirely preventable.
**The Dunning Sequence**:
1. **Pre-Dunning**: Email 7 days before a card expires.
2. **Immediate Failure**: Email immediately upon failure, but retry automatically in 3 days.
3. **Escalation**: If 3 retries fail, lock the account but do not delete data. Use SMS or in-app modals, not just email.

## 2. High-Signal Revenue Attribution
Software attribution (Google Analytics, Mixpanel) is fundamentally flawed due to ad-blockers, cross-device usage, and the death of third-party cookies (ITP).

### Zero-Party Data (Self-Reported Attribution)
You must implement a "How did you hear about us?" (HDYHAU) free-text or structured survey on the post-purchase or post-signup screen.
- **Why**: Software tells you they clicked a Google Ad (Last-Touch). The HDYHAU survey tells you they originally heard about you on a podcast 6 months ago (First-Touch/True Discovery).
- **Action**: Triangulate your software analytics with your zero-party survey data to accurately allocate marketing spend.

## 3. The Expert Panel (Quality Gates)
Do not launch marketing campaigns or product updates in a vacuum.
- **Concept**: Before finalizing a positioning statement or ad creative, pass it through an "Expert Panel" check.
- **Application**: The panel should identify:
  1. Is the value proposition immediately obvious?
  2. Is the headline impactful and free of generic fluff?
  3. Are we highlighting the "Aha!" moment fast enough?
