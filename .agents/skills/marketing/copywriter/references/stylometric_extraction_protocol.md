# Protocol: Stylometric Extraction & Voice Cloning
> **Focus**: Deconstructing written communication to its molecular level.
> **Resonance Phase**: Analysis / Emulation

## 1. The Strategy of Cognitive Archaeology
We do not just "copy" a style. We dismantle it. We reveal the hidden psychological architecture that creates influence, engagement, and memorability. Our goal is to extract a style so precisely that someone could write content virtually indistinguishable from the original author.

**The 6 Layers of Extraction**:
1. **Surface Patterns**: Formatting, punctuation, vocabulary, and sentence structure.
2. **Psychological Architecture**: Persuasion frameworks and emotional triggers used to anchor the reader.
3. **Subconscious Rhythms**: Pacing, flow, and musical qualities of the text.
4. **Linguistic Fingerprints**: Unique syntax and structural preferences that define the author.
5. **Influence Mechanisms**: How the style creates psychological impact (attention, engagement, behavioral influence).
6. **Replication Blueprint**: The actionable framework for recreating the exact style.

## 2. Context Discovery (The Initialization)
Before analyzing, define the environment and the target. A style never exists in a vacuum; it is shaped by its context.
1.  **Format Constraints**: What is the medium? (e.g., 280 characters, long-form sales letter, thread).
2.  **Audience State**: Who is the intended reader, and what is their Sophistication/Awareness level?
3.  **Core Intent**: What is the text trying to achieve? (Educate, Agitate, Entertain, Convert).

## 3. The Extraction Framework (The Output Schema)
To ensure the profile is deterministic and usable by generation agents, output the analysis as a strict JSON or YAML configuration object covering:

*   **style_metadata**: `content_type`, `sample_size_analyzed`, `confidence_score`.
*   **surface_heuristics**:
    *   `vocabulary_complexity` (e.g., Flesch-Kincaid read level).
    *   `formatting_rules` (e.g., "one-sentence paragraphs for emphasis").
    *   `punctuation_quirks` (e.g., heavy use of em-dashes `—` instead of commas).
*   **rhythm_and_flow**:
    *   `sentence_length_variance` (Burstiness - mix of short punchy sentences vs long explanatory ones).
    *   `paragraph_density` (Average words per visual block).
*   **psychological_architecture**:
    *   `primary_framework` (e.g., PAS, StoryBrand).
    *   `dominant_emotion` (e.g., Urgency, Relief, Intellectual Superiority).
    *   `influence_triggers` (e.g., Authority, Social Proof).
*   **voice_personality**: `character_archetype`, `core_values`, `tone_descriptors`.
*   **replication_blueprint**:
    *   `do_always` (Mandatory stylistic rules and structural habits).
    *   `do_never` (The author's implicit Taboo list—the exact terms and habits they actively avoid).

## 4. Quality Standards (The Linting)
Every extracted pattern must pass the **Evidence Test**. If you claim a pattern exists, you must prove it.

*   **Traceable**: Every claim in the `replication_blueprint` MUST be paired with a `source_quote` from the text.
*   **Quantitative**: Use metrics when possible. Instead of "uses short sentences," state "Average Sentence Length: 6 words. Shortest: 2 words."
*   **Actionable**: Rules must be enforceable. "Sound smart" is useless. "Use high-context industry terminology without defining it" is actionable.
*   **Negative Constraints**: Identifying what the author *excludes* (e.g., "Never uses adverbs," "Never uses emojis") is often more revealing than what they include.
*   **Consistent**: Validated across multiple samples to avoid overfitting to a single anomalous piece of text.

> 🔴 **Rule**: If a stylistic instruction cannot be programmed into an LLM system prompt deterministically, the extraction has failed. Do not assume; prove it with the text.
