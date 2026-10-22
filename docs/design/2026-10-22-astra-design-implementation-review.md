# Astra implementation review: project design contract

**Verdict: ACCEPT WITH EVIDENCE LIMITS.** The three original P2 findings are resolved, and final integration checks pass. Latest response-level evidence is **22 pass, 2 partial across 24 unique cases**, with **20/20 deterministic output checks passing**. This is a behavioral smoke result, not measured lift or live-product validation. The original failures and their dispositions remain below.

## Final implementation assessment

The implementation addresses the actual consistency failure: equivalent tasks must use a concrete approved default, and a variant needs an observable, approved selector. It does not merely ask two designers to make independently usable screens. Explicit declarations, an optional `05_design.md`, and local discovery form a repeatable lookup. Unfilled scaffold content falls through; authored proposals and broken pointers keep their status. Current source values cannot approve changes to their own meaning.

Ownership remains in the Designer knowledge skill. Core, plan/build, frontend/mobile/backend, reviewer, and QA reach the same contract through short conditional hooks. Effects determine applicability, including backend status names; invisible internal work skips it. The updated Build sequence explicitly resolves the entry point before implementation and uses browser evidence for web and device/simulator evidence for native. The separate system-generation reference now points conceptually to that same contract instead of defining a second exception authority. General craft remains in existing Designer references. No new mandatory palette, token layering, global breakpoint, registry, parser, schema, conductor, or approval ceremony was introduced.

The public scaffold is neutral and matches its template. Existing project sources remain canonical when their approval is established. Consumer design content lies outside updater ownership; the executed preservation test confirms both authored-rule and pointer cases.

### Final finding dispositions

| Finding | Disposition and evidence |
| --- | --- |
| P2, overlapping approved rules | **Resolved.** `project_design_contract.md` explicitly leaves overlapping conflicting rules unresolved without specificity/document-order priority. The ordinary approved fixture is consistent. New Designer 25 identifies both conflicting rules and the owner decision needed. |
| P2, unsupported shared-pattern recommendation | **Resolved.** Case 19 now supplies observed Customers/Invoices/Audit tasks and synthetic usage facts. The fresh answer proposes toolbar lookup and a bounded reconciliation-sidebar candidate, names the existing owner, distinguishes observations from approval, and leaves old screens unchanged. |
| P2, incorrect provenance | **Resolved.** Fresh cases 23/24 cite the actual DEC-244 and DEC-252 fixtures. Declared-source priority and broken-pointer treatment remain correct. |
| P2, cross-case variant carryover in first QA rerun | **Resolved for the isolated response; recurrence remains a model risk.** The batched QA answer imported a narrow-layout approval absent from its own input. The isolated QA answer restricts the route to the supplied full-record-editing exception and identifies Suppliers inspection as a mismatch. The canonical contract and QA rubric now explicitly forbid importing another task's variant. |
| P2, browser-only Build visual-check wording, identified during integration | **Resolved at source.** Build now distinguishes browser and native device/simulator evidence and marks unavailable comparison evidence unverified. This final prose correction has not received another behavior run. |
| P3, integration freshness/link/format errors | **Resolved.** Final independent generation freshness, library scan, oracle integrity, and diff checks pass. The onward-link correction uses the existing owning-skill reference, without a validator exemption. |

No P0 or P1 issue was identified. No unresolved product-correctness issue remains in the inspected source. The two partial behavioral responses are verification limits, not waived acceptance evidence.

### Final behavioral grading and acceptance coverage

Use the original answers for unchanged cases; supersede 11/19/23/24/25 and Backend 07 with `/tmp/resonance-design-behavior-rerun.md`; supersede QA 08 with `/tmp/resonance-design-qa08-isolated.md`; supersede Core 08 with `/tmp/resonance-design-core08-final.md`; use `/tmp/resonance-design-native-build-isolated.md` for the latest Designer 20 and Build 09 attempts.

