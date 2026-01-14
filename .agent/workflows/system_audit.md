---
description: Run a full system health check (Automated + Manual).
---

# Workflow: System Audit ("The MRI")

**Trigger**: "Audit the system", "Health check".
**Context**: Deep scan of the project status.

## 1. Code Quality
*Activate Skill*: `resonance-core`

- [ ] **Tech Debt**: Scan for `TODO` and `FIXME`.
- [ ] **Entropy**: Check file structure. Is it clean?

## 2. Security
*Activate Skill*: `resonance-security`

- [ ] **Deps**: Run dependency audit.
- [ ] **Config**: Check exposed headers/secrets.

## 3. Performance
*Activate Skill*: `resonance-performance`

- [ ] **Lighthouse**: Run Audit. Target > 90.
- [ ] **Bundle**: Check size.

## 4. Growth/SEO
*Activate Skill*: `resonance-seo` / `resonance-growth`

- [ ] **Meta**: Check tags.
- [ ] **Analytics**: Is tracking firing?

## 5. Report
- [ ] **Output**: Generate `docs/audit_report_YYYY-MM-DD.md`.
- [ ] **Action**: Create tasks for critical issues.
