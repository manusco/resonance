# Resonance v3 — Framework Evaluation & Recommendation

> Author: assessment for Manuel, 2026-05-30.
> Scope: evaluate the whole framework against the May/June 2026 state of the art, answer the skills-vs-workflows question, and specify the rebuild of the skill-author (and a workflow builder).
> Decisions taken from you: **cross-tool first** (open Agent Skills standard + `AGENTS.md`, no single-vendor lock-in), **bold / first-principles**, deliverable is this doc.

---

## 0. The one-paragraph verdict

Resonance is a strong *idea* sitting on a *pre-standard* foundation. You built it in November 2024 — eleven months before Anthropic shipped the Agent Skills standard (Oct 2025) that the whole industry then converged on. The result: your best inventions (the `.resonance/` brain, the Job-to-be-Done discipline in workflows, the anti-slop voice work, the "push determinism to Layer 3" philosophy) are genuinely ahead of the curve, but they're encoded in a **bespoke `.agents/` format with invalid frontmatter** that no current runtime reads natively, and you're **missing the three things that now define a serious framework: evals, deterministic validators, and packaging.** The redo is not a rewrite of your ideas. It's re-platforming your ideas onto the open standard, deleting ceremony, and adding the verification layer you already preach but never built.

---

## 1. What you must NOT delete (the cathedral)

You said "improve, don't replace." These are the parts that are still ahead of the state of the art. Keep them, port them forward:

| Asset | Why it survives |
| :--- | :--- |
| **`.resonance/` externalized cognition** (soul/state/memory/systems/learnings) | This is "agent memory" before it was a product category. Anthropic, OpenAI, and Google all shipped memory features in 2025-26; you had the pattern in 2024. Keep verbatim. |
| **JTBD / Input / Output / Definition-of-Done discipline in workflows** | The bare Agent Skills standard has *no* notion of "definition of done." Yours does. This is a real edge — fold it into the new skill format, don't lose it. |
| **The reference libraries (203 protocols)** | This is the actual IP. The MEDDIC/SPIN, GEO, friction-collider, anti-slop, stylometric extraction material is the moat. The *packaging* is wrong; the *content* is gold. |
| **Anti-slop / voice protocols** | Fighting AI slop is now a mainstream concern. You were early. Keep and make it a shared, enforced layer. |
| **3-Layer architecture philosophy** ("push complexity into Layer 3") | This is exactly right and matches Anthropic's "scripts solve, don't punt" guidance. Your problem is you *under-apply your own rule* — see §4. |

Everything below assumes these are preserved.

---

## 2. The core problem: you're on a pre-standard format

This is the root cause of most weaknesses. Concrete evidence from your own files:

**Your frontmatter is invalid against every current runtime.**
```yaml
# resonance-skill-author/SKILL.md today:
tools: [read_file, write_file, edit_file, run_command]   # ← not real tool names anywhere
model: inherit                                            # ← not a standard Skill field
skills: [resonance-core, resonance-copywriter]           # ← skill composition isn't declared here
```
The open Agent Skills standard (agentskills.io, the cross-tool spec you should target) defines exactly **two** required fields: `name` and `description`. Everything else is either a runtime-specific extension or doesn't exist. Your `tools:` list uses names (`read_file`, `run_command`) that map to nothing — the real ecosystem uses `Read`, `Write`, `Edit`, `Bash`, `Grep`. So today none of this frontmatter does anything; it's decorative.

**Your descriptions don't trigger well.** The single most important field in the standard is `description` — it's the only thing loaded at startup, and the model selects skills from it. Yours are thin and sometimes first-person-adjacent:
- `resonance-core`: *"The Resonance Kernel and Orchestrator. Manages Persistent Memory, Task Planning, and State."* → no "use when", no trigger phrases. The model can't tell when to fire it.
- The spec is explicit: third person, state **what it does AND when to use it**, lead with the use case, ≤1024 chars.

**Your `.agents/skills/` path is invisible to the standard.** The open standard and every tool that implements it (Claude Code, and increasingly Cursor/Windsurf via the agentskills.io spec) discover skills from a known skills directory. `.agents/skills/` is your own convention, so the progressive-disclosure engine — the entire reason skills exist — never runs. Your 203 protocols only load if an agent happens to read `AGENTS.md` and then manually navigates. You built a progressive-disclosure library and then disabled progressive disclosure.

