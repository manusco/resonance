# Skill Spec (the authoritative contract)

The single source of truth for what a Resonance skill must be. The validator
(`.forge/validate_skill.py`) enforces this; if you change the rules, change both.

## Contents
- Frontmatter
- The three archetypes
- Body rules
- References
- Evals
- What the Forge injects

## Frontmatter

Required:
- `name` — `^[a-z0-9-]{1,64}$`. Lowercase, digits, hyphens. Avoid the words "claude"/"anthropic" in the name; they hurt cross-tool namespacing.
- `description` — third person, <= 1024 chars. States what the skill does AND when to use it. This is the only text loaded at startup; it is what makes the skill trigger. Lead with the use case.
- `archetype` — `knowledge | procedure | orchestration`.

Optional, host-dependent (the Forge emits these where the host supports them; do not hand-author tool-specific fields in the template):
- manual-only flag for side-effecting procedures (so the model does not auto-fire a deploy).
- pre-approved tools, model, effort, paths.

## The three archetypes

| Archetype | Is | Invoked | Must contain |
| :-- | :-- | :-- | :-- |
| **knowledge** | a domain expert applied inline | auto, when relevant | principles, frameworks, boundaries, reference library |
| **procedure** | a gated multi-step job | as `/name` | Input, Output, Definition of Done, Recovery, a step checklist |
| **orchestration** | a procedure that drives other skills | as `/name` | the same contract + an ordered pipeline of named skills/subagents |

Procedure and orchestration skills MUST carry the operating contract sections
(Input / Output / Definition of Done / Recovery). The validator fails without them.

## Body rules

- Overview, not encyclopedia. Keep SKILL.md under 500 lines; move detail to references.
- Only add what the model does not already know. Challenge every paragraph's token cost.
- Imperative, concrete. No KPIs, no "you are a craftsman", no motivational filler.
- Forward slashes in all paths. No em dashes. No banned vocabulary (see resolvers/voice.md).
- No time-sensitive claims ("as of August 2025…"). Put deprecated info behind an "Old patterns" note.

## References

- One level deep from SKILL.md. A reference must not fan out to more reference files; the model partial-reads nested links and misses content.
- Files over 100 lines start with a `## Contents` table.
- Name files for content: `migration_safety.md`, not `doc2.md`.
- No context cost until opened, so bundle generously, but link precisely.

## Evals

- >= 3 golden cases in `evals/*.json` before the skill is "done".
- Each case: `query`, optional `files`, `expected_behavior` (a list of observable, gradeable statements).
- Cover happy path, an edge case, and a failure the skill must prevent.

## What the Forge injects (never hand-copy these)

Templates use placeholders; the compiler fills them from `.forge/resolvers/`:
- `{{RESOLVER:voice}}` — anti-slop voice
- `{{RESOLVER:decision_brief}}` — recommendation-first decisions
- `{{RESOLVER:completion}}` — status protocol
- `{{RESOLVER:locks}}` — the four operating locks
- `{{RESOLVER:learnings}}` — the Ratchet
- `{{OVERLAY}}` — the per-model behavioral patch
- `{{TOOL:logical}}` — maps a logical tool name to the host's real tool name

Edit the template, run `forge.py build`, never the generated `SKILL.md`.