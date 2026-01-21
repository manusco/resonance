# Boy Scout Protocol (Elite Standard)

> "Always leave the campground cleaner than you found it."
> — Robert Baden-Powell

## 1. The Protocol

When you touch a file to add a feature:
1.  Scan for **Dead Code** (Unused imports, commented out blocks).
2.  Scan for **Formatting Issues** (Inconsistent indentation).
3.  Scan for **Weak Types** (`any`).

## 2. The "Drive-By" Refactor

*   **Allowed**:
    *   Renaming a confusing variable.
    *   Extracting a 50-line block into a private function.
    *   Fixing a typo in a comment.
*   **Forbidden**:
    *   Rewriting the entire architecture. (Make a separate PR).
    *   Changing public API contracts.

## 3. The Ratio

*   **1 Feature** : **1 Cleanup**.
*   Every PR should have at least one small " Boy Scout" improvement.

> 🔴 **Rule**: If you see commented-out code, DELETE it. Git has history.
