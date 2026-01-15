# 🧠 AGENTS.md has Evolved!

> **IMPORTANT**: The "Legacy Role System" (v1.8 and prior) has been superseded by the **Resonance v1.9 (Antigravity Edition)** architecture.

If you are looking for your agents, they haven't disappeared—they have **leveled up**.

## 🚀 What changed?

1.  **From Roles to Skills**: Instead of monolithic `roles/`, we now use granular, elite **Skills** located in [`.agent/skills/`](./.agent/skills/).
2.  **From Chat to Workflows**: Instead of just "acting" like a role, the agent now follows scientific **Workflows** in [`.agent/workflows/`](./.agent/workflows/).
3.  **Unified Kernel**: The "Brain" of the project is now managed by the **Resonance Core** in [`.resonance/`](./.resonance/).

## 🛠️ How to Upgrade

If you just updated and things look different:

### 1. The New Entry Point
You no longer need to check `AGENTS.md` to see what I can do. Just ask me for `/status` or check the new structure.

### 2. Migration Guide
*   **Old Role** -> Now a **Skill** in `.agent/skills/`.
*   **Old Instructions** -> Now part of the **Soul** in `.resonance/00_soul.md`.
*   **Old Goal** -> Now the **Objective** in `.resonance/01_state.md`.

### 3. "Waking Up" the System
Run the new system check to ensure everything is in order:
```bash
./resonance.sh
```

---

## 🖤 Why the change?
We moved from "Roleplay" to "Engineering". Resonance v1.9 is designed to be **Agentic Native**, leveraging the full power of the Antigravity environment (Terminal, Browser, Filesystem) with persistent memory that survives session reboots.

**Welcome to the future of agentic coding.**

---
*This file exists to guide users and agents transitioning from older versions. You can safely delete it once you are comfortable with the new structure, but keeping it helps other agents find their way.*
