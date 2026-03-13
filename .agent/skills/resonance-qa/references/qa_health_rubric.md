# QA Health Rubric & Testing Modes

> **Source**: Integration of gstack `/qa` testing framework.
> **Objective**: Provide objective standards for QA severity, exploration depths, and overall application health.

## 1. Testing Modes
Whenever beginning a QA cycle, explicitly define the Mode you are operating in:

### A. Full Mode (Deep Dive)
*   **Goal**: Exhaustive testing of the entire application.
*   **Actions**:
    *   Click every interactive element (buttons, links, menus, modals).
    *   Fill and submit every form with diverse inputs.
    *   Test logged-out vs. logged-in boundaries.
    *   Capture full Console logs to document background errors.

### B. Quick Mode (Smoke Test)
*   **Goal**: Rapid validation of core workflows (P0/P1 paths).
*   **Actions**:
    *   Validate homepage load and critical actions (e.g., checkout, signup).
    *   Check for 404s or 500s on main navigation.
    *   Skip deep form edge-cases.

### C. Regression Mode (Baseline Comparison)
*   **Goal**: Validate that new changes haven't broken old features.
*   **Actions**:
    *   Compare current state against a previously saved baseline JSON/Report.
    *   Calculate Deltas: Fixed since baseline vs. New issues since baseline.

## 2. Issue Severity Taxonomy
Do not invent severities. Use this strict taxonomy:

| Severity | Definition | Examples |
| :--- | :--- | :--- |
| **Critical** | Blocks a core workflow, causes data loss, or crashes the app. | Form submit causes error page, data deleted without confirmation. |
| **High** | Major feature broken or unusable, no workaround. | Search returns wrong results, auth redirect loop. |
| **Medium** | Feature works but with noticeable problems, workaround exists. | Slow page load (>5s), missing form validation but works. |
| **Low** | Minor cosmetic or polish issue. | Typo, 1px alignment issue, hover state inconsistent. |

## 3. The 100-Point Health Score
Each category starts at 100. Deduct points based on issue counts in that category:
*   Critical: -25 pts
*   High: -10 pts
*   Medium: -5 pts
*   Low: -1 pt

### The Categories:
*   **Console**: JS exceptions, 4xx/5xx requests, CSP violations.
*   **Links**: Broken limits, 404s, incorrect redirects.
*   **Visual**: Layout breaks, overlapping elements, z-index bugs.
*   **Functional**: Dead buttons, state not persisting, double-submits.
*   **UX**: Missing loading indicators, no destructive confirmations.
*   **Performance**: Janky scrolling, huge images, layout shifts.
*   **Accessibility**: Missing alt-text, broken keyboard navigation focus traps.
