---
description: Synchronize state.md (The Map) with Git History (The Territory).
---

# Roadmap Sync Protocol (`/update-roadmap`)

> **Role**: The Manager (`resonance-core`)
> **JTBD**: Realignment. Anti-Hallucination.
> **Input**: `git log`, `.resonance/01_state.md`.
> **Output**: Updated `state.md`.

## 1. Prerequisites
*   [ ] `state.md` exists.
*   [ ] Git history exists.

## 2. Context (The Reality Check)
<thinking>
I am the GPS.
The "Plan" says we are at Step 1. The "Code" says we are at Step 5.
Drift = Failure.
I must make the Map match the Territory.
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Read Territory
*   **Tool**: `run_command("git log -n 10 --oneline")`.
*   **Action**: Identify what *actually* happened.

### Step 2: Read Map
*   **Tool**: `read_file(".resonance/01_state.md")`.
*   **Action**: Identify what we *thought* happened.

### Step 3: Reconcile
*   **Mark Done**: If Git says feature is merged -> `[x]`.
*   **Context Update**: Add new constraints found during code.
*   **Next Step**: Re-calculate the immediate next step.

## 4. Recovery
*   **Conflict**: If Map and Territory diverge wildly, favor Territory (Git). Update Map to reflect Reality.

## 5. Governance (Definition of Done)
*   **Artifact**: Updated `state.md`.
*   **State Update**: "Roadmap Synced."
