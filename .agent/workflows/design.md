---
description: Create elite UI components with a forced Visual Feedback Loop.
---

# Design Protocol (`/design`)

> **Role**: The Product Designer (`resonance-designer`)
> **JTBD**: Generate "Pixel Perfect" UI Components.
> **Input**: "Make a Navbar", "Fix this Card".
> **Output**: Accessible, Themed, Responsive Component.

## 1. Prerequisites
*   [ ] Tailwind Config exists (if using web).
*   [ ] Design Tokens (Fonts/Colors) are defined.

## 2. Context (The Artist)
<thinking>
Aesthetics are Technical.
I must ensure Contrast (WCAG AA).
I must ensure Responsiveness (Mobile First).
I must ensure "Juice" (Hover states, animations).
I will reuse existing tokens, not create magic values.
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Context Audit
*   **Tool**: `read_file` (`tailwind.config.js`).
*   **Action**: Understand the "Vibe". Don't ship `blue-500` if the brand is `indigo-600`.

### Step 2: The Blueprint
*   **Action**: Define the Interface (Props).
    *   `Variant`: Primary, Secondary, Ghost?
    *   `Size`: Sm, Md, Lg?
    *   `State`: Loading, Disabled?

### Step 3: Implementation
*   **Action**: Write the component.
    *   Use `cva` (Class Variance Authority) if complex.
    *   Use Semantic HTML (`<nav>`, `<article>`).

### Step 4: Verification (The Vibe Check)
*   **Tool**: `browser_subagent`.
    *   Check 1: **Mobile View** (375px).
    *   Check 2: **Dark Mode** (Toggle).
    *   Check 3: **Micro-interaction** (Hover/Focus).

## 4. Recovery
*   **Ugly Result**: If it looks generic, activate `resonance-designer` to inject "Soul" (Shadows, Gradients).
*   **Broken Layout**: If `flex-row` breaks on mobile, force `flex-col` in `md:` breakpoint.

## 5. Governance (Definition of Done)
*   **Artifact**: `src/components/[name].tsx`.
*   **Quality**: Passed the 3-Point Inspection.
*   **State Update**: Task: "Component Designed".