- **22 pass:** Designer 11–19 and 21–25; Frontend 09; Mobile 07; Backend 07; Core 07/08; QA 08; Reviewer 07; Plan 07. These are response-level decisions, not executed UI implementations.
- **2 partial:** Designer 20 still does not explicitly constrain native departures to approved platform variants. Build 09 still does not demonstrate the source-lookup step or explicitly require native comparison evidence. Both isolated reruns retained these omissions. The later Build source correction addresses the latter instruction gap, but is not counted as a new passing response.
- **20/20 deterministic checks pass** against the latest answers and current cases. Planner's original literal `user-visible` check was replaced by `marketing`; the semantic rubric was unchanged. This is correction of a brittle check, not measured quality lift.

All fourteen prior acceptance scenarios now have substantive evidence at the owning boundary: scenarios 1–11 and 13–14 have the specific response-level coverage mapped in the initial table below, with case 1 replaced by corrected Designer 11, case 9 replaced by evidence-backed Designer 19, case 11 supplemented by direct Backend 07, and case 13 replaced by final Core 08. Scenario 12 has executed updater preservation evidence. Mobile 07 supplies explicit native-selector and native-evidence coverage for scenario 10 despite the two combined-answer partials. Supplemental lookup cases 22–24 and overlap case 25 pass. This is complete scenario coverage, not proof that all product behavior has been executed.

The isolated QA response catches the actual Suppliers divergence and rejects draft-Figma authority. Final Core 08 explicitly reconsiders the check when user-visible interface behavior appears. These fixes were verified from actual answers, not inferred from updated prompts or case counts.

### Verification boundary

Independently executed: template tests, updater preservation, full-library generation freshness checks, contract-link resolution, selected reference/eval byte parity, all-eval structural checks, and deterministic checks on the model outputs. The final checks report **73 generated skills fresh**, **library scan zero errors/zero warnings**, **485 eval cases with zero structural problems**, **638 oracle files with zero problems**, and a clean `git diff --check`. These checks ran after the final Build and reference edits. Parent-reported full test result is **353 tests, 1 skipped**; this reviewer did not rerun that suite.

No score-run baseline/with-without comparison was performed. The reruns are targeted corrections selected after failures, so neither their pass count nor the changed rubric/checks supports a causal lift claim. No real app, browser/native capture, deployed product, or consumer upgrade environment was inspected.

## Scope and method

Read `AGENTS.md`, the public state/memory scaffold, the proposal, the prior Astra decision review and its fourteen acceptance scenarios, canonical skill changes, untracked templates/evals/fixtures, generated-file ownership, and the updater/eval runtime. Reviewed source beyond `git diff`, which excludes the new files. No product contract or running application was supplied.

The source review covers Designer, core initialization, plan/build, frontend/mobile/backend, reviewer/QA, token ownership, design-system generation, and the public scaffold. Upgrade ownership is defined by `resonance_update.py::PROFILE_ROOTS` and `managed_path`; both profiles exclude consumer design content. No new updater, typed job schema, parser, skill archetype, or dependency is needed.

The behavioral review independently compares `/tmp/resonance-design-behavior-answers.md` with the actual eval queries, supplied fixture bytes, and expected-behavior rubrics. Correct recommendations are distinguished from executed implementation. A valid JSON case or an answer that repeats a principle does not demonstrate the associated product behavior.

## Findings raised during implementation

1. **P2, Product Correctness: conflicting approved rules needed an explicit rule.** The prior decision review required overlapping approved rules to remain unresolved. The first canonical reference handled source/declaration conflicts but omitted conflicts inside one approved contract. The initial approved fixture contradicted itself about the narrow-layout selector, and Luna selected the table without acknowledging the scope conflict. Requested an explicit conflict rule and a separate adversarial case, preserving the ordinary selector test.
2. **P2, Verification Quality: the shared-pattern case lacked the evidence its rubric demanded.** Designer case 19 originally had no files and no actual placements, task facts, or representative component. Its answer explicitly declined to choose a concrete default. This was sensible under the input but did not satisfy the required outcome. Requested a small fixture and a fresh answer without weakening the rubric.
3. **P2, Verification Quality: provenance assertions were wrong.** The initial case 23 answer attributed the declared source to DEC-231 although the supplied source cites DEC-244. Case 24 cited DEC-244 although the pointer cites DEC-252. Lookup behavior was otherwise correct. Requested fresh responses against the actual fixtures, not silent editing of the model's answer.

