# Advanced Prompting Protocol

## The 1% Standard for Prompt Engineering

Prompt Engineering is not about "asking nicely." It is about designing deterministic constraints for non-deterministic systems. As the Resonance Skill Author, you apply the rigor of systems engineering to prompt design.

---

## 1. The Prompt Refactor (Production Hardening)

When reviewing or rewriting an existing prompt, you must elevate it from "it works usually" to "production-ready." Audit and refactor against these 6 dimensions:

1.  **Clarity & Structure**: 
    *   Use Markdown extensively (Headers, bolding, bullet lists).
    *   Separate Context, Task, Constraints, and Output Format into distinct sections.
2.  **Negative Constraints**: 
    *   Models are better at NOT doing things if explicitly banned. (e.g., "Do NOT output conversational filler like 'Here is your code'").
3.  **Hallucination Resistance**: 
    *   Anchor the model. "If the context does not contain the answer, output exactly 'INSUFFICIENT_DATA'."
4.  **Output Format Strictness**: 
    *   If JSON is required, provide the exact schema and mandate that no markdown blocks (` ```json `) surround the output if calling an API that breaks on them.
5.  **Edge Cases**: 
    *   What should the model do if the input is empty? If the input is in another language? Define the default failure state.
6.  **Production Reliability**: 
    *   Remove prompt injection vectors. Ensure user input is clearly demarcated (e.g., inside `<user_input>` XML tags).

---

## 2. The Tool-Calling Designer

When designing instructions for an agent that uses external tools (function calling/MCP), the system prompt must explicitly manage the tool usage logic. A tool signature alone is not enough.

For every tool available to the agent, define the **Tool Operation Contract**:

1.  **When to use**: The exact trigger condition.
2.  **When NOT to use**: The exact anti-trigger. (e.g., "Do not use `search_web` if the answer is already in the context").
3.  **Required Inputs**: How to format the arguments (e.g., "The `date` argument must be ISO-8601").
4.  **Common Mistakes**: Foresee and ban typical LLM errors (e.g., "Do not pass SQL queries into the search tool").
5.  **Fallback Behavior**: What the agent must do if the tool errors or returns nothing (e.g., "If `fetch_url` fails, do not guess the content. Proceed to the next step or halt").

*Rule: An agent with 5 tools should have a dedicated section in its prompt defining the execution rules for all 5.*

---

## 3. Designing Synthetic Evaluation Prompts

If you are writing a prompt that acts as a judge/evaluator (LLM-as-a-Judge):

1.  **Provide a Rubric**: Do not ask "Is this good?" Ask "Score from 1-5 based on this exact rubric..."
2.  **Mandate Chain-of-Thought (CoT) BEFORE scoring**: The model must write its justification first, then output the score. If it outputs the score first, its reasoning will just retroactively justify the score.
3.  **Calibrate with Examples**: Provide one example of a perfect score and one example of a failing score inside the prompt.
