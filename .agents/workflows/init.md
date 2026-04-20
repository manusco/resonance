---
description: Initialize the Resonance "Brain" (.resonance) and optionally scaffold the project.
---

# Resonance Unified Initialization (`/init`)

> **Role**: The Architect (`resonance-architect`)
> **JTBD**: Establish the Project Soul and Physical Foundation.
> **Input**: An existing folder (empty or full).
> **Output**: A `.resonance/` directory (Mind) and optional Scaffolding (Body).

## 1. Prerequisites
*   [ ] User is in the root of the project.

## 2. Context (The Vision)
<thinking>
I am the Spark.
I must extract the User's Intent (Soul) and ground it in Reality (Files).
If the folder is empty, I will offer to build the Body (Scaffolding).
If code exists, I will simply inhabit it (Memory Injection).
</thinking>

## 3. The Algorithm (Execution)

### Step 1: The Connection
*   **Action**: check for `.resonance/` directory.
    *   **Condition**: If it exists:
        *   Output: "🧠 Resonance Active. Core systems online."
        *   **Proceed to Step 2.**
    *   **Condition**: If it does NOT exist:
        *   Output: "🔌 Connecting to Resonance Core..."
        *   Action: Create `.resonance/` directory.
        *   **Proceed to Step 2.**

### Step 2: The Interview (Extraction)
*   **Action**: Assess the "Void".
    *   Check if `00_soul.md` exists.
*   **Action**: Ask the **Prime Question**:
    *   **If New Project**: "What do you want to build today? Describe in as much detail as possible."
    *   **If Existing Project**: "Resonance Memory detected. How shall we evolve the system today?"
*   **Wait**: For User Input.
*   **Analysis (Deep Thinking)**:
    *   **Vision**: Extract the "Why" and "North Star" for `00_soul.md`.
    *   **PRD**: Draft a high-level Problem/Solution/Scope for `docs/prd/00_vision.md`.
    *   **Architecture**: Infer the logical components (Frontend/Backend/DB) for `docs/architecture/system_overview.md`.

### Step 3: The Synthesis (Materialization)
*   **Action**: Create `.resonance/` and `docs/` structure.
*   **Action**: **Write the Soul** (`00_soul.md`).
    *   **Vision**: The "One Sentence" North Star.
    *   **Laws**: Derive 3 Technical Laws from the User's requested stack (e.g. "If React -> Law: Functional Components Only").
*   **Action**: **Write the PRD** (`docs/prd/00_vision.md`).
    *   **Format**: Use Amazon's "Working Backwards" style (Press Release + FAQ).
    *   **Content**: Problem, Solution, Customer Persona.
*   **Action**: **Write the Architecture** (`docs/architecture/system_overview.md`).
    *   **Format**: Mermaid JS `graph TD`.
    *   **Requirement**: Show User -> Frontend -> Backend -> DB data flow.
*   **Action**: Create `01_state.md` and `02_memory.md` (Linked).
*   **Action**: Create `03_tools.md` (Tool Boundaries) and `04_systems.md` (Architecture Map).

### Step 4: The Body (Genesis)
*   **Condition**: IF directory was empty OR user requested a new stack.
*   **Action**: **Propose Scaffolding**.
    *   "*Based on your request for [Stack], I recommend running: [Command]. Shall I proceed?*"
*   **If Yes**:
    1.  **Execute**: Run the `npm/npx/cargo` command.
    2.  **Git**: Initialize repository.
    3.  **Docs**: Generate `docs/architecture/stack_decision.md` (ADR).
*   **If No**:
    1.  **Scan**: Analyze existing codebase.
    2.  **Log**: Update `01_state.md` with "Legacy Codebase Detected".

### Step 5: Awakening
*   **Action**: Output: "🟢 Resonance Online. Memory Initialized. Foundation Set."
*   **Action**: "Ready. What is our first step?"

## 4. Governance
*   **Verification**: Check `00_soul.md` has content.
*   **State Update**: Set Phase to "Inception".