These are the original findings; final dispositions appear above. No P0 or P1 finding was identified.

## Initial behavioral grading

Grades apply to the original 22 answers, not later reruns. **Pass** means the response demonstrates the named decision behavior; it never means the requested implementation was executed. **Partial** identifies an omitted rubric outcome, an invalid test premise, or incorrect fixture evidence. No aggregate score is reported because the defects include test construction and omitted evidence, not just model quality.

| Case | Grade | Independent assessment |
| --- | --- | --- |
| Designer 11, approved task-family default | Partial | Correctly rejects the unqualified Suppliers route, cites the actual selector and sibling, but silently chooses one of two contradictory approved statements. Rerun after fixture correction; retain conflict as its own case. |
| Designer 12, scoped registers and apps | Pass | Keeps marketing/workspace scopes and second-app ownership distinct. |
| Designer 13, routine reuse | Pass | Uses the existing component and sibling, permits the local fix without a new gate, and names a focused check. |
| Designer 14, mutable source authority | Pass | Rejects self-approval by the modified theme and preserves the approved role/accessibility; correctly withholds a measured contrast claim. |
| Designer 15, unapproved sources | Pass | Reads the two draft directions accurately, establishes neither as approved, and leaves the choice unresolved. |
| Designer 16, accessibility conflict | Pass | Refuses hidden keyboard focus and does not call the corrective deviation conforming. |
| Designer 17, missing visual evidence | Pass | Separates source reuse from rendered conformance and requests comparable state/viewport evidence. |
| Designer 18, brownfield repair | Pass | Permits the local alignment repair from observed conventions without creating product policy. Actual repair was not executed. |
| Designer 19, shared-pattern proposal | Partial | Explicitly declines to choose a default because the case lacks task/component evidence. This misses two core rubric requirements. |
| Designer 20, native/backend effects | Partial | Correctly includes the visible rename, excludes the internal index, and uses native evidence; does not explicitly constrain native departures to approved platform variants. |
| Designer 21, multiple apps | Pass | Evaluates the shared change independently against both contracts and requires authorized variants. |
| Designer 22, unfilled scaffold | Pass | Correctly reaches the maintained approved source, cites DEC-231, and does not treat placeholders as authority. |
| Designer 23, declared-source priority | Partial | Correct lookup and conflict reporting, wrong approval identifier for the declared source. |
| Designer 24, broken pointer | Partial | Correctly refuses replacement by convenient local notes, wrong approval identifier for the pointer. |
| Build 09 | Partial | Correct default/theme/status/index decisions; does not demonstrate source resolution or explicitly require native comparison evidence as its rubric asks. |
| Frontend 09 | Pass | Uses the exact declared source, keeps the repair local, and preserves separate app intent without a new gate. |
| Mobile 07 | Pass | Applies the documented compact-width sheet selector and requires native evidence; does not substitute browser proof. |
| Core 07 | Pass | Preserves draft provenance and avoids approving/migrating sources. No initialization was executed. |
| Core 08 | Partial | Correct headless decision, but omits explicit reconsideration if user-visible interface behavior is introduced. |
| QA 08 | Partial | Correctly withholds visual conformance and rejects draft Figma authority. Its divergence-detection rubric clause is not exercised by the supplied conforming scenario. |
| Reviewer 07 | Pass | Distinguishes intent from linked values, checks the visible rename, excludes the index, and withholds visual proof. |
| Plan 07 | Partial | Correct behavioral scope/defaults, but fails the authored literal `user-visible` check. This is a lexical check failure, not evidence of an incorrect design choice. |

