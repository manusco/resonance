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
Before I touch any code, I will explicitly name: which file, which function, which lines I intend to change. Nothing adjacent gets touched.
</thinking>

## 3. The Algorithm (Execution)

### Step 0: Surgical Scope Declaration
Before touching production code:
*   **Action**: Name exactly what you believe is broken and which file/function/line you expect to change.
*   **Rule**: If the scope is unclear, do not begin. Ask: "I expect to change [X]. Is that correct?"
    → verify: Scope is explicit. You can draw a straight line from bug report to target line.

### Step 1: Reproduction (The Evidence)
Before touching production code:
*   **Action**: Create `reproduction_script.ts` (or strict test case).
*   **Experiment**: Run it.
    *   *Result*: It MUST fail. If it passes, you have not found the bug.
    → verify: Script fails 100% of the time with the reported error.

### Step 2: Root Cause Analysis (RCA)
Isolate variables.
*   **Tool**: `read_file`, `grep_search`.
*   **Action**: Trace the data flow. Where does it become invalid?
*   **Hypothesis**: "I suspect X is null because Y didn't await."
    → verify: Hypothesis is written down before any experiment.

### Step 3: The Fix (The Surgery)
Apply the minimal effective change.
*   **Action**: Edit ONLY the lines identified in Step 0. Do not reformat adjacent code, change quote style, add type hints, or add docstrings. Match existing style.
*   **Verify**: Run the Reproduction Script.
    *   *Result*: It MUST pass.
    → verify: Reproduction script passes. Zero adjacent lines changed beyond the fix.

### Step 4: Regression Check
Did we break the world?
*   **Action**: Run related test suites (`npm test`).
    → verify: Full suite green. No new failures introduced.

## 4. Recovery
*   **Rabbit Hole**: If RCA takes > 5 steps without clarity, stop.
    *   **Escalate**: Activate `resonance-researcher` to trace dependency graph or read raw logs.
    *   **Ask User**: Summarize findings and request inputs.
*   **Fix Fails**: If the fix doesn't work, revert immediately. Do not stack hacks.

## 5. Governance (Definition of Done)
*   **Artifacts**: `reproduction_script.ts` (or added test).
*   **Knowledge**: Run `/capture` to document the finding.
*   **State Update**: Update `state.md` -> Task: "Bug Resolved".
