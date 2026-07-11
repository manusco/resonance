# AI Design Slop: the visual tells to refuse

> Every model trained on the same screenshots reaches for the same defaults. The result is instantly recognizable as machine-made. This is the catalog of those reflexes, so you can refuse them on sight.

Run this as a checklist against any generated UI. Each item is a concrete pattern, not a vibe. If the design trips one, it is not "modern", it is the median. Name a reason to keep it or replace it.

## Typography tells

- **Default sans everywhere**: reaching for the same neutral system sans (Inter and its lookalikes) for every project regardless of brand. A font choice that expresses nothing is a decision skipped. Choose a face that fits the register.
- **One weight, one size, no hierarchy**: body text and headings a hair apart, so nothing leads the eye. Set a real typographic scale.
- **Center-aligned everything**: long paragraphs and multi-item lists centered, which destroys the reading edge. Left-align body content.

## Color tells

- **The purple-to-blue gradient**: the reflex hero background and button fill. Instantly reads as AI default. Commit to a real palette instead.
- **Gradient text**: headline text filled with a color gradient. Almost always a tell, rarely legible, never necessary.
- **Rainbow of accent colors**: five unrelated bright colors because each felt nice alone. Pick one accent and earn any second.
- **Pure black on pure white, or pure black in dark mode**: `#000` on `#fff` strains the eye; `#000` dark-mode surfaces crush depth. Use near-black and layered near-dark surfaces.
- **The premium-consumer default palette**: reaching for beige and cream with a brass, clay, or oxblood accent and espresso text the moment a brief says wellness, artisan, or cookware. It is a real and tasteful palette, which is exactly why the model overuses it. Earn it, or rotate off it.

## Layout and surface tells

- **Identical card grids**: every piece of content forced into the same rounded rectangle, three across, forever. Vary weight and rhythm; not everything is a card.
- **Glassmorphism by default**: frosted translucent panels applied with no reason, hurting contrast and legibility. Use only when depth genuinely helps.
- **The side-stripe accent border**: a colored left border glued onto every callout and card. A dated template signature.
- **Over-rounded corners**: pill-shaped everything, giant radii on containers that should feel structural. Match radius to the surface's job.
- **Decorative grid or dot backgrounds**: faint graph-paper or dotted textures behind hero sections as filler. Usually noise pretending to be design.
- **The eyebrow on every section**: a tiny uppercase label above every single heading, often numbered (`001 - Capabilities`, `02 / Features`). Once is a pattern, everywhere is a tic.
- **The hero-metric template**: the same three big stat numbers in a row ("10k+ users, 99.9% uptime, 24/7"). Reads as filler when unearned.
- **Fake product UI as decoration**: a fabricated dashboard, chart, or app screenshot built from divs purely to fill the hero, showing nothing real. Decoration pretending to be product, and a quiet honesty violation the moment a user notices it does nothing.
- **Version labels and status theater in the hero**: `V0.6`, `BETA`, a green `Online` dot, a live-looking counter, none of it wired to anything. Borrowed signals of a real product, faked.
- **The weather-and-locale strip**: a header decoration showing a city, a time, a temperature, or coordinates for texture, on a page that has nothing to do with any of them.
- **The hero-bottom decoration bar**: a row of spaced uppercase words across the bottom of the hero (`BRAND. MOTION. SPATIAL.`), or a fake scroll cue, added because the space felt empty. Filler in a typographic costume.

## Interaction tells

- **Emoji as UI icons**: emoji standing in for navigation, settings, or status. Font-dependent and unprofessional. Use real icons.
- **Instant state snaps**: hover and active states that jump in 0ms, or hovers that shift surrounding layout. Transition state, and never reflow neighbors on hover.
- **No empty, loading, or error state**: only the happy path designed, so the real product looks broken the moment data is absent. Design the shadow states first.

## The AI slop test

Ask three questions of any generated screen. If the honest answer to any is yes, iterate before shipping.

1. Could I swap in any competitor's content and have this still look right? (Too generic.)
2. Does it lean on a default the model reaches for by reflex (default sans, purple gradient, card grid)? (Unexamined.)
3. If I removed every decorative flourish, would anything of the design remain? (Decoration standing in for structure.)