The direct backend case and added overlap case were not present in this initial answer set. The reviewer did not manufacture substitute answers for them.

## Prior fourteen-case acceptance coverage

| Prior case | Initial evidence and remaining boundary |
| --- | --- |
| 1. Equivalent record inspection | Designer 11 demonstrates the intended default decision, but its contradictory fixture requires correction and rerun. |
| 2. Marketing/workspace scopes | Designer 12 demonstrates bounded scope and no register-based exemption. |
| 3. Local reuse without ceremony | Designer 13 and Frontend 09 demonstrate proportional reuse. |
| 4. Mutable token authority | Designer 14 and Reviewer 07 demonstrate effect-based review. |
| 5. Draft and Figma disagreement | Designer 15 and Core 07 demonstrate unresolved authority. |
| 6. Approved bad focus rule | Designer 16 demonstrates accessibility conflict handling. |
| 7. Missing browser evidence | Designer 17 and QA 08 refuse a visual pass. |
| 8. Small brownfield repair | Designer 18 allows repair without creating a baseline. |
| 9. New shared brownfield pattern | Not complete: case 19 lacked evidence for a concrete proposed default/reference. |
| 10. Web/native shared intent | Mobile 07 substantively demonstrates approved platform selector and native evidence; the combined Designer/Build summaries are weaker. |
| 11. Visible backend rename | Designer 20 and Reviewer 07 demonstrate classification. The direct Backend entry hook and new case still need final verification. |
| 12. Consumer upgrade | Executed updater test passes both authored-content and pointer cases; ownership inspection supports both installation profiles. |
| 13. Headless project | Core 08 demonstrates no invented screen contract. Its future-applicability clause remains omitted. |
| 14. Distinct app brands | Designer 12/21 and Frontend 09 demonstrate separate authority despite shared code. |

All fourteen scenarios had an intended owner, but the initial evidence was not a complete fourteen-case acceptance pass. The final section records the targeted gap closures. The source-level requirements remain stronger than the available product execution evidence.

## Checks executed independently

- `python3 .forge/tests/test_design_template.py`: **3 passed**. The public file equals its canonical template, remains optional, and supports a pointer without prescribed product styling.
- `python3 .forge/tests/test_update.py UpdateTests.test_consumer_design_entry_survives_source_upgrade`: **1 passed**, with authored-rule and pointer subcases. The test performs initial install and a subsequent update and checks bytes plus planned writes/removals/conflicts.
- Inspected the updater's source and compiled profile boundaries. Consumer `.resonance/05_design.md` is outside both write sets; canonical project documentation is not newly claimed by this change.

## Evidence limits

These model answers are a behavioral smoke exercise. They are not a randomized with/without comparison, a Forge score run, measured lift, implementation execution, or proof of actual cross-screen consistency. Most cases supply a short scenario rather than executable UI code. No browser or native screenshot, real product approval history, installed consumer session, or live product task was tested.

The initial planner case 07 answer follows the intended scope but fails its literal `contains_all` check for `user-visible`, because it says `visible`. Core case 08 correctly avoids inventing a screen contract but omits the rubric's explicit revisit-if-UI-is-added point. QA case 08's query contains conforming drawers and an allowed editor route, so it cannot prove the rubric's detection of an inspection-route violation; Designer case 11 is the substantive owner of that adverse input. These must not be hidden inside a blanket all-cases-pass claim.

**DONE_WITH_CONCERNS:** source review, targeted response grading, and final generated-artifact validation are complete. No unresolved P0–P3 implementation finding remains. Two combined behavioral answers remain partial, with the relevant acceptance requirement covered by Mobile 07.

Skipped shipping, commits, infrastructure access, live-product validation, and measured-lift testing. Real application consistency remains unverified until the contract is exercised against rendered product evidence.
