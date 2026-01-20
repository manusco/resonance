# Audit Logging Compliance (SOC2)

> "Who did what, when, and from where?"

## 1. The Event Structure

Every critical action needs a log entry.

```json
{
  "timestamp": "2023-01-01T12:00:00Z",
  "actor_id": "user_123",
  "actor_ip": "1.2.3.4",
  "action": "user.deleted",
  "resource_id": "user_456",
  "status": "success",
  "metadata": { "reason": "gdpr_request" }
}
```

## 2. Immutability

Audit logs must be **Append-Only**.
*   **Write**: To dedicated Audit Table or S3 Bucket (Object Lock enabled).
*   **Read**: Admin access only.
*   **Delete**: Forbidden (Retention policy: 1 year).

## 3. Scope

Log these events:
1.  Login/Logout (Success & Fail).
2.  Permission Changes (Role upgrade).
3.  Data Export/Deletion.
4.  API Key Creation.

> 🔴 **Rule**: `console.log` is debugging. `AuditService.log` is compliance. Do not confuse them.
