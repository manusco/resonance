# Touch Physics Config

> Spring physics make interfaces feel heavy and real. Linear animations feel cheap.

## 1. Spring Constants (Reanimated / Framer Motion)

| Feel | Stiffness | Damping | Mass | Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Snappy** | 300 | 20 | 1 | Buttons, Toggles, Small UI |
| **Bouncy** | 200 | 10 | 1 | Notifications, Success Badges |
| **Heavy** | 100 | 20 | 2 | Modals, Drawers, Bottom Sheets |
| **Precise** | 400 | 30 | 1 | Drag-and-drop snapping |

## 2. Interaction Rules

### The "Overdrag"
When scrolling ends, the list should "rubber band".
*   **iOS**: Native support.
*   **Android**: Add `overscroll-behavior`.

### The "16ms Rule"
Visual feedback must happen within **1 frame (16ms)** of the touch start.
*   **Bad**: Logic -> State Update -> Render -> Feedback.
*   **Good**: Native Driver / UI Thread Feedback -> Logic.

## 3. Haptics Protocol

*   **Light**: `ImpactFeedbackStyle.Light` on small switches.
*   **Medium**: `ImpactFeedbackStyle.Medium` on primary CTAs.
*   **Heavy**: `ImpactFeedbackStyle.Heavy` on errors/delete.
*   **Success**: `NotificationFeedbackType.Success` (Double tap feel).
