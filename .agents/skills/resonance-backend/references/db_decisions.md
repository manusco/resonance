# Database Selection Matrix

> "Data gravity is real. Moving DBs is harder than moving code."

## 1. The Decision Tree

```
Where is the compute?
│
├── Edge (Cloudflare/Vercel Edge)
│   ├── Need Relational? → **Turso (LibSQL)** or **Neon (Serverless PG)**
│   └── Need KV/Cache? → **Upstash (Redis)**
│
├── Serverless (Lambda/Vercel Functions)
│   ├── Need Relational? → **Neon** or **Supabase**
│   └── Need NoSQL? → **DynamoDB** or **MongoDB Atlas**
│
└── Long-Running Server (VPS/Docker)
    ├── Standard? → **PostgreSQL** (The default choice)
    └── Simple/Embedded? → **SQLite** (Wal mode)
```

## 2. Verdicts

*   **Default**: **PostgreSQL** (Supabase/Neon). It handles 99% of use cases (Relational, JSON, Vectors).
*   **Local-First**: **SQLite**. Use with Turso for sync.
*   **Vector/AI**: **pgvector** (Keep it in Postgres). Don't add Pinecone unless you hit scale limits.

## 3. ORM Selection

*   **TypeScript**: **Drizzle ORM** (Lightweight, SQL-like) > **Prisma** (Heavy runtime).
*   **Python**: **SQLAlchemy 2.0** or **Prisma Python**.
