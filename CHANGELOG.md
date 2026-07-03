# Changelog

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
