# First-principles guidance for task-first interfaces

**Research date:** 2026-10-14
**Purpose:** Replace universal UI scoring recipes with a task-first method grounded in what the evidence and current standards actually support. This note is research input for future skill work; it does not change skills, generators, or evaluations.

## Recommendation

Start every screen from the user's next consequential task and the information needed to complete it. Prioritize by task frequency, user consequence, uncertainty, and recovery cost as explicit questions, not as a pseudo-precise score. Then make the action, its state, and its context findable; keep related information together; expose advanced controls progressively only when hiding them does not obstruct discovery or comparison. Check the result with representative tasks, keyboard and assistive technology paths, small viewports, and real data density.

This is a decision process, not a claim that four factors combine into a validated universal formula. Weighting depends on the product, user, and task. Record the evidence and the decision in plain language.

## Evidence and boundaries

| Popular rule or finding | What evidence supports | What it does not establish | Use in practice |
| --- | --- | --- | --- |
| Fitts' law | In aimed-movement tasks, movement time varies with movement distance and target width. The original experiments studied controlled motor tasks. | A single universal pixel size, a universal touch target, or that every control should be enlarged regardless of layout. Input device, target position, precision, and motor ability matter. | Put frequent/high-consequence controls close to the relevant content; make targets forgiving; check pointer, touch, and keyboard use. Apply WCAG's actual target-size criterion where applicable. |
| Hick-Hyman law | Choice reaction time grows approximately with the information/uncertainty in the available alternatives in studied choice tasks. The relationship depends on task and choice probabilities. | “Fewer options are always faster,” a cap on navigation items, or that hiding choices improves task completion. Recognition, labels, learned structure, and search also matter. | Group alternatives by the user's goal, use explicit labels, and test time/error for realistic decisions. Reduce genuinely irrelevant choices; do not hide needed alternatives to hit a count. |
| Miller's 7±2 | Miller reviewed multiple distinct limits, including absolute identification and immediate memory span. “Chunk” depends on what a person knows and how stimuli can be grouped. | A maximum number of controls, menu items, fields, or headings. Miller himself cautioned about the number's varied appearances; later memory work specifies boundary conditions and often finds smaller capacity estimates in particular tasks. | Use meaningful grouping, labels, and external memory (visible state, summaries, comparison). Decide grouping from task structure, not a seven-item quota. |
| “Visual hierarchy” | Contrast, position, size, grouping, and alignment can make elements more or less salient; interface visual-attention research studies effects in specified tasks and stimuli. | A fixed seven-lever checklist, guaranteed eye path, or proof that the most visually salient element is the most useful next step. Attention depends on goals, content, user, and competing signals. | Make the task's primary action and status easy to locate; use restrained emphasis; verify with first-click/first-action and task-completion evidence. |
| 60/30/10 color | A recurring interior/color-design convention. | A validated interface allocation formula, accessibility conformance, or useful distribution for arbitrary data visualizations and states. | Choose color for semantic role, hierarchy, and brand. Check text/non-text contrast and never encode meaning with color alone. |
| Fixed chrome/workspace percentages | Some products benefit from persistent navigation or a stable work area. | A universal proportion for header/sidebar/canvas, or that persistent chrome is always worth the space. Responsive behavior and task context change the tradeoff. | Keep global navigation persistent when frequent cross-area movement justifies it; let secondary panels collapse or adapt. Test at actual supported widths and zoom. |
| “Recognition over recall” | Recognition cues and visible context can help users act without retaining details in memory. | That all options and instructions should be permanently visible, or that progressive disclosure is inherently easier. | Preserve labels, current values, constraints, and feedback at the point of action. Reveal advanced/rare controls when discoverability remains clear and the user need not compare them concurrently. |

