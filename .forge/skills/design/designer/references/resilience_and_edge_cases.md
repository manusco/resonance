# Resilience and Edge Cases

> A design that only survives the demo is not done. Real content is messy, networks fail, text translates longer, and users do the unexpected. The basics have to be right and the edges have to be designed, not discovered in production.

## Contents
- Design the shadow states first
- The full state matrix
- Text that does not cooperate
- Data: none, one, and far too much
- Network and time
- Internationalization and direction
- Accessibility as resilience

## Design the shadow states first

Design the empty, loading, and error states before the happy path, not after. If you design the happy path first, the other states become afterthoughts bolted on under deadline, which is exactly why so many products look broken the moment data is missing or slow. The shadow states are where craft is proven.

## The full state matrix

Identify the interaction and data states a user can reach in this task. Specify the relevant ones, including:

- **Interactive element**: identify the states that apply to this control and task, such as rest, hover, focus, active/pressed, disabled, loading, selected, or error. Design reachable states and make unavailable actions clear; do not invent states a control does not have. A disabled button must look unavailable, not just slightly faded.
- **Data view**: empty (nothing yet), loading, partial (some loaded), loaded, error (failed to load), and stale (loaded but refreshing). Each needs a designed treatment.
- Do not conflate empty and loading. A spinner is not an empty state, and an empty state shown while data is still loading tells the user a lie.

## Text that does not cooperate

- **Length.** Titles run long, names are missing, descriptions are empty or enormous. Decide per element: truncate with an ellipsis and a way to see the full text, wrap to a capped number of lines, or let it grow. Never let overflow break the layout or clip silently with no recovery.
- **Unbroken strings.** A long URL, email, or token with no spaces will blow out a container. Handle with wrapping or break rules so it never forces horizontal scroll.
- **Numbers.** Prices, counts, and durations have a realistic maximum. Design the counter for 8 digits, the price for the expensive plan, the timer past an hour. Reserve the space so the layout does not jump as they change.
- **Missing values.** Design what shows when a field is absent: a considered placeholder, a dash, or a hidden row, never "null" or "undefined" leaking to the screen.

## Data: none, one, and far too much

- **None.** The empty state does onboarding work: what goes here, why, and the action to fill it. See copy_as_interface. Hide the controls that cannot do anything yet: filters, sort, tabs, and bulk actions are noise on an empty list. Show them once there is content to act on.
- **One.** A list designed only for many looks wrong with a single item. Check the one-item case.
- **Too much.** A table with 100,000 rows, a chat with 10,000 messages, a select with 5,000 options. Design for scale: virtualize long lists, paginate or lazy-load, make search and filter first-class, and keep performance smooth. A layout that is elegant at ten items and unusable at ten thousand is unfinished.

## Network and time

- **Slow.** Assume the connection is bad. Show instant feedback on action, reserve space to prevent layout shift, and prefer streaming partial real content over a blocking full-screen loader. See motion_and_feel.
- **Failed.** Every request can fail. Design the retry, keep the user's input, and explain what happened in plain language. A failed action must never lose the user's work.
- **Offline.** Where it matters, design the offline state: what still works, what is queued, and how the user knows they are offline. Reconnect and sync without making them redo anything.
- **Stale.** When showing cached data while refreshing, signal it quietly rather than flashing the whole view.

## Internationalization and direction

- **Translation length.** Text expands when translated; German and Finnish commonly run 30 to 40 percent longer than English, and some strings far more. A button sized to fit "Save" exactly will clip "Speichern". Design flexible containers and test with long strings.
- **Direction (RTL).** For Arabic, Hebrew, and others, the entire layout mirrors. Use logical CSS properties (`margin-inline-start`, not `margin-left`) so the design flips correctly. Icons with direction (arrows, back) mirror; logos and clocks do not.
- **Formats.** Dates, times, numbers, currency, and names follow the user's locale, not a hardcoded assumption. Name order and honorifics differ across cultures.
- **Fonts.** The type stack must cover the scripts you support, including tall scripts and combining marks, without clipping line boxes.

## Accessibility as resilience

- Accessibility is not a separate compliance pass; it is the same discipline as handling edge cases. The user with a screen reader, the user at 200 percent zoom, and the user on a keyboard are the same category as the user on a slow network: real, common, and worth designing for.
- Contrast that meets the target, focus order that follows the visual order, targets large enough to hit, motion that respects the reduced-motion preference, and meaning never carried by color alone. See color_and_contrast, motion_and_feel, responsive_canvas.
- Get these right and the design is more resilient for everyone, the curb-cut effect: captions help in a loud room, large targets help on a train, high contrast helps in sunlight.


## Controls, surfaces, and recovery

Choose a control that matches the decision: radios for a small mutually exclusive set, checkboxes for independent choices, segmented controls for a few immediate modes, tabs for peer sections, and a select when inline scanning or comparison is not needed. Keep choices visible when users compare them together. Label overflow menus; do not hide frequent or consequential actions there.

Choose the editing surface by scope and context: inline for a small local edit, dialog for a short focused decision, drawer when surrounding context matters, and a page for substantial work or a task that needs its own URL and navigation. Use native semantics and labels. A drawer may be modal when the task should interrupt, or nonmodal when users need background reference. For a modal dialog, move focus into it, keep keyboard focus within it, support Escape when safe, provide a visible close or cancel action, and return focus to the opener. For a nonmodal panel, leave the background operable and keep focus order coherent. For route changes, move focus to the new page heading or main region and announce the change appropriately.

On validation or save failure, explain the field or action and next step, associate errors with their controls, announce dynamic status to assistive technology, retain entered values, and keep a safe way to cancel or recover. For destructive work, show the exact target and consequence. Use confirmation when recovery cost is high and undo is unavailable or insufficient; prefer a timely undo when it safely covers likely mistakes.
