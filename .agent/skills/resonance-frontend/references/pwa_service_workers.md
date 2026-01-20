# PWA & Service Worker Protocol

> "Reliable. Fast. Engaging."

## 1. The Offline Fallback

The App MUST render *something* when offline.

*   **App Shell**: Cache the HTML/CSS skeleton.
*   **Offline Page**: "You are offline, check your connection."

## 2. Manifest.json

Every app needs a `manifest.json`.
*   `name`: Full name.
*   `short_name`: Homescreen name.
*   `display`: `standalone` (Removes browser bar).
*   `icons`: 192x192, 512x512 (Maskable).

## 3. Caching Strategies (Workbox)

1.  **Stale-While-Revalidate**: (Best for Assets). Serve fast from cache, update in background.
2.  **NetworkFirst**: (Best for API). Try network, fall back to offline cache if failed.
3.  **CacheFirst**: (Best for Fonts/Images). They never change.

> 🔴 **Rule**: If I turn off WiFi and reload, I should see the UI (even if empty). White screen is failure.
