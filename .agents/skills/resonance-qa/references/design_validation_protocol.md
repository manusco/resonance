# Protocol: Design Validation (Figma vs Code)
> **Objective**: Ensure pixel-perfect implementation of the design.
> **Philosophy**: "If it doesn't look like Figma, it's a bug."

## 1. The Validation Checklist

### A. Layout & Spacing (The Box Model)
*   [ ] **Padding**: Open DevTools. Hover. Does the green padding match Figma?
*   [ ] **Margins**: Check element spacing. Are we using the defined variables (e.g., `gap-4`)?
*   [ ] **Alignment**: Is the content centered/aligned exactly as specified?

### B. Typography (The Font Stack)
*   [ ] **Line Height**: This is the #1 missed detail. Check `line-height` against Figma.
*   [ ] **Letter Spacing**: Check for `tracking-tight` or `wide`.
*   [ ] **Weight**: Is it `500` (Medium) or `600` (SemiBold)? Don't guess.

### C. Visuals (Colors & Radius)
*   [ ] **Shadows**: Do the `box-shadow` values align? (e.g., `shadow-lg` vs `shadow-xl`).
*   [ ] **Border Radius**: Is it `rounded-md` (6px) or `rounded-lg` (8px)?
*   [ ] **Hex Codes**: Sample the color. Is it exact?

---

## 2. Bug Reporting Standard (Visuals)

**Title**: `[UI] Button padding mismatch on Login`

| Field | Value |
| :--- | :--- |
| **Component** | PrimaryButton |
| **Expected (Figma)** | `px-4 py-2` (16px / 8px) |
| **Actual (Code)** | `p-3` (12px) |
| **Fix** | Update classes to match tokens. |
