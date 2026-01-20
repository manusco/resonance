---
description: Identify Root Cause and fix bugs using the Scientific Method.
---

# Debugging Protocol (`/debug`)

> **Role**: The Debugger (`resonance-debugger`)
> **JTBD**: Scientifically isolate and resolve defects.
> **Input**: Bug Report, Stack Trace, or "It's broken".
> **Output**: Reproduction Script, Fix, Regression Test.

## 1. Prerequisites
*   [ ] Git Status is clean (Recommended).
*   [ ] The codebase is buildable (we can run tests).

## 2. Context (The Science)
<thinking>
I cannot fix what I cannot reproduce.
"Reasoning backwards" from the error to the cause is the only path.
I will not guess. I will measure.
Hypothesis -> Experiment -> Conclusion.
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Reproduction (The Evidence)
Before touching production code:
*   **Action**: Create `reproduction_script.ts` (or strict test case).
*   **Experiment**: Run it.
    *   *Result*: It MUST fail. If it passes, you have not found the bug.

### Step 2: Root Cause Analysis (RCA)
Isolate variables.
*   **Tool**: `read_file`, `grep_search`.
*   **Action**: Trace the data flow. Where does it become invalid?
*   **Hypothesis**: "I suspect X is null because Y didn't await."

### Step 3: The Fix (The Surgery)
Apply the minimal effective change.
*   **Action**: Edit the code.
*   **Verify**: Run the Reproduction Script.
    *   *Result*: It MUST pass.

### Step 4: Regression Check
Did we break the world?
*   **Action**: Run related test suites (`npm test`).

## 4. Recovery
*   **Rabbit Hole**: If RCA takes > 5 steps without clarity, stop. Summarize findings and ask user for more context.
*   **Fix Fails**: If the fix doesn't work, revert immediately. Do not stack hacks.

## 5. Governance (Definition of Done)
*   **Artifacts**: `reproduction_script.ts` (or added test).
*   **Knowledge**: Run `/capture` to document the finding.
*   **State Update**: Update `state.md` -> Task: "Bug Resolved".