> **Bold recommendation:** Re-home skills to the standard skills directory layout and rewrite every frontmatter to `name` + a *real* trigger-rich `description`. Keep `AGENTS.md` at root as the human-readable manifest and the cross-tool entry point, but make it a generated index, not the source of truth.

---

## 3. Skills vs. Workflows — your central question, answered

Your model today:
- **Skill** = a role/persona ("the who"): `resonance-copywriter`, `resonance-architect`.
- **Workflow** = a sequence with input/output/JTBD/DoD ("the how/when"): `/build`, `/plan`, `/ship`, stored separately in `.agents/workflows/`.

**Is this a good setup? Half right — and the standard has already resolved it for you.**

Here's the first-principles read. In the Agent Skills standard there is **no separate "workflow" primitive**. A skill is just a `SKILL.md`, and it comes in two flavors distinguished *only by how it's invoked*:

1. **Reference / knowledge skills** — applied inline, loaded automatically when relevant. *This is exactly what your "personas" are.* (`resonance-copywriter` is a body of knowledge + judgment the model applies.)
2. **Task / command skills** — a step-by-step procedure, invoked deliberately as `/name`, often flagged so the model can't auto-fire it (for things with side effects like deploy/ship). *This is exactly what your "workflows" are.* (`/build`, `/ship`.)

So your skill/workflow split is **conceptually correct but mechanically redundant.** You invented a two-primitive system; the world settled on **one primitive with two modes.** Both `resonance-backend` and `/build` are just skills. The difference is metadata, not folder location:

| Your term | Becomes | Distinguishing frontmatter (Claude Code) / convention (cross-tool) |
| :--- | :--- | :--- |
| Persona ("role" skill) | Knowledge skill | auto-loaded; "use this expertise when…" |
| Workflow ("command" skill) | Procedure skill | invoked as `/name`; marked manual-only for side effects |

**What you should keep from your model:** the *discipline* — JTBD, explicit Input, explicit Output, Definition-of-Done, Recovery. The bare standard doesn't mandate these and is weaker for it. Your workflows are better-engineered than a default skill. So:

> **Keep the distinction as an authoring convention, not a storage format.** One skills tree. Two archetypes — `knowledge` and `procedure` — defined by a shared spec. Procedure skills carry your Input/Output/DoD/Recovery contract. A procedure skill *composes* knowledge skills (invokes them, or delegates to them as subagents when the runtime supports it). This gives you the best of both: the world's portability + your operational rigor.

The net: **delete the `.agents/workflows/` vs `.agents/skills/` divide.** Replace with `skills/` (everything) where each skill declares its archetype. `AGENTS.md` regenerates the two human-facing lists (Roster + Workflow Map) from frontmatter so you keep the nice ergonomics you have now.

---

## 4. State-of-the-art gaps (what everyone else now ships that you don't)

I read the current Anthropic, OpenAI, and Google material. The frameworks have converged on a clear shape. Here's where Resonance is behind, ranked by impact.

### 4.1 Evals — the #1 miss
Anthropic's top authoring rule is now literally **"Build evaluations BEFORE writing documentation."** OpenAI's AgentKit centers on datasets + trace grading + automated prompt optimization. Google's ADK ships eval as a first-class step. Resonance has **zero evals** — no golden datasets, no runner, no baseline measurement. Your `outstanding_skills_protocol.md` *mentions* "golden dataset" and "model-graded eval" as theory, but nothing exists. This is the biggest single gap and the highest-leverage fix.

> Adopt **eval-driven skill development**: every skill ships with ≥3 golden cases (`query`, optional `files`, `expected_behavior` rubric). A runner measures the model with vs. without the skill. You don't author a skill until you've shown the gap it closes. This is also the rigorous version of your own "Self-Annealing Loop."

### 4.2 Deterministic validators — you preach Layer 3 but never built it
Your own Prime Directive says "push complexity into Layer 3 (deterministic scripts)." Yet skill quality is enforced by *prose* in `AGENTS.md` ("don't use the word delve"), which is probabilistic Layer 1. Meanwhile the one validator you have (`banned_phrase_scan.py`) proves you know how. The state of the art ("scripts solve, don't punt"; "create verifiable intermediate outputs") wants the fragile, checkable stuff to be code.

