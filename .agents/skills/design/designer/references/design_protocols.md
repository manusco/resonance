# The Elite Design Protocols

> "If the layout is predictable, you have failed."

## 1. Topological Betrayal Protocol

**The Problem**: Users maintain "Banner Blindness" for standard layouts (Left Text, Right Image).
**The Fix**: You must "Betray" their expectation of where elements should be.

| Standard (Banned) | The Betrayal (Mandatory) |
| :--- | :--- |
| **Hero Split** (50/50) | **Massive Type**: Text is 90% of screen. Visual is background. |
| **Bento Grid** | **Fragmentation**: Break the grid. Overlap elements. Use organic positioning. |
| **Centered H1** | **Extreme Asymmetry**: Push H1 to bottom-left corner. Leave 70% negative space. |
| **Cards** | **List/Table**: Or huge single-item focus. Cards are a crutch. |

> 🔴 **Rule**: Every section must use a DIFFERENT topology. If Section 1 is Grid, Section 2 must be List or Freeform.

## 2. The Purple Ban Protocol

**The Problem**: `#800080` and "Blurry Neon Gradients" scream "AI Gened".
**The Fix**: Use difficult, specific colors.

| Banned Color | Allowed Alternative |
| :--- | :--- |
| **Purple/Violet** | **Acid Green** (`#CCFF00`), **Signal Orange** (`#FF4500`), **Deep Burgundy**. |
| **Cyan/Teal** (SaaS Blue) | **Electric Blue** (`#0047FF`), **Slate Black**. |
| **Mesh Gradients** | **Solid Color** or **Grain Texture**. |

## 3. The "Motion Trinity" Protocol

Static elements are dead. Every interactive object needs 3 states:

1.  **Entrance**: Staggered reveal on scroll. (Never load all at once).
2.  **Hover**: Physical reaction (Scale, Color, or Icon swap).
3.  **Active/Click**: Haptic squeeze (Scale down).

> 🔴 **Rule**: If I hover a button and nothing happens, the design is broken.
