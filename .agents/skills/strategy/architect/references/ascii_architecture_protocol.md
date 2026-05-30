# Protocol: Low-Fidelity Visualization (ASCII Architecture)

> **Status**: Core Implementation Standard
> **Objective**: Use portable, text-based diagrams to verify logic, workflow, and structural changes before implementation.

## 1. Why ASCII? (The Expert Rationale)

High-fidelity tools (Figma, Mermaid) have their place, but ASCII art is **Atomic**.
*   **Zero Render Pipeline**: It works in pure text, terminals, and code comments.
*   **Version Controlled**: Changes show up as clear diffs in Git.
*   **Shared Mental Model**: It forces both Agent and User to agree on the "Nodes" and "Edges" of a system without being distracted by styling.

## 2. Diagram Archetypes

### A. The "Before vs. After" (Delta Analysis)
Always visualize the *Current State* and the *Target State* to highlight the impact of the change.

```text
CURRENT:
[User] -> [Monolith] -> [DB]

TARGET:
[User] -> [API Gateway] -> [Auth Service]
                        -> [Business Logic] -> [DB]
```

### B. Functional Flow (The Pipeline)
Describe how data moves through the gates of the system.

```text
Input -> [Validation Gate] -> [Sanitization] -> [Persistence]
               |                  ^
               v                  |
          [Error Handler] ---------+
```

## 3. Operational Rules

1.  **Mandatory for /plan**: For any non-trivial change (e.g., adding a new service, changing a state machine), an ASCII diagram is required.
2.  **Naming Consistency**: Labels in the diagram must match the `class` or `function` names used in the code.
3.  **Horizontal for Flow**: Read left-to-right for sequential logic.
4.  **Vertical for Stack**: Read top-to-bottom for layering.

---
*Created by the Architect. Part of the Outstanding Skills Standard.*
