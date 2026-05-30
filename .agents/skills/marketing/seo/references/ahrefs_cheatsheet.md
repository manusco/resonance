# Ahrefs CLI Reference

> **Context**: Tool-specific reference for `ahrefs-pp-cli`. Kept here for automated API SEO tasks if needed. The core `resonance-seo` skill relies on the mental models of keyword gaps and SERP trajectories.

## Installation
```bash
npx -y @mvanhorn/printing-press install ahrefs --cli-only
```

## Notable Commands
*   `keywords-explorer matching-terms` / `overview`: Keyword research.
*   `site-explorer organic-competitors` / `organic-keywords`: Content gap analysis.
*   `site-explorer backlinks-stats`: Link building targets.
*   `rank-tracker serp-overview`: Monitor SERP volatility.
*   `site-audit issues`: Technical SEO crawling.

Add `--agent` to any command for JSON output. Filter with `--select`.
