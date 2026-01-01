# Multi-Agent Orchestration with Resonance

The future of AI-assisted development isn't a single omniscient agent. It's **specialized agents working together**.

Resonance v1.1 is designed from the ground up for multi-agent orchestration.

---

## The Single-Agent Problem

Traditional AI coding assistants try to be everything:
- Product manager
- System architect  
- Frontend developer
- Backend developer
- QA engineer
- DevOps specialist

**The result?** Jack of all trades, master of none.

---

## The Multi-Agent Vision

Instead of one agent doing everything, imagine:

- **Agent A** (Product role) → Writes requirements  
- **Agent B** (Architect role) → Designs architecture  
- **Agent C** (Default role) → Implements features  
- **Agent D** (Frontend role) → Polishes UI/UX  
- **Agent E** (QA role) → Writes comprehensive tests  

Each agent is **world-class** at their specialty. None of them step on each other's toes.

---

## How Resonance Enables Multi-Agent Orchestration

### 1. Shared State (`.resonance/01_state.md`)

All agents read and write to the same state file. This is the **single source of truth**.

```markdown
# .resonance/01_state.md

## Current Phase
Implementation

## Active Tasks
- [x] PRD written (Agent A - product role)
- [x] Architecture designed (Agent B - architect role)
- [/] Feature implementation (Agent C - default role)
- [ ] UI polish (Agent D - frontend role)
- [ ] Test coverage (Agent E - qa role)
```

Agents coordinate through the state file. No overlap. No confusion.

### 2. Role-Based File Access

Each role has **strict boundaries**:

**Product role** (Agent A):
- ✅ Can edit: Requirements docs
- ❌ Cannot: Write code, design architecture

**Architect role** (Agent B):
- ✅ Can edit: `00_soul.md`, ADRs, system diagrams
- ❌ Cannot: Write implementation code

**Default role** (Agent C):
- ✅ Can edit: All production code
-  ❌ Cannot: Override architectural decisions

**Frontend role** (Agent D):
- ✅ Can edit: UI/CSS files, design systems
- ❌ Cannot: Touch backend code

**QA role** (Agent E):
- ✅ Can edit: Test files only
- ❌ Cannot: Fix bugs directly (documents them instead)

**Why this matters**: Agents can't interfere with each other's work. The product agent can't accidentally write code. The QA agent can't "fix" bugs instead of testing them.

### 3. Handoff Protocol

Agents hand off work explicitly:

```
Agent A (product): 
"PRD complete. Saved to .resonance/state.md. 
Ready for architect to design system."

Agent B (architect):
"Architecture designed. ADR-001 created. 
3 implementation options documented.
Ready for developer to choose and implement."

Agent C (default):
"Feature implemented per architecture.
Ready for frontend polish."

Agent D (frontend):
"UI polished with custom design system.
Ready for QA."

Agent E (qa):
"20 tests written. 
Found 3 edge cases. Documented in 02_memory.md.
Ready for developer to fix."
```

Each agent updates `01_state.md` when done. The next agent picks up from there.

### 4. Immutable Learning Log

`.resonance/02_memory.md` prevents agents from repeating mistakes:

```markdown
## 2025-01-15: Bug Fix - Auth Token Expiry
- **Problem**: Users logged out unexpectedly
- **Solution**: Refresh token 5 minutes before expiry
- **Lesson**: Always implement token refresh proactively
- **Agent**: Agent C (default role)

## 2025-01-16: Design Decision - Color Palette
- **Decision**: Use HSL instead of hex for brand colors
- **Rationale**: Easier to generate tints/shades programmatically
- **Agent**: Agent D (frontend role)
```

All agents read from this shared memory. Nobody repeats past mistakes.

---

## Example: Multi-Agent Build Workflow

**Scenario**: Build an authentication system

