# Changelog

## v2.4.90

The evidence-binding fix-forward release. It tightens the v2.4.89 evidence
kernel before more work builds on it.

### Changed
- **Evidence must match the recorded execution.** Evidence now compares the full
  execution receipt against the receipt recorded by the active goal run, not only
  the execution id.
- **Terminal goals are immutable.** Completed or cancelled goals reject new
  checks, executions, and evidence.
- **Goal starts fail closed.** `/goal` now rejects empty goals, invalid contracts,
  invalid plan hashes, and attempts to overwrite an active goal.
- **Execution ids and run ids are collision-resistant.** Goal runs and execution
  receipts now include random nonces instead of relying on second-resolution
  timestamps.
- **Generated script runtime is covered.** The compiled `.agents` goal script can
  locate `.forge/kernel/` from generated locations.

## v2.4.89

The evidence-kernel release. Goal work now has a deterministic receipt boundary
under the skills, and software delivery gets one governed conductor without
adding another slash command.

### Added
- **Evidence kernel.** `.forge/kernel/` adds versioned contract helpers, legal
  goal transitions, atomic state writes, file locks, evidence receipt validation,
  typed ledger recall, and a generated skill manifest.
- **Evidence-bound goal state.** `/goal` now requires an approved plan hash,
  rejects stale evidence, requires accepted evidence for every acceptance
  criterion before `achieved`, refuses to clear active goals, and retains
  completed history.
- **Machine-readable skill catalog.** `docs/skill-manifest.json` records each
  skill's id, archetype, derived owner label, authority class, invokes, and
  failure policy. Library validation fails when this manifest drifts.
- **Software delivery conductor.** `software/deliver-change` coordinates goal,
  grill, plan, build, QA, audit, second opinion, and ship proposal for software
  changes without autonomous merge, tag, deploy, or release.
- **Kernel documentation and eval coverage.** New docs explain the receipt
  boundary, and the eval oracle now protects the kernel tests and conductor evals.

### Changed
- **Typed ledger is the recall authority.** Superseded ledger entries are
  excluded from recall by default, so active decisions no longer compete with
  retired ones.
- **Graph and manifest checks are release gates.** Generated graph docs include
  the new conductor, and `validate_library.py` now checks the machine-readable
  manifest.

## v2.4.88

The execution-integrity release. Framework upgrades, host compilation, Git gates, credentials, and evaluation runs now fail closed at their trust boundaries.

### Changed
- **Upgrades are transactional.** The updater previews by default, tracks owned files, stages same-volume replacements, records a durable journal, validates the result, and supports recovery or rollback without replacing project-owned files.
- **Credentials stay bound to their provider.** Model execution requires an explicit provider and does not send a provider key to a foreign default endpoint.
- **Git gates inspect committed intent.** Secret checks read staged blobs, support common text encodings and formats, and stop when Git cannot provide trustworthy input.
- **Compilation has one canonical output.** Portable skills have one writer while host adapters own only their command and bridge surfaces. Stale generated files are removed through explicit ownership markers.
- **Scored evaluations fail closed.** Fixture paths are contained, answer and judge identities must differ, protected holdouts are required, arm order alternates, and malformed or failed model output cannot pass.

### Added
- **Tamper-evident evaluation oracle.** A normalized SHA-256 manifest protects 308 eval cases, tests, runners, and orchestration fixtures from silent mutation.
- **Updater and compiler diagnostics.** Machine-readable doctor output reports pending recovery, conflicts, planned writes, and stale generated surfaces.
- **Adversarial regression coverage.** Tests cover interrupted upgrades, unsafe adoption, dirty sources, staged secrets, path escapes, provider routing, stale host output, and benchmark contamination.

## v2.4.87

The benchmark-integrity release. QA, context engineering, and skill-authoring now make comparative claims harder to fool.

### Changed
- **Eval and benchmark claims now need clean comparisons.** QA now requires isolated arms, fixed inputs, recorded runtime details, one measurement source, and explicit limits before publishing comparative LLM or agent results.
- **Context compression keeps a recovery path.** AI engineering now treats summaries and compressed context as navigation aids. Decisions must trace back to the original source.
- **Simplicity has a safety floor.** Core coding guidance now forbids shrinking a diff by cutting validation, authorization, security checks, accessibility, observability, or plausible error handling.

### Added
- **Benchmark-integrity eval coverage.** QA now has a regression case for contaminated baselines, mixed meters, and shorter-output claims without safety checks.
- **Public maintenance foundation.** GitHub now runs the deterministic Forge gate for every pull request and `main` update, routes questions, bug reports, and proposals to clear support paths, checks action updates, and provides private security reporting guidance.
- **Repeatable releases.** A maintainer guide defines Semantic Versioning from `v2.4.87` forward. A manual GitHub workflow validates increasing tags, extracts the matching changelog section, reruns the release gate, and publishes the tested commit.

