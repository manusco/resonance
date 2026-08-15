# Context Engineering

> "The prompt is a system you assemble, not a paragraph you write."

Context engineering is deciding what tokens enter the model, in what order, on every call. The model has no memory and no access to your data except what you put in the window. Everything it knows about this request, you handed it. Design that handoff.

## Contents
- The anatomy of a prompt
- Order matters: lost in the middle
- Instructions that hold
- Few-shot examples
- Token budgeting
- Structured output
- Common mistakes

## 1. The Anatomy Of A Prompt

A production prompt is layered, not a blob:

1. **System instructions**: role, task, rules, output format, what to refuse.
2. **Few-shot examples**: 1 to 5 input/output pairs showing the exact shape you want.
3. **Retrieved context**: the facts for this specific request (documents, records, prior turns).
4. **The user turn**: the actual input, placed last.

Keep these sections separated and labeled. The model follows structure. A wall of undifferentiated text invites it to blur instructions and data together, which is also how prompt injection sneaks in.

## 2. Order Matters: Lost In The Middle

Models attend most strongly to the beginning and end of the context and weakest to the middle. Bury a critical instruction or the key document in the middle of 30k tokens and the model will miss it.

- Put the most important instructions at the top or restate them at the bottom.
- In retrieval, put the highest-ranked chunk at the edges, not the center.
- Do not assume "it's in the context" means "the model used it". Long context is necessary, not sufficient. Verify with an eval.

More context is not more quality. Past a point, added tokens dilute attention and add cost. Give the model what it needs, not everything you have.

## 3. Instructions That Hold

- **Be specific and positive**: "Respond in at most 3 sentences" beats "don't be too long". Tell it what to do, not only what to avoid.
- **State the format explicitly**: if you want JSON, show the schema. If you want a refusal on out-of-scope input, say the exact refusal.
- **Put rules where they survive**: safety and format rules go in system instructions, above user-controlled text, so a user cannot easily override them.
- **One instruction per line**: dense, scannable, unambiguous.

## 4. Few-Shot Examples

Examples teach shape faster than description.

- Use them when the output format is specific, the task is subtle, or zero-shot is inconsistent.
- 1 to 5 is usually enough. Diminishing returns and rising cost after that.
- Cover the tricky cases: an edge input, a "none found" case, the format under pressure.
- Keep examples consistent with your rules. A contradictory example is worse than none.

## 5. Token Budgeting

Every token in the window is paid for on every call and eats into attention. Budget it.

- Allocate: how many tokens for instructions, examples, retrieved context, and the reserved output? Decide before you assemble.
- Compress retrieved context: summarize or extract the relevant span, do not paste whole documents.
- Preserve recovery paths: if a summary, compressed payload, or extracted span can affect a decision, keep a stable pointer to the original source and reopen it before final claims, edits, audits, or destructive actions.
- Trim history: for multi-turn, summarize old turns instead of carrying the full transcript forever.
- Cap output: set max output tokens so a runaway generation cannot blow the budget or the latency target.

## 6. Structured Output

When you need machine-readable output, do not hope for clean JSON.

- Specify the schema in the prompt and use the model's structured-output or tool-calling mode where available.
- Validate the parsed output against a schema. On failure, retry once with the error fed back.
- Prefer a flat, shallow schema. Deeply nested output is harder for the model to keep valid.

## 7. Common Mistakes

- **Dumping everything into context "just in case"**: pay more, attend less, hide the signal.
- **Trusting compressed context as evidence**: summaries are navigation aids, not source material. Decisions trace back to the original record.
- **Burying the key instruction in the middle**: it gets ignored. Top or bottom.
- **Mixing instructions and user data with no separation**: fragile and injectable.
- **Vague instructions**: "be helpful and accurate" is not a spec. Say the format, the length, the refusal.
- **Assuming retrieval success equals usage**: the chunk being present does not mean the model read it. Test the answer, not the pipeline stage.
