# Protocol: API Handoff (Backend -> Frontend)
> **Objective**: Eliminate "What's the payload?" questions.
> **Constraint**: This document MUST be produced before the ticket is moved to "Ready for Frontend".

## 1. The Handoff Logic
Do not dump code. Dump **Contracts**.
The frontend engineer does not care about your ORM or Database Schema. They care about:
1.  **The URL** (Route)
2.  **The Payload** (JSON Request/Response)
3.  **The Edge Cases** (Errors)

---

## 2. The Handoff Template

```markdown
# API Handoff: [Feature Name]

## 1. Business Context
*Briefly explain what this feature does and who it's for.*

## 2. Endpoints

### [METHOD] /api/v1/path/to/resource
*   **Auth Scope**: `user` | `admin` | `public`
*   **Purpose**: Creates a new resource.

#### Request (Body)
```json
{
  "name": "string (required, max 50 chars)",
  "type": "enum ('active' | 'pending')",
  "settings": {
    "notifications": "boolean"
  }
}
```

#### Response (200 OK)
```json
{
  "id": "uuid",
  "name": "string",
  "status": "active",
  "created_at": "ISO-8601 string"
}
```

#### Errors
| Code | Reason | Message (User Facing) |
| :--- | :--- | :--- |
| 400 | Validation | "Name is too long" |
| 403 | Permissions | "You must be an admin" |
| 409 | Conflict | "Resource already exists" |

## 3. Validation Rules (Frontend Mirror)
*These rules must be enforced in the UI form.*
*   `name`: Min 3, Max 50 chars. Rename allowed only once per day.
*   `type`: Cannot change from 'active' to 'pending'.

## 4. Enums & Constants
```typescript
// Copy this into your frontend types
export enum ResourceType {
  ACTIVE = 'active',
  PENDING = 'pending',
  ARCHIVED = 'archived'
}
```

## 5. Integration Notes / Gotchas
*   ⚠️ **Latency**: This endpoint triggers an external AI call, expect 2-3s latency. Show a skeleton loader.
*   ⚠️ **Optimistic Updates**: Safe to do.
```
