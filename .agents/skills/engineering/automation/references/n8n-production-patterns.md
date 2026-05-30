# n8n Production Integration Patterns

Production-quality automation workflows must be stable, observable, and resilient. This playbook outlines standard structural design patterns, error-handling conventions, and integration strategies in n8n.

---

## 📐 Node Organization & Naming Conventions

Never leave default node names (e.g., `HTTP Request`, `IF`, `Set`). Apply this unified structure to every node:

$$\text{[Category]} - \text{[Action]} \text{ [Context]}$$

### Standard Naming Examples:
*   *Triggers*: `Trigger - Webhook New Lead`
*   *HTTP Requests*: `GET - Clay Enrich Person` / `POST - Slack Notify Channel`
*   *Validations / IFs*: `Check - Email Format Valid` / `Check - Lead Duplicated`
*   *lemlist Nodes*: `lemlist - Add Lead to Campaign`
*   *HubSpot Nodes*: `HubSpot - Upsert Contact`
*   *Slack Alerting*: `Slack - Notify GTM Alerts`
*   *Data Formatting*: `Set - Normalize Lead Payload`

---

## 🛡️ Resilient Error Handling

### 1. The Global Error Trigger Node
Always include a top-level **Error Trigger** node connected to an active alert notifier (Slack is the preferred channel). The failure alert must capture:
- Workflow Name
- Failed Node Name
- Exact Error Message
- n8n Execution ID (for rapid log mapping)
- Timestamp

### 2. HTTP Request Retry Policies
All external HTTP Request nodes calling API endpoints must be configured with a retry policy:
*   **Retry on Fail**: `true`
*   **Max Retries**: `3`
*   **Wait Between Retries**: `1,000ms`
*   **Backoff Policy**: Exponential backoff enabled (where supported)

### 3. Validation Gates
Before performing any write or downstream mutation (CRM insert, campaign add, Slack alerts), insert a validation `IF` or `Filter` node to check for required fields:

```
[Trigger / Data Ingest] ────► [Check - Required Fields Present?]
                                      │
                             ┌────────┴────────┐
                             ▼ (YES)           ▼ (NO)
                     [Perform Action]    [Log - Skip and End]
```

---

## 📈 Observability & Logging Schema

Every production workflow must output telemetry logging data.

### Notion Log Table Schema:
For enterprise audit trails, append workflow statuses directly to a master Notion tracking log:

| Field | Property Type | Value / Purpose |
| :--- | :--- | :--- |
| **Workflow Name** | Title | Name of the executing n8n workflow |
| **Status** | Select | `Success` / `Error` / `Partial` |
| **Record Count In** | Number | Number of source records ingested |
| **Record Count Out** | Number | Number of target records created/mutated |
| **Error Message** | Text | Capture string from failed node catch block |
| **Execution ID** | Text | n8n Execution ID string for tracking |
| **Timestamp** | Date | execution start datetime |

---

## ⛓️ Core Integration Flow Charts

### 1. lemlist Campaign Addition (with Duplication Gate)
```
[Trigger - Lead Input] 
       │
       ▼
[Check - Lead Already in Campaign?] ────► (YES) ────► [Log - Skip Duplicate]
       │
       ▼ (NO)
[lemlist - Add Lead to Campaign] ────► [Log - Lead Added]
```

### 2. HubSpot Upsert Pattern
```
[Input Lead] ────► [HubSpot - Search Contact by Email]
                           │
                  ┌────────┴────────┐
                  ▼ (Exists)        ▼ (New)
          [HubSpot - Update]   [HubSpot - Create]
                  │                 │
                  └────────┬────────┘
                           ▼
          [Set - Store Contact ID] ────► [Log - Sync Success]
```

### 3. Clay Waterfall Email Enrichment
```
[LinkedIn profile URL] ────► [Clay - Find Email via Provider 1]
                                     │
                            ┌────────┴────────┐
                            ▼ (Found)         ▼ (Empty)
                   [HubSpot - Sync Contact]  [Clay - Find Email via Provider 2]
                                                      │
                                             ┌────────┴────────┐
                                             ▼ (Found)         ▼ (Empty)
                                    [HubSpot - Sync]    [Log - No Email, Skip]
```
