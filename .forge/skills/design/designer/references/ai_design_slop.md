# AI Design Slop: defaults to question

> Familiar patterns become generic when chosen without regard to the product, brand, and task. Use this catalog to spot unexamined defaults, then keep or replace each one for a stated reason.

Use this as a review prompt, not a ban list. Each item describes a common reflex. Check the actual context before deciding whether it fits.

## Typography tells

- **Unexamined defaults**: reaching for a neutral system sans (including Inter), a purple gradient, or familiar component patterns without checking the product, brand, and task. These are not forbidden choices; they become slop when they are automatic and unsupported. Choose and explain what fits.
- **One weight, one size, no hierarchy**: body text and headings a hair apart, so nothing leads the eye. Set a real typographic scale.
- **Center-aligned everything**: long paragraphs and multi-item lists centered, which destroys the reading edge. Left-align body content.

## Color tells

- **The purple-to-blue gradient**: a familiar hero background or button fill. Keep it only when it fits an established palette or a clear brand purpose; otherwise choose color from the product system.
- **Gradient text**: headline text filled with a color gradient. Check legibility and whether the effect serves the brand; do not use it just to make a generic headline look designed.
- **Unrelated accent colors**: bright colors with no distinct role compete. Give each color a semantic job; preserve the colors needed to compare categories and status.
- **Black-and-white pairings without context checks**: `#000` on `#fff` or a pure-black dark surface can fit the product, device, brand, and contrast target. Test the actual hierarchy and surface separation; do not reject these values by default.
- **The premium-consumer default palette**: reaching for beige and cream with a brass, clay, or oxblood accent and espresso text the moment a brief says wellness, artisan, or cookware. It is a real and tasteful palette, which is exactly why the model overuses it. Earn it, or rotate off it.

## Layout and surface tells

- **Card grid by reflex**: unrelated content forced into identical cards because the template suggests it. Cards and grids are valid when items are independent summaries; preserve a table or aligned rows when the task depends on comparison.
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

Ask three questions of any generated screen. If the answer points to an unexamined choice, explain it or iterate.

1. Could I swap in any competitor's content and have this still look right? (Too generic.)
2. Does it use a familiar font, gradient, or card grid without evidence that it fits this product and task? (Unexamined.)
3. If I removed every decorative flourish, would anything of the design remain? (Decoration standing in for structure.)
