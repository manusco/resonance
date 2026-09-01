# Resonance

> Operator-grade AI agent skills for builders. A cross-tool skill library and slash-command system for Claude Code, Cursor, Codex, and opencode, covering strategy, design, engineering, marketing, sales, and ops.

<div align="center">
    <a href="https://github.com/manusco/resonance/releases/latest"><img src="https://img.shields.io/badge/Resonance-v2.5.2-7025eb?style=for-the-badge&logo=github" alt="Resonance v2.5.2" /></a>
    <a href="https://github.com/manusco/resonance/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/manusco/resonance/ci.yml?branch=main&style=for-the-badge&label=CI" alt="CI status" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-black?style=for-the-badge" alt="License" /></a>
<!-- RESONANCE-GENERATED:SKILL_COUNT_BADGE:START -->
    <img src="https://img.shields.io/badge/Skills-72-00f2ea?style=for-the-badge" alt="72 skills" />
<!-- RESONANCE-GENERATED:SKILL_COUNT_BADGE:END -->
<!-- RESONANCE-GENERATED:COMMAND_COUNT_BADGE:START -->
    <img src="https://img.shields.io/badge/Commands-37-7025eb?style=for-the-badge" alt="37 commands" />
<!-- RESONANCE-GENERATED:COMMAND_COUNT_BADGE:END -->
</div>

<div align="center">
    <strong>Claude Code</strong> &nbsp;·&nbsp; <strong>Cursor</strong> &nbsp;·&nbsp; <strong>Codex</strong> &nbsp;·&nbsp; <strong>opencode</strong> &nbsp;·&nbsp; <strong>Antigravity</strong>
</div>

---

## What it is

Resonance is an AI agent skill library you drop into any project. It turns a general coding agent into a roster of specialists that follow the same expert protocol every time, on whatever tool you use.

<!-- RESONANCE-GENERATED:SKILL_COUNT_SUMMARY:START -->
- **72 domain-tested skills** across design, engineering, finance, leadership, marketing, ops, people, research, sales, software, strategy, and success. Each skill is a structured procedure with prerequisites, a step-by-step algorithm, a Recovery path, and a Definition of Done, backed by a deep reference library. Not a prompt. A protocol.
<!-- RESONANCE-GENERATED:SKILL_COUNT_SUMMARY:END -->
<!-- RESONANCE-GENERATED:COMMAND_COUNT_SUMMARY:START -->
- **37 slash commands** like `/brief`, `/plan`, `/grill`, `/council`, `/build`, `/debug`, `/design`, `/test`, `/improve`, and `/ship`. Type the command, or describe the job and let the specialist auto-fire.
<!-- RESONANCE-GENERATED:COMMAND_COUNT_SUMMARY:END -->
- **Cross-tool by design.** One source compiles to the native format of every major agent tool. The `SKILL.md` / `AGENTS.md` open standard is the shared content; the Forge emits the per-tool command shims and the per-tool context bridge, so the operating standard, the commands, and the project memory all load after a clone in Claude Code, Cursor, Codex, opencode, and Antigravity.
- **A project memory** (`.resonance/`) that loads at the start of every session and the agent writes back to. It does not forget your architecture, your decisions, or your voice.
- **Token-efficient.** The shared operating standard is stated once in `AGENTS.md`, not repeated in every skill. Compiled skills are lean, so per-session context stays cheap.

You get consistent, high-quality output because the agent runs the same protocol every time, not because you remembered to ask nicely.

---

## Works in your tool

| Tool | How commands are delivered | Status |
| :--- | :--- | :--- |
| **Claude Code** | Native skills in `.claude/skills/<cmd>` | `/plan`, `/ship`, ... |
| **Cursor** | Skills in `.cursor/skills/<cmd>` | `/plan`, `/ship`, ... |
| **Codex** | Agent Skills discovery plus `AGENTS.md` routing | describe the job or select a skill |
| **opencode** | Commands in `.opencode/commands/<cmd>` plus `AGENTS.md` routing | `/plan`, `/ship`, ... |
| **Antigravity** and other AGENTS.md tools | `AGENTS.md` command map | describe the job |

