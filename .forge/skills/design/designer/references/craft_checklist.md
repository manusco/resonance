# Craft Checklist: the pre-ship 1% audit

> The basics right, the edges designed, and the invisible details tuned. Run this before calling any design done. Each item is small. Together they are the difference between a design that works and one that feels outstanding. If an item fails, fix it before ship.

## Hierarchy and clarity
- [ ] Squint test passes: the single most important element leads when the design is blurred.
- [ ] One primary action per view. Secondary and destructive actions are weighted to match their role.
- [ ] A first-time user knows what to do without being told. Nothing requires a second read.
- [ ] Emphasis is scarce: not everything is bold, colored, or boxed.

## Typography
- [ ] Body text sits at a comfortable measure (around 45 to 75 characters), never full-width on a wide screen.
- [ ] Type sizes come from one scale. No off-scale one-offs.
- [ ] Leading fits the size: tight on headlines, open on body.
- [ ] Real punctuation: curly quotes, proper apostrophes, a real ellipsis, and a clear range separator ("to", or an en dash only where house style permits).
- [ ] No orphans or widows in headlines. Multi-line titles are balanced.
- [ ] Tabular numerals anywhere numbers align or change in place.

## Color and contrast
- [ ] Authored in a perceptual space; neutrals are tuned, not pure gray.
- [ ] Body text meets the contrast target; nothing critical relies on color alone.
- [ ] One accent, spent on what matters. Dark mode carries depth by lightness, not black.
- [ ] The hierarchy still reads in grayscale.

## Space and alignment
- [ ] All spacing comes from one scale. No stray off-grid values.
- [ ] Space, not borders, carries most grouping. Space above a heading exceeds space below it.
- [ ] Everything aligns to a shared edge. Optical alignment overrides mechanical where they disagree.
- [ ] The layout breathes at the outer margins; content is not jammed to the edge.

## Optical detail
- [ ] Nested corners are concentric (inner radius = outer minus padding).
- [ ] Icons and glyphs are optically centered, not box-centered. Any triangle or circle is nudged and overshot as needed.
- [ ] Separators are hairlines, not hard gray lines.
- [ ] One consistent light source; every shadow falls the same way.
- [ ] Shadows are soft, layered, and tinted, not a single default blur.

## Motion and feel
- [ ] Nothing snaps. Every state change is eased.
- [ ] Entrances decelerate (ease-out); durations sit under 400ms for anything the user waits on.
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
- [ ] Works from a 360px phone to a large display; type is fluid, not stepped.
- [ ] Touch targets are at least 44px; hover is never the only way to reach something.
- [ ] Safe areas respected; nothing critical under a notch or gesture bar.
- [ ] Survives 200 percent zoom and reflows to one column without horizontal scroll.
- [ ] Behaves correctly for the actual input (touch, pointer, keyboard, remote), not just the width.

## The final pass
- [ ] Zero AI-slop tells (see ai_design_slop): no default-sans-everywhere, purple-to-blue gradient, gradient text, identical card grid, or unjustified glass.
- [ ] Remove one more thing. If nothing was lost, it stays removed.
- [ ] Every decision on screen has a reason. Nothing is there by default or by accident.
