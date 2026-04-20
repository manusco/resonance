# Root Cause Tracing Techniques

When you need to find the specific origin of a bug, use these techniques.

## 1. The Backward Trace (Backtracking)
Start at the symptom (where the error happens) and move up the stack.

1.  **Identify Sinking Point**: Where does the bad value crash the app? (e.g., `func_a(null)`)
2.  **Find Caller**: Who called `func_a` with `null`?
3.  **Inspect Caller**: How did *they* get `null`? From a variable? A return value?
4.  **Repeat**: Keep going up until you find the **Origin Point** (where the valid data became invalid).

## 2. The Binary Search (Isolation)
If the code path is complex or unknown:

1.  **Bisect the Code**: Comment out half the logic. Does the bug persist?
    *   **Yes**: The bug is in the remaining half.
    *   **No**: The bug is in the commented-out half.
2.  **Bisect Input**: If processing a large file fails, cut the file in half.
3.  **Bisect History**: Use `git bisect` to find the exact commit that introduced the bug.

## 3. The Data Probe (Logging)
Don't just log "Error happened". Log the *state*.

*   **Bad**: `console.log("Error", error)`
*   **Good**:
    ```javascript
    console.log("Boundary Check:", {
        inputID: id,
        userContext: context,
        dbConnectionState: db.state
    });
    ```
*   **Strategy**: Place probes at **System Boundaries** (API entry, DB query, Function entry).

## 4. The Minimal Reproduction (MinRepro)
Strip away everything that isn't the bug.

1.  Create a new file `repro.js`.
2.  Copy *only* the failing function.
3.  Mock the inputs hardcoded to the failing values.
4.  Run `node repro.js`.
5.  If it fails, you have isolated the bug. If it passes, the bug is in the environment/dependencies.