The command shims are generated from one source (`.forge/commands.json`) by the Forge, which also emits the per-tool **context bridge**: the file each tool loads at session start, pointing it at `AGENTS.md` and the `.resonance/` memory. Claude Code loads `CLAUDE.md`, not `AGENTS.md`, so the Forge writes a root `CLAUDE.md` that imports both; Cursor gets an always-applied `.cursor/rules/resonance.mdc`; Codex, opencode, and Antigravity read `AGENTS.md` natively. Without the bridge the operating standard and memory never reach the model. Adding a new tool is one host-config line.

---

## Quickstart (60 seconds)

```bash
git clone https://github.com/manusco/resonance
cd resonance
```

Open the folder in Claude Code, Cursor, Codex, or opencode. The slash commands are already committed, so they work immediately. In your AI chat:

```
/init          # scaffold this project's memory (.resonance/)
/plan          # turn an idea into an atomic, approved plan
/grill         # stress-test the plan or goal contract before code
/build         # execute it with a TDD loop
/ship          # release with pre-flight checks
```

That is the whole setup. No install step, no plugin required.

---

## The command catalog

Every command is a structured procedure with a Definition of Done, not a loose prompt. Full map in [AGENTS.md](AGENTS.md).

<!-- RESONANCE-GENERATED:COMMAND_CATALOG:START -->
The registry contains **37 commands**.

**Autonomous loop**
`/goal`: The autonomous goal loop: frame, decompose, then build and verify each slice against real checks, bounded, never auto-ship.

**Inception**
`/init`: Bootstrap the .resonance/ project memory (soul, state, docs scaffold). Run once per new project. · `/venture-model`: Model the business, offer stack, and revenue math before planning. · `/brief`: Turn a rough request into an intent-faithful execution brief, then run or route it within the user's authority. · `/blueprint`: Create or revise a durable architecture constitution, or check a plan, change, PR, or release for architectural drift. · `/plan`: Turn a feature or idea into an atomic, approved implementation plan. Deep research, 4-pass spec. · `/grill`: Stress-test a plan or design before any code: relentless one-question-at-a-time interrogation to shared understanding. · `/council`: Challenge an analysis or high-risk decision through relevant specialist reviews, debate, scenarios, and reconciliation. · `/gtm-thinker`: Stress-test and expand a go-to-market campaign concept into a strategic blueprint with kill criteria. · `/market-research`: Discover Existential Data Points in a B2B SaaS vertical. Positioning from nice-to-have to must-have. · `/update-roadmap`: Sync .resonance/01_state.md with the git log so the map matches the territory.

**Execution**
`/build`: Execute the implementation plan with a TDD loop (test, code, verify). · `/debug`: Root-cause a bug via the Scientific Method. Reproduction script required, no fix without a proven cause. · `/refactor`: Atomic, behavior-preserving cleanup. Mikado method, safe sequence, SOLID. · `/design`: Design or audit UI with elite craft: hierarchy, perceptual color, motion, and the subconscious detail layer. · `/studio`: Produce production-ready visual assets with structured prompt engineering. · `/friction`: Friction Collider: simulate the anti-persona to find and remove conversion drag.

**Verification**
`/test`: Write or audit tests against the 8-Path Matrix. Destructive and property-based coverage. · `/audit`: Run the audit swarm (security, review, QA, architect) and output P0-P3 classified findings. · `/page-audit`: First-principles experience audit of a page or whole site: job, value promise, clarity, CTA, craft, function, trust, plus a forward backlog. · `/review-pr`: Audit a PR or diff against the Blocking Registry. Findings ranked by user harm, not by file order. · `/second-opinion`: Independent second-model review of a diff, reconciled with the primary review. · `/improve`: Work the eval scorecard: sharpen the weakest skills or their rubrics and keep only changes that raise the measured lift. · `/system-health`: Score system health 0-100 with qualitative flags (auth, env, test depth).

