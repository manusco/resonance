# UI/UX skill evaluation plan

**Date:** 2026-10-14 | **Status:** Research plan, no skill or eval fixtures changed
**Purpose:** Define acceptance cases and a credible comparison protocol for improving the design, frontend, mobile, page-audit, and conversion skills.

## Recommendation

Add one representative, task-grounded case to each of the five skills, then compare the same Luna answerer in paired cold and skill-context arms using the existing Forge scorer only after a protected holdout, judge calibration, and approved operating contract exist. Keep the public cases useful for authoring and structure checks. They are not a baseline and must not produce a lift claim.

Evaluate observable decisions and consequences: what the user needs to find, what stays visible, which action is safe, how errors recover, and what changes at a small viewport. Do not grade output for merely naming Gestalt, Hick, Fitts, Miller, LIFT, or other frameworks. Score a principle only when the response applies it correctly to the stated task and identifies evidence that could disprove its recommendation.

## Current evidence and boundaries

- `.resonance/01_state.md` and `.resonance/02_memory.md` are template placeholders. There are no `.resonance/memory/` leaf notes. The ledger recall for “UI UX evaluation design skill evals HCI” returned only scaffold references, with no settled project decision.
- The five skills have 24 public eval cases: designer 8, frontend 6, mobile 4, page-audit 4, and conversion 4. Current cases cover craft, states, attention path, touch, page-audit theater, trust, and offer problems. They have little direct coverage of dense operational tables, contextual form surfaces, and evidence-bounded HCI heuristics.
- `python3 .forge/run_evals.py --all --check` passed: **341 cases, 0 structural problems**. This verifies fixture structure only.
- The scorer's current checks are `regex_absent`, `regex_present`, `contains_any`, `contains_all`, `section_present`, and `max_lines`. These are literal or syntactic checks; none proves a semantic design decision. Rubric items are judged by a model and then averaged equally with deterministic checks.
- `--score` uses one answerer command in both arms, once with the skill body and once without it. It alternates arm order across repetitions and enforces at least three generations per arm. It requires an external holdout directory, external evidence root, baseline ID, distinct answerer and judge commands, and distinct model IDs. Human-gold judge calibration is required by the private baseline protocol but is not performed by the runner.
- No Luna model configuration, holdout, evidence root, baseline ID, or machine config is available in this session. The `claude` and `codex` CLIs exist, but their availability says nothing about Luna access. No provider credentials or config contents were read, and no live model run was made.
- `docs/research/2026-10-14-ux-first-principles.md` already documents the evidence limits of Fitts, Hick, Miller's 7±2, hierarchy claims, and several popular design rules, plus task-first examples and falsification criteria. Use it as the evidence source when revising skill references.

## Acceptance cases to add

Each new case should use a realistic synthetic context with enough detail to make different recommendations distinguishable. Keep private validation cases separate from the public prompts after authors have seen these examples.

