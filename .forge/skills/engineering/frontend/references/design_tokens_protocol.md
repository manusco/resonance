# Protocol: Design Tokens (Semantic Layering)
> **Objective**: Decouple design decisions from code values.
> **Philosophy**: "Developers shouldn't know hex codes."

## 1. The Token Hierarchy

### Level 1: Primitives (The Palette)
*Raw values. Do not use these directly in components.*

```typescript
const primitives = {
  blue: {
    500: '#3b82f6',
    600: '#2563eb', // Brand Primary
  },
  gray: {
    900: '#111827', // Text Primary
    100: '#f3f4f6', // Background
  }
}
```

### Level 2: Semantic (The Meaning)
*Contextual aliases. Use these.*

```typescript
const semantic = {
  text: {
    primary: primitives.gray[900],
    secondary: primitives.gray[500],
    inverse: primitives.white,
  },
  bg: {
    surface: primitives.white,
    canvas: primitives.gray[100],
  },
  action: {
    primary: primitives.blue[600],
    primaryHover: primitives.blue[700],
  }
}
```

---

## 2. Naming Convention
*   **Scale**: `xs, sm, md, lg, xl` (T-Shirt sizing for spacing/radius).
*   **Intent**: `success, warning, error, info` (Feedback colors).
*   **Interactive**: `default, hover, active, disabled` (States).

## 3. Dark Mode Strategy
tokens should be implemented via CSS Variables or a Theme Provider that swaps the *Semantic* layer, not the *Primitive* layer.

```css
:root {
  --text-primary: #111827;
}

[data-theme="dark"] {
  --text-primary: #f9fafb;
}
```
