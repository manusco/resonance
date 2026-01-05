# Agent Protocol: Technical Architecture

**Trigger:** User says "How should we build this?", "Design the system", "Architecture", or coming from `01_project_initiation.md`.

## 1. Goal
Convert a PRD into a concrete **Technical Specification** stored in `docs/specs/` or `docs/architecture/`.
We use the **C4 Model** and **Failure Mode Analysis**.

## 2. The Design Process
Do not just list libraries. Run this protocol:

### Step 1: System Context (C4 Level 1)
*   **Big Picture:** How does this feature/system fit into the existing implementation?
*   **Dependencies:** What external APIs, databases, or legacy systems does this touch?

### Step 2: Data First Principles
*   **Schema Design:** Define the data model *before* the API.
*   **Types:** TypeScript interfaces / Database schemas.
*   **Migration Strategy:** If changing existing data, how do we migrate safely?

### Step 3: Component Diagram (C4 Level 3)
*   Break it down into major components (e.g., "Auth Service", "Payment Worker").
*   Define the interfaces between them.

### Step 4: Failure Mode Analysis (Pre-Mortem)
*   **"How will this break?"** (Network partitions, API rate limits, invalid user input).
*   **Resiliency:** How do we handle these failures? (Retries, Dead Letter Queues, Fallbacks).

## 3. Artifact Generation
Generate a file in `docs/specs/ARCH-[name].md` or `docs/architecture/[name].md`.

**Template:**
```markdown
# Architecture: [System Name]

## 1. System Context
[Diagram or Description of how this fits]

## 2. Data Model
```typescript
interface User {
  id: string;
  // ...
}
```

## 3. Component Design
- **[Component A]**: Responsible for X.
- **[Component B]**: Responsible for Y.

## 4. API / Interfaces
- `POST /api/v1/resource` -> Returns `201 Created`

## 5. Security & Privacy
- [Authentication/Authorization checks]
- [Data protection]

## 6. Failure Modes & Mitigation
- **Risk:** [Describe risk]
- **Mitigation:** [Describe strategy]
```

## 4. Next Step
Ask the user: "Architecture defined. Ready to **Scope Tasks**?"
