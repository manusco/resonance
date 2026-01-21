---
description: Ensure code meets standards before merging (CI/CD, Linting, Security).
---

# Incoming PR Protocol (`/review-pr`)

> **Role**: The Gatekeeper (`resonance-reviewer`)
> **JTBD**: Filter Noise. Safe Merging.
> **Input**: PR ID.
> **Output**: Merged PR or Rejection Comment.

## 1. Prerequisites
*   [ ] GitHub CLI (`gh`) installed and authenticated.
*   [ ] Repo is clean.

## 2. Context (Paranoia)
<thinking>
External code is untrusted. I must run it in a sandbox (my local machine) to verify it.
I checking for:
1.  **Malware/Backdoors**: (Supply chain attacks).
2.  **Quality**: Does it match our Platinum Standard?
3.  **Correctness**: Does it actually fix the issue?
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Checkout
*   **Action**: `gh pr checkout [ID]`.
*   **Action**: `npm ci` (Install dependencies safely).

### Step 2: The Audit
*   **Action**: Run `/review` workflow.
*   **Check**: `gh pr checks [ID]` (CI Status).

### Step 3: The Verdict
Use GitHub CLI.
*   **APPROVE**: `gh pr review [ID] --approve --body "LGTM. Passed Resonance Protocols."`
*   **REQUEST CHANGES**: `gh pr review [ID] --request-changes --body "Blocked: [List Reasons]"`
*   **MERGE**: `gh pr merge [ID] --squash --delete-branch`

## 4. Recovery
*   **Bad Code**: If build fails locally, reject immediately. Do not fix it for them.
*   **Conflict**: If merge conflict, ask user to rebase manually or request author to fix.

## 5. Governance (Definition of Done)
*   **State Update**: PR Merged or Commented.
