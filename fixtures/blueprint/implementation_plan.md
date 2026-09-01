# Implementation Plan: Customer ownership service

- Status: APPROVED
- Plan revision: PLAN-CUSTOMER-OWNERSHIP-001
- Approval role: Maintainer group
- Approval evidence: PLAN-APPROVAL-001

## Goal

Move the canonical customer write from the account domain service into a new
customer service.

## Architecture impact

- Creates a new deployable service and cross-service contract.
- Changes the canonical owner and write path for customer records.
- Requires compatibility, failure, rollback, and reconciliation behavior.

## Planned slices

1. Add the new service and contract.
2. Send new writes through the new service.
3. Migrate existing records.
4. Remove the old write path after reconciliation proves parity.

## Verification

- Contract tests cover both service versions during migration.
- Ownership tests prove only the new service accepts canonical writes.
- Reconciliation compares old and new records before removing the old path.
- Rollback restores the old write path without losing accepted writes.
