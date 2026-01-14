---
description: Structurally refine code for readability and maintainability.
---

# Workflow: Refactor Code ("The Cleaner")

**Trigger**: "Clean this up", "Refactor", "Tech Debt".
**Context**: Improving structure without changing behavior.

## 1. Safety Net (The Harness)
*Activate Skill*: `resonance-qa`

- [ ] **Check Tests**: Do tests exist for this module?
- [ ] **Add Tests**: If no, WRITE TESTS FIRST. You cannot refactor without a safety net.

## 2. Strategy (The Approach)
*Activate Skill*: `resonance-architect`

- [ ] **Pattern**: Identify the Target Design Pattern (e.g., "Extract Strategy", "Facade").
- [ ] **Strangler Fig**: If large, create a parallel implementation.

## 3. Execution (The Surgery)
*Activate Skill*: `resonance-backend` / `resonance-frontend`

- [ ] **Move**: Extract methods/classes.
- [ ] **Rename**: Improve naming clarity.
- [ ] **Simplify**: Remove nested `if/else`.

## 4. Verification (The Proof)
- [ ] **Test**: Run the test suite. MUST pass.
- [ ] **Diff**: Check the diff. Did logic change? (It shouldn't).
