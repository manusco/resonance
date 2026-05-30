# Protocol: Lifecycle Email Architecture
> **Focus**: User State Management via Email
> **Resonance Phase**: Scaling / Retention

## 1. The State Machine Paradigm
Do not think of "newsletters." Think of **User States**. Emails are the transitions between these states.

**The States**:
1.  `Visitor` -> (Signup) -> `Lead`
2.  `Lead` -> (Nurture) -> `User`
3.  `User` -> (Activation) -> `Power User`
4.  `Power User` -> (Monetization) -> `Customer`
5.  `Churned` -> (Resurrection) -> `User`

## 2. Sequence Patterns

### Pattern A: The Onboarding Ramp (Lead -> User)
*   **Trigger**: Sign up.
*   **Goal**: "Aha Moment" (First Value).
*   **Sequence**:
    1.  **T+0 (The Hook)**: Deliver the asset immediately. One clear "Click here."
    2.  **T+1 (The Quick Win)**: Unblock the first obstacle. A "Did you know?" tip that works in <5 mins.
    3.  **T+3 (The Philosophy)**: "Why we built this." Build tribe affinity.
    4.  **T+5 (The Social Proof)**: "How Company X uses us."

### Pattern B: The Nurture Loop (User -> Customer)
*   **Trigger**: Active usage but Free tier.
*   **Goal**: Upgrade.
*   **Sequence**:
    1.  **The Value Gap**: Point out what they *could* be doing (Premium features).
    2.  **The Case Study**: Detailed breakdown of a paid user's ROI.
    3.  **The Direct Ask**: "Ready to upgrade?" with a friction-reducer (Guarantee).

### Pattern C: The Lazarus Pit (Churned -> User)
*   **Trigger**: 30 days inactivity.
*   **Goal**: Re-activation.
*   **Sequence**:
    1.  **The Gentle Nudge**: "Is everything okay?"
    2.  **The Value Update**: "Here is what we shipped since you left." (New features).
    3.  **The Goodbye**: "I won't email you again." (Reverse psychology/List cleaning).

## 3. Engineering The Output
*   **Subject Line**: The API Endpoint of attention. Must yield high open rate.
    *   *Good*: "The mistake I made", "Your report is ready", "Question for you".
    *   *Bad*: "Newsletter #43", "Update".
*   **Pre-header**: The payload preview. Use it to support the Subject Line.
*   **The "From" Name**: Humans trust humans. "Peter from Stripe" > "Stripe Team".

## 4. Text-Only vs. HTML
For B2B and High-Ticket, **Text-Only** (Plain Text) usually outperforms heavily designed HTML templates.
*   **Why**: It parses as a "personal letter" by the brain, not a "marketing flyer."
*   **Rule**: If you wouldn't send it to a friend, don't send it to a user.

## 5. Metrics & Telemetry
Measure the pipeline, not just vanity metrics.
*   **Open Rate**: Subject Line efficacy.
*   **Click Rate**: Copy efficacy / CTA clarity.
*   **Reply Rate**: Relationship depth (The ultimate signal).
