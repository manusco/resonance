# Automatic design proposal population

**Status:** DONE. Integration report: [automatic design proposal population integration](2026-10-22-auto-design-population-integration.md).

## Goal and scope

During normal UI coding, Designer automatically writes a bounded, evidence-based `PROPOSED` application design entry when the affected app has no filled entry point or the task adds its first or a new shared pattern. The proposal records usable app-specific choices and open questions, not a blank template. Existing pointers and approved content remain authoritative. Read-only audits never write project files.

This work owns Designer instructions, its canonical contract reference, fixture scenarios, and Designer evals. Workflow routing hooks and their evals belong to the workflow owner. Generation and repository-wide checks belong to integration.

## Plan

- [x] Define automatic triggers, proposal content, source preservation, incremental resume, and read-only boundary in the canonical contract reference.
- [x] Add the bounded population step to the Designer source template.
- [x] Add evidence fixtures and separate evals for a new app, an existing app, pointer preservation, proposal resume, tiny repair, and read-only audit.
- [x] Add approved-source shared-pattern coverage proving proposed additions preserve canonical status and approved rules.
- [x] Reconcile wording with Core, Plan, Build, Frontend, Mobile, and project-instruction routing hooks.
- [x] Run generation, fixture integrity, eval structure, repository tests, and behavioral verification after all owners declared ready.

## Decisions

- A coding task authorizes this reversible draft write. It does not approve the proposed defaults.
- Greenfield task reasoning can support concrete proposed choices without implementation evidence, if observed facts, proposed choices, and assumptions are labeled separately.
- A shared-pattern proposal for an approved canonical source is added to that same source as a proposed subsection; the approved status and approved sections stay intact.
- A consuming project may not include the framework template. Designer writes the concise app-aware proposal shape directly, including status, scope, task defaults, evidence/references, variants, assumptions, and open choices.
- A declared source or pointer is continued in place. No duplicate `.resonance/05_design.md` is created for a canonical source elsewhere.
- Proposed entries are updated only in relevant unfinished sections. Supported existing approved choices are not regenerated.
- A small repair can proceed from local evidence without a whole-app audit or new approval gate. A proposal, if useful for the missing baseline, stays scoped to that screen.
- A small repair alone does not make broader app-baseline creation mandatory; meaningful first UI work and new shared patterns still trigger automatic population.
- The framework repository's public `.resonance/05_design.md` stays template-clean.

## Evidence map

| Case | Evidence | Expected boundary |
| --- | --- | --- |
| New app | `new-app/brief.md` | Filled proposal from a short brief; no invented identity, source, or approval owner |
| Existing app | `existing-app/brief.md`, `existing-app/current-source.md` | Proposed pattern grounded in inspected sources; unrelated task patterns stay intact |
| Pointer | `pointer/.resonance/05_design.md`, `pointer/product/design-system.md` | Continue the declared target without a duplicate |
| Resume proposal | `proposed-resume/.resonance/05_design.md` | Fill only unfinished, supported content; preserve proposed status and completed content |
| Tiny repair | `tiny-repair.md` | Keep repair narrow; any proposal stays screen-scoped and observational |
| Read-only audit | `read-only-audit.md` | Can report proposed text but must not write |

Eval cases 26–32 map one-to-one to these behaviors. They are acceptance rubrics, not execution evidence. The workflow agent separately owns automatic routing cases at Core and Frontend boundaries.

## Verification record

Integration is complete. See the linked integration report for exact commands, counts, six actual-file behavior cases, and limits. Eval cases are acceptance rubrics; they are separate from the executed behavioral evidence.
