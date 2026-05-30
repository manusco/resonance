# Strategic Debugging Protocols

> "A bug is just a hypothesis waiting to be disproven."

## 1. The Binary Search Method (O(log n))

**Stop guessing lines. Divide the search space.**

1.  **Hypothesis**: "The error is between Line A (Start) and Line B (Crash)."
2.  **Test**: Place a log at Middle Line (M).
3.  **Result**:
    *   Output printed? -> Error is after M. (Discard A-M).
    *   Output NOT printed? -> Error is before M. (Discard M-B).
4.  **Repeat**: Until the exact line is isolated.

> 🔴 **Rule**: Never make a random change "to see if it works". Isolate first.

## 2. Git Bisect Protocol (Regression Hunting)

**When did it break? Do not scan history manually.**

1.  **Start**: `git bisect start`
2.  **Bad**: `git bisect bad` (Current HEAD).
3.  **Good**: `git bisect good <commit-hash>` (Last known working commit).
4.  **Test**: Git checks out the middle commit. Run verification.
    *   Works? -> `git bisect good`.
    *   Fails? -> `git bisect bad`.
5.  **Result**: Git identifies the *exact* commit that introduced the bug.

## 3. The 5 Whys (Root Cause Analysis)

**Do not fix the symptom. Fix the cause.**

*   **Problem**: Database connection failed.
1.  **Why?**: Connection timeout.
2.  **Why?**: Server overloaded.
3.  **Why?**: Connection pool exhausted.
4.  **Why?**: Connections not returned to pool.
5.  **Why?**: **Missing `finally` block in `UserService.ts`.** (ROOT CAUSE).

> ✅ **Fix**: Add the `finally` block. (Not just increasing pool size).
