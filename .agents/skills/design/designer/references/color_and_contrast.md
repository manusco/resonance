# Color and Contrast

> Color affects legibility, grouping, and meaning. Choose colors in the representation your system supports, then evaluate the actual contrast, semantic roles, and task hierarchy.

## Contents
- Choose a workable color representation
- Contrast as one hierarchy cue
- WCAG 2.2 AA and supplementary APCA checks
- Choose neutral colors from the product context
- Building a scale
- Dark mode by surface roles and contrast
- Accent use guided by hierarchy and product identity
- Color as meaning

## Choose a workable color representation

HSL and hex do not represent perceptual lightness directly. OKLCH can help explore perceptual palette steps, but it is not required. Use the format supported by the product and tooling; judge the rendered colors rather than the notation. Hue, display, background, and viewing conditions affect how a color reads, so check actual combinations and contrast.

OKLCH (lightness, chroma, hue) is designed to make perceptual color relationships easier to explore. A declaration such as `oklch(0.62 0.19 265)` is one possible authoring format. Gamut support and existing tokens may favor another representation. Keep conformance checks on the final rendered colors.

## Contrast as one hierarchy cue

Contrast is the primary tool of hierarchy, and it is a budget you spend. Contrast is one cue among size, weight, position, grouping, and spacing. Emphasis follows the task: status and action may need equal visibility when both are needed to decide safely. Contrast is not only dark-vs-light. You have several channels, and elite design uses them together, deliberately:

- **Lightness contrast** against the background. The strongest and most accessible channel. The heading, status, or action that matters at the current task moment should read clearly.
- **Size contrast.** Bigger reads as more important before the eye even resolves the text.
- **Weight contrast.** A heavier weight pulls rank without changing size or color.
- **Color contrast.** Use saturation to distinguish relevant emphasis without muting status or categories users need to compare.
- **Spatial contrast.** More space around an element raises its status. Crowding lowers it.

Use contrast to distinguish the task, current status, and actions according to their roles. One element may lead, or several related elements may need comparable prominence for a safe decision. Reduce competing decoration; do not mute information the user needs together.

## WCAG 2.2 AA and supplementary APCA checks

- Meet WCAG 2.2 AA contrast requirements: generally 4.5:1 for normal text and 3:1 for large text, with the standard exceptions applied only within their scope. Check non-text contrast where required.
- APCA may supplement design exploration, especially for polarity and perceptual legibility, but it does not replace WCAG conformance. Do not prescribe fixed APCA targets as normative pass criteria.
- Never convey meaning by color alone. A red border with no icon or label fails color-blind users and anyone in a hurry. Pair color with text, an icon, or a shape.

## Choose neutral colors from the product context

Achromatic grays, tinted grays, warm neutrals, and cool neutrals can all fit a product. Choose from the brand, adjacent colors, content, platform, and desired contrast; no neutral temperature is mandatory.

- If a tinted neutral supports the palette, keep related surface and text roles coherent. A low-chroma OKLCH value is one way to explore that direction, not a required range.
- Pure black or white can be appropriate for contrast, OLED displays, brand expression, or a deliberately high-contrast theme. Check the actual hierarchy and applicable contrast requirements.

## Building a scale

- A ramp can make repeated surfaces and text levels easier to tune. Choose the number and spacing of steps from the system and rendered results.
- Keep functional colors distinguishable for the tasks that use them; they need not share identical lightness steps when that harms their meaning or legibility.
- Semantic tokens can help coordinate roles such as surface, border, text, status, and accent. Use the product's existing token model where one exists.

## Dark mode by surface roles and contrast

Dark mode needs its own tested color relationships. It may use near-black, pure black, or another surface color when that fits the product and device.

- Check text, controls, boundaries, and states on the actual dark surface, including pure black where used.
- Use whichever cues fit the chosen system to distinguish layers: surface color, borders, shadows, or combinations. No elevation treatment is mandatory.
- Retune accent and status colors for legibility and meaning on the dark surface; do not apply a fixed saturation shift.
- Establish text levels that preserve required contrast and the intended hierarchy.

## Restraint and semantic color

A restrained accent palette often keeps emphasis clear, but there is no universal accent count. Assign colors clear semantic roles and preserve distinctions needed to compare status or categories. Check that color is not the only signal.

## Color as meaning

- Preserve familiar functional color associations where the product and audience rely on them. If the mapping differs, make state clear through labels, shapes, or other non-color cues.
- Separate brand and status roles when they would otherwise be confused; choose tokens that fit the existing system.
- Test the whole palette in grayscale. If the hierarchy survives without hue, the design does not depend on color to be understood, which is exactly where you want to be.
