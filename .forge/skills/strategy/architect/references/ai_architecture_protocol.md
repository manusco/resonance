# AI System Boundary Protocol

Use this protocol when an AI subsystem changes the wider system. Architect owns the boundary. AI Engineering owns the subsystem internals.

## Placement

Place the AI subsystem in the C4 context and container views. Name every caller, downstream dependency, human gate, and external model provider.

## Contracts and data ownership

Define the service contract, input and output schemas, source-of-truth owner, retention rule, and failure response. State which system may create, read, modify, approve, or publish each artifact.

## Trust zones

Mark where private data, untrusted content, model output, and consequential actions cross a boundary. Name the validation and approval required at each crossing.

## Cross-system failure

Map timeouts, unavailable providers, malformed model output, stale retrieval data, partial writes, and human-review failure. Give each failure an owner and a safe system response.

## Typed handoff

Hand AI Engineering the approved placement, contracts, data ownership, trust zones, budgets imposed by the wider system, and unresolved subsystem questions. AI Engineering decides model routing, prompting, retrieval, chunking, reranking, agent control, grounding, and AI eval design.

## Completion gate

The boundary is complete when the wider system can fail safely without knowing the AI subsystem's internal implementation, and AI Engineering has enough constraints to design that implementation without redefining system topology.
