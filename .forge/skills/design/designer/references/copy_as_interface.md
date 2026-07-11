# Copy as Interface

> The writing is the design. Users do not read around the interface to reach the content; the interface is made of words. Labels, buttons, empty states, and error messages carry more of the experience than any color choice. A beautiful screen with vague copy is a broken screen.

## Contents
- Design with real content
- Clarity is the whole job
- Buttons and labels say what happens
- Error messages help, they do not scold
- Empty states are the first impression
- Microcopy at the point of doubt
- Voice, tone, and register
- The mechanics that read as care

## Design with real content

- Never design with lorem ipsum. Fake text hides the real problems: the title that is actually three lines long, the name with no last name, the description that is empty, the price with eleven digits. Design with the real strings, or with realistic worst-case strings.
- Layout follows content, not the reverse. A card sized to a perfect two-word title collapses the moment a real seven-word title arrives. Design for the content that will actually show up.

## Clarity is the whole job

- Don't make the user think. Every label, every action, every message should be understood on the first read with no interpretation. If a word makes the user pause to decode it, it has failed.
- Plain over clever. Cute microcopy that obscures what a button does costs comprehension. Save personality for moments that do not carry critical meaning.
- Write for scanning, not reading. Front-load the important word. People scan interfaces; they do not read them start to finish.
- Cut words until it breaks. "In order to get started, please go ahead and click the button below" is "Get started". Concise copy is faster to parse and looks more confident.

## Buttons and labels say what happens

- A button describes its outcome, not a generic verb. "Save changes", "Send invite", "Delete project", not "OK" or "Submit". The user should know what happens before they click.
- Labels name the thing in the user's language, not the system's. "Members", not "User entities". Match the words your user already uses.
- One primary action per view, worded as the outcome the user wants. Secondary and destructive actions are worded and weighted to match their risk. Watch two failure modes: a secondary button styled too light-grey reads as disabled, and a filled-red destructive button competes with the primary. Give the secondary real but quieter weight, and prefer a text-weighted destructive action over a loud filled one.

## Error messages help, they do not scold

- A good error says what went wrong, why, and how to fix it, in plain language. "That email is already registered. Try signing in instead." beats "Error 409" and beats "Invalid input".
- Never blame the user and never expose the machine. No stack traces, no codes as the primary message, no "you did X wrong". The system failed to prevent the state; the message helps the user out of it.
- Put the message where the problem is (next to the field), at the moment it can be acted on, not in a distant banner after submit.
- Validate helpfully: confirm what is right, guide toward what is missing, and never clear the user's work on an error.

## Empty states are the first impression

- The empty state is what a new user sees first, before any data exists. It is an onboarding moment, not a blank void. Say what goes here, why it is useful, and give the one action that fills it.
- Distinguish the kinds of empty: nothing yet (guide them to create the first one), nothing found (help them adjust the search), and nothing left (reassure, for a cleared inbox). Each wants different copy.
- A blank screen that just says "No data" wastes the highest-intent moment in the product.

## Microcopy at the point of doubt

- Anticipate the small hesitations and answer them in place: a hint under a field about the format expected, a note on why you need a permission, a one-line reassurance next to a scary action ("You can undo this").
- Placeholder text is not a label and not help. It disappears on focus and fails accessibility if it carries meaning. Use real labels and separate helper text.
- Confirmations should state the consequence, not ask a vague "Are you sure?". "Delete 3 projects? This cannot be undone." lets the user actually decide.

## Voice, tone, and register

- Voice is constant (who the product is); tone flexes with the moment. The same product is warm on a success and calm and plain on an error. Never jokey in a failure or a payment.
- Match the register of the product and audience. A developer tool is precise and terse; a consumer wellness app is warm and encouraging. The words set the personality as much as the visuals.
- Consistency is craft. One product should not say "Log in" on one screen and "Sign in" on the next. Keep a small internal glossary and hold to it.

## The mechanics that read as care

- Sentence case for UI text in most modern systems; it is friendlier and easier to read than Title Case, and reserve all-caps for small labels with tracking added.
- Use the user's numerals and formats: local date, time, currency, and number grouping. A date shown in the wrong regional order is a small daily friction.
- Real punctuation in copy too: curly quotes, a proper apostrophe, an ellipsis character on a menu item that opens more. See typographic_system.
- Numbers that update in place use tabular figures so they do not jitter. The copy and the typography are the same craft, seen from two sides.
