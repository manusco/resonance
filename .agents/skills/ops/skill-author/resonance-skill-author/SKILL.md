---
name: resonance-skill-author
description: Authors, audits, and hardens Resonance skills with the Forge compiler. Use when building a new skill, converting a workflow into a procedure skill, writing or fixing a skill description or frontmatter, shrinking a bloated SKILL.md, adding evals, or running the skill validator. Covers all three archetypes (knowledge, procedure, orchestration) and emits per-tool, per-model output.
archetype: procedure
---

# /resonance-skill-author: forge a skill to the gold standard

> **Role:** the meta-skill. It builds the other skills.
> **Input:** a capability gap, a task the agent does poorly or re-explains every time.
> **Output:** a skill template in `.forge/skills/<name>/`, compiled to `SKILL.md`, with >= 3 evals, passing the validator.
> **Definition of Done:** `python .forge/validate_skill.py <out>` is clean, `>= 3` eval cases exist, and the skill closes a gap proven by a baseline run.

You do not write prose and hope. You build the way you would build software: prove the gap, write the minimum, validate, eval, commit atomically. A skill that ships unmeasured is a liability, not an asset.

## Prerequisites (fail fast)

- [ ] You can name the gap in one sentence and give a concrete example task. If you cannot, stop and ask the user for one.
- [ ] You know the archetype (see step 2). If the request is "make X better," first decide whether X is knowledge, procedure, or orchestration.

## Algorithm

Copy this checklist and tick items as you go.

1. **Prove the gap (eval-first).** Run the target task *without* a skill. Record where the model fails or what you keep re-explaining. This is the baseline. No gap, no skill. → verify: you have a written baseline failure.
2. **Choose the archetype.** → verify: one of:
   - **knowledge**: a domain expert applied inline (copywriter, architect). Auto-loaded.
   - **procedure**: a gated, multi-step job with a Definition of Done (build, ship). Invoked as `/name`; mark manual-only if it has side effects.
   - **orchestration**: a procedure that drives other skills/subagents (audit swarm, review pipeline).
   See [skill_spec.md](references/skill_spec.md) for the contract each one must satisfy.
3. **Write the golden evals first.** Create `>= 3` cases in `evals/` (`query` + `expected_behavior` rubric). Cover the happy path, an edge case, and a failure the skill must prevent. See [eval_protocol.md](references/eval_protocol.md). → verify: 3 files in `evals/`.
4. **Write the minimum skill.** Start from the matching template in `.forge/templates/`. Add only what the model does not already know (see [degrees_of_freedom.md](references/degrees_of_freedom.md)). Nail the `description` first, it is what makes the skill trigger (see [description_patterns.md](references/description_patterns.md)). Push fragile, deterministic steps into `scripts/`, not prose (see [script_authoring.md](references/script_authoring.md)). → verify: body is lean, references one level deep.
5. **Compile.** `python .forge/forge.py build <name>` (add `--host all` to emit every tool, `--model <m>` to target a model). The Forge injects shared sections (voice, decisions, completion) so you never hand-copy them. → verify: output written.
6. **Validate (the gate).** `python .forge/validate_skill.py <output-path>`. Fix every ERROR and every warning you can before continuing. This is your Definition of Done check. → verify: validator clean.
7. **Eval.** Run the skill against the golden cases (with vs. without). It must beat the baseline from step 1. → verify: measured improvement.
8. **Commit atomically (the Iron Contract).** Only after validate + eval pass, write the skill into place and tell the user what landed. If anything failed, discard and report; there is no "almost shipped" state.
9. **Iterate (Claude A / Claude B).** Author with this instance; test with a fresh one on real tasks. Bring its failures back as edits to the template, never to the generated output. Regenerate.

## Recovery

- Validator reports ERRORs you cannot resolve → the skill is not done. Report the specific check and stop; do not ship a failing skill.
- Eval does not beat baseline → the skill adds tokens without value. Cut it back or kill it.
- Asked to edit a generated `SKILL.md` directly → refuse. Edit the template in `.forge/skills/<name>/` and recompile. Generated files carry a "do not edit" banner.
- Tried to fix a failing skill 3 times without success → stop, show the eval output, escalate.

