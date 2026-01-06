# Workflow: Framework Update Protocol

**Trigger**: User says "Update Resonance" or "Upgrade System".
**Primary Role**: Default (Autonomous Engineer)
**Goal**: Update core files to the latest version while **strictly preserving** user memory and customizations.

## 1. The Prime Directive of Updates
**"Memory is Sacred."**
Under NO circumstances shall you overwrite:
*   `.resonance/00_soul.md` (Vision)
*   `.resonance/01_state.md` (State)
*   `.resonance/02_memory.md` (Logs)
*   `.resonance/03_tools.md` (Boundaries)
*   `docs/` (User Documentation)

## 2. Pre-Flight Check
Before downloading anything:
1.  **Check Git Status**: Are there uncommitted changes?
    ```bash
    git status --porcelain
    ```
2.  **Scan for New Components**:
    *   Visit `https://github.com/manusco/resonance` to check if new Workflows or Roles have been added since your last update.
    *   If found, add them to your download list.

## 3. The Update Loop
Execute these steps effectively.

### A. Core & Workflow Update ("Smart Overwrite")
**Logic:**
For each file (`AGENTS.md`, `resonance.sh`, workflows...):
1.  Check if modified: `git diff --quiet [file]`
2.  **If Clean (Exit 0)**: Update.
    ```bash
    curl -o [file] https://raw.githubusercontent.com/manusco/resonance/main/[file]
    ```
3.  **If Dirty (Exit 1)**: PROMPT USER.
    *   "File `[file]` has local changes. Overwrite? (y/n)"
    *   If yes: Overwrite.
### B. Workflows (Smart Update)
Update standard protocols.
*   `01_project_initiation.md`
*   `02_technical_architecture.md`
*   `03_task_scoping.md`
*   `04_pull_request.md`
*   `05_testing_strategy.md`
*   `06_security_audit.md`
*   `07_system_check.md`
*   `08_scientific_debugging.md`
*   `99_framework_update.md`


**CRITICAL:** Users often modify roles. Do not blind-overwrite.
**Logic:**
1.  Check if role file is modified: `git diff --quiet .resonance/roles/[role].md`
2.  **If Clean (Exit Code 0)**: Safe to update.
    ```bash
    curl -o .resonance/roles/[role].md https://raw.githubusercontent.com/manusco/resonance/main/.resonance/roles/[role].md
    ```
3.  **If Dirty (Exit Code 1)**: SKIPPED.
    *   *Notify User:* "Skipped update for `[role].md` (Customized)."

## 4. Post-Update Verification
1.  Reload Context:
    ```bash
    ./resonance.sh
    ```
2.  Report:
    > "Resonance updated to v[X.X].
    > - Core files updated.
    > - [N] Roles updated.
    > - [N] Roles skipped (customized).
    > - **Memory files untouched.**"
