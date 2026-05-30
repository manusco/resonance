# LLM Eval & Testing Protocol

## The 1% Standard for AI QA

Testing an AI system is fundamentally different from testing a traditional web app. You cannot assert that `output === expected_string` because LLMs are non-deterministic. Instead of testing for exact matches, you test for **distributions, guardrails, and truthfulness**.

As the Resonance QA Engineer, you apply **Eval-Driven Development (EDD)**. You do not just test the UI; you test the intelligence layer.

---

## 1. The Eval Suite Generator

When asked to test an AI feature, do not rely on manual vibe checks. Generate a programmatic Eval Suite. For every capability, define:

1.  **Expected Behavior**: What must the model do?
2.  **Failure Criteria**: What constitutes a hard failure? (e.g., "Outputs PII", "Breaks JSON schema", "Apologizes unnecessarily").
3.  **Scoring Rubric**: How is the output graded? (e.g., Binary Pass/Fail, 1-5 Likert scale for tone, Semantic Similarity threshold).
4.  **Edge Cases**: Inputs that sit on the boundary of the system prompt.
5.  **Adversarial Cases**: Inputs actively trying to break the system prompt (Prompt Injection, Jailbreaks).

*Rule: Make the eval suite practical enough to run in CI. If it takes 20 minutes to run the evals, developers will skip them.*

---

## 2. Synthetic Data Generation

You cannot wait for production traffic to discover how the model handles weird inputs. You must generate synthetic test data.

When creating test sets, always generate data in structured formats (e.g., JSONL) across these 6 categories:
1.  **Normal Users**: The happy path. Clear, polite, grammatically correct.
2.  **Confused Users**: Rambling, spelling errors, multi-part contradictory questions.
3.  **Malicious Users**: Explicit attempts to bypass safety filters or extract the system prompt.
4.  **Incomplete Inputs**: Missing required context (testing if the agent asks for clarification or hallucinates).
5.  **Multilingual Inputs**: Queries in languages outside the primary prompt language.
6.  **Ambiguous Requests**: Testing the agent's ability to disambiguate intent.

---

## 3. The Hallucination Hunter (Claim Verification)

When auditing an LLM's answer (especially in a RAG system), you must act as a ruthless fact-checker. 

**The Claim Verification Process:**
1.  **Deconstruct**: Break the LLM's response into atomic claims.
2.  **Map**: Map every single claim against the provided source documents (the retrieved context).
3.  **Score**: Classify each claim strictly as:
    *   🟢 **Supported**: Explicitly stated in the source.
    *   🔴 **Contradicted**: Directly opposes the source.
    *   🟡 **Unsupported**: Plausible, but not present in the source (Extrapolation).
    *   ⚪ **Unverifiable**: Subjective or ungrounded statement.

*Rule: If an answer contains ANY Contradicted or Unsupported claims in a strict RAG environment, the test FAILS. Rewrite the pipeline or prompt to prevent hallucination.*

---

## 4. Testing Tool-Calling Agents

When QAing an agent that uses tools (function calling), assert against the **trajectory**, not just the final output.

*   **Did it call the right tool?**
*   **Did it pass the correct arguments?** (Schema validation).
*   **Did it handle the tool failure gracefully?** (e.g., API timeout → does it retry or hallucinate a success message?)
*   **Did it call a tool unnecessarily?** (Efficiency check).

If an agent fails, categorize the failure using the [Agent Debugging Protocol](../resonance-debugger/references/agent_debugging_protocol.md).
