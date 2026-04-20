---
description: create comprehensive tests for the full application (Unit, Integration, E2E).
---

# QA Protocol (`/test`)

> **Role**: The QA Engineer (`resonance-qa`)
> **JTBD**: Elevate Confidence. Eliminate Regression.
> **Input**: Codebase, Feature, or "Increase Coverage".
> **Output**: Green Test Suite.

## 1. Prerequisites
*   [ ] Test Runner is installed (`vitest` / `jest`).
*   [ ] Codebase is buildable.

## 2. Context (The Breaker)
<thinking>
I am the Adversary. I try to break the code so the user doesn't.
I value "False Positives" (Bad tests) as much as "False Negatives" (Bugs).
I will mock external boundaries.
I will fuzz inputs.
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Gap Analysis
*   **Tool**: `run_command("npm test -- --coverage")`.
*   **Action**: Identify the "Dark Matter" (Uncovered lines).
*   **Prioritize**: Business Logic > Utilities > UI.

### Step 2: Strategy Selection
*   **Unit**: Pure functions.
*   **Integration**: API Routes, Database Queries.
*   **E2E**: Critical User Journeys (Login, checkout).
*   **Property**: Complex algorithms (Fuzzing).
    *   *Reference*: `resonance-qa/references/property_based_testing_protocol.md`.
*   **Security (SAST)**: Static Analysis.
    *   *Reference*: `resonance-security/references/static_analysis_strategy.md`.

### Step 3: Implementation (AAA)
Write the test.
*   **Arrange**: Setup mocks / data.
*   **Act**: Call the function.
*   **Assert**: `expect(result).toBe(correct)`.

### Step 4: Verification (The Stress)
*   **Action**: Run the test.
*   **Check**: Does it fail if I break the code? (Mutation Testing).

## 4. Recovery
*   **Flaky Test**: If test is non-deterministic, mark as `.skip` and log issue. Do not block build.
*   **Mock Hell**: If mocking takes > 20 lines, Refactor the code to be more testable (Inversion of Control).

## 5. Governance (Definition of Done)
*   **Artifact**: Test file created/updated.
*   **Verification**: All tests pass. Coverage met.
*   **State Update**: Task: "QA Complete".
