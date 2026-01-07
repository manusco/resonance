# Workflow: Resonance Update ("The Upgrade")

**Trigger**: User says "Update Resonance" or "Upgrade System".
**Goal**: Update core files while **preserving User Memory**.
**Principle**: "Memory is Sacred."

---

## 1. Safety Check (Pre-Flight)
1.  **Git Clean?**: `git status --porcelain` must be empty. Stash or commit if dirty.
2.  **Backup**: Copy current `.resonance` to `.resonance_backup_[date]` (Optional but recommended).

## 2. The Core Update (Overwrite Safe)
These files define the "OS" and are safe to overwrite IF standard.
*   `AGENTS.md`
*   `resonance.sh`
*   `workflows/*.md` (Standard ones)

**Command:**
```bash
# Update Kernel
curl -o AGENTS.md https://raw.githubusercontent.com/manusco/resonance/main/AGENTS.md
curl -o resonance.sh https://raw.githubusercontent.com/manusco/resonance/main/resonance.sh

# Update Workflows (Standard Only)
curl -o .resonance/workflows/01_project_initiation.md https://raw.githubusercontent.com/manusco/resonance/main/.resonance/workflows/01_project_initiation.md
# ... (repeat for 02-07 & 99)
```

## 3. The Role Update (Smart Merge)
Roles are often customized. Do NOT overwrite blindly.

1.  **Check**: `git diff .resonance/roles/[role].md` with upstream.
2.  **Strategy**:
    *   **If identical**: Update.
    *   **If modified**: Prompt user or skip. "Found custom [role]. Skipping update to preserve customizations."

## 4. The Immune System (Immutable Files)
**NEVER TOUCH THESE:**
*   `.resonance/00_soul.md` (Vision)
*   `.resonance/01_state.md` (Context)
*   `.resonance/02_memory.md` (History)
*   `.resonance/03_tools.md` (Capabilities)
*   `docs/` (Specs)

## 5. Post-Upgrade Verification
1.  **Reload**: Run `./resonance.sh`.
2.  **Report**:
    > "Resonance upgraded to v[Latest].
    > - Kernel updated.
    > - [N] Workflows updated.
    > - Roles skipped: [List of custom roles].
    > - Memory intact."

## 6. Integration with State
Log the upgrade in `02_memory.md`: "System upgraded on [Date]. Changelog: ..."
