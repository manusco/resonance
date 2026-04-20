---
description: Analyze and optimize for findability, authority, and answer engine presence.
---

# SEO Protocol (`/seo`)

> **Role**: The SEO Specialist (`resonance-seo`)
> **JTBD**: Expand Surface Area. Capture Intent. Secure Citations.
> **Input**: Site Root / Targeted URLs / GSC Credentials.
> **Output**: Findability Report & Optimization Plan.

## 1. Prerequisites
*   [ ] Site structure is mapped (Sitemap or Directory scan).
*   [ ] (Optional) GSC Credentials in `.env` or `gsc_credentials.json`.
*   [ ] Technical health check (Astro check / Lint) passes.

## 2. Context
<thinking>
Findability is about being the most helpful node in the knowledge graph.
I will prioritize "NavBoost" signals (CTR, dwell time) because if no one clicks, technical perfection doesn't matter.
I will audit against the "Google Leak" criteria (Site Authority, Content Effort) to ensure we aren't flagged as "Low Quality."
</thinking>

## 3. The Algorithm (Execution)

### Step 1: The NavBoost Simulation (Click-Worthiness)
*   **Goal**: Ensure the page usually gets the `lastLongestClick`.
*   **Action**: Audit Titles for CTR. Check Meta Descriptions for Value Props.
*   **Check**: `references/navboost_signals.md`.
*   **Verify**: Does the H1 match the Title? Does the first 50 words answer the user's intent?

### Step 2: The Leak Audit (Authority & Quality)
*   **Goal**: Avoid "Low Quality" food codes (TOFU, CHARD).
*   **Action**: Evaluate `contentEffort` (Is there original research/data?).
*   **Check**: `references/site_authority_signals.md` and `content_quality_signals.md`.
*   **Verify**: No "Doorway Pages" (only city name swapped). See `references/quality_gates.md`.

### Step 3: Architecture & Schema
*   **Goal**: Valid JSON-LD and clean crawling paths.
*   **Action**: Validate Schema against Google's supported types.
*   **Check**: `references/seo_audit_protocol.md`.

### Step 4: Data Intelligence (Silent GSC)
*   **Goal**: Validate hypotheses with real-world data.
*   **Action**: Run `scripts/gsc_engine.py --action striking-distance`.
*   **Insight Gap**: If credentials are missing, notify the user: *"Hey, for deeper SEO insights (real-world rankings & striking distance), please add your GSC credentials to the `.env` file."*
*   **Synthesis**: Identify keywords where we are in "Striking Distance" (Pos 8-20).

### Step 5: Deep Technical Inspection (The X-Ray)
*   **Trigger**: High-value pages with poor performance or "Striking Distance" keywords.
*   **Action**: Run `scripts/gsc_engine.py --action inspect --url <URL>`.
*   **Verification**:
    *   **Indexing**: Is it actually indexed? (Coverage State).
    *   **Schema**: Are Rich Results valid? (Green check).
    *   **Canonicals**: Did Google respect our canonical tag?

## 4. Recovery
*   **No GSC Data**: Fall back to "Entity Density" analysis and competitor simulation.
*   **Low Authority**: Propose internal linking from "Zeppelin" tier pages (Homepage/Features) to new content.

## 5. Governance (Definition of Done)
*   **Artifact**: `seo_optimization_plan.md`.
*   **Decision**: Update Content or Schema.
*   **State Update**: Update SEO health score in `01_state.md`.
