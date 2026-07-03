# Refinement Moves: a vocabulary for changing a design on purpose

> "Make it better" is not a direction. These are the named moves a design goes through after the first draft. Pick the move that matches the diagnosis, and apply one at a time so you can see what each did.

Each move is a single directional intent. State which one you are making and why before you touch the design. Applying several at once means you cannot tell which change helped.

## Direction: intensity

- **Bolder**: the design is safe and forgettable. Increase visual interest: stronger type contrast, a committed color, more decisive spacing. Use when a brand-register surface reads as generic. Do not sacrifice legibility to do it.
- **Quieter**: the design is loud and tiring. Reduce intensity: fewer accents, calmer color, more whitespace. Use when a product-register surface fights the user for attention.
- **Distill**: the design is cluttered with elements that do not earn their place. Strip to the essential. Remove a control, a divider, a label, and check whether anything was lost. Usually nothing was.

## Direction: polish

- **Polish**: the design is right in concept but rough in execution. Fix alignment, unify spacing to the scale, tighten inconsistent radii and weights, correct optical misalignments. The final pass before shipping.
- **Layout**: the structure itself is weak. Fix rhythm, hierarchy, and spacing. Address cramped padding, monotonous grids, and a flat visual order where nothing leads.
- **Typeset**: the words are set poorly. Fix the type scale, weights, line length, and pairing so the hierarchy is legible at a glance.

## Direction: resilience

- **Harden**: the design only survives the demo. Design the states it will actually meet: long text that overflows, empty data, error and loading, the translated string that is 40% longer, the edge that breaks the layout.
- **Adapt**: the design assumes one screen. Make it hold across sizes and contexts: breakpoints, fluid spacing, touch targets no smaller than 44 by 44, and no forced horizontal scroll on mobile.
- **Clarify**: the interface is understood only by its author. Fix labels, error messages, and instructions so a first-time user knows what each control does and what went wrong.

## Direction: character

- **Colorize**: a monochrome UI needs strategic color to guide the eye and carry meaning. Add color where it does a job (state, hierarchy, emphasis), not everywhere.
- **Animate**: static elements should acknowledge the user. Add purposeful motion: entrance, hover, and click feedback that confirms actions. Respect reduced-motion preferences. Motion that delays the user is a bug, not a flourish.
- **Delight**: the design works but feels merely functional. Add a moment of personality where it will be noticed and will not get in the way: a considered empty state, a small reward on completion. One earned touch beats ten scattered ones.

## The discipline

Diagnose before you move. "This landing page is forgettable" points to bolder. "This dashboard is exhausting" points to quieter. "This breaks with real data" points to harden. Making the wrong move confidently is how a design gets worse while everyone stays busy.
