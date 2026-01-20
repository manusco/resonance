# Model Context Protocol (MCP) Standards

> "Standardize the interface between AI and the World."

## 1. The Core Primitives

1.  **Resources**: Passive data (Files, Logs, Database Rows).
    *   Must be readable via `read_resource`.
2.  **Tools**: Active functions (Execute Code, Search Web).
    *   Must be executable via `call_tool`.
3.  **Prompts**: Canned instructions (Templates).
    *   Must be retrievable via `list_prompts`.

## 2. The JSON-RPC Mandate

All tools must speak JSON-RPC 2.0.

*   **Request**: `{ "method": "tools/call", "params": { ... } }`
*   **Response**: `{ "result": { "content": [ { "type": "text", "text": "..." } ] } }`

## 3. Error Handling

*   **Never Crash**: Return a JSON error.
*   **Helpful Messages**:
    *   ❌ `Error: 500`
    *   ✅ `Error: File not found. Did you mean 'script.py'?`

> 🔴 **Rule**: Review the [Official MCP Specification](https://modelcontextprotocol.io) before publishing.
