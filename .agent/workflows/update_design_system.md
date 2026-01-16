---
description: Convert a PRD into a Technical Design with C4 diagrams and ADRs.
---

# Workflow: Update Design System ("The Refiner")

**Trigger**: "Update the UI", "Change the theme", "Add a component".
**Context**: You are modifying the visual language of the application.

## 1. Audit (The Archeologist)
*Activate Skill*: `resonance-designer`

- [ ] **Check Existing**: Do we already have this component? Don't duplicate.
- [ ] **Check Tokens**: Are we introducing a new color/spacing? Try to use existing tokens `tailwinc.config.js`.

## 2. Design (The Artist)
*Activate Skill*: `resonance-designer`

- [ ] **Draft**: Create the markup structure (HTML only).
- [ ] **Style**: Apply atomic classes.
- [ ] **Comply**: Check against Accessibility constraints (Contrast, Focus states).

## 3. Implementation (The Builder)
*Activate Skill*: `resonance-frontend`

- [ ] **Component**: Extract to `src/components/ui/[name].tsx`.
- [ ] **Variant**: Use `cva` (Class Variance Authority) or equivalent for variants.
- [ ] **Story**: Create a usage example (Storybook or specific route).

## 4. Verification (The Vibe Check)
*Activate Skill*: `resonance-designer`

- [ ] **Mobile Check**: Shrink browser to 375px. Does it break?
- [ ] **Dark Mode**: Toggle theme. Does it look good?
- [ ] **Vibe Check**: Does it feel "Premium"? Adjust shadows/radius.
