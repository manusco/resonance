# Depth and Materials

> Depth in an interface should behave like depth in the real world: driven by a consistent light source and expressed through shadow, layering, and material. Fake depth (a default gray blur, glass for no reason) is a tell. Real depth is quiet and physical.

## Contents
- One light source
- Shadows are layered, not single
- Elevation as a system
- Hairlines and edges
- Texture and grain
- Glass, only when it earns it
- The flat trap and the skeuomorphic trap

## One light source

Decide where the light comes from, almost always top or top-left, and commit. Every shadow in the product falls the same way, every raised edge catches light on the same side. Inconsistent light direction is felt as wrongness even when the viewer cannot say why. This single rule makes a set of components feel like one physical object rather than a pile of parts.

## Shadows are layered, not single

A single `box-shadow: 0 2px 4px rgba(0,0,0,0.2)` is the default that says no one tuned the depth. Real shadows are soft, tinted, and built from more than one layer.

- Stack two to four shadows at increasing blur and distance, each at low opacity. The near, tight, slightly darker layer grounds the object; the far, wide, fainter layer gives ambient softness.
- Tint the shadow toward the background or the brand hue rather than pure black. A shadow tinted with a little of the surface color sits into the scene; a pure black shadow floats on top of it.
- Larger elevation means longer distance, wider blur, and lower opacity, not just a bigger single shadow. As things rise, their shadow softens and spreads.
- Keep shadow opacity low. Two soft layers at 6 to 12 percent read as expensive; one hard layer at 30 percent reads as a drop-shadow filter.

## Elevation as a system

- Define a small set of elevation levels (for example: flat, raised card, sticky bar, popover, modal) and give each a fixed shadow recipe. Every component picks a level; nothing invents its own shadow.
- Elevation should map to meaning: the higher something sits, the more temporary and the more focused it is. A modal is high because it is a moment; a page background is flat because it is the ground.
- In dark mode, shadows barely register. Carry elevation with lightness instead: each level up is a small step lighter. See color_and_contrast.

## Hairlines and edges

- Separate with a hairline before a heavy border. A translucent edge (black or white at 8 to 12 percent) suggests structure without shouting. See optical_craft.
- A subtle top highlight (a 1px inset light line) on a raised surface catches the light source and reads as a real edge. Pair it with the shadow below for a physical, pressed-metal feel when the style calls for it.
- Prefer one separation cue at a time. A border plus a shadow plus a background change on the same edge is three answers to one question.

## Texture and grain

- A faint grain or noise overlay (very low opacity) warms up flat color and kills banding in gradients. It is one of the quiet tricks that makes a screen feel less digital and more like a printed surface.
- Texture belongs in the brand register and in backgrounds, kept subtle. Loud texture competes with content.
- Decorative grid and dot backgrounds are the opposite: they read as filler, not material. Grain adds warmth; graph paper adds noise.

## Glass, only when it earns it

- Backdrop blur (glassmorphism) is a real material with one honest job: showing that a layer floats above moving content, like a translucent toolbar over a scrolling page. There it aids depth and context.
- Applied by reflex to static cards, it hurts contrast and legibility and marks the design as trend-chasing. If there is nothing meaningful behind the glass, it is decoration.
- When you use it: keep enough contrast for the text on top, add a faint border to define the pane's edge, and make sure it degrades gracefully where backdrop blur is unsupported.

## The flat trap and the skeuomorphic trap

- Pure flat with no depth cues makes it hard to tell what is interactive and what is a surface. Users need affordance; a button should look pressable.
- Heavy skeuomorphism (literal leather, glossy bevels) dates instantly and adds noise. The target is between: subtle, consistent depth that communicates layering and interactivity without imitating physical objects literally. Soft, honest, restrained.
