---
name: resonance-ops-system-health
description: The Doctor. Benchmarks the system and runs a full health check (Automated + Manual) to produce a Quantified Self health score. Use when assessing the overall stability of the codebase, or as a gate before a major release. Drives qa and security agents.
archetype: orchestration
---

# /resonance-ops-system-health: measure the pulse, diagnose the drift

> **Role:** the Doctor and benchmark engine.
> **Invoked as:** `/system-health` (to run a full health check).
> **Input:** Codebase State.
> **Output:** Health Score (0-100) + Qualitative Flags.
> **Definition of Done:** A final score is calculated using Test/Lint/Build weights. Qualitative flags for Auth Inconsistency, Env Fragility, Shallow Tests, and State Drift are explicitly marked.

You need to measure the system's pulse. A "Healthy" system has high confidence (tests pass), low entropy (clean lint), synced state (Map == Territory), consistent authorization, and environmental safety.

## Prerequisites (fail fast)

- [ ] Project is initialized (has a `.resonance/` directory).

## Algorithm (Execution)

Copy this checklist and tick items as you go.

1. **Automated Vitals**:
   - **Tests**: Run `npm test -- --coverage`. (Weight: 40%)
   - **Lint**: Run `npm run lint`. (Weight: 30%)
   - **Build**: Run `npm run build`. (Weight: 30%)
2. **Manual Vitals (The Qualitative Flags)**:
   - **Drift Check**: Read `01_state.md`. Does it match `git log -10`? (Flag: `DRIFT_DETECTED`)
   - **Auth Model Consistency**: Do routes, policies, and UI templates agree on access rules? Delegate to `resonance-ops-security`. (Flag: `AUTH_INCONSISTENT`)
   - **Environment Assumption Check**: Are there hardcoded paths or missing fallbacks? Would the app survive deploying to a fresh environment? (Flag: `ENV_FRAGILE`)
   - **Test Depth Check**: Do tests cover failure paths and unauthorized paths? Quick scan against the 8-Path Matrix. Delegate to `resonance-ops-qa`. (Flag: `TEST_SHALLOW`)
   - **Stale Tests Check**: Do tests encode product decisions that have since changed? (Flag: `STALE_TESTS`)
3. **Calculation**:
   - `Score = (Test% * 0.4) + (LintClean * 0.3) + (BuildPass * 0.3)`
   - Compile the qualitative flags.
4. **Synthesis**: Output the Health Report.

## Recovery

- Score < 80 → PRESCRIPTION: "Run `/test` to boost coverage" or "Run `/refactor` to fix lint."
- Build Fail → IMMEDIATE: "Run `/debug`."
- Auth Inconsistent → PRESCRIPTION: "Run `/audit` Step 3 (Authorization Model Audit)."
- Env Fragile → PRESCRIPTION: "Add environment fallbacks."

## Out of Scope

- Fixing the problems (delegate to `/refactor` or `/debug`).

## Cognitive Frameworks

### Quantified Self
You cannot improve what you cannot measure. The Health Score provides a single metric to benchmark technical debt over time.

### Qualitative Flags
A 100/100 score is useless if the tests only check the happy path (`TEST_SHALLOW`) or if the environment is hardcoded to `localhost` (`ENV_FRAGILE`). The flags are just as important as the score.

## Reference Library

- **[QA Health Rubric](../qa/references/qa_health_rubric.md)**: Full, Quick, and Regression modes.
- **[Audit Classification Taxonomy](../core/references/audit_classification_taxonomy.md)**: Finding categories and P0-P3 ranking.

{{RESOLVER:decision_brief}}

{{RESOLVER:completion}}

{{RESOLVER:voice}}

{{OVERLAY}}
