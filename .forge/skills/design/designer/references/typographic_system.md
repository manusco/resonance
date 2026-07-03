# Typographic System

> Most of an interface is text. Set it well and the design is most of the way there. Set it carelessly and no amount of color or motion will save it. Typography carries hierarchy before any other tool.

## Contents
- Measure: the line length that reads
- Leading tied to measure
- The modular scale
- Weight and size as hierarchy
- Optical sizing and tracking
- Numerals: tabular vs proportional
- Micro-typography
- Font selection without the default reflex

## Measure: the line length that reads

The measure is the number of characters per line. The eye loses its place on lines that are too long and tires on lines too short.

- Body text: 45 to 75 characters per line, 66 is the classic target. Set it with `max-width` in `ch` units, around `65ch`.
- Never let long-form body text run the full width of a wide screen. This is one of the most common and most damaging layout mistakes.
- Short UI labels and captions are exempt; the measure rule is about reading passages.

## Leading tied to measure

Line height is not a fixed number, it is a relationship. Longer lines need more leading so the eye can find the next line start.

- Body copy: line-height around 1.5 to 1.65 at a normal measure.
- Large headlines: tighter, 1.05 to 1.2. Display type with body leading looks slack.
- Dense UI text and captions: 1.35 to 1.45.
- As measure grows, leading grows. As type size grows, relative leading shrinks.

## The modular scale

Sizes come from a ratio, not from picking numbers that feel nice. A scale creates harmony the way a musical key does.

- Pick a base (commonly 16px for body) and a ratio. Useful ratios: 1.2 (minor third, calm), 1.25 (major third), 1.333 (perfect fourth, strong hierarchy), 1.5 (perfect fifth, dramatic).
- Each step multiplies the last. A 1.25 scale from 16: 16, 20, 25, 31, 39, 49, 61.
- Round to sensible pixels. Do not invent off-scale sizes for one-off headings; if you need a new size, question whether the hierarchy is right.
- Fluid type: interpolate size between viewport widths with `clamp()`, for example `clamp(2rem, 1.2rem + 3vw, 3.5rem)`, so headings scale smoothly instead of jumping at breakpoints.

## Weight and size as hierarchy

Hierarchy is built from contrast, and type gives you two axes before color: size and weight.

- A clear step in size or weight separates levels. A timid step (16px next to 17px, or 400 next to 500) reads as a mistake, not a hierarchy.
- Prefer a strong weight jump over a color change for emphasis in body text. Bold carries more hierarchy than a hue shift and survives on any background.
- Do not use more than two or three weights in one system. Regular for body, a heavier weight for headings and emphasis, maybe one lighter for large display. More weights is noise.
- Avoid faux bold and faux italic. Load the real weight or do not use it.

## Optical sizing and tracking

- **Tracking (letter-spacing) is size-dependent.** Large display type wants slightly negative tracking (tighter) so it does not look loose. Small text and all-caps want positive tracking so letters do not collide. Body text at reading size wants none.
- All-caps labels always need positive tracking, roughly 0.05 to 0.1em, or they read as cramped.
- **Optical sizing.** Variable fonts with an optical size axis render differently at display vs text sizes (thinner hairlines and tighter spacing when large). Use it where available; it is why headlines from a good type family look refined rather than just enlarged.

## Numerals: tabular vs proportional

- **Tabular numerals** (equal width) for anything that changes in place or lines up in columns: tables, timers, prices in a list, dashboards, counters. Without them, numbers jitter as they update. Set `font-variant-numeric: tabular-nums`.
- **Proportional numerals** for running prose, where equal spacing looks gappy.
- **Slashed or dotted zero** where zero and capital O could be confused (codes, IDs).
- Old-style figures (with ascenders and descenders) sit better in body prose; lining figures suit UI and tables.

## Micro-typography

The finishing that separates typeset from typed:

- Curly quotes and apostrophes, never straight ones. For ranges use the word "to", or an en dash only where the brand's house style allows it. Replace the em dash with a comma or colon. Use a real ellipsis character. (Resonance's own prose uses no en or em dashes; this guidance is for the typeset UI you design.)
- No orphans (a single word alone on the last line) and no widows (a short last line at the top of a column) in headlines. Use `text-wrap: balance` on headings and `text-wrap: pretty` on body to let the browser fix these.
- Hanging punctuation so quotes and bullets sit in the margin and the text edge stays clean.
- Ligatures on for display, kerning enabled (`font-kerning: normal`).
- Hyphenation on for justified or narrow columns; justified text without hyphenation opens ugly rivers of space.
- Prevent line breaks inside things that belong together: a name and its honorific, a number and its unit, with a non-breaking space.

## Font selection without the default reflex

- The neutral system sans on everything is the loudest AI tell. A typeface is a voice; silence is a choice you probably did not mean to make.
- One strong pairing is enough: a characterful display or heading face and a legible workhorse for body. Or one good family used across weights, which is often the more disciplined choice.
- Judge a face by its numerals, its punctuation, its bold, and how it looks at small sizes, not by its marketing specimen.
- In the product register, legibility and a full weight range beat personality. In the brand register, a face with a point of view is the fastest way to not look generic.
