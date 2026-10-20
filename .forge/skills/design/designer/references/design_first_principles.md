# Design First Principles

> The mental model that separates elite design from competent design, and both from AI slop. Read this first. Everything else is application.

## Contents
- The one belief
- Dieter Rams as the baseline
- The perception laws that actually change decisions
- Clarity over cleverness
- Restraint and editing
- Why AI design looks like AI design
- The taste references worth studying

## The one belief

Design is decision-making made visible. Every pixel is either intentional or it is an accident someone will feel. The elite designer is not more artistic than the average one. They are more deliberate. They make a hundred small correct decisions where others make one big flashy one and leave the rest to defaults. Outstanding is the accumulation, not the flourish.

The user came to do a job. The design either helps them do it and feels good in the doing, or it gets in the way while looking busy. Beauty that fights the task is not beauty, it is vanity.

## Dieter Rams as the baseline

Rams' ten principles are not decoration on the wall of a design studio. They are a working filter. Good design is:

1. Innovative, but in service of function, not novelty.
2. Useful. It makes the product work better, not just look better.
3. Aesthetic, because objects we use daily affect how we feel.
4. Understandable. It explains itself. No manual.
5. Unobtrusive. A tool, not a decoration. Restrained, so the user's content leads.
6. Honest. It does not pretend to be more than it is, or promise what it cannot do.
7. Long-lasting. It avoids being fashionable, so it never looks dated.
8. Thorough to the last detail. Nothing is arbitrary. Care is visible under a magnifying glass.
9. Environmentally and cognitively light. It does not waste the user's attention.
10. As little design as possible. Less, but better. Concentrate on the essential.

Points 7, 8, and 10 are where most AI design fails. It chases the fashionable (point 7), leaves the details to defaults (point 8), and adds decoration to look designed (point 10).

## Task fit and bounded evidence

Start with the user's task, not a law or a preferred composition. Record the user, trigger, goal, information needed at the decision point, and what counts as success. For consequential choices, describe frequency, urgency, uncertainty, error consequence, and recovery cost separately. These questions structure judgment; they are not inputs to a validated universal score.

Then make a concrete choice and say what evidence could prove it wrong. Prefer task completion, first-action success, missed information, wrong-action rate, and recovery success over claims that a screen feels simpler. Separate observed product facts from assumptions.

Use perception research as a bounded explanation, not a layout recipe:

- **Proximity and common region** can help show which labels, values, and actions belong together. Use the lightest grouping cue that makes the relationship clear.
- **Fitts' law** describes aimed movement under studied conditions. Keep relevant controls close to the content they affect and make targets forgiving. It does not set one universal pixel size. Meet WCAG 2.2 AA target-size criteria where applicable, and follow platform guidance such as 44 pt or 48 dp only for its named platform and context.
- **Hick-Hyman law** models choice reaction time in studied choice tasks. It does not mean fewer options are always faster. Group by user goal and reduce irrelevant choices, but preserve legitimate alternatives users need to compare.
- **Miller's 7±2** is not a cap on fields, tabs, or menu items. Group by task structure; keep status and context visible when users must compare them.
- **Jakob's law** supports familiar patterns in familiar product tasks. Use convention to reduce relearning, while respecting the product's actual workflow.
- **Visual hierarchy** is a set of salience cues, not a guaranteed eye path. Emphasize the useful next action and status, then check first-action success with representative users or tasks.
- **Aesthetic-usability findings** do not excuse broken flows. Craft earns its place when it supports legibility, orientation, trust, or the intended brand.
- **Response feedback** should acknowledge an action promptly. A 400ms figure is a rough historical guideline, not a universal pass line; perceived wait depends on task, feedback, and system response. Give honest progress when work takes longer.
- **Progressive disclosure** helps when detail is advanced or rare and can be found before it is needed. It harms comparison, discovery, or urgent action when the hidden choice matters now.

Do not apply a “one primary CTA,” fixed chrome ratio, card grid, or color allocation formula across all surfaces. A marketing page may benefit from a clear next step; an operations workspace may need several equally valid dispositions. Choose based on task and evidence. For deeper evidence limits, see the UX research note and the operational sequence in the skill.

## Clarity over cleverness

The user's brief said it: a don't-make-me-think design. Clarity is not the absence of creativity. It is creativity aimed at the right target. A layout so novel the user cannot find the button is not brave, it is broken. Put the creativity in the details and the feel, and keep the structure legible. The most sophisticated designers make the complex look obvious. The junior ones make the obvious look complex.

## Restraint and editing

The first draft is always too much. Editing is the skill. Remove an element and ask whether anything was actually lost. Usually not. Remove a color, a weight, a border, a shadow, a word. Keep removing until the design starts to break, then add back the one thing that broke it. What remains is the design. Whitespace is not wasted space, it is the room that makes the rest legible and calm.

## Why AI design looks like AI design

It reaches for the median of its training data: the same neutral sans, the same purple gradient, the same three-card grid, the same centered hero. It adds decoration to signal effort (grid backgrounds, eyebrow labels, stat rows) instead of making structural decisions. It never sweats the optical details because they are invisible in a screenshot but felt in use. The cure is not more decoration. It is intention, restraint, and the subconscious craft layer.

## The taste references worth studying

Study the people and products that got it right, and ask why, not what. Rams and Braun for restraint. Josef Muller-Brockmann and the Swiss school for grid and hierarchy. Massimo Vignelli for discipline and timelessness. Paul Rand for the single strong idea. In software: the craft of Stripe, Linear, and Things for detail; Apple's Human Interface Guidelines for input-appropriate behavior; Teenage Engineering for personality with restraint. Do not copy their surface. Absorb the discipline underneath.
