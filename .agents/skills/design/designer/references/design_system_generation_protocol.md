# Design System Generation Protocol

> **Source**: Integration of `ui-ux-pro-max-skill` methodology.
> **Objective**: Eliminate haphazard styling by forcing the creation of a hierarchical Design System before any UI code is written.

## 1. The Reasoning Engine (Pre-Design)
Before choosing styles, analyze the product context via these dimensions:
1.  **Product Type**: Is this a SaaS Dashboard, a Luxury E-commerce, or a Productivity Tool?
2.  **Conversion Focus**: Is the goal lead gen, storytelling, or data density?
3.  **Target Audience**: Enterprise C-Suite vs Gen Z consumers.

## 2. The Output: Master + Overrides Architecture
Do not use scattered CSS or inline styles. Establish a Source of Truth.

### Step 1: Create `design-system/MASTER.md`
This is the global source of truth. It must define:
*   **Semantic Colors**: Primary, Secondary, Background, Text, Surface, Error, Success (Never hardcode raw hex values in components).
*   **Typography**: Heading Font, Body Font, Scale (e.g., base 16px, 1.5 line-height).
*   **Spacing System**: Base-8 rhythm (4px, 8px, 16px, 24px, 32px).
*   **Global Effects**: Define exact shadow values (`--shadow-sm`, `--shadow-md`) and transition durations (e.g., `200ms ease`).

### Step 2: Create Page Overrides (`design-system/pages/[page-name].md`)
When building a specific page (e.g., the Checkout page), create a local override file.
*   **Rule**: If the page override exists, its rules take precedence over the `MASTER.md` for that specific page context. This prevents the global file from becoming bloated with single-use utility classes.

## 3. The 5 Core Directives
When generating the Design System, enforce these constraints:
1.  **Stop Emoji Architecture**: Never use emojis (🎨, 🚀) as structural icons. Use proper vector SVG libraries (Lucide, Heroicons).
2.  **No Pure Flat or Pure Skeuomorphism**: Use subtle depth, distinct layering, and "Soft UI Evolution" unless Brutalism or a specific artistic direction is requested.
3.  **Accessibility is Default**: All text must pass WCAG 4.5:1 contrast. Focus states must be visible.
4.  **Motion has Meaning**: Animations should explain state changes, not just act as decoration. Target 150-300ms duration.
5.  **Touch Target Supremacy**: Minimum 44x44px for all interactive elements on mobile views.
