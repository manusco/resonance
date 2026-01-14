---
description: Ensure code meets standards before merging (CI/CD, Linting, Security).
---

# Workflow: Review PR ("The Gatekeeper")

**Trigger**: "Review this", "Check my work".
**Context**: Validating a change before integration.

## 1. Automaton Check (The Robot)
*Activate Skill*: `resonance-devops`

- [ ] **Lint**: Run linter. Zero warnings allowed.
- [ ] **Test**: Run full test suite.
- [ ] **Build**: Does it build for production?

## 2. Security Scan (The Guard)
*Activate Skill*: `resonance-security`

- [ ] **Dependencies**: Check `npm audit`.
- [ ] **Secrets**: Grep for keys/tokens.
- [ ] **Injection**: Check all new inputs.

## 3. Semantic Review (The Human)
*Activate Skill*: `resonance-reviewer`

- [ ] **Readability**: Can a junior understand this?
- [ ] **Architecture**: Does it violate boundaries? (e.g., DB call in View).
- [ ] **Performance**: Any N+1 queries?

## 4. Decision
- [ ] **Block**: If Security/Correctness fail.
- [ ] **Nit**: Styling/Naming suggestions.
- [ ] **Approve**: If it meets the Elite Standard.
