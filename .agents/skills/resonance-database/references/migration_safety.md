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
    *   Avoid `ALTER TABLE` on large tables without `CONCURRENTLY`.
    *   Create Indexes `CONCURRENTLY`.

## 2. The Verification

*   **Up**: Deploy the migration.
*   **Down**: Revert the migration. (Does it succeed?)
*   **Cross-Check**: Does the Code crash if the migration hasn't run yet?

> 🔴 **Rule**: Never rename a column. Create new -> Copy -> Drop old.
