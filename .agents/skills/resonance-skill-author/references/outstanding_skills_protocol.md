# Protocol: Outstanding Skills Mastery

> **Status**: Core Implementation Standard
> **Objective**: Implement peak-performance agent capabilities through structural and prompt engineering excellence.

## 1. The Skill Constitution

A world-class skill is not just a prompt; it is a discrete piece of system intelligence.

### Structural Integrity & Progressive Disclosure
*   **The 3-Level Model**:
    1. **Metadata (name + description)**: Always in context (~100 words). Triggering mechanism.
    2. **SKILL.md body**: Loaded on trigger. Essentials only (<500 lines).
    3. **Bundled Resources**: `scripts/` (deterministic logic), `references/` (documentation), and `assets/` (templates/icons).
*   **XML Over Mentions**: Use XML tags (`<instructions>`, `<constraints>`, `<examples>`, `<context>`) to eliminate ambiguity.
*   **No Clutter**: Do NOT include `README.md`, `CHANGELOG.md`, or other meta-docs inside the skill folder.

---

## 2. Setting Degrees of Freedom

Match the constraint level to the task's fragility:

*   **High Freedom (Markdown instructions)**: Use for heuristics, creative tasks, or context-dependent logic.
*   **Medium Freedom (Pseudocode/Parameterized Scripts)**: Use when a preferred pattern exists but configuration varies.
*   **Low Freedom (Specific Scripts)**: Use for fragile, deterministic, or error-prone operations (e.g., PDF rotation, complex data migration).

## 3. Prompt Engineering Best Practices

### Concise is Key
*   **The Smart Agent Assumption**: Claude is already intelligent. Only add context it doesn't possess.
*   **Token Efficiency**: Challenge every paragraph: "Does this justify its token cost?"
*   **Imperative Form**: Use imperative/infinitive form for instructions.

### The Directive Hierarchy
1.  **Role**: Establish the expert persona.
2.  **Context**: Provide the frame of reference.
3.  **Task**: Define the clear, actionable directive.
4.  **Constraints**: Negative markers (Do NOT do X).
5.  **Output Format**: Explicitly define the response structure.

### The "Show, Don't Tell" Mandate (Few-Shot)
*   **Quality over Quantity**: Provide high-fidelity examples that cover edge cases.
*   **The Chain of Thought Inclusion**: Embed reasoning traces *inside* your examples to show Claude *how* to arrive at the conclusion.
*   **Negative Examples**: Include "How NOT to do it" examples to clarify boundaries for high-stakes tasks.

## 3. Evaluation & Testing (Verification)

### The Golden Dataset
*   Every skill must have a set of "Ground Truth" inputs and expected tool-call outputs.
*   **Model-Graded Eval**: Use a superior model (Sonnet 3.5+) to audit the performance of a skill's output relative to the protocol.

### Recovery Archetype
*   **Descriptive Errors**: Tools must return "Teacher-like" errors. Instead of `Error 404`, return `Error: File "/path/to/x" does not exist. Did you mean "/path/to/y"?`.
*   **Interpretation Loop**: Explicitly instruct Claude to interpret terminal/API errors and attempt recovery autonomously.

---

## 4. Constraint Optimization

Models follow "Negative Constraints" (Do NOT) more strictly than positive "vague" suggestions.
*   ❌ "Try to keep it short."
*   ✅ "Do NOT exceed 200 words. Do NOT use passive voice."

---
*Created by the Skill Author & Researcher agents. Enforcing the Outstanding Skills Standard.*
