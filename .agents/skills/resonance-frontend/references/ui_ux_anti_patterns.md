# UI/UX Anti-Patterns & Strict Guidelines

> **Source**: Integration of `ui-ux-pro-max-skill`.
> **Objective**: Professionalize UI implementation by strictly avoiding amateur visual and interaction mistakes.

## 1. Interaction & State Anti-Patterns
*   **Layout-Shifting Hovers**: ❌ Never use `transform: scale()` or border width changes on hover if it causes the surrounding layout to jump or shift.
*   **Instant State Changes**: ❌ Never snap between states (hover/active/disabled) in 0ms. Always use `transition: all 150ms ease-in-out` (or similar).
*   **Invisible Disabled States**: ❌ Never leave disabled buttons looking clickable. Reduce opacity to 0.5, change the cursor to `not-allowed`, and remove hover effects.
*   **Missing Cursors**: ❌ All clickable elements (that do not default to it, like custom divs acting as buttons) MUST have `cursor: pointer`.

## 2. Visual & Theming Anti-Patterns
*   **Emoji as Icons**: ❌ Never use emojis for navigation, settings, or system controls. They are font-dependent and unprofessional. Use SVGs.
*   **Hardcoded Hex Values**: ❌ Never hardcode `#1a1a1a` in a component. It breaks Dark Mode scaling. Use semantic variables (`var(--color-surface)` or Tailwind `bg-surface`).
*   **Pure Black/White in Dark Mode**: ❌ Never use `#000000` background with `#FFFFFF` text. It causes eye strain. Use `#121212` background and `#E0E0E0` text.
*   **Color-Only Indicators**: ❌ Never convey critical information (like an error state) using solely color (e.g., a green vs red border). Always include a text label or distinct icon.

## 3. Layout & Mobile Anti-Patterns
*   **Ignoring Safe Areas**: ❌ Don't place fixed headers or footers in the device notch or gesture bar areas. Respect `safe-area-inset-bottom`.
*   **Tiny Touch Targets**: ❌ Do not make mobile buttons smaller than `44x44px` (iOS) or `48x48dp` (Android). If the visual icon is smaller, expand the hit area.
*   **Horizontal Scroll Traps**: ❌ Ensure no main content forces a horizontal scroll on mobile viewport settings. Use `max-w-full` and `overflow-x-hidden` on roots if necessary.
*   **Gesture Conflicts**: ❌ Do not put a horizontal swipe carousel inside a drawer that is dismissed via a horizontal swipe.
