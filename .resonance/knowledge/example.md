---
summary: Example knowledge document demonstrating frontmatter protocol
read_when:
  - creating new knowledge documents
  - learning the Resonance framework
  - setting up documentation structure
last_updated: 2026-01-01
---

# Knowledge Document Template

This is an example of a properly formatted knowledge document in the Resonance framework.

## Frontmatter Fields

### Required Fields

**`summary`**: A brief, one-line description of what this document contains. This helps both humans and AI agents quickly understand the purpose of the document.

### Recommended Fields

**`read_when`**: An array of trigger conditions that indicate when this document should be consulted. These are context-based hints that help determine relevance.

Examples of good `read_when` triggers:
- "modifying authentication flows"
- "adding new API endpoints"
- "debugging database queries"
- "updating deployment configuration"
- "refactoring component architecture"

### Optional Fields

**`last_updated`**: ISO date (YYYY-MM-DD) of the last significant update to this document. Helps track staleness.

## Best Practices

1. **Keep summaries concise**: One line, under 100 characters
2. **Make triggers specific**: Avoid vague conditions like "working on backend"
3. **Update last_updated**: Change the date when making significant edits
4. **Use present participles**: "modifying", "adding", "debugging" (not "modify", "add", "debug")
5. **Group related triggers**: If multiple conditions apply to the same work, list them all

## Example Frontmatter

### Authentication Documentation
```yaml
---
summary: NextAuth.js configuration and custom provider implementations
read_when:
  - modifying authentication flows
  - adding new OAuth providers
  - debugging login/logout issues
  - updating session management
last_updated: 2026-01-01
---
```

### Database Schema Documentation
```yaml
---
summary: PostgreSQL schema design and migration strategy
read_when:
  - creating new database tables
  - modifying existing schemas
  - debugging data integrity issues
  - planning database migrations
last_updated: 2026-01-01
---
```

### API Architecture Documentation
```yaml
---
summary: REST API design patterns and endpoint conventions
read_when:
  - creating new API endpoints
  - refactoring API routes
  - reviewing API performance
  - updating API documentation
last_updated: 2026-01-01
---
```

## When to Create Knowledge Documents

Create a knowledge document when:
- You've solved a complex problem and want to preserve the solution
- You've made architectural decisions that need documentation
- You've discovered project-specific patterns or conventions
- You've researched a topic deeply and want to save insights
- You've documented workflows that should be repeatable

## Where NOT to Put Information

- **Active tasks** → Use `.resonance/01_state.md`
- **Lessons learned** → Use `.resonance/02_memory.md`
- **Feature specs** → Knowledge docs are for explaining *how*, not *what to build*
- **Code comments** → Knowledge docs are for context, not inline documentation