**Delivery and maintenance**
`/ship`: Release protocol: pre-flight checks, changelog, semantic version, tag, deploy. · `/incident`: Drive a live production incident: triage, severity, mitigate, comms, blameless postmortem. · `/seo`: SEO and GEO audit: structured data, canonical, schema, AI-citation optimization. · `/voice-profile`: Extract a portable behavioral voice profile from a corpus (person, brand, or character). · `/call-intelligence`: Analyze a call transcript for persona insights, objection patterns, and feature requests. · `/cold-call`: Generate a B2B cold-call script using the 6-part permission-based framework. · `/sales-pipeline`: Render a pipeline analytics dashboard with velocity and forecasting from CRM data. · `/capture`: Document a solved problem in the correct Diataxis quadrant so it is never re-discovered. · `/explain`: Teach the operator, not the repo: a dense explainer of a concept, diff, or recent work, with an optional predict-then-reveal check-in. · `/handover`: Write an end-of-session handover doc: what was done, decisions, open TODOs, backlog. · `/retro`: Git-driven retrospective: shipping streak, focus score, complexity delta. · `/update-resonance`: Upgrade the Resonance framework with backup and restore safety. Preserves .resonance/. · `/skill-author`: Author, validate, and eval a new Resonance skill with the Forge.

**Which command should I use?**
- Use `/brief` to recover intent and route unclear work. Use `/plan` when the intended outcome is already clear and needs an implementation plan.
- Use `/grill` to interrogate a plan or goal contract before execution. Use `/council` to challenge a completed analysis or a consequential decision.
- Use `/test` for test design and coverage, `/review-pr` for a concrete diff, `/audit` for a multi-specialist finding review, and `/system-health` for a repeatable health score.
- Use `/blueprint` to establish or revise the durable architecture baseline and check conformance. Use the architect for an isolated system design, `/plan` for implementation sequencing, and `/review-pr` for general correctness.
- Use `/goal` to drive an outcome across stages, `/build` to execute an approved implementation plan, and `/ship` to prepare and perform a release.

If the route is still unclear, start with `/brief`.
<!-- RESONANCE-GENERATED:COMMAND_CATALOG:END -->

---

## The skill domains

<!-- RESONANCE-GENERATED:SKILL_DOMAIN_COUNT:START -->
72 skills across 12 domains, each a self-contained protocol backed by reference docs.
<!-- RESONANCE-GENERATED:SKILL_DOMAIN_COUNT:END -->

- **Strategy**: `blueprint`, `plan`, `grill`, `architect`, `venture`, `finance`, `growth`, `researcher`, `gtm-thinker`. Architecture governance, planning, system design, business and financial modeling, fundraising, and pre-build interrogation.
- **Software**: `deliver-change`. End-to-end software delivery from contract through plan, build, evidence, audit, and release proposal without auto-shipping.
- **Finance**: `run-operating-cycle`. Actuals, runway, scenarios, decisions, and metric follow-up from sourced data.
- **Leadership**: `run-operating-cycle`. Goals, decisions, delegation, hiring, feedback, cadence, and operating reviews.
- **Engineering**: `backend`, `frontend`, `mobile`, `database`, `devops`, `debugger`, `build`, `automation`, `performance`, `game-dev`, `ai-engineering`. Build, debug, and ship, including AI and LLM products built eval-first, with defense-in-depth and deterministic tests.
- **Design**: `designer`, `studio`. First-principles UI craft: optical precision, perceptual color (OKLCH), typographic hierarchy, motion with physics, the subconscious detail layer, and cross-canvas design from phone to TV.
- **Marketing**: `seo`, `conversion`, `copywriter`, `content-distribution`, `paid-acquisition`, `analytics`, `lifecycle`, `run-campaign`. Search and GEO, conversion, organic distribution, paid media, measurement, lifecycle, and governed campaign preparation.
- **Sales**: `pipeline`, `cold-call`, `call-intelligence`, `account-intelligence`, `lead-ops`, `outbound-sequence`, `revops`, `run-revenue-motion`. Qualification, outreach, call analysis, forecasting, and governed revenue motions.
- **Ops**: `goal`, `founder-os`, `improve`, `audit`, `page-audit`, `qa`, `security`, `reviewer`, `second-opinion`, `refactor`, `ship`, `incident`, `observability`, `legal`, `librarian`, `explain`, `handover`, `retro`, `product`, `productivity`, `voice`, `core`, `skill-author`. Quality, security, delivery, reliability, incident response, legal and GDPR compliance, evidence-based self-improvement, teaching the operator, the founder operating system, and governance.
- **Research**: `market-research`. Market sizing, competitive intelligence, and positioning.
- **People**: `hiring`. Scorecards, structured interview loops, evidence-based debriefs, comp bands, and onboarding.
- **Success**: `customer-success`. Time-to-value, health scoring, the renewal and NRR motion, expansion, and churn saves.

