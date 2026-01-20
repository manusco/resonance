---
description: Ensure code meets standards before merging (CI/CD, Linting, Security).
---

# Audit Protocol (`/review`)

> **Role**: The Auditor (`resonance-security` + `resonance-reviewer`)
> **JTBD**: Prevent Entropy. Detect Vulnerabilities.
> **Input**: Current Branch / Recent Changes.
> **Output**: Review Report (Blocker/Warning/Nit).

## 1. Prerequisites
*   [ ] Code is committed or staged.
*   [ ] Build passes.

## 2. Context (The Swarm)
<thinking>
I am the Gatekeeper. I assume the code is broken/insecure until proven otherwise.
I will spawn specialists to look at the code from different angles:
1.  **Security**: OWASP, Auth, Secrets.
2.  **Performance**: Re-renders, Query speed.
3.  **Quality**: DRY, YAGNI, Smell.
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Security Scan
*   **Tool**: `grep_search`
*   **Action**: Scan for secrets, `eval()`, weak crypto.
*   **Task**: `Task(resonance-security, "Audit recent changes for vulnerabilities.")`

### Step 2: Quality Scan
*   **Tool**: `run_command("npm run lint")`
*   **Action**: Check for structural issues.
*   **Task**: `Task(resonance-reviewer, "Check for code smell and Cognitive Complexity.")`

### Step 3: Synthesis
Combine findings.
*   **BLOCKER (P0)**: Security holes, Data Loss.
*   **WARNING (P1)**: Perf regression, spaghetti code.
*   **NIT (P2)**: Style, Naming.

## 4. Recovery
*   **False Positives**: If a linter rule is overly strict, suppress it with a comment AND rationale.
*   **Too Many Issues**: If > 5 Blockers, reject wholesale. Return to `/refactor`.

## 5. Governance (Definition of Done)
*   **Artifact**: Review Summary.
*   **Decision**: APPROVE (Clean) or REJECT (Changes Requested).
*   **State Update**: Task status.
