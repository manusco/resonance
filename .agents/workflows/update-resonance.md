---
description: Migrate a Resonance project from v1.8 to v2.0.
---

# Evolution Protocol (`/update-resonance`)

> **Role**: The Maintainer (`resonance-core`)
> **JTBD**: Upgrade the Framework kernel without breaking the user.
> **Input**: Upstream Changes.
> **Output**: Upgraded `.agent` folder.

## 1. Prerequisites
*   [ ] Network access allowed.
*   [ ] Git Status clean.

## 2. Context (The Transplant)
<thinking>
I am upgrading the OS.
I must not overwrite user customizations.
I must back up before I touch anything.
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Backup
*   **Action**: `cp -r .agent .agent.bak`.
*   **Safety**: Ensure we can revert.

### Step 2: Fetch
*   **Action**: Clone/Pull latest Resonance definitions.
*   **Note**: This updates `templates/`, `workflows/`, and `skills/`.

### Step 3: Merge (Smart)
*   **Action**: Update `skills/` and `workflows/`.
*   **Memory Check**:
    *   Resonance v2.0 stores memory in `.resonance/`.
    *   Files are tracked in git.
    *   **User Action**: Resolve any git conflicts in `00_soul.md` or `memory.md` manually to preserve your context.


### Step 4: Verification
*   **Action**: Run `/system-health`.

## 4. Recovery
*   **Broken System**: If `/system-health` fails < 50, restore backup immediately. `rm -rf .agent && mv .agent.bak .agent`.

## 5. Governance (Definition of Done)
*   **Artifact**: `.agent/` folder updated.
*   **State Update**: "Resonance Upgraded to v2.0".