> Build a **`validate_skill.py`** (cross-tool, pure Python — no runtime lock-in) that hard-checks every skill: frontmatter valid, `name` matches `^[a-z0-9-]{1,64}$`, `description` is third-person + contains a "use when" trigger + ≤1024 chars, body ≤500 lines, references are one level deep, all paths use forward slashes, long reference files (>100 lines) have a table of contents, no banned ceremony words. This is your skill-author's "test suite" and it runs anywhere.

### 4.3 Deterministic enforcement of the Behavioral Locks
Your "4 Behavioral Locks" and "4 Zeros" are enforced by hope. Where a runtime offers event hooks (Claude Code does today; the pattern is spreading), the locks that *can* be deterministic should be: block a "ship" without a passing test; run `banned_phrase_scan.py` automatically on generated copy; refuse a commit that touches `.resonance/00_soul.md`. Keep the prose for cross-tool fallback, but add hooks as an optional Layer-3 enforcement when present. (This is an *enhancement*, not the foundation, per your cross-tool priority.)

### 4.4 Packaging & distribution
Anthropic now has **plugins** (skills + references + scripts + optional MCP/hooks/agents bundled as one installable unit) and **marketplaces** (the official directory had 101 plugins as of March 2026). OpenAI has the Connector Registry; Google has a Skill Registry in its Agent Registry. Resonance installs by `cp -r` and a migration note about renaming `.agent/`→`.agents/`. You have a 26-skill, 203-protocol library that is *exactly* what a marketplace plugin is — but it's shaped as a folder dump.

> Package Resonance as a distributable bundle with a manifest. Even staying cross-tool, a single `resonance.bundle` manifest + a tiny installer beats the current copy ritual, and positions you to publish to the Anthropic plugin marketplace later with near-zero rework.

### 4.5 Outdated prompt-engineering references
The skill-author's references are 2023-era: `chain_of_thought_protocol.md` teaches *"Let's think step by step"* and the *"magic phrase"*; `few_shot_library.md` and `persona_injection.md` are generic. Modern frontier models (Opus 4.x, GPT-5-class, Gemini) have native extended thinking — telling them "think step by step" in a skill body is mostly wasted tokens and occasionally *suppresses* better default reasoning. The current guidance is the opposite of your template: **"Claude is already very smart — only add what it doesn't know; challenge every paragraph's token cost."** Your `SKILL_TEMPLATE.md` is maximalist (8 sections incl. KPIs, "Iron Man Suit", "ELI16", `recovery_mode`) — ceremony that fights the conciseness rule.

> Rewrite these references to 2026 practice (degrees of freedom, description-writing, progressive disclosure depth, "solve don't punt", plan-validate-execute, fully-qualified MCP tool names). Delete or radically shrink the CoT/few-shot/persona docs.

### 4.6 Summary table

| Capability | Anthropic (Skills/Plugins) | OpenAI (AgentKit) | Google (ADK) | Resonance today | Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Skill primitive | `SKILL.md`, 2-field frontmatter, progressive disclosure | Agent nodes | SkillToolset / Skill Registry | Bespoke `.agents/`, invalid frontmatter | **Re-platform onto standard** |
| Workflows | = task skills | Visual Agent Builder | Multi-agent graphs | Separate `.agents/workflows/` | **Collapse into skills** |
| Evals | Eval-first, golden datasets | Datasets, trace grading, auto-optim | First-class eval | **None** | **Build eval harness** |
| Validators | "scripts solve, don't punt" | Guardrails | Callbacks | 1 script (banned phrases) | **Build `validate_skill.py`** |
| Packaging | Plugins + marketplace | Connector Registry | Agent Registry | `cp -r` | **Bundle + manifest** |
| Memory | Memory tool | Sessions | Sessions/State | `.resonance/` (ahead) | **Keep** |

---

## 5. The skill-author redo (the priority)

You said this is the most important skill — the skill that makes skills. Get it right and everything else is regenerated from it. Here's the target spec.

### 5.1 What's wrong with it today
- Generates **invalid frontmatter** (`tools: [read_file…]`, `model`, `skills`).
- Enforces a **bloated template** that violates the conciseness rule it claims to follow.
- References are **dated** (CoT magic phrases, generic few-shot).
- **No eval step.** It can't measure whether a skill it produced is good.
- **No validator.** It can't mechanically check its own output.
- Doesn't teach the **role-skill vs procedure-skill** distinction, `description` craft, one-level-deep references, degrees-of-freedom calibration, "solve don't punt", or MCP naming.
- Personality-heavy ("The Teacher"), instruction-light.

### 5.2 The new skill-author — design

