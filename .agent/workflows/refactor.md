---
description: Structurally refine code for readability and maintainability.
---

# Refactoring Protocol (`/refactor`)

> **Role**: The Craftsman (`resonance-refactor`)
> **JTBD**: Reduce technical debt, improve readability, enforce SOLID.
> **Input**: "Messy" file or module.
> **Output**: Clean Code (Zero Behavioral Change).

## 1. Prerequisites
*   [ ] Git Status must be clean. **CRITICAL**.
*   [ ] Existing tests must pass (The Safety Net).

## 2. Context (The Essentialist)
<thinking>
**Ultrathink Directive**: "Simplify Ruthlessly".
Elegance is achieved when there is nothing left to take away.

My goal is not just "clean code", but "inevitable code".
I will question every assumption.
I will delete dead code with extreme prejudice.
I will decouple dependencies until the logic sings.
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Safety Check
*   **Action**: Run tests on the target module.
*   **Decision**:
    *   *Pass*: Proceed.
    *   *Fail*: **ABORT**. "Cannot refactor broken code. Run `/debug` first."
    *   *Missing*: Write a "Snapshot Test" to lock in current behavior.

### Step 2: Pattern Recognition
Activate `resonance-simplifier`.
*   **Scan**: Look for:
    *   **DRY Violations**: Duplicated logic?
    *   **God Classes**: Doing too much?
    *   **Magic Numbers**: Unnamed constants?
    *   **Dead Code**: Unused variables/imports?

### Step 3: The Surgery (Atomic Loop)
Repeat until clean:
1.  **Extract**: Move logic to helper/component.
2.  **Simplify**: Flatten nested ifs (Guard Clauses).
3.  **Rename**: Variables should tell stories.
4.  **Verify**: Run tests after EACH change.

## 4. Recovery
*   **Test Failure**: If a step breaks tests, `git restore [file]` immediately. Try a smaller step.
*   **Complexity Trap**: If refactoring makes it *harder* to read, Revert.

## 5. Governance (Definition of Done)
*   **Verification**: All tests pass.
*   **Metric**: Code is smaller (lines) or cleaner (readability).
*   **State Update**: Update `state.md` -> Task: "Refactor Complete".
