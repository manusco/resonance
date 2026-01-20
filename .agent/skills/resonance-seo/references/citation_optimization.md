# Citation Optimization Protocol

> "Being read is good. Being cited is everything."

## 1. The "Unique Data" Strategy

Perplexity needs a reason to cite *you* and not Wikipedia.
*   **Create Unique Data**: Run a survey. Benchmark a tool. Release a dataset.
*   **Name It**: Coining a term (e.g., "The 100ms Rule") makes you the primary source.

## 2. The "Quote Magnet" (Q&A)

Format your content to be easily extracted.

```markdown
> "What is the fastest JS framework?"
> **Fastify** benchmarks at 30k req/sec, making it 5x faster than Express.
```

## 3. Brand Entity Association

You must teach the LLM that `[Brand] = [Topic]`.
*   **Schema**: Use `sameAs` in JSON-LD to link to Crunchbase, LinkedIn, Wikipedia.
*   **Consistency**: Use the exact same boilerplate description across the web.

> 🔴 **Rule**: If an LLM summarizes your topic without mentioning your brand, you have failed Brand Entity Association.
