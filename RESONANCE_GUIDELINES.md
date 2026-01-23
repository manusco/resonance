# Builder Guidelines

This document explains how to build and maintain Resonance.
It is for **us** (the builders). It is not for the user.

## 1. How We Write

We respect the reader's time.

*   **Prune**. If a word doesn't add meaning, kill it. No "very", "extremely", or "really".
*   **Hook**. Start in the middle. Make them curious.
*   **One Thought**. One idea per sentence. If you see a comma, ask if it should be a period.
*   **Active Voice**. Subject-Verb-Object. "The Agent writes the code," not "The code is written by the Agent."
*   **Be Human**. Admit what you don't know. Speak as a peer, not a god.

## 2. Core Philosophy

### Externalized Cognition
**If it is not in a file, it does not exist.**
Agents die. Chat history fades.
The File System is the only persistent Mind.
*   **Soul** (`00_soul.md`): Conscience.
*   **State** (`01_state.md`): Short-term memory.
*   **Memory** (`02_memory.md`): Long-term logs.
*   **Tools** (`03_tools.md`): Capabilities & Boundaries.
*   **Systems** (`04_systems.md`): Architecture Map.

### The Ratchet
**Never solve the same problem twice.**
If you fix a bug, write a test.
If you learn a quirk, write a doc.
Lock progress in place.

### Evolution
**Improve. Don't replace.**
Resonance is mature. Users rely on it.
Do not delete functionality unless it is broken.
If you see a new way, integrate it. Do not overwrite the old way without understanding why it was there.

## 3. Building Workflows

A Workflow is a `markdown` file in `.agent/workflows/`.
It must follow this schema:

1.  **Identity**: Role + Job to be Done.
2.  **Prerequisites**: Fail fast if input is wrong.
3.  **Context**: `<thinking>` block. Align strategy.
4.  **Algorithm**: Step-by-step logic.
5.  **Recovery**: What to do if it fails.
6.  **Governance**: Verify and update State.

**The Interview Rule**:
Never dump templates on a user.
Ask them questions.
Use their answers to generate artifacts (`soul.md`, `PRDs`, `diagrams`).

## 4. Building Skills

When adding external skills (from other frameworks):

1.  **The Expert Test**. Would a top 1% expert use this approach? If no, reject it.
2.  **Context First**. Understand how Resonance works.
3.  **Bridge**. Don't just copy. Adapt the skill to use Resonance's Memory and State.

## 5. Engineering Standards

*   **Docs over Chat**. Complex logic belongs in `docs/`.
*   **No Black Boxes**. Explain *why*.
*   **Aesthetics**. If we generate UI, it must be beautiful. No generic defaults.
*   **Verification**. "No Commit Without Evidence". Verify every change.
