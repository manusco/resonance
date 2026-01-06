# Workflow: Testing Strategy ("The Safety Net")

**Primary Role**: `qa` (QA Engineer)
**Goal**: Implement a robust testing strategy, not just "add tests".
**Constraint**: Quality > Quantity. Flaky tests are worse than no tests.

## 1. Trigger
User says: "Add tests", "Test this", "Setup QA", or "Increase coverage".

## 2. Phase 1: Analysis & Strategy
Before writing code, define the **Test Pyramid** for this task.

1.  **Analyze the Target**:
    *   Is it logic-heavy? (Needs **Unit Tests**).
    *   Is it a user flow? (Needs **E2E/Integration Tests**).
    *   Is it a visual component? (Needs **Snapshot/Interaction Tests**).

2.  **Define Scope**:
    *   "We will add 100% coverage to utils."
    *   "We will add 1 E2E test for the Checkout flow."

## 3. Phase 2: Scaffolding
Create the test skeleton first.
1.  **Create Files**: `src/features/X/__tests__/X.test.ts` (or strict project convention).
2.  **Mocking Strategy**: Decide what to mock (DB, API) and what to keep real.
3.  **Draft Scenarios**:
    ```typescript
    describe('Auth Service', () => {
      it.todo('should login with valid creds');
      it.todo('should lock account after 3 failed attempts');
    });
    ```
    *Stop here and ask User to validate the scenarios.*

## 4. Phase 3: Implementation (TDD / Red-Green)
1.  **Write Test**: Implement the `it(...)` blocks.
2.  **Verify Failure**: Run it. Ensure it fails (Red).
3.  **Implement Logic**: (If not already present).
4.  **Verify Success**: Run it. Ensure it passes (Green).

## 5. Phase 4: Regression & Stability
1.  **Run Full Suite**: `npm test`. Did we break anything else?
2.  **Check Flakiness**: Run the new test 5 times.
    ```bash
    for i in {1..5}; do npm test -- -t "My New Test"; done
    ```

## 6. Artifact Generation
Update `01_state.md`:
*   Metrics: "Test Coverage: X%"
*   Strategy: "Added E2E for Auth Flow"

## 7. Next Steps
Ask the user: "Tests implemented and stable. Should I commit or **run the full System Check**?"
