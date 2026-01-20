---
description: Transform feature descriptions into well-structured project plans using deep research and SpecFlow analysis.
---

# Inception Protocol (`/plan`)

> **Role**: The Architect (`resonance-architect`)
> **JTBD**: Convert ambiguity into a "World Class" Implementation Plan.
> **Input**: User Request, Feature Idea, or Issue Link.
> **Output**: `docs/prd/00_launch.md`, `implementation_plan.md`.

## 1. Prerequisites
*   [ ] Git status is clean.
*   [ ] User has provided a high-level goal.

## 2. Context (The Vision)
<thinking>
I must transform a vague request into a rigorous engineering specification.
I will assume nothing. I will verify everything.
Is this a new feature or a modification?
Do I understand the user's intent?
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Deep Research (The Swarm)
Spawn parallel researchers to map the territory.
*   **Tool**: `grep_search`, `view_file`
*   **Action**: Scan existing code patterns to ensure consistency.
    *   `Task(resonance-researcher, "Analyze existing patterns for [Feature]. Find similar implementations.")`
    *   `Task(resonance-product, "Validate against Opportunity Tree.")`

### Step 2: Working Backwards (The Press Release)
Write the vision first.
*   **Action**: Create/Update `docs/prd/00_launch.md`.
    *   **Headline**: Customer-centric title.
    *   **Problem**: Why does the ecosystem suffer?
    *   **Solution**: The "Plasma" fix.

### Step 3: SpecFlow Analysis (The Logic)
Synthesize research into requirements.
*   **Action**: Define usage constraints.
    *   **Scale**: 10 users or 10k?
    *   **Performance**: < 100ms or background job?
    *   **Security**: Public or Internal?

### Step 4: Plan Generation
Write the authoritative `implementation_plan.md`.
*   **Structure**:
    *   **Goal**: One-line summary.
    *   **Modules**: `[NEW]`, `[MODIFY]`.
    *   **Verification**: Exact commands to prove it works.

## 4. Recovery
*   **Ambiguity Error**: If research is inconclusive, ask the User clarifying questions (`notify_user`).
*   **Conflict Error**: If existing code conflicts with the vision, flag it in the plan as a "Risk".

## 5. Governance (Definition of Done)
*   **Output**: `implementation_plan.md` exists and is detailed.
*   **State Update**: Update `state.md` -> Task: "Planning Complete".
*   **Handoff**: "Plan ready. Run `/build` to execute."
