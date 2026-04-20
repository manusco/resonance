# LLMs.txt Protocol (Agent-First Documentation)

> "The future of documentation is reading by machines, not humans."

## 1. The Purpose

To allow AI agents (like me) to instantly understand a library or API without scraping HTML.

## 2. The Format

File: `/public/llms.txt` (or `/llms.txt` in root).

```markdown
# [Project Name]

> [Short Description]

## Documentation Links

*   [Getting Started](https://example.com/docs/start)
*   [API Reference](https://example.com/docs/api)
*   [Concepts](https://example.com/docs/concepts)

## Core libraries
*   [Hono](https://hono.dev) - routing
*   [Drizzle](https://orm.drizzle.team) - database
```

File: `/public/llms-full.txt` (Optional).
*   Contains the **entire documentation** concatenated into a single Markdown file.
*   Optimized for "Context Window Stuffing".

## 3. The Mandate

**For every Open Source Project or Public API you build:**
1.  You MUST generate an `/llms.txt`.
2.  You MUST strip all "Marketing Fluff" from it.
3.  Focus on **Types**, **Inputs**, **Outputs**, and **Examples**.

> 🔴 **Rule**: If an Agent can't curl it and understand it in 1 second, your docs are broken.
