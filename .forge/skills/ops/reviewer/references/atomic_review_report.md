# Atomic Review Report

> **Concept**: A high-density summary of a review session to ensure clarity and accountability.

## 1. The Summary Table

| Category | Finding | Status | Priority |
| :--- | :--- | :--- | :--- |
| **Logic** | [Description of issue] | BLOCKING | P1 |
| **Safety** | [Security risk] | BLOCKING | P1 |
| **Style** | [Lint/Pattern] | NITPICK | P2 |
| **Tests** | [Missing coverage] | BLOCKING | P1 |

## 2. Decision Matrix (Iron Man Suit)

For any non-obvious issue, present:
1.  **Context**: The line/logic affected.
2.  **RECOMMENDATION**: What to do and **WHY**.
3.  **Options**:
    *   **A)** Surgical Fix (Matches existing style, minimal change).
    *   **B)** Ideal Refactor (Cleaner but more files/effort).
    *   **C)** Deferred (Add TODO and log to `learnings.jsonl`).

## 3. Operational Sign-off

*   [ ] CI passed (Lint, Test).
*   [ ] Blocking patterns checked.
*   [ ] 100% of new logic has test coverage.
*   [ ] Learnings logged to `learnings.jsonl`.
