# 04 Systems & Operations

## 1. Testing Strategy
*If empty, assume manual testing only.*
- **Critical Paths:** [List the 3 flows that MUST NOT break, e.g., Login, Payment, Data Fetch]
- **Tooling:** [e.g. Playwright, Jest]
- **Command:** `npm run test`

## 2. CI/CD & Deployment
- **Provider:** [e.g. Vercel]
- **Triggers:** [e.g. Push to main deploys automatically]
- **Environment Variables:** [List required keys, do NOT list values]

## 3. Background Jobs (Cron)
- **Harvester:** [e.g. Runs every 4h via GitHub Actions. Source: /jobs/harvest.ts]
- **Cleanup:** [e.g. Runs daily. Logic: /jobs/cleanup.sql]