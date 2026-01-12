# Workflow: Task Scoping ("The Execution Plan")

**Primary Roles**: `backend`, `frontend`, `database`
**Goal**: Convert Architecture into **Atomic, Verifiable Steps**.
**Output**: `implementation_plan.md` with "Ralph Loop" integration.

---

## 1. Trigger
User accepts the Architecture from `02_technical_architecture.md` OR runs `/plan`.

## 2. Phase 0: The Spec Gap
**CRITICAL**: You CANNOT plan what hasn't been specified.

**Check**: Does a detailed specification exist in `docs/specs/` for this feature?
*   **NO**: 🛑 STOP. Tell the user: "I cannot plan this without a spec. Use `/spec` first."
*   **YES**: Proceed.

## 3. Phase 1: Context Pinning & Story Mapping (Role: `product`)
1.  **Context Pinning**:
    *   Locate the source spec (e.g., `docs/specs/PRD-auth.md`).
    *   **CRITICAL**: You must LINK this spec in the `implementation_plan.md` header.
2.  **Story Mapping**:
    *   Ensure every User Story in the PRD has a corresponding set of Technical Tasks.
    *   *If stories are missing Gherkin*: Pause and fix the PRD.

## 3. Phase 2: The Breakdown (Roles: `backend` / `frontend`)
Decompose the work into vertical slices.

1.  **Database First (Role: `database`)**:
    *   Define the Schema (SQL) first.
    *   Task: "Create migration X."
2.  **API Second (Role: `backend`)**:
    *   Define the Interface (OpenAPI/Types).
    *   Task: "Implement Endpoint Y with Mock."
3.  **UI Third (Role: `frontend`)**:
    *   Define the Component Props.
    *   Task: "Build Component Z connected to Mock Y."

## 4. Phase 3: The Verification Protocol ("Ralph Loop")
**Every step must be verifiable.**
For each task, define *how* the Agent will prove it works without human success.

*   **Pattern**: `Repro` -> `Fix` -> `Verify`.
*   **Constraint**: If you can't verify it with a script, break it down further.

## 5. Artifact Generation
Update `implementation_plan.md`.

**Template:**
```markdown
# Implementation Plan
> **Spec**: [docs/specs/PRD-name.md](...)

## Phase 1: Database & Core Logic
- [ ] **DB Migration**: Add `orders` table.
    - *Verification*: Run `_check_db_schema.ts` (Inspects information_schema).
- [ ] **API Endpoint**: `POST /orders`
    - *Loop Check*: `curl` returns 404.
    - *Implementation*: NestJS Controller.
    - *Verification*: `curl` returns 201 + DB row exists.

## Phase 2: Frontend
- [ ] **Order Component**
    - *Verification*: `npm run test:component Order` (React Testing Library).
```

## 6. Transition
Ask: "Plan locked. **Execute**?" (Implicitly moving to specific Role modes).
