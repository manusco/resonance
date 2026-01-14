---
description: Update Resonance skills and workflows from the source.
---

# Workflow: Update Framework ("The Upgrade")

**Trigger**: "Update Resonance", "Get latest skills".
**Context**: Syncing with the Antigravity upstream.

## 1. Backup
- [ ] **Snapshot**: Copy current `.agent` to `.agent_backup`.

## 2. Fetch
- [ ] **Pull**: Get latest `SKILL.md` and Workflows.
- [ ] **Diff**: Check for breaking changes/customizations.

## 3. Validation
- [ ] **Verify**: Ensure JSON/YAML syntax is valid.
- [ ] **Test**: Run a dummy task to ensure no regression.
