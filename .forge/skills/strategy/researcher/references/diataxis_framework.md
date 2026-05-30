# Diataxis Framework Protocol

> "Documentation is not one thing. It is four things."
> — Daniele Procida

## 1. The 4 Quadrants

### 1. Tutorials (Learning-Oriented)
*   **Goal**: "Take me by the hand."
*   **User**: Beginner.
*   **Structure**: Step-by-step practical lesson.
*   **Example**: "Build a Blog in 10 Minutes."
*   **In Resonance**: `walkthrough.md`.

### 2. How-To Guides (Problem-Oriented)
*   **Goal**: "Solve a specific problem."
*   **User**: Busy Developer.
*   **Structure**: A recipe. "How do I add a database?"
*   **Example**: "Setting up Postgres with Drizzle."
*   **In Resonance**: `references/*.md`.

### 3. Explanation (Understanding-Oriented)
*   **Goal**: "Understand the concept."
*   **User**: Architect.
*   **Structure**: Context, history, design decisions.
*   **Example**: "Why we chose Turso over Neon."
*   **In Resonance**: `ADR` or `implementation_plan.md` context.

### 4. Reference (Information-Oriented)
*   **Goal**: "Facts."
*   **User**: Expert.
*   **Structure**: Dry, technical, accurate.
*   **Example**: API Docs, Config Options.
*   **In Resonance**: `SKILL.md` properties list.

## 2. The Mandate

*   **Don't Mix Them**:
    *   Do not put "Philosophy" (Explanation) in a "Tutorial".
    *   Do not put "Step 1" (Tutorial) in a "Reference".

> 🔴 **Rule**: Before writing, declare the Type: "This is a [How-To Guide] for [Problem]."
