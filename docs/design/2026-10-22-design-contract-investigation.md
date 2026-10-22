# Project design contract: first-principles proposal

**Status:** Proposal for review. No implementation or scaffold change was made.

## Recommendation

Give each application one discoverable, persistent source for approved design intent and shared UI patterns. Resolve it in this order: an explicit application design-source declaration in loaded project instructions; otherwise `.resonance/05_design.md`; otherwise local discovery for the affected application. A pointer-only `05_design.md` is the default when a maintained `DESIGN.md`, design-system document, or equivalent is already canonical. Discovery alone does not approve a draft, vendor kit, or Figma exploration. Adopt existing approval evidence when available; otherwise keep the source observed or proposed and record that status. Do not duplicate its content or force migration.

Keep lifecycle ownership in the existing `resonance-design-designer` knowledge skill. A new shared baseline and a material departure from an approved rule need owner approval. Approved rules bind every applicable UI change, whether or not a linter can check them. Every UI-scoped design, planning, build, frontend, and native/mobile task reads the entry point and only the applicable rules and cited sources. Reusing an approved pattern in a local screen needs no new approval, revision, Designer handoff, or full conformance report. Applicability follows effects on user-visible behavior, names, status, or interaction, not file extensions or engineer role. Non-UI changes with no such effects skip the design contract.

## What already exists

The architecture blueprint supplies a governance precedent, but it expressly excludes style. `.agents/skills/strategy/blueprint/SKILL.md:86-92` makes `.resonance/04_systems.md` the architecture baseline and says it is not a style guide. `.agents/skills/strategy/blueprint/references/blueprint_protocol.md:18-34` keeps one authority and non-normative evidence separate. `.agents/skills/strategy/blueprint/references/conformance_protocol.md:75-84` exempts routine styling that does not touch architecture rules. Design should use that separation and proportionality without merging design into architecture.

The Designer skill already owns product-fit reasoning. `.agents/skills/design/designer/SKILL.md:65-76` covers project context, user task, layout and controls, product conventions, reachable states, and accessibility. Its generation protocol allows concise shared documentation for system-wide work and local exceptions when they help maintenance (`.agents/skills/design/designer/references/design_system_generation_protocol.md:11-22`). It also says a system document is not required for each screen or component. The skill explicitly rejects transferring palettes, typefaces, radii, density, or layouts across products (`.agents/skills/design/designer/SKILL.md:53-54,73`). Existing designer evals cover system creation and product style transfer, but not discovery of an existing canonical file or its persistent use.

Implementation references are present but do not define a project contract. Frontend token guidance is at `.agents/skills/engineering/frontend/references/design_tokens_protocol.md:1-62`; the Designer's visual/behavior split is at `.agents/skills/design/designer/references/skill_chaining_protocol.md:1-43`; frontend reads project patterns and tokens at `.agents/skills/engineering/frontend/SKILL.md:67-75`; mobile covers platform fit at `.agents/skills/engineering/mobile/SKILL.md:31-47`. The chaining protocol's absolute “never hardcode” and three-tier token rules conflict with the Designer's product-context rule to establish only foundations this scope needs (`designer/SKILL.md:73`). A project should not need to introduce a token engine or three token layers to follow its approved design.

Review and QA have partial UI coverage. QA's 8-path matrix includes visible UI text and render behavior (`.agents/skills/ops/qa/SKILL.md:80-101`). Its design validation reference assumes Figma pixel matching and fixed example dimensions (`.agents/skills/ops/qa/references/design_validation_protocol.md:1-33`), although no project must have a Figma source. The code reviewer has an architecture screen but no design contract screen (`.agents/skills/ops/reviewer/SKILL.md:42-49`). `/page-audit` delegates the design lens for broad page experience (`.agents/skills/ops/page-audit/SKILL.md:70-83`), not routine component review.