## v2.4.86

The command-map accuracy release. Public docs now describe the v2.4.85 decision-contract behavior in the same terms the skills use.

### Changed
- **AGENTS command map.** `/goal`, `/grill`, `/plan`, and `/second-opinion` now mention goal contracts, targeted risk passes, and decision-artifact review where relevant.
- **README quickstart and catalog.** `/grill` now says it can stress-test a plan or goal contract before code.

## v2.4.85

The decision-contract release. Goal work now separates outcomes from requested tactics before execution, grill gains a targeted risk pass instead of simulated councils, and second opinion can review concrete decision artifacts without pretending to be an oracle.

### Added
- **Goal contracts.** `/goal` now confirms outcome, requested tactics, hard constraints, non-goals, risks, acceptance checks, and deferred metrics before the bounded loop starts.
- **Targeted risk pass.** `/grill` now applies narrow high-risk checks for one-way doors, security, privacy, money, legal, migration, data-loss, broad blast-radius, and missing-fact cases.
- **Decision-mode second opinion.** `.forge/second_opinion.py` and `/second-opinion` now support `--mode decision` for confirmed plans, ADRs, adoption verdicts, and goal contracts.
- **Independent review policy.** Shared resolver clarifies when to use primary work, one independent reviewer, or human/domain authority.

### Changed
- **No fake council consensus.** The framework now rejects role-played panels as independent judgment and routes true independence through configured review.
- **Second-opinion dispatch is fail-closed.** Missing reviewer config, same reviewer identity, empty output, failed command, secrets, or oversized input cannot satisfy the gate.
- **Goal loop state persists contracts.** `loop_state.py start` can store an approved contract and plan hash for resume and status.

## v2.4.84

The marketing ownership release. Organic distribution, lifecycle email, paid media, copy, analytics, studio assets, and growth strategy now have clearer boundaries and regression coverage.

### Added
- **`marketing/content-distribution`.** New organic distribution skill for unpaid feed, community distribution, repurposing, surface adaptation, and video packaging.
- **Shared marketing ownership resolver.** Growth, copywriter, lifecycle, paid acquisition, analytics, and studio now use the same owner map before drafting.
- **Content and asset references.** Added organic distribution, video packaging, content learning loop, and marketing asset brief references.
- **Boundary evals.** Added regression cases for organic routing, lifecycle newsletter ownership, content learning signals, studio asset rights, growth routing, copy routing, and outbound privacy.
- **Fingerprint scan.** Added a deterministic scan for source markers and optional private-corpus phrase overlap.

### Changed
- **Eval runner baseline mode.** Evals can now compare a candidate skill against the existing relevant skill stack through `baseline_skills`.
- **Copywriter scope.** Social copy now depends on a channel brief and no longer owns the content calendar or measurement verdict.
- **Outbound safety.** Outbound sequences now reject fake reply framing, invasive personalization, risky link use, and auto-send without approval.
- **Doc drift domain counting.** The release gate now counts domains from real `SKILL.md` files, so empty local folders cannot distort the check.

## v2.4.83

The source-resolution release. `/update-resonance` no longer depends on a target application repo knowing the framework upstream URL.

### Changed
- **Source resolution is explicit.** The updater now resolves the framework source from an explicit user source, trusted local checkout, package metadata, or the official public Resonance repository.
- **App remotes are not framework remotes.** The updater now forbids inferring Resonance from the target application's `origin` remote.
- **No-upstream projects are covered.** Projects that only have compiled `.agents/` and no `.forge/` can still resolve the official framework source safely.

### Added
- **Regression coverage for missing upstream metadata.** A new eval covers targets with `.agents`, no `.forge`, and no recorded Resonance upstream URL.
## v2.4.82

The safe upgrade release. `/update-resonance` now treats framework upgrades as migrations with preflight, ownership boundaries, backups, staged application, validation, and rollback, instead of a broad file transplant.

### Changed
- **Upgrade preflight is mandatory.** The maintainer now classifies dirty paths by ownership, prints a plan before edits, and blocks unresolved conflicts in touched framework paths.
- **Project-owned files are protected.** Project memory, application code, project docs, and customized `AGENTS.md` or host bridges are preserved unless a diff proves they are generated framework files.
- **Generated trees are replaced only through a safe path.** The protocol now requires backup, staging, inside-project path checks, validation, and rollback instructions before replacing generated framework directories.
- **Legacy memory migration is explicit.** `learnings.jsonl` can be moved into loaded memory only after approval and verification that no lesson was lost.

