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
- **Active Workflows** → `.resonance/workflows/` scripts guide you through PRDs and Architecture
- **Persistent sessions** → Agent maintains context across conversations

### Universal Socket for Agent Skills
Import any specialist from Anthropic Skills or custom prompts:
```
Role Switch product     # Product requirements (no code)
Role Switch architect   # System design (no implementation)
Role Switch qa          # Testing specialist (finds edge cases)
Role Switch researcher  # Deep research (no coding, just insights)
Role Switch frontend    # High-end UI/UX (prevents AI slop)
Role Switch backend     # API & Logic implementation (no DB/Frontend)
Role Switch growth      # Funnel optimization & AARRR metrics
Role Switch debugger    # Root Cause Analysis & fixation
Role Switch venture_validator # Business model validation
```

Infinite extensibility. Zero maintenance.

---

## Installation

### Option 1: Copy & Paste (Fastest)
```bash
# In your project root
curl -o AGENTS.md https://raw.githubusercontent.com/manusco/resonance/main/AGENTS.md
```

> **⚠️ Important**: This downloads **only the kernel file** (`AGENTS.md`). You must then **initialize the framework** (see Quick Start below).

### Option 2: Clone Template
```bash
npx degit manusco/resonance/template my-project
cd my-project
```

### Option 3: Manual
1. Download [`AGENTS.md`](https://github.com/manusco/resonance/blob/main/AGENTS.md)
2. Place it in your project root
3. **Next**: Initialize the framework (see Quick Start below)

---

## Quick Start (30 seconds)

**In Google Antigravity:**

1. **Install**: Copy `AGENTS.md` to your project root (using curl or manual download)
2. **Initialize**: Open your project in Antigravity and say to your agent:
   ```
   Resonance Init
   ```
3. **The agent will automatically**:
   - Create `.resonance/` directory
   - Generate `00_soul.md`, `01_state.md`, `02_memory.md`, `03_tools.md`
   - **Download 10 benchmark-quality specialist roles from GitHub** (not AI-generated)
   - Start operating with persistent memory

4. **(Optional) Load a specialist**:
   ```
   Role Switch architect
   ```

**That's it.** No npm install. No configuration files. Just paste and go.

### ✅ What You Should See

After running `Resonance Init`, your project structure should look like:

```text
├── AGENTS.md                   # The kernel (you downloaded this)
├── resonance.sh                # Self-healing script (auto-generated)
├── docs/                       # UNIFIED MEMORY (PRDs, Specs)
└── .resonance/                 # Created by agent
    ├── 00_soul.md
    ├── 01_state.md
    ├── 02_memory.md
    ├── 03_tools.md
    ├── workflows/              # Active Protocols (Initiation, Scoping)
    ├── scripts/                # Utility scripts (safe-commit)
    └── roles/                  # 16 specialist personas
        ├── product.md
        ├── ...
```

### 🔧 Troubleshooting

**Problem**: "I ran curl but nothing happened"
- **Solution**: The curl command only downloads `AGENTS.md`. You must tell the agent `Resonance Init` to create the folder structure.

**Problem**: "The `.resonance/` folder is missing or incomplete"
- **Solution**: Say to your agent: `Resonance Init` or `./resonance.sh` to regenerate missing files.

---

## What Happens Next?

Your agent now has:
- ✅ **Persistent memory** - Remembers context across sessions (`.resonance/01_state.md`)
- ✅ **Self-healing** - Can run `./resonance.sh` to check system health
- ✅ **Artifact sync** - UI task lists automatically sync to disk
- ✅- **Benchmark specialist roles** - Downloaded 14 curated roles from GitHub (not AI-generated)
- ✅ **Research logging** - All web research saved to `.resonance/02_memory.md`

---

## ⚡ Quick Command Cheatsheet

### 🟢 Start
*   **Init System**: `Resonance Init`
*   **Start Project**: *"I want to build [idea]. Draft a PRD."*

### 🟡 Plan
*   **Draft Specs**: *"Start initiation protocol"* (Generates PRD)
*   **Design System**: *"Run architecture protocol"* (Generates C4/ADR)
*   **Scope Tasks**: *"Plan the work"* (Generates task list)

### 🔵 Roles
*   **Product Mode**: `Role Switch product`
*   **Architecture Mode**: `Role Switch architect`
*   **Implementation**: `Role Reset` (Default)
*   **Testing**: `Role Switch qa`
*   **Marketing**: `Role Switch conversion_engineer`

### 🟣 Utils
*   **Check Health**: `./resonance.sh`
*   **Update System**: *"Update Resonance"* (Runs Update Protocol)
*   **Review PRs**: *"Review open pull requests"* (Runs PR Protocol)
*   **Testing**: *"Test this module"* (Runs Testing Protocol)
*   **Audit Security**: *"Start security audit"* (Runs Security Protocol)
*   **System Check**: *"Run system check"* (Runs Health & Quality Protocol)
*   **Debug**: *"Fix this bug"* (Runs Scientific Debugging Protocol)
*   **Safe Commit**: `.resonance/scripts/safe-commit.sh "msg" file`

---

## Example: First Session

```
You: "Resonance Init"

Agent: "✅ Resonance System Online
...
To get started, simply describe your idea."

You: "A SaaS app for managing podcasts."

Agent: "**Understood. I have drafted a PRD for 'PodcastOS'.**
It includes a Press Release, User Stories, and Non-Goals.
Please review `docs/specs/PRD-PodcastOS.md`."
```

---

## Upgrading to v1.6
Already using Resonance? Update your roles to get the new **Backend**, **Growth**, **Debugger**, and **Venture Validator** personas.

Ask your agent to run this:
```bash
# Update existing roles
curl -o .resonance/roles/frontend.md https://raw.githubusercontent.com/manusco/resonance/main/.resonance/roles/frontend.md

# Install new roles
curl -o .resonance/roles/backend.md https://raw.githubusercontent.com/manusco/resonance/main/.resonance/roles/backend.md
curl -o .resonance/roles/growth.md https://raw.githubusercontent.com/manusco/resonance/main/.resonance/roles/growth.md
curl -o .resonance/roles/debugger.md https://raw.githubusercontent.com/manusco/resonance/main/.resonance/roles/debugger.md
curl -o .resonance/roles/venture_validator.md https://raw.githubusercontent.com/manusco/resonance/main/.resonance/roles/venture_validator.md
```

---

## Advanced: Skills (The Game-Changer)

Resonance v1.6 includes **knowledge frontmatter protocol** and **safe-commit helpers** for better documentation discovery and atomic git commits.

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

Resonance ships with 16 benchmark-quality specialist roles:

- **product**: Product Requirements Engineer - Write world-class PRDs, user stories, acceptance criteria
- **architect**: System Architect - Design system architecture, ADRs, trade-off analysis  
- **qa**: QA Engineer - Comprehensive testing strategy, edge case discovery, quality metrics
- **researcher**: Research Engineer - Technical research, documentation, knowledge synthesis
- **reviewer**: Code Reviewer - Static analysis, style enforcement, security checks ("The Gatekeeper")
- **frontend**: Frontend/UX Engineer - High-end UI/UX, design systems, prevents AI slop
- **backend**: Backend Engineer - API design, business logic, integrations
- **database**: Database Architect - Schema design, query optimization, data modeling
- **security**: Security Auditor - Vulnerability assessment, OWASP, threat modeling
- **performance**: Performance Engineer - Profiling, latency optimization, Core Web Vitals
- **devops**: DevOps Engineer - CI/CD, IaC, containers, observability
- **seo**: SEO Strategist - Technical SEO, content strategy, keyword research
- **growth**: Growth Strategist - AARRR metrics, funnel optimization
- **conversion_engineer**: Conversion Engineer - Landing page architecture, CRO, persuasion psychology
- **debugger**: Elite Debugger - Root Cause Analysis, surgical fixes
- **venture_validator**: Venture Validator - Business model stress-testing

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

**For builders who ship fast**: Resonance is your AI agent's operating system. One file (`AGENTS.md`) to start. The agent maintains the rest.

---

## Pro Tips

- **Commit `.resonance/`** to git - It's your agent's brain. Don't lose it.
- **Use `Role Switch product`** when planning - Get clear requirements before coding
- **Use `Role Switch architect`** for design - Prevents premature implementation
- **Use `Role Switch frontend`** for UI - Prevents generic AI SaaS slop
- **Check `02_memory.md`** regularly - See what your agent learned
- **Run `./resonance.sh`** if agent seems confused - Reloads context
- **Run `./resonance.sh`** if agent seems confused - Reloads context
- **Trigger Workflows** - Say "Start new project" to run the Initiation Protocol
- **Use knowledge frontmatter** - Add `summary` and `read_when` to `docs/*.md` for smart doc discovery
- **Use `.resonance/scripts/safe-commit`** - Atomic commits with safety guardrails (prevents accidental `git add .`)


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

├── AGENTS.md                   # The kernel (default full-stack role)
├── resonance.sh                # Self-healing script
├── docs/                       # UNIFIED MEMORY (Specs, PRDs)
└── .resonance/
    ├── 00_soul.md              # Vision, principles, North Star
    ├── 01_state.md             # Current status (persistent memory)
    ├── 02_memory.md            # Lessons learned (immutable log)
    ├── 03_tools.md             # Terminal command boundaries
    ├── workflows/              # Active Protocols (Initiation, Arch, Scoping)
    ├── scripts/                # Utility scripts (safe-commit)
    └── roles/                  # Specialist personas
        ├── product.md          # Product Requirements Engineer
        ├── architect.md        # System Architect
        ├── ... (14 total)
```

---

## License

MIT © [divisionAI.co](https://divisionAI.co)

---

## Contributing

Resonance is designed for solo developers and small teams. If you need enterprise features, reach out to [divisionAI.co](https://divisionAI.co) for custom architecture.

**Built with ❤️ for builders who ship.**