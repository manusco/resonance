# Search Evidence and Report Contract

## Evidence bundle

Each scoped property records:

- source and property identifier
- extraction timestamp and timezone
- current and comparison windows
- dimensions and filters
- row limit, returned row count, and `truncated`
- evidence state: `complete`, `partial`, `stale`, `missing`, or `unavailable`
- private artifact reference, not raw rows in the report

Evidence limits are part of the result. A cap, truncation flag, stale extraction, missing property, or failed connector must remain visible through the final disposition. Never translate incomplete evidence into "no issue found."

## Cannibalization evidence

A cannibalization finding requires observations at the joint grain:

```json
{"dimensions": ["query", "page"], "query": "example", "page": "/example", "clicks": 12, "impressions": 320}
```

Query-only and page-only totals cannot establish which pages compete for the same query. Without joint rows, record a candidate and request the right evidence.

## Report contract

Use only the canonical categories:

1. Product Correctness
2. Runtime Safety
3. Authorization Integrity
4. Data Integrity
5. Environment Robustness
6. Verification Quality
7. Maintainability

Use only P0, P1, P2, and P3. Severity reflects harm, not confidence. A suspected high-harm issue with weak proof is a candidate, not a proven finding.

Each finding contains:

- property identifier
- category and severity
- lifecycle state
- evidence reference and observed limit
- user or system harm
- recommended action
- owner role
- verification method

The report also includes coverage, incomplete or skipped properties, rejected candidates worth remembering, approved repository writes, and the next comparison boundary. Store the report privately unless the user approves an exact redacted repository artifact.

Record every contracted property identifier once in `scoped_property_ids`, and
record exactly one matching `property_outcomes` entry for each identifier. A
report with a missing, blank, duplicate, or extra property outcome fails
validation. This is the proof that no scoped property disappeared silently.
