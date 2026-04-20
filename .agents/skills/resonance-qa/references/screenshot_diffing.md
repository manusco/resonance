# Visual Regression Protocol (Pixel Perfect)

> "CSS breaks silently. Catch it loudly."

## 1. The Snapshot Strategy

1.  **Golden Master**: The "Correct" image (committed to git).
2.  **Test Run**: Render component -> Screenshot.
3.  **Diff**: Compare pixels. If > 0.1% difference -> FAIL.

## 2. The Isolation

Visual tests are FLAKY unless isolated.
*   **Disable Animations**: CSS `* { animation: none !important; }`.
*   **Mock Dates**: Freeze time to "Jan 1, 2000".
*   **Mock Images**: Replace random Unsplash URLs with solid colors.

## 3. The Tooling

*   **Playwright**: `await expect(page).toHaveScreenshot()`.
*   **Percy/Chromatic**: For Storybook component libraries in CI.

> 🔴 **Rule**: Never approve a visual change without seeing the "Before/After" diff image.
