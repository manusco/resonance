# RAG Architecture

> "RAG has two halves that fail independently. Most 'the model is dumb' bugs are a retrieval problem."

Retrieval-Augmented Generation grounds a model in your data: fetch relevant text, put it in the context, answer from it. It exists because models do not know your private data and will invent an answer rather than admit ignorance. RAG replaces invention with citation. It only works if the right facts reach the model.

## Contents
- The pipeline
- Retrieval and generation are separate systems
- Chunking
- Embedding and retrieval
- Reranking
- Grounding the answer
- Diagnosing a broken pipeline
- When RAG is the wrong tool

## 1. The Pipeline

```
Documents -> Chunk -> Embed -> Store (vector index)
                                    |
Query -> Embed -> Retrieve (top-k) -> Rerank -> Assemble context -> Generate -> Answer
```

Two phases: indexing (offline, one time per document) and retrieval+generation (per query). Every stage can silently degrade the final answer.

## 2. Retrieval And Generation Are Separate Systems

This is the core mental model. Measure each half on its own:

- **Retrieval quality**: did the right chunks come back? Metric: recall at k. If the answer is not in the retrieved chunks, no prompt can save you.
- **Generation quality**: given the right chunks, did the model answer correctly and faithfully? Metric: faithfulness (every claim traceable to a chunk) and answer relevance.

If you only look at the final answer, you cannot tell which half failed, so you fix the wrong thing. Always split the diagnosis.

## 3. Chunking

How you cut documents determines what can be retrieved.

- **Too large**: chunks contain the answer plus noise; embeddings blur; the relevant span gets diluted.
- **Too small**: chunks lose the context that makes them meaningful; the answer is split across chunks that do not co-retrieve.
- **Start**: a few hundred tokens with a modest overlap, then tune against retrieval recall.
- **Respect structure**: split on section and paragraph boundaries, not mid-sentence. Keep tables and lists intact.
- **Attach metadata**: source, section title, date. It powers filtering and citation.

## 4. Embedding And Retrieval

- **Embeddings encode meaning**: similar text lands near in vector space. Semantic search finds "refund window" when the user typed "how long to return".
- **Pure vector search misses exact terms**: product codes, names, acronyms. Combine vector search with keyword (hybrid search) so exact matches are not lost.
- **Query and documents must use the same embedding model**: mixing models makes distances meaningless.
- **top-k is a tradeoff**: too few risks missing the answer, too many floods the context with noise and cost. Retrieve wider, then rerank down.

## 5. Reranking

Retrieval optimizes for speed over a huge corpus, so its ranking is rough. A reranker re-scores the top candidates for true relevance to the query.

- Retrieve top 20 to 50 cheaply, rerank to the best 3 to 5.
- This is often the single most effective fix for "the right chunk was retrieved but ranked 15th and dropped".
- The reranked few go into the context; the rest are discarded.

## 6. Grounding The Answer

Retrieval is pointless if the model ignores the chunks or adds facts of its own.

- **Instruct explicitly**: "Answer only from the provided context. If the context does not contain the answer, say you don't know."
- **Require citation**: have the model point to the chunk that supports each claim. Uncited claims are suspect.
- **Reject the ungrounded**: an answer that cannot be traced to a retrieved chunk is a hallucination, even if it sounds right.
- **Handle empty retrieval**: if nothing relevant came back, the answer is "I don't know", not a guess from parametric memory.

## 7. Diagnosing A Broken Pipeline

"RAG returns wrong answers." Isolate before you fix:

1. **Inspect the retrieved chunks for a failing query.** Was the correct chunk present?
2. **If the chunk was NOT retrieved**: this is a retrieval bug. Suspects, in order: chunking (answer split or diluted), embedding (wrong model, no hybrid search for an exact term), top-k too small, missing metadata filter.
3. **If the chunk WAS retrieved but ranked low and dropped**: add or fix reranking, or raise k.
4. **If the chunk was retrieved and present in context but the answer is still wrong**: this is a generation bug. Suspects: weak grounding instruction, lost-in-the-middle (chunk buried), the model overriding context with its own prior, or an ambiguous chunk.
5. **Confirm with the split metrics**: retrieval recall isolates half one, faithfulness isolates half two.

Do not change the model when the bug is in chunking. Do not re-chunk when the bug is a missing grounding instruction.

## 8. When RAG Is The Wrong Tool

- The knowledge is small and static: put it directly in the prompt. No vector DB needed.
- The task needs reasoning over the whole corpus, not a few passages: RAG's top-k retrieval will not see enough.
- The data changes per user and per request: a database query or tool call may be the right retrieval, not semantic search.
- You need exact, structured lookups (a user's order status): call the API. Do not embed a database you can query precisely.
