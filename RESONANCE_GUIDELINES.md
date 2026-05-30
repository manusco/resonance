# Builder Guidelines

How to build and maintain Resonance. This is for **us**, the builders. It is not for the end user.

Resonance is a cross-tool, cross-model operating system for AI agents. It runs on Claude Code, Codex, Cursor, Antigravity, and OpenCode, on Claude, GPT, Gemini, and open-weight models. We do not lock to one vendor. We author above the format and compile to the open `SKILL.md` / `AGENTS.md` shape that every major tool already reads.

## 1. How We Write

We respect the reader's time.

- **Prune.** If a word does not add meaning, cut it. No "very", "extremely", "really".
- **Hook.** Start in the middle. Make them curious.
- **One thought.** One idea per sentence. If you see a comma, ask whether it should be a period.
- **Active voice.** Subject, verb, object. "The agent writes the code", not "the code is written by the agent".
- **Be human.** Admit what you do not know. Speak as a peer, not a god.
- **No tells.** No em dashes. No AI vocabulary (delve, crucial, robust, comprehensive, nuanced, seamless, landscape, tapestry, leverage, elevate). Name the file, the function, the command. If you have not run it, do not vouch for it with empty superlatives.

This voice lives in one place: `.forge/resolvers/voice.md`. It is injected into every skill at compile time. Fix it once, recompile, every skill updates.

## 2. Core Philosophy

### Externalized Cognition

**If it is not in a file, it does not exist.**
Agents die. Chat history fades. The file system is the only persistent mind.

The `.resonance/` brain is the single source of truth for a project:

- **Soul** (`00_soul.md`): vision and user. Who we build for.
- **State** (`01_state.md`): the active task. What we are doing now.
- **Memory** (`02_memory.md`): the decision log. Why we chose what we chose.
- **Systems** (`04_systems.md`): the map. Schemas, contracts, logic flows.
- **Learnings** (`learnings.jsonl`): hard-won project quirks.

Code must never contradict the brain. The brain is owned by the project and is never overwritten on upgrade.

### The Ratchet (Self-Annealing)

**Never solve the same problem twice.**
Fix a bug, write the test. Learn a quirk, write it down. When something breaks or the user corrects your logic:

1. Read the error, trace, or correction.
2. Fix the **deterministic layer** (a script, a validator, a directive), not just the prompt, and prove the fix.
3. Record the learning so the next session starts ahead.
4. Iterate until the mistake rate hits zero.

A correction that only changes one output is a missed ratchet. Push the fix down so the mistake cannot recur.

### The 3-Layer Architecture

We separate concerns to make a probabilistic system reliable.

1. **Directive (intent).** Skills in `.agents/skills/`, compiled by the Forge. Natural-language goals, inputs, outputs, edge cases.
2. **Orchestration (decision).** The model. Reads directives, calls tools in order, handles errors, routes intent to execution.
3. **Execution (deterministic).** Scripts, validators, evals, MCP servers. Reliable, testable, fast.

> **Rule:** push fragility into Layer 3. A step that is 90% reliable becomes 59% over five hops. The validator, the Forge, and the eval harness are Layer 3. So is every script a skill runs. If a step is order-sensitive or destructive, it is code, not prose.

### Evolution

**Improve, do not replace.**
Resonance is mature. Do not delete working functionality. If you see a better way, integrate it; understand why the old way existed before you overwrite it. It is fine to remove what is genuinely outdated. It is not fine to burn the cathedral.

## 3. What Resonance Is (Hard Rule)

Resonance is a **Company OS**: a complete set of skills, frameworks, and mental models covering every essential function of a business. It is built for operators (founders, CEOs, CTOs, the teams around them) and for small and medium businesses that want to operate like the top 1%.

**A Resonance skill IS:**
- A mental model or thinking framework (Jobs-to-be-Done, SPIN, OKRs).
- A best practice or decision protocol (how to run a hiring process, a board meeting).
- An operational sequence (how to structure a sprint, ship a release).
- Domain expertise distilled to its essence (how a CFO thinks about cash).

