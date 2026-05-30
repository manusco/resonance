# Protocol: Performance Engineering & CWV Optimization

> **Status**: Core Implementation Standard
> **Objective**: Achieve Lighthouse 100 through First-Principles Resource Management.

## 1. The Asset Pipeline (Zero-Waste Payloads)

Browser performance begins at the build step. Native optimization pipelines must handle every pixel and glyph.

### Progressive Image Loading
*   **The "Static" Trap**: Referencing images via raw string paths in a public assets folder bypasses build-time optimization.
*   **The Component Pattern**: Import images directly into your components. This allows the build engine to generate modern formats (WebP/AVIF) and responsive source sets.
*   **Prevent Layout Shift**: Explicitly define `width` and `height` or `aspect-ratio` on every image tag to reserve space before the asset loads.
*   **Lazy as Default**: Every image should be `loading="lazy"` by default, except for those in the initial viewport.

### Typography & Font-Face
*   **Self-Hosting is Mandatory**: External font loaders (Google Fonts API) add DNS lookups and pre-connection overhead.
*   **Format Priority**: Use `.woff2` exclusively. It offers the highest compression.
*   **FOIT/FOUT Mitigation**: Use `font-display: swap`. Ensure text is visible immediately using a system fallback.

---

## 2. The Critical Path (Priority Orchestration)

The browser is a resource-scheduling engine. You must tell it what to care about.

### LCP (Largest Contentful Paint) Optimization
*   **The Eager Exception**: The LCP element (usually a hero image) must be the *only* image set to `loading="eager"`.
*   **Fetch Priority**: Apply `fetchpriority="high"` to the LCP element. This forces the browser to prioritize the download above all other scripts and assets.
*   **Preconnect**: Only preconnect to truly critical 3rd party domains (e.g., Auth, Payments). Limit to < 3 domains to avoid connection saturation.

---

## 3. Infrastructure & Delivery

The server is the final bottleneck. Efficiency here is non-negotiable.

### Immutable Caching
*   **Fingerprinting**: Ensure all static assets (JS, CSS) use content-based hashing in filenames to allow for permanent caching.
*   **TTL Strategy**: Set `Cache-Control` headers to `public, max-age=31536000, immutable` for all fingerprinted assets.
*   **Expiry Headers**: Configure the server (Apache, Nginx, or Edge) to enforce long-lived expiry on invariant assets like fonts and brand images.

### Transmission Efficiency
*   **Modern Compression**: Enable Brotli (with Gzip fallback) for all text-based assets.
*   **Minification**: Ensure the build process strips unnecessary characters from the production bundle.

---

## 4. Performance Invariants (The "Golden Rules")

1.  **Payload < 100KB**: The initial HTML document should target < 100KB uncompressed.
2.  **No Render-Blocking Fonts**: Fonts must not block the first paint.
3.  **Visual Over-Implementation**: If a feature costs > 10 points in Lighthouse, find a lower-cost implementation or kill it.

---

## 5. Framework Implementation Notes

While these principles are universal, the implementation varies by environment:

### Astro Implementation
*   **Images**: Use the `<Image />` component from `astro:assets`. It automatically handles the "Component Pattern" and "Responsive Scaling."
*   **Assets**: Place assets in `src/assets/` rather than `public/` to trigger the build-time pipeline.
*   **Head**: Use the `fetchpriority` attribute directly on the component defining your Hero image.

### General Node/Vite Frameworks
*   **Vite**: Use the `?url` or direct import syntax for assets to ensure they are tracked by the graph.
*   **Next.js**: Utilize the `next/image` component for similar managed optimization.

---
*Created by the Performance Engineer & Librarian agents. Enforcing the Universal 1% Standard.*
