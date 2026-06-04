# Cross-CRM Sync Protocol

> **Goal**: Keep opportunity, account, and customer records aligned across multiple CRMs while preserving ownership, attribution, commission accuracy, and governance. For teams operating with more than one CRM (e.g., different business units, acquired companies, regional instances).

## When You Need This

- Two or more CRMs hold overlapping customer or opportunity data.
- Reps see different pipeline values in different systems.
- Commission or attribution disputes arise from split records.
- An acquisition brought a second CRM that can't be immediately retired.
- Regional teams operate on different CRM instances with shared enterprise accounts.

If you have one CRM with clean data, you do not need this protocol. Fix your single-CRM hygiene first (see [CRM Operations Protocol](crm_operations_protocol.md)).

---

## 1. Architecture — The Sync Model

```
CRM A (Source for Segment X)
  ↕  event-driven sync
Master Customer Record (Golden Record)
  ↕  event-driven sync
CRM B (Source for Segment Y)
```

**Iron Rule**: Every sync has exactly one source of truth per field. If two CRMs can both write the same field, you will have conflicts within a week.

### Field Ownership Map

Before writing a single line of sync logic, build this map:

| Field | Source CRM | Direction | Conflict Resolution |
|:---|:---|:---|:---|
| Account name | CRM A | A → B | Source wins |
| Opportunity amount | Owning CRM | Bidirectional | Most recent update wins, flag for review |
| Contact email | CRM A | A → B | Source wins |
| Deal stage | Owning CRM | Bidirectional | Higher stage wins (no backward movement without flag) |
| Owner | Owning CRM | No sync | Each CRM maintains its own ownership |
| Commission split | Neither | Manual only | Never auto-sync commission data |

**Rule**: If a field is not in this map, it does not sync. Unmapped fields are the #1 source of data corruption in cross-CRM setups.

---

## 2. Record Matching

### Match Key Strategy

| Priority | Match Key | Confidence |
|:---|:---|:---|
| 1 | External ID (shared customer ID, ERP ID) | High |
| 2 | Email domain + company name (normalized) | Medium |
| 3 | Fuzzy match (company name similarity + location) | Low — requires human review |

**Hard Rules**:
- Never auto-merge on fuzzy matches. Route to human review.
- Log every match decision with the match key used, confidence level, and timestamp.
- Build a "no-match" queue for records that can't be confidently paired. Review weekly.

### Deduplication Across CRMs

When both CRMs have a record for the same entity:
1. Determine which CRM is the source of truth for that entity's segment.
2. Merge field-by-field according to the Field Ownership Map.
3. Preserve both CRM record IDs as cross-references.
4. Log the merge with before/after state for audit.

---

## 3. Sync Patterns

### Event-Driven Sync (Recommended)

Trigger a sync when a record changes, not on a schedule. This minimizes task volume and ensures near-real-time consistency.

```
Record updated in CRM A
  → Webhook fires
  → Sync service reads the changed fields
  → Checks Field Ownership Map
  → Writes only owned fields to CRM B
  → Logs the sync event
```

**Advantages**: Low task volume, near-real-time, auditable.
**Disadvantage**: Requires webhook support from both CRMs.

### Scheduled Reconciliation (Fallback)

Run a daily or weekly reconciliation job that compares records across both CRMs and flags discrepancies.

| Discrepancy Type | Action |
|:---|:---|
| Field value mismatch on source-owned field | Auto-correct to source value, log |
| Field value mismatch on bidirectional field | Flag for human review |
| Record exists in A but not B | Create in B if it matches the sync filter |
| Record exists in B but not A | Flag for review (possible deletion or segment mismatch) |

**Warning**: Scheduled full-table syncs at short intervals (every 5 minutes) will generate hundreds of unnecessary operations per day. Use event-driven for real-time, scheduled for catch-up only.

---

## 4. Conflict Resolution

### The Conflict Taxonomy

| Conflict Type | Example | Resolution |
|:---|:---|:---|
| **Value conflict** | Amount is $50K in CRM A, $45K in CRM B | Source-owned field: source wins. Bidirectional: most recent wins, flag for review. |
| **Stage conflict** | Deal is "Proposal" in A, "Negotiation" in B | Higher stage wins (stages only move forward). Backward movement requires human approval. |
| **Owner conflict** | Different reps own the same account in each CRM | Never auto-resolve. Flag for sales ops review. |
| **Existence conflict** | Record deleted in A but still active in B | Do not auto-delete. Flag for review. Deletion requires human approval. |
| **Attribution conflict** | Different first-touch sources in each CRM | Preserve both. Let the attribution model reconcile. Never overwrite source data. |

### Conflict Queue

Every unresolved conflict goes into a queue with:
- Record IDs from both CRMs
- Conflicting field values
- Conflict type
- Timestamp of detection
- Recommended resolution
- Status: Open / Resolved / Escalated

Review the conflict queue daily until stable, then weekly.

---

## 5. Governance

### Sandbox-to-Production Promotion

Never deploy a new sync rule directly to production.

1. **Sandbox**: Test the sync rule with 50-100 sample records.
2. **Validate**: Compare synced records against expected values.
3. **Dry-run**: Run the rule in production with logging only, no writes.
4. **Promote**: Enable writes after human review of dry-run results.

### Audit Trail

Every sync event must log:
- Source CRM and record ID
- Target CRM and record ID
- Fields changed (before and after values)
- Match key used
- Sync timestamp
- Operator or automation that triggered the sync

### Revenue-Touching Workflows

Any sync that affects:
- Deal amounts
- Close dates
- Commission splits
- Forecast categories
- Pipeline stage

...requires a separate approval gate before production writes. Revenue data corruption is the fastest way to lose sales team trust in the system.

---

## 6. Common Failures

| Failure | Symptom | Root Cause | Fix |
|:---|:---|:---|:---|
| Duplicate records multiply | Same account appears 3-4 times across systems | No match key strategy, fuzzy matches auto-merging | Implement match key hierarchy, require human review for fuzzy |
| Pipeline double-counting | Forecast shows 2x the real pipeline | Same opportunity exists in both CRMs | Designate one CRM as the pipeline source of truth per segment |
| Attribution wars | Marketing and sales disagree on source | Different CRMs track different first-touch events | Preserve both, reconcile in a shared attribution model |
| Ghost records | Records deleted in one CRM reappear | Sync recreates deleted records from the other CRM | Add a "sync-deleted" flag instead of hard-deleting |
| Commission disputes | Reps in different CRMs claim the same deal | No clear ownership model for shared accounts | Build an explicit ownership map per account, enforce in both CRMs |

---

## 7. When to Consolidate

Cross-CRM sync is a bridge, not a destination. If you find yourself maintaining sync rules for more than 18 months, evaluate consolidation:

- **Cost test**: Is the sync maintenance cheaper than migrating to one CRM? (Include engineer time, conflict resolution time, and data quality costs.)
- **Complexity test**: Can a new hire understand the sync logic in under 30 minutes?
- **Trust test**: Do sales teams trust the data in both CRMs? If not, one of them is already dead weight.

If two of three tests fail, start planning the migration.
