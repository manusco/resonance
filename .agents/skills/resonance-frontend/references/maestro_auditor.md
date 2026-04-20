# The Maestro Auditor (Self-Correction Protocol)

> "The difference between Junior and Senior is the ability to catch your own mediocrity."

## 1. The Rejection Triggers (Auto-Fail)

**Run this mental check before submitting code:**

| Trigger | Description | Corrective Action |
| :--- | :--- | :--- |
| **The "Safe Split"** | Using `grid-cols-2` or 50/50, 60/40 layouts. | **Switch to** `90/10` or `100% Stacked`. (See Design Protocols). |
| **The "Glass Trap"** | Using `backdrop-blur` without raw borders. | **Add** a 1px solid border (alpha 0.5) to define edges. |
| **The "Static Hover"** | Hovering creates no movement. | **Add** `scale(1.02)` or `y-translate(-2px)`. |
| **The "Div Soup"** | Nesting > 4 divs deep. | **Refactor** into a sub-component. |
| **The "Loading Flash"** | Content jumps on load. | **Add** a Skeleton Loader of the exact same height. |

## 2. The "Template Test" (Brutal Honesty)

Ask yourself:
1.  **"Could this be a Vercel Template?"**
    *   YES -> You failed. **Add weirdness.**
    *   NO -> Proceed.
2.  **"Would I scroll past this?"**
    *   YES -> You failed. **Increase contrast/size.**
    *   NO -> Proceed.
3.  **"Did I check Mobile?"**
    *   NO -> You failed. **Open DevTools Mobile View.**

## 3. Performance Law Verified

*   [ ] Images are `WebP`/`AVIF`.
*   [ ] `next/font` is used (No google font CSS requests).
*   [ ] Input debouncing is active (No API call on every keystroke).