### Added
- **Upgrade regression evals.** New evals cover unrelated dirty application files, managed-path conflicts, and project-specific `AGENTS.md` preservation.
## v2.4.81

The security evidence release. Security review now separates candidate discovery from confirmed findings, ranks severity apart from confidence, and requires every scoped target to end with an explicit outcome.

### Added
- **Agentic vulnerability review.** A new security reference defines surface inventory, candidate queues, bounded investigation, revalidation, headless planning, and evidence gates for model-assisted security audits.
- **Security eval coverage.** Added cases for safe parameterized sinks and route-name-only candidates, so the skill does not turn weak scanner signals into blockers.

### Changed
- **Automated scanning is now an evidence system.** The scanning protocol now names scope, scan layers, candidate lifecycle, CI trust boundaries, stop conditions, and false-positive controls.
- **Static analysis gets rule contracts.** Rules now need scope, sources, sinks, sanitizers, fixtures, confidence, and lifecycle behavior, with a depth ladder from token checks through interprocedural summaries.
- **Audit reports gain lifecycle states.** Shared taxonomy and reviewer reports now distinguish clean, candidate, finding, rejected, fixed, skipped, and incomplete.
- **Security references are stricter.** The checklist, anti-pattern registry, and sharp-edge protocol now require proof paths and avoid treating risky API usage as automatic vulnerability evidence.

## v2.4.8

The compound-engineering release. A blind six-cluster integrator pass over Every's compound-engineering plugin (32 skills, most rejected as tool-bound or already covered) yields eight surgical elevations and one new skill, plus the sales, audit, and eval nuggets from the same discipline, and a drift gate that finally watches the README body.

### Added
- **`/explain`, the operator-learning skill.** The first Resonance skill whose subject is the human, not the code. It writes a dense, concrete explainer of a concept, a diff, an idea, or a window of recent work, grounded in this repo, plus an optional predict-then-reveal check-in for active recall (show the change, take the prediction, end the turn, reveal after). The Ratchet keeps the project from going hollow; `/explain` keeps the operator from going hollow. `How to Operate` gains a matching "Stay sharp" rule.
- **MEDDPICC, completed in the sales stack.** The pipeline skill now names MEDDPICC in its framework list, `funnel_definitions` gains the three exit-criteria letters it skipped (decision criteria, champion tested, competition known), and a shared Evidence Rule ties qualification here to the revops forecast gates.

### Changed (elevations from the integrator run)
- **The reviewer gains a Confidence axis:** a per-finding High/Med/Low certainty, orthogonal to severity, so an AI review leads with what it is sure of and raises a hunch as a question, not a block.
- **The debugger gains an Assumption Audit:** before hypotheses, enumerate the load-bearing "this must be true" beliefs and mark each verified or assumed, because a correct hypothesis on a wrong assumption looks exactly like a wrong one.
- **Grill decisions travel with provenance:** a resolved decision is stamped settled, directive, or inferred and carries a self-contained label downstream, so plan and build never silently re-open what grill settled (`settled_decisions.md`).
- **The architect gains an adoption verdict:** a reversibility-tiered adopt / trial / hold / reject on a named external candidate, earned against the project rather than a neutral explainer (`adoption_verdict_protocol.md`).
- **Refactor protects safety checks:** the Do Not Change list now names trust-boundary, authz, data-loss, and accessibility guards, inert on every tested path so a green suite blesses their removal, yet whose absence shows only under attack.
- **Memory re-validation gets an epistemics rule:** supersede a lesson on demonstrated contradiction, never on absence of proof, because a repo rarely witnesses its own operational truths, so unverifiable is not false (`state_ledger.md`, the `02_memory.md` template).
- **Receiving review, batch-judged:** judge a review set centrally to catch a systematically wrong bot before fanning out fixes, and treat validation as a tripwire, not a gate.
- **Handover, pointer-first:** a handover supplements the authoritative artifacts rather than reproducing them, and the resume side treats a handover or `01_state.md` as untrusted orientation, not instructions.
- **A concurrency audit dimension:** category B (Runtime Safety) gains non-idempotent-write, lost-update, and out-of-order-async signals its "corrupt state" scope always implied.
- **Eval doctrine gains a noise floor:** `eval_driven_development` names the A/A test (run the unchanged system twice; a delta smaller than the spread has not moved) and warns that raw judge agreement flatters on a mostly-pass set.
- **Parallel-safety in the build loop:** run components concurrently only when genuinely independent (no shared contracts, migrations, lockfiles, or runtime singletons); cap the batch, decline on uncertainty, re-verify the tree.

