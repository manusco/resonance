# Resonance

> Operator-grade AI agent skills for builders. A cross-tool skill library and slash-command system for Claude Code, Cursor, Codex, and opencode, covering strategy, design, engineering, marketing, sales, and ops.

<div align="center">
    <a href="https://github.com/manusco/resonance"><img src="https://img.shields.io/badge/Resonance-v2.4.83-7025eb?style=for-the-badge&logo=github" alt="Resonance" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-black?style=for-the-badge" alt="License" /></a>
    <img src="https://img.shields.io/badge/Skills-60+-00f2ea?style=for-the-badge" alt="63 skills" />
    <img src="https://img.shields.io/badge/Commands-34-7025eb?style=for-the-badge" alt="34 commands" />
</div>

<div align="center">
    <strong>Claude Code</strong> &nbsp;·&nbsp; <strong>Cursor</strong> &nbsp;·&nbsp; <strong>Codex</strong> &nbsp;·&nbsp; <strong>opencode</strong> &nbsp;·&nbsp; <strong>Antigravity</strong>
</div>

---

## What it is

Resonance is an AI agent skill library you drop into any project. It turns a general coding agent into a roster of specialists that follow the same expert protocol every time, on whatever tool you use.

- **60+ domain-tested skills** across strategy, engineering, design, marketing, sales, ops, research, people, and success. Each skill is a structured procedure with prerequisites, a step-by-step algorithm, a Recovery path, and a Definition of Done, backed by a deep reference library. Not a prompt. A protocol.
- **34 slash commands** like `/plan`, `/grill`, `/build`, `/debug`, `/design`, `/test`, `/improve`, and `/ship`. Type the command, or describe the job and let the specialist auto-fire.
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
| **Codex** | Custom prompts in `.codex/prompts/<cmd>` plus `AGENTS.md` routing | `/plan`, `/ship`, ... |
| **opencode** | Commands in `.opencode/command/<cmd>` plus `AGENTS.md` routing | `/plan`, `/ship`, ... |
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
/grill         # stress-test that plan before any code
/build         # execute it with a TDD loop
/ship          # release with pre-flight checks
```

That is the whole setup. No install step, no plugin required.

---

## The command catalog

Every command is a structured procedure with a Definition of Done, not a loose prompt. Full map in [AGENTS.md](AGENTS.md).

**The autonomous loop**
`/goal "<outcome>"` frames the goal, decomposes it, then builds and verifies each slice against real checks (tests, validators, audit), bounded and never auto-shipping. The conductor for the skills below.

**Inception**
`/init` bootstrap project memory · `/venture-model` business and revenue math · `/plan` atomic implementation plan · `/grill` stress-test a plan before code · `/gtm-thinker` go-to-market blueprint · `/market-research` B2B vertical intelligence · `/update-roadmap` sync state with git

**Execution**
`/build` TDD build loop · `/debug` root-cause analysis · `/refactor` behavior-preserving cleanup · `/design` elite UI craft and audit · `/studio` production visual assets · `/friction` conversion friction removal

**Verification**
`/test` 8-Path test matrix · `/audit` security + review + QA + architect swarm · `/page-audit` first-principles page and site audit · `/review-pr` PR gatekeeper · `/second-opinion` independent second-model review · `/improve` self-improving eval loop · `/system-health` health score 0-100

**Delivery & maintenance**
`/ship` release protocol · `/incident` production incident response · `/seo` SEO and GEO audit · `/voice-profile` extract a voice profile · `/call-intelligence` analyze a sales call · `/cold-call` cold-call script · `/sales-pipeline` pipeline analytics · `/capture` document a solved problem · `/explain` teach the operator · `/handover` end-of-session handover · `/retro` git-driven retrospective · `/update-resonance` safe framework upgrade · `/skill-author` build a new skill

---

## The skill domains

60+ skills across 9 domains, each a self-contained protocol backed by reference docs.

- **Strategy**: `plan`, `grill`, `architect`, `venture`, `finance`, `growth`, `researcher`, `gtm-thinker`. Planning, system design, business and financial modeling, fundraising, and pre-build interrogation.
- **Engineering**: `backend`, `frontend`, `mobile`, `database`, `devops`, `debugger`, `build`, `automation`, `performance`, `game-dev`, `ai-engineering`. Build, debug, and ship, including AI and LLM products built eval-first, with defense-in-depth and deterministic tests.
- **Design**: `designer`, `studio`. First-principles UI craft: optical precision, perceptual color (OKLCH), typographic hierarchy, motion with physics, the subconscious detail layer, and cross-canvas design from phone to TV.
- **Marketing**: `seo`, `conversion`, `copywriter`, `paid-acquisition`, `analytics`, `lifecycle`. Search and GEO, conversion, paid media, measurement and attribution, and the full lifecycle from activation to win-back.
- **Sales**: `pipeline`, `cold-call`, `call-intelligence`, `account-intelligence`, `lead-ops`, `outbound-sequence`, `revops`. Qualification, outreach, call analysis, and revenue operations.
- **Ops**: `goal`, `founder-os`, `improve`, `audit`, `page-audit`, `qa`, `security`, `reviewer`, `second-opinion`, `refactor`, `ship`, `incident`, `observability`, `legal`, `librarian`, `explain`, `handover`, `retro`, `product`, `productivity`, `voice`, `core`, `skill-author`. Quality, security, delivery, reliability, incident response, legal and GDPR compliance, evidence-based self-improvement, teaching the operator, the founder operating system, and governance.
- **Research**: `market-research`. Market sizing, competitive intelligence, and positioning.
- **People**: `hiring`. Scorecards, structured interview loops, evidence-based debriefs, comp bands, and onboarding.
- **Success**: `customer-success`. Time-to-value, health scoring, the renewal and NRR motion, expansion, and churn saves.

---

## How it works

**Determinism beats improvisation.** When the agent runs `/debug`, it does not guess. It writes a reproduction script that fails 100% of the time before it writes a single line of fix, then hardens every layer the bad data crossed so the bug class cannot recur. When it runs `/audit`, it follows a fixed swarm order, not a vibe. Same protocol, same checklist, every time.

**The Forge compiles one source to many targets.** Skills are authored once as templates in `.forge/skills/`, then compiled per tool and per model into ready `SKILL.md` files, with shared sections (voice, decisions, completion, the operating standard) injected from one place. A static validator checks every skill, and each ships with at least three golden evals.

```
template.skill.md   x   host (tool)   x   overlay (model)   ->   SKILL.md
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

