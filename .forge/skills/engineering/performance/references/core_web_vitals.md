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

*   **Lighthouse**: Run it locally. Score > 90.
*   **WebPageTest**: Run it on 3G.
*   **RUM (Real User Monitoring)**: Vercel Analytics / Sentry.

> 🔴 **Rule**: If LCP > 2.5s, the feature is not shipped.
