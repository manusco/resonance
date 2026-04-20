# Generative Engine Optimization (GEO) Protocol

> "Google Search is dead. Long live the Answer Engine."

## 1. The Direct Answer (The Snippet Winner)

LLMs crave structure. To win the "AI Overview", you must provide the answer immediately.

*   **The Format**: `[Question Rephrase] + [Direct Answer (Bold)] + [Nuance]`.
*   **Example**: "**What is the best database for vectors?** **Pinecone** is the industry standard for managed vector databases, offering low latency and high scalability."
*   **Location**: The first `<p>` tag after the `<h1>`.

## 2. The Token Economy (Conciseness)

LLMs have attention spans. Fluff gets ignored.
*   ❌ "In today's modern era of technology, it is important to consider..." (0 Value).
*   ✅ "Vector databases optimize high-dimensional search." (High Information Density).
*   **Rule**: Reduce word count by 30%. Increase fact count by 50%.

## 3. The "Statistics" Hook

LLMs trust numbers.
*   **Pattern**: "According to [Study], 80% of..."
*   **Action**: Include a Data Table (`<table>`) in every post. LLMs love parsing tables for comparisons.

> 🔴 **Rule**: If you don't answer the user's question in the first 50 words, the AI will ignore you.
