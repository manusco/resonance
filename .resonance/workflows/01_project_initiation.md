# Agent Protocol: Project Initiation

**Trigger:** User says "I have an idea", "Start a new project", "New feature", or "Draft a PRD".

## 1. Goal
Convert a vague user intent into a rigorous **Product Requirement Document (PRD)** stored in `docs/specs/`.
We use the "Working Backwards" method (Amazon) combined with First-Principles thinking.

## 2. The Process: Draft First, Ask Second

**CRITICAL:** Do not interrogate the user with a list of 10 questions.
**INSTEAD:** Take their initial input (even if it's just "I want a dark mode") and **IMMEDIATELY DRAFT** the entire Press Release and PRD sections using your best judgment.

### Step 1: Ingest & Hybrid Draft
*   Read the user's input.
*   **Confident?** Draft the sections you can reasonably infer (Headline, Solution path).
*   **Unsure?** Leave placeholders or ask specific questions for *critical* missing info.
*   **The Goal:** Show a 80% complete draft. It is easier for a user to correct a wrong guess than to answer a blank page.

### Step 2: The "Press Release" (Amazon Style)
Draft this **FOR** the user, but highlight your assumptions.
*   **Headline:** [Proposal]
*   **The Problem:** [Inferred]
*   **The Solution:** [Inferred]
*   **MISSING:** "I wasn't sure about [X], so I guessed [Y]. Is that right?"

### Step 3: First Principles & Scope
Only ask clarifying questions if you are truly stuck.
*   **Strip to Reality:** Check constraints.
*   **Non-Goals:** Propose a list of things NOT to do (e.g., "I've excluded mobile support for V1, correct?").

## 3. Artifact Generation
Once the user affirms the direction, generate `docs/specs/PRD-[name].md`.

**Template:**
```markdown
# PRD: [Feature Name]

## 1. The Press Release
> [Headline]
> [Summary]

## 2. Problem Statement
[First-principles analysis of the core user pain]

## 3. Solution (The "Happy Path")
[Step-by-step user journey]

## 4. Non-Goals (Out of Scope)
- [ ] [Feature X]
- [ ] [Feature Y]

## 5. Success Metrics
- [Metric 1]
- [Metric 2]
```

## 4. Next Step
Ask the user: "PRD drafted. Should we move to **Architecture Design** or straight to **Scoping**?"
