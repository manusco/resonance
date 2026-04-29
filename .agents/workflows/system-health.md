---
description: Run a full system health check (Automated + Manual).
---

# System Health Protocol (`/system-health`)

> **Role**: The Doctor (`resonance-qa` + `resonance-security`)
> **JTBD**: Benchmarking. "Quantified Self".
> **Input**: Codebase State.
> **Output**: Health Score (0-100) + Qualitative Flags.

## 1. Prerequisites
*   [ ] Project is initialized.

## 2. Context (Vital Signs)
<thinking>
I need to measure the system's pulse.
A "Healthy" system has:
1.  **High Confidence**: Tests Pass.
2.  **Low Entropy**: Code is clean (Lint).
3.  **Sync**: Map (State) == Territory (Git).
4.  **Auth Consistency**: Permissions enforced at all layers.
5.  **Environment Safety**: No hidden assumptions that break on deploy.
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Automated Vitals
*   **Tests**: `npm test -- --coverage`. (Weight: 40%)
*   **Lint**: `npm run lint`. (Weight: 30%)
*   **Build**: `npm run build`. (Weight: 30%)

### Step 2: Manual Vitals
*   **Drift Check**: Read `01_state.md`. Does it match `git log -10`?
*   **Docs Check**: Is `docs/` updated?
*   **Auth Model Consistency**: Do routes, policies, and UI templates agree on who can access what? Are role checks centralized or scattered? Flag any layer where enforcement is missing.
*   **Environment Assumption Check**: Are there hard-coded paths, missing fallbacks for optional schema, or preview/staging divergence? Would the app survive deploying to a fresh environment with only migrations and no seed data?
*   **Test Depth Check**: Do tests cover failure paths and unauthorized paths, or only happy paths? Quick scan against the [8-Path Matrix](../skills/resonance-qa/SKILL.md).

### Step 3: Calculation
`Score = (Test% * 0.4) + (LintClean * 0.3) + (BuildPass * 0.3)`

**Qualitative Flags** (not captured by the score but critical):
*   🔴 **AUTH_INCONSISTENT**: Permissions enforced at some layers but not others.
*   🔴 **ENV_FRAGILE**: Code assumes conditions that may not exist on staging/production.
*   🟡 **TEST_SHALLOW**: Tests pass but only cover happy paths.
*   🟡 **DRIFT_DETECTED**: State file doesn't match git history.
*   🟡 **STALE_TESTS**: Tests encode product decisions that have since changed.

## 4. Recovery
*   **Score < 80**: PRESCRIPTION.
    *   "Run `/test` to boost coverage."
    *   "Run `/refactor` to fix lint."
*   **Build Fail**: IMMEDIATE. "Run `/debug`."
*   **AUTH_INCONSISTENT flag**: "Run `/audit` Step 3 (Authorization Model Audit)."
*   **ENV_FRAGILE flag**: "Add environment fallbacks. See [Environment Robustness Directive](../skills/resonance-core/references/universal_audit_directives.md)."

## 5. Governance (Definition of Done)
*   **Artifact**: Health Report (score + qualitative flags).
*   **Decision**: If Score < 80 OR any 🔴 flag, BLOCK `/ship`.
*   **State Update**: Log score and flags to `memory.md`.
