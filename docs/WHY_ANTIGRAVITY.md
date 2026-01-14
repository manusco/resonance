# Why Google Antigravity Needs Resonance

Google Antigravity represents a paradigm shift in AI-assisted development. It's not just a chatbot—it's an **autonomous agent** with native skills, terminal access, and browser control.

But with great power comes a critical challenge: **state management**.

---

## The Problem: Stateless Agents

Traditional AI coding assistants are stateless. Every new chat session is a blank slate.
This forces you to re-explain the stack, the rules, and the context every single time. It wastes hours.

---

## The Resonance Solution (v1.9)

Resonance acts as the **Operating System** for Antigravity, providing:

### 1. Persistent State (The Brain)
`.resonance/01_state.md` acts as the agent's external hard drive. Sessions come and go, but the state persists.
*   **Soul (`00_soul.md`)**: The Vision.
*   **Memory (`02_memory.md`)**: The History.

### 2. Specialized Skills (The Talent)
Antigravity supports "Skills" (`.agent/skills/`) natively. Resonance provides **17 Elite Skills** out of the box:
*   `resonance-architect`: Design systems.
*   `resonance-qa`: Break systems.
*   `resonance-devops`: Automate systems.

These aren't just prompts; they are **interactive toolkits** that Antigravity can call upon to perform expert labor.

### 3. Scientific Workflows (The Protocol)
Blind coding is forbidden. Resonance enforces specific workflows (`.agent/workflows/`):
*   **Project Init**: Validation -> Press Release -> Spec.
*   **Refactoring**: Structural Audit -> Code Surgery -> Verification.
*   **Debugging**: Reproduction -> Hypothesis -> Fix (Scientific Method).

---

## Why Local Native?

Resonance v1.9 lives **in your repo**.
*   **No API Keys**: It uses your project's context.
*   **No External Servers**: It runs locally in your workspace.
*   **Portable**: The `.agent/` folder travels with your git repo. Any developer with Antigravity becomes an expert instantly.

---

## Comparison

| Capability | Antigravity Alone | Antigravity + Resonance |
|-----------|-------------------|-------------------------|
| **Memory** | Session-only (Ephemermal) | **Persistent** (`.resonance/`) |
| **Roles** | Generic "Assistant" | **17 Elite Specialists** (`.agent/skills/`) |
| **Process** | Ad-hoc / Chat-based | **Scientific Workflows** (`.agent/workflows/`) |
| **Learning** | Forgets after chat closes | **Remembers forever** (`02_memory.md`) |

---

## Get Started

1. **Install**: Clone the `.agent/` and `.resonance/` folders into your root.
2. **Initialize**: Run `@Resonance /init_project`.
3. **Build**: Your agent now has persistent memory and specialist skills.

**Antigravity gives agents autonomy. Resonance gives them purpose.**
