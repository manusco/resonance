# Protocol: Karpathy Guidelines

> **Objective**: Reduce common LLM coding mistakes through behavioral guardrails.
> **Tradeoff**: Bias toward **Caution** over **Speed**.

## 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**

*   **Explicit Assumptions**: State them. If uncertain, ask.
*   **Multiple Interpretations**: Present them. Don't pick silently.
*   **Simpler Approach**: If it exists, say so. Push back on complexity.
*   **Stop Condition**: If confused, stop. Name the confusion. Ask.

## 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**

*   ❌ No features beyond what was asked.
*   ❌ No abstractions for single-use code.
*   ❌ No "configurability" that wasn't requested.
*   ❌ No error handling for impossible scenarios.
*   **Refactor Rule**: If you write 200 lines and it could be 50, rewrite it.

> *Ask yourself: "Would a senior engineer say this is overcomplicated?"*

## 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**

*   **Isolation**: Don't "improve" adjacent code/comments/formatting.
*   **Legacy**: Don't refactor things that aren't broken.
*   **Orphans**: Remove imports/variables YOUR changes made unused.
*   **The Test**: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**

*   **Validation**: "Add validation" -> "Write tests for invalid inputs, then pass."
*   **Bug Fix**: "Fix bug" -> "Write reproduction test, then pass."
*   **Refactor**: "Refactor X" -> "Ensure tests pass before and after."

**Multi-Step Plan Pattern:**
1.  [Step] -> verify: [check]
2.  [Step] -> verify: [check]
3.  [Step] -> verify: [check]
