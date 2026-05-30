# Contributing

Resonance is an open skill library. If you work in a domain and know what good looks like, you can improve it.

## How to contribute

**Fix something that's wrong.** If a skill gives bad advice, open a PR with the corrected template and the eval that proves it.

**Add a missing protocol.** If a reference document is thin or missing, write it. Put it in the right `references/` folder.

**Build a new skill.** Use the `resonance-ops-skill-author` skill to author it correctly. Every new skill needs:
- A template in `.forge/skills/<domain>/<name>/skill.tmpl.md`
- At least 3 evals in `.forge/skills/<domain>/<name>/evals/`
- A clean run of `py .forge/validate_skill.py` with 0 errors

## The Forge workflow

Skills are not edited directly in `.agents/`. They are compiled from templates.

```bash
# Edit the template
# .forge/skills/<domain>/<name>/skill.tmpl.md

# Compile
py .forge/forge.py build <name>

# Validate
py .forge/validate_skill.py .agents/skills/<domain>/<name>/SKILL.md
```

Do not edit `.agents/skills/` directly. Generated files carry a "do not edit" banner. Changes made there will be overwritten on the next build.

## Standards

- **Evals before shipping.** A skill without 3 passing evals is not done.
- **No broken references.** Every linked file must exist. Run the validator.
- **One skill, one job.** If a skill tries to do two things, split it.
- **Concrete language.** Name the file, the function, the command. No generic advice.

## Domain structure

| Domain | What lives here |
| :--- | :--- |
| `strategy/` | Planning, architecture, business modeling |
| `engineering/` | Building, debugging, performance, DevOps |
| `design/` | Visual systems, UI components, assets |
| `marketing/` | SEO, conversion, copywriting |
| `sales/` | Pipeline, outreach, call intelligence |
| `ops/` | Quality, security, delivery, governance |
| `research/` | Market and competitive intelligence |

Thank you for contributing.
