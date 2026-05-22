# Resonance: The Agentic Coding Operating System
> *Turn your LLM into a structured, memory-backed Headless Engineering Team.*

<div align="center">
    <a href="https://github.com/manusco/resonance"><img src="https://img.shields.io/badge/Resonance-v2.1.1-7025eb?style=for-the-badge&logo=github" alt="Resonance AI Framework" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-black?style=for-the-badge" alt="License" /></a>
    <a href="AGENTS.md"><img src="https://img.shields.io/badge/Operators_Manual-v2.1.1-00f2ea?style=for-the-badge" alt="Operators Manual" /></a>
</div>

---

## 👋 Hi. We built this to stop the "Groundhog Day" of prompting.

You know the feeling. You start a new chat. You paste your tech stack. You remind the AI to use TypeScript. You remind it to check for security vulnerabilities. You remind it to write tests.
**And you do it again. And again. And again.**

It's exhausting. And frankly, it's a waste of your time.

**Resonance is the cure for repetitive prompting.**

It is a comprehensive **Agentic Operating System** that comes pre-loaded with battle-tested engineering protocols.
*   **Security?** Built-in.
*   **Testing?** Standardized.
*   **Deployment?** One command.

We took the best practices from elite engineering teams and baked them directly into the file system. So you don't have to prompt for quality. You just get it.

---

## 🗂️ How Resonance Is Structured (Read This First)

Resonance installs **three things** into your project root. Understanding this prevents every installation mistake.

| Bucket | Location | What It Is |
| :--- | :--- | :--- |
| **Agent Identity** | `AGENTS.md` at root | Your IDE reads this automatically on every session. Loads the 26-agent roster, the 4 Behavioral Locks, and the Prime Directives into every chat. |
| **Agent Capabilities** | `.agents/` at root | Skills and Workflows. The protocol library — what agents *know how to do*. Owned by Resonance. Safe to overwrite on upgrade. |
| **Project Brain** | `.resonance/` at root | Soul, State, Memory. Project-specific. What agents *remember about your project*. Owned by you. Never overwrite. |

After installation, your project looks like this:

```
your-project/
├── AGENTS.md              ← IDE reads this automatically on every session
├── .agents/               ← agent capabilities (from this repo, updated on upgrades)
│   ├── skills/
│   └── workflows/
├── .resonance/            ← your project brain (YOU own this, never overwrite on upgrade)
│   ├── 00_soul.md
│   ├── 01_state.md
│   ├── 02_memory.md
│   └── ...
└── src/  package.json  etc.
```

> **The upgrade rule in one sentence**: Update `.agents/` and `AGENTS.md` freely. Never touch `.resonance/` — that is your project's permanent memory.

---

## 🚀 Installation & Upgrading

### Option A: Fresh Installation (New Project)

**1. Clone the repo to a temporary location**

Do **not** clone directly into your project. The repo *contains* the three buckets — it is not one of them.

```bash
git clone https://github.com/manusco/resonance /tmp/resonance
```

**2. Copy the three buckets into your project root**

```bash
# From your project root:
cp /tmp/resonance/AGENTS.md ./AGENTS.md
cp -r /tmp/resonance/.agents ./.agents
```

> `.resonance/` is **not** copied from the repo. It gets scaffolded for your project in the next step.

**3. Wake up the system**

In your IDE (Cursor, Windsurf, Cline, etc.), type:

```
/init
```

Resonance will ask: *"What are we building?"*
Tell it your vision. It writes it down in `.resonance/00_soul.md`. From that moment on, it never forgets.

---

### Option B: Upgrading an Existing Project

When upgrading, you update the agent capabilities while **preserving your project brain**.

**What to overwrite (safe):**

| File / Folder | Action |
| :--- | :--- |
| `AGENTS.md` | ✅ Overwrite |
| `.agents/` | ✅ Overwrite entirely |
| `resonance.sh` / `resonance.ps1` | ✅ Overwrite |

**What to never touch (yours):**

| File | Why |
| :--- | :--- |
| `.resonance/00_soul.md` | Your project's vision and identity |
| `.resonance/01_state.md` | Active task state |
| `.resonance/02_memory.md` | Architectural decision log |
| `.resonance/04_systems.md` | Logic flows, schemas, API contracts |
| `.resonance/learnings.jsonl` | Hard-won project wisdom |

**Steps:**

```bash
# Clone latest to a temp location
git clone https://github.com/manusco/resonance /tmp/resonance

# From your project root — overwrite capabilities, leave brain alone
cp /tmp/resonance/AGENTS.md ./AGENTS.md
cp -r /tmp/resonance/.agents ./.agents
```

> **v2.1.1 migration note**: We moved from `.agent/` (singular) to `.agents/` (plural). Delete your old `.agent/` folder after copying the new `.agents/`.

**3. Verify the upgrade**

```
/system-health
```

---

## ⚡ The Workflow Library (Token-Efficient Intelligence)
Resonance workflows are not just "prompts". They are structured algorithms designed to save tokens and time. 
We stripped away the fluff. Each workflow is a **templatized, rigorous protocol** that gets straight to the point.

### 🟡 Strategy & Inception
*   **`/venture-model`**: **Business Logic**. Validates the business model, offer, and revenue math before you build.
*   **`/plan`**: **The Architect**. Reads 80% of the time. Writes 20%. Generates a detailed `implementation_plan.md` to prevent "hallucinated scope".
*   **`/update-roadmap`**: **State Sync**. Keeps your `01_state.md` aligned with reality.

