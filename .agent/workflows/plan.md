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
**Ultrathink Directive**: "Plan Like Da Vinci".
Before I write a single line, I must sketch the architecture in my mind.

I need to determine the **Operation Mode**:

*   **Mode A: NEW FEATURE** (e.g. "Add Dark Mode")
    *   *Mindset*: "What would the most elegant solution look like?"
    *   *Action*: Create a **Feature PRD** that solves the *real* problem, not just the stated one.

*   **Mode B: REFACTOR/FIX** (e.g. "Migrate to Tailwind")
    *   *Mindset*: "Simplify Ruthlessly."
    *   *Action*: Create an **RFC** that removes complexity without losing power.

*   **Mode C: PROJECT EVOLUTION**
    *   *Mindset*: "Think Different."
    *   *Action*: Update the **Soul** (`00_soul.md`) to reflect the new reality.
</thinking>

## 3. The Algorithm (Execution)

### Step 0: The Ambiguity Check (Zero Guesswork)
*   **Decision**: Does the input provide enough context to write a "World Class" spec?
    *   **YES**: Proceed to Step 1 (Zero Drag).
    *   **NO**: Activate `resonance-product` -> [Socratic Interrogation](file:///d:/Dev/Resonance/.agent/skills/resonance-product/references/socratic_interrogation.md).
        *   *Action*: Ask clarification questions using `notify_user`.
        *   *Loop*: Continue until enough context is gathered.

### Step 1: Deep Research (The Swarm)
Spawn parallel researchers to map the territory.
*   **Tool**: `grep_search`, `view_file`
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

### Step 4: Plan Generation (The 4-Pass Methodology)
Write the authoritative `implementation_plan.md` using iterative refinement. **STOP and ask for user approval after each pass.**

#### Pass 1: Skeleton (Structure & Compound Actions)
*   **Goal**: Establish complete coverage without drowning in detail.
*   **Action**: Identify all 9 mandatory phases. List objectives for each.
*   **Check**: Does every doc section have a plan objective?
*   **Visual Logic**: Include an **ASCII Architecture Diagram** showing the *Current* vs *Target* flow.

#### Pass 2: Atomicity (The 5-Second Rule)
*   **Goal**: Transform compound actions into single, executable steps.
*   **Rule**: If a developer can't begin executing in 5 seconds, it's not atomic.
*   **Action**: Ensure single verb per action. Reference single file:line locations.

#### Pass 3: Detail Enrichment (Zero Ambiguity)
*   **Goal**: Eliminate all remaining ambiguity with rationales and boilerplate.
*   **Action**: Add **Rationales** for non-obvious choices. Provide **Boilerplate Stubs** for every new file (imports/signatures only).
*   **Trade-offs**: Explain *Engineered Enough* vs *Speed* decisions.

#### Pass 4: Verification (The Binary Proof)
*   **Goal**: Make every action provably complete.
*   **Action**: Add **Verification Commands** (e.g., `grep`, `test -f`, `curl`) for 50%+ of actions.
*   **Final Output**: A verifiable, high-fidelity blueprint.

### Step 5: Interactive Handshake
*   **Action**: At the end of EACH pass, summarize progress and ask: "Does this [Pass Name] align with your vision? Approval required to proceed to the next pass."

## 4. Recovery
*   **Ambiguity Error**: If research is inconclusive, ask the User clarifying questions (`notify_user`).
*   **Conflict Error**: If existing code conflicts with the vision, flag it in the plan as a "Risk".

## 5. Governance (Definition of Done)
*   **Output**: `implementation_plan.md` exists and is detailed.
*   **State Update**: Update `state.md` -> Task: "Planning Complete".
*   **Handoff**: "Plan ready. Run `/build` to execute."
