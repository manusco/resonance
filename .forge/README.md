# The Resonance Forge

The skill compiler. Author a skill once as a template; compile it per tool and per
model into a ready `SKILL.md`. You author above the format and emit the open
`SKILL.md` / `AGENTS.md` shape that every major tool reads, without locking to any
one vendor.

```
template.skill.md   x   host (tool)   x   overlay (model)   ->   SKILL.md
```

## Why a compiler, not hand-written skills

- **Cross-tool.** Antigravity (Google), Codex (OpenAI), Cursor, OpenCode, and Claude Code all read `AGENTS.md` + `.agents/skills`. Tool differences (tool names, paths) live in one host config, not in every skill.
- **Cross-model.** Strong models get terse prompts; weaker and open-weight models get more explicit guardrails. One overlay file per model family, injected at compile time.
- **DRY.** Shared sections (voice, decision format, completion protocol, the operating locks, the Ratchet) live once in `resolvers/` and are injected into every skill. Fix the voice in one place, recompile, every skill updates.
- **Verifiable.** Every skill is checked by `validate_skill.py` (free, deterministic) and backed by `>= 3` golden evals before it ships.

## Layout

```
.forge/
├── forge.py                 # the compiler: build / list / --dry-run
├── validate_skill.py        # static validator (Tier 1, free, <1s)
├── resolvers/               # shared sections injected into every skill
│   ├── voice.md  decision_brief.md  completion.md  locks.md  learnings.md
├── hosts/                   # one config per TOOL (tool-name map + output path)
│   ├── claude-code.json  codex.json  cursor.json  antigravity.json  opencode.json
├── overlays/                # one behavioral patch per MODEL family
│   ├── claude.md  gpt.md  gemini.md  open-weights.md
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
| `{{OVERLAY}}` | the chosen model overlay |
| `{{TOOL:logical}}` | this host's real name for a logical tool (e.g. `{{TOOL:edit}}` -> `Edit` on Claude, `apply_patch` on Codex) |

## Commands

```bash
py .forge/forge.py list                                  # skills, hosts, overlays
py .forge/forge.py build <name>                          # default host + model
py .forge/forge.py build <name> --host all               # every tool
py .forge/forge.py build <name> --model open-weights     # target a model family
py .forge/forge.py build --all                           # every skill
py .forge/forge.py build <name> --dry-run                # CI freshness: exit 1 on drift

py .forge/validate_skill.py <path-to-SKILL.md>           # one skill
py .forge/validate_skill.py --all .agents/skills         # all skills
py .forge/validate_skill.py --all .agents/skills --strict  # warnings fail too
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

The `resonance-skill-author` skill walks an agent through exactly this.