**A Resonance skill is NOT:**
- A guide to one piece of software ("how to configure Slack"). Tool-specific steps belong in `references/` as cheat sheets, never in a `SKILL.md`.
- A narrow vertical play. Skills must work for most businesses.
- Anything below the 1% standard. If it reads like a blog post, reject it.

> If you are writing steps that click a button in a named app, stop. That is a reference doc. The skill is the strategy: why you would take the action, and when.

## 4. Skills Are the Only Primitive

We used to split "skills" (roles) from "workflows" (procedures) into two folders with two formats. We do not anymore. A workflow is not a separate thing. It is a kind of skill. There is one primitive and three archetypes:

- **knowledge**: a domain expert applied inline (resonance-copywriter, resonance-architect). Auto-loaded when relevant.
- **procedure**: a gated, multi-step job with a Definition of Done (build, ship). Invoked as `/name`. Marked manual-only when it has side effects.
- **orchestration**: a procedure that drives other skills or subagents (an audit swarm, a review pipeline).

Workflows hold most of the value, because a knowledge skill alone is inert until a procedure drives it. So the procedure and orchestration archetypes are first-class. What made our old workflows good, the **Input / Output / Definition of Done / Recovery** contract, is now required on every procedure skill and checked by the validator.

Each skill declares its `archetype` in frontmatter. The `description` declares what it does and when to fire; it is the only text loaded at startup and the single highest-leverage line in the file.

## 5. The Forge (How We Build Skills)

We do not hand-write skills and hope. We compile them. The Forge lives in `.forge/`.

```
skill.tmpl.md   x   host (tool)   x   overlay (model)   ->   SKILL.md
```

- **Author once.** A template with placeholders, plus `references/`, `scripts/`, `evals/`.
- **Compile per tool.** `hosts/*.json` map logical tools to each tool's real names and output paths. One config per tool, not per skill.
- **Compile per model.** `overlays/*.md` patch behavior per model family. Strong models get terse prompts; open-weight models get explicit guardrails and lower freedom.
- **Share once.** `resolvers/*.md` inject voice, decisions, completion, the locks, and the Ratchet into every skill. No copy-paste.

Generated `SKILL.md` files are build output. Do not edit them. Edit the template and recompile.

```bash
py .forge/forge.py build <name>            # compile
py .forge/forge.py build <name> --host all # every tool
py .forge/forge.py build --all --dry-run   # CI freshness: exit 1 on drift
```

## 6. The Eval-First Mandate

**Build evals before you build the skill.** This is the rule the craft turns on.

1. **Prove the gap.** Run the task with no skill. Write down the exact failure. No gap, no skill.
2. **Write `>= 3` golden cases** in `evals/` (`query` + `expected_behavior` rubric). Cover the happy path, an edge case, and a failure the skill must prevent.
3. **Baseline, then write the minimum** skill that beats it.
4. **Validate.** `py .forge/validate_skill.py <path>` must be clean. This is the Definition of Done check.
5. **Iterate** with a fresh agent on real tasks. Bring failures back to the template, recompile.

A skill that ships unmeasured is a liability, not an asset. The validator (Layer 3, free, deterministic) and the golden cases are how we know a skill is real.

## 7. The Iron Contract

A broken skill on disk makes agents reach for the wrong tool. So we write through a gate, never directly:

> stage the work, run the validator and the evals, commit only on green and on explicit approval. On any failure, discard and report. There is no "almost shipped" state.

## 8. Engineering Standards

- **No commit without evidence.** Verify every change with output, a passing test, or a diff.
- **Docs over chat.** Complex logic belongs in `docs/` and the brain, not in a chat that fades.
- **No black boxes.** Explain why. Justify every magic constant.
- **Aesthetics.** Generated UI must be beautiful. No thoughtless defaults.
- **User sovereignty.** Models recommend; the user decides. Never run a destructive or architectural change without presenting the recommendation and waiting.
