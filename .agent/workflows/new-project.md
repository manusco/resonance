---
description: Start a new project or feature using the 'Working Backwards' methodology.
---

# Bootstrap Protocol (`/new-project`)

> **Role**: The Founder (`resonance-product` / `resonance-architect`)
> **JTBD**: Create a "Zero to One" Foundation.
> **Input**: A "Big Idea" or Domain.
> **Output**: A Git Infrastructure with CI/CD and "Hello World".

## 1. Prerequisites
*   [ ] Folder is empty (or new folder requested).
*   [ ] `node`, `git`, `npm` are installed.

## 2. Context (The Vision)
<thinking>
I am the Architect of Genesis.
I must set defaults that prevent Technical Debt later.
I must start with the "Why" (PRD) before the "How" (Code).
I will not just copy-paste. I will tailor the stack to the need.
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Discovery (Working Backwards)
*   **Action**: Create `docs/prd/00_launch.md`.
    *   **Headline**: 6 words max.
    *   **Problem/Solution**: The Value.
    *   **MVP Scope**: The "Walking Skeleton".

### Step 2: Methodology Selection
Choose the Stack based on the Problem.
*   **Web App**: Next.js + Tailwind.
*   **API**: NestJS or Hono.
*   **Tool**: TypeScript CLI.
*   **Action**: Write `docs/adr/001_initial_stack.md`.

### Step 3: Scaffolding (The Build)
Execute the "Gold Standard" Init.
1.  **Init**: `npm init -y` / framework init.
2.  **Git**: `git init`, `.gitignore`.
3.  **Lint**: Install `eslint`, `prettier` (Strict).
4.  **Test**: Install `vitest`.
5.  **CI**: Create `.github/workflows/ci.yml`.

### Step 4: The Spark
Deploy the Walking Skeleton.
*   **Action**: Create `src/index.ts` (or equivalent).
*   **Test**: Run `npm test`. It must pass.

## 4. Recovery
*   **Init Failure**: If framework init fails (network), retry once. If fail, fall back to plain TS.
*   **Permissions**: If git init fails, warn user but proceed with files.

## 5. Governance (Definition of Done)
*   **Artifacts**: `package.json`, `.gitignore`, `docs/prd/`.
*   **Verification**: `npm test` passes.
*   **State Update**: Initialize `state.md`.
