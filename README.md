# Resonance ⚡️
**The Vibe Coding Operating System.**

> Maintained by [divisionAI.co](https://divisionAI.co)

Resonance is a protocol for AI-assisted development. It turns "Chatting with AI" into "Engineering with AI." It works with **Cursor**, **Windsurf**, and **Google Antigravity**.

## Why Resonance?
* **Memory:** AI forgets. The File System remembers.
* **Safety:** Prevents spaghetti code by enforcing a "Docs-First" workflow.
* **Intelligence:** The `lessons.md` file makes your AI smarter the longer you use it.

## Quick Start

### Option A: Standard Setup (Recommended)
1.  Run `./init.sh` (Mac/Linux) or `./init.ps1` (Windows) to create the `.resonance/` memory bank.
2.  **For Cursor/Windsurf:** Copy `RESONANCE_MASTER_PROTOCOL.md` content into your `.cursorrules` or `.windsurfrules`.
3.  **For Google Antigravity:** Paste the `RESONANCE_MASTER_PROTOCOL.md` content into your Agent's "System Instructions."

### Option B: The "One-Shot" (Zero Setup)
Don't want to clone the repo? Paste this prompt into your AI Agent to bootstrap instantly:

```markdown
# RESONANCE BOOTSTRAP
I am starting a new project. Perform the following setup sequence immediately:

1. **SCAFFOLD**: Create a folder named `.resonance`.
2. **POPULATE**: Inside that folder, create these 4 files with the following content:
   - `00_blueprint.md`: "# Project Vision\n\n[Context Needed]"
   - `01_todo.md`: "# Active Tasks\n- [ ] Complete Setup"
   - `02_lessons.md`: "# Learned Lessons\n"
   - `03_decisions.md`: "# Architecture Decisions\n"
3. **ADOPT PERSONA**:
   From now on, you are the Resonance Engine.
   - You NEVER write code without checking `00_blueprint.md` first.
   - You ALWAYS update `01_todo.md` after a task.
   - You CHECK `02_lessons.md` before complex logic.

Report status when done.
```

## The Complexity Ceiling
Resonance is designed for high-velocity solo developers and small teams.
**Building something massive?** If you need multi-agent swarms or enterprise architecture, you have hit the ceiling.
[Hire divisionAI.co to architect your swarm.](https://divisionAI.co)
