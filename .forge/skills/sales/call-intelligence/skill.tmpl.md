---
name: resonance-sales-call-intelligence
description: Analyzes sales call transcripts to extract deep persona insights, objection handling metrics, vocabulary libraries, and feature requests. Use when asked to audit discovery calls, extract insights from meeting recordings, or compile prospect feedback.
archetype: procedure
---

# /resonance-sales-call-intelligence: analyze sales transcripts

> **Role:** resonance-frontend
> **Input:** Sales call transcripts (pasted text, CSV, or MCP connections).
> **Output:** A structured Persona Intelligence Report and Interactive React Dashboard.
> **Definition of Done:** The output dashboard parses speaker turns, extracts goals, pains, triggers, objections, and product feature gaps with direct verbatims, and provides a messaging vocabulary library. Free of AI slop and em dashes. Passed the validator.

## Prerequisites (fail fast)

- [ ] Transcripts or call recordings are available for analysis.
- [ ] You have identified if speaker attribution (rep vs. prospect) is present or needs auto-inference.

## Algorithm

Copy this checklist and tick items as you go.

1. **Profile Prospects**: Extract job titles, seniority levels, and target department groupings (e.g., C-Suite, VP, Manager). → verify: dataset confidence level is declared at top.
2. **Ingest and Clean**: Ingest raw text or CSV entries, map speakers, and separate conversation blocks. → verify: transcript source type is declared.
3. **Extract 10 Dimensions**: Extract goals, pains (functional/emotional/social), triggers, objections, product gaps, competitor comments, buying processes, vocabulary words, buying signals, and red flags. → verify: all quotes are extracted exactly as spoken.
4. **Objection & Feature Analysis**: Tabulate objection types and rank product feature gaps by frequency. → verify: objection handling is rated as Effective, Neutral, or Missed.
5. **Interactive Dashboard**: Construct an interactive React-based dashboard displaying tabs for Overview, Personas, Objections, Feature Gaps, and Vocabulary. → verify: contains a bar chart representing objection frequency.

## Recovery

- Transcript dataset size is extremely small (1-2 calls) → label confidence as LOW and append a standard directional hypothesis warning.
- Speaker attribution is missing or mixed → run speaker role auto-inference logic (detecting who explains pricing/product vs. who highlights constraints) before continuing.
- Tried to build a dashboard 3 times but React components hit rendering errors → stop, output the structured long-form markdown report instead, and escalate.

{{RESOLVER:decision_brief}}

{{RESOLVER:completion}}

{{RESOLVER:voice}}

{{OVERLAY}}
