---
description: Automates the creation of documentation for solved problems.
---

# Knowledge Protocol (`/capture`)

> **Role**: The Librarian (`resonance-librarian`)
> **JTBD**: Prevent Amnesia. Compound Intelligence.
> **Input**: Solved Problem / Bug Fix.
> **Output**: `docs/solutions/[topic].md`.

## 1. Prerequisites
*   [ ] A "Win" occurred (Fixed bug, Shipped feature).
*   [ ] Context is fresh in memory.

## 2. Context (The Compound)
<thinking>
We just wasted X hours solving this.
If we don't write it down, we will waste X hours again next month.
I will write this for "Future Me".
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Synthesis
*   **Action**: Summarize the "War Story".
    *   **Context**: What broke?
    *   **Root Cause**: Why?
    *   **Solution**: How fixed?

### Step 2: Categorization
*   **Action**: Pick a `docs/` subfolder.
    *   `docs/patterns/` (Architecture).
    *   `docs/troubleshooting/` (Bugs).
    *   `docs/setup/` (Config).

### Step 3: Archival
*   **Action**: Write markdown file.
    *   Format: Problem -> Diagnosis -> Solution.

## 4. Recovery
*   **Vague Docs**: If LLM writes generic text ("fixed bug"), REJECT. Demand specific error codes and diffs.

## 5. Governance (Definition of Done)
*   **Artifact**: New file in `docs/`.
*   **State Update**: Task: "Knowledge Captured".