Primary evidence: [Fitts (1954)](https://doi.org/10.1037/h0055392); [Hick (1952)](https://www2.psychology.uiowa.edu/faculty/mordkoff/InfoProc/pdfs/Hick%201952.pdf); [Miller (1956), full text](https://psychclassics.yorku.ca/Miller/); [Cowan (2001), memory-capacity reconsideration](https://pubmed.ncbi.nlm.nih.gov/11515286/). For visual salience, see the task-bound mobile UI study [Understanding Visual Saliency in Mobile User Interfaces](https://arxiv.org/abs/2101.09176); its scope is measured gaze/saliency in its study stimuli, not a general hierarchy recipe.

Jakob Nielsen's ten usability heuristics are useful broad inspection prompts, not a validated scoring equation or a screen-priority model. Nielsen describes them as general principles and “heuristics,” not specific usability guidelines. Use them to find possible problems (such as missing system status or unfamiliar terms), then test the task and the proposed correction. See [Nielsen's original heuristic summary, updated 2024](https://www.nngroup.com/articles/ten-usability-heuristics/).

## Task-first screen procedure

1. **Name the user and task.** Write a concrete trigger, desired outcome, and what makes failure costly. Example: “A support agent opens a billing case, confirms the disputed invoice, and records the resolution without losing the current case context.”
2. **List the task path and decision inputs.** For each step, record the action, information needed before acting, likely errors, and how to recover. Separate must-see information from occasional reference material based on evidence about the task.
3. **Prioritize in plain language.** Ask: How often does this task happen? How serious is a wrong or missed action? How uncertain is the user about the current state or next step? How hard is recovery? State the answers and rationale. Frequency helps optimize routine flow; it must not bury rare, time-critical, safety-critical, or legally required actions. Give urgent exceptions a clear contextual route and signal their state where the user can act on them. A 2×2 can help compare two dimensions; it cannot honestly collapse frequency, importance, risk, and cognitive effort into a single score without validated weights and data.
4. **Arrange around work.** Keep an object and the controls acting on it together. Show identity, status, relevant constraints, and feedback near the decision. Use headings and labels that name the user's concepts rather than internal system terms. Make selected, pending, saved, and failed states explicit.
5. **Choose disclosure and navigation from the job.** Keep choices visible when users compare them, need to discover them, or move between them often. Use a disclosure control for secondary material that is infrequent and independently understandable. Do not hide required content or split a sequence of questions just to reduce apparent density. GOV.UK's current accordion guidance explicitly says to test without it first and use it only where research supports show/hide; its tabs guidance limits tabs to switching related views, not page navigation.
6. **Fit the data and controls to the viewport.** At narrow widths and enlarged text, preserve the task, label-control associations, feedback, and access to actions. Reflow ordinary content. For inherently two-dimensional content such as a data table, keep its row/column meaning and provide an operable way to inspect it rather than shrinking text until it is unreadable.
7. **Verify with observable outcomes.** Give representative users realistic tasks. Capture completion, errors, time where speed matters, first action, backtracking, requests for help, and confidence. Pair these with keyboard-only, screen-reader, zoom/reflow, and touch checks. Aesthetic preference alone does not verify usability; a benchmark pass alone does not establish that the task is easy.

## Choose controls by the relationship they express

Choose a control by the user's mental model and the state transition, not by a decorative style recipe. Use a radio group for one choice from a small set when seeing the alternatives before committing helps; use a checkbox when each option is independently on/off and multiple selections are valid; use a select/listbox when the option set is long or space constrained and users can still recognize the desired value; use tabs only to switch among peer content panels in the same view; use navigation links for moving to another location; use a disclosure for showing/hiding content in place. A segmented-looking control is just a visual treatment until its keyboard, selected-state, and semantic behavior are defined. Avoid tabs when users need to compare panels concurrently or when the control actually navigates pages. Follow native platform patterns where available and check semantics and keyboard behavior against the appropriate APG pattern.

Example: “Monthly / yearly” that changes a price estimate is a single mutually exclusive choice, so exposed radios or a properly implemented radio-like selector express the state. “Overview / activity / settings” can be tabs if each reveals a peer panel in the same view; use ordinary navigation if each has its own route and should support browser history, bookmarking, or a distinct page heading.

## Applying the method to common screen types

### Dense workspaces and dashboards

Do not begin with a target percentage for navigation, chrome, and canvas. Identify the repeated task, primary object, and the information users compare at once. Pin only navigation and status that are repeatedly needed to orient or switch work. Put filters and secondary actions near the result set they change. Keep the working object visible while details are inspected if losing it would cause errors. Collapse panels when users rarely need them, but label the affordance and retain state if reopening is common. Validate with common and exception tasks at the minimum supported width, browser zoom, and realistic record volume.

### Tables and data-heavy views

Use a table when users need to scan records or compare values across shared attributes; use a list/cards when each record is read independently and cross-row comparison is not central. Provide a meaningful caption or title, column headers, and row headers where they identify the record. Align numbers consistently. Make sorting/filtering state visible and preserve it when users inspect a record and return. Do not solve density by removing context or reducing type by default. GOV.UK's table guidance advises reducing/splitting data where possible and limits its smaller-text option to genuinely data-heavy tables. On narrow screens, prioritize the fields for the task, support horizontal inspection for true tabular comparison, and make the scroll affordance discoverable.

### Forms and errors

Put a visible, programmatically associated label on every control; do not rely on placeholder text as the label. Put format examples and constraints before the user needs them. Group fields only when the information is conceptually related. On error, preserve valid entries, identify the field in plain language, explain how to fix it, associate the message with the control, and provide a linked summary for long forms. Move focus or otherwise announce the error summary when appropriate, without making the user hunt. Distinguish validation from server/network failure and tell users whether their data was saved. GOV.UK component guidance and WCAG's relationships, labels, and error identification criteria are actionable references.

### Dialogs, drawers, and overlays

Choose an overlay only when a contained, interrupting subtask benefits from maintaining the underlying page context. A modal makes the outside unavailable, so reserve it for work that truly requires that focus. For a web modal, label the dialog, make the background inert, move focus to a meaningful starting point, keep keyboard operation inside while open, support a visible close/cancel route and Escape where appropriate, then restore focus to the trigger or a logical next step. Initial focus depends on content: a long structured dialog may need focus on its heading; a short confirmation may focus its primary control. Do not add `aria-modal="true"` unless the behavior really blocks interaction outside. For a nonmodal drawer/popover, do not trap focus; ensure it does not obscure the focused item, can be dismissed, and leaves a clear route back to the invoking context. On mobile, use a full-screen route/sheet when the available area makes a narrow side panel hard to read or operate. Validate keyboard and screen-reader behavior; visual resemblance to a modal is not sufficient.

The WAI-ARIA APG modal pattern documents focus entry, containment, Escape, labeling, return focus, and exceptions for initial focus. W3C notes that incorrectly marking a nonmodal overlay as modal can hide the rest of the interface from assistive technologies. These behavior requirements are stronger evidence than any fixed modal-versus-drawer rule.

## Accessibility constraints that affect prioritization

- **Targets:** WCAG 2.2 SC 2.5.8 AA generally requires a 24×24 CSS-pixel target or sufficient spacing, with defined exceptions. This is a conformance floor, not a claim that 24 px is ideal for every motor context. Larger targets can improve use; test the actual interaction and platform guidance. Do not call 44 px a universal WCAG minimum.
- **Reflow:** WCAG 2.2 SC 1.4.10 expects content to work at a width equivalent to 320 CSS px without two-dimensional scrolling, except for content whose meaning or use requires a two-dimensional layout. A genuinely comparative table is an example requiring careful treatment, not a license to let the whole page overflow.
- **Focus:** WCAG 2.2 includes Focus Not Obscured (Minimum) at AA; focus must not be entirely hidden by author-created content. Focus Appearance is an AAA criterion. Keep a visible focus indicator and test sticky chrome, drawers, dialogs, and responsive layouts for occlusion.
- **Color and status:** Meet the applicable WCAG contrast requirements for text and non-text controls. Do not rely on hue alone for errors, selection, status, or charts; pair color with text, shape, or another cue.
- **Semantics:** Use native controls and structural HTML where possible. A custom control owes the same name, role, value, keyboard operation, and state communication as its native counterpart.

Normative/current sources: [WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/), [Target Size (Minimum) understanding](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html), [Reflow understanding](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), [Focus Not Obscured understanding](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html), [WAI-ARIA APG modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/).

## Decision examples

**Case triage screen:** Agents handle this screen dozens of times daily, a missed refund risk is high, and they must compare invoice status with account history. Put case identity, payment status, and the next action in the working area; keep relevant history one step away or visible if comparison is frequent. Do not collapse the evidence solely to make the screen look sparse. Measure time-to-correct disposition and wrong dispositions.

**Rare advanced settings:** Users occasionally configure a secondary export field and otherwise need a clear default export action. A labeled “Advanced options” disclosure can reduce routine scan cost if the advanced settings are not needed for comparison and users can find them. Validate discoverability with first-time users and retain entered settings when toggled closed.

**Destructive confirmation:** A permanent delete has low frequency, high consequence, and poor recovery. Put object identity and consequence in the confirmation, make the safe exit obvious, and focus the dialog according to risk. Consider an undo path if the product can provide one safely. Do not use a confirmation for every reversible action merely to signal seriousness.

## Falsification and evaluation criteria

Treat each layout choice as a hypothesis with a named task and a predicted observable effect. Examples:

- “Keeping invoice status beside the refund action will reduce wrong refunds.” Falsify if representative agents make the same or more wrong decisions, or need extra searching to interpret the status.
- “Collapsing the rarely used export fields will speed routine exports without reducing successful discovery.” Falsify if first-time users miss the fields, abandon the task, or take longer overall when they need them.
- “A persistent left navigation helps frequent section switching.” Falsify if task completion does not improve and the panel materially reduces usable space at common viewport widths.
- “A side drawer is suitable for editing a record while retaining context.” Falsify if users lose their place, cannot see enough content at 320 CSS px/zoom, or focus becomes obscured or inaccessible.

Use a small formative study to find comprehension and navigation failures; instrument production outcomes only where privacy and consent permit. Segment by experience, input mode, viewport, and relevant access needs when the sample allows. Avoid declaring success from a single aggregate completion percentage if high-severity errors or an affected user group regress. Record sample, task script, measures, and decision so a later team can challenge the conclusion.

## Guidance for future skill revisions

Replace numerical design recipes with this contract: name the user/task; state the priority evidence; show the relationship between task, information, and controls; explain any hidden or persistent UI; identify accessibility and responsive risks; give one testable prediction and a failure condition. The skill should call out Fitts/Hick as bounded models and Miller's number, 60/30/10, fixed chrome percentages, and “7 levers” as unsupported universal constraints. A future skill change should be evaluated on whether outputs cite concrete user goals, useful tradeoffs, access paths, and falsifiable checks, not on whether it repeats a checklist.

## Sources and dates

Sources were accessed 2026-10-14. Standards and design-system pages can change; verify their current version when implementing a skill update.

- Fitts, P. M. (1954), “The information capacity of the human motor system in controlling the amplitude of movement,” *Journal of Experimental Psychology*, 47(6), 381–391. [DOI](https://doi.org/10.1037/h0055392).
- Hick, W. E. (1952), “On the rate of gain of information,” *Quarterly Journal of Experimental Psychology*, 4(1), 11–26. [Original paper](https://www2.psychology.uiowa.edu/faculty/mordkoff/InfoProc/pdfs/Hick%201952.pdf).
- Miller, G. A. (1956), “The Magical Number Seven, Plus or Minus Two,” *Psychological Review*, 63, 81–97. [Full text](https://psychclassics.yorku.ca/Miller/).
- Cowan, N. (2001), “The magical number 4 in short-term memory: A reconsideration of mental storage capacity,” *Behavioral and Brain Sciences*, 24(1), 87–114. [PubMed](https://pubmed.ncbi.nlm.nih.gov/11515286/).
- W3C, [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/), Recommendation published 2023-10-05; criterion understanding pages accessed 2026-10-14.
- W3C WAI, [ARIA Authoring Practices Guide: Dialog (Modal) Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/), accessed 2026-10-14.
- W3C WAI, [ARIA APG radio group](https://www.w3.org/WAI/ARIA/apg/patterns/radio/), [tabs](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/), and [disclosure](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/) patterns, accessed 2026-10-14.
- Nielsen Norman Group, [10 Usability Heuristics for User Interface Design](https://www.nngroup.com/articles/ten-usability-heuristics/), Jakob Nielsen, first published 1994, reviewed 2024-01-30; accessed 2026-10-14.
- GOV.UK Design System, [Accordion](https://design-system.service.gov.uk/components/accordion/), [Tabs](https://design-system.service.gov.uk/components/tabs/), [Table](https://design-system.service.gov.uk/components/table/), [Text input](https://design-system.service.gov.uk/components/text-input/), [Error summary](https://design-system.service.gov.uk/components/error-summary/), accessed 2026-10-14.
- Apple Human Interface Guidelines, [Layout and organization](https://developer.apple.com/design/human-interface-guidelines/layout-and-organization), accessed 2026-10-14.
- Luis A. Leiva, Yunfei Xue, Avya Bansal, Hamed R. Tavakoli, Tuğçe Köroğlu, Jingzhou Du, Niraj R. Dayama, and Antti Oulasvirta, [Understanding Visual Saliency in Mobile User Interfaces](https://doi.org/10.1145/3379503.3403557), MobileHCI 2020. Study-specific results; not a universal layout standard. The 2021 arXiv posting is a later preprint record, not the publication year.
