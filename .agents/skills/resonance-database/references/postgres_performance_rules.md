# Postgres Performance Rules

> **Objective**: Maintain a high-performance, secure database layer. "Query first, scale later."

## 1. Rule Priorities

| Priority | Category | Impact | Trigger |
| :--- | :--- | :--- | :--- |
| **1** | **Query Performance** | CRITICAL | Slow endpoints / High CPU. |
| **2** | **Connection Mgmt** | CRITICAL | "Too many clients" errors. |
| **3** | **Security (RLS)** | CRITICAL | Multi-tenant data access. |

## 2. Query Performance Guidelines

### ❌ Anti-Patterns
*   **Missing Indexes**: Filtering on a column without an index.
*   **N+1 Queries**: Fetching related data in a loop.
*   **Select ***: Fetching unused columns (bloats network/memory).

### ✅ Best Practices
*   **Index Foreign Keys**: Always index columns used in `JOIN` or `WHERE`.
*   **Partial Indexes**: Index only active rows (`WHERE deleted_at IS NULL`).
*   **GIN for JSONB**: Always use GIN indexes for querying inside JSONB blobs.
*   **Explain Analyze**: Run `EXPLAIN ANALYZE` on any query taking > 100ms.

## 3. Connection Management

### ❌ Anti-Patterns
*   **Direct Connections**: Connecting directly from serverless functions.
*   **Long-lived Transactions**: Keeping potential locks open excessively.

### ✅ Best Practices
*   **Connection Pooling**: Use transaction pooling (Supabase/PgBouncer) for serverless envs.
*   **Short Transactions**: Keep logic inside transactions minimal.

## 4. Security (RLS)

### ✅ Best Practices
*   **Enable RLS**: `ALTER TABLE users ENABLE ROW LEVEL SECURITY;`
*   **Least Privilege**: Users should only see their own data (`auth.uid() = user_id`).
*   **Policy Tests**: Verify policies prevent unauthorized access.