### Phase 1: Product Requirements (Agent A)
```
User: "Role Switch product"
User: "Write a PRD for user authentication"

Agent A:
- Writes detailed PRD
- Defines user stories, acceptance criteria
- Lists edge cases (expired tokens, concurrent logins,  etc.)
- Saves to .resonance/01_state.md
- Marks: "✅ PRD complete. Ready for architecture."
```

### Phase 2: Architecture (Agent B)
```
User: "Role Switch architect"
User: "Design the auth system based on the PRD"

Agent B:
- Reads PRD from 01_state.md
- Creates ADR-005: "Use NextAuth.js vs Auth0"
- Designs system architecture (diagram)
- Documents trade-offs
- Updates 00_soul.md with auth principles
- Marks: "✅ Architecture complete. Ready for implementation."
```

### Phase 3: Implementation (Agent C)
```
User: "Role Reset"
User: "Implement the auth system per the architecture"

Agent C:
- Reads architecture from 01_state.md and ADR-005
- Implements NextAuth.js integration
- Follows the documented design decisions
- Marks: "✅ Implementation complete. Ready for frontend."
```

### Phase 4: Frontend Polish (Agent D)
```
User: "Role Switch frontend"
User: "Create a premium login UI"

Agent D:
- Designs custom login component (no AI slop)
- Implements design tokens for consistency
- Adds microinteractions (button states, loading spinners)
- Ensures accessibility (keyboard nav, ARIA labels)
- Marks: "✅ UI complete. Ready for QA."
```

### Phase 5: QA Testing (Agent E)
```
User: "Role Switch qa"
User: "Test the auth system comprehensively"

Agent E:
- Writes unit tests, integration tests, E2E tests
- Tests edge cases: expired tokens, invalid credentials, concurrent logins
- Finds bug: "Token doesn't refresh on mobile Safari"
- Documents bug in 02_memory.md
- Marks: "❌ 1 bug found. Needs dev fix."
```

### Phase 6: Bug Fix (Agent C)
```
User: "Role Reset"
User: "Fix the Safari token refresh bug"

Agent C:
- Reads bug report from 02_memory.md
- Fixes the issue
- Logs solution to 02_memory.md
- Marks: "✅ Bug fixed. Ready for re-test."
```

---

## Benefits of Multi-Agent Orchestration

### 1. Specialization
Each agent is world-class at their role. The QA agent *thinks like a tester*. The frontend agent *thinks like a designer*.

### 2. No Context Switching
Single agents suffer from "mode confusion"—one moment they're writing PRDs, the next they're implementing CSS. Multi-agent systems stay in their lane.

### 3. Parallel Work
Multiple agents can work simultaneously:
- Agent C implements Feature A
- Agent D polishes UI for Feature B
- Agent E writes tests for Feature C

All coordinated through `01_state.md`.

### 4. Quality Through Constraints
When the QA agent **cannot** fix bugs (only document them), it stays adversarial. It doesn't fall into "oh I'll just fix this real quick" mode.

---

## Future: Fully Autonomous Swarms

Imagine:
```
User: "Build a SaaS for podcast management"

[Resonance spawns 5 agents]

Agent A (product): Writes PRD
    ↓ Hands off to Agent B
Agent B (architect): Designs system
    ↓ Hands off to Agent C
Agent C (default): Implements backend + frontend
    ↓ Hands off to Agent D
Agent D (frontend): Polishes UI
    ↓ Hands off to Agent E
Agent E (qa): Tests everything, documents bugs
    ↓ Loops back to Agent C if bugs found

All agents coordinate through .resonance/01_state.md
All agents learn from .resonance/02_memory.md
All agents respect boundaries in their role files
```

**Result**: A production-ready SaaS built by specialized AI agents, coordinated by Resonance.

---

## Get Started with Multi-Agent Orchestration

1. Install Resonance: `curl -o AGENT.md https://raw.github.com/manusco/resonance/main/AGENT.md`
2. Initialize: `Resonance Init` in Antigravity
3. Switch roles: `Role Switch [product|architect|qa|researcher|frontend]`
4. Coordinate through `01_state.md`

**Built for the multi-agent future. Ready today.**
