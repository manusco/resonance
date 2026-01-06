# Workflow: Task Scoping ("The Vibe Coder's Map")

**Primary Role**: Default / Tech Lead
**Goal**: Break architecture into atomic, verifyable steps.
**Constraint**: Do not simply list "Build X". List "Build X, Verify with Y".

## 1. Trigger

## 1. Goal
Convert a PRD/Architecture Spec into a rigorous **Implementation Plan** (`implementation_plan.md` or **Task List**) that an AI Agent can execute reliably ("Vibe Coding").

## 2. The Scoping Process
The enemy is ambiguity. Steps must be **Atomic** and **Verifiable**.

### Step 1: Decomposition
*   Break features into chunks that take < 4 hours to implement.
*   Separate **Refactoring** from **New Features**.
*   Separate **Frontend** from **Backend** (unless vertical slice is cleaner).

### Step 2: Verification Definition
*   For EACH step, define: **"How do we know it works?"**
*   Bad: "Implement API."
*   Good: "Implement API. Verify with `curl -X POST ...` returns 200."

### Step 3: Complexity & Risk Assessment
*   Flag steps that are "One-Way Doors" (hard to reverse).
*   Flag steps that require manual user testing.

## 3. Artifact Generation
Create or Update `implementation_plan.md` (or the active Task List).

**Template:**
```markdown
# Implementation Plan - [Feature]

## User Review Required
[Critical interaction points]

## Proposed Changes
### [Component]
- [ ] **Step 1:** [Action]
    - *Verification:* [Command/Check]
- [ ] **Step 2:** [Action]
    - *Verification:* [Command/Check]

## Verification Plan
### Automated Tests
[Commands to run]

### Manual Verification
[User actions]
```

## 4. State Update
**CRITICAL:** Update `.resonance/01_state.md` to reflect that we are now in the **Execution Phase** for this feature.
- Update `## Current Phase` to `Development`.
- Add the high-level goal to `## Active Work`.
