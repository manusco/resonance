# Builder Guidelines

This document explains how to build and maintain Resonance.
It is for **us** (the builders). It is not for the user.

## 1. How We Write

We respect the reader's time.

* **Prune**. If a word doesn't add meaning, kill it. No "very", "extremely", or "really".
* **Hook**. Start in the middle. Make them curious.
* **One Thought**. One idea per sentence. If you see a comma, ask if it should be a period.
* **Active Voice**. Subject-Verb-Object. "The Agent writes the code," not "The code is written by the Agent."
* **Be Human**. Admit what you don't know. Speak as a peer, not a god.

## 2. Core Philosophy

### Externalized Cognition

**If it is not in a file, it does not exist.**
Agents die. Chat history fades.
The File System is the only persistent Mind.

* **Soul** (`00_soul.md`): Conscience.
* **State** (`01_state.md`): Short-term memory.
* **Memory** (`02_memory.md`): Long-term logs.
* **Tools** (`03_tools.md`): Capabilities & Boundaries.
* **Systems** (`04_systems.md`): Architecture Map.

### The Ratchet & The Self-Annealing Loop

**Never solve the same problem twice.**
If you fix a bug, write a test. If you learn a quirk, write a doc.
When things break, or when the **user corrects your logic**, execute the **Self-Annealing Loop**:

1. Read the error, stack trace, or user correction.
2. Fix the *deterministic script* or logic (not just the prompt) and test it.
3. Update the *Directive/Workflow* or your `lessons.md` with what you learned (e.g., API limits, user preferences, edge cases).
4. Ruthlessly iterate on these lessons until the mistake rate drops to zero.
Lock progress in place. The system continuously strengthens itself.

### The 3-Layer Architecture

We separate concerns to maximize reliability. LLMs are probabilistic, but business logic requires consistency.

1. **Layer 1: Directive (Intent)**
   * **What it is**: SOPs, Workflows (`.agents/workflows/`), and Skills (`.agents/skills/`).
   * **Purpose**: Natural language instructions defining goals, inputs, outputs, and edge cases.
2. **Layer 2: Orchestration (Decision Making)**
   * **What it is**: You. The LLM Agents (The Kernel).
   * **Purpose**: Read directives, call tools in the correct order, handle errors, and route intent to execution. You are the glue.
3. **Layer 3: Execution (Deterministic Work)**
   * **What it is**: Scripts (`.agents/skills/*/scripts/`), Tools, MCP Servers.
   * **Purpose**: Reliable, testable, fast execution of API calls, DOM manipulation, and file I/O.

> 🔴 **Rule**: Push complexity into Layer 3. 90% accuracy per step = 59% success over 5 steps. Deterministic code prevents compounding LLM errors.

### Evolution

**Improve. Don't replace.**
Resonance is mature. Users rely on it.
Do not delete functionality unless it is broken.
If you see a new way, integrate it. Do not overwrite the old way without understanding why it was there.

## 3. Building Workflows

A Workflow is a `markdown` file in `.agents/workflows/`.
It must follow this schema:

1. **Identity**: Role + Job to be Done.
2. **Prerequisites**: Fail fast if input is wrong.
3. **Context**: `<thinking>` block. Align strategy.
4. **Algorithm**: Step-by-step logic.
5. **Recovery**: What to do if it fails.
6. **Governance**: Verify and update State.

**The Interview Rule**:
Never dump templates on a user.
Ask them questions.
Use their answers to generate artifacts (`soul.md`, `PRDs`, `diagrams`).

## 4. Building Skills

### What Resonance Is (Hard Rule)

Resonance is a **Company OS** — a complete set of skills, frameworks, and mental models covering every essential function of a business. It is built for operators: founders, CEOs, COOs, CTOs, developers, and the teams around them. It is designed for small and medium-sized businesses that want to operate like the top 1%.

**What a Resonance Skill IS:**
- Mental models and thinking frameworks (e.g., SPIN Selling, Jobs-to-be-Done, OKRs)
- Best practices and decision-making protocols (e.g., how to run a hiring process)
- Workflows and operational sequences (e.g., how to structure a sprint, run a board meeting)
- Domain expertise distilled to its essence (e.g., how a CFO thinks about cash flow)

**What a Resonance Skill is NOT:**
- A guide to using a specific tool (e.g., "How to configure Slack", "How to use HubSpot"). Tool-specific instructions belong in `references/` as cheat sheets — never in a `SKILL.md`.
- A narrow, industry-specific niche play. Skills must work for most businesses, not just one vertical.
- Anything below the 1% standard. If it reads like a blog post or a junior's playbook, reject it.

> 🔴 **Rule**: If you're writing steps that involve clicking a button in a specific piece of software, stop. That's a reference doc. The skill is the strategy behind *why* you'd take that action and *when*.



## 5. Engineering Standards

* **Docs over Chat**. Complex logic belongs in `docs/`.
* **No Black Boxes**. Explain *why*.
* **Aesthetics**. If we generate UI, it must be beautiful. No generic defaults.
* **Verification**. "No Commit Without Evidence". Verify every change.
