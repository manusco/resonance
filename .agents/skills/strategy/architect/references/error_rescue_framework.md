# Error & Data Flow Mapping Framework

> **Source**: Integration of gstack `/plan-eng-review` & `/plan-ceo-review` principles.
> **Objective**: Catch silent failures in the planning phase before they become production incidents.

## 1. Zero Silent Failures
Every failure mode must be visible—to the system (logs), to the team (alerts), and to the user (UI). A failure that happens silently is a critical architectural defect.

## 2. The Error & Rescue Map
For every new service, API call, database mutation, or complex method, you MUST define the following table in your design:

| Method / Codepath | What can go wrong? | Exception Class | Rescued? (Y/N) | User Sees | System Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ProcessPayment` | External API timeout | `TimeoutError` | Y | "Gateway unavailable" | Retry 2x, then fail |
| `ParseImport` | Bad JSON structure | `JSON::ParserError` | N (GAP) | 500 Server Error | NONE (BAD) |

*Rule:* `rescue StandardError` is always an anti-pattern. Name the specific exceptions.

## 3. Data Flow Shadow Paths
A happy path is not enough. Every data flow has one happy path and **three shadow paths**. Trace all four for every new flow:

1.  **Happy Path**: Data is present and valid.
2.  **Nil Path**: Input is totally missing (nil/null). What happens?
3.  **Empty Path**: Input exists but is empty/zero-length. What happens?
4.  **Error Path**: The upstream service/database fails. What happens?

## 4. Interaction Edge Cases
Map UI/User interactions adversarially:
*   **Double-click/submit**: Concurrent requests processing the same action.
*   **Stale state**: User submits a form but the background data changed 5 minutes ago.
*   **Async timeout**: User navigates away while a background job is still running.

## 5. ASCII Diagrams Mandatory
No non-trivial flow goes undiagrammed. Use ASCII art to map:
*   State Machine transitions
*   Data pipelines
*   Architecture boundaries
