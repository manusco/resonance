# Accessibility (A11y) Protocol

> "The web is for everyone. No exceptions."

## 1. The Input Labels

Every `<input>` MUST have a `<label>`.

*   ❌ `<input placeholder="Email" />`
*   ✅ `<label htmlFor="email">Email</label><input id="email" />`
*   ✅ (Hidden Label): `<label class="sr-only">Email</label>`

## 2. Focus Management

*   **Keyboard Nav**: Can you use the site with ONLY `Tab` and `Enter`?
*   **Focus Ring**: Never remove `outline` without replacing it.
    *   ❌ `outline: none;`
    *   ✅ `outline: none; ring: 2px solid blue;`

## 3. Semantic HTML

*   Use `<button>` for actions.
*   Use `<a>` for navigation.
*   Do NOT use `<div onClick={...}>`. (Divs are not buttons).

## 4. Color Contrast

*   **Text**: 4.5:1 ratio minimum.
*   **Icons**: 3:1 ratio minimum.

## Source Card

- Primary source: https://www.w3.org/TR/WCAG22/
- Secondary source: https://www.w3.org/WAI/standards-guidelines/wcag/
- Verified: 2026-08-15
- Scope: WCAG 2.2 conformance and accessibility testing.
- Review trigger: W3C publishes a new WCAG recommendation or the project changes its accessibility target.

> 🔴 **Rule**: Lighthouse accessibility is a useful lab check, not WCAG conformance. Target WCAG 2.2 AA unless the project has a stricter legal or product requirement. Verify with keyboard navigation, focus order, semantic structure, labels, contrast, screen-reader checks where practical, and user-flow testing.
