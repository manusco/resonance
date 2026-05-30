# GitHub Repository SEO & Discoverability Guide

A GitHub repository is a product. Its visibility is governed by search engine algorithms (Google) and internal platform algorithms (GitHub Search/Trending).

## 1. Repository Metadata Optimization

### The README.md (The Landing Page)
- **H1**: Must contain the repository name and a clear, 3-word description of what it does.
- **Above the Fold**: The first paragraph must define: What is it? Who is it for? Why use it over the alternative?
- **Badges**: Use status, license, and CI/CD badges. They provide visual trust signals.
- **TOC**: Always include a Table of Contents for repositories with > 500 lines of documentation.

### The Repository "About" Section
- **Description**: 1-2 concise sentences. Do not use generic terms ("A tool for..."). Use action verbs ("Deploy serverless apps...").
- **Website**: Always link back to the documentation site or marketing page.
- **Topics**: You must max out relevant topics (up to 20). Use a mix of broad (`python`, `cli`) and hyper-specific (`aws-lambda`, `cost-optimization`) tags.

## 2. Community Health Signals (E-E-A-T)
GitHub search heavily weights community engagement.
- **Stars/Forks**: Primary velocity metrics.
- **Issue/PR Resolution**: Repositories with high open-to-close ratios for issues rank higher than abandoned ones.
- **CONTRIBUTING.md**: A clear contribution guide signals project maturity.
- **SECURITY.md**: Required for enterprise trust.

## 3. SEO for Documentation Sites
If using GitHub Pages, Docusaurus, or Nextra for documentation:
- **`robots.txt` & `sitemap.xml`**: Ensure they are generated and submitted to Google Search Console.
- **Clean URLs**: Avoid hash-based routing (`/#/docs`). Use clean paths (`/docs/getting-started`).
- **Canonical Tags**: If you publish tutorials on Medium/Dev.to, always point the canonical tag back to your repository's documentation site.

## 4. LLM Discoverability (`llms.txt`)
AI agents and LLMs crawl GitHub differently.
- Provide an `llms.txt` file at the root of your documentation.
- Provide a clean, markdown-only summary of your API surface so agents can ingest it without parsing complex UI elements.
