# Protocol: Karpathy Guidelines

> **Objective**: Reduce common LLM coding mistakes through behavioral guardrails.
> **Tradeoff**: Bias toward **Caution** over **Speed**.
> See also: `references/karpathy_examples.md` for ✅/❌ code walkthroughs.

## 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**

*   **Explicit Assumptions**: State them. If uncertain, ask.
*   **Multiple Interpretations**: Present them. Don't pick silently.
*   **Simpler Approach**: If it exists, say so. Push back on complexity.
*   **Stop Condition**: If confused, stop. Name the confusion. Ask.

> ❌ **Anti-Pattern**: "Add a feature to export user data" → assumes ALL users, assumes format, assumes file location.
> ✅ **Pattern**: "Before implementing, I need to clarify: (1) Scope - all users or filtered? (2) Format - file download or API? (3) Fields - which are sensitive?"

## 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**

*   ❌ No features beyond what was asked.
*   ❌ No abstractions for single-use code.
*   ❌ No "configurability" that wasn't requested.
*   ❌ No error handling for impossible scenarios.
*   ❌ No cutting validation, authorization, security checks, accessibility, observability, or plausible error handling to make a diff look smaller.
*   **Runnable Check**: Non-trivial logic leaves one small check behind: a test, an assertion script, or a reproduction that fails if the logic breaks.
*   **Refactor Rule**: If you write 200 lines and it could be 50, rewrite it.

### The implementation selection ladder

After understanding the request and tracing the flow the change touches, stop
at the first option that satisfies the contract:

1. Remove work that is not needed.
2. Reuse code already in the repository.
3. Use the standard library.
4. Use a native platform capability.
5. Reuse an installed dependency.
6. Compose the shortest clear expression.
7. Add new custom machinery only when the earlier options do not satisfy the contract.

The ladder controls implementation choice, not scope. Do not silently shrink
what the user asked for. Do not use a shorter implementation as a reason to
remove validation, authorization, security, accessibility, error handling that
prevents data loss, or a required behavior.

> *Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.*

> ❌ **Anti-Pattern**: Strategy pattern + abstract classes + config dataclass for a single `calculate_discount(amount, percent)` call.
> ✅ **Pattern**: `def calculate_discount(amount: float, percent: float) -> float: return amount * (percent / 100)`

## 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**

*   **Isolation**: Don't "improve" adjacent code/comments/formatting.
*   **Legacy**: Don't refactor things that aren't broken.
*   **Style**: Match existing style, even if you'd do it differently.
*   **Orphans**: Remove imports/variables YOUR changes made unused.
*   **The Test**: Every changed line should trace directly to the user's request.

> ❌ **Anti-Pattern (Style Drift)**: Fixing a bug and also changing quote style, adding type hints, adding a docstring, reformatting whitespace.
> ✅ **Pattern**: Only the lines that fix the reported issue change. Everything else is untouched.

> ❌ **Anti-Pattern (Drive-by Refactoring)**: "Fix empty email crash" → also rewrites username validation, improves comments, changes indentation.
> ✅ **Pattern**: Fix the 2 lines that handle the empty email. Stop.

## 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**

*   **Validation**: "Add validation" → "Write tests for invalid inputs, then make them pass."
*   **Bug Fix**: "Fix bug" → "Write reproduction test → watch it fail → fix → watch it pass."
*   **Refactor**: "Refactor X" → "Ensure tests pass before and after."

**Multi-Step Plan Pattern:**
```
1.  [Step] → verify: [check]
2.  [Step] → verify: [check]
3.  [Step] → verify: [check]
```

> **Key Insight**: Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

## ⚠️ Key Insight on Complexity

The overcomplicated examples are not obviously wrong - they follow design patterns and best practices. The problem is **timing**: they add complexity **before it is needed**, which makes code harder to understand, introduces more bugs, takes longer to implement, and is harder to test.

> **Good code solves today's problem simply, not tomorrow's problem prematurely.**
