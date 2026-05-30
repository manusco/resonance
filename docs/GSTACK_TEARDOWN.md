# gstack Teardown — what `skillify` actually is, what to steal, and how it changes the v3 plan

> Companion to `RECOMMENDATION_V3.md`. You pointed me at `_input/gstack` (Garry Tan's framework) and its `skillify` skill as inspiration. Here's the honest read, plus how it reshapes the plan given your clarified constraints: **must run on every tool (Antigravity/Google, Codex/OpenAI, Cursor, OpenCode, …), every major LLM including open-source, not locked to the Anthropic standard, 1% elite.**

---

## 1. The headline: `skillify` is not what you think — but gstack around it is the real prize

You asked "is `skillify` a good skill to make skills?" **`skillify` is not a SKILL.md authoring tool at all.** It does one narrow thing: it takes the last successful `/scrape` run in the conversation and **codifies it into a permanent, deterministic browser-skill** — `script.ts` + `script.test.ts` + an HTML fixture — so the next time you ask for that data it runs a 200ms Playwright script instead of re-driving the page with an LLM. "Skill" here means a *scraping recipe*, not a `SKILL.md` persona/procedure.

So: as a "skill builder," it's the wrong reference. **But the pattern inside it is gold, and the architecture surrounding it is exactly the cross-tool, cross-model, eval-backed system you've been trying to build.** That's the real find. Don't copy `skillify`. Study gstack.

---

## 2. What `skillify` does that you SHOULD steal (the pattern, not the skill)

`skillify` is your own philosophy — "never solve the same problem twice," "push complexity into Layer 3," the Ratchet — turned into a concrete, shippable loop. Read its **"Iron contract — never write a half-broken skill to disk"**:

1. **Prototype slow, codify fast.** An LLM-driven exploration (slow, probabilistic) runs once; its successful path is frozen into deterministic code (fast, reliable). This is Layer 3 capture, operationalized.
2. **Provenance guard.** It refuses to synthesize from chat fragments — it only codifies a *verified, user-accepted* result. (Step 1: walk back ≤10 turns, find a bounded scrape the user didn't invalidate, else refuse with an exact message.)
3. **Synthesize artifact + test + fixture together.** Never code without a test and a captured fixture to test against.
4. **Atomic write through a temp dir.** Stage → run the test in the temp dir → only `commitSkill()` into the real path on (test passes) AND (explicit user approval). On any failure, `discardStaged()` — "there is no 'almost shipped' state."
5. **Post-commit verify.** Re-run and diff against the prototype output; surface drift, never silently roll back.

**This is the single most valuable transferable idea in the whole project.** Your `skill-author` and `workflow-builder` should both work exactly this way: stage to temp → run `validate_skill.py` + the skill's own evals → commit only on green + approval → verify. You already believe this ("No Commit Without Evidence"). gstack shows you the mechanism.

---

## 3. The real prize: gstack's generation architecture answers your cross-tool / cross-model requirement

This is what changes the v3 plan. You said you don't want to "just go with the Anthropic standard" and you need it to run everywhere — Antigravity, Codex, Cursor, OpenCode, open-source models. gstack has *already solved this*, and the solution is **not** "pick one standard." It's: **author once in templates, generate a tailored output per tool and per model.**

The evidence, straight from the repo:

```
gstack/
├── <skill>/SKILL.md.tmpl     ← YOU EDIT THIS (one source per skill)
├── <skill>/SKILL.md          ← GENERATED, "do not edit directly"
├── scripts/
│   ├── gen-skill-docs.ts      ← .tmpl → {{PLACEHOLDERS}} → resolve → write .md  (--host claude|codex|cursor|...|all)
│   └── resolvers/             ← shared sections injected into EVERY skill
│       ├── preamble.ts  voice  review-army  testing  model-overlay  composition ...
├── hosts/                     ← one typed config per TOOL
│   ├── claude.ts codex.ts cursor.ts opencode.ts factory.ts kiro.ts slate.ts openclaw.ts ...
│   └── host-adapters/         ← per-tool tool-name mapping (e.g. OpenClaw)
└── model-overlays/            ← one behavioral patch per MODEL FAMILY
    └── claude.md gemini.md gpt.md gpt-5.4.md o-series.md opus-4-7.md
```

Read that structure against your three problems:

| Your requirement | gstack's mechanism | What it means for you |
| :--- | :--- | :--- |
| "Works on every tool (Antigravity, Codex, Cursor, OpenCode…)" | `hosts/*.ts` + `host-adapters/` + `gen-skill-docs --host all` | Tool differences (tool names, invocation, path conventions) are abstracted into a host config. The generator emits a correct skill per tool from one template. |
| "Works on every LLM incl. open-source" | `model-overlays/*.md` + `resolvers/model-overlay.ts` | Per-model behavioral patch compiled into the skill. Weaker/open models get more explicit guardrails; strong models get terser prompts. Same skill, tuned per brain. |
| "Don't lock to the Anthropic standard" | Templates are the source of truth; `SKILL.md` is just *one* compiled output format | You own a generation layer *above* the format. The `SKILL.md`/`AGENTS.md` shape is the lingua franca every tool now reads — but you're not "adopting their standard," you're emitting it as one target among several. |

**This is the reconciliation of my v3 doc with what you actually want.** v3 said "adopt the open Agent Skills standard." You pushed back. gstack shows the correct, more ambitious answer: **emit the open format as a build target, but author in a tool-/model-agnostic template layer you control.** That's the 1% move. It's the difference between *writing skills* and *having a skill compiler.*

---

## 4. gstack also already built the two things v3 said you're missing

My v3 doc flagged evals and validators as your biggest gaps. gstack has both, fully realized — proof they're achievable, and a concrete blueprint:

**Eval harness (four tiers, from `CLAUDE.md` + `test/`):**
- Tier 1 — `skill-validation.test.ts`: static structural validation, free, <1s (the `validate_skill.py` I proposed).
- Tier 1 — `gen-skill-docs.test.ts`: the *generator's own* output quality is tested.
- Tier 3 — `skill-llm-eval.test.ts`: LLM-as-judge, ~$0.15/run.
- Tier 2 — `skill-e2e-*.test.ts`: real end-to-end via `claude -p`, ~$3.85/run, with ground-truth fixtures and **planted-bug fixtures**.
- **Two-tier gate/periodic** + **diff-based test selection** (each test declares file deps in `touchfiles.ts`; only affected tests run). CI runs `gate`; `periodic` runs weekly. This is how you keep a paid eval suite affordable.

**Deterministic quality enforcement:**
- `slop-scan` in CI for AI-code-quality (their take is sharp: "We are AI-coded and proud of it — the goal is code quality, not passing as human").
- A **voice resolver** injecting the same anti-slop banned-word list you already maintain — but into *every* generated skill from one source, not copy-pasted.

You were going to build these from scratch. Now you have a reference implementation to study first (Layer 1 before Layer 3 — your own rule).

---

## 5. The decision-brief format: steal this wholesale

gstack's `AskUserQuestion` format is the most refined version of your "Iron Man Suit / Recommendation-First" protocol I've seen. Every decision is a structured brief with a **self-check checklist** the model runs before emitting:

```
D<N> — <question title>
Project/branch/task: <grounding>
ELI10: <plain English, name the stakes>
Stakes if we pick wrong: <one sentence>
Recommendation: <choice> because <reason>
Completeness: A=X/10, B=Y/10   (or "differ in kind, no score")
A) <label> (recommended)  ✅ <pro ≥40 chars>  ❌ <con ≥40 chars>
B) ...
Net: <what you're trading off>
```

Plus a **tool-resolution rule** (prefer `mcp__*__AskUserQuestion` if present, else native, else write into the plan file — "never silently auto-decide") that is *itself* a cross-tool portability pattern. Your decision protocol is the right idea; this is the enforced, 1% execution of it.

---

## 6. Now the thing you actually want to discuss: workflows

You said: *"workflows matter because skills alone usually are not sufficient."* **You're right, and gstack proves it — but it also resolves the confusion in your current model.**

Look at gstack's highest-value skills: `/ship`, `/autoplan`, `/land-and-deploy`, `/plan-ceo-review`. These are *workflows* in your sense — multi-step procedures with gates, orchestration, and a definition of done. `CLAUDE.md` even notes they "legitimately pack 25-35K tokens of behavior." `/autoplan` orchestrates a *pipeline of other skills* (CEO review → design review → eng review). That's a workflow composing skills.

**And yet gstack has no `workflows/` folder.** Every one of those is just a `SKILL.md`. So the lesson is precise:

> Workflows are not a separate *primitive*. They are a separate *archetype* of skill — the procedure/orchestration archetype — and they are where most of the value lives. "Skills alone aren't sufficient" is true at the **knowledge-skill** level (a persona with reference docs is inert without a procedure to drive it). It stops being true once you treat a rich, gated, multi-step procedure as *also* a skill.

This refines §3 of the v3 doc. Your instinct to elevate workflows is correct. The fix isn't to keep them in a separate folder with a separate format — it's to make the **procedure/orchestration archetype first-class in your template system**, with the parts that make them valuable baked in:

1. **Input / Output / Definition-of-Done / Recovery** (you already have this — keep it, it's better than gstack's implicit version).
2. **Gates and STOP points** (gstack's plan-mode safety, approval gates, `/ship` review gates).
3. **Orchestration**: a procedure skill can invoke other skills (gstack's `/autoplan` → review pipeline) or fan out to subagents where the tool supports it.
4. **A completion-status protocol** (DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT — you and gstack already share this).

So: **three archetypes, one format, one compiler.**
- **Knowledge skill** — a domain expert + reference library (your `resonance-copywriter`).
- **Procedure skill** — a gated workflow with a DoD (your `/build`, `/ship`).
- **Orchestration skill** — a procedure that drives other skills/subagents (your `/audit` "swarm," gstack's `/autoplan`).

Your "26 agents + 18 workflows" becomes "N skills across 3 archetypes," all generated from one template layer, all evaluated by one harness, all portable across tools and models. That is the elite version.

---

## 7. How this changes the v3 plan (the updated Phase 0)

The v3 doc's "build the forge first" is still right, but gstack upgrades what the forge *is*. It's not a skill that writes a `SKILL.md`. It's a **skill compiler**:

**Phase 0 (revised) — build the compiler, not just the author.**
1. **Template + resolver layer.** Author skills as `.tmpl` with `{{PLACEHOLDERS}}`. Shared concerns (your voice/anti-slop, the decision-brief format, completion protocol, Karpathy locks, learnings logging) live in *resolvers*, injected into every skill from one source. No more copy-pasted boilerplate across 26 skills.
2. **Host configs.** One typed config per tool you use — start with the ones you named: Antigravity, Codex, Cursor, OpenCode, plus Claude Code. Abstract tool-name mapping and path conventions. (gstack's `hosts/` is your reference.)
3. **Model overlays.** One behavioral patch per model family — Claude, GPT/o-series, Gemini, and at least one open-source family (Llama/Qwen/DeepSeek). Weaker models → lower degrees of freedom, more explicit guardrails.
4. **`gen-skills` generator.** `.tmpl × host × model → output`. `--host all`, `--dry-run` for CI freshness (fail if committed output drifts from source).
5. **Eval harness, two-tier.** Static `validate` (free) + LLM-judge + E2E with golden + planted-bug fixtures. Diff-based selection so it stays cheap.
6. **The `skillify` pattern as the write path.** Stage to temp → validate + eval → commit only on green + approval → post-commit verify.

Then regenerate the existing library through the compiler (v3 Phases 1-5 unchanged).

---

## 8. Honest cautions — don't cargo-cult gstack

gstack is elite but it is also **heavily Claude-Code-and-Garry-shaped**, and parts are anti-patterns for you:

- **The preamble is enormous.** Look at `skillify` lines 26-744 — that's ~700 lines of telemetry, upgrade checks, gbrain sync, proactive prompts, vendoring warnings, jargon glossaries *before the actual skill starts at line 746.* That's their generator injecting every cross-cutting concern into every skill. Powerful, but it's a lot of machinery and a lot of tokens. Adopt the *mechanism* (resolvers) but keep your injected preamble lean — you don't need their telemetry/upgrade/brain-sync apparatus.
- **It's a product with a business model** (telemetry, ClawHub publishing, team mode, YC promotion baked into `ETHOS.md` which contributors are forbidden to touch). You're building a personal/operator framework. Strip the product scaffolding.
- **Bun/TypeScript-heavy and macOS-arm64-first** (compiled binaries, `~/.zshrc` key sourcing). Your stack is Windows/PowerShell. The *architecture* ports; the *implementation* doesn't — write your generator and validators in something you'll actually maintain (Python is fine and cross-platform).
- **Single-maintainer voice lock-in.** Their "Garry voice" is enforced everywhere. You have your own (anti-slop), which is good — just don't import theirs.

---

## 9. Bottom line

- **`skillify` itself:** not a skill-builder; don't integrate it. **But its "prototype → codify → test → atomic-commit → verify" Iron Contract is the best single pattern in the repo** — make it the write path of your forge.
- **gstack as a whole:** the strongest existing proof of the system you're trying to build. It answers your cross-tool / cross-model / not-locked-to-Anthropic requirement with a **template + resolver + host-config + model-overlay generation pipeline**, and it already has the **eval harness and validators** v3 said you lack. Study it as your Layer-1 reference, then build your own leaner, Windows-friendly, product-scaffolding-free version.
- **Workflows:** your instinct is validated by the best-in-class example. They matter, they hold most of the value — but they're an *archetype of skill*, not a separate primitive. Make the procedure/orchestration archetype first-class in the compiler.

The v3 verdict stands, sharpened: **don't build a skill-author. Build a skill compiler** — one source, three archetypes, every tool, every model, gated by evals. That's the 1% elite version, and gstack is the proof it's reachable.
