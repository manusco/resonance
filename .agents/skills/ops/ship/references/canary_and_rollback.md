# Canary and Rollback: prove production works, and know how to undo

> A green pipeline means the code built. It does not mean production works. Ship to a few users first, prove the real system is healthy, and never deploy without a way back. The two rules: verify against production, and always have a rollback path ready before you start.

## Progressive rollout (canary)

Do not send a new release to everyone at once. Release it to a small slice first, watch it, then promote.

- **Canary slice:** route a small fraction of traffic (commonly 1 to 5 percent, or one instance, or an internal ring) to the new version. The rest stays on the known-good version.
- **Health window:** hold the canary for long enough to see real behavior (minutes for high-traffic, longer for low). Do not promote on the first green second.
- **Promote or abort:** if the canary is healthy against the checks below, roll forward to full traffic in steps. If not, abort the canary; only a few users were affected.
- **No canary path?** Then deploy and go straight to verification with a tighter watch and an itchier rollback finger. The absence of a canary raises the risk, it does not remove the need to verify.

## Post-deploy verification

The deploy is done when production is confirmed healthy, not when the pipeline passes. After deploy (or on the canary), check the real system:

- **Health endpoint** returns healthy.
- **One critical user path** actually works end to end (log in, load the core page, complete the key action). Drive it, do not assume it.
- **Error rate** is at or below baseline, not spiking.
- **Latency and saturation** are within normal range (see the observability skill for the signals).
- **The key business metric** (checkout, signup, whatever the release touched) is flowing.

Automate this as a smoke test that runs against production right after deploy, so verification is a command with output, not a vibe.

## Rollback

Know the undo before you deploy. Pick the mechanism the platform supports:

- **Roll back to the previous release** (redeploy the last known-good artifact or tag).
- **Feature flag off** (if the change is behind a flag, flip it; fastest and safest).
- **Abort the canary** (stop promoting, drain the canary slice).
- **Blue-green swap back** (point traffic at the old environment).

**Triggers to roll back, without deliberation:** a failed post-deploy smoke test, an error-rate spike, a latency regression past the SLO, or a broken critical path. When any fires, roll back first and investigate after. A fast rollback is a good outcome, not a failure; a slow debate while production is down is the failure.

## The order that matters

1. Confirm the rollback path exists. If it does not, do not deploy; build one first.
2. Deploy to the canary.
3. Verify against production.
4. Promote in steps, re-verifying, or roll back on any trigger.
5. Only after production is verified healthy is the release done.