Working in the Resonance repo directly is the simplest path (everything is committed and ready). To add Resonance to an existing project, copy the identity file, the skills, and the compiler, then generate the command shims:

**macOS / Linux**
```bash
git clone https://github.com/manusco/resonance ~/resonance-tmp
cp ~/resonance-tmp/AGENTS.md ./AGENTS.md
cp -r ~/resonance-tmp/.agents ./.agents
cp -r ~/resonance-tmp/.forge ./.forge
py ./.forge/forge.py commands --host all   # writes the per-tool command shims and the CLAUDE.md / .cursor/rules context bridges
rm -rf ~/resonance-tmp
```

**Windows (PowerShell)**
```powershell
git clone https://github.com/manusco/resonance $env:TEMP\resonance-tmp
Copy-Item "$env:TEMP\resonance-tmp\AGENTS.md" ".\AGENTS.md"
Copy-Item "$env:TEMP\resonance-tmp\.agents" ".\.agents" -Recurse
Copy-Item "$env:TEMP\resonance-tmp\.forge" ".\.forge" -Recurse
py .\.forge\forge.py commands --host all
Remove-Item "$env:TEMP\resonance-tmp" -Recurse -Force
```

Then open your AI tool and type `/init`. It writes your project's vision to `.resonance/00_soul.md` and sets up the memory structure.

---

## Project memory

The `.resonance/` folder is what makes the agent persistent across sessions. Its state and memory load at the start of every session through the per-tool context bridge, so the agent begins each session already knowing your project. You own it; upgrades never touch it.

| File | What it holds |
| :--- | :--- |
| `00_soul.md` | Vision, mission, and the laws that govern the project. Written once, referenced forever. |
| `01_state.md` | Active task, last decision, current blocker. Updated after every session. |
| `02_memory.md` | The lessons index, loaded every session so a lesson written once is read every time after. One line per lesson; detail in `memory/` leaf files. Settled decisions live under `## Decisions` in the same file. Recall deeper slices by meaning with `.forge/recall.py`. Never solve the same problem twice. |
| `03_tools.md`, `04_systems.md` | Tool boundaries and the system architecture map. |
| `guards.json` | Project-specific guardrails and constraints. |

---

## Upgrading

Resonance reorganizes its skill library between versions, so a plain copy leaves ghost files the agent will still read. Delete the generated trees first, then copy the new version in. Your `.resonance/` memory is never part of this.

```bash
git clone https://github.com/manusco/resonance ~/resonance-tmp
rm -rf .agents .claude/skills .cursor/skills .codex/prompts .opencode/command
cp -r ~/resonance-tmp/.agents ./.agents
cp -r ~/resonance-tmp/.forge ./.forge
cp ~/resonance-tmp/AGENTS.md ./AGENTS.md
py ./.forge/forge.py commands --host all
rm -rf ~/resonance-tmp
```

Verify with `/system-health`.

---

## Extend it

Add your own skill with the meta-skill:

```
/skill-author
```

It walks the eval-first loop: prove the gap, write the golden evals, author the template, compile with the Forge, pass the validator, and only then ship. See `.forge/README.md` for the compiler and `.agents/skills/ops/skill-author/resonance-skill-author/` for the spec.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

Maintained by [divisionAI.co](https://www.divisionAI.co)
