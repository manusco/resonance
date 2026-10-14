# Design System Generation Protocol

> **Objective**: Define only the shared design foundations this project or task needs. Reuse an existing system when it fits; a design-system document is not a prerequisite for every UI change.

## 1. The Reasoning Engine (Pre-Design)
Before choosing styles, analyze the product context via these dimensions:
1.  **Product Type**: Is this a SaaS Dashboard, a Luxury E-commerce, or a Productivity Tool?
2.  **Conversion Focus**: Is the goal lead gen, storytelling, or data density?
3.  **Target Audience**: Enterprise C-Suite vs Gen Z consumers.

## 2. Optional documentation for a system-wide effort
Document shared decisions when the scope spans a system or when implementation needs a durable reference. Keep local styling consistent with the product's existing conventions without requiring a new system document for a scoped screen or component.

### Step 1: Record shared foundations when useful
If the work needs a shared reference, record the decisions that recur across the product. Include only foundations relevant to the scope:
*   **Color roles**: Define reusable semantic tokens where repeated roles need coordination. Choose the palette and representation from the product system and brief.
*   **Typography**: Choose one or more typefaces, sizes, and line-height relationships that fit the content, brand, platform, and legibility needs.
*   **Spacing and shape**: Define reusable values where they help related components feel coherent. Choose a scale for this product; Base-4, Base-8, fluid values, and deliberate exceptions can all fit.
*   **Depth and motion**: Document reusable shadow, border, surface, or transition values only when the product uses those treatments. Flat, outlined, and reduced-motion designs need no invented effects.

### Step 2: Record local exceptions when useful
For a page or component with a justified contextual variation, document the exception only when it will help implementation or future maintenance. Keep the shared reference concise and explain how the local choice serves its task.

## 3. The 5 Core Directives
When generating the Design System, enforce these constraints:
1.  **Stop Emoji Architecture**: Never use emojis (🎨, 🚀) as structural icons. Use proper vector SVG libraries (Lucide, Heroicons).
2.  **Coherent Visual Language**: Flat, outlined, material, and skeuomorphic treatments can fit different products. Keep related roles consistent within the chosen system and make controls and states distinguishable.
3.  **Accessibility is Default**: Meet applicable WCAG 2.2 AA contrast criteria, including 4.5:1 for normal text and 3:1 for large text within their defined scope. APCA and perceptual lightness checks may supplement visual tuning; they do not replace conformance. Make keyboard focus visible.
4.  **Motion has Meaning**: Use animation when it helps users follow a change or gesture. Choose timing from the transition, platform, task frequency, and motion preferences; no duration range is universal.
5.  **Touch targets**: Meet applicable WCAG 2.2 AA target-size criteria and exceptions. Apply platform recommendations in their own units and contexts; make small controls forgiving where layout permits.
