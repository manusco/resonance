# Project design contract

Use this reference when work changes a user-visible choice or behavior. Applicability follows visible effects, regardless of file type: displayed names, status meanings, controls, navigation, content, and shared interaction can be design concerns. An internal query or storage change with no user-visible effect does not need this check.

## Find the source

Resolve design intent for the affected application in this order:

1. Follow an explicit application design-source declaration in the project's loaded instructions. It has priority over `05_design.md`; use the declared path and surface conflicting sources if they disagree.
2. Otherwise, check `.resonance/05_design.md`. If absent, or if it contains only the untouched scaffold instructions and placeholder values, treat it as unfilled and continue to local discovery. The unfilled framework scaffold is not evidence of a design decision and must not shadow a maintained local source.
3. If `05_design.md` has authored content, keep its stated status and role. Follow a `POINTER` to its exact target. A `PROPOSED` entry may guide investigation and gather supporting evidence, but it remains proposed until approval provenance exists; do not silently replace or elevate it based on another discovered file. Conflicting authored sources stay unresolved unless their authority is established.
4. After absent or unfilled entry-point content, discover maintained local design references for the affected application. Discovery alone does not approve them. If an authoritative source has established provenance, use it; record one persistent pointer when authorized to establish it. A pointer-only `05_design.md` is the default when appropriate.

Use the declaration or pointer's exact path. A broken declared source or authored pointer is a broken source, not proof that no contract exists and not permission to substitute a different file. You may inspect local references to diagnose the gap, but keep the authority unresolved. If declarations conflict, or sources disagree without established authority, report the conflict as unresolved. Do not resolve it by file recency, source format, or personal preference. A discovered `DESIGN.md`, design system, component library, or Figma file is not approved by discovery alone. Classify it as approved only when its provenance or an explicit project declaration establishes approval; otherwise treat it as observed or proposed.

Read the entry point, applicable rules, and only the source sections needed for this task. Do not inspect every linked component or every Designer reference for routine work. Links identify maintained value owners; they do not pre-approve future changes to those files.

## Populate a missing contract during UI work

When normal UI project work introduces the first meaningful interface, adds a shared pattern, or finds the affected application's design entry point absent or still unfilled, make a bounded proposal as part of the work. This is automatic for the coding task; do not wait for a separate `/design` request. For an existing app, inspect only the supplied brief, affected screens, and representative components needed to ground the proposal. For a new app, use the available product brief, implementation plan, and task reasoning to recommend concrete choices; mark them `PROPOSED` even when no implementation evidence exists yet.

Write to `.resonance/05_design.md` only when that is the app's applicable entry point. If an explicit declaration or existing pointer names another canonical source, continue that source and do not add a duplicate. If a shared-pattern proposal is needed in an approved canonical source, add a clearly scoped proposed-change subsection in that same source; preserve its approved status and sections. Replace stale empty proposal placeholders such as `No proposed changes` when adding the first proposal, so the source does not contradict the new subsection. Resume an existing proposal by filling relevant gaps in place; do not regenerate completed choices on each task. Keep the framework repository's public `.resonance/` scaffold template-clean.

The entry must be app-aware and inspectably useful: status, application and scope, task defaults, evidence and representative references, variants (or none), assumptions, and open choices. Distinguish observed implementation, proposed design choices, and assumptions. Ground observed claims in the brief or inspected source. Greenfield recommendations may use explicit task reasoning about the users, content, and constraints; label them proposed and identify the reasoning and uncertainty instead of presenting them as existing facts. Include foundations only when the current scope supports them. Name an approval owner only when the project supplies one. Unknown facts stay explicit as unknown. Do not turn observations into approved rules, copy implementation values already owned by tokens/components, or add generic foundations unrelated to the work. If the project does not contain the framework template, write this concise content directly; missing template tooling is not a reason to block or leave placeholders. The output must be a usable, populated proposal, not a blank scaffold or a design encyclopedia.

Keep the write incremental and idempotent: create one proposal when needed, update only relevant unfinished sections, and leave approved sections byte-for-byte intact unless the authorized task explicitly changes them. A new meaningful app baseline or shared pattern always gets its automatic proposal. A small bug repair does not require a whole-app audit, new approval gate, or broad contract; a repair alone may use nearby conventions without creating a broader proposal. A read-only audit may recommend or show proposed text in its report, but must not write project files. A broken declared source or pointer remains unresolved; do not replace it with a guessed alternative or create a competing contract.

## What the contract owns

The contract records approved meaning, invariant, pattern choice, scope, variants, and exceptions. Code, theme files, and component sources own exact implemented values, names, APIs, and current behavior. An explicitly approved design artifact can own a future visual target. Repository or runtime evidence shows what ships; it does not approve its own intent.

