# Motion and Feel

> Motion is where an interface stops being a picture and starts being a place. Done with physics and intent, it orients, confirms, and delights. Done as decoration, it annoys and delays. The line between the two is easing, timing, and restraint.

## Contents
- Nothing snaps: easing is mandatory
- The easing curves that feel natural
- Spring physics
- Duration budgets by distance
- Hover, done with care
- Focus that looks designed
- Press and active feedback
- Feedback timing and perceived speed
- Choreography and continuity
- Scroll, used tastefully
- Haptics and touch feel
- Reduced motion

## Nothing snaps: easing is mandatory

Any state change that jumps instantly reads as broken or cheap. Every transition of color, position, size, or opacity carries an easing curve. This one habit separates polished from amateur more than any single effect.

## The easing curves that feel natural

Linear motion looks robotic because nothing in the physical world moves at a constant speed. Natural motion accelerates and decelerates.

- **Ease-out for entrances and most UI.** Fast start, gentle settle. Elements arriving on screen decelerate into place, the way a real object does. This is the default for opening, revealing, and moving toward the user. A curve like `cubic-bezier(0.16, 1, 0.3, 1)` feels expensive.
- **Ease-in for exits.** Accelerate away. Things leaving the screen speed up as they go.
- **Ease-in-out for movement between two on-screen points.** Symmetric, smooth at both ends.
- **Avoid the browser default `ease`.** It is weak. Author your own curves and store them as tokens (`--ease-out`, `--ease-spring`).
- Standard-issue linear or the default `ease` on everything is a tell that motion was an afterthought.

## Spring physics

For anything the user grabs, drags, or toggles, springs feel more alive than fixed-duration curves because they carry momentum and settle naturally. A spring is defined by stiffness, damping, and mass, not a duration. Slight overshoot on a spring (a toggle that nudges just past and settles) reads as physical and satisfying. Keep overshoot subtle; a bouncy castle is not the goal. Use springs for drag, swipe, toggle, and gestural motion; use eased durations for discrete transitions like a fade or a color change.

## Duration budgets by distance

Duration scales with how far and how big the motion is. A small element moving a short distance should be quick; a full-screen transition can take longer without feeling slow.

- Micro feedback (hover, small state changes): 100 to 150ms.
- Standard transitions (dropdowns, toggles, small moves): 150 to 250ms.
- Larger moves (modals, drawers, page-level): 250 to 400ms.
- Rarely past 400ms for anything the user is waiting on. Past the Doherty threshold, motion stops feeling responsive and starts feeling like a wait.
- Exits are often a touch faster than entrances; the user has decided, so get out of the way.

## Hover, done with care

Hover is a reward for attention on pointer devices. It must never exist alone (touch has no hover) and never shift layout.

- Give hover an eased transition in and a slightly slower one out, so it feels intentional, not twitchy.
- Change something real: a subtle lift (a small translate-y up with a tuned shadow), a background shift, an icon that animates, a border that warms. Small and specific beats large and generic.
- Never use `transform: scale()` or a border-width change that reflows neighbors. Layout-shifting hover is a classic amateur mistake. Animate transform and opacity, which do not trigger layout.
- Hover reveals affordance; it does not hide critical information behind itself. Anything essential must be reachable without hover, because touch users cannot hover at all.

## Focus that looks designed

- Keyboard focus is not the browser's default blue outline unless you have chosen to keep it. Design a focus ring that matches the system: a clear, high-contrast ring with a small offset so it never touches the element's own edge.
- Use `:focus-visible`, so the ring shows for keyboard users and not on every mouse click. A beautiful, always-correct focus state is a mark of care and a requirement for accessibility, not a tradeoff between them.

## Press and active feedback

- The press state fires the instant the finger or mouse goes down, under 100ms, so the interface feels directly connected to the input. Waiting until release to react feels laggy.
- A small compression on press (a slight scale down to around 0.97, or a downward nudge) reads as a physical button taking the push. Release springs it back.
- On touch, the press state doubles as the hover affordance, since there is no hover. Make sure pressed styling exists and is visible under a fingertip.

## Feedback timing and perceived speed

- Every action gets acknowledged immediately, even if the result takes time. A button that does nothing for 300ms feels broken; a button that shows a pressed or loading state instantly feels fast even if the network is slow.
- Optimistic UI: show the successful result immediately and reconcile when the server confirms. The like fills the moment it is tapped. Roll back gracefully if it fails.
- Reserve space for content that is loading so nothing jumps when it arrives. Layout shift is the opposite of polish. Use skeletons that match the real content's shape, or a calm spinner for short waits, and prefer showing partial real content over a full-screen loader.
- Under the 400ms Doherty threshold, an interaction feels instant. Design to stay under it, and where you cannot, fill the wait with honest progress.

## Choreography and continuity

- When several elements appear together, stagger them by a small delay (around 30 to 60ms each) so they cascade instead of popping as a block. Restraint matters; a long stagger becomes a wait.
- Maintain spatial continuity. When a card opens into a detail view, the shared element should move and grow into place rather than the old view vanishing and a new one fading in. Continuity tells the user where they are and where they came from.
- Motion should have a consistent direction logic across the product: forward navigation moves one way, back moves the other, so the space feels coherent.

## Scroll, used tastefully

- Scroll-triggered reveals can bring a page to life, but restraint is the whole game. A gentle fade-and-rise as sections enter the viewport feels alive; the same effect on every element, delayed, makes the page feel slow and gimmicky.
- Reveal once, near the point the element enters view, and keep the motion small. Never hold content hostage behind a heavy scroll animation the user has to wait out.
- Parallax and scroll-driven effects belong to brand-register moments, used sparingly. In a product, scrolling should be fast, native, and momentum-preserving, not hijacked.
- Respect native scroll physics. Fighting the platform's momentum or overscroll feel is immediately noticeable and unpleasant.

## Haptics and touch feel

- On devices that support it, a light haptic tap on a meaningful action (a successful toggle, a completed swipe, a picker landing on a value) makes the interface feel physical. Use it for confirmation, sparingly, never as constant buzz.
- Match the haptic weight to the action: a light tick for a small selection, a firmer tap for a commit or an error.

## Reduced motion

- Honor `prefers-reduced-motion`. For users who request it, replace movement with a simple opacity change or no transition at all, and cut parallax, autoplay, and large motion entirely.
- Reduced motion is not no feedback. Keep the instant state acknowledgment; just remove the travel. The interface stays responsive and clear, only calmer.
