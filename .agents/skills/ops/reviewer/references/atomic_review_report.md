# Atomic Review Report

> **Concept**: A high-density summary of a review session to ensure clarity and accountability.

## 1. The Summary Table

| Category | Finding | Status | Priority | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| **Logic** | [Description of issue] | BLOCKING | P1 | High |
| **Safety** | [Security risk] | BLOCKING | P1 | High |
| **Style** | [Lint/Pattern] | NITPICK | P2 | Med |
| **Tests** | [Missing coverage] | BLOCKING | P1 | High |

**Confidence** is the reviewer's own certainty that the finding is real, scored separately from severity (how much it harms). It is the axis that most cuts false-positive noise in an AI-run review:

- **High**: verified against the actual code; the failure path is concrete and reproducible.
- **Med**: consistent with the code but not proven; rests on a path not directly read.
- **Low**: a hunch from the diff alone; may hinge on context the reviewer cannot see.

Lead the report with High-confidence P0/P1 findings. A Low-confidence finding is raised as a question, never a block.

## 2. Decision Matrix (Iron Man Suit)

For any non-obvious issue, present:
1.  **Context**: The line/logic affected.
2.  **RECOMMENDATION**: What to do and **WHY**.
3.  **Options**:
    *   **A)** Surgical Fix (Matches existing style, minimal change).
    *   **B)** Ideal Refactor (Cleaner but more files/effort).
    *   **C)** Deferred (Add TODO and log to `02_memory.md`).

## 3. Operational Sign-off

*   [ ] CI passed (Lint, Test).
*   [ ] Blocking patterns checked.
*   [ ] 100% of new logic has test coverage.
*   [ ] Learnings logged to `02_memory.md`.
