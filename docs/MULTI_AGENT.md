# Multi-Agent Orchestration with Resonance (v1.9)

The future of AI-assisted development isn't a single omniscient agent. It's **specialized skills working together**.

Resonance v1.9 is designed from the ground up for multi-agent orchestration using Antigravity's native `skills` architecture.

---

## The Vision: A Crew, Not A Chatbot

Instead of one agent attempting to do everything, Resonance defines specialized **Skills** that act as virtual expert agents:

- **`resonance-product`** (Product Manager) → Writes requirements & PRDs.
- **`resonance-architect`** (System Architect) → Designs C4 models & ADRs.
- **`resonance-backend`** (Backend Engineer) → Implements API & Database logic.
- **`resonance-frontend`** (Frontend Engineer) → Polishes UI/UX & Design Systems.
- **`resonance-qa`** (QA Engineer) → Writes destructive tests.
- **`resonance-devops`** (SRE) → Manages pipelines & reliability.

Each skill is **world-class** at its specialty. None of them step on each other's toes.

---

## How Resonance Orchestrates

### 1. Shared State (`.resonance/01_state.md`)

All skills read and write to the same state file. This is the **single source of truth**.

```markdown
# .resonance/01_state.md

## Current Phase
Implementation

## Active Tasks
- [x] PRD written (resonance-product)
- [x] Architecture designed (resonance-architect)
- [/] Feature implementation (resonance-backend)
- [ ] UI polish (resonance-frontend)
```

### 2. Skill-Based Boundaries

Each skill has **strict boundaries** defined in its `SKILL.md`:

**`resonance-product`**:
- ✅ Can edit: Requirements docs (`docs/specs/`)
- ❌ Cannot: Write code, design architecture

**`resonance-architect`**:
- ✅ Can edit: `00_soul.md`, ADRs, C4 Context
- ❌ Cannot: Write implementation code

**`resonance-qa`**:
- ✅ Can edit: Test files only
- ❌ Cannot: Fix bugs directly (documents them instead)

**Why this matters**: A Product Manager shouldn't be writing CSS. A QA engineer shouldn't be "fixing" bugs. Boundaries create quality.

### 3. Handoff Protocol

Skills hand off work explicitly through the **Task Boundary**:

```
Agent (with resonance-product skill):
"PRD complete. Spec saved to docs/specs/PRD-auth.md.
Ready for system design."

Agent (switches to resonance-architect skill):
"Architecture defined. ADR-001 created.
Ready for implementation scoping."
```

### 4. Immutable Learning Log

`.resonance/02_memory.md` prevents repeated mistakes:

```markdown
## 2026-01-15: Bug Fix - Auth Token Expiry
- **Problem**: Users logged out unexpectedly on Safari.
- **Lesson**: Always implement proactive token refresh.
- **Skill**: resonance-backend
```

All skills read from this shared memory.

---

## Example: Multi-Agent Build Workflow

**Scenario**: Build an authentication system

### Phase 1: Requirements (The Product Manager)
*   **Active Skill**: `resonance-product`
*   **Action**: Writes `docs/specs/PRD-auth.md` (Press Release, User Stories).
*   **Output**: "PRD Validated. Ready for Design."

### Phase 2: Architecture (The Architect)
*   **Active Skill**: `resonance-architect`
*   **Action**: Writes `docs/architecture/ARCH-auth.md` (C4 Diagrams, ADRs).
*   **Output**: "Architecture Locked. Ready for Plan."

### Phase 3: Scoping (The Tactician)
*   **Active Skill**: `resonance-backend, resonance-frontend`
*   **Action**: Updates `implementation_plan.md` with verification steps (Ralph Loop).
*   **Output**: "Plan Verified. Ready for Code."

### Phase 4: Implementation (The Builders)
*   **Active Skill**: `resonance-backend` -> `resonance-frontend`
*   **Action**: Writes code. Updates `01_state.md`.

### Phase 5: QA (The Destructor)
*   **Active Skill**: `resonance-qa`
*   **Action**: Runs destructive tests. Finds bugs.
*   **Output**: "3 Critical Bugs found. Blocking release."

---

## Get Started

1. **Initialize**: `@Resonance /init_project`
2. **Orchestrate**: Use the `task_boundary` to switch modes or explicitly call skills.
3. **Coordinate**: Keep `01_state.md` updated as the central brain.

**Built for the multi-agent future. Ready today.**
