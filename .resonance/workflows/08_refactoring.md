---
description: The elite protocol for structural and logical code refinement.
---

# 08 Refactoring ("The Surgeon")

> **"Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away."**  
> — *Antoine de Saint-Exupéry*

## 1. PRE-FLIGHT CHECK (First Principles)

**STOP.** Before you change a single character, ask the **Golden Question**:
> *"Does this refactor bring specific, measurable value to the project soul, or am I just shuffling deck chairs?"*

If the answer is "shuffling", **ABORT**.

### The Hierarchy of Debt
Refactoring must proceed in this specific order. Do not optimize code in a file that shouldn't exist.

1.  **SPATIAL (Structure)**: Is the file in the right place?
2.  **SEMANTIC (Naming)**: Does the name reflect the reality?
3.  **LOGICAL (Code)**: Is the internal logic elegant and robust?

---

## 2. PHASE 1: THE CARTOGRAPHER (Structural Audit)

**Objective**: Eliminate chaos. Organize the workspace.

1.  **Scan the Territory**:
    *   List all files in the target component/directory.
    *   Compare against `00_soul.md` and `02_technical_architecture.md`.

2.  **The Purge (Delete/Archive)**:
    *   Identify files that are: DUPLICATE, OBSOLETE, or DEAD.
    *   **Action**: Move them to `_archive/` or `deprecated/` (creation of this folder is authorized).
    *   *Constraint*: NEVER delete permanently without a `safe-commit` first.

3.  **The Migration (Move)**:
    *   Identify files that are "homeless" or "misplaced".
    *   **Action**: Propose a move to the correct directory.
    *   *Constraint*: You MUST check for imports/references before moving. Update references immediately.

4.  **The Baptizer (Rename)**:
    *   Check naming conventions.
    *   **Files**: `kebab-case` (default) or `PascalCase` (components/classes). BE CONSISTENT.
    *   **Ambiguity**: Rename generic names (e.g., `utils.js` -> `date-formatting.utils.js`).

---

## 3. PHASE 2: THE SURGEON (Code Refactoring)

**Objective**: Maximize readability and maintainability.

### A. The Diagnostic
Read the code. Identify **Smells**:
*   **The God Object**: Functions/Classes doing too much. -> *Break it down.*
*   **The Copy-Paste**: Identical blocks of code. -> *DRY (Don't Repeat Yourself).*
*   **The Magic Number**: Hardcoded values. -> *Extract to constants.*
*   **The Sphinx**: Complex logic with zero comments. -> *Document it.*

### B. The Procedure
1.  **Isolate**: Pick ONE file or component. Do not boil the ocean.
2.  **Protect**: Ensure tests exist for this component. If not, write a "Safety Net" test first.
3.  **Operate**:
    *   Extract methods.
    *   Rename variables for extreme clarity (e.g., `t` -> `timeoutInMs`).
    *   Add JSDoc/TSDoc to public interfaces.
    *   Remove commented-out code (it lives in git history).
4.  **Verify**: Run the "Safety Net" test.

---

## 4. PHASE 3: THE JUDGE (Validation)

You are not done until you prove it is better.

1.  **Reflect**:
    *   "Is the code smaller?"
    *   "Is the code easier to read?"
    *   "Did I break anything?"

2.  **Document**:
    *   Update `02_memory.md` with the refactoring pattern used (so others follow it).

3.  **Commit**:
    *   Use `safe-commit`.
    *   Message: `refactor: [scope] - [what changed] (e.g., "extracted auth logic")`

---

## 5. AUTO-RUN (Turbo Mode)

If you are confident, you may execute the following:

// turbo
1.  Run `npm run lint --fix` (or equivalent) to handle trivial formatting.
2.  Run `npm test` to ensure baseline stability.

---

**"Leave the campsite cleaner than you found it."**
