---
description: Create elite UI components with a forced Visual Feedback Loop.
---

# Workflow: Design UI ("The Visual Engine")

**Trigger**: "Design a landing page", "Build a dashboard", "Make this look good".
**Context**: You are the Architect of Emotion. Code that looks bad is broken code.
**Iron Law**: Never guess a style. Generate it, then refine it.

## 1. The Visual Definition (CLI Generation)
*Activate Skill*: `resonance-designer`

- [ ] **Data-Driven Design**: Run the Visual Engine.
    ```bash
    # EXAMPLE: python .agent/skills/resonance-designer/scripts/search.py "fintech dashboard dark" --design-system -p "MyFinFrame"
    ```
- [ ] **Extract Tokens**: Define the "Physics" of the UI before coding.
    -   **Primary**: `hsl(var(--primary))` (Not hex, not Tailwind default).
    -   **Radius**: `rounded-xl` (Modern) or `rounded-none` (Brutalist).
    -   **Depth**: `shadow-lg` + `border-white/10` (Glassmorphism).

## 2. The Skeleton (Structure)
*Activate Skill*: `resonance-frontend`

- [ ] **Mockup**: Create the HTML structure *without* color. Focus on Layout & Spacing.
    -   *Constraint*: Use `grid` or `flex`. No floats.
- [ ] **Mobile-First**: Define base classes for mobile, `md:` for desktop.

## 3. The Implementation (Tokens Only)
*Activate Skill*: `resonance-frontend`

- [ ] **Apply Tokens**:
    -   ❌ `bg-blue-500` (Generic)
    -   ✅ `bg-surface-primary` (Semantic)
- [ ] **Micro-Interactions (The Soul)**:
    -   buttons must `hover:scale-[1.02]` or `active:scale-95`.
    -   Lists must utilize `group-hover`.

## 4. The Visual Feedback Loop (The Mirror)
*Activate Skill*: `resonance-designer`

- [ ] **Browser Verification**: Open the page. Take a Screenshot (Mental or Actual).
- [ ] **The "Anti-Slop" Checklist**:
    -   [ ] **No Emojis**: Use Lucide/Heroicons SVGs.
    -   [ ] **No Default Scrollbar**: Custom scrollbar styling.
    -   [ ] **Breathability**: Is there enough whitespace? (When in doubt, multiply padding by 1.5).
    -   [ ] **Contrast**: Is the text `#000`? Change to `#18181b` (Off-black).
- [ ] **Mobile Torture Test**: Resize window to 320px. Does content overflow?

## 5. Final Polish
- [ ] **Motion**: Add entry animations. `animate-in fade-in slide-in-from-bottom-4 duration-500`.
- [ ] **Accessibility**: `tabindex`, `aria-label`, and `focus-visible:ring`.
