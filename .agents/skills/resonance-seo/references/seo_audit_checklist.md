# SEO Audit Checklist

> "Technical SEO is the foundation."

## 1. The Crawl (Screaming Frog Style)

Simulate the googlebot.
1.  **Broken Links (404s)**: Zero tolerance.
2.  **Redirect Chains**: Fix 301 -> 301 -> 200. Direct link only.
3.  **Hreflang**: Verify language tags match the content.

## 2. The Metadata Check

Every page needs:
*   [ ] `<title>` (Unique, < 60 chars).
*   [ ] `<meta description>` (Unique, < 160 chars).
*   [ ] `og:image` (Social preview).
*   [ ] `<link rel="canonical">` (Prevent duplicate content).

## 3. The Indexing Check

*   [ ] `robots.txt`: Is `/admin` blocked? Is `/` allowed?
*   [ ] `sitemap.xml`: Does it list only 200 OK pages?

## 4. The Performance Check
*   [ ] **LCP Element**: Is it using `fetchpriority="high"` and `loading="eager"`?
*   [ ] **Image Optimization**: Are images imported (not raw strings) and served as WebP/AVIF?
*   [ ] **Fonts**: Are they self-hosted with `font-display: swap`?
*   [ ] **Caching**: Are assets served with 1-year expiry headers?

## 5. The GSC Intelligence Check
*   [ ] **Striking Distance**: Are pages in Pos 8-20 optimized for high-impression queries?
*   [ ] **Internal Link Density**: Does the page meet the ~1 link per 50 words target?
*   [ ] **Direct Answer**: Does the page lead with a 40-60 word bolded answer?

> 🔴 **Rule**: Run `npx lighthouse` on your critical pages before every release. Target 95+ for Performance.
