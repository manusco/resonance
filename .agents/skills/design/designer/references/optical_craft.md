# Optical Craft: the subconscious detail layer

> What measures equal often looks wrong. The eye, not the ruler, is the final judge. This is the single clearest mark of a designer who cares, and the layer AI design skips because it is invisible in a screenshot and only felt in use.

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

Mechanical is what the numbers say. Optical is what the eye sees. When they disagree, the eye wins, every time. A layout can be perfectly measured and still feel off, and a layout can be mathematically "wrong" by a pixel or two and feel perfectly balanced. Train yourself to trust the discomfort and hunt the cause.

## Optical alignment

- **Punctuation hangs.** A quote mark or bullet aligned to the text edge by the box looks indented. Pull it into the margin (hanging punctuation) so the letters, not the marks, form the clean edge.
- **Left edges align by letterform, not bounding box.** A capital round letter (O, C, G) and a flat one (H, E) at the same x-coordinate look misaligned because the round one needs to overshoot. Good fonts handle this; when setting large display type by hand, nudge.
- **Optical margin.** Large headlines often need a slight negative left offset so the stroke, not the invisible side bearing, lines up with the content below it.

## Optical sizing and overshoot

- **Circles and triangles overshoot squares.** A circle that is mathematically the same height as a square next to it looks smaller, because the eye measures area at the widest point. Make circular and triangular elements roughly 2 to 5 percent larger so they read as equal weight. This is why a well-drawn icon set does not sit on a rigid grid.
- **The play button is nudged right.** A triangle centered by its bounding box looks left-heavy because its visual mass sits toward the point. Shift it right by a few percent so it looks centered inside its circle. The same logic applies to any asymmetric glyph.
- **Type overshoots the baseline.** Round and pointed letters (o, e, v, w) extend slightly past the baseline and cap height of flat letters. Correct fonts build this in. It is why text set in a font with no overshoot looks stiff.

## Optical centering of icons and glyphs

- An icon centered by its SVG viewbox is usually not optically centered, because the drawn shape rarely fills the box evenly. Center the visible ink, not the container.
- Icon plus label pairs need the gap tuned to the icon's visual weight, not a fixed token. A heavy glyph wants a touch more air than a light one at the same nominal size.
- In a circular avatar or button, a single glyph often needs a 1 to 2 percent optical nudge to sit dead center.

## Concentric border radius

When a rounded element sits inside another rounded element, the radii must be concentric or the corners look pinched. The rule:

```
inner-radius = outer-radius - padding
```

A card with a 16px radius and 8px of padding around an inner element wants an 8px radius on that inner element, not 16px and not 4px. Nested radii that ignore this are a quiet tell that no one tuned the corners. Matched concentric corners are a quiet signal that someone did.

## Hairlines and sub-pixel borders

- A hard 1px `#ccc` border is a blunt instrument. Elite separators are hairlines: a border at low opacity (a semi-transparent black or white, around 8 to 12 percent) that suggests an edge without drawing a hard line.
- On high-density displays, a true hairline is thinner than one CSS pixel. Use a translucent border or a subtle shadow rather than a solid rule.
- Prefer separation by space over separation by line. Reach for a border only when proximity and background cannot do the job.

## Spacing that looks equal

- **Buttons need more horizontal than vertical padding**, and the label sits optically centered, which often means a hair more space below than above because descenders and the visual weight of the cap line pull the eye up.
- **Icon-adjacent text** rarely wants symmetric padding. The gap between an icon and its label is not the same as the gap from the label to the button edge.
- **Mixed-size neighbors.** When a large and a small element share a row, aligning their boxes looks off. Align their optical centers or their shared baseline instead.
- **Trailing punctuation and inline icons** shift perceived center. A row that is mathematically centered with a trailing chevron looks left-shifted. Account for the chevron's weight.

## The details that read as expensive

Run this list on anything meant to feel high-class. Each is invisible alone. Together they are the entire difference.

- Consistent light source, so every shadow falls the same way.
- Concentric radii on every nested corner.
- Hairline separators, not hard gray lines.
- Real punctuation: curly quotes, proper apostrophes, a real ellipsis, and a clear range separator (the word "to", or an en dash only where the brand's house style permits it).
- No orphans or widows in headlines; balanced multi-line titles.
- Tabular numerals in tables and anywhere numbers change in place.
- Easing on every state change, nothing snaps.
- Focus states that look designed, not the browser default outline.
- Optical, not mechanical, centering on every icon and glyph.
- One or two pixels of tuning wherever the eye says something is off, even when the ruler disagrees.