| Skill | Synthetic task and required observable behavior | Failure condition |
| --- | --- | --- |
| `design/designer` | Specify a daily operations queue with realistic row density, status, owner, due time, amount, and several actions. State the primary user task and what evidence makes fields/actions worth keeping visible. Preserve side-by-side comparison when the task requires it. Adapt the composition at 360 CSS px and explain any hidden controls. For a rare permanent bulk delete, show the exact target and consequence, safe exit, and a confirmation or undo choice justified by recovery risk. | Replaces the working table with cards or strips context without addressing comparison; promotes every action equally; invents product facts; treats one HCI law or pixel/count threshold as proof. |
| `engineering/frontend` | Given a product screen with cluttered global chrome, a dense table, and a multi-field edit action, propose or implement the narrow-screen path. Keep the frequent task and status findable, preserve entered values on validation failure, expose keyboard focus/order, and pick inline, dialog, drawer, or full page from task interruption, context retention, form size, and viewport. | Desktop chrome is merely compressed; important table data/actions become inaccessible; focus or user input is lost; surface choice is justified by a universal rule instead of the provided workflow. |
| `engineering/mobile` | Design the same workflow for a 360 px touch viewport, including keyboard-open form state and a high-risk destructive action. Put frequent actions within comfortable reach, preserve status/context, provide a safe cancel path, and specify target size using the relevant platform/accessibility criterion. | Essential action is hover-only or unreachable under the keyboard; a risky action is adjacent to the common action without a guard; uses a desktop layout at smaller scale; cites touch-size guidance without naming its applicable standard/context. |
| `ops/page-audit` | Audit a supplied product-workspace page that combines persistent navigation, a daily queue, and a form. Separate the page's product job from a marketing conversion goal. Report evidence observed versus unavailable, a narrow-viewport failure hypothesis, one highest-impact change, and a falsifiable task measure such as correct disposition time or wrong-action rate. | Applies “one CTA” or landing-page LIFT mechanically to a multi-action product workspace; fabricates page evidence; declares success from cosmetic changes or an unmeasured HCI slogan. |
| `marketing/conversion` | Compare two contexts: a marketing pricing page whose truthful primary action is signup, and an in-product workspace where the user must choose among several legitimate actions. For the page, recommend a clear primary CTA and urgency only if the brief supplies a verifiable deadline or constraint. For the workspace, preserve task-specific actions and do not import conversion-page singularity. For a form, explain what evidence would justify inline validation and whether a dialog/drawer/full page fits the task. | Invents scarcity, proof, or conversion rates; presents “each field costs 3–5%” as a universal measured law; forces one CTA onto the product workflow or recommends a surface without context. |

The scenarios intentionally overlap at handoffs. The designer case tests the decision model; frontend and mobile test whether advice survives implementation constraints; page-audit tests evidence discipline; conversion tests register boundaries and truthful persuasion. Avoid copying one prompt across all skills because that would reward repeated boilerplate rather than the distinct job of each skill.

## HCI-claim scoring

Score reasoning, not citation vocabulary. A strong answer should:

1. Name the user's task, frequency, consequence, and recovery cost when those facts are supplied.
2. Tie layout or interaction choices to the task and the information the user needs at the point of action.
3. Treat laws and heuristics as bounded models. State relevant conditions or ask for a missing fact when it changes the decision.
4. Avoid universal numeric guarantees unless it gives a relevant standard or source and applies its scope correctly.
5. Give one observable prediction and a failure condition. Prefer task completion time, error rate, first-action success, missed discovery, or recovery success over “feels cleaner.”

Use the existing UX research note's evidence table as the oracle for the public myth case. In particular, do not accept Miller's 7±2 as a menu/field cap, Hick-Hyman as a mandate to hide choices, Fitts as proof of one universal pixel size, “3 clicks to value” as a universal usability rule, “3–5% per field” as an established conversion constant, or “one primary CTA” as the right model for every product surface. Preserve actual accessibility requirements and platform conventions with their stated scope.

One suitable shared prompt seed is: “A team argues that the 7±2 rule means this daily case screen may show no more than seven fields. Operators must compare account, payment, and refund status before choosing among four valid dispositions. Recommend what stays visible and what may be disclosed, name the task evidence needed, and state how you would detect a bad choice.” A good response explains why concurrent comparison and task risk matter, treats seven as no quota, and proposes a falsifiable check. A keyword-only response that repeats “Miller's law” fails.

## Rubric and deterministic checks

Keep each semantic rubric to roughly four to six independent items. Phrase items so equivalent wording passes:

- “Preserves the status and context needed to choose the correct next action.”
- “Explains what becomes hidden at 360 CSS px and how a user can still find or compare it.”
- “Chooses the form surface from task context and explains keyboard, focus, and recovery behavior.”
- “Makes destructive scope and consequence explicit and provides a safe exit or justified recovery path.”
- “Distinguishes observed facts from assumptions and gives a measurable prediction with a failure condition.”
- “Uses a heuristic as a conditional explanation, not as a universal numeric law.”

