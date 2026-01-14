---
description: Start a new project or feature using the 'Working Backwards' methodology.
---

# Workflow: Initialize Project ("The Big Bang")

**Trigger**: "Start a new project", "Scaffold app".
**Context**: Creating something from nothing.

## 1. Definition (The Vision)
*Activate Skill*: `resonance-product`

- [ ] **Press Release**: Write `docs/prd/00_launch.md`.
- [ ] **Scope**: Define the "Walking Skeleton" (The smallest deployable unit).

## 2. Architecture (The Blueprint)
*Activate Skill*: `resonance-architect`

- [ ] **Stack Choice**: Document in `docs/adr/001_stack.md`.
- [ ] **Folders**: Create the Clean Architecture structure (`src/core`, `src/infra`).

## 3. Scaffolding (The Foundation)
*Activate Skill*: `resonance-devops`

- [ ] **Init**: `npm init` / `git init`.
- [ ] **CI/CD**: Create `.github/workflows/ci.yml`.
- [ ] **Docker**: Create `Dockerfile`.

## 4. Walking Skeleton (The Spark)
*Activate Skill*: `resonance-backend`

- [ ] **Hello World**: Create a single API endpoint `/health`.
- [ ] **Deploy**: Push to prod. Verify it returns 200 OK.
- [ ] **Done**: Do not proceed until the pipeline is green.
