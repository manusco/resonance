# Skill templates moved to the Forge

The old single maximalist template (8 sections, KPIs, ceremony) is retired. Skills
are now compiled from archetype templates by the Resonance Forge.

Use one of the three archetype templates in [`.forge/templates/`](../../.forge/templates/):

- `knowledge.skill.md` — a domain expert applied inline.
- `procedure.skill.md` — a gated workflow with a Definition of Done.
- `orchestration.skill.md` — a procedure that drives other skills.

To author a skill, drive `resonance-skill-author`, or by hand:

1. Copy the matching archetype to `.forge/skills/<name>/skill.tmpl.md`.
2. Add `>= 3` golden cases in `.forge/skills/<name>/evals/`.
3. `py .forge/forge.py build <name>` then `py .forge/validate_skill.py .agents/skills/<name>/SKILL.md`.

See [`.forge/README.md`](../../.forge/README.md) for the full pipeline.
