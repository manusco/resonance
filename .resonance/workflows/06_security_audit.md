# Workflow: Security Audit ("The White Hat")

**Primary Role**: `security` (Security Auditor)
**Goal**: Identify, classify, and document vulnerabilities. **Do not fix them yet.**
**Output**: A rigorous `docs/security/AUDIT-[YYYY-MM-DD].md` report.

## 1. Trigger
User says: "Audit this", "Check for vulnerabilities", "Security review", or "Run security protocol".

## 2. Phase 1: Recon & Scope
Before looking at code, identify the **Jewels**:
1.  **What are we protecting?** (User Data, PII, Payment Info).
2.  **What affects it?** (Auth Service, Payment API, Database).
3.  **Where are requirements?** (Read `docs/specs/` or `01_state.md`).

## 3. Phase 2: Automated Recon (The Low Hanging Fruit)
Run available tooling to catch known issues.
*   **Dependencies**:
    ```bash
    npm audit
    # or
    pip check
    ```
*   **Static Analysis** (if available):
    *   Check for hardcoded secrets (`grep -r "API_KEY" .`)
    *   Check for visible configuration files.

## 4. Phase 3: Threat Modeling (STRIDE)
Perform a mental walk-through of the architecture (refer to `security.md` for definitions).
*   **Spoofing**: Can I become someone else? (Check Auth logic).
*   **Tampering**: Can I change data? (Check Validation).
*   **Information Disclosure**: Can I see what I shouldn't? (Check Logs/Errors).

## 5. Phase 4: Manual Code Review ("The Deep Dive")
Focus your "Eye of Sauron" on these critical paths:

### A. Authentication & Authorization (The Front Door)
*   [ ] Are passwords hashed?
*   [ ] Is there a "Forgot Password" logic flaw?
*   [ ] **IDOR Check**: Can I change `user_id` in the API to see others' data?

### B. Input Validation (The Shield)
*   [ ] **Injections**: SQL, NoSQL, Command Injection.
*   [ ] **XSS**: Is user input sanitized before display?
*   [ ] **Type Checking**: Do we trust the client? (Never trust the client).

### C. Data Handling (The Vault)
*   [ ] Are secrets in `.env` or hardcoded?
*   [ ] Is PII logging enabled? (Check `console.log` arguments).

## 6. Phase 5: Reporting
Generate the Audit Artifact. Do not clutter the chat. Create the file.

**Template**:
```markdown
# Security Audit Report
**Date**: [YYYY-MM-DD]
**Scope**: [Files/Features Audited]

## Executive Summary
[High-level verification of health. e.g. "System is generally secure but lacks rate-limiting."]

## Critical Issues (Must Fix Immediately)
### [CRI-001] [Title]
*   **Location**: `path/to/file.js`
*   **Vector**: [How to exploit]
*   **Remediation**: [Specific fix]

## High Issues (Fix Before Release)
...

## Medium/Low (Tech Debt)
...
```

## 7. Next Steps
Ask the user: "Audit complete. Report generated. Should I **create tickets** for the Critical issues or **switch to Debugger** role to fix them?"