---

## How it works

**Determinism beats improvisation.** When the agent runs `/debug`, it does not guess. It writes a reproduction script that fails 100% of the time before it writes a single line of fix, then hardens every layer the bad data crossed so the bug class cannot recur. When it runs `/audit`, it follows a fixed swarm order, not a vibe. Same protocol, same checklist, every time.

**The Forge compiles one source to many targets.** Skills are authored once as templates in `.forge/skills/`, then compiled per tool and per model into ready `SKILL.md` files, with shared sections (voice, decisions, completion, the operating standard) injected from one place. A static validator checks every skill, and each ships with at least three golden evals.

```
template.skill.md   x   portable profile   ->   canonical SKILL.md
```

**Rebuild after editing a template:**
```bash
py .forge/forge.py build --all        # compile every skill
py .forge/forge.py commands --host all # regenerate the slash-command shims
py .forge/validate_skill.py --all .agents/skills
```

**Enforce the rules (optional):** `py .forge/hooks/install.py` installs a git guard that blocks em/en dashes, Soul edits, and committed secrets, and runs the library validator when skills change. Deterministic, cross-tool, opt-in. See `.forge/hooks/README.md`.

**Give the agent eyes (grounded verification):** `.forge/exec/run_checks.py` runs the project's real tests on any toolchain (Node, Python, Go, Rust, Make); `.forge/exec/browser_check.mjs` opens a real headless browser and reports the title, console errors, missing elements, and a screenshot. `/test` and `/goal` ground on these, not on the model's own read of its work. See `.forge/exec/README.md`.

**Prove the skills work, do not just assert it:** `npm run eval:score` runs every golden case with and without its skill and grades the lift, with the honesty rules enforced by the runner: the judge is never the answerer, at least three generations per arm, deterministic checks where a machine can grade, planted-defect cases for ground truth, and a calibrated keep/revert gate for improvements. Results are yours and never land in this repo. Method and calibration protocol: [`docs/EVALS.md`](docs/EVALS.md). Skills with no measured lift become the work-list, not a mystery.

---

## Use it inside your own project

Working in the Resonance repo directly is the simplest path. For another project, use the transactional installer. It previews every write, refuses user-owned conflicts, records ownership hashes, stages outside the target, backs up replaced files, and rolls back a failed apply.

**macOS / Linux**
```bash
gh repo clone manusco/resonance ~/resonance-source -- --branch v2.5.2
python3 ~/resonance-source/.forge/update.py --source ~/resonance-source --target . --version 2.5.2
python3 ~/resonance-source/.forge/update.py --source ~/resonance-source --target . --version 2.5.2 --apply
```

**Windows (PowerShell)**
```powershell
gh repo clone manusco/resonance "$env:TEMP\resonance-source" -- --branch v2.5.2
py "$env:TEMP\resonance-source\.forge\update.py" --source "$env:TEMP\resonance-source" --target . --version 2.5.2
py "$env:TEMP\resonance-source\.forge\update.py" --source "$env:TEMP\resonance-source" --target . --version 2.5.2 --apply
```

