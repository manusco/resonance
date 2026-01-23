# Protocol: Risk-Based Review (Differential Analysis)
> **Objective**: Allocate review energy proportional to risk.
> **Philosophy**: "Not all lines of code are equal. 10 lines of Auth > 1000 lines of CSS."

## 1. The Blast Radius Algorithm
Before reviewing, calculate the potential impact.

| Factor | High Scoring (+10) | Low Scoring (+1) |
| :--- | :--- | :--- |
| **Logic** | Auth, Crypto, Money, PII | UI, Logging, Docs |
| **Exposure** | Public API, Unauthenticated Route | Internal tool, Admin Dashboard |
| **Dependencies** | 0-hop (Core), Shared Library | Leaf node (Feature) |

**Score > 20**: **HIGH RISK**. Requires "Adversarial Review".
**Score < 5**: **LOW RISK**. Requires "Sanity Check".

---

## 2. Review Modes

### Mode A: Sanity Check (Low Risk)
*   **Focus**: Readability, Style, Lints.
*   **Time**: 5-10 mins.
*   **Method**: Scan definition body. Check variable names.

### Mode B: Adversarial Review (High Risk)
*   **Focus**: Invariants, State Corruption, Escalation.
*   **Time**: 1-4 hours.
*   **Method**:
    1.  **Baseline**: Read the *original* code (before diff). Understanding the "Before" state is critical.
    2.  **Destruct**: Ask "How can I break this?" (e.g., Integer Overflow, Race Condition).
    3.  **Trace**: Follow data flow from `Input` to `Sink`.

---

## 3. The Red Flags (Stop & Escalate)
*   **Missing Tests**: High Risk change with 0 tests? -> **Request Changes**.
*   **Complexity**: "I don't understand this block." -> **Request Refactor**.
*   **Sneaky Logic**: Logic hidden in a Getter or Setter. -> **Flag it**.
