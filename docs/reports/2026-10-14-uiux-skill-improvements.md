# UI/UX skill improvements

**Status:** Canonical changes and generated outputs are complete. Structural and repository checks pass. A fresh-agent formative walkthrough compared the original and candidate specifications, but no scored behavior-performance or user-usability result is claimed.

## Scope and changes

The five owning skills now use a task-first decision process while keeping their responsibilities distinct. `design/designer` owns general interface hierarchy and craft; `engineering/frontend` and `engineering/mobile` apply that judgment to web and native implementation; `marketing/conversion` owns commercial friction and action choices; `ops/page-audit` frames the page job, separates observations from assumptions, and delegates detailed craft and conversion decisions.

The designer template now puts task evidence, information allocation, control and surface choice, action safety, state recovery, and verification before visual polish. It preserves positive craft guidance for color roles, spacing and grouping, typography, and shape relationships. Consistency applies within a product's own system. Flat, outlined, surface-based, or shadowed treatments can all fit; palettes, typefaces, radii, density, and layouts do not transfer as a framework house style. Optical adjustments remain subordinate to accessibility, platform, target-size, and layout constraints.

References now present OKLCH as an optional color tool, allow achromatic or tinted neutrals and pure black or white where the brief, device, and contrast needs support them, and treat depth and shadow recipes as optional. The former five-archetype style matrix is now a set of visual-direction questions for type, palette roles, shape, density, composition, and depth. Design-system documentation is optional and scoped to work that needs shared foundations. Spacing and alignment guidance allows borders, surfaces, deliberate asymmetry, and density where the task benefits. Familiar patterns and design-register examples are prompts, not universal styling rules.

Frontend guidance maps only reachable states and checks preserved input, focus semantics, keyboard and screen-reader paths, responsive content flow, dense comparison, and dialog recovery where applicable. Web Core Web Vitals remain page-level field goals at the 75th percentile when measurable: LCP ≤ 2.5s, INP ≤ 200ms, and CLS ≤ 0.1. Components use relevant contextual budgets.

Mobile guidance ties offline-first behavior to the product contract, selects motion by input and purpose, and checks reach in the expected posture and keyboard-open state. It distinguishes WCAG CSS pixels from native platform point/dp guidance. Launch and frame budgets are measured on supported devices; fixed spring presets and a fixed thumb-zone percentage are not requirements.

Conversion guidance asks for audience, offer, traffic intent, and decision stage; it reports up to three evidence-backed frictions and does not invent sample sizes, deadlines, proof, or conversion penalties. Page-audit uses above-the-fold and time-to-value checks for marketing pages where relevant, preserves product-workspace actions, and ranks a lead priority alongside other needed findings.

Six synthetic public eval cases were added across the five owning skills, including dense operations work, contrasting visual briefs, a mobile keyboard/destructive-action workflow, multiple valid product actions versus a commercial signup path, and page-audit delegation. Existing eval expectations were corrected where they encoded fixed motion, forced singular actions, generic offline/launch assertions, or unsupported exact-one-change criteria. Planted-defect safety and accessibility expectations remain.

The four downstream skill trees were snapshotted before edits in private temporary evidence, which is not included here. Generated `.agents/skills/**` resources, skill manifest, job-composition output, skill graph, command shims, and eval integrity manifest were regenerated from canonical sources. No generated files were edited by hand.

## Evidence and reasoning

The plan's research note, [First-principles guidance for task-first interfaces](../research/2026-10-14-ux-first-principles.md), bounds common HCI rules: Fitts' and Hick-Hyman describe conditional relationships rather than universal target sizes or option caps; Miller's 7±2 is not a UI quota; and familiar scan patterns and fixed color/layout ratios are not validated recipes. The implementation uses task frequency, consequence, uncertainty, and recovery cost as qualitative questions, not an unvalidated composite score.

The style review applies the same evidence discipline to visual craft. Semantic color, local token consistency, readable type, intentional spacing and grouping, coherent shape relationships, and deliberate layering remain useful craft principles. Specific color spaces, temperature, font pairings, corner radii, whitespace ratios, and shadow recipes are examples to select from the project and brief. Contrast and applicable accessibility requirements remain gates.

## Formative comparison

A blind, qualitative review compared the baseline and candidate specifications on three synthetic tasks. It found a tie on all three, with meaningful alternative decisions rather than a general winner:

- **Daily case queue:** both preserve the comparison task and case context. One spec surfaces overdue/high-impact items by default; the other preserves the user's chosen ordering. The task does not settle that tradeoff. Row density and keyboard navigation still need prototype checks.
- **Permanent workspace deletion:** both identify the target and consequence, require a typed name, provide a safe exit, and cover focus and recovery. A deletion route followed by a final modal and a focused settings modal are both plausible; the task does not dictate the number of steps.
- **Plan comparison:** both keep three plans and their limitations available and support later discussion. A scrollable comparison structure and roomy plan sections with direct selection are both plausible on mobile. Sharing and printing require product capability checks; missing details must remain distinguishable from exclusions.

This was a formative comparison of written specs, not a usability study. No interface was implemented, users performed no tasks, and the review collected no completion times, error rates, or calibrated score. Its private temporary samples are not included in this repository. The findings support task-specific tradeoffs and ties, not superiority or measured lift.

## Verification

- `python3 .forge/validate_library.py --strict`: **PASS**, 73 skills, 0 errors, 0 warnings.
- `python3 .forge/validate_skill.py --all .agents/skills --strict`: **PASS**, 73 skills, 0 errors, 0 warnings.
- `python3 .forge/run_evals.py --all --check`: **PASS**, 347 cases, 0 structural problems. This is fixture structure only, not behavior scoring.
- `python3 .forge/eval_integrity.py`: **PASS**, 459 oracle files, 0 problems.
- `python3 .forge/job_composition.py --check`, `python3 .forge/skill_graph.py --check`, `python3 .forge/routing_eval.py --check`, and `python3 .forge/orch_eval.py --check`: **PASS**. Routing covers 49 cases across 25 clusters; orchestration covers 23 cases.
- `python3 .forge/doc_drift.py`: **PASS**, 73 skills and 38 commands agree across docs and manifests.
- Forge build and command dry-runs: **PASS**, generated outputs are fresh.
- `python3 .forge/tests/run.py`: **PASS**, 323 tests, 1 skipped.
- `git diff --check` and the task-scope fingerprint scan: **PASS**. The marker scan checked 119 changed task files, including generated outputs, relevant research notes, and new fixtures; four pre-existing unrelated research notes were excluded. It found no source markers. The stock scanner also flags a source marker in one of those excluded unrelated notes.

## Limits and pending work

No governed or scored holdout evaluation was run. A separate fresh-agent formative specification walkthrough occurred as described above; it was a qualitative comparison, not an approved answerer/judge evaluation with a protected holdout or calibrated scoring protocol. Structural checks cannot establish that models apply the guidance correctly. The formative comparison tied on all three synthetic tasks and supplies no evidence of candidate superiority. A later governed run should use an unseen holdout and qualified judge; implemented interfaces still need representative user walkthroughs, including responsive, keyboard, screen-reader, and recovery paths.
