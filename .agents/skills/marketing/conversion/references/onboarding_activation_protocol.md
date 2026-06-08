# Onboarding Activation Protocol

> **Goal**: Minimize time-to-value. Get users to their "aha moment" before motivation fades.

## Contents

- [1. The Activation Framework](#1-the-activation-framework)
- [2. Identifying the "Aha Moment"](#2-identifying-the-aha-moment)
- [3. First-Run Experience Patterns](#3-first-run-experience-patterns)
- [4. Empty State Design](#4-empty-state-design)
- [5. Onboarding Email Sequence (Supporting, Not Duplicating)](#5-onboarding-email-sequence-supporting-not-duplicating)
- [6. Habit Formation Loop](#6-habit-formation-loop)
- [7. Common Failures](#7-common-failures)

## 1. The Activation Framework

```
Signup → First Value → Habit Formation → Retention
         ↑                                    ↑
    TIME-TO-VALUE (minimize)           ACTIVATION (measure)
```

**Core Axiom**: Users who don't experience value in the first session rarely return. Every unnecessary step between signup and first value is a drop-off.

## 2. Identifying the "Aha Moment"

The activation milestone is the earliest action that correlates with long-term retention.

| Product Type | Typical "Aha Moment" | Measurement |
|-------------|---------------------|-------------|
| SaaS tool | Complete first core action | Created first [thing] |
| Collaboration | Invite first teammate | Team size > 1 |
| Analytics | See first meaningful insight | Dashboard loaded with data |
| Marketplace | Complete first transaction | First purchase/sale |
| Content | Consume first high-value piece | Read/watch completion |

**How to find yours**: Cohort analysis — compare retained users vs churned users. What actions did retained users take in their first 7 days that churned users didn't?

## 3. First-Run Experience Patterns

### Pattern A: Setup Wizard (3-5 steps max)
- Collect essential config during onboarding.
- Show progress: "Step 2 of 4" (Goal-Gradient Effect).
- Allow skip but track — users who skip activate slower.
- End on a win, not a settings page.

### Pattern B: Interactive Tutorial
- Guide user through their first real action (not a video tour).
- Use their actual data, not sample data.
- Highlight value at each step: "You just [achieved outcome]."

### Pattern C: Template/Quick Start
- Offer pre-built templates so the product isn't empty.
- "Start with this template" > "Create from scratch."
- Templates reduce the Blank Canvas Problem (analysis paralysis).

### Pattern D: Checklist
- Show 5-7 setup actions as a checklist in the UI.
- Pre-check completed items (Zeigarnik Effect pulls completion).
- Celebrate completion with a congratulations state.

## 4. Empty State Design

Empty states are the most critical screens in your product. They're what every new user sees.

**Rules:**
- Never show a blank page or "No data yet."
- Show what the page *will* look like with data (sample/demo data).
- Include a single, clear CTA: "Create your first [thing]."
- Explain the value: "This is where you'll see [outcome]."

## 5. Onboarding Email Sequence (Supporting, Not Duplicating)

Emails support in-app onboarding — they don't replace it.

| Timing | Email Purpose | Content |
|--------|-------------|---------|
| Immediate | Welcome + first step | "Here's how to get started in 2 minutes" |
| Day 1 | Quick win | "Try this one feature" |
| Day 3 | Feature highlight | Showcase a feature they haven't used |
| Day 5 | Social proof | "Here's what [Customer] achieved" |
| Day 7 | Check-in | "Need help? Here's our top resources" |
| Day 10 | Advanced tip | "Power users do this" |
| Day 14 | Upgrade/expand | "Ready for more?" (if freemium) |

## 6. Habit Formation Loop

Long-term activation requires building habits, not just first-use success.

### The Hook Model (Applied to Onboarding)
1. **Trigger**: Email or in-app notification ("Your weekly report is ready").
2. **Action**: Low-friction engagement (click to view report).
3. **Variable Reward**: New insights, progress, recognition.
4. **Investment**: Customize settings, add data, invite team.

### Measuring Activation Health

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Time-to-first-value | Speed to "aha moment" | < 5 minutes |
| Setup completion rate | % who finish onboarding | > 60% |
| Day 1 retention | % who return next day | > 40% |
| Day 7 retention | % active after one week | > 25% |
| Feature adoption rate | % using core feature | > 50% in first week |

## 7. Common Failures

1. **Feature tour instead of value tour**: Showing all features ≠ showing value. Focus on the one action that delivers the first win.
2. **Asking too much at signup**: Profile photo, company size, role — every field is a dropout. Ask only what's needed to personalize the first-run.
3. **No fallback for confused users**: If a user pauses for >30 seconds, offer help (tooltip, chat, or guided path).
4. **Ignoring mobile onboarding**: Mobile users have less patience. Shorten every step.
5. **One-size-fits-all**: Segment by role/use case during onboarding and tailor the path.
