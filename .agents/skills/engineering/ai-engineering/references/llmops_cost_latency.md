# LLMOps: Cost And Latency

> "Cost and latency are decisions you make on purpose, not surprises on the invoice."

An LLM feature that ignores cost and latency works in the demo and dies in production: too slow for users, too expensive to run. Both are controllable with a handful of levers. Decide the budget, then build to hit it, then measure it in production.

## Contents
- Model selection: smallest sufficient
- Caching
- Routing
- Latency levers
- Token discipline
- Observability and budgets
- Common mistakes

## 1. Model Selection: Smallest Sufficient

The largest model is the lazy default and the expensive one. Cost and latency scale hard with model size.

- **Start cheap**: pick the smallest, fastest model that could plausibly pass your eval.
- **Run the eval**: if it passes, you are done. You just saved most of the cost.
- **Move up only on a fail**: let the eval force the upgrade, not a hunch.
- **Match model to subtask**: classification and extraction rarely need a frontier model. Reserve the big model for the genuinely hard reasoning step.
- **Consider open models for high volume**: at scale, a self-hosted smaller open model can beat per-token API pricing. This is a cost calculation, not a religion. (Serving that model is devops' job; choosing it is yours.)

## 2. Caching

The cheapest model call is the one you do not make.

| Cache type | Hits when | Use for |
| :--- | :--- | :--- |
| **Exact** | Identical input seen before | Repeated queries, idempotent lookups |
| **Semantic** | A near-duplicate query (by embedding) | FAQ-style traffic with reworded questions |
| **Prompt/context cache** | A large static prefix is reused | Long system prompts, fixed few-shot, shared context across calls |

- Exact caching is free money for repeated inputs. Do it first.
- Prompt caching cuts the cost of a big unchanging prefix that rides along on every call. Structure the prompt so the static part is cacheable.
- Semantic caching needs a similarity threshold you tune, and a check that a "near" match is actually the same intent.

## 3. Routing

Not every request needs your best model. Route by difficulty.

- A cheap classifier (or a rule) decides: easy request to the small model, hard request to the large one.
- Most traffic is easy. Routing the easy majority to a cheap model is often the biggest single cost cut.
- Fall back up on low confidence: if the small model's output fails a check, retry on the larger one. You pay the premium only for the cases that need it.

## 4. Latency Levers

Perceived speed and actual speed are different problems. Attack both.

- **Stream the output**: tokens appear as generated. Time-to-first-token is what users feel; streaming makes a 4-second response feel responsive.
- **Cap output tokens**: generation time scales with output length. A tight max cuts both latency and cost.
- **Smaller model, lower latency**: model size drives speed. The right-sizing from section 1 is also a latency lever.
- **Parallelize independent calls**: if a request needs three unrelated model calls, run them concurrently, not in series.
- **Cut round trips**: an agent's multi-step loop multiplies latency. A workflow or a single call is faster where it fits.
- **Retrieve less, rank better**: a smaller, reranked context generates faster than a bloated one.

## 5. Token Discipline

You pay per token, in and out, on every call. Trim relentlessly.

- **Prune the context**: send the relevant span, not the whole document. Summarize old conversation turns instead of carrying the full transcript.
- **Right-size few-shot**: two good examples often match five. Every example is input tokens on every call.
- **Bound output**: set max output tokens deliberately.
- **Watch the input side**: input tokens are usually the larger, quieter cost. A bloated system prompt taxes every single request.

## 6. Observability And Budgets

You cannot control what you do not measure. The demo tells you nothing about production cost.

- **State the budget up front**: cost-per-request ceiling and a P95 latency target, chosen deliberately.
- **Measure in production**: log tokens in/out, cost, and latency per request. Track P50 and P95, not just the average, the tail is what hurts users.
- **Attribute cost**: know which feature, model, and request type spends what. You cannot cut a cost you cannot locate.
- **Alert on drift**: a prompt change that quietly doubles token use should page you, not surprise you at month end.
- **Watch cache hit rate**: a falling hit rate silently raises cost.

## 7. Common Mistakes

- **Defaulting to the biggest model**: expensive and slow for tasks a small model passes.
- **No caching**: paying full price to answer the same question repeatedly.
- **Ignoring input tokens**: obsessing over output while a bloated prompt taxes every call.
- **Measuring only the average latency**: the P95 tail is the user who leaves.
- **No production cost telemetry**: the first time you learn the cost is the invoice. Instrument from day one.
- **Optimizing cost before it passes the eval**: a cheap wrong answer is worthless. Correct first, then cheap, without regressing the eval.
