# Core Web Vitals Protocol

> "Google cares about speed. Users care about speed. You care about speed."

## 1. The Big Three

1.  **LCP (Largest Contentful Paint)**: Loading. < 2.5s.
    *   *The Fix*: Optimize Images (WebP), Preload Hero, Critical CSS.
    *   *Agent Action*: Check network tab for `image.png` > 100kb.
2.  **INP (Interaction to Next Paint)**: Interactivity. < 200ms.
    *   *The Fix*: Debounce search inputs. Use `useTransition`. Do not block Main Thread.
    *   *Agent Action*: Profile CPU for long tasks.
3.  **CLS (Cumulative Layout Shift)**: Stability. < 0.1.
    *   *The Fix*: Width/Height on ALL images. Skeleton loaders.
    *   *Agent Action*: Enable "Layout Shift Regions" in Chrome DevTools.

## 2. The Verification

## Source Card

- Primary source: https://web.dev/articles/vitals
- Verified: 2026-08-15
- Scope: Core Web Vitals field-measurement guidance.
- Review trigger: Google updates Web Vitals thresholds or replaces a Core Web Vital.

*   **Field data first**: judge Core Web Vitals at the 75th percentile when real-user data exists.
*   **Lighthouse**: useful lab signal, not production truth. Use it to reproduce and debug.
*   **WebPageTest**: run on representative devices and networks, not a single arbitrary 3G preset.
*   **RUM (Real User Monitoring)**: Vercel Analytics / Sentry / browser APIs.

> 🔴 **Rule**: If field or representative lab data misses the product's Core Web Vitals target, either fix it, document a conscious exception, or ship as DONE_WITH_CONCERNS.
