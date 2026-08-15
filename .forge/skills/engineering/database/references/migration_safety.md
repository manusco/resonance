# Migration Safety Protocol

> "Data loss is permanent. Code is temporary."

## 1. The Golden Rules

1.  **Backwards Compatible**: The code MUST work with both the OLD and NEW schema.
    *   *Scenario*: Adding `email` column.
    *   *Step 1*: Add column (nullable).
    *   *Step 2*: Deploy Code that writes to it.
    *   *Step 3*: Backfill Data.
    *   *Step 4*: Make column required (Not Null).
2.  **No Locks (Zero Downtime)**:
    *   Do not use invalid PostgreSQL such as `ALTER TABLE ... CONCURRENTLY`.
    *   Create indexes with `CREATE INDEX CONCURRENTLY` when PostgreSQL supports it and the migration tool can run outside a transaction.
    *   Treat table rewrites, backfills, and constraints as staged operations. Add nullable first, backfill in batches, validate, then constrain.

## 2. The Verification

*   **Up**: Deploy the migration.
*   **Down**: Revert the migration. (Does it succeed?)
*   **Cross-Check**: Does the Code crash if the migration hasn't run yet?

> 🔴 **Rule**: Never rename a column. Create new -> Copy -> Drop old.
