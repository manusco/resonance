# Protocol: Backend Performance & Resource Stewardship

> **Status**: Core Implementation Standard
> **Objective**: Eliminate systemic inefficiencies in the persistence and processing layers.

## 1. Data Access Optimization

*   **N+1 Query Detection**: Aggressively audit loops that perform database queries. Use "Eager Loading" (JOINS) to fetch data in bulk.
*   **Index Strategy**: Ensure all queries in the "Striking Distance" (slow paths) are covered by appropriate indexes.
*   **Connection Management**: Minimize the time database connections are held open.

## 2. Memory & Compute

*   **Stream vs. Buffer**: Favor streams for large data processing to keep memory usage flat.
*   **Resource Leaks**: Check for unclosed handles, event listeners, or growing global state.
*   **Big O Awareness**: Analyze algorithmic complexity for data transformations. Target O(n) or better.

## 3. Caching Latency

*   **Caching Strategy**: Identify expensive, idempotent computations that can be cached (in-memory, Redis).
*   **Cache Invalidation**: Every cached item must have a clear TTL or invalidation trigger.
*   **Throttling/Rate Limiting**: Protect the system from resource depletion.

---
*Created by the Performance agent. Enforcing the Outstanding Skills Standard.*