Use deterministic checks only for format-independent hard constraints with low false-positive risk. Good candidates include absence of em/en dashes where repository voice requires it, an exact required output heading only when the case explicitly requires that heading, and a small maximum-line limit only for a case that requests a short answer. Prefer `regex_absent` for known prohibited tokens over exact quoted phrases. Do not make scoring depend on terms such as “Hick,” “drawer,” or “primary CTA,” because a correct answer may use different words or quote the anti-pattern while rejecting it. Keep semantic choices in `expected_behavior` and have the independent judge read the query and the complete answer.

The existing scorer averages all rubric and check items equally. It has no severity weights or per-case hard-fail field. Therefore, a high-risk deletion case cannot be declared safe from an aggregate fraction alone. For formative human review, record any unsafe destructive-action recommendation as a blocking failure separately from the score. Do not duplicate that criterion to simulate weighting. A future harness change would be needed before automating severity gates.

## Comparison protocol

1. **Authoring gate:** Add public cases and run `python3 .forge/run_evals.py --all --check` (or `npm run eval`). This only proves structure, binding, and supported check syntax.
2. **Holdout:** Before measuring lift, write unseen sibling scenarios outside the repository. Vary task frequency, row density, consequence/reversibility, viewport, form complexity, and whether the surface is brand or product. Do not score the exact public authoring prompts as independent validation after skill authors have seen them.
3. **Judge qualification:** Use a judge different from the Luna answerer. Blind and randomize arm labels, reverse response order, include human-labeled good and bad samples, agree a tie rule, and set an agreement threshold before looking at scores. Disqualify an uncalibrated judge.
4. **Run:** After an approved evaluation operating contract names the host, model identities, dataset custody, sample cap, retries, spend ceiling, wall-clock limit, and evidence age, run paired cold/skill-context arms with at least three generations per case. Pin the repository revision, model revisions, prompt hashes, and case hashes. Use an external evidence root and protected holdout.
5. **Interpret:** Report per-skill and per-scenario pass fractions, cold/skill deltas, uncertainty, regressions, judge agreement, measured cost, and limitations. Flag a case as non-discriminating if cold answers already pass, consistent with the runner. Never call a structure pass or an uncalibrated judge result “lift.”

This comparison evaluates the effect of including a skill body in the prompt for one configured answerer. It does not test host routing, actual specialist invocation, tools, rendered UI, or usability with people. If the intended claim is that two separately configured autonomous agents behave differently, the current `run_evals.py` is not that agent-level harness; document and scope a separate controlled run rather than implying the paired scorer proves it.

## Supported runner surface

`python3 .forge/run_evals.py` supports a skill path or `--all`, `--changed [ref]`, `--check`, `--score`, `--limit N`, `--parallel N`, `--model-cmd`, `--judge-cmd`, `--reps N`, `--threshold`, `--model-id`, `--judge-id`, `--holdout-dir`, `--evidence-root`, `--baseline-id`, `--promotion`, `--model-revision`, `--judge-revision`, and `--seed`. `--score` cannot be combined with `--check`. It replaces selected public cases with JSON files from an external holdout and forces at least three reps. The holdout case fields are `skill_path`, `skill`, `query`, non-empty `expected_behavior`, and optional `checks`. The scorer's documented `checks` kinds are the six listed above.

`improve.py calibrate` measures answer/judge pipeline variance; it does not human-calibrate the judge. `improve.py remeasure <skill-path>` provides a paired comparison against a baseline ref, but a changed eval set resets the measured baseline. Do not treat its statistical floor as evidence that rubric judgments match human judgments.

## Completion evidence

The design plan is complete. The only executed check was the deterministic all-case structure gate, which returned `341 cases | 0 structural problem(s)`. No eval fixtures or skill text changed, no provider command ran, no score or lift was produced, and no credentials or private configuration contents were inspected. The next concrete work is to edit the five skills' public cases and revise any overclaimed heuristic language against the cited UX research note, then prepare a governed private behavioral baseline before making a lift claim.
