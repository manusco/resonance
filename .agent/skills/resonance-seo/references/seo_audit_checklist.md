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

> 🔴 **Rule**: Run `npx lighthouse` on your critical pages before every release.
