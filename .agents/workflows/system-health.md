---
description: Run a full system health check (Automated + Manual).
---

# System Health Protocol (`/system-health`)

> **Role**: The Doctor (`resonance-qa`)
> **JTBD**: Benchmarking. "Quantified Self".
> **Input**: Codebase State.
> **Output**: Health Score (0-100).

## 1. Prerequisites
*   [ ] Project is initialized.

## 2. Context (Vital Signs)
<thinking>
I need to measure the system's pulse.
A "Healthy" system has:
1.  **High Confidence**: Tests Pass.
2.  **Low Entropy**: Code is clean (Lint).
3.  **Sync**: Map (State) == Territory (Git).
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Automated Vitals
*   **Tests**: `npm test -- --coverage`. (Weight: 40%)
*   **Lint**: `npm run lint`. (Weight: 30%)
*   **Build**: `npm run build`. (Weight: 30%)

### Step 2: Manual Vitals
*   **Drift Check**: Read `01_state.md`. Does it match `git log -10`?
*   **Docs Check**: Is `docs/` updated?

### Step 3: Calculation
`Score = (Test% * 0.4) + (LintClean * 0.3) + (BuildPass * 0.3)`

## 4. Recovery
*   **Score < 80**: PRESCRIPTION.
    *   "Run `/test` to boost coverage."
    *   "Run `/refactor` to fix lint."
*   **Build Fail**: IMMEDIATE. "Run `/debug`."

## 5. Governance (Definition of Done)
*   **Artifact**: Health Report displayed.
*   **Decision**: If Score < 80, BLOCK `/ship`.
*   **State Update**: Log score to `memory.md`.