### 🟢 Execution & Engineering
*   **`/build`**: **The Builder**. Runs the TDD Loop (Red -> Green -> Refactor).
*   **`/debug`**: **The Scientist**. Forces Root Cause Analysis (RCA) with reproduction scripts. No guessing allowed.
*   **`/refactor`**: **The Essentialist**. Cleans up technical debt without changing behavior.
*   **`/design`**: **The Glasssmith**. Generates premium, "Touch Physics" UI components.

### 🔵 Quality & Verification
*   **`/audit`**: **The Swarm**. Runs a 50-point Security (OWASP), Performance, and Lint check.
*   **`/test`**: **The Pyramid**. Generates Unit, Integration, and E2E tests.
*   **`/friction`**: **The Collider**. Simulates a user journey to find and remove "Drag" (latency, confusion).
*   **`/seo`**: **The Growth Engine**. Optimizes for Search and Answer Engines (GEO).

### 🟣 Operations & Delivery
*   **`/ship`**: **The Ritual**. Updates Changelog, bumps version, checks health, and deploys.
*   **`/capture`**: **The Librarian**. Documents solved problems so you never solve them twice.
*   **`/system-health`**: **Self-Repair**. Checks the integrity of the Resonance system itself.

> **Why this matters**: You don't pay for the AI to "think" about how to be a security auditor. We already taught it. You only pay for the work.

---

## 👩‍🚀 The Engineering Team (26 Specialists, 203 Protocols)
You wouldn't ask a backend engineer to design your logo. So why ask a generic chatbot to do everything?
Resonance comes with **26 Specialized Personas**, each backed by a deep library of reference protocols. These aren't thin wrappers around a system prompt — they're codified domain expertise with decision frameworks, checklists, and battle-tested playbooks.

**What "backed by protocols" actually means:**

| Domain | What's Inside | Reference Count |
| :--- | :--- | :--- |
| **Security** | OWASP audits, STRIDE threat modeling, JWT hardening, CSP headers | 14 protocols |
| **SEO & GEO** | Google ranking architecture (informed by the 2024 Systems Leak), AI citation optimization, programmatic SEO, schema markup | 22 protocols |
| **Frontend** | Touch Physics, micro-interaction patterns, design system generation, accessibility | 12 protocols |
| **Growth & Revenue** | AARRR metrics, viral loops, B2B sales pipeline (BANT/MEDDIC/MEDDPICC), CRM operations, launch strategy | 13 protocols |
| **Conversion** | Friction Collider simulation, behavioral psychology, onboarding activation, churn prevention | 13 protocols |
| **Quality** | E2E testing (Playwright), property-based fuzzing, destructive testing, test pyramid | 13 protocols |
| **Copywriting** | Anti-slop filter, stylometric voice extraction, neuro-marketing triggers, email sequences | 16 protocols |

Every protocol is a standalone reference document — not a prompt, but a playbook an agent reads before doing the work.

> **Why this matters**: When your AI runs a security audit, it doesn't "try its best" — it follows a 14-point protocol based on OWASP Top 10. When it writes SEO content, it cross-references the 2024 Google ranking signals leak. The difference between a generic chatbot and Resonance is the difference between asking someone and asking an expert with a reference library.

---

## 🧩 The Second Brain (`.resonance/`)
This is the engine that makes it all possible. A structured "Second Brain" that lives in your repo.

| The Cortex | File | Function |
| :--- | :--- | :--- |
| **The Soul** | `00_soul.md` | **The Constitution**. Your Vision, Mission, and User Persona. Even if you change LLMs, the Soul remains. "Who are we building for?" |
| **The State** | `01_state.md` | **The RAM**. What is the *active* task? What was the last decision? This prevents the "What was I doing?" loop. |
| **The Memory** | `02_memory.md` | **The Hard Drive**. A permanent audit log of architectural decisions (ADRs). We never solve the same problem twice. |
| **The Map** | `04_systems.md` | **The Blueprint**. Logic flows, database schemas, and API contracts. The LLM reads this *before* it writes a line of code. |

---

## 📋 What's New in v2.1.1

**Gold-Standard Marketing & Revenue Intelligence** — Resonance now ships with deep B2B sales and CRM reference protocols alongside upgraded SEO, Growth, and Conversion skills.

- **B2B Sales Pipeline**: 4 qualification frameworks (BANT → MEDDIC → MEDDPICC → SPICED) with selection guidance, 4 sales methodologies (Challenger, SPIN, Gap, Command of the Message), multi-threading strategy, mutual action plans, and a full objection playbook.
- **CRM Operations**: Revenue stack architecture, CRM selection by GTM motion, lifecycle/deal/CS automation workflows, data hygiene protocols, three-audience dashboards with attribution models, and a 6-level RevOps maturity model.
- **SEO & GEO**: Expanded to 22 protocols. New site architecture protocol, competitor page engineering, and AI citation optimization (GEO) now split into its own dedicated protocol.
- **Conversion**: New onboarding activation protocol (time-to-value, first-run patterns, habit loops) and churn prevention protocol (cancel flows, dunning sequences, dynamic save offers, win-back campaigns).
- **Growth**: Community-driven growth loop variant, directory distribution strategy, and content strategy protocol (Searchable vs Shareable framework).

---

## 💙 Why we built this
We believe that software engineering is a craft.
It shouldn't be a slot machine where you pull the lever (prompt) and hope for a jackpot (working code).

It should be:
1.  **Intentional**: You define the Soul.
2.  **Persistent**: The system remembers.
3.  **Standardized**: The protocols protect you.

Resonance is just a set of files in your folder. But it's also a collection of the best engineering practices, ready to work for you.
We are proud of what we've built. We hope it helps you build something amazing.

**Happy Building.**

---
Maintained by [www.divisionAI.co](https://www.divisionAI.co) 🚀