The framework keeps canonical skill sources under `.forge` and generates `.agents/skills` (`.forge/README.md:3-40`). `/init` creates `04_systems.md` from `.forge/templates/04_systems.md` (`.agents/skills/ops/core/SKILL.md:87-100`); `.forge/tests/test_systems_template.py:8-33` checks template/scaffold parity. The repository's `AGENTS.md:46-50` says `.resonance/` is a public scaffold and must not hold framework development state. It also requires plans for non-trivial work and names `/design`, `/plan`, `/build`, `/test`, `/audit`, and `/review-pr` in its routing map. Here the state and memory files remain blank scaffold content, there is no `.resonance/memory/`, and four unrelated untracked research notes existed before this investigation.

## Authority and scope

The contract applies to one application, with named surfaces and variants inside it. A product can have an operational workspace, settings, onboarding, a marketing surface, dark/light themes, and mobile/desktop layouts, each with a scoped variant. Separate applications keep separate design intent even when they use the same framework. A Resonance-wide palette or default layout is out of scope.

Use this source-of-truth boundary. Links locate maintained value owners; they do not pre-approve future changes to those files. Assess ordinary diffs by the effect on the approved choice. A code or token change cannot certify its own conformance.

| Concern | Authority |
| :--- | :--- |
| Approved meaning, invariant, pattern choice, variant scope, exception | The approved design contract |
| Exact implemented color, spacing, typography value, token name, component API, current behavior | The maintained code, token/theme file, or component source cited by the contract; these are current facts and value owners |
| Approved future visual target | An explicitly approved design/Figma artifact, when one exists; Figma is never assumed |
| What currently ships | Repository/runtime evidence. Current code is evidence, not approval of its design intent and not an automatic winner in a conflict. |

Do not duplicate CSS, raw token values, or component inventories when a maintained implementation source exists. A conflict between approved intent and implementation must be named, marked as a gap, and resolved by the design contract's approval owner. The resolution updates the contract and implementation references in the same approved change. Keep current state, approved target, and transition/gap distinct. Without an approved contract, infer observed conventions for a local fix, but do not call them approved, use them to bless poor UX, or canonize the whole product from one screen.

Approved rules are binding even without deterministic enforcement. A missing screenshot, browser check, or other evidence leaves conformance **unverified**; it does not become a pass because there is no linter. Report the verification gap with the evidence needed. A project may adopt deterministic checks for rules that can be tested reliably, but absence of such checks does not make rules optional. When an approved pattern conflicts with accessibility, safety, or data-loss safeguards, identify the conflict and perform already-authorized corrective work where governing constraints determine the repair. Do not implement inaccessible or unsafe output for consistency, claim conformance, or silently rewrite the rule. A material replacement decision remains explicit; the user's existing instruction can supply approval without a second ceremony.

## Artifact choice

| Choice | Assessment |
| :--- | :--- |
| Put design rules in `.resonance/04_systems.md` | Reject. The blueprint explicitly says that file is not a style guide; combining them would blur ownership and spread UI gates to architecture work. |
| Use `.resonance/05_design.md` as the default home | Recommend when no maintained canonical design reference exists. It fits the project context and initialization model, while leaving architecture in `04_systems.md`. |
| Keep an existing root `DESIGN.md` or design-system file canonical | Support when maintained and its approval provenance is established. Add a single pointer from the project context/contract entry point. A draft remains observed or proposed. Do not force a move or maintain competing copies. |
| Keep everything in `02_memory.md` or code | Reject as a general reference. Memory indexes lessons; code shows implementation. Neither alone records approved pattern meaning, surface scope, and exceptions. |

`.resonance/05_design.md` is therefore a default location, not a required migration or second authority. If the project already maintains a design source, use a short pointer file or existing project context entry with its exact path and canonical status.

## Small illustrative outline

This is shape only, not a prescribed style or mandatory section quota:

```md
# Application design contract
- Status / revision / approval owner / evidence
- Application and surfaces in scope; exclusions and variants
- Canonical design source and implementation references
- Approved invariants and reusable patterns
- Scoped exceptions and change history

## Approved patterns
### Record table and detail view
| Rule | Scope | Invariant | Allowed variant | Source | Verification |
| ... | ... | ... | ... | ... | ... |
```

One worked example shows how the artifact can preserve a pattern without dictating a universal look:

