# Changelog

## v2.4.5

The grounded orchestration evals and the turnkey model adapter finish the measurement story the v2.4.4 scorecard opened. The copywriter gains the long-form argument for readers who are not yet convinced. And a new skill, `/page-audit`, adds an experience auditor to sit beside the code auditor.

### Added
- **Grounded orchestration evals (`.forge/orch_eval.py`, `.forge/orch_evals/`).** The completion scorecard cannot measure the skills whose value is a runtime (`/goal`, `/audit`, `/reviewer`): a single chat turn can only describe spawning agents or driving a repo, so they score near zero even when excellent. This harness measures them by grounded outcome instead. It stands up a fixture with planted ground truth, runs a real tools-capable agent against the task, then checks the world. Three cases ship: `/goal` must make a failing `node --test` pass (proven end to end, an agent fixed the planted bug and the executed suite went green), `/audit` must name a planted SQL-injection-and-missing-auth vulnerability, and `/reviewer` must flag a promote-to-admin endpoint with no authorization check. New npm script `orch-eval`.
- **A turnkey model adapter (`.forge/exec/model_cli.py`).** Turns any OpenAI-compatible endpoint into the stdin-prompt, stdout-completion contract the eval tools expect, with every lesson that cost real debugging time baked in: forced UTF-8 on stdin and stdout (the cp1252 default silently corrupts skill bodies into false zeros), a browser User-Agent (Cloudflare-fronted gateways 403 a bare urllib), bare `{model, messages}` by default (some gateways 500 on `temperature`), and retry with backoff. The key comes only from the environment, never a tracked file. Wire it with `RESONANCE_MODEL_CMD="python .forge/exec/model_cli.py"` and three env vars.
- **The copywriter learns long-form (`marketing/copywriter`).** A new `longform_sales_page_protocol.md` reference and the wiring to reach for it: the page you write when the reader is not yet convinced. It adds the half of Eugene Schwartz the skill was missing, the five stages of awareness, which set where the argument starts and how far it runs, next to RMBC and its write-the-lead-last order, Sugarman's slippery slide for line-by-line momentum, eye-relief formatting so a long page still reads fast, and voice-of-customer mining so the argument is harvested from real customer language, not invented. Three guardrails keep it honest for a trust-first framework: the mechanism of the problem must be real (a fabricated one fails fact preservation), precise numbers only where they are true, and readability is contextual, not a dogmatic grade. A sixth core principle, Length Follows the Argument, makes the stance explicit: go long only until every objection is answered, then stop. A fourth golden eval grades the failure it must prevent, a fabricated mechanism or statistic. Depth grew, not the skill count.
- **A new skill, `/page-audit`, the experience auditor (`ops/page-audit`).** The twin to `/audit`. Where the code swarm hunts for what is broken, this one walks up to each page and makes it prove why it deserves to exist. It grounds in `.resonance/`, inventories every page and state, and runs a first-principles battery per page, handing each lens to the skill that owns it (`/copywriter`, `/friction`, `/design`, `/seo`, `/audit`, `/test`, `/system-health`) and adding the three frames none of them carried: the page's job and what to remove, the gap between the promise and the delivery, and the anti-theater rule that the one change which moves a real user beats ten cosmetic ones. It writes a per-page findings sheet, a forward-looking `FUTURE_IMPROVEMENTS.md`, and a cross-site master report, then hands building to `/goal` and shipping to `/ship`. Two references, three evals, one command. The library is now 58 skills and 33 commands.

## v2.4.4

The "make it measurably the best" plan, Tracks 1 through 3, plus the full live eval scorecard. Resonance can now run the project's real tests and a real browser, measure whether each skill actually helps, improve the weak ones by evidence, and it covers three new domains an AI-era founder needs.

