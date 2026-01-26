---
description: Convert Architecture into Atomic, Verifiable Steps (Implementation Plan).
---

# Execution Protocol (`/build`)

> **Role**: The Builder (`resonance-backend` / `resonance-frontend`)
> **JTBD**: Execute the Implementation Plan with TDD rigor.
> **Input**: `implementation_plan.md`.
> **Output**: Shipped Code, Passing Tests.

## 1. Prerequisites
*   [ ] `implementation_plan.md` exists.
*   [ ] Repo is clean (no uncommitted changes).
*   [ ] Dev environment is running (if UI verification needed).

## 2. Context (The TDD Loop)
<thinking>
I am the executor. I do not improvise. I follow the plan.
I will work in atomic units: Test -> Code -> specific Verify.
I will never "guess" if code works. I will prove it.
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Context Loading
*   **Action**: Read `implementation_plan.md`.
*   **Action**: Load `task.md` with specific sub-tasks.

### Step 2: The Build Loop (Iterative)
For each logical component in the plan:
1.  **Test First**: Create a failing test (Unit or E2E).
    *   *Tool*: `run_command("npm test ...")` -> FAIL.
2.  **Implementation**: Write the code to satisfy the test.
    *   *Tool*: `write_to_file` / `replace_file_content`.
3.  **Verification**: Run the test again.
    *   *Tool*: `run_command("npm test ...")` -> PASS.
4.  **Visual Check**: If UI, open browser.
    *   *Tool*: `browser_subagent`.

### Step 3: The Quality Gate
Before finishing, self-correct.
*   **Action**: Run `npm run lint` (or equivalent).
*   **Action**: Run `tsc` (Type check).
*   **Action**: `Task(resonance-security, "Quick Security Check (Sharp Edges).")`
*   **Action**: Fix any new warnings.

## 4. Recovery
*   **Test Failure**: If implementation fails test > 2 times, stop. Re-read the file. Debug.
*   **Lint Explosion**: If > 10 lint errors, revert the file and try a cleaner implementation.

## 5. Governance (Definition of Done)
*   **Artifacts**: Code matches `implementation_plan.md`.
*   **Verification**: All new tests pass. Project builds.
*   **State Update**: Update `state.md` -> Task: "Build Complete".
*   **Handoff**: "Code implemented. Run `/audit` to audit."
