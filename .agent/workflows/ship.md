---
description: Deploy the project to production using the 'ShipIt' protocol.
---

# Release Protocol (`/ship`)

> **Role**: The Logistics Officer (`resonance-devops`)
> **JTBD**: Safe Transport of Code to User.
> **Input**: Merged `main` branch.
> **Output**: Deployed artifact + Tagged Release.

## 1. Prerequisites
*   [ ] Branch is `main`.
*   [ ] Local tree is clean.
*   [ ] CI is Green.

## 2. Context (The Checkpoint)
<thinking>
Shipping is irreversible.
I must verify the artifact *before* I tag it.
I am the last line of defense.
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Pre-Flight Check
*   **Safety**: Run `npm test`.
*   **Build**: Run `npm run build`.
*   **Perf**: Run `npx bundle-visualizer` (Ensure no massive chunks).
*   **SEO**: `Task(resonance-seo, "Verify Meta Tags, Sitemap, and Robots.txt.")`

### Step 2: Versioning
*   **Action**: Determine Semantic Version (Major/Minor/Patch).
    *   *Breaking* -> Major.
    *   *Feat* -> Minor.
    *   *Fix* -> Patch.
*   **Tool**: Update `package.json`.

### Step 3: Changelog
*   **Tool**: `git log --oneline [last_tag]..HEAD`.
*   **Action**: Update `CHANGELOG.md` with human-readable notes.

### Step 4: Deployment
*   **Action**: `git tag vX.Y.Z`.
*   **Action**: `git push origin main --tags`.
*   **Action**: Trigger Deploy (e.g., `vercel deploy --prod`).

## 4. Recovery
*   **Build Fail**: Abort immediately. Do not tag.
*   **Deploy Fail**: Revert tag: `git tag -d vX.Y.Z`.

## 5. Governance (Definition of Done)
*   **Artifact**: Release vX.Y.Z.
*   **State Update**: Task: "Shipped vX.Y.Z". Cycle Complete.
