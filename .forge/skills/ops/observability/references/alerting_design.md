# Alerting Design and On-Call Hygiene

## Contents
- The one rule
- Symptom vs cause
- The test for an actionable alert
- Multiwindow burn-rate alerts
- Severity: page vs ticket
- Killing alert noise
- Anatomy of a good alert
- On-call hygiene

## The one rule

Every alert that reaches a human must be worth waking that human for, and must tell them what to do. If either half fails, it is not an alert. It is a dashboard, a log, or noise. This single rule generates almost every guideline below.

## Symptom vs cause

Alert on symptoms (what the user experiences), diagnose with causes (what the machine is doing).

- **Symptom** (page-worthy): elevated error rate, latency past the SLO threshold, the service is unreachable, checkout success is dropping, the queue that feeds a user-facing job is not draining. The user feels these.
- **Cause** (diagnostic, not page-worthy on its own): CPU at 90%, memory climbing, a pod restarted, disk 70% full, a single node unhealthy behind a healthy load balancer. The user may feel nothing.

Why causes make bad pages: a system can run hot and serve every request correctly. A pod can restart with zero user impact because the replica set covered it. Paging on causes floods the on-call with alerts that had no consequence, and the predictable result is that people mute the pager or learn to ignore it, so the one page that mattered gets ignored too.

The correct use of causes: they populate the dashboard you open after a symptom alert fires, to answer "why." CPU saturation is a superb diagnostic and a terrible page. The exception: a cause that is itself an unrecoverable, imminent symptom, disk that will be full in 30 minutes with no auto-remediation, can page, because inaction guarantees user pain soon and a human must act now.

## The test for an actionable alert

Before creating any alert, answer all four. A no on any one means do not page.

1. **Is a user affected, now or imminently and certainly?** If the impact is purely internal and self-healing, it is not a page.
2. **Is human action required?** If the system recovers on its own, or auto-remediation already handles it, let it. Page only when a person must decide or intervene.
3. **Is it urgent?** If it can wait until business hours, it is a ticket, not a 3am page. Urgency is what separates a page from a ticket.
4. **Is there a clear first response?** If the only answer is "watch it and see," there is nothing to do, so there is no alert. Attach the runbook link; if you cannot write step one, you do not have an alert.

If the honest runbook is "acknowledge and go back to sleep," delete the alert. It is training the on-call to distrust the pager.

## Multiwindow burn-rate alerts

The mature way to alert on an SLO. Instead of "the SLO is breached" (which fires only after the damage is done) or "any error at all" (which cries wolf), alert on how fast the error budget is burning, measured over two windows at once.

The problem each piece solves:
- A **fast, short window** catches a sudden hard outage within minutes. But short windows alone are twitchy and fire on brief blips.
- A **slow, long window** catches a low-grade leak that would quietly drain the month's budget. But long windows alone are slow to notice a real outage.
- Requiring a **short confirmation window to also be burning** before firing removes the twitch: a one-minute blip that already recovered will not page, because the confirmation window is no longer hot.

A common two-tier setup for a 30-day budget:
- **Fast burn (page)**: budget burning about 14x (would exhaust the month in ~2 days), evaluated over a 1-hour window and confirmed by a 5-minute window. This is an outage happening right now.
- **Slow burn (ticket)**: budget burning about 3x (would exhaust the month in ~10 days), evaluated over a 6-hour window and confirmed by a 30-minute window. This is a persistent problem worth fixing this week, not tonight.

The pair gives you fast detection of real outages without paging on every transient error, and it ties the page directly to user-facing budget loss rather than to an arbitrary threshold. The burn-rate math itself is in the SLO reference.

## Severity: page vs ticket

Two channels, and be strict about which is which.

- **Page** (wakes a human, immediate): user-facing symptom, urgent, action required now. Fast-burn SLO alerts, hard outages, data-loss risk in progress.
- **Ticket / async** (a queue reviewed in hours): slow-burn budget alerts, capacity trends approaching a limit, non-urgent degradations, anything the system tolerated for now.

The failure mode is severity inflation: making everything a page because it feels safer. It is not safer. Every false page raises the odds the next real one is missed, because attention and trust are finite. Under-paging loses one incident; over-paging erodes the response to all of them.

## Killing alert noise

Noise is the tax that makes an alerting system useless. Attack it directly.

- **Delete alerts that never lead to action.** Audit fired alerts on a regular cadence: for each, did anyone do anything? A rule that fired 40 times and produced zero actions is pure noise. Delete it or downgrade it to a ticket.
- **Alert on the symptom, not on each contributing cause.** One "checkout error rate high" page beats separate pages for the DB, the cache, and the payment gateway that all feed it. The symptom is one page; the causes are the dashboard you then open.
- **Group and deduplicate.** A hundred failing requests are one incident, not a hundred pages. Group related alerts into a single notification.
- **Set thresholds off real distributions, not round numbers.** A threshold at a made-up "sounds bad" number fires constantly under normal variance. Base it on the SLO and observed behavior.
- **Add hysteresis and a for-duration.** Require the condition to hold for N minutes before firing so a two-second spike does not page, and require it to clear before resolving so an alert does not flap open and shut.
- **Track alert precision.** Of alerts that paged, what fraction were real and actionable? A low number is a broken alerting system regardless of how much it "covers." Coverage without precision just trains people to ignore pages.

## Anatomy of a good alert

When it fires, the notification itself should carry:

- **What symptom**, in user terms: "checkout error rate is 12% (SLO: under 1%)," not "error_ratio > 0.01 on svc-checkout."
- **User impact**: who is affected and how much (all EU checkouts failing vs a 2% degradation on one endpoint). Impact drives the response.
- **First response step or runbook link.** Even one line, "check the payment gateway dashboard first," saves minutes when the responder is half awake.
- **A pivot into telemetry**: a link to the trace exemplars or the filtered logs for this symptom, so the responder goes from page to evidence in one click.
- **Severity and whether it self-clears**, so the responder knows if they must act or merely confirm.

## On-call hygiene

The alerting system exists to protect the humans who answer it. Keep the human side healthy or the best rules still fail.

- **Every page is reviewable.** Was it actionable? Was it a real symptom? Feed the answers back into tuning; an alert that keeps paging for nothing gets fixed or deleted, not endured.
- **Cap the page budget.** If on-call is paged more than a small handful of times per shift, the system is too noisy to sustain and the noise itself becomes the top incident. Treat alert volume as a health metric with a target.
- **Every page has a runbook.** No runbook means the responder improvises under stress at the worst time. Writing the runbook also forces the question "is there actually an action here," which culls non-alerts.
- **Alert on your alerting.** If the telemetry pipeline or the alert evaluator dies, you go blind and silent, which looks identical to "everything is fine." Have a heartbeat that pages when the signal itself stops arriving.
- **Feed resolved incidents into the retro, not back into more alerts by reflex.** The post-incident review decides whether the fix is a new alert, a code change, or auto-remediation. Adding an alert is one option, and often the lazy one; sometimes the right answer is to remove the failure mode so nothing needs to page.
