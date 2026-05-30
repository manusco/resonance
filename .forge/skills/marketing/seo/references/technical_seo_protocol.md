# Technical SEO Protocol — 9-Category Audit Framework

> The infrastructure layer. If the foundation is broken, nothing else matters.

## 1. Crawlability

- **robots.txt**: Exists, valid, not blocking critical resources or API endpoints that render content
- **XML sitemap**: Exists, referenced in robots.txt, valid format, contains only 200 OK canonical URLs
- **Noindex tags**: Verify intentional vs accidental
- **Crawl depth**: Important pages within 3 clicks of homepage
- **JavaScript rendering**: Check if critical content requires JS execution
- **Crawl budget**: For large sites (>10k pages), efficiency matters — eliminate index bloat
- **Orphan nodes**: Pages with 0 internal inbound links (the bot cannot find them)

### AI Crawler Management

| Crawler | Company | robots.txt token | Purpose |
|---------|---------|-------------------|---------|
| GPTBot | OpenAI | `GPTBot` | Model training |
| ChatGPT-User | OpenAI | `ChatGPT-User` | Real-time browsing |
| ClaudeBot | Anthropic | `ClaudeBot` | Model training |
| PerplexityBot | Perplexity | `PerplexityBot` | Search index + training |
| Bytespider | ByteDance | `Bytespider` | Model training |
| Google-Extended | Google | `Google-Extended` | Gemini training (NOT search) |
| CCBot | Common Crawl | `CCBot` | Open dataset |

**Key distinctions:**
- Blocking `Google-Extended` prevents Gemini training but does NOT affect Google Search indexing or AI Overviews
- Blocking `GPTBot` prevents OpenAI training but does NOT prevent ChatGPT from citing via browsing (`ChatGPT-User`)
- **Recommendation**: Cross-reference `geo_protocol.md` for full AI visibility strategy before blocking

**Example selective blocking:**
```
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: *
Allow: /
```

---

## 2. Indexability

- **Canonical tags**: Self-referencing, no conflicts with noindex
- **Duplicate content**: Near-duplicates, parameter URLs, www vs non-www
- **Thin content**: Pages below minimum word counts per page type (see `quality_gates.md`)
- **Pagination**: rel=next/prev or load-more pattern
- **Hreflang**: Correct for multi-language/multi-region sites
- **Index bloat**: Unnecessary pages consuming crawl budget

---

## 3. Security

- **HTTPS**: Enforced, valid SSL certificate, no mixed content
- **Security headers**:
  - Content-Security-Policy (CSP)
  - Strict-Transport-Security (HSTS)
  - X-Frame-Options
  - X-Content-Type-Options
  - Referrer-Policy
- **HSTS preload**: Check preload list inclusion for high-security sites

---

## 4. URL Structure

- **Clean URLs**: Descriptive, hyphenated, no query parameters for content
- **Hierarchy**: Logical folder structure reflecting site architecture
- **Redirects**: No chains (max 1 hop), 301 for permanent moves
- **URL length**: Flag >100 characters
- **Trailing slashes**: Consistent usage

---

## 5. Mobile Optimization

- **Responsive design**: Viewport meta tag, responsive CSS
- **Touch targets**: Minimum 48x48px with 8px spacing
- **Font size**: Minimum 16px base
- **No horizontal scroll**
- **Mobile-first indexing**: 100% complete as of July 5, 2024. Google crawls and indexes ALL websites exclusively with mobile Googlebot user-agent

---

## 6. Core Web Vitals

| Metric | Target | Replaced |
|--------|--------|----------|
| **LCP** (Largest Contentful Paint) | < 2.5s | — |
| **INP** (Interaction to Next Paint) | < 200ms | FID (March 12, 2024) |
| **CLS** (Cumulative Layout Shift) | < 0.1 | — |

- Evaluation uses 75th percentile of real user data
- FID was fully removed from all Chrome tools on September 9, 2024. Do NOT reference FID anywhere.
- Cross-reference `performance_optimization_protocol.md` for implementation details

---

## 7. Structured Data

- **Detection**: JSON-LD (preferred), Microdata, RDFa
- **Validation**: Against Google's currently supported types (see `schema_types_current.md`)
- **JS rendering warning** (December 2025): Structured data injected via JavaScript may face delayed processing. For time-sensitive markup (Product, Offer), include JSON-LD in initial server-rendered HTML

---

## 8. JavaScript Rendering

### JavaScript SEO Guidance (December 2025 Update)

1. **Canonical conflicts**: If canonical in raw HTML differs from one injected by JS, Google may use EITHER. Ensure canonical tags are identical between server-rendered and JS-rendered output.
2. **noindex with JavaScript**: If raw HTML has `noindex` but JS removes it, Google MAY still honor the noindex from raw HTML. Serve correct directives in initial HTML.
3. **Non-200 status codes**: Google does NOT render JavaScript on non-200 pages. JS-injected content/meta on error pages is invisible to Googlebot.
4. **Structured data in JS**: Product, Article, and other schema injected via JS may face delayed processing.

**Best practice**: Serve critical SEO elements (canonical, meta robots, structured data, title, meta description) in the initial server-rendered HTML.

**SPA frameworks** (React, Vue, Angular): Flag client-side rendering that may cause indexing issues. Verify dynamic rendering or SSR setup if applicable.

---

## 9. IndexNow Protocol

- Supported by Bing, Yandex, Naver (not Google)
- Provides near-instant indexing notification for content changes
- Recommend implementation for faster indexing on non-Google engines
- Complements traditional sitemap submission

---

## Audit Output

| Category | Status | Score |
|----------|--------|-------|
| Crawlability | pass/warn/fail | XX/100 |
| Indexability | pass/warn/fail | XX/100 |
| Security | pass/warn/fail | XX/100 |
| URL Structure | pass/warn/fail | XX/100 |
| Mobile | pass/warn/fail | XX/100 |
| Core Web Vitals | pass/warn/fail | XX/100 |
| Structured Data | pass/warn/fail | XX/100 |
| JS Rendering | pass/warn/fail | XX/100 |
| IndexNow | pass/warn/fail | XX/100 |

### Priority Levels
- **Critical**: Blocks indexing or causes penalties (fix immediately)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)
