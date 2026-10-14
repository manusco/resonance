# Touch Physics Config

Choose motion from the interaction. Springs can suit direct manipulation and settling; discrete status changes can use a brief fade, another platform-native transition, or no motion. Follow the platform and the user's motion preference.

## 1. Optional Spring Tuning (Reanimated / Framer Motion)

| Feel | Stiffness | Damping | Mass | Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Snappy** | 300 | 20 | 1 | Buttons, Toggles, Small UI |
| **Bouncy** | 200 | 10 | 1 | Notifications, Success Badges |
| **Heavy** | 100 | 20 | 2 | Modals, Drawers, Bottom Sheets |
| **Precise** | 400 | 30 | 1 | Drag-and-drop snapping |

These values are starting points for tuning a specific interaction, not platform-independent requirements. Test with the actual gesture, content, and device.

## 2. Interaction Checks

### The "Overdrag"
Use the platform's expected scroll and overscroll behavior. Do not add a web CSS property to native Android interactions.

### The "16ms Rule"
Respond promptly to touch using the platform's interaction and rendering tools. A one-frame target depends on device refresh rate and implementation; verify perceived responsiveness on supported hardware.
*   **Bad**: Logic -> State Update -> Render -> Feedback.
*   **Good**: Native Driver / UI Thread Feedback -> Logic.

## 3. Haptics Protocol

*   Use haptics only when they reinforce a meaningful action and are supported by the device.
*   Keep destructive/error feedback calm and pair it with clear text; do not assume stronger haptics are always safer.
