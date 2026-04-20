# Chain of Thought (CoT) Protocol

> "If you don't ask the model to think, it will guess."

## 1. The Magic Phrase

**"Let's think step by step."**

## 2. The Structure

When prompting for complex logic, you MUST force the model to output a `thought` block before the `answer`.

### Example (React Component)

**Bad Prompt:**
"Write a React Component for a Signup Form."

**Good Prompt (CoT):**
"Create a React Component for a Signup Form.
First, outline the state management (Zod schema).
Second, design the layout (Tailwind).
Third, write the code.
Finally, write the test."

## 3. The XML Wrapper

For System Prompts, use XML tags to force thinking:

```xml
<thinking>
Analyze the user's request.
Identify edge cases.
Plan the execution.
</thinking>
<response>
[The actual code]
</response>
```

> 🔴 **Rule**: Never ask a model to "Just code it". Ask it to "Plan then code".
