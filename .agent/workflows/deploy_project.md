---
description: Deploy the project to production using the 'ShipIt' protocol.
---

# Workflow: Deploy Project ("The ShipIt Protocol")

**Trigger**: "Deploy this", "Go live", "Production push".
**Context**: "It works on my machine" is not a valid deployment strategy.

## 1. The Deep Audit (Pre-Flight)
*Activate Skill*: `resonance-devops`

- [ ] **Type Safety**: `tsc --noEmit`. Zero errors allowed.
- [ ] **Lint Safety**: `eslint . --max-warnings 0`. Zero warnings allowed.
- [ ] **Tree Shake**: Run `npx bundle-visualizer` (or similar).
    -   *Gate*: No single chunk > 250kb (Initial Load).
- [ ] **Secrets**: Verify `.env` vs `.env.example`. Are all keys present in Vercel/AWS?

## 2. Asset Optimization
*Activate Skill*: `resonance-performance`

- [ ] **Images**: All static assets must be WebP/AVIF.
- [ ] **Fonts**: Verify `font-display: swap` is used.
- [ ] **Metadata**: Title, Description, and OG Image present for all public routes.

## 3. The Push
*Activate Skill*: `resonance-devops`

- [ ] **Deploy**: `vercel deploy --prod` (or equivalent).
- [ ] **Smoke Test (Automated)**:
    ```bash
    curl -I https://project.com/health
    # Must return HTTP 200
    ```

## 4. Post-Deploy Verification (The Lighthouse)
*Activate Skill*: `resonance-qa`

- [ ] **Performance**: Run Google Lighthouse (or PageSpeed).
    -   *Target*: >90 Performance, >95 Accessibility.
- [ ] **Console check**: Open DevTools on production.
    -   *Gate*: Zero Red Errors.
- [ ] **Tag**: `git tag -a v1.x.y -m "Release"`
