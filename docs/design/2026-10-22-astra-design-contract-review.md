# Astra decision review: project design contract

**Verdict: REVISE, then proceed to implementation planning.** The artifact location and owner are sound. The proposed rules do not yet close the user's main failure mode: two screens can satisfy the same loose contract while choosing different patterns for the same task.

Reviewed `docs/design/2026-10-22-design-contract-investigation.md`, SHA-256 `3bb8c80c24fb456cd99c91bcb2e988f104a8c5d2cc314ca9e7ab8047de53fa72`, against repository HEAD `7ba9395abefa1d7408ee633ed744176e5246c5a4`. This is an independent decision critique, not an implementation review or product UI validation. The primary review remains responsible for reconciling these findings.

## Strongest objection: a contract can preserve freedom to drift

The worked rule allows drawer versus route based on “task context.” The filter example allows toolbar versus sidebar when comparison needs justify it. Those are good Designer reasoning prompts. They are insufficient product decisions.

Counterexample: agent A builds Customers with a detail drawer and top filters. Agent B builds Suppliers with a detail route and side filters. Both preserve state, keyboard access, and readable detail. Both cite comparison needs. The proposed checks can pass both implementations, even when the workflows are equivalent. The user's complaint survives the new file.

**Required correction:** a durable project pattern must settle the recurring choice. Record a default for a named task family, the existing component or representative screen that embodies it, and observable conditions for allowed variants. For example, an actual product might approve its existing contextual drawer for workspace record inspection and its existing route for the named full-record editing workflow. Its responsive switch should point to the real component/layout constraint. These are project decisions, never a Resonance-wide drawer rule or invented universal breakpoint.

Verification must compare the changed screen with the relevant approved reference or sibling under comparable state and viewport. A screenshot of one isolated screen can prove legibility but cannot prove consistency across screens. A short comparison is sufficient for routine reuse. A full product inventory is not required.

## Required clarifications

### 1. Close authority loopholes without copying implementation values

The proposal correctly separates approved intent from current implementation. However, “exact implemented color ... current behavior” as code authority plus a mutable source link can permit an agent to change the shared token or component and then use that changed source as proof of conformance. No document rule was edited, but every screen changed.

Determine material design change by its effect on the approved choice, including changes inside linked sources. A source link identifies the maintained value owner; it does not pre-approve all future changes to that file. Use ordinary version-control diffs and approval evidence to assess the change. Do not mirror hex values into Markdown or pin every routine component edit to a second approval ritual.

A maintained `DESIGN.md` is not automatically an approved baseline. A historical draft, a copied vendor kit, or a Figma exploration must not gain authority merely because discovery found it. Adopt its existing approval evidence when available; otherwise classify it as observed/proposed. Where two sources disagree and neither has established authority, keep the choice unresolved instead of silently selecting the newer file.

### 2. Make the entry point deterministic

The proposal alternates among a pointer file, “project context,” and an “existing project context entry.” Those are valid implementation options but not one discovery contract. A new agent needs a repeatable lookup, and a preserved consumer `AGENTS.md` may never receive a new framework sentence.

Minimum rule: honor an explicit application design-source declaration in the project's loaded instructions; otherwise check `.resonance/05_design.md`; if absent, discover maintained local design references for the affected application. After discovery, record one persistent entry point when authorized to establish it. A pointer-only `05_design.md` is the simplest default for existing sources. Do not create a second rule body. Broken pointers, conflicting declarations, and proposed documents must remain distinguishable from “no design contract.”

Applicability follows user-visible effects, not file extension or engineer role. A backend edit that changes displayed lifecycle names or shared status semantics can affect the design contract. A database index change normally does not. Native mobile implementation also needs the same contract lookup; the implementation map currently leaves that integration optional despite claiming every applicable UI change is bound.

### 3. Define how approved bad UX is handled

The existing Designer explicitly requires applicable accessibility and forbids losing input or task context. Its first operational step also says preserve a specified system unless evidence shows it blocks the task. A new binding contract must resolve that boundary, not introduce two contradictory commands.

