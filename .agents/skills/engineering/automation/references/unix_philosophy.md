# Unix Philosophy Protocol

> "Write programs that do one thing and do it well."
> - Doug McIlroy

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

*   **Inputs**: Validate untrusted inputs at the boundary with the project's existing schema or validation stack.
*   **Outputs**: Match the caller. Use structured text or a schema when a person, script, or model needs to inspect or consume the result.
    *   ❌ Output: A binary blob.
    *   ✅ Output: "Success: File created at /tmp/foo.txt"

> 🔴 **Prompt**: More than five arguments may signal that the job or interface needs review; split only when separate owners or callers benefit.
