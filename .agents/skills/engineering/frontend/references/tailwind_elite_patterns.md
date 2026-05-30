# Tailwind Elite Patterns

> "Utility-first does not mean messy."

## 1. The Layout Primitives

### The "Grid Stack" (Overlay)
Instead of `position: absolute`, use CSS Grid to stack elements.

```html
<div class="grid isolate">
  <!-- Layer 1: Image -->
  <img class="col-start-1 row-start-1 -z-10 w-full" />
  <!-- Layer 2: Gradient -->
  <div class="col-start-1 row-start-1 bg-black/50" />
  <!-- Layer 3: Text -->
  <div class="col-start-1 row-start-1 self-center justify-self-center text-white">
    Hero Text
  </div>
</div>
```

### The "Full Bleed" (Breakout)
Allow content to span full width inside a constrained container.

```css
.full-bleed {
  width: 100vw;
  margin-left: calc(50% - 50vw);
}
```

## 2. Dynamic Typography (Fluid Type)

Don't use static `text-xl`. Use `clamp()` via Tailwind Arbitrary Values or Config.

*   **Pattern**: `text-[clamp(1rem,2.5vw,1.5rem)]`
*   **Why**: Scales perfectly from Mobile to Ultra-Wide.

## 3. The "Group Hover" Card

Animate child elements when the *parent* is hovered.

```html
<div class="group relative overflow-hidden rounded-xl">
  <img class="transition-transform duration-500 group-hover:scale-110" />
  <div class="absolute inset-0 bg-black/60 opacity-0 transition-opacity group-hover:opacity-100" />
  <p class="translate-y-4 opacity-0 transition-all group-hover:translate-y-0 group-hover:opacity-100">
    Revealed Content
  </p>
</div>
```

## 4. The Mandate

*   **No `@apply`**: Do not use `@apply` in CSS files unless creating a global base style. Keep utility classes in HTML.
*   **Arbitrary Value Abuse**: If you use `w-[123px]` more than twice, make it a `theme.extend` value.
*   **Ordering**: Use `prettier-plugin-tailwindcss`.

> 🔴 **Rule**: If you write `style="..."`, you have failed.
