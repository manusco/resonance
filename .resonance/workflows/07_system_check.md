# Workflow: System Check ("The Health Inspector")

**Primary Role**: `architect` (System Architect)
**Goal**: Perform a comprehensive deep-dive into the codebase to ensure currency, stability, and excellence.
**Output**: A consolidated `docs/reports/SYSTEM_CHECK-[date].md` report.

## 1. Trigger
User says: "System Check", "Run diagnostics", or "Health check".

## 2. The Protocol: Sequential Deep-Dive
Do not try to do everything at once. Iterate through the layers of the application.

### Phase 1: Foundation & Logic (The Core)
1.  **Architectural Audit** (`Role Switch architect`)
    *   **Check**: Circular dependencies, file structure, code duplication.
    *   **Question**: "Is the house built on rock or sand?"

2.  **Logic & Data** (`Role Switch backend` / `database`)
    *   **Check**: API efficiency, error handling, schema normalization.
    *   **Question**: "Does the data flow make sense?"

3.  **Security Scan** (`Role Switch security`)
    *   **Check**: Dependencies (`npm audit`), hardcoded secrets.
    *   *(Refer to `06_security_audit.md` for details, but keep this high-level).*

### Phase 2: Surface & Delivery (The Experience)
4.  **Frontend Polish** (`Role Switch frontend`)
    *   **Check**: Accessibility (a11y), UI consistency, Console errors.
    *   **Question**: "Does it look and feel premium?"

5.  **Quality Assurance** (`Role Switch qa`)
    *   **Check**: Test coverage, passing status.
    *   **Action**: Run `npm test` (if safe/fast).

### Phase 3: Synthesis (The Decision)
**Return to `architect` role.**

**Conflict Resolution Strategy:**
If recommendations conflict (e.g., Security vs. Performance), use this hierarchy:
1.  **Security & Stability** (Non-negotiable)
2.  **Data Integrity** (Must be accurate)
3.  **Performance** (Must be fast)
4.  **Maintainability** (Must be clean)

## 3. Artifact Generation
Create `docs/reports/SYSTEM_CHECK-[date].md`.

**Template:**
```markdown
# System Check Report: [YYYY-MM-DD]

## Executive Summary
**Health Score**: [1-10]
**Status**: [Stable/Degraded/Critical]

## Critical Issues (Immediate Action)
- [ ] [Issue 1] (Role: Security)
- [ ] [Issue 2] (Role: Backend)

## improvements (Next Sprint)
- [ ] [Improvement 1] (Role: Frontend)

## Conflict Resolution
[Notes on any trade-offs made]
```

## 4. Next Steps
Ask the user: "System Check complete. Score is [X]/10. Should we **start a repair sprint** for the critical issues?"
