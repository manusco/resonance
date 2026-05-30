# Resonance

> A builder's AI stack. Operator-grade skills for every business domain, shared project memory, and structured protocols that make your AI consistent by default.

<div align="center">
    <a href="https://github.com/manusco/resonance"><img src="https://img.shields.io/badge/Resonance-v2.2.0-7025eb?style=for-the-badge&logo=github" alt="Resonance" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-black?style=for-the-badge" alt="License" /></a>
    <a href="AGENTS.md"><img src="https://img.shields.io/badge/Operators_Manual-v2.2.0-00f2ea?style=for-the-badge" alt="Operators Manual" /></a>
</div>

---

## What it is

Resonance is a collection of files you drop into any project. It gives your AI agent:

- **A skill library** — 42 domain-tested skills across strategy, engineering, design, marketing, sales, ops, and research. Each skill is a structured protocol with prerequisites, a step-by-step algorithm, a Recovery path, and a Definition of Done.
- **A project memory** — a `.resonance/` folder that holds your project's soul, state, and decisions. The AI reads this before every task and writes to it after. It never forgets what you've told it.
- **Slash commands** — `/plan`, `/build`, `/audit`, `/ship`, and 14 others. Each one triggers a specific skill. They are not prompts — they are procedures.

You get consistent, high-quality output because the agent follows the same protocol every time, not because you remembered to ask nicely.

---

## How it's structured

Three things install into your project root.

| Bucket | Location | What it is |
| :--- | :--- | :--- |
| **Agent Identity** | `AGENTS.md` | Your IDE reads this on every session. Loads the agent roster, behavioral locks, and directives. |
| **Skill Library** | `.agents/skills/` | 42 skills organized by domain. The agent's protocol library. Safe to overwrite on upgrade. |
| **Project Memory** | `.resonance/` | Your project's soul, state, and decisions. You own this. Never overwrite on upgrade. |

```
your-project/
├── AGENTS.md                  ← loaded by your IDE every session
├── .agents/
│   └── skills/
│       ├── strategy/          ← plan, architect, venture, growth, researcher
│       ├── engineering/       ← backend, frontend, debugger, build, devops, ...
│       ├── design/            ← designer, studio
│       ├── marketing/         ← seo, conversion, copywriter
│       ├── sales/             ← pipeline, cold-call, call-intelligence
│       ├── ops/               ← audit, qa, security, reviewer, refactor, ship, ...
│       └── research/          ← market-research
├── .resonance/
│   ├── 00_soul.md             ← your project's vision and laws
│   ├── 01_state.md            ← active task and last decisions
│   ├── 02_memory.md           ← architectural decision log
│   └── learnings.jsonl        ← project-specific lessons
└── src/  package.json  ...
```

> **Upgrade rule**: Overwrite `AGENTS.md` and `.agents/` freely. Never touch `.resonance/` — that is your project's permanent memory.

---

## Installation

There are two scenarios. Pick the one that matches your situation.

---

### Scenario A: You are pointing Claude Code (or similar) at this repo directly

If you cloned Resonance and your AI tool is running inside this repo, you are already set up. `AGENTS.md` is at the root and your tool loads it automatically on every session.

**What to do next:**

1. Open a chat in your AI tool.
2. Type `/init`.
3. The agent will ask what you are building. Tell it. It scaffolds `.resonance/` for your project inside this folder.

That is it. The skill library in `.agents/skills/` is already compiled and ready.

---

### Scenario B: You want to use Resonance inside your own project

Copy two things into your project root, then run `/init`.

**macOS / Linux:**
```bash
# Clone to a temp location (not into your project)
git clone https://github.com/manusco/resonance ~/resonance-tmp

# From your project root
cp ~/resonance-tmp/AGENTS.md ./AGENTS.md
cp -r ~/resonance-tmp/.agents ./.agents

# Clean up
rm -rf ~/resonance-tmp
```