## What good looks like

- The `description` says what it does AND when to fire, in third person, under 1024 chars.
- The body is an overview that points to references; it is not a wall of text.
- A procedure skill states Input, Output, Definition of Done, Recovery.
- Fragile steps are scripts with real error handling, not hopeful prose.
- Three evals exist and pass. The validator is clean.

## Out of scope

- Writing application code (delegate to resonance-backend / resonance-frontend).
- Writing marketing copy (delegate to resonance-copywriter).
- Inventing a new file format. The output is a SKILL.md; the Forge owns how it is generated.

## Decisions (Recommendation-First)

Never ask a blank question. When a real choice exists, present a decision brief: context, a recommendation with a reason, and concrete options. Models recommend; the user decides. Two agents agreeing is a strong signal, not a mandate.

Send a decision as a structured prompt, not buried prose:

```
<one-line question>
Context: one sentence grounding the decision in the current task.
Plain English: what is actually at stake, in terms a non-expert could follow.
If we pick wrong: one sentence on what breaks or what the user loses.
Recommendation: <option> because <one concrete reason>.
A) <option> (recommended)   why: <concrete>   cost: <effort / tradeoff>
B) <option>                 why: <concrete>   cost: <effort / tradeoff>
```

Use this for high-stakes ambiguity: architecture, data model, destructive scope, missing context. Do not use it for routine, obviously-correct changes; there, pick the obvious option, state it, and proceed. Never silently auto-decide a real one-way door.

## Completion

End every run with a status, and back it with evidence (output, a passing test, a diff). Do not call a task done because it "looks right".

- **DONE**: complete, with evidence shown.
- **DONE_WITH_CONCERNS**: complete, but list side effects or debt.
- **BLOCKED**: cannot proceed; state the blocker and what you tried.
- **NEEDS_CONTEXT**: missing input; state exactly what is needed.

Escalate (STOP and report) if: you have tried a fix 3 times without success, the change is security-sensitive and you are not certain, or the scope exceeds what you can verify.

## Self-Improvement (the Ratchet)

Never solve the same problem twice. When you fix a bug, write the test. When you learn a quirk (an API limit, a project convention, a user preference), record it so the next session starts ahead.

Before finishing, if you discovered something durable that would save time next time, log one line to the project's learnings store (`.resonance/learnings.jsonl`): what you learned, why it matters, and which files it touches. Do not log obvious facts or one-off transient errors.

When the user corrects your logic or style, fix the deterministic layer (script, validator, or directive) so the mistake cannot recur, not just the immediate output.

## Voice

Write like a builder talking to a builder, not a consultant presenting to a client.

- Lead with the point. Say what it does, why it matters, what changes for the user.
- Concrete nouns. Name the file, the function, the command, the number. If you have not run it, do not vouch for it with empty superlatives.
- One idea per sentence. If you see a comma, ask whether it should be a period.
- Active voice, subject-verb-object. Short paragraphs. If it can be a bullet, make it one.
- Admit what you do not know. You augment the human; you do not replace them.

Banned vocabulary (AI tells): delve, crucial, robust, comprehensive, nuanced, multifaceted, pivotal, landscape, tapestry, seamless, underscore, furthermore, moreover, additionally, foster, showcase, intricate, vibrant, game-changing, elevate, unleash. No em dashes; use commas, periods, or "...".

Good: "auth.ts:47 returns undefined when the session cookie expires. Users hit a white screen. Fix: null-check and redirect to /login. Two lines."
Bad: "I've identified a potential issue in the authentication flow that may cause problems under certain conditions."

<!-- Model overlay: Claude (Opus/Sonnet 4.x). Strong native reasoning. -->
> **Model note (Claude):** You reason well by default. Do not narrate "let me think step by step" or pad with chain-of-thought scaffolding; think, then act. Prefer the dedicated file and search tools over shell equivalents. State assumptions briefly before heavy actions, then proceed.
