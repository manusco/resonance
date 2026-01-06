# Workflow: Pull Request Review

**Trigger**: User says "Review PRs", "Check pull requests", or "Merge this".
**Primary Role**: `reviewer` (Code Reviewer) or `qa`
**Goal**: Verify code quality and strictly gate-keep the main branch.

## 1. Preparation Phase
*   **Check Auth**: Ensure `gh` CLI is ready.
    ```bash
    gh auth status
    ```
*   **List Candidates**:
    ```bash
    gh pr list --state open
    ```
    *(Ask user which PR to review if multiple exist)*

## 2. Ingestion Phase
*   **Fetch Code**:
    ```bash
    gh pr checkout [ID]
    ```
*   **Get Context**:
    ```bash
    gh pr view [ID] --comments
    ```
*   **Detailed Diff Analysis**:
    ```bash
    # Read the diff filenames to understand scope
    gh pr diff [ID] --name-only
    
    # Read the actual changes
    gh pr diff [ID]
    ```

## 3. Analysis Protocol ("The Gatekeeper Review")
As the **Reviewer**, analyze the `gh pr diff` output for:
1.  **Correctness**: Does it actually solve the stated problem?
2.  **Security**: Any unvalidated inputs? Hardcoded secrets?
3.  **Maintainability**: Is the code readable? Are functions too complex?
4.  **Tests**: Are there new tests covering the changes?

## 4. Verification Execution
*   **Run Tests**:
    ```bash
    npm test # or equivalent
    ```
*   **Start Dev Server** (if visuals needed):
    *(Ask user to verify UI if applicable)*

## 5. Decision & Action
Present your findings to the User using the **Review Template**:

> **PR #[ID]: [Title]**
> *   **Summary**: [What changed]
> *   **Risk Level**: [Low/Med/High]
> *   **Test Status**: [Pass/Fail]
> *   **Recommendation**: [Merge / Request Changes]
>
> **Top Issues:**
> 1. [Issue 1]
> 2. [Issue 2]

### If Approved:
```bash
gh pr merge [ID] --squash --delete-branch
```

### If Changes Requested:
*(Draft the comment for the user)*
```bash
gh pr comment [ID] --body "Review feedback: ..."
```
