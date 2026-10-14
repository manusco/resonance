# Motion and Feel

> Motion is where an interface stops being a picture and starts being a place. Done with physics and intent, it orients, confirms, and delights. Done as decoration, it annoys and delays. The line between the two is easing, timing, and restraint.

## Contents
- Should this animate at all?
- Motion vocabulary by job
- Nothing snaps: easing is mandatory
- The easing curves that feel natural
- Spring physics
- Gesture physics: handoff and interruption
- Timing by interaction and user wait
- Hover, done with care
- Focus that looks designed
- Press and active feedback
- Feedback timing and perceived speed
- Choreography and continuity
- Scroll, used tastefully
- Haptics and touch feel
- Reduced motion

## Should this animate at all?

Before easing or duration, ask whether the change should animate at all. Motion is not free; on the wrong action it is drag.

- A frequently repeated action may work better without an animation. For example, a command palette used many times a day should open promptly; use motion only if it helps orientation without slowing the task.
- A keyboard-initiated action gets no animation. The keyboard user is optimizing for speed, and motion is in the way.
- Animate the changes the user needs to follow (something moved, appeared, or turned into something else), not the ones they just want done. When in doubt, cut it. Respecting the frequent user is faster than delighting the first-time one.

## Motion vocabulary by job

Choose motion by the job it does, not by the raw number or effect. A premium system has a small vocabulary that repeats with intent, so users learn how the product moves.

- **Feedback**: hover, focus, press, selected, disabled. Keep it tiny and immediate: color, opacity, shadow, a small transform, or a clear focus ring on explicit properties.
- **Reveal**: dropdowns, popovers, panels, tooltips. Anchor the motion to the trigger when there is one, use opacity plus a small scale or translate, and make close faster than open.
- **Navigation**: list to detail, step to step, forward and back. Preserve direction logic so the space feels stable. Symmetric movement between two on-screen states usually wants the same duration both ways.
- **Loading**: skeletons, streamed content, partial data. Reserve space first, then reveal real content without layout shift. A loader must explain wait, not decorate it.
- **Error**: invalid field, failed action, conflict. Use restrained motion to draw attention once, pair it with text, and let the user continue without fighting a repeated shake.
- **Confirmation**: saved, paid, sent, completed. Spend the most character here, but only after a real user win. Keep it short, replayable, and easy to skip through reduced motion.

When motion is useful, tune the properties that matter for that interaction, such as duration, easing, distance, scale, or blur. Match them to intent. A close can be faster than an open; a text swap can be short while a confirmation gets more time. Do not add an effect only because it looks good in isolation.

## When motion helps, choose easing with intent

An abrupt change can be appropriate for frequent actions, keyboard-driven work, reduced-motion preferences, or instant state feedback. Animate only when movement helps users follow a change; when used, choose easing that fits the transition.

## Easing by interaction

Choose easing to clarify how a change relates to the user's action. A reveal may decelerate into place; direct manipulation may track the pointer; a status update may need no travel at all. Linear motion is useful when the visual value should track elapsed time, such as a progress indicator. These are starting patterns, not requirements. Match motion to the product, platform, task, and reduced-motion setting.

A brief scale or fade can help a new surface read as an entrance, but it is optional. Avoid motion that obscures content, delays task completion, or makes the result hard to predict. Choose exit behavior to match the action and give control back promptly.

## Springs and gesture physics

Springs can suit continuous movement, dragging, or snapping between positions when they preserve the user's momentum and make the destination clear. A toggle or discrete control may need a simple state change instead. Match stiffness and settling to the input and platform; avoid bounce that distracts from the task.

For a draggable surface, continue from its current position and release velocity when the motion model supports it. Decide dismissal or snap-back from the gesture, the surface's purpose, and a clear threshold; there is no universal projection formula. If interrupted, continue from the element's current visible state so it does not jump.

## Timing and response

Tune duration to distance, task urgency, platform conventions, and whether users are waiting or following a change. Short feedback often feels responsive, but 100 to 400ms ranges are examples, not pass criteria. A longer transition may suit orientation; a frequent keyboard action may need none. Acknowledge input promptly, preserve control, and show honest progress for longer work.


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

- A visible press state can acknowledge touch or pointer input. Keep feedback prompt and proportional; the exact delay depends on platform and interaction.
- A small compression or color change can make a press legible. Choose feedback that fits the control and does not cause unwanted movement or ambiguity.
- On touch, the press state doubles as the hover affordance, since there is no hover. Make sure pressed styling exists and is visible under a fingertip.

## Feedback timing and perceived speed

- Acknowledge actions promptly, especially while waiting on a server. Use a clear pressed, pending, or loading state when useful; do not imply completion before it is known.
- Optimistic UI: show the successful result immediately and reconcile when the server confirms. The like fills the moment it is tapped. Roll back gracefully if it fails.
- Reserve space for content that is loading so nothing jumps when it arrives. Layout shift is the opposite of polish. Use skeletons that match the real content's shape, or a calm spinner for short waits, and prefer showing partial real content over a full-screen loader.
- Acknowledge input promptly. Treat 400ms as a rough guideline, not a universal threshold. When work takes longer, show honest progress and preserve control.

## Choreography and continuity

- A short stagger can help users follow a coordinated reveal, but immediate display is often better for dense or repeated work. Avoid making users wait for content to appear.
- Maintain spatial continuity. When a card opens into a detail view, the shared element should move and grow into place rather than the old view vanishing and a new one fading in. Continuity tells the user where they are and where they came from.
- Motion should have a consistent direction logic across the product: forward navigation moves one way, back moves the other, so the space feels coherent.
- Anchor a popover or menu to its trigger: it should scale and fade from the `transform-origin` of the control that opened it, not from its own center, so it visibly grows out of the thing you clicked. Modals and full sheets are exempt; they own the screen.

## Scroll, used tastefully

- Scroll-triggered reveals can bring a page to life, but restraint is the whole game. A gentle fade-and-rise as sections enter the viewport feels alive; the same effect on every element, delayed, makes the page feel slow and gimmicky.
- Reveal once, near the point the element enters view, and keep the motion small. Never hold content hostage behind a heavy scroll animation the user has to wait out.
- Parallax and scroll-driven effects belong to brand-register moments, used sparingly. In a product, scrolling should be fast, native, and momentum-preserving, not hijacked.
- Respect native scroll physics. Fighting the platform's momentum or overscroll feel is immediately noticeable and unpleasant.

## Haptics and touch feel

- On devices that support it, a light haptic tap on a meaningful action (a successful toggle, a completed swipe, a picker landing on a value) makes the interface feel physical. Use it for confirmation, sparingly, never as constant buzz.
- Match the haptic weight to the action: a light tick for a small selection, a firmer tap for a commit or an error.
- When an action fires visual, sound, and haptic feedback together, land them on the same frame. Split by even a fraction of a second they read as a glitch; together they read as one physical event.

## Reduced motion

- Honor `prefers-reduced-motion`. For users who request it, replace movement with a simple opacity change or no transition at all, and cut parallax, autoplay, and large motion entirely.
- Reduced motion is not no feedback. Keep the instant state acknowledgment; just remove the travel. The interface stays responsive and clear, only calmer.
