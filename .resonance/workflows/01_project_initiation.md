# Workflow: Project Initiation ("The Launchpad")

**Primary Roles**: `product`, `venture_validator`
**Goal**: Convert a vague intent into a **Validated Product Spec**.
**Output**: `docs/specs/PRD-[name].md` containing a Press Release and Lean Canvas.

---

## 1. Trigger
User says: "I have an idea", "Start a new project", or "New feature".

## 2. Phase 1: The Validation Check (Role: `venture_validator`)
Before describing *what* to build, ask *if* we should build it.

1.  **Identify the Riskiest Assumption**:
    *   *User*: "I want an AI cat namer."
    *   *Assumption*: "People pay for cat names."
2.  **Define Kill Criteria**:
    *   "If we can't find 5 competitors making money, we kill it."
3.  **Draft Lean Canvas (Mental or Scratchpad)**:
    *   Problem? Segments? Unfair Advantage?

## 3. Phase 2: The Working Backwards Draft (Role: `product`)
Do not interrogate the user. **Draft the Press Release** immediately based on the validation.

### Step 1: The Press Release
Draft a specific, customer-centric announcement:
*   **Headline**: The value prop.
*   **Problem**: The current pain.
*   **Solution**: The new reality.
*   **Quote**: Fictional customer testimonial.

### Step 2: The "Six-Pager" (Core Requirements)
*   **User Persona**: "Solo Founder Sam".
*   **Core Loop**: User does X -> System does Y -> User gets Z.
*   **Non-Goals**: What are we NOT doing in V1? (Crucial for speed).

## 4. Artifact Generation
Create `docs/specs/PRD-[name].md`.

**Template:**
```markdown
# PRD: [Project Name]

## 1. The Validation (Lean Canvas)
*   **Problem**: [Top 3 problems]
*   **Unfair Advantage**: [Why us?]
*   **Kill Criteria**: [When do we quit?]

## 2. The Press Release (Working Backwards)
> **[Headline]**
> [Summary of the future state]
> "I used to [Problem], but now [Solution]." - [Customer]

## 3. Functional Requirements (The "What")
*   **User Story 1**: As a [User], I want [Action], so that [Benefit].
*   **User Story 2**: ...

## 4. Non-Goals (The "Anti-Scope")
*   ❌ Mobile App (V1 is Web only)
*   ❌ Multi-player (V1 is Single player)
```

## 5. Transition
Ask: "PRD Invalidated/Validated. Move to **Architecture**?"
