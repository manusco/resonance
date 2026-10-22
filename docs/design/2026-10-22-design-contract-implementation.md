# Design contract implementation plan and evidence map

**Status:** Complete. This plan applies the revised contract in `2026-10-22-design-contract-investigation.md` and Astra's required corrections in `2026-10-22-astra-design-contract-review.md`. The framework repository's `.resonance/` remains template-clean.

## Scope and success

Add one optional project design-contract entry point, preserve existing design-source ownership, and bind UI-scoped work to the applicable approved choices with proportional checks. A discovered source is evidence, not approval. Discovery is deterministic: an explicit application source declaration in loaded project instructions, then `.resonance/05_design.md`, then maintained local sources for the affected app. Do not duplicate maintained rules or invent UI intent for a headless project.

Success means every accepted case below has a named owner and executable behavioral evidence where the existing Forge runtime supports it. Template parity and updater preservation have focused regression checks. Generated outputs are produced only after source owners report ready, then regenerated and checked through Forge. No updater is added. No consumer project content is changed.

## Work plan

- [x] Add a neutral optional `.forge/templates/05_design.md` and parity check; allow authored rules or a pointer-only entry. Owner: template/core implementation.
- [x] Update `/init` synthesis to discover and classify existing sources, preserve them, and create only the neutral optional entry point where needed. Owner: `.forge/skills/ops/core/**`.
- [x] Preserve adopter-authored `.resonance/05_design.md` rules and pointers across framework updates using the existing updater ownership boundary. Owner: updater regression test.
- [x] Update Designer-owned lifecycle, authority, variants, approval, accessibility conflict, and evidence guidance; maintain the existing knowledge-skill archetype. Owner: Designer.
- [x] Add scoped hooks to plan/build, frontend/mobile, reviewer, and QA. Backend also checks visible effects while skipping internal-only changes. Owner: each skill source owner.
- [x] Reconcile token and QA guidance with project-owned sources and evidence. Owner: frontend and QA.
- [x] Add or extend behavioral evals for the accepted cases. Owner: owning skill sources; run only after all owners declare ready.
- [x] Generate all touched skills/routing via existing Forge commands, run focused tests, validator, and executable evals; record exact outputs below. Owner: integration.

## Adversarial coverage map

| # | Adversarial case | Required evidence/outcome | Owning source / check |
|---:|---|---|---|
| 1 | Equivalent Customers and Suppliers screens choose different detail surfaces | Detect mismatch to the approved task-family default; align or require an approved variant | Designer `11_approved_task_family_default.json`; plan `07_design_contract_scope.json`; QA `08_design_validation_evidence.json` |
| 2 | Marketing and workspace screens have different approved scopes | Apply named scoped variants and reject cross-scope exception laundering | Designer `12_scoped_register_and_app_identity.json` |
| 3 | Local icon-spacing fix reuses an approved component | Read relevant source and permit routine fix without approval, baseline, or full audit | Designer `13_routine_reuse_without_gate.json`; frontend `09_project_design_contract.json` |
| 4 | Shared token changes primary-action treatment without contract edit | Judge diff against approved intent; changed implementation cannot self-certify | Designer `14_mutable_source_authority.json`; reviewer `07_design_contract_review.json`; build `09_design_contract_reuse.json` |
| 5 | Maintained `DESIGN.md` is draft and old Figma disagrees | Retain both as evidence and leave approval unresolved | Designer `15_unapproved_conflicting_sources.json`; core `/init` `07_init_design_source_preservation.json` |
| 6 | Approved rule removes visible keyboard focus | Report hard-constraint conflict and refuse conformance claim | Designer `16_accessibility_conflict.json` |
| 7 | Approved contract but rendered comparison is unavailable | Name missing proof and leave visual conformance unverified | Designer `17_unverified_visual_evidence.json`; QA `08_design_validation_evidence.json` |
| 8 | One-screen bug with no contract | Repair from supplied intent/observed convention without product-wide canonization | Designer `18_brownfield_small_repair.json` |
| 9 | Brownfield app proposes a shared pattern | State current variation and proposed default; do not rewrite old screens or imply approval | Designer `19_shared_pattern_proposal.json` |
| 10 | Desktop and native mobile share one product | Read shared intent and apply only approved platform variants with native evidence | Mobile `07_design_contract_native_variants.json`; Designer `20_native_and_visible_backend_effects.json`; build `09_design_contract_reuse.json` |
| 11 | Backend renames displayed status; separate internal query optimization | Route visible vocabulary through design contract and skip no-UI change | Designer `20_native_and_visible_backend_effects.json`; plan `07_design_contract_scope.json`; reviewer `07_design_contract_review.json`; backend `07_visible_product_effects.json` |
| 12 | Adopter upgrades with authored contract or pointer | Existing updater check proves both forms survive real planned/apply upgrade; source scaffold is excluded, with no new updater | `.forge/tests/test_update.py::test_consumer_design_entry_survives_source_upgrade` |
| 13 | Headless CLI runs `/init` or adds a command | Create no screen contract, palette, or browser check absent actual user-facing interaction | Core `/init` `08_init_headless_no_design.json` |
| 14 | Two apps share component package but distinct brands | Resolve app intent independently; shared implementation does not transfer visual approval | Designer `12_scoped_register_and_app_identity.json`, `21_multiple_apps_distinct_design.json`; frontend `09_project_design_contract.json` |
| 15 | One approved contract has overlapping rules with conflicting narrow-layout behavior | Identify both applicable rules and affected scope; leave unresolved for the owner without inventing priority | Designer `25_overlapping_approved_rules.json`; isolated from the internally consistent drawer/route example in case 1 |

