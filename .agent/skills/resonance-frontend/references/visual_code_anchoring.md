# Protocol: Visual-to-Code Anchoring (Screenshot Mapping)

> **Status**: Core Implementation Standard
> **Objective**: Bridge the gap between visual screenshots and the underlying code structure to ensure 100% targeting accuracy.

## 1. The Anchoring Hack

When a project is complex, verbal descriptions of UI elements (e.g., "the blue button at the bottom") are brittle. 

**The Strategy**: Use a screenshot to create a "Visual Map" that anchors pixels to code components.

## 2. Implementation Loop

1.  **Ingestion**: If provided with a screenshot of the UI, do not just look at it. Create an internal **Functional Map**.
2.  **Mapping**: Identify the "Partials" or "Components" that correspond to visual areas.
3.  **Naming**: Assign names to these regions that reflect their CSS class or Component filename (e.g., `Header.astro` -> `#header-region`).

### Example Diagram:
```text
+---------------------------------------+
| [A] Navbar (GlobalNav.astro)          |
+---------------------------------------+
| [B] Hero Section (Hero.jsx)           |
|     - CTA Button (#hero-cta)          |
+---------------------------------------+
| [C] Content Grid (CardStack.tsx)     |
|     - Item Card (.item-card)          |
+---------------------------------------+
```

## 3. Why This Works

*   **Shared Vocabulary**: The Agent and User now speak the same language. "Moving [B] into [C]" has a deterministic meaning.
*   **Topological Integrity**: Ensures that the agent doesn't accidentally move a component to a parent it shouldn't belong to.
*   **Refactor Speed**: Greatly reduces the "Discovery" phase when performing visual redesigns or migrations.

---
*Created by the Frontend Specialist. Part of the Outstanding Skills Standard.*