**Name & description (the part that makes it fire correctly):**
```yaml
---
name: skill-author
description: Creates, audits, and hardens Agent Skills and procedure skills (workflows) to the open Agent Skills standard. Use when the user wants to build a new skill, convert a workflow, refactor or shrink an existing SKILL.md, write or fix a skill description/frontmatter, add evals to a skill, or run the skill validator.
---
```
Third person, leads with the job, dense with trigger terms. ≤1024 chars.

**Body — lean, under ~150 lines, pointing to references.** Core sections:

1. **The two archetypes.** Decide first: *knowledge skill* (applied inline, auto-loaded) or *procedure skill* (invoked as a command, carries Input/Output/Definition-of-Done/Recovery — your old "workflow"). Different templates, same spec.
2. **Eval-first protocol (mandatory gate).** Before writing prose: (a) run the target task *without* a skill, record where the model fails; (b) write ≥3 golden cases to `evals/`; (c) write the *minimum* skill that passes; (d) measure with/without. No eval, no skill. This replaces the old "write the template then hope."
3. **Degrees of freedom.** High (prose heuristics) → Medium (parameterized scripts) → Low (exact scripts) matched to task fragility. Keep this — it's the one modern idea your current version already has.
4. **Description craft.** The rules from §2/§4.5, with good/bad examples.
5. **Progressive disclosure rules.** Body ≤500 lines; references one level deep; TOC for refs >100 lines; "solve, don't punt" for scripts; fully-qualified `Server:tool` MCP names; forward slashes always.
6. **Validate.** Run `scripts/validate_skill.py` and fix every failure before declaring done. This is the skill-author's own definition-of-done.
7. **Iterate (Claude A / Claude B loop).** Author with one instance ("A"), test with a fresh instance ("B") on real tasks, bring B's failures back to A. This is the current best-practice iteration loop and is just a sharper version of your Self-Annealing Loop.

**Bundled resources the new skill-author owns:**
```
skill-author/
├── SKILL.md                      # lean body, above
├── references/
│   ├── skill_spec.md             # the authoritative frontmatter + structure spec (replaces SKILL_TEMPLATE ceremony)
│   ├── description_patterns.md   # good/bad descriptions, trigger-term craft
│   ├── degrees_of_freedom.md     # the bridge/field analogy, calibration
│   ├── eval_protocol.md          # golden-dataset format + how to baseline
│   └── script_authoring.md       # "solve don't punt", voodoo-constants, plan-validate-execute
├── templates/
│   ├── knowledge_skill.md        # minimal role skill
│   └── procedure_skill.md        # minimal command skill WITH your Input/Output/DoD/Recovery
└── scripts/
    ├── validate_skill.py         # hard structural checks (cross-tool, stdlib only)
    └── run_evals.py              # model-graded eval runner against evals/*.json
```

Delete from the old version: `chain_of_thought_protocol.md`, `persona_injection.md`, and most of `few_shot_library.md` (fold a 10-line "examples beat instructions" note into `description_patterns.md`). Shrink `SKILL_TEMPLATE.md`'s 8-section ceremony to the two lean templates above.

**Why this is "best of the best":** it is eval-gated (you cannot ship an unmeasured skill), self-validating (it runs its own checker), spec-correct (valid frontmatter, real tool names), token-honest (lean body, progressive disclosure), and it encodes *your* operational rigor (DoD, Recovery) that the bare standard lacks. That combination is ahead of both the vanilla standard and the community skill-writers.

### 5.3 The golden-dataset format (concrete)
```json
{
  "skill": "resonance-copywriter",
  "query": "Write the hero headline + subhead for a B2B payroll tool. No AI clichés.",
  "files": [],
  "expected_behavior": [
    "Produces one headline and one subhead",
    "Contains zero banned phrases (delve, robust, seamless, landscape...)",
    "Headline is benefit-led and reads at <= grade 8",
    "Makes no claim not supported by an actual product feature"
  ]
}
```
`run_evals.py` feeds `query` to a model with the skill loaded, then a grader model scores the output against `expected_behavior`. Three cases minimum, run before and after every edit.

---

## 6. The workflow builder

Given §3 (workflows *are* procedure skills), you have two clean options:

