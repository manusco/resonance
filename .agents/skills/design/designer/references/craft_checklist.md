# Craft Checklist: the pre-ship 1% audit

> The basics right, the edges designed, and the invisible details tuned. Run this before calling any design done. Each item is small. Together they are the difference between a design that works and one that feels outstanding. If an item fails, fix it before ship.

## Hierarchy and clarity
- [ ] The task, current status, and useful next action are findable. Give each emphasis according to its role; multiple valid actions may share prominence.
- [ ] Actions are weighted by task frequency and consequence. Destructive actions identify their target and consequence and have a safe exit or recovery path.
- [ ] A first-time user knows what to do without being told. Nothing requires a second read.
- [ ] Emphasis is scarce: not everything is bold, colored, or boxed.

## Typography
- [ ] Body text has a readable measure for its content and viewport; constrain long reading lines where useful.
- [ ] Type sizes come from one scale. No off-scale one-offs.
- [ ] Leading fits the size: tight on headlines, open on body.
- [ ] Real punctuation: curly quotes, proper apostrophes, a real ellipsis, and a clear range separator ("to", or an en dash only where house style permits).
- [ ] No orphans or widows in headlines. Multi-line titles are balanced.
- [ ] Tabular numerals anywhere numbers align or change in place.

## Color and contrast
- [ ] Color roles are intentional and contrast is checked against WCAG 2.2 AA; perceptual authoring spaces are optional tools.
- [ ] Body text meets the contrast target; nothing critical relies on color alone.
- [ ] Color roles remain clear; dark themes preserve surface and text separation.
- [ ] The hierarchy still reads in grayscale.

## Space and alignment
- [ ] Related spacing values form a coherent rhythm; deliberate exceptions fit the content or task.
- [ ] Grouping cues fit the information relationship; use proximity, borders, surfaces, or a combination.
- [ ] Related elements align clearly; optical refinements preserve readable layout and supported zoom.
- [ ] The layout breathes at the outer margins; content is not jammed to the edge.

## Optical detail
- [ ] When rounded surfaces nest, their radii relate to padding and the chosen shape language; check the rendered corners.
- [ ] Icons and glyphs are optically centered, not box-centered. Any triangle or circle is nudged and overshot as needed.
- [ ] Separators have sufficient contrast and fit the chosen visual language.
- [ ] Directional lighting is coherent when the style uses it.
- [ ] Shadows, if used, are tuned to the surface and role; flat and outline-based styles need no shadow recipe.

## Motion and feel
- [ ] Motion helps users follow a change and does not delay frequent work or feedback; reduced-motion behavior is clear.
- [ ] Motion serves orientation or feedback, respects reduced-motion preferences, and does not delay frequent actions or user control.
- [ ] Hover never shifts layout and never hides anything essential. Press feedback fires under 100ms.
- [ ] Focus states are designed and use `:focus-visible`, not the raw browser outline.
- [ ] `prefers-reduced-motion` is honored without losing feedback.

## States and resilience
- [ ] Empty, loading, and error states are designed, not just the happy path.
- [ ] Disabled, loading, and selected states exist for interactive elements.
- [ ] Long text, missing values, and huge numbers do not break the layout.
- [ ] Long lists stay smooth at scale (virtualized or paginated).
- [ ] Failed and slow network states keep the user's input and explain what happened.

## Copy
- [ ] Designed with real content, not placeholder text.
- [ ] Buttons name their outcome. Labels use the user's words.
- [ ] Error messages say what happened and how to fix it, in plain language.
- [ ] Empty states guide the first action.

## Canvas and input
- [ ] Adapts across supported widths, including 320 CSS px reflow where applicable; type stays readable.
- [ ] Applicable WCAG 2.2 AA target-size criteria and platform guidance are met; essential actions are never hover-only.
- [ ] Safe areas respected; nothing critical under a notch or gesture bar.
- [ ] Reflows at 320 CSS px where applicable without losing information or function; verify zoom and text resizing.
- [ ] Behaves correctly for the actual input (touch, pointer, keyboard, remote), not just the width.

## The final pass
- [ ] Check for unexamined defaults (see ai_design_slop); familiar fonts, gradients, and card grids are acceptable when the system, brand, and task support them.
- [ ] Remove one more thing. If nothing was lost, it stays removed.
- [ ] Every decision on screen has a reason. Nothing is there by default or by accident.
