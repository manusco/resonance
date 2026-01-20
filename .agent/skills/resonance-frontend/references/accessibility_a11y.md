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

> 🔴 **Rule**: Run `Lighthouse > Accessibility` on every page. Score MUST be 100.
