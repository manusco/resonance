# Mobile Audit Protocol

Check reach, posture, screen size, input precision, and platform behavior in the actual task.

## 1. The Thumb Zone

*   **Reach**: Place frequent actions where the intended posture can reach them; do not assume one universal safe zone.
*   **Placement**: Keep navigation consistent with the target platform and user expectation. Test important actions with one-hand use when that is a supported scenario.

## 2. The Touch Target

*   **Size**: Follow target platform guidance and applicable accessibility criteria. WCAG 2.2 AA target size (minimum) is 24×24 CSS px or spacing, with exceptions; native platform recommendations can be larger.
*   **Spacing**: Provide enough separation to avoid accidental activation for the actual controls and context.
*   **Audit**: Turn on "Show Taps" in Developer Settings. Do you miss?

## 3. The Keyboard

*   **Input Type**: `type="email"` shows `@`. `type="number"` shows numpad.
*   **Overlay**: Does the keyboard cover the input field? (Push content up).
*   **Auto-Complete**: `autocomplete="one-time-code"` for 2FA.

> 🔴 **Rule**: Test on a *real device*. Chrome DevTools is a lie for touch physics.
