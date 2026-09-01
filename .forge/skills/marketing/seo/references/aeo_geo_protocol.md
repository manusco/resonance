# Generative Engine Optimization (GEO) Protocol

> The discipline of optimizing content for AI-generated answers - Google AI Overviews, ChatGPT, Perplexity, Bing Copilot.

## Contents

- [1. Evidence Boundary](#1-evidence-boundary)
- [2. Entity and Source Signals](#2-entity-and-source-signals)
- [3. The GEO Scoring Framework (5 Dimensions)](#3-the-geo-scoring-framework-5-dimensions)
- [4. AI Crawler Management](#4-ai-crawler-management)
- [5. llms.txt Standard](#5-llmstxt-standard)
- [6. Experimental Machine Signals](#6-experimental-machine-signals)
- [7. RSL 1.0 (Really Simple Licensing)](#7-rsl-10-really-simple-licensing)
- [8. Platform-Specific Optimization](#8-platform-specific-optimization)
- [9. The "Statistics" Hook](#9-the-statistics-hook)
- [10. The "Unique Data" Strategy (Citation Optimization)](#10-the-unique-data-strategy-citation-optimization)
- [11. Action Tiers](#11-action-tiers)
- [12. Audit Output](#12-audit-output)

## 1. Evidence Boundary

AI answer surfaces, crawler behavior, traffic share, and citation sources change quickly. Verify current platform behavior from primary documentation and direct observation before making a platform-specific claim. Record the query, locale, device, date, signed-in state when relevant, and the observed links or citations.

Treat AI citation as a distinct visibility channel. Do not assume its reach, value, or relationship to organic ranking is the same for every market.

---

## 2. Entity and Source Signals

Brand mentions, links, source reputation, topical fit, and first-party evidence may all matter to discovery or selection. Correlation studies do not establish a universal ranking formula. Use them to form hypotheses, then inspect actual citations, referral data, logs, and customer discovery for the target market.

---

## 3. The GEO Scoring Framework (5 Dimensions)

### 3.1 Citability Score (25%)

There is no universal passage length for AI citation extraction. Prefer the shortest passage that answers the question completely and keeps its qualifications and sources intact.

**Strong signals:**
- Clear, quotable sentences with specific facts/statistics
- Self-contained answer blocks (extractable without surrounding context)
- Direct answer early in the section, followed by the context and evidence it needs
- Claims attributed with specific sources
- Definitions following "X is..." or "X refers to..." patterns
- Unique data points not found elsewhere

**Weak signals:**
- Vague, general statements without specifics
- Opinion without evidence
- Buried conclusions (answer at end of paragraph)
- No specific data points

**The Direct Answer Format** (Resonance Standard):
```
[Question Rephrase] + [Direct Answer (Bold)] + [Nuance]
```
Place the direct answer near the heading when that serves the reader. Do not claim an engine will skip a page because an answer crosses a fixed word boundary.

### 3.2 Structural Readability (20%)

Compare AI citations with organic results for the actual query set. Overlap can inform a hypothesis, but it does not prove one stable selection rule.

**Strong signals:**
- Clean H1→H2→H3 heading hierarchy
- Question-based headings (match query patterns)
- Paragraphs sized for one coherent idea
- Tables for comparative data
- Ordered/unordered lists for step-by-step or multi-item content
- FAQ sections with clear Q&A format

**The Token Economy**: LLMs have limited attention. Fluff gets ignored.
- ❌ "In today's modern era of technology, it is important to consider..." (0 value)
- ✅ "Vector databases optimize high-dimensional search." (high information density)
- **Rule**: Remove filler, preserve needed qualifications, and support material claims.

### 3.3 Multi-Modal Content (15%)

Use multi-modal elements when they add evidence, explanation, or utility. Do not promise citation lift from their presence.

**Check for:**
- Text + relevant images (with descriptive alt text)
- Video content (embedded or linked)
- Infographics and charts
- Interactive elements (calculators, tools)
- Data tables (`<table>`) - LLMs parse tables for comparisons

### 3.4 Authority & Brand Signals (20%)

**Strong signals:**
- Author byline with credentials
- Publication date and last-updated date
- Citations to primary sources (studies, official docs, data)
- Organization credentials and affiliations
- Expert quotes with attribution
- Entity presence in Wikipedia, Wikidata
- Mentions on Reddit, YouTube, LinkedIn
- `sameAs` in JSON-LD linking to Crunchbase, LinkedIn, Wikipedia

**Weak signals:**
- Anonymous authorship
- No dates
- No sources cited
- No brand presence across platforms

**Brand Entity Association Rule**: If an LLM summarizes your topic without mentioning your brand, you have failed Brand Entity Association.

### 3.5 Technical Accessibility (20%)

Crawler rendering capabilities differ and change. Verify whether critical content is present in the fetched or rendered response used by the target system. Server-rendered content is the safest default for broad accessibility.

**Check for:**
- Server-side rendering (SSR) vs client-only content
- AI crawler access in robots.txt
- llms.txt file presence and configuration
- RSL 1.0 licensing terms
- Content behind login/paywall (invisible to AI)

---

## 4. AI Crawler Management

Check `robots.txt` for these AI crawlers:

| Crawler | Owner | Purpose |
|---------|-------|---------|
| GPTBot | OpenAI | Model training |
| OAI-SearchBot | OpenAI | OpenAI search features |
| ChatGPT-User | OpenAI | ChatGPT real-time browsing |
| ClaudeBot | Anthropic | Claude web features |
| PerplexityBot | Perplexity | Perplexity AI search |
| Google-Extended | Google | Gemini training (NOT Search) |
| CCBot | Common Crawl | Training data (often blocked) |
| Bytespider | ByteDance | TikTok/Douyin AI |
| cohere-ai | Cohere | Cohere models |

**Key distinctions:**
- Blocking `Google-Extended` prevents Gemini training but does NOT affect Google Search or AI Overviews (those use `Googlebot`)
- Blocking `GPTBot` prevents training but does NOT prevent ChatGPT from citing via browsing (`ChatGPT-User`)

**Recommendation:** Decide crawler access from current vendor documentation, the site's licensing and privacy posture, and observed access needs. Do not equate training crawler access with search citation eligibility.

---

## 5. llms.txt Standard

The emerging standard provides AI crawlers with structured content guidance.

**Location:** `/llms.txt` (root of domain)

**Format:**
```
# Title of site
> Brief description

## Main sections
- [Page title](url): Description
- [Another page](url): Description

## Optional: Key facts
- Fact 1
- Fact 2
```

---

## 6. Experimental Machine Signals

Experimental machine-facing signals can help discovery, but they are not proof of AI citation readiness by themselves.

**Audit rule:** separate directly observed crawler access from future-facing hints.

- Verify crawler access with `robots.txt`, status codes, server-rendered content, and logs where available.
- Treat llms.txt, AI preference declarations, HTTP Link discovery, and content negotiation as informational unless current primary documentation and the site context justify a stronger recommendation.
- Do not assign score points, pass/fail status, or promised citation lift to an emerging signal without measured evidence.
- Recommend HTTP Link service discovery only for API-first, developer-tooling, or documentation-heavy sites. Omit it for ordinary business pages unless there is a clear service-discovery use case.
- Test content negotiation with direct HTTP or browser request capture that shows headers and content type. A rendered body fetch is not enough for header-level claims.

---

## 7. RSL 1.0 (Really Simple Licensing)

Machine-readable AI licensing terms standard (December 2025).
Backed by Reddit, Yahoo, Medium, Quora, Cloudflare, Akamai, Creative Commons.

---

## 8. Platform-Specific Optimization

| Platform | Key Citation Sources | Optimization Focus |
|----------|---------------------|-------------------|
| **Google AI Overviews** | Verify citations on the target query set | Search fundamentals, clear passages, source quality |
| **ChatGPT** | Inspect returned citations and referral evidence | Entity clarity, inspectable primary sources |
| **Perplexity** | Inspect returned citations and referral evidence | Source quality, direct support for claims |
| **Bing Copilot** | Bing index, authoritative sites | Bing SEO, IndexNow |

---

## 9. The "Statistics" Hook

Use numbers when they materially answer the question, and present them in a table only when comparison benefits from rows and columns.
- **Pattern**: "According to [Study], 80% of..."
- **Rule**: Every claim should have a named source.

---

## 10. The "Unique Data" Strategy (Citation Optimization)

AI engines need a reason to cite *you* and not Wikipedia.
- **Create Unique Data**: Run a survey. Benchmark a tool. Release a dataset.
- **Name It**: Coining a term (e.g., "The 100ms Rule") makes you the primary source.
- **Quote Magnets**: Format content as extractable Q&A blocks.

---

## 11. Action Tiers

### Quick Wins
1. Add a direct definition when the reader needs one
2. Create self-contained answer passages with inspectable sources
3. Add question-based H2/H3 headings
4. Include specific statistics with sources
5. Add publication/update dates
6. Implement Person schema only when the visible content and current eligibility support it
7. Set crawler access intentionally from current vendor documentation and the site's licensing and privacy posture

### Medium Effort
1. Create or repair `/llms.txt` when site context and verified adoption justify it
2. Add author bio with credentials + Wikipedia/LinkedIn links
3. Ensure server-side rendering for key content
4. Build entity presence on Reddit, YouTube
5. Add comparison tables with data
6. Implement FAQ sections (structured, not schema for commercial sites)

### High Impact
1. Create original research/surveys (unique citability)
2. Build Wikipedia presence for brand/key people
3. Establish YouTube channel with content mentions
4. Implement comprehensive entity linking (`sameAs` across platforms)
5. Develop unique tools or calculators

---

## 12. Audit Output

Generate GEO analysis with:
1. **GEO Readiness Score: XX/100** (weighted across 5 dimensions)
2. **Platform breakdown** (Google AIO, ChatGPT, Perplexity scores)
3. **AI Crawler Access Status** (which crawlers allowed/blocked)
4. **Machine-Facing Signal Notes** (llms.txt, preference declarations, service discovery, or content negotiation when relevant)
5. **Brand Mention Analysis** (presence on Wikipedia, Reddit, YouTube, LinkedIn)
6. **Passage-Level Citability** (self-contained, source-backed passages identified)
7. **Server-Side Rendering Check** (JavaScript dependency analysis)
8. **Top 5 Highest-Impact Changes**
