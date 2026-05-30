# Protocol: Rigorous Review & Trade-off Analysis

> **Status**: Core Implementation Standard
> **Objective**: Conduct multi-dimensional audits that balance architectural integrity, code quality, testing, and performance.

## 1. Professional Preferences (The "Bar")

*   **Aggressive DRY**: Flag repetition at the component and logic level. One change should ideally happen in one place.
*   **Testing is Non-Negotiable**: Priority is given to test coverage over speed of implementation.
*   **Engineered Enough**: Avoid "Fragile/Hacky" (under-engineered) AND "Premature Abstraction" (over-engineered).
*   **Edge Case Obsession**: Thoughtfulness > Speed. Every `if` needs an `else` or a handled failure path.
*   **Explicit over Clever**: Readability is the primary metric for long-term health.

---

## 2. Review Dimensions (The Audit Matrix)

### A. Architecture Audit
*   **Boundaries**: Are component/module boundaries clear?
*   **Coupling**: Check the dependency graph. Are we creating circular dependencies?
*   **Data Flow**: Map the path of data. Are there potential bottlenecks or "prop drilling" issues?
*   **Security**: Validate auth/access boundaries and API exposure.

### B. Code Quality Audit
*   **Structure**: Evaluate the organization of modules.
*   **Error Handling**: Are errors caught, logged, and handled gracefully for the user?
*   **Technical Debt**: Identify "hotspots" that are becoming hard to maintain.

### C. Test Audit
*   **Strength**: Evaluate assertion strength (are we just checking for existence, or true state?).
*   **Failure Modes**: Verify that failure paths (SAD paths) are tested, not just the happy path.
*   **Coverage**: Identify gaps in unit vs. integration vs. e2e.

### D. Performance Audit
*   **N+1 Patterns**: Rigorously check for database/API loops.
*   **Memory**: Note large data fetches or unmanaged state.
*   **Complexity**: Identify slow/high-complexity code paths using Big O analysis.

---

## 3. Communication Pattern (Trade-off Analysis)

For every issue found, do NOT just state the problem. Provide a **Decision Matrix**:

1.  **Issue Description**: Concrete file/line reference and "smell" category.
2.  **Options**:
    *   **Option A (The fix)**: Implementation effort, risk, and long-term impact.
    *   **Option B (The workaround/Minimal fix)**: Trade-offs in debt vs. speed.
    *   **Option C ("Do Nothing")**: Why this might be acceptable (or why it isn't).
3.  **Opinionated Recommendation**: We explicitly recommend the first option that aligns with the "Bar."
4.  **Consensus Check**: Explicitly ask "Does this direction align with your vision?" before proceeding.

---
*Created by the Reviewer & Architect agents. Enforcing the Outstanding Skills Standard.*