**Windows (PowerShell):**
```powershell
# Clone to a temp location
git clone https://github.com/manusco/resonance $env:TEMP\resonance-tmp

# From your project root
Copy-Item "$env:TEMP\resonance-tmp\AGENTS.md" -Destination ".\AGENTS.md"
Copy-Item "$env:TEMP\resonance-tmp\.agents" -Destination ".\.agents" -Recurse

# Clean up
Remove-Item "$env:TEMP\resonance-tmp" -Recurse -Force
```

**Then open your AI tool and type `/init`.**

The agent will ask: *"What are you building?"* Tell it. It writes your project's vision to `.resonance/00_soul.md` and sets up the rest of the memory structure.

---

### Upgrading

**Why delete, not overwrite.** Resonance reorganises its skill library between versions. A plain copy (`cp -r`) leaves ghost files from the previous version alongside the new ones. Your AI reads everything in `.agents/`, so stale old skills sit there contradicting the new ones. The correct upgrade is: delete `.agents/` first, then copy the new version in.

**Why no archive.** `.agents/` is entirely Resonance-owned. You do not write to it. If something breaks, the right restore is to clone the repo again — not to restore a stale backup from the last version. Keeping an archive creates clutter without benefit.

**The one thing you never touch: `.resonance/`.** This is your project's brain. The upgrade does not go near it. Your soul, state, memory, and learnings are untouched.

---

**macOS / Linux:**
```bash
# 1. Clone the latest version
git clone https://github.com/manusco/resonance ~/resonance-tmp

# 2. Delete the old skill library (this is intentional — do not skip)
rm -rf .agents/

# 3. Copy in the new skill library and identity file
cp -r ~/resonance-tmp/.agents ./.agents
cp ~/resonance-tmp/AGENTS.md ./AGENTS.md
cp ~/resonance-tmp/resonance.sh ./resonance.sh

# 4. Clean up
rm -rf ~/resonance-tmp
```

**Windows (PowerShell):**
```powershell
# 1. Clone the latest version
git clone https://github.com/manusco/resonance $env:TEMP\resonance-tmp

# 2. Delete the old skill library (this is intentional — do not skip)
Remove-Item ".agents" -Recurse -Force

# 3. Copy in the new skill library and identity file
Copy-Item "$env:TEMP\resonance-tmp\.agents" -Destination ".\.agents" -Recurse
Copy-Item "$env:TEMP\resonance-tmp\AGENTS.md" -Destination ".\AGENTS.md" -Force
Copy-Item "$env:TEMP\resonance-tmp\resonance.ps1" -Destination ".\resonance.ps1" -Force

# 4. Clean up
Remove-Item "$env:TEMP\resonance-tmp" -Recurse -Force
```

**5. Verify the upgrade:**
```
/system-health
```

The health check confirms the correct number of skills loaded and flags any state drift between your project memory and git history.

> `.resonance/` is never part of this process. It stays exactly as you left it.

---

## The skill domains

Resonance ships with skills across 7 domains. Each skill is a self-contained protocol backed by reference documents.

### Strategy
Planning, architecture, and business modeling.
- **`/plan`** — Deep research, ambiguity checks, 4-pass atomic implementation plan. User approves each pass.
- **`/venture-model`** — Business model, offer stack, and revenue math before a single line of code.
- **architect** — System design, C4 models, API contracts, database policies.
- **researcher** — Technical investigations, trade-off analysis, Buy vs Build recommendations.

### Engineering
Building, debugging, and shipping code.
- **`/build`** — Executes the implementation plan via TDD: Test → Code → Verify. Orchestrates backend and frontend specialists.
- **`/debug`** — Root Cause Analysis. Reproduction script required. Hypothesis before fix. Scientific method, not guesswork.
- **backend, frontend, mobile, database, devops, performance, automation, game-dev** — Domain specialists, each with a reference library.

### Design
Visual systems and UI components.
- **`/design`** — Generates components with Entrance, Hover, and Click states. Visual system specs: HSL palette, typographic scale, spacing scale.
- **studio** — Asset generation and style consistency.

