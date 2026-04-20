# Schema Validation Protocol

> "Data Integrity is not optional."

## 1. The Migration Check

Before applying a migration, validate it.
*   **Tool**: `prisma migrate diff` or equivalent.
*   **Check**: Does this delete columns? Warnings?
*   **Policy**: If `IsDestructive: True`, require manual approval.

## 2. The Drift Detection

Does the Database match the Code?
*   **Command**: `prisma migrate status`.
*   **CI**: Fail if the database has drift (untracked changes).

## 3. The Seeding Verification

A schema is useless without valid data.
*   **Action**: Run `npm run seed` in CI against a fresh container.
*   **Verify**: Ensure Foreign Keys constraints hold.

> 🔴 **Rule**: Never run `db push` in production. Always `migrate deploy`.