The first command is a dry run. Review its JSON plan before `--apply`. For an older installation with no ownership manifest, check out its installed Resonance version and pass that checkout as `--source` to the new updater with `--adopt`. Adoption claims only byte-identical released files and changes no framework file. Then use the new version checkout for the dry run and apply. A project-owned `AGENTS.md` or modified framework file remains a conflict until you review and resolve it.

Then open your AI tool and type `/init`. It writes your project's vision to `.resonance/00_soul.md` and sets up the memory structure.

For architecture, `.resonance/04_systems.md` keeps two explicit layers in one
place. Its architecture constitution contains the normative principles and
constraints. Its system record captures current technologies, topology,
deployment, and workflows without turning every implementation fact into law.
Run `/blueprint create` before a change creates a durable boundary or makes
failure costly to reverse, such as canonical data ownership, authorization,
billing, multi-tenancy, async delivery, a critical provider, recovery behavior,
a second deployable service, or a measurable scale or reliability target.
Before `/build`, every approved plan gets a quick applicability screen. Plans
that touch a governed concern require `/blueprint check`; routine local changes
do not. Small projects use the same file without inventing a second architecture
document or a speculative target.

---

## Project memory

The `.resonance/` folder is what makes the agent persistent across sessions. Its state and memory load at the start of every session through the per-tool context bridge, so the agent begins each session already knowing your project. You own it; upgrades never touch it.

| File | What it holds |
| :--- | :--- |
| `00_soul.md` | Vision, mission, and the laws that govern the project. Written once, referenced forever. |
| `01_state.md` | Active task, last decision, current blocker. Updated after every session. |
| `02_memory.md` | The lessons index, loaded every session so a lesson written once is read every time after. One line per lesson; detail in `memory/` leaf files. Settled decisions live under `## Decisions` in the same file. Recall deeper slices by meaning with `.forge/recall.py`. Never solve the same problem twice. |
| `03_tools.md`, `04_systems.md` | Tool boundaries, then the architecture constitution and descriptive system record in one canonical file. |
| `guards.json` | Project-specific guardrails and constraints. |

---

## Upgrading

Use the source checkout's transactional updater. It removes stale framework-owned files, but it never overwrites modified or project-owned files without review. Your project memory remains outside the managed write set.

```bash
gh repo clone manusco/resonance ~/resonance-source -- --branch <version-tag>
python3 ~/resonance-source/.forge/update.py --source ~/resonance-source --target . --version <version>
python3 ~/resonance-source/.forge/update.py --source ~/resonance-source --target . --version <version> --apply
```

The first command previews the transaction. Installations created before ownership manifests must run `--adopt` from a clean checkout of their installed version first. Adoption accepts only byte-identical released files. Recovery uses `update.py --rollback <backup-directory>`.

Verify with `/system-health`.

---

## Extend it

Add your own skill with the meta-skill:

```
/skill-author
```

It walks the eval-first loop: prove the gap, write the golden evals, author the template, compile with the Forge, pass the validator, and only then ship. See `.forge/README.md` for the compiler and `.agents/skills/ops/skill-author/resonance-skill-author/` for the spec.

Project-specific or private team skills belong in the same repository under `.agents/skills/`. They stay multiplayer, reviewable, and branchable with the code. After installing Resonance, run `python3 .forge/project_skills.py` and commit `.resonance/project-skills.lock.json`; use `--check` in CI. Framework upgrades preserve those unowned skill files and refuse mixed ownership instead of overwriting them. Do not use a mutable global skills directory as the canonical copy of a team procedure.

---

## Contributing

Questions belong in [GitHub Discussions](https://github.com/manusco/resonance/discussions). Bugs, proposals, and support routes are listed in [SUPPORT.md](SUPPORT.md).

See [CONTRIBUTING.md](CONTRIBUTING.md) to improve the framework and [MAINTAINING.md](MAINTAINING.md) for versioning and releases. Report suspected vulnerabilities through the private process in [SECURITY.md](SECURITY.md).

---

Maintained by [divisionAI.co](https://www.divisionAI.co)
