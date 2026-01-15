---
description: Migrate a Resonance project from v1.8 to v1.9.
---

# Workflow: Legacy Migration ("The Great Leap")

**Trigger**: "Migrate from v1.8", "/migrate_legacy", "Upgrade structure".
**Context**: Reorganizing legacy folders into the new Antigravity-native structure.

## 1. Audit
- [ ] **Scan**: Look for legacy directories (`roles/`, `.resonance/roles/`, `agents.md`).
- [ ] **Inventory**: List existing custom agents and their instructions.

## 2. Transformation
- [ ] **Core Setup**: Initialize `.resonance/` with `00_soul.md`, `01_state.md`, and `02_memory.md` if missing.
- [ ] **Skill Conversion**: Convert legacy role definitions into `.agent/skills/` markdown format.
- [ ] **Workflow Setup**: Copy standard Resonance v1.9 workflows into `.agent/workflows/`.

## 3. Cleanup
- [ ] **Decommission**: Rename old folders to `[folder]_old` to avoid confusion.
- [ ] **Redirect**: Ensure `AGENTS.md` is replaced with the v1.9 redirector.

## 4. Verification
- [ ] **Health Check**: Run `./resonance.sh`.
- [ ] **Status**: Update `.resonance/01_state.md` to reflect the new v1.9 state.

---
*Note: This workflow is destructive regarding folder names but preserves content in backup directories.*
