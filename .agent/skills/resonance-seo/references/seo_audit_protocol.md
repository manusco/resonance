# Protocol: SEO System Diagnostics (The Audit)
> **Framework**: The Resonance Diagnostic Method
> **Resonance Phase**: Maintenance / verification

## 1. The Diagnostic Philosophy
An SEO Audit is a **System Health Check**. We do not look for "tricks." We look for **blockers** (technical debt), **leaks** (lost authority), and **inefficiencies** (crawl budget waste).

**Hierarchy of Needs**:
1.  **Availability**: Is the system online and reachable?
2.  **Crawlability**: Can the bot traverse the graph?
3.  **Indexability**: Is the content allowed in the database?
4.  **Rankability**: does the content deserve to win?

## 2. Layer 1: The Technical Foundation (Infrastructure)

### Bottleneck: Crawl Budget & Directives
*   **Robots.txt**: Verify `Disallow` rules. Ensure critical API endpoints are NOT blocked if they render content.
*   **Sitemap.xml**:
    *   Is it current?
    *   Does it contain *only* 200 OK, Canonical URLs? (No redirects, no 404s in sitemap).
*   **Orphan Nodes**: Identify pages with 0 internal inbound links (The bot cannot find them).

### Bottleneck: Rendering & Performance (Core Web Vitals)
*   **LCP (Largest Contentful Paint)**: Must be < 2.5s.
*   **CLS (Cumulative Layout Shift)**: Must be < 0.1.
*   **INP (Interaction to Next Paint)**: < 200ms.
*   **Mobile Parity**: Does the Mobile render match the Desktop render 1:1? (Google indexes Mobile-First).

## 3. Layer 2: On-Page Signal Integrity

### Signal: The Topic Vector (Keywords)
*   **Title Tags**: Unique vector per page. No duplicates. Front-load the primary token.
*   **H1**: Single H1 per document. Structure valid HTML5 outline (H1 -> H2 -> H3).
*   **Cannibalization Check**: Are 2 pages fighting for the same intent? Merge or De-optimize one.

### Signal: The Meta-Data
*   **Meta Description**: Not a ranking factor, but a *CTR factor*. Must act as "Ad Copy" for the SERP.
*   **Canonicals**: The most critical tag.
    *   Self-referencing canonical on original content?
    *   Correct pointer on duplicate/parameterized URLs?

## 4. Layer 3: Content Quality (E-E-A-T)

### The Credibility Check
*   **Authorship**: Is there a clear `Byline` linked to a Bio?
*   **Sourcing**: Are claims cited (outbound links)?
*   **Depth**: Does the content answer the "Next Reasonable Question"?

### The 'Thin Content' Purge
Identify "Zombie Pages" (0 traffic, 0 value) and apply the **R.I.P. Protocol**:
1.  **Redirect (301)**: If a better version exists.
2.  **Improve**: If the topic is valuable but executed poorly.
3.  **Prune (410)**: If the page serves no purpose. Delete it to save Crawl Budget.

## 5. Layer 4: Data-Driven Optimization (The GSC Lever)

### The "Striking Distance" Protocol
Mining GSC for Pos 8-20 queries is the highest-ROI activity an expert can perform.
1.  **Extract**: Identify pages with high impressions but low CTR due to position.
2.  **Align**: Update Title/H1 with latent queries Google already associates with the page.
3.  **Harden**: Implement the **Direct Answer (GEO)** at the top of the content.

### Semantic Network Integrity
*   **Internal Link Ratios**: Aim for 1 link per 50 words to create a "Trust Skeleton."
*   **Anchor Relevance**: Ensure anchor text matches the *Entity* of the target page exactly.

## 6. Security & Trust
*   **HTTPS**: Non-negotiable. Check for "Mixed Content" warnings.
*   **HSTS**: Enforce strict transport security.

## 6. The Output: The Remediation Plan
Do not just "list errors." Group them by **Impact vs. Effort**.

*   **P0 (Critical)**: Blocking Indexation (e.g., accidental `noindex`). Fix: Immediate.
*   **P1 (High)**: Performance Failures (CWV), Broken Links (404s). Fix: This Sprint.
*   **P2 (Medium)**: Title Tag optimization, Content expansion. Fix: Next Sprint.
*   **P3 (Low)**: Minor warnings, alt text missing. Fix: Backlog.
