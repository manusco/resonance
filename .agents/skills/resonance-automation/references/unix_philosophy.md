# Unix Philosophy Protocol

> "Write programs that do one thing and do it well."
> — Doug McIlroy

## 1. The 3 Tenets

1.  **Modularity**: Write simple parts connected by clean interfaces.
2.  **Composition**: Write programs that work together.
3.  **text-streams**: Write to handle text streams, because that is a universal interface.

## 2. The Agent Application

*   **Bad Tool**: `manage_project` (Does Git, JIRA, and Slack).
*   **Good Tools**:
    *   `git_commit`
    *   `jira_update`
    *   `slack_notify`
*   **Why?**: The Agent can compose small tools (Chain of Thought). It fails at giant tools.

## 3. The Input/Output Mandate

*   **Inputs**: Must be JSON Schema validated.
*   **Outputs**: Must be structured text (Markdown or JSON) that an LLM can parse easily.
    *   ❌ Output: A binary blob.
    *   ✅ Output: "Success: File created at /tmp/foo.txt"

> 🔴 **Rule**: If your tool needs more than 5 arguments, splits it.