### Marketing
Search visibility, conversion, and copy.
- **`/seo`** — Full SEO and GEO audit. Structured data, canonical, schema, AI citation optimization (22 protocols).
- **`/friction`** — Friction Collider: simulates the "Anti-Persona" to find and remove drag from funnels.
- **copywriter** — Anti-slop filter, stylometric voice extraction, neuro-marketing, email sequences.

### Sales
Pipeline management and outreach.
- **pipeline** — B2B sales qualification (BANT, MEDDIC, MEDDPICC, SPICED), sales methodologies, objection playbooks.
- **cold-call** — Opening frameworks, objection handling, follow-up cadences.
- **call-intelligence** — Call analysis, talk-to-listen ratios, next-step extraction.

### Ops
Quality, security, delivery, and governance.
- **`/audit`** — The Swarm: orchestrates Security + Reviewer + QA + Architect. P0–P3 classified findings. APPROVE or REJECT.
- **`/test`** → qa — 8-Path Matrix: Happy, Sad, Unauthorized, Malformed, Missing Dependency, Legacy, UI, Redirect.
- **`/review-pr`** → reviewer — PR gatekeeper. Blocking Registry check. Risk summary.
- **`/refactor`** → refactor — Mikado Method, Safe Sequence (Lock → Extract → Centralize → Split → Cleanup). Zero behavioral change.
- **`/ship`** — Pre-flight, changelog, semantic versioning, logical commits, tag, deploy.
- **`/system-health`** — Health Score (0–100). Flags: `AUTH_INCONSISTENT`, `ENV_FRAGILE`, `TEST_SHALLOW`, `DRIFT_DETECTED`.
- **`/capture`** → librarian — Documents solved problems in the correct Diataxis quadrant.
- **`/retro`** — Git-driven retrospective: Shipping Streak, Focus Score, Complexity Delta.
- **`/init`** → core — Bootstraps `.resonance/` structure. Writes soul, state, docs scaffold.

### Research
Market and competitive intelligence.
- **market-research** — Market sizing, competitive landscape, ICP analysis, positioning.

---

## The project memory

The `.resonance/` folder is the engine that makes everything persistent.

| File | What it holds |
| :--- | :--- |
| `00_soul.md` | Your vision, mission, and the laws that govern the project. Written once during `/init`, referenced forever. |
| `01_state.md` | The active task, the last decision, the current blocker. The AI updates this after every session. |
| `02_memory.md` | Architectural decision log. Why we chose Postgres over SQLite. Why we didn't use Redux. Never solve the same problem twice. |
| `learnings.jsonl` | Project-specific lessons learned from bugs, edge cases, and hard-won discoveries. |

---

## What's new in v2.2.0

**Unified skill library.** Skills are now organized by domain (`strategy/`, `engineering/`, `design/`, `marketing/`, `sales/`, `ops/`, `research/`) with a shared Forge compiler. Each skill has a template, evals, and compiled output.

**Slash commands are skills.** Every slash command (`/plan`, `/build`, `/debug`, `/audit`, `/ship`, etc.) is now a first-class skill in the library with a Definition of Done, prerequisites, a step-by-step algorithm, and a Recovery path.

**Skill Author.** A meta-skill for building new skills. Includes the Forge compiler, eval protocol, and validator. Use it when you need to extend the library for your specific domain.

---

## Why it works

The agent gets the same instruction every time. Not a rephrased version of it. Not an interpretation. The exact same protocol, with the exact same checklist.

When it runs `/audit`, it doesn't decide what to check. It follows the 9-step Swarm protocol: security scan, quality scan, authorization model audit, data truth audit, environment check, verification gap analysis, product integrity check, performance scan, synthesis. In that order.

When it runs `/debug`, it doesn't guess. It writes a reproduction script that fails 100% of the time before it writes a single line of fix.

That's the difference.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

Maintained by [www.divisionAI.co](https://www.divisionAI.co)