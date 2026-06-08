# Handover Document Structure

## Contents
- Full document template
- Section guidance
- Append-mode format
- Quality bar

---

## Full Document Template (new file)

```markdown
# Handover — YYYY-MM-DD

## Status Snapshot
[Current phase from 01_state.md. 2-3 sentences: where the project stands, the current
momentum, and any active blocker. If the project is blocked, say so explicitly.]

## What Was Done
[Bullet list. One item per concrete output: file changed, feature shipped, bug fixed,
decision reached. Pull from session context and git log. No vague entries like "worked on
auth" — name the file, the function, the endpoint.]

- Implemented `auth.service.ts:login()` — JWT issue on successful email/password login
- Fixed rate-limit bug in `api/users.ts` (#143)
- Decided on Supabase over Auth0 (see Decisions Made)

## Decisions Made

| Decision | Rationale | Alternatives Considered |
|---|---|---|
| [What was decided] | [Why this choice, one sentence] | [What was rejected and why] |

If no architectural decisions were made: write `No architectural decisions this session.`

## Current State
[What is in flight right now. Unresolved threads. Key constraints the next person must
know before touching the code. Mirror .resonance/01_state.md but translate for a human:
drop agent-state metadata, keep the human-relevant context.]

- `password-reset` branch is open, 3 of 6 tasks done
- Supabase local instance must be running: `supabase start`
- Env var `SUPABASE_JWT_SECRET` not yet set in staging

## Open TODOs
[Pull unchecked items from task.md. If no task.md, synthesize from session context.
Prioritize: P0 = blocking, P1 = this sprint, P2 = lower urgency.]

- [ ] **P0** — Rotate JWT secret before staging deploy
- [ ] **P1** — Fix 2 failing tests in `auth.test.ts` (lines 47, 112)
- [ ] **P1** — Implement password reset email flow
- [ ] **P2** — Add refresh token rotation

## Backlog
[Potential next steps. Not committed — just captured so they are not lost.
Roughly ordered by value. The next person can promote any of these to TODOs.]

- Add rate limiting to `/auth/login` — needed before public launch
- Migrate to edge functions for auth — reduces cold start latency
- Write E2E test for full signup flow

## Gotchas & Context
[Tribal knowledge. Things that would waste a colleague's time if they did not know.
API quirks, env setup requirements, fragile assumptions, known untracked bugs.
Be specific: name the file, the line, the gotcha.]

- `supabase start` must be run before any test; the test suite has no auto-setup
- The `users` table has a soft-delete column (`deleted_at`) — raw queries bypass it; always use the `UserRepository` wrapper
- Auth0 SDK left in `package.json` (unused) — remove before next release to reduce bundle

If nothing notable: write `None identified this session.`
```

---

## Append-Mode Format

When a handover already exists for today, append this block at the end of the file:

```markdown
---

### Session HH:MM

## What Was Done
[Delta only — what changed since the earlier session]

## Decisions Made
[New decisions only. If none: "No architectural decisions this session."]

## Current State
[Updated state — supersedes the earlier session's Current State]

## Open TODOs
[Updated list — mark completed items with ~~strikethrough~~ or remove them]

## Backlog
[Additions or reprioritizations only]

## Gotchas & Context
[New gotchas only]
```

---

## Quality Bar

A handover passes if a colleague can answer these questions from it without asking:

1. What is working and what is not?
2. What was the last significant decision and why?
3. What is the single most important thing to do next?
4. What will break if they forget something?

If any of those questions is unanswerable from the document, add the missing information.
