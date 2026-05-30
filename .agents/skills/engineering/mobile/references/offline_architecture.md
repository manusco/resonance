# Offline-First Architecture

> The subway test: Can I open the app, read content, and "like" a post while in a tunnel?

## 1. Sync Strategies

### Strategy A: Cache-First (Read-Only Offline)
*   **Best for**: News apps, Social feeds (Consumption).
*   **Data**: `react-query` or `swr` with `persist-client`.
*   **Behavior**: Show stale data instantly. Background revalidate. Gray out "Write" actions.

### Strategy B: Optimistic UI (Write Offline)
*   **Best for**: To-do lists, Chat (Simple mutations).
*   **Data**: Optimistic update -> Queue mutation -> Retry on reconnect.
*   **Risk**: Conflict resolution if server rejects change.

### Strategy C: Local-First (True Offline)
*   **Best for**: Tools, Note-taking, Complex Apps (Production Standard).
*   **Data**: The "Truth" is `SQLite` / `WatermelonDB` / `Realm`.
*   **Sync**: A background service ("Sync Engine") pushes changes to server when possible. Server is just a backup.

## 2. Decision Tree

```
Does the app need to work on a plane?
├── No (Banking, Live Stock) → **Online-Only (Fail gracefully)**
└── Yes
    ├── Read only? → **Cache-First (React Query Persist)**
    └── Read/Write?
        ├── Simple? → **Optimistic UI**
        └── Complex? → **Local-First (SQLite)**
```
