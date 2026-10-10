# Resonance architecture boundary

Resonance is a portable framework for authoring, distributing, composing, and evaluating agent work. A host runs the instructions. An adopter supplies the organization-specific runtime and accountable people. A declaration in a skill or manifest describes intent; it does not grant or enforce a capability.

## Ownership by layer

| Wayfinder layer | Resonance-provided | Host-dependent | Adopter-owned or future |
| --- | --- | --- | --- |
| Interaction and review | Issue templates and review conventions | Chat UI, command discovery, human confirmation surface | Named reviewers, escalation path, shared work queue |
| Knowledge | Portable Markdown skills, references, `.resonance/` templates, ledger formats and local recall tools | Skill loading and project-file access | Organization knowledge sources, access partitions, retention and freshness policy |
| Workflows | Host-run procedure/orchestration skills and typed composition declarations | Dispatch, stage handoffs, persistence supported by a particular host | Business workflow definition, instance state, entry/exit rules, dependencies, value and cost |
| Skills | Canonical source, generated portable files, metadata and eval fixtures | Loading and selecting the files | Adopter changes, approval and deployment of local overrides |
| Policy | Declared authority, side effects, artifact rights and user-approval requirements | Tool permissions and execution-time confirmation, when the host supports them | Identity policy, least-privilege mapping, exception approval and monitoring |
| Evals | Public fixtures, validators, eval runners, evidence and promotion formats | Model invocation, trace access, sandbox and usage telemetry | Protected holdouts, human gold labels, actual business outcomes and data custody |
| Harness and orchestration | Local development/evidence tooling, including the bounded `/goal` loop | Skill invocation and any host agent orchestration | General workflow runtime, durable queue, retries and human handoffs |
| Events and triggers | No event service or scheduler | Host trigger integrations, if available | Event bus, schedule, idempotency, replay, dead-letter handling and trigger health |
| Memory and state | Consumer scaffolds, ledger schema and developer-local goal state | Persistence and project context exposed by the host | Organization records, tenant isolation, retention, live-run memory and correction state |
| Model routing | Routing guidance and routing evaluation | Model selection, credentials, invocation and provider fallback | Model policy, spend authority and organization-level routing requirements |
| Identity, tools and infrastructure | Requirements and declared scopes | Identity and tool boundary only to the extent a host enforces them | Systems of record, network controls, credentials, data isolation, service health and audit retention |
| Observability and outcomes | Evidence formats and local measurement tools | Execution traces, latency and usage data exposed by the host | Production monitoring, attribution to business outcomes and delayed outcome review |

“Adopter-owned or future” does not mean the adopter already has the capability. It identifies work outside this repository. No checked-in adapter currently proves an adopter's identity, permission, isolation, scheduler, queue or business outcome behavior.

## What a compatible adapter must prove

An adapter conformance report should identify the host and adapter version and link to reproducible evidence for each supported capability. A declaration or prompt is not proof.

| Capability | Minimum evidence |
| --- | --- |
| Identity | An authenticated actor and stable run ID bound to the invoked skill/workflow version; distinguish verified identity from submitter-provided metadata. |
| Permissions | Tool-boundary tests showing allowed operations succeed and denied operations are rejected, including the effective capability set for the run. |
| State | A trace showing stage, artifact and approval state across a handoff, plus recovery behavior after interruption or duplicate delivery where supported. |
| Trace | Timestamped invocation and tool events tied to run, host, model/version and artifact digest, with private data redacted or access-controlled. |
| Approval | A durable decision record naming the human actor, requested operation, artifact/version and decision; the host must block the consequential action until approval. |
| Outcome and rollback | A due outcome with its owner and source, plus a tested way to restore the prior artifact or adapter behavior after a failed canary. |

Report unsupported capabilities as unsupported. A successful fixture run does not establish production enforcement, and a framework contract does not make a host permission boundary.

## Skills and business workflows

A skill is a reusable capability: it says what expertise or procedure it supplies, what it may contribute, and how to evaluate it. A business workflow is an owned process with an entry condition, stages, state, external dependencies, approval points, completion condition and expected outcome. A workflow may call skills, but a list of skills or a procedure does not become a durable workflow instance just by being run in chat.

Resonance currently represents skills and some stage/artifact relationships through procedure and orchestration skills plus composition contracts. It does not define or execute general business workflow instances. Keep this distinction explicit when adapting Resonance. Add a first-class workflow artifact only for a named use case that needs durable state or cross-stage control.

## Related guidance

- [Field report and correction proposal lifecycle](FIELD_REPORTS.md)
- [Evidence kernel boundaries](EVIDENCE_KERNEL.md)
- [Eval method and privacy](EVALS.md)
