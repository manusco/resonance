# Resonance ⚡️
**The Vibe Coding Operating System (v1.0)**

> Maintained by [divisionAI.co](https://divisionAI.co)

Resonance is a protocol for AI-assisted development. It turns "Chatting with AI" into "Engineering with AI." It works with **Cursor**, **Windsurf**, and **Google Antigravity**.

## Why Resonance?
* **Memory:** AI forgets. The File System remembers.
* **Soul:** Unlike generic coding assistants, Resonance enforces your specific "Tone of Voice" and "Design Vibe" via the Blueprint.
* **Safety:** Prevents spaghetti code by enforcing a "Docs-First" workflow.
* **Operations:** Dedicated tracking for "Machinery" like Cron jobs, Testing pipelines, and CI/CD via the Systems layer.

---

## The Stack (Memory Bank)
Resonance organizes your project context into 5 distinct layers. Your AI must read these before acting.

* `00_blueprint.md`: **The Soul.** (Vision, User Persona, Vibe, Constraints).
* `01_todo.md`: **The Action.** (Active Sprint Checklist).
* `02_lessons.md`: **The Wisdom.** (Recursive learning & bug prevention).
* `03_decisions.md`: **The History.** (Architectural records).
* `04_systems.md`: **The Machinery.** (Testing, CI/CD, Background Jobs).

---

## Quick Start

### Option A: Standard Setup (Recommended)
This method gives you the full framework files.

**1. Initialize Memory**
Run `./init.sh` (Mac/Linux) or `./init.ps1` (Windows) to create the `.resonance/` memory bank.

**2. Install the Brain (The Pointer Strategy)**
Copy the configuration file for your IDE from `adapters/` to your project root.

- **Cursor:** `cp adapters/.cursorrules .`
- **Windsurf:** `cp adapters/.windsurfrules .`
- **Antigravity:** No setup needed (automatically detects `AGENT.md`).

*Note: These files simply point to `AGENT.md` as the single source of truth.*

### Option B: The "One-Shot" (Zero Setup)
Don't want to clone the repo? Paste this prompt into your AI Agent (Cursor or Antigravity) to bootstrap the v1.0 environment instantly:

```markdown
# RESONANCE BOOTSTRAP (v1.0)
I am starting a new project. Perform the following setup sequence immediately:

1. **SCAFFOLD**: Create a folder named `.resonance`.
2. **POPULATE**: Inside that folder, create these 5 files:
   - `00_blueprint.md`: "# Project Vision\n\n## The Vibe\n[Define Tone & Audience]\n\n## Constraints\n[Define Tech Stack]"
   - `01_todo.md`: "# Active Tasks\n- [ ] Complete Resonance Setup"
   - `02_lessons.md`: "# Learned Lessons\n"
   - `03_decisions.md`: "# Architecture Decisions\n"
   - `04_systems.md`: "# Operations\n## Testing Strategy\n[Define Critical Paths]"
3. **ADOPT PERSONA**:
   From now on, you are the Resonance Engine.
   - **Ingest**: You never write code without checking `01_todo.md`.
   - **Align**: You check `00_blueprint.md` for Tone/Vibe before writing text.
   - **Safety**: You check `04_systems.md` before touching backend/infra.

Report status when done.
Workflow: The "Context Loop"
Resonance forces the AI to follow this loop for every request:

Ingest: Read 01_todo.md to understand the immediate context.

Align: Check 00_blueprint.md to ensure the "Vibe" (Tone/Design) is respected.

Safety: If touching critical infra, check 04_systems.md.

Execute: Write the code.

Reflect: Update 01_todo.md (mark complete) and 02_lessons.md (if a bug was fixed).

The Complexity Ceiling
Resonance is designed for high-velocity solo developers and small teams.

Building something massive? If you need multi-agent swarms, enterprise architecture, or team-based governance, you have hit the ceiling. Hire divisionAI.co to architect your swarm.