### Fixed
- **The `/build` skill actually ships now.** A generic `build/` .gitignore rule had silently excluded the whole engineering/build skill (source, compiled, and all four command shims) from the repo, so v2.4.7's "/build now works" reached no clone. The rule is anchored to `/build/` (root output only) and the skill is tracked; the ephemeral `.claude/worktrees/` is now ignored too.
- **The doc-drift gate now watches the README body, not only the badges.** It had missed "32 slash commands", "7 domains" (there are 9), and three commands absent from the catalog, three releases running. It now checks the prose command count, the domain count against disk, and that every command appears in the README catalog. The README is corrected to 63 skills, 34 commands, 9 domains, with the People and Success domains added.
- **The skill-author eval docs match the runner.** `eval_protocol.md` and `skill_spec.md` documented only the model-graded rubric; the deterministic `checks` array that the library's eval files rely on, and the dash-encoding rule, lived only in `docs/EVALS.md` and private memory. Both now carry the contract they claim to be authoritative for.

The library is now 63 skills and 34 commands.

## v2.4.71

The copywriter learns to catch AI's rhetorical tells, not just its words, and gains a dedicated grill pass.

### Added
- **`rhetorical_tells.md`, the shape layer of anti-slop.** The word lists catch "delve" and "leverage". This catches the sentence architecture that still marks machine prose: the "not X, but Y" pivot, the drumroll rule of three, negative anaphora, the dramatic landing sentence, nominalization, stacked nouns. The rule throughout is dose, not ban: a figure once is craft, the same figure every paragraph is the machine, so the reference rations the figures rather than forbidding them (banning contrast or triads outright would gut the copy).
- **A Grill pass in the copywriter.** The Operational Sequence is now Draft, Edit, Humanize, Grill, Polish. The grill reads the near-final draft as an artifact and hunts the rhetorical tells, the Kill List, the rubric, and the facts, line by line, with a proposed fix for every finding.

### Changed
- **Deterministic catches for the mechanical tells.** The copy-mode guard and a new eval flag the shapes regex catches cleanly: "not only... but also", "isn't just/only/about", the filler intensifiers truly and genuinely, hedge stacks, and a few throat-clearing openers. The judgment-heavy figures stay with the grill pass. `taboo_phrases` gained the word-level filler and hedge items.

## v2.4.7

The operating-loop and agentic-business release. Project memory becomes a typed ledger the agents query, cite, and supersede; the autonomous loop gains real bounds and a resume; the skill graph becomes machine-checked; and the framework grows the spine to run a whole company, a founder operating system plus the people, retention, and revenue-operations functions a founder needs.