For a taste or convenience improvement that departs from an approved pattern, propose the revision and retain the current default until authorized. For a demonstrated accessibility, safety, or data-loss defect, do not treat design approval as a waiver. Identify the conflict, perform already-authorized corrective work where the governing constraints determine the repair, and make any material unresolved replacement decision explicit. Do not claim conformance with the defective rule or silently rewrite it to make the check pass. Approval can be the user's existing explicit instruction; it need not be a second ceremonial question.

### 4. Keep variants bounded and reuse cheap

Named scopes alone do not prevent exception laundering. “This screen is a different register” must not let every page choose a new palette or table pattern. Register guides reasoning; it does not grant a new approved variant. New variants that relax a shared default require the same decision treatment as other material changes.

Use one applicable default plus explicitly approved variant conditions. If overlapping rules produce conflicting instructions, surface the conflict rather than inventing a most-specific-wins override hierarchy. Separate applications retain separate contracts. A monorepo only needs a small application-to-source mapping when there is more than one actual application.

Read the entry point and relevant rule/source sections, not every linked component and every Designer reference on every UI edit. Read-only reuse requires neither a Designer handoff nor a contract edit. This is how the design owner remains a knowledge skill rather than becoming a new orchestration layer.

## What I accept

- **Optional `.resonance/05_design.md` default:** fits the adopter's project context and keeps architecture separate. The actual path is less important than reliable discovery and one authority.
- **Existing `DESIGN.md` adoption:** superior to forced migration when that source is maintained and its authority is established. A pointer is enough.
- **Designer ownership:** create, revise, and inspect durable design intent within the existing skill. Knowledge ownership does not require a new CLI or a new skill archetype.
- **Code as value owner:** tokens and component APIs remain in their maintained implementation sources. The document records purpose, choice, scope, and references.
- **Binding rules with visual verification:** lack of a deterministic checker does not make an approved decision optional. A known violation remains a violation. Missing required evidence remains unverified and cannot support a passing conformance claim.
- **Proportional brownfield adoption:** a small repair can use observed conventions without first canonizing the entire application. A blank template proves nothing about design approval.

## What I reject

- **Putting this in `04_systems.md`:** the existing blueprint separates architecture from styling. Shared storage would widen architecture gates without resolving design ambiguity.
- **Generic Designer knowledge alone:** it teaches how to choose; it does not remember which choice this product approved.
- **Current code alone:** it can preserve accidental inconsistency and cannot distinguish accepted intent from implementation debt.
- **A new design-contract skill or mandatory workflow:** it duplicates an existing owner and increases routing cost before solving a demonstrated ownership gap.
- **Mandatory three-tier tokens, global style lint, or a universal visual grammar:** these prescribe implementation structure or style beyond the user's need.
- **Automatic approval on discovery or automatic code-wins conflict resolution:** both turn evidence into authority without a decision.

## Minimum necessary implementation

1. One small Designer reference defining discovery, authority, shared-pattern defaults, variants, approval scope, and evidence. Link it from the existing Designer workflow and description where needed for natural-language discovery.
2. An optional template supporting authored rules or a pointer-only form. Keep this framework repository's scaffold free of actual product decisions.
3. Short conditional hooks in plan, build, frontend, mobile, reviewer, and QA. Direct local UI work must reach the same rule even when it bypasses `/plan` and `/build`. No full design report for routine reuse.
4. Reconcile the existing mandatory token-layer language and Figma-only QA reference with project-owned sources and appropriate evidence.
5. Behavioral evals covering the failure modes below, template parity checks, and a preservation check showing adopter-owned design content is excluded from framework upgrade writes. Use existing Forge generation and validation.

Defer a design registry, contract parser, source scanner, screenshot infrastructure, component catalog, mandatory rule IDs, and automated enforcement until an actual project rule and reliable check justify them. Do not build a special updater merely for this file; verify the existing project-preservation boundary.

