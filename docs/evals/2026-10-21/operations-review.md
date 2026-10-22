# Operations skill eval review, 2026-10-21

Baseline at `5a5fcc4e10b1dbc43d42e1924421b62af07d65d6`: 26 Operations skills and 131 cases. 19 skills were below six and needed 35 distinct cases to reach the floor.

Current source: 26 skills and 166 cases, including 35 additions. 26/26 now have at least six cases; 0 invalid or misbound fixtures.

## Per-skill counts

| Skill | HEAD cases | Added | Current |
|---|---:|---:|---:|
| `ops/audit` | 4 | 2 | 6 |
| `ops/core` | 4 | 2 | 6 |
| `ops/explain` | 4 | 2 | 6 |
| `ops/founder-os` | 4 | 2 | 6 |
| `ops/goal` | 8 | 0 | 8 |
| `ops/handover` | 4 | 2 | 6 |
| `ops/improve` | 4 | 2 | 6 |
| `ops/incident` | 4 | 2 | 6 |
| `ops/legal` | 4 | 2 | 6 |
| `ops/librarian` | 4 | 2 | 6 |
| `ops/observability` | 4 | 2 | 6 |
| `ops/page-audit` | 5 | 1 | 6 |
| `ops/product` | 4 | 2 | 6 |
| `ops/productivity` | 5 | 1 | 6 |
| `ops/qa` | 7 | 0 | 7 |
| `ops/refactor` | 7 | 0 | 7 |
| `ops/retro` | 4 | 2 | 6 |
| `ops/reviewer` | 5 | 1 | 6 |
| `ops/second-opinion` | 8 | 0 | 8 |
| `ops/security` | 7 | 0 | 7 |
| `ops/ship` | 6 | 0 | 6 |
| `ops/skill-author/resonance-skill-author` | 4 | 2 | 6 |
| `ops/system-health` | 4 | 2 | 6 |
| `ops/update-resonance` | 9 | 0 | 9 |
| `ops/update-roadmap` | 4 | 2 | 6 |
| `ops/voice` | 4 | 2 | 6 |

## Content review

New cases target separate behavior boundaries such as authorization, evidence quality, stale state, incomplete measurements, source conflicts, failure recovery, or communication authority. The complete case inventory, rubric lengths, deterministic-check counts, and owner-ID checks are in [operations-review.json](operations-review.json).

I reviewed every original one-item rubric in the Operations scope. The cases for `retro/01-03`, `ship/02-03`, `system-health/02-03`, `update-resonance/03`, and `update-roadmap/01-03` now separate the observable behaviors their prompts exercise. Additional stale expectations were corrected: audit dispatch follows scope; system-health detects the actual toolchain and still computes a score when build fails; update-roadmap checks current implementation before treating commit messages as proof.

The shared policy now requires six distinct cases per framework skill and preserves the legacy three-case floor for unowned project skills in an installed consumer. The validator applies six to manifest-owned skills and defaults to six when no consumer ownership manifest exists. Malformed manifests fail closed at six.

A second review removed lexical `contains_all` checks that merely looked for rubric vocabulary. The remaining new deterministic checks enforce exact output contracts: an APPROVE/REJECT disposition and the two named system-health flags. The librarian case now supplies a typed decision record and stale runbook, so its source-of-truth behavior is gradeable from evidence in the fixture.

No live model evaluation or paid API call was run. These checks establish fixture structure and coverage intent, not measured skill lift.
