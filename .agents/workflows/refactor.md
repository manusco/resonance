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

But I will always name the BUSINESS CONSEQUENCE, not just the smell.
I will never refactor for aesthetics alone.
I will explicitly list what must NOT change.
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Safety Check
*   **Action**: Run tests on the target module.
*   **Decision**:
    *   *Pass*: Proceed.
    *   *Fail*: **ABORT**. "Cannot refactor broken code. Run `/debug` first."
    *   *Missing*: Write a "Snapshot Test" to lock in current behavior.

### Step 2: Do Not Change Declaration (**Required**)
Before touching anything, explicitly document:
*   **Preserved Behavior**: User-facing flows and interactions that must not change.
*   **Preserved Copy**: Labels, error messages, and UI text that must not regress.
*   **Preserved Contracts**: Public API signatures, response shapes, and redirect destinations.
*   **Product vs Test Divergence**: If any existing test contradicts current product intent, flag it here — do not silently pick a side.

### Step 3: Pattern Recognition
Activate `resonance-refactor`.
*   **Business-Consequence Smells** (check these first):
    *   **Duplicated Access Logic**: Are permission checks scattered across routes, policies, and templates?
    *   **Duplicated Persistence Mapping**: Is the same field mapped in multiple places?
    *   **Role-as-Permission Scatter**: Are role labels used directly as access decisions?
    *   **Environment-Sensitive Crash Paths**: Does the code assume tables/config/data that may not exist?
*   **Structural Smells** (check after business smells):
    *   **DRY Violations**: Duplicated logic?
    *   **God Classes**: Doing too much?
    *   **Magic Numbers**: Unnamed constants?
    *   **Dead Code**: Unused variables/imports?

> 🔴 **Rule**: For every smell found, name the business consequence. "God class" is not a finding. "Billing logic in `UserController` will drift when pricing changes" is a finding.

### Step 4: The Surgery (Safe Sequence)
Follow this risk-ordered sequence:

1.  **Lock**: Ensure current behavior is captured by tests. If missing, write them first.
2.  **Extract**: Pull duplicated truth into a single source (mapper, calculator, policy).
3.  **Centralize**: Consolidate scattered access/permission rules into one authority.
4.  **Split**: Separate overloaded responsibilities (God classes, fat controllers).
5.  **Cleanup**: Formatting, naming, dead code removal. **Always last.**

After each step:
*   Run tests. If red, `git restore [file]` immediately. Try a smaller step.
*   Verify the Do Not Change list is still intact.

### Step 5: Verification
*   **Tests**: All tests pass.
*   **Do Not Change**: All items verified.
*   **Diff**: `git diff --stat` shows only expected files.

## 4. Recovery
*   **Test Failure**: If a step breaks tests, `git restore [file]` immediately. Try a smaller step.
*   **Complexity Trap**: If refactoring makes it *harder* to read, Revert.
*   **Stale Test**: If a test fails because it encodes an outdated product decision, update the test (after verifying the product change was intentional). Log the finding.

## 5. Governance (Definition of Done)
*   **Verification**: All tests pass. Do Not Change list verified.
*   **Metric**: Code is smaller (lines) or cleaner (readability), AND each change traces to a named business risk.
*   **Attestation**: Use the [Completion Attestation](../skills/resonance-core/references/completion_attestation.md). Include blast radius, preserved behavior, and verification evidence.
*   **State Update**: Update `state.md` → Task: "Refactor Complete".
