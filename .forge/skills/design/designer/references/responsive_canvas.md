# Responsive Canvas

> A phone is not a small laptop, and a TV is not a big one. Each canvas has its own input, viewing distance, and posture. The design must be right for the surface it lands on, from a 360px phone in one hand to a wall-sized display across the room. Fluid, input-appropriate, and tested at the edges.

## Contents
- Design for input, not just width
- Fluid over fixed
- Content-driven breakpoints
- Touch: targets, thumbs, and gestures
- Pointer: precision and hover
- The 10-foot canvas: TV and remotes
- Large screens: do not just stretch
- Safe areas and notches
- Zoom, reflow, and orientation
- The test matrix

## Design for input, not just width

Screen width is the crude signal. The real question is how the user points at things. Query the input directly.

- `@media (hover: hover) and (pointer: fine)` is a mouse or trackpad: hover states apply, targets can be small and dense.
- `@media (hover: none) and (pointer: coarse)` is touch: no hover, larger targets, gesture support.
- A large tablet may have coarse touch input; a small laptop has fine pointer input. Do not infer input from size. A hover-only affordance on a touch device is invisible and broken.

## Fluid over fixed

- Type scales fluidly with `clamp(min, preferred-with-vw, max)` so headings grow smoothly between breakpoints instead of jumping. Set a floor so text never gets too small and a ceiling so it never gets absurd on wide screens.
- Space and layout flex with the viewport and the container. Fixed pixel widths that only change at three breakpoints leave awkward dead zones between them.
- **Container queries over viewport queries for components.** A card should adapt to the width of its container, not the window, so the same component works in a sidebar, a grid, and a full-width hero without bespoke breakpoints. This is the modern default for reusable components.
- Use intrinsic layout patterns that wrap and redistribute on their own (flexible grids that fit as many columns as will fit, sidebars that collapse when space runs out) so the layout responds continuously rather than at hard steps.

## Content-driven breakpoints

- Add a breakpoint where the content breaks, not at device names. When a line of text passes its comfortable measure, or a row of items gets too cramped, that is the breakpoint. Chasing specific device widths is a losing game; there are too many.
- Design mobile-first: start from the smallest canvas where every decision about priority is forced, then let the layout earn more columns and air as space appears. Adding constraints later is harder than adding room.

## Touch: targets, thumbs, and gestures

- Minimum touch target 44 by 44px (iOS) or 48 by 48dp (Android), even when the visible icon is smaller; expand the hit area beyond the glyph. Space targets apart so fat fingers do not hit the wrong one.
- Respect the thumb. On a large phone, the top corners are hard to reach one-handed. Put primary actions within thumb reach, often a bottom bar, not a top-right corner.
- Support the platform gestures (swipe back, pull to refresh, swipe to dismiss) and do not collide with them. A horizontal carousel inside a swipe-to-dismiss sheet fights the user.
- Provide press feedback, since there is no hover. Every tappable thing needs a visible pressed state. See motion_and_feel.

## Pointer: precision and hover

- With a fine pointer you can use hover to reveal, smaller and denser targets, right-click context, and precise drag. Reward the precision, but never make essential actions hover-only, because the same layout may load on touch.
- Keyboard is a first-class pointer substitute on this canvas. Full keyboard navigation, visible focus, and shortcuts for power users belong here. See motion_and_feel for focus craft.

## The 10-foot canvas: TV and remotes

- Viewing distance is meters, not centimeters. Everything scales up: larger type, heavier weights, more spacing, fewer elements per screen.
- Input is a directional remote, not a pointer. Design explicit focus navigation: a clearly visible focused element, logical up/down/left/right order, and a strong focus treatment (scale, glow, or border) far bolder than a desktop focus ring.
- Respect overscan. Older TVs crop the edges; keep important content within a safe margin from the screen edge (roughly 5 percent).
- High contrast and generous spacing matter more; the viewer cannot lean in to read fine print.

## Large screens: do not just stretch

- A 2560px display is not a reason to run body text 2000px wide. Cap the reading measure and use the extra space for margin, a second column, or persistent navigation, not for stretched lines. See typographic_system on measure.
- Center or constrain content to a max width, then decide deliberately what fills the surrounding space. Empty margin is a valid, calm choice; stretched content is not.
- Multi-column and master-detail layouts earn their place on wide screens, where a phone would stack them.

## Safe areas and notches

- Honor device safe areas with `env(safe-area-inset-*)`. Fixed headers, footers, and bottom bars must not sit under the notch, the status bar, or the home-gesture indicator.
- Full-bleed backgrounds extend under the safe area; interactive content and text stay inside it.

## Zoom, reflow, and orientation

- The layout must survive 200 percent browser zoom and reflow to a single column at 400 percent without horizontal scrolling or clipped content. This is both an accessibility requirement and a stress test that exposes brittle fixed layouts.
- Support both orientations where the device rotates. A form that only works in portrait, or a video tool that assumes landscape, fails half its users. Reflow, do not letterbox, unless the content genuinely demands one orientation.
- Account for foldables and split-screen: the viewport can be unusually narrow or tall, or change mid-session. Fluid layouts handle this for free; fixed ones break.

## The test matrix

Before calling a responsive design done, verify it on each real canvas, not just by dragging the window:

- 360px phone, portrait and landscape, touch, with the on-screen keyboard open.
- Tablet, both orientations, touch and pointer.
- Laptop and a large desktop display, pointer and keyboard.
- 200 percent zoom and a screen reader pass.
- If in scope, a TV with remote focus navigation.
- The narrow and wide states of every reusable component in its container.
