# Skill Chaining Protocol (The Visual/Behavior Split)

> **Objective**: Keep visual values maintainable and reusable where the product needs shared styling.
> **Rule**: Reuse the project's maintained value owner. Do not require a token system where the platform or local component already owns the styling.

## 1. The Core Principle
Code defines structure and behavior. A project's theme or component source may own visual values. Preserve its existing boundaries and use tokens where the project already has them or a real shared need justifies them.

```
Component structure and behavior  --->  Project value owner (theme, token, component, or platform)
```

## 2. The Golden Rules
1. **Use existing owners**: Follow the project's token, theme, component, or native platform conventions. Add a semantic token only for a real shared role.
2. **Name by role**: When the project uses semantic names, describe purpose and state rather than a literal color.
3. **Use platform direction support**: In CSS, use logical properties where they correctly express the layout and support the project's RTL needs. Native platforms use their own direction-aware APIs.

## 3. Optional token layers

Projects may distinguish raw values, semantic roles, and component-specific values when that structure helps them. This is an option, not a required three-layer architecture.

## 4. Implementation check

- Reuse maintained values and behavior; avoid copying values into a competing source.
- Use logical CSS properties where appropriate and preserve native platform conventions.
- Verify the affected pattern in its supported themes, states, and direction when those are in scope.
