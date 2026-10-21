# Systems: Architecture Constitution

- Status: APPROVED
- Architecture version: 1.2
- Approval role: Maintainer group
- Approval evidence: ARCH-APPROVAL-001
- Last verified repository revision: 9f00cafe

# Part I: Architecture constitution

## 3. Normative rules

- SYS-101: The account domain service owns account eligibility decisions and canonical account writes.
- SYS-102: Notification state becomes `delivered` only after durable provider delivery evidence. Queue acceptance is `queued`.
- SYS-103: Browser code may request named domain operations but may not call payment providers or coordinate stateful bulk work.

## Verification

- Boundary tests prove browser requests terminate at the domain API.
- Delivery tests cover queue acceptance, provider failure, callback retry, and reconciliation.
