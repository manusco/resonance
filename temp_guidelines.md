# Resonance Framework: Internal Development Guidelines

> **INTERNAL DOCUMENT DO NOT PUBLISH**
> This document serves as the "North Star" for all contributions and improvements to the Resonance framework.

## What is Resonance?

Resonance is an **Operating System for AI Agents** designed specifically for the Google Antigravity environment. It transforms a standard chat-based agent into a persistent, state-aware engineer by giving it:

1.  **Persistent Memory**: A file-based file system (`.resonance/`) that acts as a hard drive for long-term context, preventing amnesia between sessions.
2.  **Elite Specialist Roles**: A library of rigorously defined personas (Product Manager, Architect, Reviewer, etc.) that embody "world-class" methodologies (e.g., Amazon's Working Backwards, C4 Models).
3.  **Structured Workflows**: A set of active protocols (`workflows/`) that guide the agent through complex engineering phases (Initiation -> Architecture -> Scoping -> Implementation).

**Purpose**: To enable solo founders and engineers to ship high-quality, production-ready software faster by giving their AI agent a "brain" and "muscle memory."

---

## Core Guidelines

Every change to the Resonance framework must adhere to these principles:

### 1. User First
*   We exist to serve the builder. Every feature must solve a real problem for the user, not just be "cool tech."
*   Respect the user's time and attention. Be concise, be helpful, be accurate.

### 2. Easy to Understand (The "30-Second Rule")
*   New users should be able to grok the value and start using Resonance in under 30 seconds.
*   Avoid jargon where simple language suffices.
*   The `AGENTS.md` file should be self-explanatory.

### 3. Useful for Experienced Users (High Ceiling)
*   While easy to start, the system must offer depth for power users.
*   Advanced roles, custom workflows, and deep integration with Antigravity features (terminal, browser) provide this depth.
*   Don't hide power features; make them discoverable.

### 4. High Signal, Low Noise
*   Every file, every log, every output line must carry weight.
*   Avoid "AI slop" (verbose, empty pleasantries).
*   If a file doesn't need to exist, delete it. If a log message doesn't inform a decision, remove it.

### 5. Not Too Complex, Not Overly Simplified
*   **Goldilocks Zone**: We are building a *framework*, not a heavy platform.
*   Avoid over-engineering (e.g., complex databases for simple state).
*   Avoid over-simplifying (e.g., treating "coding" as a single task without architecture or QA).
*   Use the filesystem as the database. It's simple, portable, and transparent.

### 6. Complement, Don't Compete with Antigravity
*   **Do NOT** rebuild features Antigravity already has (e.g., don't build a poor man's terminal wrapper if we have direct terminal access).
*   **Leverage** Antigravity's strengths: Use the Artifacts UI for micro-tasks, use the Terminal for execution, use the Browser for verification.
*   Resonance is the *software* running on the *hardware* of Antigravity.

### 7. The State Machine Mindset
*   The agent is not a chatbot; it is a **State Machine**.
*   It transitions between states (Planning -> Coding -> Verifying).
*   It reads state from `01_state.md` and writes state to `cards`.
*   Every action should move the project from one valid state to another.

### 8. Files > Context Window
*   The context window is ephemeral and expensive. The filesystem is permanent and cheap.
*   **Write to disk immediately.** If it's not in a file (`00_soul.md`, `02_memory.md`, `docs/`), it didn't happen.
*   Design for "Session Amnesia": Assume the agent will be rebooted every 10 minutes. The filesystem must maintain continuity.

### 9. Elite Defaults
*   "Good enough" is not enough. The roles (`.resonance/roles/`) must embody **elite** standards.
*   A "Product Manager" role shouldn't just "chat about features"; it should force a *Press Release* and *FAQ* (Amazon style).
*   A "Reviewer" role shouldn't just say "looks good"; it should check for security, performance, and maintainability.
*   We encode the wisdom of senior engineers into prompt files.

### 10. Self-Healing Systems
*   Things will break. The user will delete files. The agent will hallucinate.
*   The framework must be resilient.
*   `resonance.sh` (or its equivalent) must be able to restore the system to a working state from any level of entropy.
*   Error messages should be actionable fixes, not just stack traces.

### 11. "If You Can't Prove It, You Didn't Build It" (The Ralph Protocol)
*   Blind coding is forbidden.
*   Every implementation must be paired with a verification step (test script, browser check, curl command).
*   The framework should encourage/enforce this verify-first loop.

### 12. Radical Transparency
*   The system should never be a "black box."
*   The user should always know *what* the agent is doing and *why*.
*   Use `01_state.md` and explicit status updates to keep the user in the loop without overwhelming them.
