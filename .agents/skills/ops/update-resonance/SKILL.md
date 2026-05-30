---
name: resonance-ops-update-resonance
description: The Maintainer. Upgrades the Resonance framework kernel without breaking the user's project context. Use when migrating to a new version of Resonance.
archetype: procedure
---

# /resonance-ops-update-resonance: upgrade the framework, preserve the context

> **Role:** the Maintainer.
> **Invoked as:** `/update-resonance` (to upgrade the Resonance OS).
> **Input:** Upstream Changes.
> **Output:** Upgraded `.forge` and `.agents` folders.
> **Definition of Done:** Resonance framework files are updated while `00_soul.md` and user memory remain intact. `/system-health` passes after the upgrade.

You are upgrading the OS. You must not overwrite user customizations. You must back up before you touch anything.

## Prerequisites (fail fast)

- [ ] Network access allowed.
- [ ] Git Status clean.

## Algorithm (Execution)

Copy this checklist and tick items as you go.

1. **Verify ownership boundary**: Confirm `.resonance/` will not be touched. It holds the user's soul, state, and memory. The upgrade only touches `.agents/` and `AGENTS.md`. → verify: `.resonance/` is not in scope.
2. **Clone latest**: Fetch the new version to a temp location outside the project root. → verify: temp directory exists and is not inside the project.
3. **Delete `.agents/`**: Remove the entire old skill library. Do not overwrite — delete. Overwriting leaves ghost files from renamed or removed skills, which the agent will silently read and contradict new skills. → verify: `.agents/` no longer exists.
4. **Copy new `.agents/`**: Copy the compiled skill library from the temp location. → verify: `.agents/skills/` contains the new domain structure.
5. **Copy `AGENTS.md`** and the `resonance.sh` / `resonance.ps1` scripts. → verify: files exist.
6. **Verify the upgrade**: Run `/system-health`. It must report the correct skill count. Flag if score < 80. → verify: health check passes.
7. **Clean up**: Remove the temp directory.


## Recovery

- Something went wrong after deleting `.agents/` → clone the repo and copy `.agents/` back in. This is faster and cleaner than restoring a backup of an old version.
- `/system-health` fails (score < 50) → do not use the system. Re-run steps 3–5 from a fresh clone. The issue is almost always a partial copy.
- Conflict in `00_soul.md` → this should not happen because `.resonance/` is never touched. If it does happen, the user has accidentally run the wrong command. Stop and confirm scope before proceeding.


## Out of Scope

- Modifying the application code (this is strictly a framework upgrade tool).

## Cognitive Frameworks

### The Transplant
Upgrading a framework while preserving the user's project memory is like a transplant. You must preserve the Soul (`00_soul.md`) and the Memory (`01_state.md`, `02_memory.md`).

## Reference Library

- **[Completion Attestation](../core/references/completion_attestation.md)**: Required sign-off format.

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