### Added
- **The full library scored by the tool, on two models (`docs/EVAL_SCORECARD.md`).** Every skill run cold versus skill-applied and graded per rubric. Under Claude (answerer and judge) mean lift was +0.68. A real-tool run via `run_evals.py --score` with GLM-5, a weaker independent model, scored **mean +0.38 with 40 of 57 skills measurably helped** (lift >= +0.20). The lift is real and model-dependent: large under a strong model, solid under a weak one. The doc explains the caveats: lift, not the near-ceiling `with`, is the signal; one case per skill; and orchestration skills (`/audit`, `/goal`, `/second-opinion`) read low because a single completion cannot spawn agents or dispatch a second model.
- **The execution surface (`.forge/exec/`): the agent's eyes.** `run_checks.py` detects the project's toolchain (Node with the right package manager, Python, Go, Rust, Make) and runs its real tests, returning structured pass or fail. `browser_check.mjs` opens a real headless browser and reports the title, console and page errors, whether required elements exist, and a screenshot. Both proven end to end (a real failing test caught, a broken page's console error and missing element caught). `/test` and `/goal` now ground on these, not on the model's own read of its work. New npm scripts `exec:test` and `exec:browser`.
- **The eval scorecard.** `run_evals.py --score` runs every golden case with and without its skill, grades both against the rubric, and writes a per-skill lift table to `docs/EVAL_SCORECARD.md` (with `--changed`, `--limit`, and parallelism). A live 4-skill sample is included: the rigor skills (debugger, plan) show large measured lift (+0.60 and +0.67); two came out flat and correctly flag their eval rubrics as too coarse (the /improve work-list). New npm script `eval:score`.
- **Three new domains (Track 2).** `engineering/ai-engineering`: build AI products the right way (eval-driven development, context engineering, RAG, agent design, guardrails, cost and latency), the glaring gap for an AI framework. `strategy/finance`: the money the venture skill leaves out (driver-based model, unit economics, runway, the raise, investor updates, cap table). `ops/legal`: a GDPR and DACH-native first pass on privacy, terms, DPAs, and contract review, with a clear line on where a lawyer must take over. 57 skills now.
- **The self-improving loop `/improve` (Track 3).** Reads the eval scorecard, works the skills with no measured lift, sharpens the body or the rubric, rebuilds, and keeps a change only when `improve.py remeasure` shows the lift actually rose. Its one hard rule: never weaken a rubric to pass it. New tool `.forge/improve.py`.
- **A cross-project brain.** `recall.py` now also reads `~/.resonance` (or `$RESONANCE_GLOBAL_BRAIN`), so a learning earned in one repo raises the floor in the next; `--local-only` opts out.

### Fixed
- **A silent Windows bug the scorecard caught.** The eval runner wrote prompts to the model subprocess with the OS locale (cp1252), which cannot encode the arrows and quotes in skill bodies, so every such skill failed silently. Forced UTF-8 on the subprocess I/O in the runner and the check runner. Measurement found a bug inspection missed.

## v2.4.3

The hygiene-and-craft release. The deterministic enforcement layer is now complete, the studio no longer contradicts the designer, and the last open items from the State of Resonance audit are shipped. 53 skills, 31 commands, both validators clean, 164 eval cases, and the whole repository is dash-clean including the tooling itself.

### Added
- **The hooks layer is complete.** The pre-push **ship-gate** blocks pushing a release tag or `main` when the gate is not green (skill validator, library validator, eval check, doc-drift): the deterministic form of "do not ship without a passing test." A **banned-vocabulary scan** for generated copy (`guard.py --copy`, or fold it into the pre-commit with `RESONANCE_STRICT_VOCAB=1`). And a **shipped Claude Code hook config** in `.claude/hooks/`, enabled with `py .forge/hooks/install.py --claude`, so the guard runs at edit time and hands any violation back to fix.
- **Designer depth.** Two new first-principles references: `data_visualization.md` (the perceptual encoding hierarchy, truthful axes, perceptual color for data, decluttering) and `iconography_system.md` (keyline grids, optical weight and correction, metaphor clarity, accessible hit targets).

### Changed
- **`design/studio` rebuilt.** De-tool-locked (model-agnostic prompting, no Midjourney-only flags) and de-slopped (no glassmorphism or bento grids as promoted styles). Studio now owns asset craft and defers all interface taste and the timeless-versus-slop call to `resonance-design-designer`, instead of contradicting it.
- **Cleaner domain boundaries.** The heavy B2B pipeline and CRM references moved from `strategy/growth` to `sales/pipeline` and `sales/lead-ops`, where the execution belongs. Growth stays focused on loops, retention, and GTM; the two sales procedures gain the reference libraries they lacked.
- **Consolidations.** `pricing_psychology` folded into `pricing_strategy_protocol` (with MaxDiff added); `launch_day_protocol` folded into `launch_strategy_protocol`; the audit taxonomy de-duplicated so `audit_classification_taxonomy` is the single canonical severity-and-category source and `universal_audit_directives` points to it.

### Fixed
- **The validator's blind spot.** `validate_library.py` now scans eval fixtures for em and en dashes, not only references and skill bodies. Fifty-nine dashes were stripped from 42 eval files, and the whole repository (skills, docs, and the Python tooling) is now dash-clean, so the guard passes its own source.
- Drift: `docker_optimization` pinned to a current Node LTS, the C4 model "System Context" typo, the thin `engineering/build` evals enriched to the full behavior set, and a perceptual-contrast (APCA) note added to the design-system contrast directive.

## v2.4.2

Close the remaining lifecycle gaps. The five domain-gap skills (observability, incident, paid-acquisition, analytics, lifecycle) and the test-execution surface shipped in v2.3.0; per-version overlays and deploy verification in v2.4.1. This release finishes the depth.

### Added
- **Auto-doc-drift.** `.forge/doc_drift.py` checks that the version matches across every manifest, README badge, and installer; that the AGENTS command map matches `commands.json`; and that the README counts and CHANGELOG are not stale. Wired into `/ship` as a pre-release gate, and run as the gate for this very release.
- **Activation reference in `strategy/growth`** (`activation_loops.md`): the aha moment and time-to-value as the top of every retention and growth loop, distinct from the lifecycle skill's execution view.
- **Toolchain Detection** (`ops/core/references/toolchain_detection.md`): a shared protocol to detect and run a project's real test, build, and lint commands.

### Changed
- **`/ship` and `/system-health` are toolchain-agnostic.** They detect the project's ecosystem (Node with the right package manager, Python, Go, Rust, Make, or CI) and run its commands, instead of hardcoding `npm test`. No more silent failure on a non-Node project.

## v2.4.1

Release safety and enforcement. Per-version model overlays, a real deploy story in `/ship`, and an opt-in deterministic guard.

### Added
- **Per-version model overlays.** Alongside the family overlays (`claude`, `gpt`, `gemini`, `open-weights`), per-version patches: `opus-4-8`, `sonnet-5`, `haiku-4-5`, `gpt-5`, `o-series`. Stronger models get terser prompts; smaller models get more explicit step structure; reasoning models get no chain-of-thought scaffolding. The committed build stays on the family default; target a version with `--model opus-4-8`.
- **Deploy verification and canary in `/ship`.** Ship now confirms a rollback path before deploying, rolls out canary-first where supported, runs a post-deploy smoke test against production (health, a critical path, error rate), and rolls back on any trigger. Green CI is not done; verified production is. New `canary_and_rollback.md` reference and eval.
- **The hooks layer (opt-in).** `py .forge/hooks/install.py` installs a git pre-commit guard that blocks em/en dashes, edits to the Soul, and committed secrets, and runs the library validator when skills change. Cross-tool (git hooks), with a documented Claude Code option. Deterministic Layer-3 enforcement you turn on when you want it.

### Removed
- The stray untracked `VERSION` file at the repo root (Resonance versions via `package.json`).

## v2.4.0

The autonomous, memory-backed, cross-model-checked release. Resonance can now carry a goal to a verified finish, remember by meaning, and pressure a change with a second model. 53 skills, 31 commands, both validators clean, 163 eval cases.

### Added
- **`/goal`** (`ops/goal`): the autonomous goal loop. Frames the goal (via `/grill` into a checkable Definition of Done, human-approved), decomposes it into slices, then builds and verifies each against grounded checks (real tests via live execution, validators, `/audit`), bounded by `loop_state.py`, gated at one-way doors, and never auto-shipping. Defaults to running multiple slices between check-ins. The conductor over the existing skills.
- **`/second-opinion`** (`ops/second-opinion`): independent second-model review. Dispatches a diff to a different model via `.forge/second_opinion.py` (pluggable, graceful fallback), then reconciles the two reviews so agreements are high-confidence and disagreements get investigated, every finding verified against the code.
- **Memory recall (R6).** `.forge/recall.py` retrieves project memory by meaning (pure-Python BM25 by default, embeddings opt-in via `RESONANCE_EMBED_CMD`), and `.forge/decisions.py` is an append-only, event-sourced decision log (add, list, search, supersede, redact). Wired into `ops/core` so settled decisions resurface at session start and skills recall relevant memory instead of loading the whole brain.
- The bound enforcer `loop_state.py`, the review harness `second_opinion.py`, and the `memory_recall` reference.

### Changed
- `/test` now the grounded verifier the goal loop leans on (the R3 live-execution surface from v2.3.0).
- Moved lifecycle references fully out of `marketing/conversion` (superseded by `marketing/lifecycle` in v2.3.0).
- README memory table now documents `decisions.jsonl`, `03_tools`, `04_systems`, and `guards.json`.

### Tooling
- New npm-runnable tools alongside the compiler: `decisions.py`, `recall.py`, `second_opinion.py`, and `loop_state.py`, all pure stdlib and cross-platform.

## v2.3.0

The elevation release. A first-principles design rebuild, cross-tool slash commands that work on clone, a 34% token diet, a real eval runner and a cross-skill validator, an execution surface, five new skills, and a full hygiene pass. 51 skills, 0 errors, 0 warnings, 157 eval cases.

### Added
- **Cross-tool slash commands.** The Forge now generates per-tool command shims from one source (`.forge/commands.json`) into `.claude/skills/`, `.cursor/skills/`, `.codex/prompts/`, and `.opencode/command/`. `/plan`, `/ship`, and the rest work immediately after a clone, no install step. 29 commands.
- **A plugin.** `.claude-plugin/plugin.json` and `marketplace.json` for install-based use.
- **`/grill`** (`strategy/grill`): the pre-build interrogation gate. One question at a time, recommend an answer to each, gate implementation until shared understanding.
- **`/incident`** (`ops/incident`): production incident response. Triage, severity, mitigate-before-diagnose, cadenced comms, blameless postmortem.
- **New knowledge skills:** `ops/observability` (logging, metrics, tracing, SLOs, alerting), `marketing/paid-acquisition` (SEM, paid social, creative testing, unit economics), `marketing/analytics` (measurement plans, attribution, experimentation), `marketing/lifecycle` (activation, email, retention, churn, win-back).
- **The eval runner** (`.forge/run_evals.py`, R1): a structure-check gate plus a live with/without run and LLM-judge grading via a pluggable model command.
- **The cross-skill validator** (`.forge/validate_library.py`, R2): catches orphan references, diverged duplicates, eval name-drift, two-level links, attribution leaks, and dashes across the whole library.
- **A live-execution surface** (R3): `/test` (`ops/qa`) gained a `live_execution` protocol to run tests and drive a browser to verify against reality, the grounded verifier a goal loop needs.
- **Design craft library.** The rebuilt `design/designer` ships 11 new references: first principles, optical craft, typographic system, color and contrast (OKLCH, APCA), spatial system, motion and feel, depth and materials, responsive canvas, copy as interface, resilience and edge cases, and a pre-ship craft checklist.

### Changed
- **`design/designer` rebuilt from first principles.** Ten principles (optical over mechanical, clarity, contrast hierarchy, typography as interface, space as meaning, motion as physics, depth from light, perceptual color, copy as design, canvas-appropriate craft) plus restraint. The old "break every grid" dogma is demoted to a brand-only scalpel.
- **Token diet: 34% smaller.** The operating standard (voice, decisions, completion, ratchet) is stated once in the always-loaded `AGENTS.md` and referenced by a one-line pointer per skill instead of being injected into all skills. Resolvers and the model overlay compressed. No rule removed.
- **Absorbed external gold** into Resonance-native skills: defense-in-depth into the debugger, async test stability into qa, receiving-review discipline into the reviewer, and the design register plus AI-slop catalog into the designer.

### Fixed
- Systematic eval name-drift across five skills (15 files) that broke eval binding.
- Numbering and label bugs (qa Algorithm, debugger header), a startup-description typo, two wrong Role lines in sales, and the copywriter misrepresenting its own references.
- Stripped all attribution and provenance leaks and 394 em and en dashes from reference files.
- De-duplicated `resonance-skill-author`, reconciled the legacy designer references, resolved the `style_matrix` naming collision, and linked or removed the orphaned references.
- Reconciled naming conventions and moved lifecycle content out of the conversion skill into the new `marketing/lifecycle`.

### Tooling
- `npm run build` (compile all), `npm run commands` (regenerate shims), `npm run validate` (per-skill), `npm run check` (cross-skill library), `npm run eval` (eval structure gate).
