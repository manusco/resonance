# Resonance: The Operating System for AI Agents

**Persistent memory • Elite Specialist Roles • Built for Google Antigravity**

[![Google Antigravity](https://img.shields.io/badge/Google-Antigravity-blue)](https://github.com/manusco/resonance)
[![AI Agent Framework](https://img.shields.io/badge/AI-Agent%20Framework-green)](https://github.com/manusco/resonance)
[![License MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> Give your AI agent **persistent memory**, **elite specialist roles**, and **self-healing** capabilities. Built for solo founders using Google Antigravity who need to ship world-class software fast.

**Maintained by [divisionAI.co](https://divisionAI.co)**

---

## Why AI Agents Need Persistent Memory

**The Problem**: Your AI coding assistant forgets context between sessions. You spend hours re-explaining your architecture, coding style, and project goals.

**The Solution**: Resonance gives your agent a persistent file system (`.resonance/`) that acts as its long-term memory and operating system.

---

## What Makes Resonance Different

### 1. Active Operating System, Not Passive Docs
Resonance is an **operating system** the agent runs on, not just a set of markdown files.

### 2. Elite Specialist Roles (v1.7)
We don't just give you "personas". We give you **Elite Roles** with specific frameworks and "Jobs to be Done":
*   **Product Manager** → Uses *Amazon Working Backwards* (Press Release first).
*   **Architect** → Uses *C4 Models* and *Domain-Driven Design*.
*   **DevOps** → Uses *GitOps* and *SRE Principles* (SLOs/SLIs).
*   **Growth** → Uses *Reforge Loops* and *AARRR Metrics*.
*   **Researcher** → Uses *First Principles* and *Decision Matrices*.
*   **Designer** → Uses *Visual Systems* and *Interaction Physics*.

### 3. Built for Google Antigravity
Leverages Antigravity's unique capabilities:
- **Terminal access** → Self-healing via `resonance.sh`
- **Artifact sync** → UI task lists auto-sync to `.resonance/01_state.md`
- **Active Workflows** → `.resonance/workflows/` scripts guide you through "The Pipeline"
- **Persistent sessions** → Agent maintains context across conversations

---

## Quick Start (30 seconds)

**In Google Antigravity:**

1. **Install**: Copy `AGENTS.md` to your project root.
   ```bash
   curl -o AGENTS.md https://raw.githubusercontent.com/manusco/resonance/main/AGENTS.md
   ```
2. **Initialize**: Open your project in Antigravity and say:
   ```
   Resonance Init
   ```
3. **The agent will automatically**:
   - Create `.resonance/` directory structure.
   - Generate `00_soul.md` (Vision) and `01_state.md` (Context).
   - **Download 17 Elite Specialist Roles**.
   - Start operating with persistent memory.

---

## The "Elite" Workflow Pipeline

Resonance v1.7 introduces a strict, high-quality pipeline for shipping software.

### 1. Initiation ("The Launchpad")
**Trigger**: "I have an idea."
**Protocol**: `01_project_initiation.md`
**Output**: A **Press Release** and **Lean Canvas** (Validated Spec).
**Roles**: `product`, `venture_validator`

### 2. Architecture ("The Blueprint")
**Trigger**: "Design the system."
**Protocol**: `02_technical_architecture.md`
**Output**: **C4 Diagrams** and **ADRs** (Architectural Decision Records).
**Roles**: `architect`, `researcher`

### 3. Scoping ("The Plan")
**Trigger**: "Plan the work."
**Protocol**: `03_task_scoping.md`
**Output**: An `implementation_plan.md` broken into **Atomic Steps** with **Verification Scripts**.
**Roles**: `backend`, `frontend`, `database`

### 4. Quality Gate ("The Shield")
**Trigger**: "Test this."
**Protocol**: `05_quality_assurance.md`
**Output**: **Destructive Testing Report**, **STRIDE Security Audit**, **Lighthouse Performance Score**.
**Roles**: `qa`, `security`, `performance`

---

## ⚡ Quick Command Cheatsheet

### 🟢 Start
*   **Init System**: `Resonance Init`
*   **Start Project**: *"I want to build [idea]. Draft a PRD."*

### 🟡 Plan & Build
*   **Draft Specs**: *"Start initiation protocol"* (Generates PRD)
*   **Design System**: *"Run architecture protocol"* (Generates C4/ADR)
*   **Scope Tasks**: *"Plan the work"* (Generates task list)
*   **Review Code**: *"Review this PR"* (Runs Google-Standard Review)

### 🔵 Roles (Switch Mode)
*   `Role Switch product` (Working Backwards)
*   `Role Switch architect` (System Design)
*   `Role Switch devops` (GitOps/SRE)
*   `Role Switch growth` (Viral Loops)
*   `Role Switch debugger` (Scientific RCA)

### 🟣 Utils
*   **Check Health**: *"Run system check"* (Scores your codebase 0-100)
*   **Update System**: *"Update Resonance"* (Smart Update)
*   **Safe Commit**: `.resonance/scripts/safe-commit.sh "msg" file`

---

## Architecture

```text
├── AGENTS.md                   # The Kernel (v1.7)
├── resonance.sh                # Self-healing script
├── docs/                       # UNIFIED MEMORY
│   ├── specs/                  # PRDs & User Stories
│   ├── architecture/           # C4 Diagrams & ADRs
│   └── reports/                # Health Checks & QA Reports
└── .resonance/
    ├── 00_soul.md              # Vision & Principles
    ├── 01_state.md             # Macro-State Context
    ├── 02_memory.md            # Immutable Logs
    ├── workflows/              # The Pipeline (01-07)
    └── roles/                  # 17 Elite Specialists
```

---

## License

MIT © [divisionAI.co](https://divisionAI.co)

**Built with ❤️ for builders who ship.**