## Implementation evidence

| Check | Command / evidence | Result |
|---|---|---|
| Updater regression | `python3 .forge/tests/test_update.py UpdateTests.test_consumer_design_entry_survives_source_upgrade` | Pass in the full suite: authored rules and pointer entry survive source-profile initial install and subsequent update; source scaffold file is excluded from update plan; path is absent from writes, removals, and conflicts. |
| Forge generation | `python3 .forge/forge.py build <skill> --dry-run` for all nine touched skills | All nine outputs fresh: Designer, core, plan, build, frontend, mobile, backend, reviewer, and QA. |
| Skill/library validation | `python3 .forge/validate_skill.py <generated SKILL.md>` for changed focused skills; `python3 .forge/validate_library.py` | Focused Build, Designer, frontend, QA checks each pass with 0 errors and 0 warnings; library has 73 skills, 0 errors and 0 warnings. `docs/skill-manifest.json` and job compositions regenerated before validation. |
| Eval integrity and structure | `python3 .forge/eval_integrity.py --update`; `python3 .forge/eval_integrity.py`; `python3 .forge/run_evals.py --all --check` | 638 fixture/oracle files, 0 integrity problems; 485 eval cases structurally checked, 0 problems (Astra's final independent run). The changed-only check covered 417 cases, also with 0 problems. New coverage is 24 evals: 15 Designer, 7 cross-skill hooks, and 2 core. |
| Full test suite | `python3 .forge/tests/run.py` | 353 tests ran: 352 passed, 1 skipped. This full suite ran before the final prose-only Build/reference refinements; focused skill and library validators passed on the final generated files. Includes updater preservation and template parity checks. |
| Link and whitespace checks | Local Markdown link resolver over 192 source/generated Markdown files; `git diff --check` | 192 files checked with no broken local links; diff check clean. |
| Behavioral smoke | Fresh Luna responses in `/tmp/resonance-design-behavior-answers.md`, isolated follow-ups in `/tmp/resonance-design-qa08-isolated.md` and `/tmp/resonance-design-core08-final.md`; independently reviewed by Astra | 22 of 24 graded cases passed; 2 were partial. Smoke evidence is not a measured lift or a durable eval score. The 14 acceptance cases are covered; Mobile07 supplies native-variant behavior coverage. Raw responses are ephemeral and remain under `/tmp`. |

## Decisions and limits

- Keep design ownership in the existing `resonance-design-designer` knowledge skill; no new design-contract skill, parser, registry, or updater.
- Keep the framework `.resonance/` scaffold free of product-specific design decisions.
- Existing files remain canonical when their authority is established. `/init` may add a pointer, but must not overwrite, approve, or migrate a source.
- Missing evidence is unverified. No global style or universal breakpoints are introduced.
- Executable behavioral smoke was reviewed against rubrics. The smoke is finite evidence, not a measured score lift; two responses were partial and this report does not claim improved eval performance.
