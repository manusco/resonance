# Production Readiness Checklist

> **Objective**: Ensure the system is observable, resilient, and recoverable.

## 1. Observability (The "Eyes")
- [ ] **Structured Logging**: JSON logs (not text) with valid trace IDs.
- [ ] **Error Tracking**: Sentry/Datadog connected and reporting.
- [ ] **Health Checks**: `/healthz` endpoint returning 200 OK (and checking DB connection).

## 2. Infrastructure (The "Bones")
- [ ] **Environment Variables**: Audit all `NEXT_PUBLIC_` vars (No secrets!).
- [ ] **Secrets Management**: Secrets injected at runtime, not build time.
- [ ] **CDN/Caching**: Static assets cached with long TTL.
- [ ] **Database**: Connection pooling enabled (Supabase Transaction Mode / PgBouncer).

## 3. Deployment Safety (The "Brakes")
- [ ] **Rollback Plan**: "If this fails, how do I revert in < 30s?"
- [ ] **Database Migration**: Non-breaking changes only (Expand-Contract pattern).
- [ ] **Smoke Tests**: Automated check running immediately after deploy.

## 4. Vercel Specifics
- [ ] **Edge vs Node**: Verify runtime compatibility (Node for extensive libraries).
- [ ] **Region**: Serverless functions running in same region as Database (e.g., iad1).
