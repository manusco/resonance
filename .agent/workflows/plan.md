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
I must transform the User's intent into the correct Engineering Specification.
I need to determine the **Operation Mode**:

*   **Mode A: NEW FEATURE** (e.g. "Add Dark Mode", "Create Invite System")
    *   *Action*: I must create a **Specific Feature PRD** (`docs/features/[name].md`).
    *   *Reason*: Do not clutter the Master Soul (`00_soul.md`) with implementation details.

*   **Mode B: REFACTOR/FIX** (e.g. "Migrate to Tailwind", "Fix Auth Bug")
    *   *Action*: I must create an **RFC** (`docs/rfcs/[name].md`).
    *   *Reason*: These are technical changes that require a technical spec.

*   **Mode C: PROJECT EVOLUTION** (e.g. "Pivot to AI", "Rebrand")
    *   *Action*: I must update the **Master PRD** (`docs/prd/00_vision.md`) or **Soul** (`00_soul.md`).
    *   *Reason*: This changes the fundamental nature of the project.
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Deep Research (The Swarm)
Spawn parallel researchers to map the territory.
*   **Tool**: `grep_search`, `view_file`
*   **Action**: Scan existing code patterns to ensure consistency.
*   **Action**: Scan existing code patterns to ensure consistency.
    *   `Task(resonance-researcher, "Analyze existing patterns for [Feature]. Find similar implementations.")`
*   `Task(resonance-venture, "Validate against Kill Criteria. Is this feature risky?")`
    *   `Task(resonance-growth, "Analyze Virality/Retention loop. Does this drive growth?")`
    *   `Task(resonance-product, "Validate against Opportunity Tree.")`

### Step 2: Working Backwards (The Press Release)
Write the spec based on the **Operation Mode**.

#### IF FEATURE (Mode A):
*   **Action**: Create `docs/features/YYYY-MM-DD_[feature_name].md`.
    *   **Headline**: Customer-centric title.
    *   **Problem**: Why does the ecosystem suffer?
    *   **Solution**: The "Plasma" fix.
    *   **Scope**: What is IN and OUT.

#### IF REFACTOR (Mode B):
*   **Action**: Create `docs/rfcs/YYYY-MM-DD_[rfc_name].md`.
    *   **Context**: Current technical debt.
    *   **Proposal**: The new architecture.
    *   **Trade-offs**: Cost vs. Benefit.

#### IF EVOLUTION (Mode C):
*   **Action**: Update `docs/prd/00_vision.md`.
    *   **Pivot**: Rewrite the Problem/Solution/Scope.

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
