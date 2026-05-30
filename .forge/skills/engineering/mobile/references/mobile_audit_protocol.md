# Mobile Audit Protocol

> "Thumbs are fat. Screens are small."

## 1. The Thumb Zone

*   **Bottom Navigation**: Critical actions (Home, Search) within easy reach.
*   **Top Left**: The "Zone of Death". Only put Back buttons or Logos there.

## 2. The Touch Target

*   **Size**: Minimum 44x44px (iOS Standard) / 48x48px (Material).
*   **Spacing**: 8px between tappable elements.
*   **Audit**: Turn on "Show Taps" in Developer Settings. Do you miss?

## 3. The Keyboard

*   **Input Type**: `type="email"` shows `@`. `type="number"` shows numpad.
*   **Overlay**: Does the keyboard cover the input field? (Push content up).
*   **Auto-Complete**: `autocomplete="one-time-code"` for 2FA.

> 🔴 **Rule**: Test on a *real device*. Chrome DevTools is a lie for touch physics.
