# Workflow: Task Scoping ("The Execution Plan")

**Primary Roles**: `backend`, `frontend`, `database`
**Goal**: Convert Architecture into **Atomic, Verifiable Steps**.
**Output**: `implementation_plan.md` with "Ralph Loop" integration.

---

## 1. Trigger
User accepts the Architecture from `02_technical_architecture.md`.

## 2. Phase 1: The Breakdown (Roles: `backend` / `frontend`)
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

## 3. Phase 2: The Verification Protocol ("Ralph Loop")
**Every step must be verifiable.**
For each task, define *how* the Agent will prove it works without human success.

*   **Pattern**: `Repro` -> `Fix` -> `Verify`.
*   **Constraint**: If you can't verify it with a script, break it down further.

## 4. Artifact Generation
Update `implementation_plan.md`.

**Template:**
```markdown
# Implementation Plan

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

## 5. Transition
Ask: "Plan locked. **Execute**?" (Implicitly moving to specific Role modes).
