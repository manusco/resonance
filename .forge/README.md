# The Resonance Forge

The skill compiler. Author a skill once as a template and compile one portable
`SKILL.md`. Host adapters own only discovery paths, command shims, and context bridges.

```
template.skill.md   x   portable profile   ->   .agents/skills/<name>/SKILL.md
```

## Why a compiler, not hand-written skills

- **Cross-tool.** Antigravity (Google), Codex (OpenAI), Cursor, OpenCode, and Claude Code all read `AGENTS.md` + `.agents/skills`. Tool differences (tool names, paths) live in one host config, not in every skill.
- **Cross-model.** Canonical skills use one portable execution profile. Model selection and independent review happen at runtime, so a model choice cannot rewrite shared skill files.
- **DRY.** Shared sections (voice, decision format, completion protocol, the operating locks, the Ratchet) live once in `resolvers/` and are injected into every skill. Fix the voice in one place, recompile, every skill updates.
- **Verifiable.** Every skill is checked by `validate_skill.py` (free, deterministic) and backed by `>= 3` golden evals before it ships.

## Layout

```
.forge/
├── forge.py                 # the compiler: build / list / --dry-run
├── validate_skill.py        # static validator (Tier 1, free, <1s)
├── resolvers/               # shared sections injected into every skill
│   ├── voice.md  decision_brief.md  completion.md  locks.md  learnings.md
├── hosts/                   # one adapter config per tool
│   ├── claude-code.json  codex.json  cursor.json  antigravity.json  opencode.json
├── overlays/                # the single portable execution profile
│   └── portable.md
├── templates/               # the three archetype starting points
│   ├── knowledge.skill.md  procedure.skill.md  orchestration.skill.md
└── skills/                  # the source of truth for each skill
    └── <name>/
        ├── skill.tmpl.md    # YOU EDIT THIS
        ├── references/       # copied next to the generated SKILL.md
        ├── scripts/
        └── evals/            # >= 3 golden cases
```

The generated `.agents/skills/<name>/SKILL.md` is **build output**. Do not edit it;
edit the template and recompile.

## Placeholders

| Placeholder | Expands to |
| :-- | :-- |
| `{{RESOLVER:name}}` | the contents of `resolvers/<name>.md` |
| `{{OVERLAY}}` | the portable execution profile |
| `{{TOOL:logical}}` | a portable logical tool name; adapters do not rewrite canonical skills |

## Commands

```bash
py .forge/forge.py list                                  # skills, hosts, portable profile
py .forge/forge.py build <name>                          # default host + model
py .forge/forge.py build --all                           # every skill
py .forge/forge.py build <name> --dry-run                # CI freshness: exit 1 on drift
py .forge/forge.py commands --host all                   # host adapters only
py .forge/forge.py doctor --json                         # ownership and support report

py .forge/validate_skill.py <path-to-SKILL.md>           # one skill (Tier 1, structural)
py .forge/validate_skill.py --all .agents/skills         # all skills
py .forge/validate_skill.py --all .agents/skills --strict  # warnings fail too

py .forge/validate_library.py                            # Tier 1.5: cross-skill (orphans, dup/diverged refs, eval-name drift, two-level links, leaks, dashes)
py .forge/run_evals.py --all --check                     # eval structure gate (free)
py .forge/run_evals.py marketing/seo --model-cmd "claude -p"  # live with/without run, LLM-judged
```

(`py` on Windows; `python3` on macOS/Linux. Pure stdlib, no install.)

## The three archetypes

- **knowledge**: a domain expert applied inline (copywriter, architect). Auto-loaded when relevant.
- **procedure**: a gated multi-step job with a Definition of Done (build, ship). Invoked as `/name`. Carries Input / Output / Definition of Done / Recovery.
- **orchestration**: a procedure that drives other skills or subagents (an audit swarm, a review pipeline).

Workflows are not a separate thing. A workflow is the procedure (or orchestration)
archetype. One format, three kinds, one compiler.

## Authoring loop

1. Prove the gap: run the task with no skill, record the failure.
2. Write `>= 3` evals in `skills/<name>/evals/`.
3. Copy the matching archetype template to `skills/<name>/skill.tmpl.md`, write the minimum.
4. `forge build <name>` then `validate_skill.py` until clean.
5. Eval against the golden cases; beat the baseline.
6. Commit only when validate + eval pass.

The `resonance-ops-skill-author` skill walks an agent through exactly this.
