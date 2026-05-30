# Eng Manager Review Protocol

> **Concept**: A high-rigor technical review that ensures reliability, observability, and simplicity.

## 1. EM Cognitive Patterns

Apply these during the review:
1.  **Blast Radius**: What is the worst-case scenario? How many systems/people are affected?
2.  **Boring by Default**: Use proven technology. Only spend "innovation tokens" where they provide 10x value.
3.  **Systems over Heroes**: Design for a tired human at 3am, not a genius on their best day.
4.  **Essential vs Accidental Complexity**: Are we solving the business problem, or a problem we created with our architecture?
5.  **Make it Easy, then make the easy change**: Refactor first, implement second. Never change structure and behavior simultaneously.

## 2. Failure Mode Registry

For every new codepath/integration, map the failures:

| Codepath | Failure Mode | Rescued? | Test? | User Sees? | Logged? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| API Call | Timeout | Y | Y | Retry Msg | Y |
| DB Write | Lock Timeout | N | N | **Silent/500** | N |

**CRITICAL GAP**: Any row with Rescued=N, Test=N, User Sees=Silent.

## 3. Data Flow Tracing (Shadow Paths)

Trace every data flow through these four paths:
1.  **Happy Path**: Data flows correctly.
2.  **Nil Path**: Input is nil/missing.
3.  **Empty Path**: Input is zero-length/empty.
4.  **Error Path**: Upstream dependency fails.

## 4. Operational Requirements

*   **Observability**: Logs, Metrics, and Traces are first-class deliverables.
*   **Rollback Path**: Explicit plan for "What if this breaks production?".
*   **ASCII Diagrams**: mandatory for data pipelines and state transitions.
