# Color and Contrast

> Color is where most designs quietly go wrong, because the tools lie. HSL says two colors are equally bright when the eye sees one as far darker. Work in a perceptual space, build contrast on purpose, and treat emphasis as a scarce resource.

## Contents
- Work in OKLCH, not HSL
- The contrast hierarchy
- Measuring contrast: APCA over WCAG 2 ratios
- Neutrals are never pure gray
- Building a scale
- Dark mode by lightness, not black
- Restraint: one accent, earned
- Color as meaning

## Work in OKLCH, not HSL

HSL and hex are not perceptually uniform. Fix the lightness at 50 percent and sweep the hue, and yellow looks far brighter than blue, though the number says they match. This is why palettes built in HSL have some steps that pop and others that sink.

OKLCH (lightness, chroma, hue) is perceptually uniform. Equal lightness looks equal, so a scale steps evenly, and you can shift hue without the brightness lurching. Author color in OKLCH: `oklch(0.62 0.19 265)`. It also reaches colors outside the old sRGB gamut for wide-gamut displays. When you need a single control that behaves, lightness in OKLCH is it.

## The contrast hierarchy

Contrast is the primary tool of hierarchy, and it is a budget you spend. The most important element gets the most contrast against its surroundings; everything else steps down. Contrast is not only dark-vs-light. You have several channels, and elite design uses them together, deliberately:

- **Lightness contrast** against the background. The strongest and most accessible channel. The primary heading and the primary action win here.
- **Size contrast.** Bigger reads as more important before the eye even resolves the text.
- **Weight contrast.** A heavier weight pulls rank without changing size or color.
- **Color contrast.** The one accent hue marks the one thing you want acted on. Saturation draws the eye; mute everything that is not the point.
- **Spatial contrast.** More space around an element raises its status. Crowding lowers it.

The discipline: decide the single most important thing on the screen, give it the contrast lead across these channels, and actively de-emphasize the rest. Emphasis by de-emphasis. If three things are bold, none is.

## Measuring contrast: APCA over WCAG 2 ratios

- The WCAG 2 ratio (4.5:1 for body, 3:1 for large text) is the legal floor. Meet it, but know it is a crude model that misjudges especially dark themes and mid-tones.
- APCA (the model behind WCAG 3) accounts for how the eye actually reads text against a background, including polarity (dark-on-light vs light-on-dark). Prefer it when tuning real legibility. Aim for an Lc around 90 for body text, 75 for larger or secondary text, 60 for large or disabled.
- Never convey meaning by color alone. A red border with no icon or label fails color-blind users and anyone in a hurry. Pair color with text, an icon, or a shape.

## Neutrals are never pure gray

Pure gray (equal R, G, B) looks dead and slightly dirty next to any colored UI. Elite neutrals carry a temperature: a whisper of the brand hue, or a cool blue-gray or warm taupe-gray chosen on purpose.

- Tint your grays toward the brand or toward a deliberate temperature. In OKLCH, hold a low chroma (around 0.01 to 0.03) at the brand hue across the neutral ramp.
- Warm neutrals feel human and inviting; cool neutrals feel technical and calm. Pick one and stay consistent.
- Text is rarely pure black. Near-black (around oklch 0.2 to 0.25) on white reads softer and more refined and cuts the harsh vibration of `#000` on `#fff`.

## Building a scale

- Build a neutral ramp of steps from background to strongest text, evenly spaced in OKLCH lightness (for example 12 steps from near-white to near-black). Even lightness steps give even visual jumps.
- Give each functional color (primary, success, warning, danger, info) the same set of lightness steps, so a success and a danger of the "same" level match in weight.
- Define semantic tokens on top of the ramp: surface, surface-raised, border, text, text-muted, accent. Components reference the semantic tokens, never the raw ramp. This is what lets a theme swap cleanly.

## Dark mode by lightness, not black

Dark mode is not inverting the palette and it is not pure black.

- Base surface is a dark near-neutral (around oklch 0.16 to 0.20), not `#000`. Pure black makes shadows invisible and edges vibrate.
- **Elevation is lightness, not shadow.** In light mode, raised surfaces cast shadows. In dark mode, raised surfaces get lighter. A modal sits a lightness step or two above the page. Shadows barely read on dark, so lightness carries depth.
- Reduce saturation in dark mode. Colors that sang on white glare on dark. Drop chroma and raise lightness slightly so the accent stays legible without buzzing.
- Do not use your lightest text at full strength for everything; a near-white primary and a dimmer secondary preserve hierarchy, same as light mode.

## Restraint: one accent, earned

One accent color does more work than five. The accent means "this is the thing to act on or notice." Spend it on the primary action, the active state, the key data point. The moment a second and third accent appear with equal strength, the eye has nowhere to land and the isolation effect is gone. If you need more than one accent, they must occupy different jobs (brand accent vs status colors), never compete for the same emphasis.

## Color as meaning

- Keep functional colors conventional where users rely on them: red for destructive and error, green for success, amber for warning. Novelty here costs comprehension.
- Reserve the brand accent for brand moments and primary actions, and keep it out of status roles so the two never blur.
- Test the whole palette in grayscale. If the hierarchy survives without hue, the design does not depend on color to be understood, which is exactly where you want to be.
