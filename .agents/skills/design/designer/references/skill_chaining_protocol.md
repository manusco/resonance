# Skill Chaining Protocol (The Visual/Behavior Split)

> **Source**: AI Design Components (`ancoleman`)
> **Objective**: Decouple logic from visuals to enable infinite theming.
> **Rule**: "Components must never hardcode styles. They must emit Token Variables."

## 1. The Core Principle
Code defines **Structure & Behavior**. Tokens define **Visual Style**.
These two must never mix.

```
Component Skill (Logic)  --->  Uses Tokens (Variables)  <---  Theme File (Values)
```

## 2. The Golden Rules
1.  **No Hardcoded Values**: Never use `16px`, `#3B82F6`, or `sans-serif` in component code.
2.  **Semantic Naming**: Use names that describe *what* it is, not *what it looks like*.
    *   ❌ `blue-button-bg`
    *   ✅ `button-bg-primary`
3.  **Logical Properties**: Always use logical CSS properties for RTL support.
    *   ❌ `margin-left`
    *   ✅ `margin-inline-start`

## 3. The Token Hierarchy

### Level 1: Primitives (Internal)
*   Raw values. Agents should never reference these directly.
*   Example: `--blue-500: #3B82F6`

### Level 2: Semantic (The Interface)
*   The contract between design and engineering.
*   Example: `--color-primary: var(--blue-500)`

### Level 3: Component (The Implementation)
*   Scoped to the specific element.
*   Example: `--button-bg-primary: var(--color-primary)`

## 4. Implementation Checklist
When generating code for a component:

- [ ] **Tokenize Colors**: Are all colors mapped to `--component-property-state`?
- [ ] **Tokenize Spacing**: Are paddings/margins using `--spacing-md` or logical tokens?
- [ ] **RTL Check**: Did you use `padding-inline` instead of `padding-left/right`?
- [ ] **Theme Agnostic**: Will this look correct if the underlying variable changes to black/white?