| Field | Example rule |
| :--- | :--- |
| Rule | `DES-001 Record inspection` (IDs are useful for shared invariants, not required on every design choice) |
| Scope | Record tables and detail inspection in the application workspace, desktop and mobile |
| Approved invariant | Keep filters and sort attached to the result set. Opening a record preserves the current query, filters, sort order, page, and selection when the user returns. |
| Approved default and selectors | Illustrative only: workspace record inspection uses the application's existing shared contextual drawer at its supported wide layout. Its approved narrow-layout variant uses a full route. The approved selector is the actual supported layout threshold and component behavior already defined in that application, cited here as `[repo breakpoint/layout rule]` and `[drawer/route component]`; do not invent a universal breakpoint. |
| Variant | The narrow-layout route is the named approved variant, not task-context discretion. Other departures require an approved variant decision. |
| Exception | A workflow that must interrupt the table may use a modal detail surface only when that workflow is explicitly named and approved. A surface “register” alone grants no override. |
| Source | Link to the actual table, filter, detail component, supported breakpoint/layout rule, and relevant tokens if they exist. Links do not authorize unreviewed changes to shared behavior. Do not copy CSS or values into this table. |
| Verification | Compare the changed screen with the named approved sibling/reference implementing the same task, including comparable empty/loading/error/success states and viewport. Verify state restoration, keyboard access, focus/return behavior, and detail readability. Missing evidence is `UNVERIFIED`. |

A second illustrative pattern chooses one product default: place filters in the shared result toolbar and preserve its placement across equivalent workspace tables. A sidebar is allowed only for an explicitly named, approved surface variant, such as `[named comparison workspace]`, with an observable selector and a reference implementation. Keep keyboard paths to open, change, and clear filters. This example does not prescribe a toolbar or palette for other applications.

## Lifecycle and approval

1. **Discover first.** Follow the deterministic lookup above. Read the entry point and only the applicable rules/source references, not every linked component or every Designer reference. This applies to local UI changes that reuse a pattern, direct frontend/mobile work, and backend changes that alter displayed names, statuses, or interactions. A backend query optimization with no user-visible effect skips it.
2. **Handle missing, broken, or proposed baselines proportionally.** A missing, broken, or `PROPOSED` reference does not stall a small bug fix. Use observed conventions as current-state evidence, state assumptions, and avoid claiming conformance. Work spanning screens or introducing a shared pattern should propose a durable baseline or rule before treating the choice as approved. Do not convert a single existing defect into product-wide policy. If two discovered sources conflict and neither has established authority, leave the choice unresolved.
3. **Approve only durable design decisions.** The design owner approves a new shared baseline and a material departure from an approved invariant or pattern. Correcting an implementation to match an approved pattern is routine work. Extending a pattern within its approved scope and constraints does not trigger a new gate. Stable IDs are optional and reserved for invariants that need traceability; not every screen choice needs a rule ID.
4. **Plan and build with scoped checks.** A UI plan/build identifies only the relevant rules and source references. Routine reuse needs no separate approval, contract revision, or full report. A proposed material change names the conflict, current behavior, target, transition, verification, and required owner decision. An advisory-looking or nondeterministic check cannot waive an approved rule.
5. **Review evidence, not assumptions.** Review and QA compare a UI change to applicable rules and a named approved sibling/reference for the same task under comparable states and viewport. A single isolated screenshot can show legibility, but not cross-screen consistency. Use browser, screenshot, or native-platform evidence appropriate to the surface; use Figma only when the project has an approved Figma target. Insufficient visual or behavioral evidence stays unverified. Keep findings in the existing severity taxonomy.
6. **Record narrow exceptions.** Name the surface, affected rule, reason, accountable role, risk, allowed duration or reconsideration trigger, and removal condition. A mobile route or distinct surface register that fits an approved variant is not an exception.

## Smallest implementation map if approved

