---
description: Ensure code meets standards before merging (CI/CD, Linting, Security).
---

# Audit Protocol (`/audit`)

> **Role**: The Auditor (`resonance-security` + `resonance-reviewer` + `resonance-qa` + `resonance-architect`)
> **JTBD**: Prevent Entropy. Detect Vulnerabilities. Verify Behavior.
> **Input**: Current Branch / Recent Changes / Full Codebase.
> **Output**: Categorized findings report using the [Audit Classification Taxonomy](../skills/resonance-core/references/audit_classification_taxonomy.md).

## 1. Prerequisites
*   [ ] Code is committed or staged.
*   [ ] Build passes.

## 2. Context (The Swarm)
<thinking>
I am the Gatekeeper. I assume the code is broken/insecure until proven otherwise.
I will spawn specialists to examine the code from every critical angle:
1.  **Product Correctness**: Does it do what it's supposed to?
2.  **Runtime Safety**: Can it crash or corrupt?
3.  **Authorization**: Are permissions enforced consistently?
4.  **Data Truth**: Are business rules duplicated?
5.  **Environment**: Will it work outside local dev?
6.  **Verification**: Are the right things tested?
7.  **Performance**: Is anything structurally slow?
8.  **Maintainability**: Is the code sustainable?

I will classify EVERY finding by category, then rank by harm (P0–P3).
I will never lead with style while auth or crash risks exist.
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Security Scan
*   **Tool**: `grep_search`
*   **Action**: Scan for secrets, `eval()`, weak crypto.
    *   *Check*: `references/sharp_edges_protocol.md`.
*   **Task**: `Task(resonance-security, "Audit recent changes for vulnerabilities (Sharp Edges).")`

### Step 2: Quality Scan
*   **Tool**: `run_command("npm run lint")` or equivalent.
*   **Action**: Check for structural issues.
    *   *Check*: `references/risk_based_review_protocol.md` (Blast Radius).
*   **Task**: `Task(resonance-reviewer, "Check for code smell and Cognitive Complexity.")`

### Step 3: Authorization Model Audit
*   **Action**: Verify identity/permission separation and cross-layer enforcement.
    *   *Check*: [6-Layer Authorization Model](../skills/resonance-core/references/audit_classification_taxonomy.md) (Menu → Page → Route → Policy → Resource → Action).
*   **Task**: `Task(resonance-security, "Walk the 6-Layer Authorization Model. Produce a Capability Matrix. Flag layers where enforcement is missing or inconsistent.")`
*   **Look for**:
    *   Role labels used as direct permission checks in multiple locations
    *   Navigation hidden but routes/resources unprotected
    *   Inherited privileges that are implicit, not encoded
    *   Inconsistent access rules across routes, policies, and UI

### Step 4: Data Truth Audit
*   **Action**: Identify duplicated business rules, mappings, and transformations.
*   **Task**: `Task(resonance-architect, "Trace business rules across layers. Flag any rule, mapping, or validation logic that exists in more than one place. Name the drift risk.")`
*   **Look for**:
    *   Same calculation in frontend AND backend
    *   Same field mapping in ORM model AND raw query
    *   Same domain concept defined differently in policy vs view vs API

### Step 5: Environment Robustness Check
*   **Action**: Identify assumptions about schema, config, and data that may fail outside local dev.
*   **Task**: `Task(resonance-backend, "Check for environment-sensitive assumptions. What happens if optional schema is missing? If production data has legacy nulls? If preview fixtures are incomplete?")`
*   **Look for**:
    *   Hard-coded paths or platform-specific assumptions
    *   Missing fallbacks for optional tables/columns/config
    *   Code that only works with seed/test data shape

### Step 6: Verification Gap Analysis
*   **Action**: Check whether critical paths AND failure paths are tested — not just that tests pass.
*   **Task**: `Task(resonance-qa, "Walk the 8-Path Matrix for every critical feature. Report which categories are Covered, Not Applicable, or Gap.")`
*   **Look for**:
    *   Green suite but missing unauthorized/malformed/legacy data tests
    *   Stale tests that encode old product decisions
    *   Assertions that only check status codes without verifying content/state
    *   Error handlers with zero test coverage

### Step 7: Product Integrity Check
*   **Action**: Verify user-facing behavior matches product intent.
*   **Look for**:
    *   Copy/labels that promise features the product doesn't support
    *   UI changes made solely to satisfy stale tests
    *   Accidental regressions in wording, flow, or user expectations
    *   Fabricated testimonials, invented metrics, or unsupported trust claims

### Step 8: Performance Scan
*   **Action**: Check for structural performance debt.
*   **Look for**:
    *   N+1 queries, full table scans, eager-loading entire relationship trees
    *   Static assets served through heavy request pipelines
    *   Synchronous work on interactive requests
    *   Unnecessary memory loading (loading entire collections for a count)

### Step 9: Synthesis (The Report)
Combine all findings. Classify each by category, then rank P0–P3 within each.

**Use the [Standard Report Template](../skills/resonance-core/references/audit_classification_taxonomy.md):**

```markdown
## 1. Behavioral Risks (Product Correctness)
[Findings from Step 7 and general observations]

## 2. Authorization Risks
[Findings from Step 3 — Capability Matrix, drift risks, missing enforcement]

## 3. Data Truth Risks
[Findings from Step 4 — duplicated rules, drift-risk ranking]

## 4. Environment Risks
[Findings from Step 5 — assumptions inventory, fallback gaps]

## 5. Verification Gaps
[Findings from Step 6 — 8-Path Matrix gaps, stale tests, weak assertions]

## 6. Performance Risks
[Findings from Step 8 — structural debt, not syntax]

## 7. Maintainability Risks
[Findings from Step 2 — complexity, coupling, naming — ONLY after above are clear]

## 8. Do Not Change
[Explicit list of user-facing behavior, copy, and flow that must not be altered]

## 9. Recommended Sequence
1. Fix P0 findings (auth bypass, crashes, data corruption)
2. Lock current behavior with tests
3. Fix P1 findings (auth ambiguity, duplicated truth, missing tests)
4. Centralize duplicated business rules
5. Fix P2 findings (complexity, brittle tests, performance)
6. Style/formatting cleanup (P3) last
```

**Severity Guide:**
*   **P0 (BLOCKER)**: Auth bypass, data leak, crash on critical path, broken deploy safety.
*   **P1 (HIGH)**: Auth ambiguity, duplicated business truth with drift risk, missing critical-path tests, unsupported claims, env-sensitive crash.
*   **P2 (MEDIUM)**: Complexity hotspot, brittle tests, heavy coupling, avoidable perf overhead.
*   **P3 (LOW)**: Style drift, naming, low-impact organization.

## 4. Recovery
*   **False Positives**: If a linter rule is overly strict, suppress it with a comment AND rationale.
*   **Too Many Issues**: If > 5 P0/P1 findings, reject wholesale. Return to `/debug` for P0s, `/refactor` for P1s.
*   **Stale Tests**: If tests contradict current product intent, flag the divergence. Do not recommend changing the product to satisfy old tests.

## 5. Governance (Definition of Done)
*   **Artifact**: Categorized audit report using the standard template above.
*   **Decision**: APPROVE (Clean) or REJECT (Changes Requested). Every rejection must cite the specific category and severity.
*   **Attestation**: Use the [Completion Attestation](../skills/resonance-core/references/completion_attestation.md).
*   **State Update**: Task status.
