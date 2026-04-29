# Boy Scout Protocol (Elite Standard)

> "Always leave the campground cleaner than you found it."
> — Robert Baden-Powell

## 1. The Protocol

When you touch a file to add a feature:
1.  Scan for **Dead Code** (Unused imports, commented out blocks).
2.  Scan for **Formatting Issues** (Inconsistent indentation).
3.  Scan for **Weak Types** (`any`).

## 2. The "Drive-By" Refactor

*   **Allowed** (within the file you're already touching):
    *   Renaming a confusing variable.
    *   Extracting a 50-line block into a private function.
    *   Fixing a typo in a comment.
*   **Forbidden**:
    *   Rewriting the entire architecture. (Make a separate PR).
    *   Changing public API contracts.
    *   Crossing file boundaries (cleanup in file A while working on file B).

> 🔴 **Reconciliation with Karpathy Surgical Lock**: Boy Scout cleanup applies ONLY within files already touched by the current task. If the cleanup exceeds 5 lines or changes behavior, it becomes its own task — tracked separately.

## 3. The Ratio

*   **1 Feature** : **1 Cleanup**.
*   Every PR should have at least one small " Boy Scout" improvement.

> 🔴 **Rule**: If you see commented-out code, DELETE it. Git has history.
