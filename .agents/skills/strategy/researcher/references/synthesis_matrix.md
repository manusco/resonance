# Synthesis Matrix Protocol

> "Knowledge is not just gathering dots. It is connecting them."

## 1. The Matrix Format

When researching a topic (e.g., "Best Database for AI"), do NOT just list them. Create a Matrix.

| Theme / Feature | Source 1 (Postgres) | Source 2 (Pinecone) | Source 3 (Weaviate) | **Synthesis (The Insight)** |
| :--- | :--- | :--- | :--- | :--- |
| **Vector Search** | extension (pgvector) | Native | Native | Native works best for scale, but pgvector simplifies stack. |
| **Cost** | Cheap (Existing) | Expensive (SaaS) | Moderate | Use pgvector for MVP, Pinecone for Scale. |
| **Latency** | High | Low | Low | Scale demands specialized DB. |

## 2. The Mandate

*   **Never Summarize**: "Source A said X" is useless.
*   **Always Synthesize**: "Source A and B disagree on X because of Y."
*   **Identify Gaps**: "None of the sources mentioned Z."

## 3. The Output

Your research must conclude with a **Synthesis Statement**:
> "While Pinecone offers better performance, the operational overhead of a separate DB makes Postgres (pgvector) the superior choice for early-stage products."
