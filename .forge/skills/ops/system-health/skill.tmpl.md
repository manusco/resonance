---
name: resonance-ops-system-health
description: System health assessor. Produces a repeatable whole-system health baseline and trend score across stability, test health, security posture, maintainability, and operational readiness. Use for periodic health checks or release readiness trends. Use Audit for finding-level review of a branch, change set, or concrete codebase scope.
archetype: orchestration
owner: ops.system-health
activation: manual
authority: consequential
triggers:
  - score repository or system health
entrypoints:
  - /system-health
negative_triggers:
  - mutate the system being scored
inputs:
  - user_request
  - artifact
  - health_scope
outputs:
  - user_request
  - recommendation
  - evidence
  - test_scope
  - qa_scope
  - security_scope
side_effects:
  - may_coordinate_work
  - may_execute_checks
write_sets:
  - project:health-report
failure_policy: stop
invokes:
  - resonance-ops-qa
  - resonance-ops-security
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

1. **Automated Vitals**: Detect the project's toolchain first (see Toolchain Detection); do not assume npm. Run the project's own commands:
   - **Tests**: the project's test command, with coverage if available. (Weight: 40%)
   - **Lint**: the project's lint command. (Weight: 30%)
   - **Build**: the project's build command. (Weight: 30%)
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
- **[Toolchain Detection](../core/references/toolchain_detection.md)**: Detect and run the project's test/lint/build, not npm by reflex.
- **[Audit Classification Taxonomy](../core/references/audit_classification_taxonomy.md)**: Finding categories and P0-P3 ranking.

{{RESOLVER:operating_standard}}

{{OVERLAY}}
