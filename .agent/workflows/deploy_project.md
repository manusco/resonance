---
description: Deploy the project to production using the 'ShipIt' protocol.
---

# Workflow: Deploy Project ("The ShipIt Protocol")

**Trigger**: "Deploy this", "Go live", "Production push".
**Context**: "It works on my machine" is not a valid deployment strategy.

# Workflow: Deploy Project ("The ShipIt Protocol")

**Trigger**: "Deploy this", "Go live", "Production push".
**Context**: "It works on my machine" is not a valid deployment strategy.

## 1. PREPARE: The Deep Audit (Pre-Flight)
*Activate Skill*: `resonance-devops`

- [ ] **Type Safety**: `tsc --noEmit`. Zero errors allowed.
- [ ] **Lint Safety**: `eslint . --max-warnings 0`. Zero warnings allowed.
- [ ] **Tree Shake**: Run `npx bundle-visualizer` (or similar).
    -   *Gate*: No single chunk > 250kb (Initial Load).
- [ ] **Secrets**: Verify `.env` vs `.env.example`. Are all keys present in Vercel/AWS?

## 2. BACKUP: Asset Optimization & Safety
*Activate Skill*: `resonance-performance`

- [ ] **Snapshot**: Create a specific git tag for this release state.
- [ ] **Images**: All static assets must be WebP/AVIF.
- [ ] **Metadata**: Title, Description, and OG Image present for all public routes.

## 3. DEPLOY: The Push
*Activate Skill*: `resonance-devops`

- [ ] **Exec**: `vercel deploy --prod` (or equivalent).
- [ ] **Smoke Test (Automated)**:
    ```bash
    curl -I https://project.com/health
    # Must return HTTP 200
    ```

## 4. VERIFY: Post-Deploy Verification
*Activate Skill*: `resonance-qa`

- [ ] **Performance**: Run Google Lighthouse. (Target: >90 Perf).
- [ ] **Console check**: Open DevTools on production. (Gate: Zero Red Errors).
- [ ] **Logs**: Check server logs for start-up crashes.

## 5. CONFIRM or ROLLBACK
*Activate Skill*: `resonance-devops`

- [ ] **Decision Matrix**:
    -   **Stable**: `git tag -a v1.x.y -m "Release"` -> **CONFIRM**
    -   **Unstable (>1% Errors)**: Execute **Rollback Protocol** immediately.
