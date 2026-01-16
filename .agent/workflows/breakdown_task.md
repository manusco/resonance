---
description: Break down complex objectives into atomic, verifiable sub-tasks.
---

# Workflow: Breakdown Task ("The Decomposition")

**Trigger**: "Build the entire backend", "Refactor the core engine".
**Context**: The task is too big for the Context Window. It must be chunked.
**Principle**: If you can't verify it, you can't build it.

## 1. The Context Dump
*Activate Skill*: `resonance-product`

- [ ] **Scan**: Read all related files (`view_file`).
- [ ] **History**: Read `.resonance/02_memory.md` to avoid repeating past mistakes.
- [ ] **Constraints**: List the hard constraints (e.g., "Must communicate with Legacy API").

## 2. The Seam Identification
*Activate Skill*: `resonance-architect`

- [ ] **Identify Seams**: Where can we cut?
    -   *Vertical Slice*: Frontend + Backend for ONE feature.
    -   *Horizontal Slice*: API Layer -> DB Layer (Risky, prefer Vertical).
- [ ] **Dependency Graph**: Task A -> Task B. Ensure no circular dependencies.

## 3. The Manus Plan (Atomic Units)
*Activate Skill*: `resonance-core`

- [ ] **Initialize**: Create/Update `task_plan.md`.
- [ ] **Atomic Definition**:
    For EACH sub-task, define:
    1.  **Input**: what files will change?
    2.  **Output**: what is the verifiable artifact?
    3.  **The Test**: What command proves it works?
    
    *Example Atomic Task*:
    *   *Goal*: Create User Schema.
    *   *File*: `src/db/schema.ts`.
    *   *Verify*: `npm run db:push` (Success).

## 4. The Execution Loop
- [ ] **Route**: Pass the first Atomic Task to execution.
- [ ] **Stop**: Do not plan 10 steps ahead. Plan 3, Execute 1, Refine Plan.
