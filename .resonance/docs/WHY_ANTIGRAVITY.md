# Why Google Antigravity Needs Resonance

Google Antigravity represents a paradigm shift in AI-assisted development. It's not just a chatbot—it's an **autonomous agent** with terminal access, browser control, and artifact management.

But with great power comes a critical challenge: **state management**.

---

## The Problem: Stateless Agents

Traditional AI coding assistants are stateless. Every new chat session is like:

```
You: "Remember, we're using Next.js with Tailwind"
AI: "Got it!"

[2 hours later, new session]

You: "Add a button to the navbar"
AI: *Generates Vue.js code*
You: "We're using React!"
AI: "Oh sorry, here's the React version"
```

This wastes hours. Every. Single. Day.

---

## Antigravity's Unique Capabilities

Google Antigravity gives agents unprecedented power:

### 1. Terminal Access
Agents can run commands directly:
```bash
npm install
git commit -m "Add feature"
npm test
```

**The risk**: Without boundaries, agents might run destructive commands.

**Resonance solution**: `.resonance/03_tools.md` defines command boundaries. Safe commands auto-run. Destructive commands require approval.

### 2. Artifact System
Agents can create UI task lists and implementation plans.

**The risk**: These artifacts are ephemeral. If you close the chat, they're gone.

**Resonance solution**: The **Sync Rule**. Every UI artifact MUST sync to `.resonance/01_state.md`. Your disk is the source of truth, not the UI.

### 3. Browser Control
Agents can research solutions online.

**The risk**: You lose the research when the session ends.

**Resonance solution**: `.resonance/02_memory.md` logs all research with URLs. Future sessions can reference past learnings.

---

## Why Resonance is Built for Antigravity

### Persistent State
`.resonance/01_state.md` acts as the agent's external hard drive. Sessions come and go, but the state persists.

### Self-Healing
`./resonance.sh` script loads the agent's "consciousness" at session start:
```bash
./resonance.sh
# Loads 00_soul.md (vision)
# Loads 01_state.md (current tasks)
# Restores context instantly
```

### Role-Based Constraints
Antigravity's power needs guardrails. Resonance provides **role-based file access**:

- **Product role**: Can only edit requirements docs (no code)
- **Architect role**: Can only design systems (no implementation)
- **QA role**: Can only write tests (no production code)
- **Frontend role**: Can only edit UI files (no backend)

This prevents the chaos of an all-powerful agent making decisions it shouldn't.

---

## The Workflow: Antigravity + Resonance

```
1. User: "Resonance Init"
   → Agent creates .resonance/ directory structure

2. User: "Role Switch product"
   → Agent reads .resonance/roles/product.md
   → Constraints applied: No code, only requirements

3. User: "Write a PRD for user authentication"
   → Agent writes detailed PRD
   → Saves to .resonance/ and updates 01_state.md

4. User: "Role Switch architect"
   → Agent reads .resonance/roles/architect.md
   → Constraints applied: No code, only design

5. User: "Design the auth system based on the PRD"
   → Agent creates ADR, system diagram
   → Updates 00_soul.md with architectural principles

6. User: "Role Reset"
   → Agent returns to full-stack developer mode
   → Implements the architecture

7. Session ends. Tomorrow:
   User: "./resonance.sh"
   → Agent instantly loads all context
   → Continues exactly where it left off
```

---

## The Key Insight

**Antigravity gives agents autonomy. Resonance gives agents memory.**

Without memory, autonomy is dangerous (agents repeat mistakes, forget constraints, lose context).

With memory, autonomy is powerful (agents remember, learn, and evolve).

---

## Comparison: Antigravity Alone vs Antigravity + Resonance

| Capability | Antigravity Alone | Antigravity + Resonance |
|-----------|-------------------|-------------------------|
| Terminal access | ✅ Yes | ✅ Yes (with boundaries) |
| Persistent memory | ❌ No | ✅ Yes (`.resonance/`) |
| Role switching | ❌ No | ✅ Yes (`roles/`) |
| Research logging | ❌ Lost | ✅ Saved to `02_memory.md` |
| Self-healing | ❌ No | ✅ Yes (`resonance.sh`) |
| Multi-agent ready | ❌ No | ✅ Yes (shared state) |

---

## Get Started

1. Copy `AGENT.md` to your project root
2. In Antigravity, say: `Resonance Init`
3. Your agent now has persistent memory and specialist roles

**Built for Google Antigravity. Designed for builders who ship.**
