# Pre-Landing PR Review Checklist

> **Source**: Integration of the gstack `/review` checklist.
> **Objective**: Identify structural, security, and architectural issues often missed by tests and linters.

## Critical Issues (Block Merge)

If any of these are found, use `gh pr review --request-changes`.

1.  **SQL and Data Safety**
    *   Any string interpolation in SQL queries?
    *   Are we trusting raw input without sanitization?
    *   Mutations occurring in GET requests?
2.  **LLM Trust Boundaries**
    *   Are we rendering raw, unescaped LLM output into the DOM?
    *   Are we executing LLM-generated code/scripts without sandbox or confirmation?
3.  **Authentication & Crypto**
    *   Are passwords/tokens logged or stored in plaintext anywhere?
    *   Are permissions checked on *every* protected route (not just the UI)?
4.  **Race Conditions & Time Safety**
    *   Concurrent execution bugs (e.g., deducting balance without locking).
    *   Time window safety (e.g., assumes `Date.now()` is constant across async ticks).

## Informational Issues (Recommend fixes, but don't block)

If only these are found, use `gh pr review --comment` or approve with notes.

1.  **Conditional Side Effects**
    *   Are side effects happening deep inside nested `if` statements instead of cleanly extracted?
2.  **Code Quality / Readability**
    *   Magic numbers / un-named constants.
    *   Commented-out code (dead code).
    *   Excessive cognitive complexity.
3.  **Test Gaps**
    *   Are the tests actually asserting behavior, or just that the code doesn't throw?
    *   Are shadow paths (Nil, Error, Empty) tested?

## The Two-Pass Procedure
1.  **Pass 1: Broad Context**: Read the PR description and commit messages. Understand the *why*. Scan the diff line-by-line looking for Critical Issues.
2.  **Pass 2: The Attack**: Adversarially try to find ways the code breaks. If the user does X while Y is happening, what fails?
