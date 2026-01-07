# Workflow: Technical Architecture ("The Blueprint")

**Primary Roles**: `architect`, `researcher`
**Goal**: Convert a PRD into a **Technical Design** with known trade-offs.
**Output**: `docs/architecture/ARCH-[name].md` containing C4 Diagrams and ADRs.

---

## 1. Trigger
User accepts the PRD from `01_project_initiation.md`.

## 2. Phase 1: The Research (Role: `researcher`)
Before designing, identify the unknowns.

1.  **Identify "Magic"**: Is there a requirement ("Real-time sync") that we don't know how to build?
2.  **Trade-off Matrix**: Compare solutions (e.g., WebSocket vs Polling).
3.  **Output**: A brief "Research Note" used by the Architect.

## 3. Phase 2: The Design (Role: `architect`)
Define the system structure using **DDD** and **C4**.

### Step 1: System Context (C4 Level 1)
*   What external systems (Stripe, OpenAI) do we touch?
*   Who are the users?

### Step 2: Container/Component (C4 Level 2/3)
*   Breakdown of services/modules.
*   **Domain Model**: Define the Entities (User, Order) and Value Objects (Email, Money).

### Step 3: Hard Decisions (ADRs)
*   Write an **Architectural Decision Record** for each major choice.
*   *Example*: "Decision: Use Postgres. Rationale: Need ACID compliance."

## 4. Artifact Generation
Create `docs/architecture/ARCH-[name].md`.

**Template:**
```markdown
# Architecture: [System Name]

## 1. System Context (C4)
[User] -> [Web App] -> [API] -> [Database]

## 2. Domain Model (DDD)
*   **Aggregate**: Order (Root)
    *   **Entity**: LineItem
    *   **Value Object**: Money
*   **Service**: PaymentService

## 3. Key Decisions (ADRs)
*   [ADR-001]: Use Supabase for Auth (Speed > Customization)
*   [ADR-002]: Use Tailwind (Standardization > Uniqueness)

## 4. Failure Modes
*   **Risk**: OpenAI API down.
*   **Mitigation**: Circuit Breaker + Queue.
```

## 5. Transition
Ask: "Architecture defined. Move to **Implementation Scoping**?"