These are future touchpoints, not changes made here. Keep `.forge` sources canonical, regenerate `.agents` and generated routing through existing tools, and leave this repository's `.resonance/` template clean. Preserve the actual plan/build job contracts: their current artifacts are `implementation-plan` and `build-evidence`/`build-result`; UI rule references can live in those existing artifacts and evidence. Do not add a `design_scope` typed field unless a concrete job-composition consumer needs one. The Designer remains a knowledge skill, not a new command, orchestration skill, or mandatory handoff.

| Owner | Candidate files | Minimum work |
| :--- | :--- | :--- |
| Project context | `.forge/templates/05_design.md`, `.resonance/05_design.md`, `.forge/tests/test_design_template.py` | Add the optional default scaffold and parity/contract check. Support a pointer-only form for an existing canonical source. No prescribed palette or automatic approval on discovery. |
| `/init` and routing | `.forge/skills/ops/core/skill.tmpl.md`, root `AGENTS.md`, generated command/router outputs only if needed | Follow explicit declaration -> `05_design.md` -> local discovery. Offer a baseline only when shared UI work justifies it. Update Designer's description for natural-language discovery, keeping `archetype: knowledge`, existing `/design`, and direct-work routing. |
| Design owner | `.forge/skills/design/designer/skill.tmpl.md`, `.forge/skills/design/designer/references/design_system_generation_protocol.md`, existing evals | Define approval provenance, shared defaults, observable variants, recovery, and evidence. Cover approved-source lookup, local reuse without a gate, app isolation, conflict handling, pointer adoption, and exceptions. Keep at least six distinct behavior cases; add only uncovered cases. |
| Plan/build | `.forge/skills/strategy/plan/skill.tmpl.md`, `.forge/skills/engineering/build/skill.tmpl.md` | Add short prose to existing UI planning/build steps and implementation-plan/build evidence artifacts. Evaluate applicability by visible effects. Do not widen typed job output schemas or reuse `blueprint_scope` for design. |
| UI implementation | `.forge/skills/engineering/frontend/skill.tmpl.md`, `references/design_tokens_protocol.md`, `.forge/skills/engineering/mobile/skill.tmpl.md` | Require scoped source lookup for web and native UI. Resolve absolute token mandates into reuse of the project's value owner; add semantic tokens only for an actual shared need. Do not require a token engine or CSS in native code. |
| Review and QA | `.forge/skills/ops/reviewer/skill.tmpl.md`, `.forge/skills/ops/qa/references/design_validation_protocol.md` | Compare to a named sibling/reference for the same task and states. Replace assumed Figma matching with project-appropriate evidence; mark missing proof unverified. |
| Upgrade preservation | Existing updater tests and project-preservation profile, as applicable | Add a preservation check proving that consumer-authored `05_design.md` content and pointer-only files are excluded from framework-upgrade writes. Reuse the existing updater and ownership boundary; do not create a new updater. |
| Generated outputs | `.agents/skills/**`, generated `AGENTS.md` sections only as emitted by Forge | Compile and validate from canonical sources; do not hand-edit generated copies. |

Do not add a new design skill or command, global lint, mandatory contract for every project, CSS/token parser, or design-specific typed job schema without evidence of a real consumer. Do not add automated enforcement unless an approved rule can be checked reliably.

## Reconciliation after independent review

The first review found that loose variant language could let equivalent screens choose different patterns while both appeared compliant. The examples now choose a concrete product default and name observable variant selectors; adopters must replace illustrative placeholders with actual components and supported layout rules. The review also identified approval provenance and mutable-link risks, nondeterministic source discovery, effects beyond UI file paths, hard constraints overriding defective design rules, and unnecessary orchestration/schema growth. These are addressed above through explicit authority, deterministic lookup, narrow read scope, visible conflict handling, and reuse of existing knowledge and job artifacts.

## Evidence and limits

This is a repository-grounded investigation on branch `codex/eval-coverage-six`. The four pre-existing untracked files under `docs/research/` and the public `.resonance/` scaffold were left untouched. The report is under `docs/` per `AGENTS.md:46-50`, which defines the framework-repository exception. No external research was needed. No tests were run because this is a proposal with no executable change. The recommendation treats an empty `05_design.md` as a discoverable default; adopters with a maintained canonical design file keep that source and use one pointer, with no forced migration.