## Adversarial acceptance cases

| Case | Required outcome |
| :--- | :--- |
| Same-task Customers and Suppliers screens choose different detail surfaces | Detect divergence from the approved task-family default even if both are individually usable. Require an approved variant or align them. |
| One screen is a marketing surface and one a workspace | Apply the approved scoped variants. Do not infer that the marketing register grants arbitrary exceptions to workspace rules. |
| A local icon-spacing fix follows an approved component | Read the relevant source, make the fix, run an appropriate check. No new baseline, full audit, or approval round. |
| A token file changes the shared primary-action treatment without editing the contract | Assess the effect against approved intent and existing authorization. The changed file cannot certify its own conformity. |
| Root `DESIGN.md` is maintained but marked draft; old Figma disagrees | Preserve both as evidence, do not mark either approved automatically, and name the unresolved decision. |
| An approved rule removes visible keyboard focus | Flag the hard-constraint conflict. Do not implement inaccessible output merely for consistency or call it conforming. |
| Contract is approved; browser evidence is unavailable | Cite the binding rule and missing proof. Do not issue a passing visual-conformance claim because source inspection passed. |
| No contract exists; one screen has a small bug | Repair using observed conventions and supplied intent. Do not create product-wide policy from that screen. |
| A new shared pattern is proposed in a brownfield app | Show current variation and the proposed default. Obtain the durable decision through existing authorization/approval, without silently rewriting all older screens. |
| A desktop and native-mobile implementation share the same product | Read the same applicable intent; use explicitly scoped platform variants and appropriate native evidence. Do not impose CSS/token tooling on native code. |
| A backend-only diff renames a user-visible status | Check applicable vocabulary/status rules despite the backend file path. Skip a separate internal query optimization with no UI effect. |
| An adopter upgrades Resonance with an authored `05_design.md` or pointer | Preserve authored content and canonical-source ownership. Template or generated-skill updates must not replace it. |
| A headless CLI project runs `/init` or adds a command | No invented screen contract, palette, or browser verification. Respect any actual user-facing interaction requirements separately. |
| Two apps share a component package but have distinct brands | Resolve application-specific intent first; sharing implementation does not authorize copying one app's approved visual treatment into the other. |

## Evidence, gaps, and reversal conditions

Verified the proposal against the local Designer skill and its generation, chaining, conceptual-model, and register references; Blueprint authority and conformance protocols; plan/build context gates; core initialization; frontend/mobile sequences; QA and reviewer checks; and the updater skill's project-preservation policy. Relevant existing facts: Designer is `archetype: knowledge`; the chaining reference currently mandates three token tiers; QA's visual reference currently assumes Figma; the architecture conformance protocol distinguishes normative authority from descriptive evidence; updater policy preserves project-owned documentation.

No real application's contract, UI, screenshots, component tree, or approval history was supplied. Therefore this review cannot prove that the proposed document granularity is sufficient for the user's product or that these hooks prevent drift in actual agent sessions. That proof needs adversarial evals first and an adopted product example later. The state/memory files are blank public scaffold content, not project evidence.

**Go:** after the proposal requires concrete project defaults and variant selectors, closes source/approval loopholes, specifies reliable discovery for all UI paths, and resolves hard-constraint conflicts. Then implement the small hooks and test them.

**Revise:** if evals still permit two equivalent screens to choose different approved defaults, or routine reuse needs repeated permission. Tighten the rule or simplify the lifecycle based on the failure, rather than adding a new conductor.

**No-go:** if implementation turns the optional artifact into a universal house style, overwrites adopter content, or claims automatic enforcement that only prose prompts provide.

**DONE:** decision critique completed against the named artifact and local sources; no framework implementation or Git mutation performed.

Skipped live-product validation and executable tests because this is a proposal review. Main remaining risk: the contract can become another generic guide unless the approved choices actually distinguish consistent from inconsistent screens.
