# 🔄 Resonance Upgrade Guide: v1.8 to v1.9

This guide helps you migrate your existing Resonance project to the **v1.9 (Antigravity Edition)**.

## 🧱 The Core Shift

Resonance v1.9 is a fundamental refactor focused on **Continuity** and **Elite Specialization**. 

| Feature | Legacy (v1.8) | Modern (v1.9) |
| :--- | :--- | :--- |
| **Logic Root** | `AGENTS.md` | `.agent/skills/` & `.agent/workflows/` |
| **Memory** | Volatile Chat History | `.resonance/` Persistent Files |
| **Specialists** | `roles/` (Loose) | `resonance-*` Skills (Strict) |
| **Execution** | Prompting | Protocols / Workflows |

---

## 🏃 Quick Start: The "Auto-Upgrade"

Antigravity can help you migrate. Open a chat and run:

```bash
@Resonance /migrate_legacy
```

*(Note: If the workflow isn't available yet, follow the manual steps below.)*

---

## 🛠️ Manual Migration Steps

### 1. Structure Cleanup
The new structure uses `.agent/` for instructions and `.resonance/` for project state.

**Move your configurations:**
*   If you had custom agent prompts, convert them into `SKILL.md` format in `.agent/skills/`.
*   If you had project goals, move them to `.resonance/00_soul.md`.
*   If you had a "Todo" list, move it to `.resonance/01_state.md`.

### 2. Rename Legacy Folders
If you have these folders, they are now obsolete:
*   `roles/` -> Replace with `.agent/skills/`
*   `.resonance/roles/` -> Replace with `.agent/skills/`
*   `.resonance/workflows/` -> Replace with `.agent/workflows/`

### 3. Initialize the States
Create the "Brain" of your project if it doesn't exist:
- `.resonance/00_soul.md`: High-level vision.
- `.resonance/01_state.md`: Current phase and task.
- `.resonance/02_memory.md`: Log of decisions.

---

## ⚡ The Antigravity Advantage

v1.9 is optimized for the **Antigravity environment**:
- **Tool-Aware**: Skills now explicitly know how to use `run_command`, `browser_subagent`, and `multi_replace_file_content`.
- **Session Continuity**: If the agent reboots, it reads `.resonance/01_state.md` and picks up exactly where it left off.
- **Workflow Driven**: Workflows like `/design_system` force the agent to produce artifacts (C4 diagrams, ADRs) instead of just talking.

---

## 🆘 Troubleshooting

**"The agent is still looking for AGENTS.md"**
We've added a proxy `AGENTS.md` to redirect legacy lookups. Once the agent is "retrained" by reading the new `README.md` or `.resonance/00_soul.md`, it should stop looking for the old file.

**"My custom roles are gone"**
The new framework is stricter. We recommend using the provided `resonance-*` skills and adding your custom logic as specific *Skills* in `.agent/skills/`.

---

*Need help? Run `@Resonance /system_audit` to check your project health.*