- **Option A (recommended): one forge, two modes.** Don't build a second meta-skill. The `skill-author` produces both archetypes; `templates/procedure_skill.md` *is* the workflow builder. Less surface area, one source of truth, no drift. Add thin command aliases `/new-skill` and `/new-workflow` that both call the same forge with a different `--archetype` flag if you like the ergonomics.
- **Option B: a separate `workflow-author` procedure skill** that depends on `skill-author`'s spec + validator. Only worth it if workflow authoring grows materially different rules (e.g., heavy multi-skill orchestration graphs). I'd hold off until you feel that pain.

The **procedure-skill template** must preserve your contract — this is the part the standard lacks and you should be proud of:
```markdown
---
name: ship
description: Release protocol — health check, changelog, version bump, tag, deploy. Use when the user says ship/release/cut a version. Manual-only (side effects).
---
# /ship — Release Protocol
**Role:** delegates to resonance-devops, resonance-qa.
**Input:** clean working tree, green CI.
**Output:** tagged release, updated changelog, deployed build.
**Definition of Done:** health score >= threshold; changelog updated; tag pushed; deploy verified.

## Prerequisites (fail fast)
- [ ] Working tree clean
- [ ] Tests green

## Algorithm
1. ... → verify: ...

## Recovery
- Deploy fails → roll back via rollback_matrix, halt, report.
```
That `Input / Output / Definition of Done / Recovery` block is your differentiator. Bake it into the template and have `validate_skill.py` *require* it for procedure skills.

---

## 7. Migration plan (phased, bold but staged)

You don't re-platform 26 skills by hand. You bootstrap the forge, then let it regenerate the library.

**Phase 0 — Forge first (1 sitting).** Rebuild `skill-author` to §5. Build `validate_skill.py` and `run_evals.py`. This is the lever; nothing else proceeds until it's right and self-validating.

**Phase 1 — Spec & convention freeze.** Write `skill_spec.md` (the single source of truth for frontmatter + the two archetypes + the DoD contract). Decide the skills directory layout and the `AGENTS.md`-as-generated-index approach. Run `validate_skill.py` across the existing 26 to produce a failure report — instant prioritized backlog.

**Phase 2 — Regenerate, don't rewrite.** Feed each existing skill + its references through the forge: fix frontmatter, sharpen `description`, strip ceremony, add ≥3 evals, validate. Start with the 5 you use most (likely `resonance-core`, `backend`, `frontend`, `copywriter`, `architect`). The reference libraries mostly survive untouched — only `SKILL.md` and frontmatter change.

**Phase 3 — Collapse workflows into skills.** Move `.agents/workflows/*` into the skills tree as procedure skills using the template. Generate `AGENTS.md` Roster + Workflow Map from frontmatter so the operator UX you have today is preserved automatically.

**Phase 4 — Enforce & package.** Add the optional hook layer (where the runtime supports it) for the deterministic Behavioral Locks. Wrap the whole thing in a bundle manifest + installer. Optionally publish.

**Phase 5 — Modernize content.** Refresh dated references (the 2023 prompt-engineering docs, any tool cheatsheets that have drifted). Lowest priority; the content is mostly still good.

---

## 8. Specific quick wins (do these even if you do nothing else)

1. **Fix every `description`.** Third person, "use when", trigger terms, ≤1024 chars. Highest ROI single change — it's what makes skills actually fire.
2. **Delete the invalid frontmatter** (`tools: [read_file…]`, `model`, `skills:`). It does nothing today and misleads future-you.
3. **Write `validate_skill.py`.** A few hours; instantly grades all 26 and becomes the forge's test suite.
4. **Add 3 evals to one skill** (`resonance-copywriter` is the easy proof — you already have `banned_phrase_scan.py` as a ready-made grader). Prove the loop, then templatize it.
5. **Shrink `SKILL_TEMPLATE.md`.** Cut KPIs / Iron Man Suit / ELI16 / recovery ceremony down to the two lean archetype templates. Your skills will get smaller and trigger better.
6. **Kill the 2023 references** in skill-author (CoT "magic phrase", persona injection). They actively work against modern models.

---

## 9. The through-line

Your framework already believes the right things: externalize cognition, push determinism down, never solve the same problem twice, fight slop, demand a definition of done. The 2026 state of the art is, almost word for word, the formalized version of your philosophy — *plus three things you wrote about but never built: evals, validators, packaging.* So this isn't a teardown. It's finishing the building you started, on the foundation the rest of the industry has now standardized, with the one skill — the forge — that lets everything else regenerate itself to the new standard.

Build the forge. Everything else follows.
