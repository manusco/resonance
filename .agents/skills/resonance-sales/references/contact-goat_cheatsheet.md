# Contact Goat CLI Reference

> **Context**: This is a tool-specific reference document for the `contact-goat-pp-cli` from the Printing Press library. It is kept here for reference if automated API-based enrichment is needed in the future. The core `resonance-sales` skill relies on native browser workflows rather than this CLI.

## Installation
```bash
npx -y @mvanhorn/printing-press install contact-goat --cli-only
```
Or via Go:
```bash
go install github.com/mvanhorn/printing-press-library/library/sales-and-crm/contact-goat/cmd/contact-goat-pp-cli@latest
```

## Auth Surfaces
1. **Happenstance Cookie**: Free monthly allocation (preferred automatically).
2. **Happenstance API Key**: Bearer token (costs credits). Use `--source api` to force.
3. **Deepline API Key**: Required for deep email enrichment (`DEEPLINE_API_KEY`).

## Notable Commands
*   `coverage <company>`: Who you know at a company, ranked by relationship strength.
*   `warm-intro <target>`: Mutual connections who could intro you.
*   `prospect <query>`: Fan-out search.
*   `waterfall <target> [--company X]`: Free-sources-first enrichment, falls through to Deepline.
*   `dossier <target>`: Unified profile.
*   `doctor`: Check CLI health and auth status.

## Agent Mode
Add `--agent` to any command for JSON output (`--json --compact --no-input --no-color --yes`).
Filter output with `--select <dotted.path>`.
