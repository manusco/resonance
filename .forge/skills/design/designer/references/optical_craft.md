# Optical Craft: the subconscious detail layer

> Optical review can refine visual balance after accessibility, platform, and geometric constraints are met. It complements measurements; it does not replace them.

## Contents
- Optical over mechanical
- Optical alignment
- Optical sizing and overshoot
- Optical centering of icons and glyphs
- Concentric border radius
- Hairlines and sub-pixel borders
- Spacing that looks equal
- The details that read as expensive

## Optical over mechanical

Measurements protect legibility, alignment systems, target sizes, and accessibility. Within those constraints, optical review can correct perceived balance. A small visual adjustment may help when it does not break the layout grid, text flow, hit area, or platform behavior. Check at supported sizes and zoom.

## Optical alignment

- **Punctuation hangs.** A quote mark or bullet aligned to the text edge by the box looks indented. Pull it into the margin (hanging punctuation) so the letters, not the marks, form the clean edge.
- **Left edges align by letterform, not bounding box.** A capital round letter (O, C, G) and a flat one (H, E) at the same x-coordinate look misaligned because the round one needs to overshoot. Good fonts handle this; when setting large display type by hand, nudge.
- **Optical margin.** Large headlines often need a slight negative left offset so the stroke, not the invisible side bearing, lines up with the content below it.

## Optical sizing and overshoot

- **Curved shapes may need visual balancing.** A circle or triangle can appear smaller than a square at the same dimensions. Inspect the actual icon set and adjust only when the weight difference is visible; do not use a fixed overshoot percentage.
- **The play button is nudged right.** A triangle centered by its bounding box looks left-heavy because its visual mass sits toward the point. Shift it right by a few percent so it looks centered inside its circle. The same logic applies to any asymmetric glyph.
- **Type overshoots the baseline.** Round and pointed letters (o, e, v, w) extend slightly past the baseline and cap height of flat letters. Correct fonts build this in. It is why text set in a font with no overshoot looks stiff.

## Optical centering of icons and glyphs

- An icon centered by its SVG viewbox is usually not optically centered, because the drawn shape rarely fills the box evenly. Center the visible ink, not the container.
- Icon plus label pairs need the gap tuned to the icon's visual weight, not a fixed token. A heavy glyph wants a touch more air than a light one at the same nominal size.
- In a circular avatar or button, a single glyph often needs a 1 to 2 percent optical nudge to sit dead center.

## Concentric border radius

When rounded elements nest, related corner shapes often look coherent when the inner radius accounts for the available padding. Use the relationship below as a starting point, then check the actual components and product style. It is not a universal requirement:

```
inner-radius = outer-radius - padding
```

A card with a 16px radius and 8px of padding could use an 8px inner radius. Square or differently shaped nested surfaces may better fit other systems.

## Hairlines and sub-pixel borders

- Use a separator only when grouping or edge definition needs it. Hairlines, solid borders, surface changes, and whitespace can all work when visible and legible.
- Check rendering at the target density and contrast; do not assume a sub-pixel or low-opacity line remains visible.
- Use proximity, surfaces, and lines according to the content relationship and visual language.

## Spacing that looks equal

- **Buttons need more horizontal than vertical padding**, and the label sits optically centered, which often means a hair more space below than above because descenders and the visual weight of the cap line pull the eye up.
- **Icon-adjacent text** rarely wants symmetric padding. The gap between an icon and its label is not the same as the gap from the label to the button edge.
- **Mixed-size neighbors.** When a large and a small element share a row, aligning their boxes looks off. Align their optical centers or their shared baseline instead.
- **Trailing punctuation and inline icons** shift perceived center. A row that is mathematically centered with a trailing chevron looks left-shifted. Account for the chevron's weight.

## The details that read as expensive

Use the relevant checks for the chosen style and task. These are craft options, not requirements for every interface.

- Coherent direction for shadows and highlights, when the style uses directional light.
- Related geometry for nested corners, when rounded surfaces are used.
- Separators with enough contrast to read at target sizes.
- Real punctuation: curly quotes, proper apostrophes, a real ellipsis, and a clear range separator (the word "to", or an en dash only where the brand's house style permits it).
- No orphans or widows in headlines; balanced multi-line titles.
- Tabular numerals in tables and anywhere numbers change in place.
- Motion is tuned where it improves orientation or feedback; immediate changes remain appropriate for frequent work and reduced-motion settings.
- Focus states that look designed, not the browser default outline.
- Optical centering where it improves balance without reducing hit areas or breaking alignment.
- Small visual adjustments only after checking text, contrast, touch targets, zoom, and layout constraints.
