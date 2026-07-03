# Changelog

## v2.5.0

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