### Added
- **The typed state ledger (`.resonance/ledger/`).** The project brain gains a typed layer the agents query, cite, and supersede: decisions, lessons, metrics, customers, and experiments as `dec-`/`les-`/`met-`/`cus-`/`exp-` entries, one per `##` heading, plain `key: value` blocks, no database. Directed edges (`supersedes`, `evidences`, `caused`) traverse forward by reading a field and backward with a single grep. A per-file `schema: resonance-ledger/N` marker carries the version, and its absence is the grace rule: a project with no `ledger/` directory skips every typed check and never breaks on upgrade. `recall.py` reads the ledger with the rest of the brain, and `validate_library.py` enforces the shape (required fields per type, id grammar, unique ids, no dangling edges, supersede reciprocity). When a ledger exists it is the system of record for its five types, so decisions and lessons stop being duplicated as prose. Documented in the `ops/core` `state_ledger.md` reference.
- **The outer loop closes.** A new `DONE_PENDING_OUTCOME` completion state for work whose real proof is a metric that lands later (a reply rate, a renewal): it records a `met-` or `exp-` entry with a `due:` date, and `py .forge/measurement_due.py` surfaces due outcomes at session start (pull, not push, silent when nothing is due). `py .forge/field_report.py` turns a field report into a lesson entry and a stub eval case, so a real-world miss compounds into a permanent regression instead of being solved once.
- **A harder autonomous loop (`/goal`).** The bound enforcer gains a duplicate-failure detector (pass `--sig` with a fingerprint of the failing observation; the same failure repeating is caught as a loop, not retried) and a `resume` command that reads the persisted state so a crashed or handed-over run continues at the last verified slice. The loop doctrine now states the three clocks (inner deterministic checks, middle evals and second opinion, outer field outcome to measured lift), the ladder that says do not spin an autonomous loop when a single skill or prompt chain suffices, and the rule that every iteration must inject new information or it is wasted.
- **The skill-dependency graph.** Orchestration skills declare an `invokes:` list in frontmatter; `validate_library.py` checks every edge resolves to a real skill and that every command resolves to a skill that exists, and `py .forge/skill_graph.py` renders `docs/SKILL_GRAPH.md` (a Mermaid diagram plus an edge table) with a freshness test.
- **The agentic-business spine.** A new `ops/founder-os` skill: the founder's operating rhythm, OKR cascade, weekly business review, a company KPI tree, a decision log written to the ledger, an agent-delegation map (which skill owns which business function), authority budgets (what an agent may spend, send, or commit unasked), and an operating cadence spec with a host-scheduler example (a spec, not a daemon). Plus three functions a whole-company stack needs: `people/hiring` (scorecards, structured interview loops, evidence-based debriefs, comp bands, onboarding), `success/customer-success` (time-to-value, leading-indicator health, the renewal and NRR motion, expansion, churn saves, support deflection), and `sales/revops` (funnel definitions, coverage and capacity math, quota and comp design, the forecast call, deal desk).
- **A distributed-systems mental-model pack.** A new `distributed_systems.md` reference (CAP and consistency, idempotency and the exactly-once illusion, the outbox pattern and sagas, back-pressure and Little's Law, error budgets as a gate, one-way versus two-way doors, FMEA), wired into the backend and database skills; the backend skill now self-verifies in-loop against the execution surface, not only by delegating to `/test`.
- **A tooling test seam (`.forge/tests/`).** The Forge tooling now ships stdlib regression tests, run by `py .forge/tests/run.py` and gated in the pre-push ship-gate. The library is now 62 skills.

### Fixed
- **The `/build` command now works.** `/build`, the TDD execution loop that `/goal` orchestrates, routed to a skill that had never been authored. `engineering/build` now exists as a full procedure skill (red-green-refactor, grounded verification, the two-miss route to `/debug`, no commit without evidence). The new command-target check keeps a command from pointing at a skill that does not exist.
- **The skill validator reports instead of crashing.** A skill with fewer than three eval cases now fails validation with a clear message rather than raising, so one malformed skill no longer takes down the whole validation run.
- **The frontmatter parser reads list-valued fields** (for example `invokes:`), instead of raising on the first list item.
- **Retro metrics are exact.** The `retro` skill's Shipping Streak, Focus Score, Complexity Delta, and Test Ratio each have one git-computable definition (`retro_metrics.md`), so two people get the same number from the same history.

### Changed
- **The operating standard learned the ledger.** `AGENTS.md`, the Ratchet, and `ops/core` route durable decisions and lessons to the typed ledger when one exists, and `ops/core` runs the due-measurement pull at session start.

## v2.4.6

The cross-tool memory release. The operating standard and project memory now load at the start of every session on every supported tool, plus a focused set of design-craft upgrades.

### Fixed
- **The operating standard reaches the model on Claude Code.** Claude Code loads `CLAUDE.md`, not `AGENTS.md`, so the Forge now emits a per-host **context bridge** that loads `AGENTS.md` and the `.resonance/` memory the way each tool expects: a root `CLAUDE.md` (importing `@AGENTS.md`) for Claude Code, an always-applied `.cursor/rules/resonance.mdc` for Cursor, and native `AGENTS.md` reading for Codex, opencode, and Antigravity. It will not overwrite a hand-authored bridge.

### Changed
- **Project memory that loads.** Durable lessons live in `.resonance/02_memory.md`, a curated index loaded every session, plus `memory/` leaf files. `AGENTS.md` gained a Project Memory section so every tool loads the memory at session start, and `recall.py` reads it alongside legacy `learnings.jsonl`.
- **Design craft upgrades.** Gesture physics in `motion_and_feel.md` (velocity handoff, momentum projection, interruption from the live value, and a "should this animate at all?" gate) and ease-out on exits. A field-tested AI-tell catalog in `ai_design_slop.md` (fake product UI, hero version labels, status theater, weather strips). A serif-reflex ban in `typographic_system.md`. Button and empty-state tactics, and object and emotional-job disciplines in `ops/product`.
- **A scope-fidelity rule in the operating standard.** Verify and Completion forbid placeholder stubs and silent truncation and require the delivered count to match the request, reconciled with Simplicity, which governs the how, never the how-much.

### Added
- **`design/designer` conceptual-model reference (OOUX).** The user-facing object, vocabulary, and state model between `/product` and `/design`: object inventory, lifecycle states, verb precision, one name per concept. Wired into the designer sequence and the PRD template.

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
