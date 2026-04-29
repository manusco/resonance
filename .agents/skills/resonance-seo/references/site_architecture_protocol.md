# Site Architecture Protocol

> **Goal**: Design website structure — page hierarchy, URL patterns, navigation, and internal linking — for user clarity and search engine optimization.

## 1. Hierarchy Design

### The 3-Click Rule
Users should reach any important page within 3 clicks from the homepage. Not absolute, but if critical pages are 4+ levels deep, something is wrong.

### Depth Guidelines

| Approach | Best For | Risk |
|----------|----------|------|
| Flat (2 levels) | Small sites, portfolios | Doesn't scale |
| Moderate (3 levels) | Most SaaS, content sites | Good balance |
| Deep (4+ levels) | E-commerce, large docs | Buries content |

**Rule**: Go as flat as possible while keeping navigation clean. If a dropdown has 20+ items, add hierarchy.

### Level Structure

| Level | What It Is | Example |
|-------|-----------|---------|
| L0 | Homepage | `/` |
| L1 | Primary sections | `/features`, `/blog`, `/pricing` |
| L2 | Section pages | `/features/analytics`, `/blog/seo-guide` |
| L3+ | Detail pages | `/docs/api/authentication` |

## 2. URL Structure Rules

1. **Readable by humans** — `/features/analytics` not `/f/a123`
2. **Hyphens, not underscores** — `/blog/seo-guide` not `/blog/seo_guide`
3. **Reflect the hierarchy** — URL path matches site structure
4. **Consistent trailing slash policy** — pick one (with or without) and enforce
5. **Lowercase always** — `/About` should 301 → `/about`
6. **Short but descriptive** — `/blog/landing-page-conversions` > `/blog/how-to-improve-landing-page-conversion-rates`

### URL Patterns by Page Type

| Page Type | Pattern | Example |
|-----------|---------|---------|
| Feature page | `/features/{name}` | `/features/analytics` |
| Blog post | `/blog/{slug}` | `/blog/seo-guide` |
| Case study | `/customers/{slug}` | `/customers/acme-corp` |
| Documentation | `/docs/{section}/{page}` | `/docs/api/authentication` |
| Comparison | `/vs/{competitor}` | `/vs/competitor-name` |
| Integration | `/integrations/{name}` | `/integrations/slack` |
| Landing page | `/lp/{slug}` or `/{slug}` | `/lp/webinar` |
| Legal | `/{page}` | `/privacy`, `/terms` |

### Common Mistakes
- **Dates in blog URLs**: `/blog/2024/01/post` adds no value. Use `/blog/post`.
- **Over-nesting**: `/products/category/subcategory/item/detail` — flatten.
- **Changing URLs without redirects**: Every old URL needs a 301. Lost backlink equity is lost authority.
- **IDs in URLs**: `/product/12345` — use slugs.
- **Inconsistent parents**: Don't mix `/features/analytics` and `/product/automation`.

## 3. Navigation Design

### Header Navigation
- **4-7 items max** (more causes decision paralysis).
- **CTA button rightmost** ("Start Free Trial", "Get Started").
- **Logo** links to homepage (left side).
- **Order by priority**: most important/visited pages first.
- Mega menus: limit to 3-4 columns.

### Footer Organization
Group into columns:
- **Product**: Features, Pricing, Integrations, Changelog
- **Resources**: Blog, Case Studies, Templates, Docs
- **Company**: About, Careers, Contact, Press
- **Legal**: Privacy, Terms, Security

### Breadcrumbs
- Mirror the URL hierarchy.
- Every segment is a clickable link except current page.
- Implement BreadcrumbList schema (JSON-LD) for SERP display.
- Format: `Home > Features > Analytics`

## 4. Internal Linking Strategy

### Link Types

| Type | Purpose | Example |
|------|---------|---------|
| Navigational | Section navigation | Header, footer, sidebar |
| Contextual | Related content within text | "Learn more about [analytics](/features/analytics)" |
| Hub-and-spoke | Cluster content → hub | Blog posts linking to pillar page |
| Cross-section | Connect across sections | Feature page → related case study |

### Rules
1. **No orphan pages** — every page must have ≥1 internal link pointing to it.
2. **Descriptive anchor text** — "our analytics features" not "click here."
3. **5-10 internal links per 1000 words** (approximate guideline).
4. **Link to important pages more often** — homepage, features, pricing.
5. **Use breadcrumbs** — free internal links on every page.
6. **Related content sections** — "You might also like" at page bottom.

### Hub-and-Spoke Model
```
Hub: /blog/seo-guide (comprehensive overview)
├── Spoke: /blog/keyword-research (links back to hub)
├── Spoke: /blog/on-page-seo (links back to hub)
├── Spoke: /blog/technical-seo (links back to hub)
└── Spoke: /blog/link-building (links back to hub)
```
Each spoke links to hub. Hub links to all spokes. Spokes cross-link where relevant.

## 5. Site Type Templates

| Site Type | Typical Depth | Key Sections |
|-----------|--------------|-------------|
| SaaS marketing | 2-3 levels | Home, Features, Pricing, Blog, Docs |
| Content/blog | 2-3 levels | Home, Blog, Categories, About |
| E-commerce | 3-4 levels | Home, Categories, Products, Cart |
| Documentation | 3-4 levels | Home, Guides, API Reference |
| Small business | 1-2 levels | Home, Services, About, Contact |

## 6. Audit Checklist

- [ ] Every page reachable within 3 clicks of homepage
- [ ] No orphan pages (every page has ≥1 inbound internal link)
- [ ] No broken internal links (404s)
- [ ] Anchor text is descriptive
- [ ] Breadcrumbs implemented with BreadcrumbList schema
- [ ] URL structure is consistent and clean
- [ ] Important pages have the most inbound internal links
- [ ] Header nav has 4-7 items
- [ ] Footer links organized by category
