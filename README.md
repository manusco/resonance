# Resonance: The Operating System for AI Agents

**Persistent memory • Role orchestration • Built for Google Antigravity**

[![Google Antigravity](https://img.shields.io/badge/Google-Antigravity-blue)](https://github.com/manusco/resonance)
[![AI Agent Framework](https://img.shields.io/badge/AI-Agent%20Framework-green)](https://github.com/manusco/resonance)
[![License MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> Give your AI agent **persistent memory**, **specialist roles**, and **self-healing** capabilities. Built for solo founders using Google Antigravity who need to ship fast without losing context.

**Maintained by [divisionAI.co](https://divisionAI.co)**

---

## Why AI Agents Need Persistent Memory

**The Problem**: Your AI coding assistant forgets context between sessions. You spend hours re-explaining your architecture, coding style, and project goals.

**The Solution**: Resonance gives your agent a persistent file system (`.resonance/`) that acts as its long-term memory.

---

## When Resonance is Perfect For You

- ✅ **Solo founders & small teams**: No time for heavyweight enterprise frameworks with dozens of folders
- ✅ **Iterative development**: Your vision evolves rapidly; your agent needs to keep up
- ✅ **Vibe coding**: You work by feel and flow, not rigid specification documents  
- ✅ **Multi-agent orchestration**: Ready for multiple specialized agents working together

---

## What Makes Resonance Different

### Active Operating System, Not Passive Docs
Other frameworks are static markdown files the agent *might* read. Resonance is an **operating system** the agent runs on.

### Built for Google Antigravity
Leverages Antigravity's unique capabilities:
- **Terminal access** → Self-healing via `resonance.sh`
- **Artifact system** → UI task lists auto-sync to `.resonance/01_state.md`
- **Persistent sessions** → Agent maintains context across conversations

### Universal Socket for Agent Skills
Import any specialist from Anthropic Skills or custom prompts:
```
Role Switch product     # Product requirements (no code)
Role Switch architect   # System design (no implementation)
Role Switch qa          # Testing specialist (finds edge cases)
Role Switch researcher  # Deep research (no coding, just insights)
Role Switch frontend    # High-end UI/UX (prevents AI slop)
```

Infinite extensibility. Zero maintenance.

---

## Installation

### Option 1: Copy & Paste (Fastest)
```bash
# In your project root
curl -o AGENT.md https://raw.githubusercontent.com/manusco/resonance/main/AGENT.md
```

### Option 2: Clone Template
```bash
npx degit manusco/resonance/template my-project
cd my-project
```

### Option 3: Manual
1. Download [`AGENT.md`](https://github.com/manusco/resonance/blob/main/AGENT.md)
2. Place it in your project root
3. Done!

---

## Quick Start (30 seconds)

**In Google Antigravity:**

1. **Install**: Copy `AGENT.md` to your project root
2. **Initialize**: Say to your agent:
   ```
   Resonance Init
   ```
3. **The agent will**:
   - Create `.resonance/` directory
   - Generate `00_soul.md`, `01_state.md`, `02_memory.md`, `03_tools.md`
   - Set up the `roles/` directory with 5 benchmark-quality specialists
   - Start operating with persistent memory

4. **(Optional) Load a specialist**:
   ```
   Role Switch architect
   ```

**That's it.** No npm install. No configuration files. Just paste and go.

---

## What Happens Next?

Your agent now has:
- ✅ **Persistent memory** - Remembers context across sessions (`.resonance/01_state.md`)
- ✅ **Self-healing** - Can run `./resonance.sh` to check system health
- ✅ **Artifact sync** - UI task lists automatically sync to disk
- ✅ **Specialist roles** - Switch between product, architect, qa, researcher, frontend modes
- ✅ **Research logging** - All web research saved to `.resonance/02_memory.md`

---

## Example: First Session

```
You: "Resonance Init"

Agent: "✅ Resonance System Online
- Created .resonance/ directory
- Generated soul.md (vision document)
- Set up state tracking
- Initialized 5 specialist roles

What are we building?"

You: "A SaaS app for managing podcasts"

Agent: "I've updated 00_soul.md with our vision.
Current state: Planning phase.
Should I switch to product role to write requirements?"
```

---

## Advanced: Skills (The Game-Changer)

Resonance v1.1 turns your agent into a **skill orchestrator**. Import personas from anywhere.

### How to Install Skills from External Libraries

Want to use a specific agent persona you found online?

1. **Find:** Browse Anthropic Skills, GitHub repos, or create custom prompts
2. **Copy:** Copy the agent's prompt text
3. **Import:** Tell Antigravity:
   ```
   Create a new role named 'SecurityExpert'. 
   Here is the prompt content: [PASTE]. 
   Save it to .resonance/roles/security.md
   ```
4. **Activate:** Say: `Role Switch SecurityExpert`

### Stock Roles Included

Resonance ships with 5 benchmark-quality specialist roles:

- **product**: Product Requirements Engineer - Write world-class PRDs, user stories, acceptance criteria
- **architect**: System Architect - Design system architecture, ADRs, trade-off analysis  
- **qa**: QA Engineer - Comprehensive testing strategy, edge case discovery, quality metrics
- **researcher**: Research Engineer - Technical research, documentation, knowledge synthesis
- **frontend**: Frontend/UX Engineer - High-end UI/UX, design systems, prevents AI slop

### Future: Multi-Agent Orchestration

Resonance is designed for the future where you can run multiple agents simultaneously:
- Agent A in `product` role → writes requirements
- Agent B in `architect` role → designs system
- Agent C in default mode → implements features
- Agent D in `frontend` role → polishes UI
- Agent E in `qa` role → writes tests  
- All sync to `01_state.md` for coordination

**Why This Matters:** You don't maintain a library of 50 skills. You become the **Universal Socket** they all plug into.

---

## The Value Proposition

**For enterprise teams**: Stick with heavyweight frameworks built for governance and compliance.

**For builders who ship fast**: Resonance is your AI agent's operating system. One file (`AGENT.md`) to start. The agent maintains the rest.

---

## Pro Tips

- **Commit `.resonance/`** to git - It's your agent's brain. Don't lose it.
- **Use `Role Switch product`** when planning - Get clear requirements before coding
- **Use `Role Switch architect`** for design - Prevents premature implementation
- **Use `Role Switch frontend`** for UI - Prevents generic AI SaaS slop
- **Check `02_memory.md`** regularly - See what your agent learned
- **Run `./resonance.sh`** if agent seems confused - Reloads context

---

## The Workflow

The ideal development flow using Resonance:

```
Product Requirements → Architecture → Implementation → Frontend → QA → Research
      (product)          (architect)     (default)      (frontend)  (qa)  (researcher)
```

Each role has strict boundaries. Specialists can't code. Coders can't design architecture. This prevents the chaos of "jack of all trades, master of none" AI behavior.

---

## Architecture

```
project-root/
├── AGENT.md                    # The kernel (default full-stack role)
├── resonance.sh                # Self-healing script
└── .resonance/
    ├── 00_soul.md              # Vision, principles, North Star
    ├── 01_state.md             # Current status (persistent memory)
    ├── 02_memory.md            # Lessons learned (immutable log)
    ├── 03_tools.md             # Terminal command boundaries
    └── roles/                  # Specialist personas
        ├── product.md          # Product Requirements Engineer
        ├── architect.md        # System Architect
        ├── qa.md               # QA Engineer
        ├── researcher.md       # Research Engineer
        └── frontend.md         # Frontend/UX Engineer
```

---

## License

MIT © [divisionAI.co](https://divisionAI.co)

---

## Contributing

Resonance is designed for solo developers and small teams. If you need enterprise features, reach out to [divisionAI.co](https://divisionAI.co) for custom architecture.

**Built with ❤️ for builders who ship.**