Assess a change to a linked token or component by its effect on the approved choice. A diff to implementation can be a material design change even when the contract file stays untouched. Do not copy CSS values, token values, or component inventories into the contract when their maintained source already owns them. Name any gap between approved intent, target, and current behavior. Resolve material changes through the existing approval owner and authorization, updating intent and implementation references together when approved.

## Make recurring choices consistent

For a durable pattern, name the application, surface and recurring task family; state one approved default; point to the component or representative screen that embodies it; and name any allowed variant with an observable selector. A selector may be an approved workflow, platform, supported layout constraint, or named surface. Use the application's actual component behavior and layout rule. Never invent a universal breakpoint, palette, typeface, or layout rule.

Equivalent tasks use the same default even when each choice would be usable in isolation. A different register, screen name, implementation package, or designer preference does not create a variant. A variant applies only when its named task, application, platform, or surface selector matches; do not carry another task's or application's variant into the current decision. New variants that relax a shared default need an explicit durable decision. Applications keep separate intent even when they share code.

If applicable approved rules within one contract overlap and conflict, name the affected scope and both rules and leave the choice unresolved for the existing owner. Do not invent a more-specific-wins priority or select a rule by document order.

For example, a project could approve its existing contextual drawer for workspace record inspection and a route for a named full-record editing task. The approved layout switch must cite the actual supported constraint. This illustrates how to record a local decision; it prescribes no Resonance-wide interface.

When no approved contract exists, a small repair can follow observed local conventions and supplied intent. State that these are observations, not approved rules. Do not turn one screen or defect into product-wide policy. Work that introduces a shared pattern should show current variation and propose a concrete default before treating it as approved; do not silently rewrite older screens.

## Select foundations and patterns for the task

Design only the foundations the scope needs. Start from the approved product system when applicable. Do not transfer another application's styling or invent a house style. A design-system effort may need reusable color roles, typography, spacing, shape, depth, or motion; a local change may need only one existing token or component. Keep values in their maintained owners.

Choose interaction, data display, and navigation from the user's task, available content, consequence of error, and recovery needs. Use the existing approved pattern for recurring task families. Preserve useful query, filter, sort, selection, and location context when users return from detail. Make a variant concrete and findable, not a discretionary phrase such as “when the task needs it.”

Apply the same selectivity to content and lifecycle vocabulary. Reuse the approved user-facing terms and state meanings. Provide realistic labels, data lengths, and state copy. Cover only states the flow can reach, including empty, loading, validation, failure, success, and disabled states where relevant. Preserve input and context on recoverable failures, and say what happened and how to continue.

For accessibility, input, and responsive behavior, follow applicable WCAG 2.2 AA and platform requirements and the project's supported canvases. Name the relevant keyboard, touch, pointer, assistive technology, zoom/reflow, safe-area, RTL, or reduced-motion needs for this surface. Do not impose CSS tokens or browser checks on native work.

## Resolve conflict and approval

An approved design rule does not waive accessibility, safety, or data-loss safeguards. For a taste or convenience improvement that departs from an approved pattern, propose the revision and retain the approved default until authorized. For a demonstrated hard-constraint defect, identify the conflict and make an already-authorized corrective change when the governing constraint determines the repair. Do not implement unsafe or inaccessible output for consistency, silently rewrite the rule, or claim conformance. Make any material unresolved replacement decision explicit. The user's existing instruction can supply approval; do not add a ceremonial approval step.

Record an exception only when needed. Name its surface, affected rule, reason, accountable owner, risk, review trigger or duration, and removal condition. A variant already allowed by its approved selector is not an exception.

## Verify within scope

For routine reuse, a short comparison with the named approved sibling or reference under the same task, comparable state, and viewport is enough. Also check relevant behavior such as context restoration, keyboard path, focus return, readable content, and recovery. A single screenshot can show a screen's legibility, but cannot establish cross-screen consistency.

Use browser, screenshot, or native-platform evidence appropriate to the surface. Use Figma only when the project has an approved Figma target. If required visual or behavioral evidence is unavailable, report **unverified** and name the evidence needed. Source inspection or the absence of a linter cannot turn a known mismatch into a pass. Keep routine reports short and findings in the existing severity system.

## Lifecycle

The Designer owns writes to the project design contract. Core, planning, build, and UI implementation workflows delegate proposal authoring to this skill.

1. Discover applicable intent before specifying or changing a visible choice.
2. During normal UI coding, automatically populate a bounded proposal when the affected app has no filled entry point or the task adds its first or a new shared pattern. Add a proposed subsection to the same canonical source when that source is approved, preserving its status and approved content.
3. Reuse approved patterns without a separate handoff, approval, contract edit, or full report.
4. Propose and obtain the existing owner's approval for a new durable default or material departure, unless the user's instruction already authorizes it.
5. Implement with scoped checks and references; keep current state, approved target, and gap distinct.
6. Review against the applicable rule and named sibling or reference. Record missing proof as unverified.
